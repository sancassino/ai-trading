#!/usr/bin/env python3
"""PREREG_FTMO_TSMOM_DIV — universe already frozen; cost-gate + formal train/test.

Regel (CEO D-098 / PREREG_FTMO_TSMOM_DIV.md):
- 12-1 TSMOM, monthly rebalance, inverse-vol 10%/yr per sleeve, port-vol cap ≈10%
- Train 2008–2016 / test 2017–2024-12; reserve 2025-01→ untouched
- Cost-gate: mean bruto/maand-trade ≥ 3× mean(RT+swap) on train; else STOP (no trial)
- Trial: day-clust netto t≥2 train én test; mean netto>0 beide helften; ≥2/3 klassen +; N_maand≥150
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/tsmom_div"
UNIVERSE = OUT / "universe.csv"
CAL_END = pd.Timestamp("2024-12-31")
TRAIN = (pd.Timestamp("2008-01-01"), pd.Timestamp("2016-12-31"))
TEST = (pd.Timestamp("2017-01-01"), pd.Timestamp("2024-12-31"))
VOL_TARGET = 0.10
SIGMA_N = 60
MOM_MONTHS = 12  # 12-1: skip most recent month inside lookback via month-end shift

MAJOR_CCY = {"USD", "EUR", "GBP", "JPY", "CHF", "AUD", "CAD", "NZD"}

FALLBACK_COST = {
    "index": {"rt": 1.5, "swap_long": 1.5, "swap_short": 0.8},
    "fx": {"rt": 1.0, "swap_long": 0.5, "swap_short": 0.5},
    "commodity/metal": {"rt": 3.0, "swap_long": 2.0, "swap_short": 2.0},
}


def _norm(s: str) -> str:
    return s.replace(".", "").replace("_", "").replace("-", "").lower()


def load_universe() -> list[dict]:
    lines = [ln for ln in UNIVERSE.read_text().splitlines() if ln.strip() and not ln.startswith("#")]
    return list(csv.DictReader(lines, delimiter=";"))


def load_costs() -> dict[str, dict]:
    out: dict[str, dict] = {}
    # primary: COSTS_FTMO (has swap)
    p = ROOT / "COSTS_FTMO.csv"
    df = pd.read_csv(p, sep=";", comment="#")
    for _, r in df.iterrows():
        out[_norm(str(r["symbol"]))] = {
            "rt": float(r["roundtrip_intraday_bp"]),
            "swap_long": float(r["swap_long_bp_per_nacht"]),
            "swap_short": float(r["swap_short_bp_per_nacht"]),
            "src": str(r["symbol"]),
        }
    # alle: RT only fill
    p2 = ROOT / "COSTS_FTMO_alle.csv"
    if p2.exists():
        lines = [ln for ln in p2.read_text().splitlines() if ln.strip() and not ln.startswith("#")]
        for r in csv.DictReader(lines, delimiter=";"):
            try:
                n = _norm(str(r["symbol"]))
                if n not in out:
                    out[n] = {
                        "rt": float(r["rondreis_bp"]),
                        "swap_long": float("nan"),
                        "swap_short": float("nan"),
                        "src": f"alle:{r['symbol']}",
                    }
            except (KeyError, ValueError, TypeError):
                continue
    # swap_specs_FTMO → fill missing swaps
    p3 = ROOT / "swap_specs_FTMO.csv"
    if p3.exists():
        df3 = pd.read_csv(p3, sep=";", comment="#")
        for _, r in df3.iterrows():
            n = _norm(str(r["symbol"]))
            try:
                lp = float(r["long_pct_yr"])
                sp = float(r["short_pct_yr"])
            except (TypeError, ValueError):
                continue
            if math.isnan(lp) or math.isnan(sp):
                continue
            # bp/night cost = -pct_yr * 100 / 365 (pct_yr signed receipt)
            sl = -lp * 100.0 / 365.0
            ss = -sp * 100.0 / 365.0
            if n in out:
                if math.isnan(out[n]["swap_long"]):
                    out[n]["swap_long"] = sl
                    out[n]["swap_short"] = ss
                    out[n]["src"] += "+swap_specs"
            else:
                out[n] = {"rt": float("nan"), "swap_long": sl, "swap_short": ss, "src": "swap_specs"}
    return out


def cost_for(ftmo: str, categorie: str, costs: dict) -> dict:
    n = _norm(ftmo)
    cands = [
        n,
        _norm(ftmo.replace(".cash", "cash")),
        _norm(ftmo.replace(".c", "")),
        _norm(ftmo.split(".")[0] + "cash"),
    ]
    if "usoil" in n:
        cands.append("usoilcash")
    if "ukoil" in n:
        cands.append("ukoilcash")
    for c in cands:
        if c in costs:
            d = dict(costs[c])
            fb = FALLBACK_COST.get(categorie, FALLBACK_COST["index"])
            if math.isnan(d.get("rt", float("nan"))):
                d["rt"] = fb["rt"]
            if math.isnan(d.get("swap_long", float("nan"))):
                d["swap_long"] = fb["swap_long"]
                d["swap_short"] = fb["swap_short"]
            d["match"] = d.pop("src")
            return d
    fb = FALLBACK_COST.get(categorie, FALLBACK_COST["index"])
    return {**fb, "match": f"fallback:{categorie}"}


def _read_daily(name: str) -> pd.Series | None:
    for sub in ("daily", "derived", "yahoo"):
        path = ROOT / "data" / sub / f"{name}.csv"
        if not path.exists():
            continue
        df = pd.read_csv(path, sep=";", comment="#")
        df.columns = [c.lower() for c in df.columns]
        if "date" not in df.columns or "close" not in df.columns:
            continue
        df["date"] = pd.to_datetime(df["date"])
        col = "adjclose" if "adjclose" in df.columns and df["adjclose"].notna().any() else "close"
        s = df.set_index("date")[col].astype(float).sort_index()
        s = s[~s.index.duplicated(keep="last")]
        s = s[s.index <= CAL_END]
        s = s.replace([np.inf, -np.inf], np.nan).dropna()
        s = s[s > 0]
        return s if len(s) > 200 else None
    return None


def load_proxy_series(proxy: str) -> pd.Series | None:
    """Load proxy; support A+B composites (FXBIS crosses, metal×FX)."""
    if "+" not in proxy:
        return _read_daily(proxy)
    parts = proxy.split("+")
    if len(parts) != 2:
        return None
    a, b = parts[0], parts[1]
    sa, sb = _read_daily(a), _read_daily(b)
    if sa is None or sb is None:
        return None
    j = pd.concat([sa.rename("a"), sb.rename("b")], axis=1).dropna()
    if len(j) < 200:
        return None
    # Conventions (data headers): FXBIS_* = local currency per USD
    # FX cross BASEQUOTE with proxy FXBIS_BASE+FXBIS_QUOTE → QUOTE/BASE = b/a
    # Metal in local: GOLD_F+FXBIS_EUR → gold * (EUR per USD) = gold in EUR
    if a.startswith("FXBIS_") and b.startswith("FXBIS_"):
        out = j["b"] / j["a"]
    elif a.endswith("_F") and b.startswith("FXBIS_"):
        out = j["a"] * j["b"]
    else:
        out = j["a"] / j["b"]
    out = out.replace([np.inf, -np.inf], np.nan).dropna()
    return out if len(out) > 200 else None


def month_ends(idx: pd.DatetimeIndex) -> pd.DatetimeIndex:
    s = pd.Series(1, index=idx)
    return s.groupby([idx.year, idx.month]).apply(lambda x: x.index.max()).values


def realized_vol(px: pd.Series, n: int = SIGMA_N) -> pd.Series:
    r = np.log(px / px.shift(1))
    return r.rolling(n, min_periods=n).std() * math.sqrt(252)


def build_panel(universe: list[dict], costs: dict):
    meta = {}
    series = {}
    for u in universe:
        px = load_proxy_series(u["proxy"])
        if px is None:
            meta[u["ftmo_symbol"]] = {**u, "loaded": False, "reason": "proxy_load_fail"}
            continue
        # require coverage into train start with mom lookback ~13m
        if px.index.min() > pd.Timestamp("2007-01-01"):
            # still allow if enough for train after warm-up; keep if spans ≥ train with 13m prep
            pass
        c = cost_for(u["ftmo_symbol"], u["categorie"], costs)
        series[u["ftmo_symbol"]] = px
        meta[u["ftmo_symbol"]] = {**u, "loaded": True, "cost": c, "px_start": str(px.index.min().date()), "px_n": int(len(px))}
    return series, meta


def simulate(series: dict[str, pd.Series], meta: dict, start: pd.Timestamp, end: pd.Timestamp):
    """Return daily portfolio bruto/netto (fraction), month-trades table, per-class daily netto."""
    # common calendar
    px = pd.DataFrame(series).sort_index()
    px = px.loc[:CAL_END].ffill(limit=2)
    # restrict to window with warm-up for vol + 12m mom
    warm = start - pd.DateOffset(months=14)
    px = px.loc[warm:end]
    if px.empty:
        return None

    # month-end dates on union calendar
    cal = px.dropna(how="all").index
    mes = sorted({d for d in month_ends(cal) if pd.Timestamp(d) >= warm})
    mes = [pd.Timestamp(d) for d in mes]

    # precompute vol
    vols = {sym: realized_vol(px[sym]).reindex(cal) for sym in px.columns}

    # signal at month-end m: sign(px[m_prev]/px[m_prev-12] - 1) where m_prev = previous month-end
    # 12-1: return from t-12 to t-1 (exclude current month) → use price at prior month-end vs 12 month-ends earlier
    me_index = {d: i for i, d in enumerate(mes)}

    weights_by_me: dict[pd.Timestamp, dict[str, float]] = {}
    month_trades = []

    for i, me in enumerate(mes):
        if i < MOM_MONTHS + 1:
            continue
        me_signal = mes[i - 1]  # t-1 month end
        me_lag = mes[i - 1 - MOM_MONTHS]  # t-12 month end (12-1)
        if me < start or me > end:
            # still compute weights for continuity inside window; skip trade log outside
            pass
        active = {}
        for sym in px.columns:
            p_sig = px[sym].loc[:me_signal].dropna()
            p_lag = px[sym].loc[:me_lag].dropna()
            if p_sig.empty or p_lag.empty:
                continue
            p1 = float(p_sig.iloc[-1])
            p0 = float(p_lag.iloc[-1])
            if p0 <= 0 or p1 <= 0 or not math.isfinite(p1 / p0):
                continue
            sig = math.copysign(1.0, p1 / p0 - 1.0) if (p1 / p0 - 1.0) != 0 else 0.0
            if sig == 0:
                continue
            v = vols[sym].loc[:me]
            v = v.dropna()
            if v.empty or float(v.iloc[-1]) <= 1e-6:
                continue
            sigma = float(v.iloc[-1])
            active[sym] = (sig, sigma)
        if not active:
            weights_by_me[me] = {}
            continue
        n_act = len(active)
        # equal risk 10% then scale port vol ≈ 10% under diagonal: scale 1/sqrt(N)
        scale = 1.0 / math.sqrt(n_act)
        w = {sym: sig * (VOL_TARGET / sigma) * scale for sym, (sig, sigma) in active.items()}
        weights_by_me[me] = w

        # month-trade bruto from me→next me (execution t+1 ≈ first available after me)
        if i + 1 >= len(mes):
            continue
        me_next = mes[i + 1]
        if me < start or me_next > end + pd.Timedelta(days=1):
            if not (start <= me <= end):
                continue
        # entry = next trading day after me; exit = me_next
        after = cal[cal > me]
        if len(after) == 0:
            continue
        entry = after[0]
        if entry > end or me_next < start:
            continue
        for sym, weight in w.items():
            path = px[sym].loc[entry:me_next].dropna()
            if len(path) < 2:
                continue
            p_e = float(path.iloc[0])
            p_x = float(path.iloc[-1])
            if p_e <= 0:
                continue
            bruto_frac = weight * (p_x / p_e - 1.0)
            # costs on this sleeve-month: |Δw| from prior * RT/2 each side ≈ |w|*RT if flat→w
            # PREREG: RT per rebalance-flip + swap per night
            c = meta[sym]["cost"]
            nights = max(int((me_next - entry).days), 1)
            swap_bp = (c["swap_long"] if weight > 0 else c["swap_short"]) * nights
            # position notional |w|; cost in portfolio-fraction ≈ |w| * (RT + swap)*1e-4
            # for gate "per maand-trade" use unit-notional trade costs vs unit bruto
            side = 1.0 if weight > 0 else -1.0
            bruto_bp_unit = side * (p_x / p_e - 1.0) * 10_000.0
            cost_bp_unit = float(c["rt"]) + float(swap_bp if weight > 0 else (c["swap_short"] * nights))
            # fix: swap already direction-specific
            cost_bp_unit = float(c["rt"]) + float(c["swap_long"] if weight > 0 else c["swap_short"]) * nights
            month_trades.append(
                {
                    "month_end": me,
                    "entry": entry,
                    "exit": me_next,
                    "sym": sym,
                    "klasse": meta[sym]["klasse"],
                    "side": side,
                    "weight": weight,
                    "bruto_bp_unit": bruto_bp_unit,
                    "cost_bp_unit": cost_bp_unit,
                    "cost_bp_unit_stress": float(c["rt"]) + 1.5 * float(c["swap_long"] if weight > 0 else c["swap_short"]) * nights,
                    "bruto_frac_port": bruto_frac,
                    "nights": nights,
                }
            )

    # daily portfolio returns
    w_dates = sorted(weights_by_me)
    # map each day → weights decided on most recent me < day (exec t+1)
    daily_rows = []
    class_rets = {k: [] for k in ("indices", "metalen", "energie_agri", "fx")}

    prev_w = {}
    me_ptr = 0
    cur_w = {}
    for i in range(1, len(cal)):
        d = cal[i]
        d_prev = cal[i - 1]
        if d < start or d > end:
            continue
        # update weights: decision on me applies from next day
        while me_ptr < len(w_dates) and w_dates[me_ptr] < d:
            # weight set at me applies starting day after me
            if w_dates[me_ptr] < d:
                cur_w = weights_by_me[w_dates[me_ptr]]
            me_ptr += 1
        # actually: find latest me with me < d
        latest = None
        for me in w_dates:
            if me < d:
                latest = me
            else:
                break
        cur_w = weights_by_me.get(latest, {}) if latest is not None else {}

        bruto = 0.0
        cost = 0.0
        class_b = {k: 0.0 for k in class_rets}
        class_c = {k: 0.0 for k in class_rets}
        nights = max(int((d - d_prev).days), 0)
        # include zeros for closed names (turnover out)
        syms = set(cur_w) | set(prev_w)
        for sym in syms:
            w = cur_w.get(sym, 0.0)
            w_prev = prev_w.get(sym, 0.0)
            c = meta[sym]["cost"]
            kl = meta[sym]["klasse"]
            p0 = px[sym].get(d_prev, np.nan)
            p1 = px[sym].get(d, np.nan)
            if math.isfinite(p0) and math.isfinite(p1) and p0 > 0 and w_prev != 0:
                r = p1 / p0 - 1.0
                bruto += w_prev * r  # position held overnight = prior weight
                class_b[kl] += w_prev * r
            # swap on prior weight (held through the night)
            if nights and w_prev != 0:
                swap_bp_night = c["swap_long"] if w_prev > 0 else c["swap_short"]
                c_swap = abs(w_prev) * swap_bp_night * nights * 1e-4
                cost += c_swap
                class_c[kl] += c_swap
            # turnover at today's decision vs prior
            turn = abs(w - w_prev)
            if turn > 0:
                c_rt = turn * (c["rt"] / 2.0) * 1e-4
                cost += c_rt
                class_c[kl] += c_rt

        netto = bruto - cost
        daily_rows.append({"date": d, "bruto": bruto, "cost": cost, "netto": netto, "n_active": len(cur_w)})
        for kl in class_rets:
            class_rets[kl].append({"date": d, "netto": class_b[kl] - class_c[kl], "bruto": class_b[kl]})
        prev_w = dict(cur_w)

    daily = pd.DataFrame(daily_rows)
    trades = pd.DataFrame(month_trades)
    return {"daily": daily, "trades": trades, "class_rets": class_rets}


def t_stat(x: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if len(x) < 5:
        return float("nan")
    m = float(np.mean(x))
    s = float(np.std(x, ddof=1))
    if s <= 0:
        return float("nan")
    return m / (s / math.sqrt(len(x)))


def nw_t(x: np.ndarray, L: int = 5) -> float:
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    n = len(x)
    if n < L + 5:
        return float("nan")
    m = float(np.mean(x))
    xc = x - m
    gamma0 = float(np.dot(xc, xc) / n)
    var = gamma0
    for ell in range(1, L + 1):
        w = 1.0 - ell / (L + 1.0)
        g = float(np.dot(xc[ell:], xc[:-ell]) / n)
        var += 2 * w * g
    if var <= 0:
        return float("nan")
    return m / math.sqrt(var / n)


def summarize(sim, label: str) -> dict:
    daily = sim["daily"]
    trades = sim["trades"]
    if daily is None or daily.empty:
        return {"label": label, "ok": False}
    # restrict trades to window
    if not trades.empty:
        # unit-trade gate metrics
        mean_bruto = float(trades["bruto_bp_unit"].mean())
        mean_cost = float(trades["cost_bp_unit"].mean())
        mean_cost_stress = float(trades["cost_bp_unit_stress"].mean())
        n_month = int(trades["month_end"].nunique())
        n_trades = int(len(trades))
    else:
        mean_bruto = mean_cost = mean_cost_stress = float("nan")
        n_month = n_trades = 0

    netto = daily["netto"].to_numpy()
    bruto = daily["bruto"].to_numpy()
    mid = daily["date"].min() + (daily["date"].max() - daily["date"].min()) / 2
    h1 = daily.loc[daily["date"] <= mid, "netto"].to_numpy()
    h2 = daily.loc[daily["date"] > mid, "netto"].to_numpy()

    class_means = {}
    for kl, rows in sim["class_rets"].items():
        if not rows:
            class_means[kl] = float("nan")
            continue
        cdf = pd.DataFrame(rows)
        class_means[kl] = float(cdf["netto"].mean()) if len(cdf) else float("nan")
    n_pos_class = sum(1 for v in class_means.values() if math.isfinite(v) and v > 0)
    n_class = sum(1 for v in class_means.values() if math.isfinite(v))

    gate_pass = bool(math.isfinite(mean_bruto) and math.isfinite(mean_cost) and mean_bruto >= 3.0 * mean_cost)
    # +50% swap stress on cost side for info (PREREG mentions +50% swap sensitivity)
    stress_pass = bool(math.isfinite(mean_bruto) and mean_bruto >= 3.0 * mean_cost_stress)

    return {
        "label": label,
        "ok": True,
        "N_days": int(len(daily)),
        "N_month": n_month,
        "N_trades": n_trades,
        "mean_bruto_bp_unit": None if not math.isfinite(mean_bruto) else round(mean_bruto, 4),
        "mean_cost_bp_unit": None if not math.isfinite(mean_cost) else round(mean_cost, 4),
        "mean_cost_stress_bp_unit": None if not math.isfinite(mean_cost_stress) else round(mean_cost_stress, 4),
        "gate_3x": gate_pass,
        "stress_3x_swap50": stress_pass,
        "mean_netto_daily": round(float(np.mean(netto)), 8),
        "mean_bruto_daily": round(float(np.mean(bruto)), 8),
        "t_day_clust_netto": round(t_stat(netto), 4),
        "t_nw_L5_netto": round(nw_t(netto, 5), 4),
        "mean_netto_h1": round(float(np.mean(h1)), 8) if len(h1) else None,
        "mean_netto_h2": round(float(np.mean(h2)), 8) if len(h2) else None,
        "class_mean_netto": {k: (None if not math.isfinite(v) else round(v, 8)) for k, v in class_means.items()},
        "n_pos_class": n_pos_class,
        "n_class": n_class,
        "class_rule_pass": n_class > 0 and n_pos_class >= math.ceil(2 * n_class / 3),
    }


def decide(train: dict, test: dict | None) -> str:
    if not train.get("gate_3x"):
        return "FAIL_COST_GATE"
    if test is None:
        return "FAIL_NO_TEST"
    # formal trial criteria
    checks = []
    checks.append(train.get("t_day_clust_netto", 0) >= 2.0)
    checks.append(test.get("t_day_clust_netto", 0) >= 2.0)
    checks.append((train.get("mean_netto_h1") or 0) > 0 and (train.get("mean_netto_h2") or 0) > 0)
    checks.append((test.get("mean_netto_h1") or 0) > 0 and (test.get("mean_netto_h2") or 0) > 0)
    checks.append(bool(train.get("class_rule_pass")) and bool(test.get("class_rule_pass")))
    n_pool = (train.get("N_month") or 0) + (test.get("N_month") or 0)
    checks.append(n_pool >= 150)
    if all(checks):
        return "PASS"
    # detailed fail label
    if not train.get("gate_3x"):
        return "FAIL_COST_GATE"
    reasons = []
    if train.get("t_day_clust_netto", 0) < 2.0 or test.get("t_day_clust_netto", 0) < 2.0:
        reasons.append("FAIL_T")
    if not ((train.get("mean_netto_h1") or 0) > 0 and (train.get("mean_netto_h2") or 0) > 0 and (test.get("mean_netto_h1") or 0) > 0 and (test.get("mean_netto_h2") or 0) > 0):
        reasons.append("FAIL_HALVES")
    if not (train.get("class_rule_pass") and test.get("class_rule_pass")):
        reasons.append("FAIL_CLASS")
    if n_pool < 150:
        reasons.append("FAIL_N")
    return "_then_".join(reasons) if reasons else "FAIL_T"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    universe = load_universe()
    costs = load_costs()
    print(f"universe={len(universe)} cost_keys={len(costs)}", flush=True)
    series, meta = build_panel(universe, costs)
    loaded = [k for k, v in meta.items() if v.get("loaded")]
    print(f"loaded_proxies={len(loaded)}/{len(universe)}", flush=True)
    (OUT / "universe_load_meta.json").write_text(json.dumps(meta, indent=2, default=str) + "\n")

    print("simulate train 2008–2016…", flush=True)
    sim_tr = simulate(series, meta, TRAIN[0], TRAIN[1])
    print("simulate test 2017–2024…", flush=True)
    sim_te = simulate(series, meta, TEST[0], TEST[1])

    tr = summarize(sim_tr, "train") if sim_tr else {"ok": False}
    te = summarize(sim_te, "test") if sim_te else None

    if sim_tr and not sim_tr["trades"].empty:
        sim_tr["trades"].to_csv(OUT / "month_trades_train.csv", index=False)
    if sim_te and not sim_te["trades"].empty:
        sim_te["trades"].to_csv(OUT / "month_trades_test.csv", index=False)
    if sim_tr and not sim_tr["daily"].empty:
        sim_tr["daily"].to_csv(OUT / "daily_train.csv", index=False)
    if sim_te and not sim_te["daily"].empty:
        sim_te["daily"].to_csv(OUT / "daily_test.csv", index=False)

    outcome = decide(tr, te)
    counts_as_trial = bool(tr.get("gate_3x"))

    board = {
        "prereg": "PREREG_FTMO_TSMOM_DIV.md",
        "decision": "D-098",
        "universe_n": len(universe),
        "loaded_n": len(loaded),
        "outcome": outcome,
        "counts_as_trial": counts_as_trial,
        "train": tr,
        "test": te,
        "reserve_2025": "untouched",
        "vol_target": VOL_TARGET,
        "sigma_n": SIGMA_N,
    }
    (OUT / "tsmom_div_board.json").write_text(json.dumps(board, indent=2) + "\n")

    md = [
        "# PREREG_FTMO_TSMOM_DIV — cost-gate + formal train/test",
        "",
        f"Universe freeze: `{UNIVERSE}` (n={len(universe)}, loaded={len(loaded)}).",
        "Train 2008–2016 / test 2017–2024-12. Reserve 2025→ **untouched**.",
        "Rule: 12-1 TSMOM monthly, inv-vol 10%/yr equal-risk, port-vol cap 10% via 1/√N diagonal scale.",
        "",
        f"**Uitkomst: {outcome}** (counts_as_trial={counts_as_trial})",
        "",
        "## Train",
        "",
        "```json",
        json.dumps(tr, indent=2),
        "```",
        "",
        "## Test",
        "",
        "```json",
        json.dumps(te, indent=2),
        "```",
        "",
    ]
    (OUT / "tsmom_div_report.md").write_text("\n".join(md) + "\n")
    print(json.dumps({"outcome": outcome, "counts_as_trial": counts_as_trial, "train": tr, "test": te}, indent=2), flush=True)
    return board


if __name__ == "__main__":
    main()
