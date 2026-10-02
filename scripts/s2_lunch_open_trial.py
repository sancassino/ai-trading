#!/usr/bin/env python3
"""S2 LUNCH_OPEN formal trial after cost-gate PASS — PREREG_S2_LUNCH_OPEN §4.

Train 2021–2023 + test 2024. Reserve 2025→ untouched.
Day-clustered netto t; 0.75% risk sizing for daily returns → ftmo_ev.
"""
from __future__ import annotations

import gzip
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from engine.ftmo import ftmo_ev  # noqa: E402

M5 = ROOT / "data" / "m5gz"
RT = {"US30cash": 0.45, "US100cash": 0.66}
ATR_N = 14
WIDTH_K = 0.40
STOP_BUF = 0.15
RISK = 0.0075  # 0.75% account risk per trade
OPEN_H, OPEN_M = 15, 30
ENTRY_H, ENTRY_M = 17, 0
FLAT_H, FLAT_M = 19, 0
OUT_DIR = ROOT / "results" / "R2" / "lunch_open_prep"
WINDOWS = {
    "train": (pd.Timestamp("2021-01-01"), pd.Timestamp("2023-12-31 23:59:59")),
    "test": (pd.Timestamp("2024-01-01"), pd.Timestamp("2024-12-31 23:59:59")),
}


def load_m5(sym: str, start, end) -> pd.DataFrame:
    with gzip.open(M5 / f"{sym}.csv.gz", "rt") as f:
        for line in f:
            if not line.startswith("#"):
                break
        df = pd.read_csv(
            f, sep=";", names=["time", "open", "high", "low", "close", "spread"]
        )
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["close"]).sort_values("time").reset_index(drop=True)
    return df[(df["time"] >= start) & (df["time"] <= end)]


def daily_atr_prior_map(df: pd.DataFrame) -> dict:
    g = df.groupby(df["time"].dt.normalize())
    h = g["high"].max()
    l = g["low"].min()
    c = g["close"].last()
    prev_c = c.shift(1)
    tr = pd.concat([(h - l), (h - prev_c).abs(), (l - prev_c).abs()], axis=1).max(axis=1)
    atr = tr.rolling(ATR_N, min_periods=ATR_N).mean()
    atr_prior = atr.shift(1)
    return {d: float(v) for d, v in atr_prior.items() if pd.notna(v) and v > 0}


def bar_at(g: pd.DataFrame, day0, hh, mm):
    t = day0 + pd.Timedelta(hours=hh, minutes=mm)
    b = g[(g["time"] >= t) & (g["time"] < t + pd.Timedelta(minutes=5))]
    return None if b.empty else b.iloc[0]


def sim_day(g: pd.DataFrame, atr_price: float, rt: float):
    if len(g) < 30 or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b_open = bar_at(g, day0, OPEN_H, OPEN_M)
    b_entry = bar_at(g, day0, ENTRY_H, ENTRY_M)
    if b_open is None or b_entry is None:
        return None
    p_open = float(b_open["open"])
    entry = float(b_entry["close"])
    entry_time = b_entry["time"]
    if p_open <= 0:
        return None
    morn_bp = 1e4 * (entry - p_open) / p_open
    atr_bp = 1e4 * atr_price / p_open
    if abs(morn_bp) < WIDTH_K * atr_bp:
        return None
    side = -1 if morn_bp > 0 else 1
    t_open = day0 + pd.Timedelta(hours=OPEN_H, minutes=OPEN_M)
    t_entry = day0 + pd.Timedelta(hours=ENTRY_H, minutes=ENTRY_M)
    t_flat = day0 + pd.Timedelta(hours=FLAT_H, minutes=FLAT_M)
    morn = g[(g["time"] >= t_open) & (g["time"] <= t_entry)]
    if morn.empty:
        return None
    mhi, mlo = float(morn["high"].max()), float(morn["low"].min())
    mr = mhi - mlo
    if mr <= 0:
        return None
    target_px = p_open
    stop_px = (mlo - STOP_BUF * mr) if side == 1 else (mhi + STOP_BUF * mr)
    stop_bp = abs(1e4 * (stop_px - entry) / entry)
    if stop_bp < 1e-6:
        return None
    after = g[(g["time"] > entry_time) & (g["time"] <= t_flat)]
    if after.empty:
        return None
    exit_px = float(after.iloc[-1]["close"])
    reason = "time"
    for _, row in after.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        hit_s = (side == 1 and lo <= stop_px) or (side == -1 and hi >= stop_px)
        hit_t = (side == 1 and hi >= target_px) or (side == -1 and lo <= target_px)
        if hit_s and hit_t:
            exit_px, reason = stop_px, "stop_samebar"
            break
        if hit_s:
            exit_px, reason = stop_px, "stop"
            break
        if hit_t:
            exit_px, reason = target_px, "target"
            break
    bruto = side * 1e4 * (exit_px - entry) / entry
    netto = bruto - rt
    # Account fraction return at 0.75% risk: R-multiple × risk
    r_mult = bruto / stop_bp
    acct_ret = (r_mult * RISK) - (rt / 1e4) * (RISK / (stop_bp / 1e4))
    # Equivalent: netto_bp/1e4 * (RISK / (stop_bp/1e4))
    acct_ret2 = (netto / 1e4) * (RISK / (stop_bp / 1e4))
    return {
        "bruto_bp": bruto,
        "netto_bp": netto,
        "rt": rt,
        "side": side,
        "stop_bp": stop_bp,
        "acct_ret": acct_ret2,
        "reason": reason,
        "morn_bp": morn_bp,
        "atr_bp": atr_bp,
    }


def collect(window: str):
    start, end = WINDOWS[window]
    # Load enough history before window for ATR warm-up
    warm = start - pd.Timedelta(days=40)
    trades = []
    for sym, rt in RT.items():
        m5_full = load_m5(sym, warm, end)
        atr = daily_atr_prior_map(m5_full)
        m5 = m5_full[(m5_full["time"] >= start) & (m5_full["time"] <= end)]
        for day, g in m5.groupby(m5["time"].dt.normalize()):
            atr_val = atr.get(day)
            if atr_val is None or atr_val <= 0:
                continue
            r = sim_day(g, atr_val, rt)
            if r is not None:
                trades.append({"date": str(day.date()), "sym": sym, "window": window, **r})
    return trades


def day_cluster_t(trades):
    if not trades:
        return {"N_trades": 0, "N_days": 0, "t": None, "mean_netto": None, "mean_day": None}
    df = pd.DataFrame(trades)
    day = df.groupby("date")["netto_bp"].sum()
    n = len(day)
    mean = float(day.mean())
    std = float(day.std(ddof=1)) if n > 1 else float("nan")
    t = mean / (std / np.sqrt(n)) if n > 1 and std > 0 else float("nan")
    return {
        "N_trades": len(trades),
        "N_days": n,
        "mean_netto_trade": round(float(df["netto_bp"].mean()), 4),
        "mean_day_netto_bp": round(mean, 4),
        "std_day_netto_bp": round(std, 4) if std == std else None,
        "t_day_clustered": round(float(t), 4) if t == t else None,
        "skew_day": round(float(day.skew()), 4),
        "cost_share": round(float(df["rt"].sum() / max(df["bruto_bp"].clip(lower=0).sum(), 1e-9)), 4)
        if float(df["bruto_bp"].sum()) > 0
        else None,
        "mean_bruto": round(float(df["bruto_bp"].mean()), 4),
        "frac_cost_of_bruto": round(
            float(df["rt"].mean() / df["bruto_bp"].mean()), 4
        )
        if abs(float(df["bruto_bp"].mean())) > 1e-9
        else None,
    }


def build_calendar_returns(trades, start, end):
    """Trading-day fractional account returns (0 on no-trade days in window)."""
    idx = pd.bdate_range(start.normalize(), end.normalize())
    s = pd.Series(0.0, index=idx)
    if trades:
        df = pd.DataFrame(trades)
        df["date"] = pd.to_datetime(df["date"])
        day = df.groupby("date")["acct_ret"].sum()
        for d, v in day.items():
            if d in s.index:
                s.loc[d] = float(v)
            else:
                # weekend/holiday trade date — map to next bday if needed
                loc = s.index.searchsorted(d)
                if loc < len(s):
                    s.iloc[loc] += float(v)
    return s


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    all_trades = []
    stats = {}
    for w in ("train", "test"):
        tr = collect(w)
        all_trades.extend(tr)
        st = day_cluster_t(tr)
        st["window"] = w
        stats[w] = st
        print(f"{w}: {json.dumps(st)}")

    pd.DataFrame(all_trades).to_csv(OUT_DIR / "trial_lunch_open_trades.csv", index=False)

    # Beslisregel §4.2
    tr, te = stats["train"], stats["test"]
    t_ok = (
        tr.get("t_day_clustered") is not None
        and te.get("t_day_clustered") is not None
        and tr["t_day_clustered"] >= 2.0
        and te["t_day_clustered"] >= 2.0
        and tr["mean_netto_trade"] > 0
        and te["mean_netto_trade"] > 0
        and tr["N_trades"] >= 150
    )
    # §4.3 cost < 50% bruto (mean rt / mean bruto)
    cost_ok = (
        tr.get("frac_cost_of_bruto") is not None
        and abs(tr["frac_cost_of_bruto"]) < 0.50
        and tr["mean_bruto"] > 0
    )
    skew_ok = tr.get("skew_day") is not None and tr["skew_day"] > 0

    # ftmo_ev on train calendar returns (discovery); test reported separately
    train_ret = build_calendar_returns(
        [t for t in all_trades if t["window"] == "train"],
        WINDOWS["train"][0],
        WINDOWS["train"][1],
    )
    test_ret = build_calendar_returns(
        [t for t in all_trades if t["window"] == "test"],
        WINDOWS["test"][0],
        WINDOWS["test"][1],
    )
    # Use trade days only (nonzero) for MC block bootstrap richness
    train_nz = train_ret[train_ret != 0].values
    test_nz = test_ret[test_ret != 0].values

    ftmo = None
    if len(train_nz) >= 20:
        # p95 daily loss at 0.75% risk
        p95_dd = float(np.percentile(-np.minimum(train_nz, 0), 95)) if (train_nz < 0).any() else 0.0
        ftmo = ftmo_ev(train_nz, n_paths=5000, seed=42)
        # Also combine train+test nonzero for sensitivity (label)
        ftmo_both = ftmo_ev(np.concatenate([train_nz, test_nz]), n_paths=5000, seed=42) if len(test_nz) >= 5 else None
        ftmo_out = {
            "p95_daily_loss_frac": round(p95_dd, 6),
            "p95_daily_loss_ok": p95_dd <= 0.02,
            "train_only": {k: (round(v, 6) if isinstance(v, float) else v) for k, v in ftmo.items()
                           if k in ("p_pass_1", "p_pass_2", "p_survive", "exp_payout_monthly", "net_ev",
                                    "attempts_mean", "horizon_months", "n_funded")},
        }
        if ftmo_both:
            ftmo_out["train_test_sens"] = {
                k: (round(v, 6) if isinstance(v, float) else v) for k, v in ftmo_both.items()
                if k in ("p_pass_1", "p_pass_2", "p_survive", "exp_payout_monthly", "net_ev")
            }
        # EV per attempt ≈ net_ev / attempts_mean (over horizon); PREREG wants ≥ €150/poging
        att = ftmo.get("attempts_mean") or 1.0
        ev_per_attempt = float(ftmo["net_ev"]) / att if att else None
        # Also monthly
        hm = ftmo.get("horizon_months") or 24
        net_ev_m = float(ftmo["net_ev"]) / hm
        ftmo_out["net_ev_monthly"] = round(net_ev_m, 2)
        ftmo_out["net_ev_per_attempt"] = round(ev_per_attempt, 2) if ev_per_attempt is not None else None
        ftmo_out["ev_per_attempt_ok"] = (
            ev_per_attempt is not None and ev_per_attempt >= 150.0
        )
    else:
        ftmo_out = {"error": "insufficient nonzero train days", "n": int(len(train_nz))}

    decision = {
        "t_ok": bool(t_ok),
        "cost_ok": bool(cost_ok),
        "skew_ok": bool(skew_ok),
        "ftmo": ftmo_out,
        "stats": stats,
        "outcome": None,
    }
    # Overall
    if not t_ok:
        decision["outcome"] = "FAIL_T"
    elif not cost_ok:
        decision["outcome"] = "FAIL_COST_SHARE"
    elif isinstance(ftmo_out, dict) and ftmo_out.get("p95_daily_loss_ok") is False:
        decision["outcome"] = "FAIL_P95_DD"
    elif isinstance(ftmo_out, dict) and ftmo_out.get("ev_per_attempt_ok") is False:
        decision["outcome"] = "FAIL_FTMO_EV"
    elif isinstance(ftmo_out, dict) and "error" in ftmo_out:
        decision["outcome"] = "FAIL_FTMO_DATA"
    else:
        decision["outcome"] = "PASS_CANDIDATE"

    (OUT_DIR / "trial_lunch_open.json").write_text(json.dumps(decision, indent=2, default=str))

    md = [
        "# S2 LUNCH_OPEN — formele trial (na cost-gate PASS)",
        "",
        "Datum: 2026-10-01 ~02:55 CEST | PREREG_S2_LUNCH_OPEN | Reserve 2025→ onaangeraakt.",
        "",
        "## Day-clustered netto (bp)",
        "",
        "| Window | N trades | N days | mean netto/trade | t (day-clust) | skew day |",
        "|--------|---------:|-------:|-----------------:|--------------:|---------:|",
    ]
    for w in ("train", "test"):
        s = stats[w]
        md.append(
            f"| {w} | {s['N_trades']} | {s['N_days']} | {s.get('mean_netto_trade')} | "
            f"{s.get('t_day_clustered')} | {s.get('skew_day')} |"
        )
    md += [
        "",
        f"**t_ok (≥2.0 train&test, mean netto>0, N≥150):** {t_ok}",
        f"**cost_ok (mean RT < 50% mean bruto):** {cost_ok} (frac={tr.get('frac_cost_of_bruto')})",
        f"**skew_ok (day PnL > 0):** {skew_ok}",
        "",
        "## ftmo_ev (train nonzero days, 0.75% risk, n_paths=5000)",
        "",
        "```json",
        json.dumps(ftmo_out, indent=2, default=str),
        "```",
        "",
        f"## **Uitkomst: {decision['outcome']}**",
        "",
        "PASS_CANDIDATE → shortlist/Manager. FAIL_* → STOP (TRIAL_COUNT already +1 on cost-gate PASS).",
    ]
    (OUT_DIR / "trial_lunch_open.md").write_text("\n".join(md))
    print("OUTCOME:", decision["outcome"])
    print(json.dumps(ftmo_out, indent=2, default=str))
    return decision


if __name__ == "__main__":
    main()
