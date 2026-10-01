#!/usr/bin/env python3
"""D-092.1 pre-screen ONLY — N7 Post-Lunch Momentum (PLM).
Train 2021–2023; mean bruto vs 3× RT. No test/reserve. No PREREG claim.
Idea: morning directional impulse (15:30–17:30 AMS) → hold same direction
17:30→20:00 AMS. ≠ IB_FADE (continue not fade); ≠ N3 (earlier window);
≠ ORB/VWAP_PB/GER_US. Top-RT: US100/US30.
"""
from __future__ import annotations
import gzip, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
M5 = ROOT / "data" / "m5gz"
RT = {"US30cash": 0.45, "US100cash": 0.66}
# Frozen for screen only (if PASS → copy into PREREG unchanged)
THR_PCT = 0.0040  # 0.40% morning move
MORN0, MORN1 = (15, 30), (17, 30)
FLAT = (20, 0)
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
OUT = ROOT / "results" / "strateeg_prescreen" / "n7_plm"


def load_m5(sym: str) -> pd.DataFrame:
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
    return df[(df["time"] >= TRAIN_START) & (df["time"] <= TRAIN_END)]


def sim_day(g: pd.DataFrame):
    if len(g) < 20:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    t0 = day0 + pd.Timedelta(hours=MORN0[0], minutes=MORN0[1])
    t1 = day0 + pd.Timedelta(hours=MORN1[0], minutes=MORN1[1])
    tflat = day0 + pd.Timedelta(hours=FLAT[0], minutes=FLAT[1])
    b0 = g[(g["time"] >= t0) & (g["time"] < t0 + pd.Timedelta(minutes=5))]
    b1 = g[(g["time"] >= t1) & (g["time"] < t1 + pd.Timedelta(minutes=5))]
    if b0.empty or b1.empty:
        return None
    p0 = float(b0.iloc[0]["open"])
    p1 = float(b1.iloc[0]["close"])
    if p0 <= 0:
        return None
    move = p1 / p0 - 1.0
    if abs(move) < THR_PCT:
        return None
    side = 1 if move > 0 else -1
    entry = p1
    # stop = opposite of morning extreme beyond entry by 0 (use morning low/high)
    morn = g[(g["time"] >= t0) & (g["time"] <= t1)]
    mhi, mlo = float(morn["high"].max()), float(morn["low"].min())
    stop = mlo if side == 1 else mhi
    # if stop on wrong side of entry (gap), widen to 0.5× morning range
    mr = mhi - mlo
    if mr <= 0:
        return None
    if side == 1 and stop >= entry:
        stop = entry - 0.5 * mr
    if side == -1 and stop <= entry:
        stop = entry + 0.5 * mr
    # walk bars after entry to flat
    after = g[(g["time"] > t1) & (g["time"] <= tflat)]
    if after.empty:
        return None
    exit_px, reason = float(after.iloc[-1]["close"]), "time"
    for _, row in after.iterrows():
        if side == 1:
            if float(row["low"]) <= stop:
                exit_px, reason = stop, "stop"
                break
        else:
            if float(row["high"]) >= stop:
                exit_px, reason = stop, "stop"
                break
    bruto_bp = 1e4 * side * (exit_px - entry) / entry
    return {
        "date": str(day0.date()),
        "side": side,
        "move_pct": move * 100,
        "bruto_bp": bruto_bp,
        "reason": reason,
        "entry": entry,
        "exit": exit_px,
    }


def run_sym(sym: str):
    df = load_m5(sym)
    rows = []
    for _, g in df.groupby(df["time"].dt.normalize()):
        r = sim_day(g)
        if r:
            r["symbol"] = sym
            rows.append(r)
    return pd.DataFrame(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    all_dfs = []
    summary = []
    for sym, rt in RT.items():
        d = run_sym(sym)
        all_dfs.append(d)
        n = len(d)
        mean = float(d["bruto_bp"].mean()) if n else float("nan")
        gate = 3.0 * rt
        summary.append(
            {
                "symbol": sym,
                "n": n,
                "mean_bruto_bp": round(mean, 4) if n else None,
                "rt_bp": rt,
                "gate_3x_rt": gate,
                "pass": bool(n and mean >= gate),
            }
        )
        print(f"{sym}: N={n} mean={mean:.3f} bp gate={gate:.2f} → {'PASS' if (n and mean>=gate) else 'FAIL'}")
    pool = pd.concat(all_dfs, ignore_index=True) if all_dfs else pd.DataFrame()
    # trade-weighted RT for pooled gate
    if len(pool):
        w_rt = pool["symbol"].map(RT)
        tw_rt = float(w_rt.mean())
        mean_p = float(pool["bruto_bp"].mean())
        gate_p = 3.0 * tw_rt
        pooled = {
            "n": int(len(pool)),
            "mean_bruto_bp": round(mean_p, 4),
            "tw_rt_bp": round(tw_rt, 4),
            "gate_3x_tw_rt": round(gate_p, 4),
            "pass": bool(mean_p >= gate_p),
            "stop_share": float((pool["reason"] == "stop").mean()),
            "date_min": pool["date"].min(),
            "date_max": pool["date"].max(),
        }
        print(
            f"POOLED: N={pooled['n']} mean={mean_p:.3f} gate={gate_p:.2f} → {'PASS' if pooled['pass'] else 'FAIL'}"
        )
    else:
        pooled = {"n": 0, "pass": False}
    out = {
        "idea": "N7_PLM_post_lunch_momentum",
        "rule": "morning |move|≥0.40% 15:30–17:30 AMS → hold dir 17:30–20:00; stop=morning extreme",
        "train": "2021-01-01..2023-12-31",
        "reserve_2025": "untouched",
        "by_symbol": summary,
        "pooled": pooled,
        "decision": "PREREG_OK" if pooled.get("pass") else "NO_PREREG_screen_fail",
    }
    pool.to_csv(OUT / "trades_train.csv", index=False)
    (OUT / "prescreen.json").write_text(json.dumps(out, indent=2))
    print("DECISION:", out["decision"])
    return out["decision"]


if __name__ == "__main__":
    main()
