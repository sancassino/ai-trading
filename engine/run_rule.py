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
            "FX_EURUSD": "EURUSD", "FX_GBPUSD": "GBPUSD", "FX_USDJPY": "USDJPY", "FX_AUDUSD": "AUDUSD", "FX_USDCAD": "USDCAD",
            "FX_USDCHF": "USDCHF", "FX_NZDUSD": "NZDUSD",
            "FTSE": "UK100cash", "N225": "JP225cash", "STOXX50": "EU50cash", "CAC40": "FRA40cash", "HSI": "HK50cash", "RUT": "US2000cash"}
EXTRA_RT_BP = {"UK100cash": 3.88, "JP225cash": 1.78, "EU50cash": 3.12, "FRA40cash": 1.37, "HK50cash": 2.35, "US2000cash": 2.12}  # S0-live / U1


# ---------- data ----------
def load_daily(name, field="adjclose"):
    d, o, h, l, c = [], [], [], [], []
    path = next((p for p in (f"data/daily/{name}.csv", f"data/derived/{name}.csv", f"data/yahoo/{name}.csv") if os.path.exists(p)))
    for line in open(path):
        if not line[:1].isdigit():
            continue
        f = line.rstrip("\n").replace(".", "-", 2).split(";") if path.startswith("data/yahoo") else line.rstrip("\n").split(";")
        if path.startswith("data/yahoo"):  # R2: alleen datum;close (adjusted) → OHLC = close
            f = [f[0], f[1], f[1], f[1], f[1], f[1], "0"]
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
RATE_ID = {"USD": "IR3TIB01USM156N", "EUR": "IR3TIB01EZM156N", "GBP": "IR3TIB01GBM156N", "JPY": "IR3TIB01JPM156N", "AUD": "IR3TIB01AUM156N",
           "CAD": "IR3TIB01CAM156N", "CHF": "IR3TIB01CHM156N", "NZD": "IR3TIB01NZM156N"}
_RATES = {}


def rate_series(ccy):
    """3m-interbankrente (%/jr), maandelijks → per datum (laatste bekende maand; publicatie ≈ 1 mnd later → 1 maand vertraging)."""
    if ccy not in _RATES:
        pts = []
        for line in open(f"data/fred/{RATE_ID[ccy]}.csv"):
            f = line.strip().split(",")
            if f[0][:1].isdigit() and f[1] not in ("", "."):
                y, m, _ = map(int, f[0].split("-")); m += 1
                if m > 12:
                    y, m = y + 1, 1
                pts.append((date(y, m, 1), float(f[1])))
        _RATES[ccy] = pts
    return _RATES[ccy]


def rate_on(ccy, dates):
    pts = rate_series(ccy); ks = [p[0] for p in pts]; import bisect
    out = np.full(len(dates), np.nan)
    for i, d in enumerate(dates):
        j = bisect.bisect_right(ks, d) - 1
        if j >= 0:
            out[i] = pts[j][1]
    return out


def _fx_markup(inst):
    # FTMO: long_pct = diff − m, short_pct = −diff − m → m = −(long_pct + short_pct)/2 (in %/jr); uit swap-bp per nacht terugrekenen
    lp, sp = -SWL[inst] * 365 / 100, -SWS[inst] * 365 / 100      # SWL/SWS zijn kosten-bp → ontvangst-%/jr
    return -(lp + sp) / 2


def financing(df, inst, p_prev, nights):
    """financieringskosten per dag (fractie). FX: historisch renteverschil − opslag (opslag geijkt op FTMO-specs van nu);
    overige: huidige FTMO-swap in bp per nacht, constant (sjabloon-aanname, vermeld)."""
    if df["name"].startswith("FX_"):
        base, quote = df["name"][3:6], df["name"][6:9]
        diff = rate_on(base, df["date"]) - rate_on(quote, df["date"])          # %/jr, NaN als een rente ontbreekt
        m = _fx_markup(inst)
        recv = np.where(p_prev > 0, p_prev * (diff - m), -p_prev * (-diff - m))  # ontvangst in %/jr
        return -recv / 100 / 365 * nights
    return np.where(p_prev > 0, p_prev * SWL[inst], -p_prev * SWS[inst]) * nights * 1e-4


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
    swap = financing(df, inst, p_prev, nights)
    gross = p_prev * r
    return gross - cost - swap, turn, gross, cost, swap


# ---------- vehikels (D-038) ----------
VEHICLE_DEFAULT = {  # rt_bp = rondreis per eenheid wijziging; ter = %/jr op |positie|; short/cash/financiering-semantiek
    "cfd": {"rt_bp": None, "ter": 0.0, "short": True, "cash_rate": False, "model": "cfd"},
    "etf": {"rt_bp": 13.0, "ter": 0.07, "short": False, "cash_rate": True, "model": "etf"},   # VEHICLE_ANALYSE v1: 0,05%/kant commissie + ≈ 3 bp spread; TER 0,07%
    "future": {"rt_bp": 1.0, "ter": 0.0, "short": True, "cash_rate": True, "model": "future", "roll_bp": 0.5, "rolls": 4},
    # D-047 (R2): retail-CFD = future-semantiek (spot + carry/benchmark-financiering) − fee% × |notional| (beide kanten) − spread (S0 × s0mult; onbekend → 3 bp)
    # R4 (C61): inverse-ETF (dagelijks gereset, swap): short toegestaan, TER 0,50% op het short-deel; totaal = p·r + rf·(1 − lang-deel) (kapitaal verdient rf, lang deel is belegd)
    "etf_inverse": {"rt_bp": 13.0, "ter": 0.07, "ter_short": 0.50, "short": True, "cash_rate": True, "model": "etf", "inverse": True},
    "cfd_retail": {"rt_bp": None, "ter": 0.0, "short": True, "cash_rate": True, "model": "future", "roll_bp": 0.0, "rolls": 0, "fee_pct": 1.5, "s0mult": 1.0},
    "cfd_retail_hi": {"rt_bp": None, "ter": 0.0, "short": True, "cash_rate": True, "model": "future", "roll_bp": 0.0, "rolls": 0, "fee_pct": 2.5, "s0mult": 2.0},
}


def vehicles():
    v = {k: dict(x) for k, x in VEHICLE_DEFAULT.items()}
    if os.path.exists("engine/vehicles.csv"):
        for r in csv.DictReader(open("engine/vehicles.csv"), delimiter=";"):
            v.setdefault(r["vehicle"], {}).update({k: (float(x) if k in ("rt_bp", "ter", "roll_bp", "rolls") and x else x) for k, x in r.items() if k != "vehicle" and x})
    return v


TR_PROXY = {"SPX": "SPX_TR"}   # DAX = performance-index (al total return); overige: prijsindex (dividend genegeerd, vermeld)
_RF = None


def rf_on(dates):
    """risicovrije rente (%/jr) = FRED DTB3 (dagelijks), laatste bekende waarde."""
    global _RF
    if _RF is None:
        pts = [(date.fromisoformat(l.split(",")[0]), float(l.split(",")[1])) for l in open("data/fred/DTB3.csv")
               if l[:1].isdigit() and l.split(",")[1].strip() not in ("", ".")]
        # FRED is vanaf onze IP's geblokkeerd: na de laatste DTB3-datum doorlopen met US Treasury 3m (data/daily/YLD_US3M.csv, officieel)
        if os.path.exists("data/daily/YLD_US3M.csv") and pts:
            last = pts[-1][0]
            pts += [(date.fromisoformat(l.split(";")[0]), float(l.split(";")[4])) for l in open("data/daily/YLD_US3M.csv")
                    if l[:1].isdigit() and date.fromisoformat(l.split(";")[0]) > last]
        _RF = ([p[0] for p in pts], [p[1] for p in pts])
    import bisect
    ks, vs = _RF
    return np.array([vs[max(0, bisect.bisect_right(ks, d) - 1)] for d in dates])


def net_returns_vehicle(df, pos, spread_mult, veh, cap=True):
    """netto dagrendement van het kapitaal per vehikel. cfd = net_returns; etf = long-only, TER, cash-rente op niet-belegd;
    future = positie × (rendement − rf) + rf op het kapitaal, rol- en handelskosten."""
    V = vehicles()[veh]
    if V["model"] == "cfd":
        if COST_MAP.get(df["name"]) is None:   # R2: geen CFD-kosten bekend (bv. synthetische obligatie, koper) → niet in het CFD-universum
            nan = np.full(len(pos), np.nan); return nan, np.zeros(len(pos)), nan, nan, nan
        return net_returns(df, pos, spread_mult)
    if df["name"].startswith("FX_") and V["model"] == "etf":
        nan = np.full(len(pos), np.nan); return nan, np.zeros(len(pos)), nan, nan, nan
    if not V["short"]:
        pos = np.maximum(pos, 0.0)
    c = df["close"]; r = np.r_[0.0, c[1:] / c[:-1] - 1]
    tr = TR_PROXY.get(df["name"])
    if tr and os.path.exists(f"data/daily/{tr}.csv"):     # total return i.p.v. prijsindex waar beschikbaar (ETF acc / future)
        t = load_daily(tr, "adjclose"); tmap = dict(zip(t["date"], t["close"]))
        for i in range(1, len(c)):
            a, b = tmap.get(df["date"][i - 1]), tmap.get(df["date"][i])
            if a and b:
                r[i] = b / a - 1
    p_prev = np.r_[0.0, pos[:-1]]
    turn = np.abs(np.diff(np.r_[0.0, pos]))
    rtbp = V["rt_bp"] if V["rt_bp"] is not None else RT.get(COST_MAP.get(df["name"]), 3.0) * V.get("s0mult", 1.0)
    cost = turn * (rtbp / 2) * 1e-4 * spread_mult
    nights = np.r_[0, [(b - a).days for a, b in zip(df["date"][:-1], df["date"][1:])]]
    rf = rf_on(df["date"]) / 100 / 365 * nights
    ter = np.abs(p_prev) * V["ter"] / 100 / 365 * nights
    if V.get("inverse"):
        ter = (np.maximum(p_prev, 0) * V["ter"] + np.maximum(-p_prev, 0) * V["ter_short"]) / 100 / 365 * nights
    if V["model"] == "etf":
        gross = p_prev * r
        cash = np.clip(1 - (np.maximum(p_prev, 0) if V.get("inverse") else np.abs(p_prev)), 0, 1) * rf if (V["cash_rate"] and cap) else 0.0   # cap=False: kasrente op portefeuilleniveau (aggregatie 'som')
        fin = ter - cash
    else:  # future: overschotrendement + rente op het volledige kapitaal
        nm = df["name"]
        fxc = len(nm) == 6 and nm.isalpha() and nm.isupper()      # R3: kruisen als EURGBP (Yahoo =X)
        if nm.startswith("FX_") or fxc:      # R2-fix: FX-future verdient het renteverschil (base − quote) bovenop spot; geen −rf
            b0 = 3 if nm.startswith("FX_") else 0
            diff = (rate_on(nm[b0:b0 + 3], df["date"]) - rate_on(nm[b0 + 3:b0 + 6], df["date"])) / 100 / 365 * nights
            gross = p_prev * (r + diff)
        elif nm.endswith("_F"):       # R2-fix: doorlopende futures-prijsreeks is al overschotrendement (rol/carry zit in de prijs) → geen −rf
            gross = p_prev * r
        else:                         # index/obligatie (adjclose = total return): overschot = r − rf
            gross = p_prev * (r - rf)
        roll = np.abs(p_prev) * V.get("roll_bp", 0.5) * V.get("rolls", 4) * 1e-4 / 365 * nights
        roll = roll + np.abs(p_prev) * V.get("fee_pct", 0.0) / 100 / 365 * nights          # cfd_retail: financieringsopslag op |notional|
        fin = roll - (rf if cap else 0.0)
    return gross - cost - fin, turn, gross, cost, fin


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
def run(rule_id, reserve=False, vehicle=None):
    mod = importlib.import_module(f"catalogus.{rule_id}")
    R = mod.RULE
    veh = vehicle or R.get("vehicle", "cfd")
    out_dir = f"results/R/{rule_id}"; os.makedirs(out_dir, exist_ok=True)
    data = {n: load_daily(n, R.get("field", "adjclose")) for n in R["instrumenten"]}
    spx = load_daily("SPX", "close")
    spx_r = dict(zip(spx["date"][1:], spx["close"][1:] / spx["close"][:-1] - 1))
    sma = {d: np.mean(spx["close"][max(0, i - 199):i + 1]) for i, d in enumerate(spx["date"]) if i >= 199}
    spx_bull = {d: bool(spx["close"][i] > sma[d]) for i, d in enumerate(spx["date"]) if d in sma}
    sleeves = {k: load_sleeve(p) for k, p in (("ORB", "results/f/F2_ORB_daily.csv"), ("RSI2", "results/f/F1_RSI2_swapcorr_daily.csv")) if os.path.exists(p)}
    lines = [f"# {R['id']} — {R['naam']} ({R['familie']})", f"Mechanisme: {R['mechanisme']}", f"Bron: {R['bron']}", ""]
    rows = []
    mode = R.get("aggregatie", "gemiddelde"); cap = mode != "som"

    def make_bh(bench, sj, bsum):
        """G-benchmark (D-038): buy-and-hold, zelfde vehikel. Standaard gelijk gewogen over de regel-instrumenten;
        R["benchmark"] = {"naam":..., "gewichten": {instrument: w}} (vast, dagelijks herwogen) voor allocatieregels (R2); per variant te overschrijven."""
        bdata = {n: (data[n] if n in data else load_daily(n, R.get("field", "adjclose"))) for n in bench["gewichten"]}
        bh, bh_abs = {}, {}
        for n, df in bdata.items():
            w = bench["gewichten"][n]
            net, *_ = net_returns_vehicle(df, np.full(len(df["date"]), float(w)), 1.0, veh, not bsum)
            for d, v in zip(df["date"], net):
                if np.isfinite(v) and (d >= RESERVE_START) == reserve and d.year >= sj and (reserve or d <= DISCOVERY_END):
                    bh.setdefault(d, []).append(v); bh_abs[d] = bh_abs.get(d, 0.0) + abs(w)
        return bh, bh_abs

    for vname, params in R["varianten"].items():
        sj = params.get("start_jaar", R.get("start_jaar", 1900))
        bench = params.get("benchmark", R.get("benchmark", {"gewichten": {n: 1.0 for n in R["instrumenten"]}})); bsum = "benchmark" in params or "benchmark" in R
        bh, bh_abs = make_bh(bench, sj, bsum)
        port, port50, ntr = {}, {}, 0
        absp = {}
        per_inst, comp = {}, {"gross": 0.0, "cost": 0.0, "swap": 0.0}
        mp = R.get("max_pos", 1.0)
        if hasattr(mod, "positions_all"):
            allpos = mod.positions_all(data, params)
        else:
            allpos = {n: mod.positions(df, params) for n, df in data.items()}
        for n, df in data.items():
            pos = np.clip(np.nan_to_num(np.asarray(allpos[n], float)), -mp, mp)
            for mult, tgt in ((1.0, port), (1.5, port50)):
                net, turn, gross, cost, swap = net_returns_vehicle(df, pos, mult, veh, cap)
                ok = np.isfinite(net) & np.array([(d >= RESERVE_START) == reserve and d.year >= sj and
                                                   (reserve or d <= DISCOVERY_END) for d in df["date"]])
                for d, v in zip(df["date"][ok], net[ok]):
                    tgt.setdefault(d, []).append(v)
                if mult == 1.0:
                    pp = np.r_[0.0, (pos if vehicles()[veh]["short"] else np.maximum(pos, 0.0))[:-1]]
                    for d, v in zip(df["date"][ok], np.abs(pp[ok])):
                        absp[d] = absp.get(d, 0.0) + v
                    ntr += int((turn[ok] > 0).sum()); per_inst[n] = net[ok]
                    comp["gross"] += float(gross[ok].sum()); comp["cost"] += float(cost[ok].sum()); comp["swap"] += float(np.nansum(swap[ok]))
        days = sorted(port)
        agg = np.sum if mode == "som" else np.mean
        x = np.array([agg(port[d]) for d in days]); x50 = np.array([agg(port50[d]) for d in days])
        # R2: etf/future-rendementen bevatten de kasrente → statistiek (SR, t) op overschotrendement (x − rf), zoals cfd al is;
        # maxDD/CAGR/equity op totaalrendement. Aggregatie 'som': kasrente/kapitaalrente één keer op portefeuilleniveau.
        nights_p = np.r_[0, [(b - a).days for a, b in zip(days[:-1], days[1:])]]
        rf_p = rf_on(days) / 100 / 365 * nights_p if veh != "cfd" else np.zeros(len(days))
        if mode == "som" and veh != "cfd":
            V_ = vehicles()[veh]
            cashfrac = np.array([np.clip(1 - absp.get(d, 0.0), 0, 1) for d in days]) if V_["model"] == "etf" else np.ones(len(days))
            x = x + rf_p * cashfrac; x50 = x50 + rf_p * cashfrac
        x_tot = x.copy(); x = x - rf_p; x50 = x50 - rf_p
        gross_turn_days = len(days)
        sr = x.mean() / x.std() * math.sqrt(252) if x.std() > 0 else float("nan")
        tb, sr_ci = boot(x)
        if not reserve:   # R2: dagreeks per regel/variant/vehikel voor de portefeuillestap (overschot en totaal)
            os.makedirs("results/R2/series", exist_ok=True)
            with open(f"results/R2/series/{R['id']}__{vname}__{veh}.csv", "w") as f:
                f.write("date;excess;total\n")
                f.writelines(f"{d};{a:.8f};{b:.8f}\n" for d, a, b in zip(days, x, x_tot))
        h = len(x) // 2
        eq = np.cumprod(1 + x_tot); dd = float(np.max(1 - eq / np.maximum.accumulate(eq)))
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
        bdays = [d for d in days if d in bh]
        bx_tot = np.array([(np.sum if bsum else np.mean)(bh[d]) for d in bdays])
        if bsum and veh != "cfd":
            V_ = vehicles()[veh]
            bx_tot = bx_tot + np.array([rf_p[days.index(d)] * (np.clip(1 - bh_abs[d], 0, 1) if V_["model"] == "etf" else 1.0) for d in bdays])
        bx = bx_tot - np.array([rf_p[days.index(d)] for d in bdays])
        beq = np.cumprod(1 + bx_tot); bdd = float(np.max(1 - beq / np.maximum.accumulate(beq))) if len(bx) else float("nan")
        bsr = bx.mean() / bx.std() * math.sqrt(252) if len(bx) and bx.std() > 0 else float("nan")
        cagr = eq[-1] ** (252 / len(x)) - 1; bcagr = beq[-1] ** (252 / len(bx)) - 1 if len(bx) else float("nan")
        calmar = cagr / dd if dd > 0 else float("nan"); bcalmar = bcagr / bdd if bdd > 0 else float("nan")
        gate_bench = sr > bsr and dd < bdd   # SR (overschot) én maxDD (totaal) beter; Calmar wordt erbij gerapporteerd
        # 5-jaarsvensters (kalender, niet-overlappend vanaf het eerste volledige jaar)
        yrs_all = sorted(yr); win = [yrs_all[i:i + 5] for i in range(0, len(yrs_all) - 4, 5)]
        w5 = [sum(sum(yr[y]) for y in w) > 0 for w in win]
        frac5 = float(np.mean(w5)) if w5 else float("nan")
        gate_cost = comp["gross"] >= 3 * comp["cost"] if comp["cost"] > 0 else comp["gross"] > 0   # ENGINE_TEMPLATE §4 (D-037)
        res = {"variant": vname, "dagen": len(x), "trades": ntr, "netto_bp_dag": x.mean() * 1e4, "SR": sr, "SR_CI90": sr_ci,
               "t_dag": t_day, "t_NW": t_n, "t_boot": tb, "t_H1": t_plain(x[:h]), "t_H2": t_plain(x[h:]), "t_50pct_spread": t_nw(x50),
               "skew": sk, "max_dagverlies": float(-x.min()), "P99_dagverlies": float(-np.percentile(x, 1)), "maxDD": dd,
               "corr": corr, "bull_bp": np.mean(bull) * 1e4 if bull else float("nan"), "bear_bp": np.mean(bear) * 1e4 if bear else float("nan"),
               "per_jaar": {y: float(np.sum(v)) for y, v in sorted(yr.items())},
               "per_instrument_t": {n: t_plain(v) for n, v in per_inst.items()}, "frac_5j_pos": frac5, "gate_kosten": gate_cost,
               "bruto_som": comp["gross"], "kosten_som": comp["cost"], "swap_som": comp["swap"]}
        rows.append(res)
        t_gate = min(res["t_NW"], res["t_boot"])
        gate = (gate_cost and t_gate >= 3 and res["t_H1"] > 0 and res["t_H2"] > 0 and sr >= 0.3 and frac5 >= 0.6
                and (ntr >= 500 or R.get("events", False) and ntr >= 100 or R.get("laag_omloop", False)))
        beslis = ("stop: kostenpoort (geen trial)" if not gate_cost else ("door G-ontdekking" if gate else "afgewezen"))
        primary = veh == R.get("vehicle", "cfd")
        with open(TRIALS, "a") as f:
            f.write(f"{date.today()};{R['id']};{vname};{R.get('dataset', 'D2')} [{veh}];{'reserve' if reserve else 'ontdekking'}{'' if primary else '-vehikelrapport'};"
                    f"{sr:.3f};{t_gate:.3f};{(f'{p_one_sided(t_gate):.6f}') if primary else ''};;"
                    f"{beslis if primary else 'vehikelrapport (geen extra trial); benchmark ' + ('beter' if gate_bench else 'niet beter')}\n")
        lines += [f"## variant {vname} {params} — vehikel {veh}",
                  f"- {'RESERVE 2025-01→' if reserve else 'ontdekking ≤ 2024'}: {len(x)} dagen, {ntr} positie-wijzigingen, netto {x.mean()*1e4:+.2f} bp/dag, SR {sr:+.2f} (90%-CI {sr_ci[0]:+.2f}…{sr_ci[1]:+.2f})",
                  f"- t: dag {t_day:+.2f} | Newey-West {t_n:+.2f} | blok-bootstrap {tb:+.2f} | H1 {res['t_H1']:+.2f} | H2 {res['t_H2']:+.2f} | +50% spread (NW) {res['t_50pct_spread']:+.2f}",
                  f"- skew {sk:+.2f} | max dagverlies {res['max_dagverlies']*100:.2f}% (P99 {res['P99_dagverlies']*100:.2f}%) | maxDD {dd*100:.1f}% (1× notional)",
                  f"- corr: " + ", ".join(f"{k} {v:+.2f}" for k, v in corr.items()) + f" | SPX > SMA200: {res['bull_bp']:+.2f} bp/dag, daaronder {res['bear_bp']:+.2f}",
                  "- per instrument t: " + ", ".join(f"{k} {v:+.2f}" for k, v in res["per_instrument_t"].items()),
                  "- per jaar (%): " + " ".join(f"{y}:{v*100:+.1f}" for y, v in res["per_jaar"].items()),
                  f"- kosten: bruto {comp['gross']*100:+.1f}% | spread/commissie {comp['cost']*100:.1f}% | financiering {comp['swap']*100:+.1f}% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) {'DOOR' if gate_cost else 'FAALT'}",
                  f"- 5-jaarsvensters positief: {frac5*100:.0f}% ({sum(w5)}/{len(w5)})",
                  f"- G-benchmark (vehikel {veh}): regel SR {sr:+.2f}, CAGR {cagr*100:+.1f}%, maxDD {dd*100:.1f}%, Calmar {calmar:.2f} | buy-and-hold ({bench.get('naam', 'gelijk gewogen')}) SR {bsr:+.2f}, CAGR {bcagr*100:+.1f}%, maxDD {bdd*100:.1f}%, Calmar {bcalmar:.2f} → {'BETER (SR én maxDD)' if gate_bench else 'niet beter'}",
                  f"- beslissing: {beslis} (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)", ""]
    recompute_fdr()
    open(f"{out_dir}/{'reserve' if reserve else 'ontdekking'}_{veh}.md", "w").write("\n".join(lines))
    print("\n".join(lines))
    return rows


def recompute_fdr():
    rows = list(csv.reader(open(TRIALS), delimiter=";"))
    hdr, body = rows[0], rows[1:]
    idx = [i for i, r in enumerate(body) if r[7]]
    q = bh_q([float(body[i][7]) for i in idx]) if idx else []
    for i, qq in zip(idx, q):
        body[i][8] = f"{qq:.4f}"
    with open(TRIALS, "w", newline="") as f:
        csv.writer(f, delimiter=";").writerows([hdr] + body)


if __name__ == "__main__":
    if not os.path.exists(TRIALS):
        os.makedirs("catalogus", exist_ok=True)
        open(TRIALS, "w").write("datum;regel_id;variant;dataset;fase;netto_SR;t_geclusterd;p;FDR_q;beslissing\n")
    veh = next((a.split("=")[1] for a in sys.argv if a.startswith("--vehicle=")), None)
    run(sys.argv[1], reserve="--reserve" in sys.argv, vehicle=veh)
