"""R0 — gemeenschappelijke engine voor catalogusregels (ENGINE_TEMPLATE.md). Dagdata (data/daily), één kostenmodel, identieke output.

Een regel = module catalogus/<id>.py met RULE = {id, naam, familie, mechanisme, bron, instrumenten, varianten{naam: params}, ...}
en een functie positions(df, params) -> np.array posities in [-1, 1] per dag, bepaald met informatie t/m het slot van dag t en
aangehouden van slot t tot slot t+1 (geen lookahead; de engine verschuift niets zelf, de regel levert pos[t] = positie ná slot t).

Gebruik: python -m engine.run_rule <regel-id> [--reserve]   (reserve-OOS 2025-01→ alleen met --reserve, één keer per regel, wordt gelogd)
"""
import csv
import importlib
import math
import os
import sys
from datetime import date

import numpy as np

DISCOVERY_END = date(2024, 12, 31)
RESERVE_START = date(2025, 1, 1)
TRIALS = "catalogus/TRIALS.csv"
# D2-reeks → FTMO-instrument voor kosten (COSTS_FTMO.csv) en swap
COST_MAP = {"SPX": "US500cash", "SPY": "US500cash", "NDX": "US100cash", "NASDAQ_COMP": "US100cash", "DJI": "US30cash", "DAX": "GER40cash",
            "GOLD_F": "XAUUSD", "SILVER_F": "XAGUSD", "WTI_F": "USOILcash", "EURUSD": "EURUSD", "GBPUSD": "GBPUSD", "USDJPY": "USDJPY",
            "FTSE": "UK100cash", "N225": "JP225cash", "STOXX50": "EU50cash", "CAC40": "FRA40cash", "HSI": "HK50cash", "RUT": "US2000cash"}
EXTRA_RT_BP = {"UK100cash": 3.88, "JP225cash": 1.78, "EU50cash": 3.12, "FRA40cash": 1.37, "HK50cash": 2.35, "US2000cash": 2.12}  # S0-live / U1


# ---------- data ----------
def load_daily(name, field="adjclose"):
    d, o, h, l, c = [], [], [], [], []
    for line in open(f"data/daily/{name}.csv"):
        if not line[:1].isdigit():
            continue
        f = line.rstrip("\n").split(";")
        px = float(f[5] if field == "adjclose" and f[5] else f[4])
        k = px / float(f[4]) if f[4] and float(f[4]) else 1.0  # OHLC op dezelfde (adj-)schaal
        d.append(date.fromisoformat(f[0]))
        o.append(float(f[1]) * k if f[1] else np.nan); h.append(float(f[2]) * k if f[2] else np.nan)
        l.append(float(f[3]) * k if f[3] else np.nan); c.append(px)
    return {"date": np.array(d), "open": np.array(o), "high": np.array(h), "low": np.array(l), "close": np.array(c), "name": name}


# ---------- kostenmodel (één plek) ----------
def _costs():
    rt, swl, sws = {}, {}, {}
    for r in csv.DictReader((l for l in open("COSTS_FTMO.csv") if not l.startswith("#")), delimiter=";"):
        rt[r["symbol"]] = float(r["roundtrip_intraday_bp"]); swl[r["symbol"]] = float(r["swap_long_bp_per_nacht"]); sws[r["symbol"]] = float(r["swap_short_bp_per_nacht"])
    for k, v in EXTRA_RT_BP.items():
        rt.setdefault(k, v); swl.setdefault(k, 2.0); sws.setdefault(k, 0.5)  # swap onbekend → indexgemiddelde (vermeld)
    return rt, swl, sws


RT, SWL, SWS = _costs()


def net_returns(df, pos, spread_mult=1.0):
    """dagelijks netto rendement per eenheid notional: pos[t-1] × r[t] − kosten bij positiewijziging − swap per kalendernacht."""
    inst = COST_MAP.get(df["name"])
    if inst is None:
        raise KeyError(f"geen kostenmapping voor {df['name']}")
    c = df["close"]; r = np.r_[0.0, c[1:] / c[:-1] - 1]
    p_prev = np.r_[0.0, pos[:-1]]
    turn = np.abs(np.diff(np.r_[0.0, pos]))                      # wijziging op slot t
    cost = turn * (RT[inst] / 2) * 1e-4 * spread_mult            # halve rondreis per eenheid wijziging
    nights = np.r_[0, [(b - a).days for a, b in zip(df["date"][:-1], df["date"][1:])]]
    swap = np.where(p_prev > 0, p_prev * SWL[inst], -p_prev * SWS[inst]) * nights * 1e-4
    return p_prev * r - cost - swap, turn


# ---------- statistiek ----------
def t_plain(x):
    x = np.asarray(x, float); return x.mean() / x.std(ddof=1) * math.sqrt(len(x)) if len(x) > 2 and x.std() > 0 else float("nan")


def t_nw(x, L=5):
    x = np.asarray(x, float); n = len(x); e = x - x.mean(); s = e @ e / n
    s += 2 * sum((1 - k / (L + 1)) * (e[k:] @ e[:-k] / n) for k in range(1, L + 1))
    return x.mean() / math.sqrt(s / n) if s > 0 else float("nan")


def boot(x, B=1000, blk=21, seed=7):
    x = np.asarray(x, float); n = len(x); rng = np.random.default_rng(seed); m, s = [], []
    for _ in range(B):
        st = rng.integers(0, n, n // blk + 1); idx = ((st[:, None] + np.arange(blk)).ravel() % n)[:n]
        y = x[idx]; m.append(y.mean()); s.append(y.mean() / y.std() * math.sqrt(252) if y.std() > 0 else 0)
    return x.mean() / np.std(m, ddof=1), np.percentile(s, [5, 95])


def p_one_sided(t):
    return 0.5 * math.erfc(t / math.sqrt(2)) if np.isfinite(t) else 1.0


def bh_q(ps):
    ps = np.asarray(ps, float); n = len(ps); o = np.argsort(ps); q = np.empty(n)
    run = 1.0
    for rank, i in reversed(list(enumerate(o, 1))):
        run = min(run, ps[i] * n / rank); q[i] = run
    return q


def load_sleeve(path):
    out, prev = {}, None
    for x in csv.DictReader(open(path), delimiter=";"):
        e = float(x["end_equity"]); p = prev or float(x["start_balance"])
        out[date(*map(int, x["date"].split(".")))] = e / p - 1; prev = e
    return out


# ---------- hoofdpijplijn ----------
def run(rule_id, reserve=False):
    mod = importlib.import_module(f"catalogus.{rule_id}")
    R = mod.RULE
    out_dir = f"results/R/{rule_id}"; os.makedirs(out_dir, exist_ok=True)
    data = {n: load_daily(n, R.get("field", "adjclose")) for n in R["instrumenten"]}
    spx = load_daily("SPX", "close")
    spx_r = dict(zip(spx["date"][1:], spx["close"][1:] / spx["close"][:-1] - 1))
    sma = {d: np.mean(spx["close"][max(0, i - 199):i + 1]) for i, d in enumerate(spx["date"]) if i >= 199}
    spx_bull = {d: bool(spx["close"][i] > sma[d]) for i, d in enumerate(spx["date"]) if d in sma}
    sleeves = {k: load_sleeve(p) for k, p in (("ORB", "results/f/F2_ORB_daily.csv"), ("RSI2", "results/f/F1_RSI2_swapcorr_daily.csv")) if os.path.exists(p)}
    lines = [f"# {R['id']} — {R['naam']} ({R['familie']})", f"Mechanisme: {R['mechanisme']}", f"Bron: {R['bron']}", ""]
    rows = []
    for vname, params in R["varianten"].items():
        port, port50, ntr = {}, {}, 0
        per_inst = {}
        for n, df in data.items():
            pos = np.clip(np.asarray(mod.positions(df, params), float), -1, 1)
            for mult, tgt in ((1.0, port), (1.5, port50)):
                net, turn = net_returns(df, pos, mult)
                keep = [(d, v) for d, v in zip(df["date"], net) if (d >= RESERVE_START) == reserve and d.year >= R.get("start_jaar", 1900)]
                for d, v in keep:
                    tgt.setdefault(d, []).append(v)
                if mult == 1.0:
                    sel = np.array([(d >= RESERVE_START) == reserve for d in df["date"]])
                    ntr += int((turn[sel] > 0).sum()); per_inst[n] = np.array([v for _, v in keep])
        days = sorted(port)
        x = np.array([np.mean(port[d]) for d in days]); x50 = np.array([np.mean(port50[d]) for d in days])
        gross_turn_days = len(days)
        sr = x.mean() / x.std() * math.sqrt(252) if x.std() > 0 else float("nan")
        tb, sr_ci = boot(x)
        h = len(x) // 2
        eq = np.cumprod(1 + x); dd = float(np.max(1 - eq / np.maximum.accumulate(eq)))
        sk = float(((x - x.mean()) ** 3).mean() / x.std() ** 3) if x.std() > 0 else float("nan")
        yr = {}
        for d, v in zip(days, x):
            yr.setdefault(d.year, []).append(v)
        vol20 = {}
        corr = {}
        for k, s in sleeves.items():
            cd = [d for d in days if d in s]
            corr[k] = float(np.corrcoef([x[days.index(d)] for d in cd], [s[d] for d in cd])[0, 1]) if len(cd) > 50 else float("nan")
        bull = [v for d, v in zip(days, x) if spx_bull.get(d) is True]; bear = [v for d, v in zip(days, x) if spx_bull.get(d) is False]
        t_day = t_plain(x); t_n = t_nw(x)
        res = {"variant": vname, "dagen": len(x), "trades": ntr, "netto_bp_dag": x.mean() * 1e4, "SR": sr, "SR_CI90": sr_ci,
               "t_dag": t_day, "t_NW": t_n, "t_boot": tb, "t_H1": t_plain(x[:h]), "t_H2": t_plain(x[h:]), "t_50pct_spread": t_nw(x50),
               "skew": sk, "max_dagverlies": float(-x.min()), "P99_dagverlies": float(-np.percentile(x, 1)), "maxDD": dd,
               "corr": corr, "bull_bp": np.mean(bull) * 1e4 if bull else float("nan"), "bear_bp": np.mean(bear) * 1e4 if bear else float("nan"),
               "per_jaar": {y: float(np.sum(v)) for y, v in sorted(yr.items())},
               "per_instrument_t": {n: t_plain(v) for n, v in per_inst.items()}}
        rows.append(res)
        t_gate = min(res["t_NW"], res["t_boot"])
        gate = (t_gate >= 3 and res["t_H1"] > 0 and res["t_H2"] > 0 and (ntr >= 500 or R.get("events", False) and ntr >= 100))
        with open(TRIALS, "a") as f:
            f.write(f"{date.today()};{R['id']};{vname};{R.get('dataset', 'D2')};{'reserve' if reserve else 'ontdekking'};"
                    f"{sr:.3f};{t_gate:.3f};{p_one_sided(t_gate):.6f};;{'door G-ontdekking' if gate else 'afgewezen'}\n")
        lines += [f"## variant {vname} {params}",
                  f"- {'RESERVE 2025-01→' if reserve else 'ontdekking ≤ 2024'}: {len(x)} dagen, {ntr} positie-wijzigingen, netto {x.mean()*1e4:+.2f} bp/dag, SR {sr:+.2f} (90%-CI {sr_ci[0]:+.2f}…{sr_ci[1]:+.2f})",
                  f"- t: dag {t_day:+.2f} | Newey-West {t_n:+.2f} | blok-bootstrap {tb:+.2f} | H1 {res['t_H1']:+.2f} | H2 {res['t_H2']:+.2f} | +50% spread (NW) {res['t_50pct_spread']:+.2f}",
                  f"- skew {sk:+.2f} | max dagverlies {res['max_dagverlies']*100:.2f}% (P99 {res['P99_dagverlies']*100:.2f}%) | maxDD {dd*100:.1f}% (1× notional)",
                  f"- corr: " + ", ".join(f"{k} {v:+.2f}" for k, v in corr.items()) + f" | SPX > SMA200: {res['bull_bp']:+.2f} bp/dag, daaronder {res['bear_bp']:+.2f}",
                  "- per instrument t: " + ", ".join(f"{k} {v:+.2f}" for k, v in res["per_instrument_t"].items()),
                  "- per jaar (%): " + " ".join(f"{y}:{v*100:+.1f}" for y, v in res["per_jaar"].items()),
                  f"- G-ontdekking (min(NW, bootstrap) ≥ 3, beide helften +, N ≥ 500): {'DOOR' if gate else 'afgewezen'}", ""]
    recompute_fdr()
    open(f"{out_dir}/{'reserve' if reserve else 'ontdekking'}.md", "w").write("\n".join(lines))
    print("\n".join(lines))
    return rows


def recompute_fdr():
    rows = list(csv.reader(open(TRIALS), delimiter=";"))
    hdr, body = rows[0], rows[1:]
    ps = [float(r[7]) if r[7] else 1.0 for r in body]
    q = bh_q(ps) if body else []
    for r, qq in zip(body, q):
        r[8] = f"{qq:.4f}"
    with open(TRIALS, "w", newline="") as f:
        csv.writer(f, delimiter=";").writerows([hdr] + body)


if __name__ == "__main__":
    if not os.path.exists(TRIALS):
        os.makedirs("catalogus", exist_ok=True)
        open(TRIALS, "w").write("datum;regel_id;variant;dataset;fase;netto_SR;t_geclusterd;p;FDR_q;beslissing\n")
    run(sys.argv[1], reserve="--reserve" in sys.argv)
