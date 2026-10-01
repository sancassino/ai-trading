#!/usr/bin/env python3
"""S2 VWAP_PB cost gate — train 2021–2023. PREREG_S2_VWAP_PB.md (C-007).
Morning-trend VWAP pullback continuation on US100/US30.
m5gz = Amsterdam wall clock; US cash open ≈ 15:30 AMS (U2 N3 convention).
Reserve 2025→ untouched.
"""
from __future__ import annotations
import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
M5 = ROOT / "data" / "m5gz"
RT = {"US100cash": 0.66, "US30cash": 0.45}
ATR_N = 14
BIAS_K = 0.30
STOP_ATR = 0.50
# Session relative to US cash open (15:30 AMS)
OPEN_H, OPEN_M = 15, 30
T90 = 90
ENTRY_START, ENTRY_END = 105, 210
FLAT_MIN = 300
OUT_DIR = ROOT / "results" / "R2" / "vwap_pb_prep"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")


def load_m5(sym: str) -> pd.DataFrame:
    with gzip.open(M5 / f"{sym}.csv.gz", "rt") as f:
        for line in f:
            if not line.startswith("#"):
                break
        df = pd.read_csv(f, sep=";", names=["time", "open", "high", "low", "close", "spread"])
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["close"]).sort_values("time").reset_index(drop=True)
    return df[(df["time"] >= TRAIN_START) & (df["time"] <= TRAIN_END)]


def daily_atr_map(df: pd.DataFrame) -> dict:
    day_df = df.set_index("time").resample("1D").agg(
        high=("high", "max"), low=("low", "min"), close=("close", "last")
    ).dropna()
    tr_list, prev = [], None
    for _, row in day_df.iterrows():
        if prev is None:
            tr_list.append(row["high"] - row["low"])
        else:
            tr_list.append(max(row["high"] - row["low"],
                               abs(row["high"] - prev), abs(row["low"] - prev)))
        prev = row["close"]
    day_df["atr"] = pd.Series(tr_list, index=day_df.index).rolling(ATR_N).mean()
    return day_df["atr"].dropna().to_dict()


def sim_day(g: pd.DataFrame, atr_price: float, rt: float):
    if len(g) < 30 or not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    t0 = day0 + pd.Timedelta(hours=OPEN_H, minutes=OPEN_M)
    # Prefer exact open bar
    open_bars = g[(g["time"].dt.hour == OPEN_H) & (g["time"].dt.minute == OPEN_M)]
    if open_bars.empty:
        after = g[g["time"] >= t0]
        if after.empty:
            return None
        open_row = after.iloc[0]
        t0 = open_row["time"]
    else:
        open_row = open_bars.iloc[0]
        t0 = open_row["time"]
    p_open = float(open_row["open"])
    if p_open <= 0:
        return None
    atr_bp = 1e4 * atr_price / p_open

    t90 = t0 + pd.Timedelta(minutes=T90)
    bar_t90 = g[(g["time"] >= t90) & (g["time"] <= t90 + pd.Timedelta(minutes=5))]
    if bar_t90.empty:
        # nearest bar at/after t90 within 15 min
        bar_t90 = g[(g["time"] >= t90) & (g["time"] <= t90 + pd.Timedelta(minutes=15))]
    if bar_t90.empty:
        return None
    p_t90 = float(bar_t90.iloc[0]["close"])
    morn_bp = 1e4 * (p_t90 - p_open) / p_open
    if morn_bp >= BIAS_K * atr_bp:
        side = 1
    elif morn_bp <= -BIAS_K * atr_bp:
        side = -1
    else:
        return None

    # Morning extreme for target
    morn_sess = g[(g["time"] >= t0) & (g["time"] <= t90 + pd.Timedelta(minutes=5))]
    if morn_sess.empty:
        return None
    h_morn = float(morn_sess["high"].max())
    l_morn = float(morn_sess["low"].min())

    # Session for VWAP from open
    sess = g[g["time"] >= t0].copy()
    if sess.empty:
        return None
    sess["tp"] = (sess["high"] + sess["low"] + sess["close"]) / 3.0
    sess["vwap"] = sess["tp"].expanding().mean()

    entry_lo = t0 + pd.Timedelta(minutes=ENTRY_START)
    entry_hi = t0 + pd.Timedelta(minutes=ENTRY_END)
    window = sess[(sess["time"] >= entry_lo) & (sess["time"] <= entry_hi)]
    if window.empty:
        return None

    entry_row = None
    for _, row in window.iterrows():
        vwap = float(row["vwap"])
        lo, hi, c = float(row["low"]), float(row["high"]), float(row["close"])
        if lo <= vwap <= hi:
            if side == 1 and c >= vwap:
                entry_row = row
                break
            if side == -1 and c <= vwap:
                entry_row = row
                break
    if entry_row is None:
        return None

    entry = float(entry_row["close"])
    vwap_e = float(entry_row["vwap"])
    # Stop: 0.50×atr_bp past VWAP against bias
    stop_dist_px = (STOP_ATR * atr_bp / 1e4) * entry  # price units approx via entry
    # PREREG: stop past VWAP against bias — LONG stop under VWAP, SHORT above VWAP
    if side == 1:
        stop_px = vwap_e - stop_dist_px
        target_px = h_morn
    else:
        stop_px = vwap_e + stop_dist_px
        target_px = l_morn

    t_flat = t0 + pd.Timedelta(minutes=FLAT_MIN)
    after = sess[(sess["time"] > entry_row["time"]) & (sess["time"] <= t_flat)]
    if after.empty:
        return None
    exit_px = float(after.iloc[-1]["close"])
    for _, row in after.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        hit_s = (side == 1 and lo <= stop_px) or (side == -1 and hi >= stop_px)
        hit_t = (side == 1 and hi >= target_px) or (side == -1 and lo <= target_px)
        if hit_s and hit_t:
            exit_px = stop_px
            break
        if hit_s:
            exit_px = stop_px
            break
        if hit_t:
            exit_px = target_px
            break
    bruto = side * 1e4 * (exit_px - entry) / entry
    return {"bruto_bp": bruto, "rt": rt, "side": side, "morn_bp": morn_bp}


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    trades = []
    for sym, rt in RT.items():
        m5 = load_m5(sym)
        atr = daily_atr_map(m5)
        for day, g in m5.groupby(m5["time"].dt.normalize()):
            prior = {d: v for d, v in atr.items() if pd.Timestamp(d) < day}
            if len(prior) < ATR_N:
                continue
            atr_val = list(prior.values())[-1]
            if pd.isna(atr_val) or atr_val <= 0:
                continue
            r = sim_day(g, atr_val, rt)
            if r is not None:
                trades.append({"date": str(day.date()), "sym": sym,
                               **{k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()}})

    if not trades:
        result = {"N": 0, "mean_bruto": None, "tw_rt": None, "gate": None, "outcome": "FAIL_NO_TRADES"}
    else:
        bruto = np.array([t["bruto_bp"] for t in trades], dtype=float)
        rts = np.array([t["rt"] for t in trades], dtype=float)
        mean_b = float(bruto.mean())
        tw_rt = float(rts.mean())
        gate = 3 * tw_rt
        by_sym = {}
        for sym in RT:
            sub = [t for t in trades if t["sym"] == sym]
            if sub:
                by_sym[sym] = {"N": len(sub), "mean_bruto": round(float(np.mean([t["bruto_bp"] for t in sub])), 4)}
        result = {
            "N": len(trades),
            "mean_bruto": round(mean_b, 4),
            "tw_rt": round(tw_rt, 4),
            "gate": round(gate, 4),
            "gate_stress50": round(3 * tw_rt * 1.5, 4),
            "outcome": "PASS" if mean_b >= gate else "FAIL",
            "by_sym": by_sym,
        }

    pd.DataFrame(trades).to_csv(OUT_DIR / "cost_gate_vwap_pb_train.csv", index=False)
    (OUT_DIR / "cost_gate_vwap_pb_train.json").write_text(json.dumps(result, indent=2))
    md = [
        "# S2 VWAP_PB — kostenpoort TRAIN 2021–2023",
        "\nDatum: 2026-10-01 ~01:21 CEST | PREREG_S2_VWAP_PB | Geen 2025+ bars.",
        "\n| Metriek | Waarde |",
        "|----|-----|",
        f"| N trades | {result['N']} |",
        f"| mean bruto | {result.get('mean_bruto')} bp |",
        f"| TW-RT | {result.get('tw_rt')} bp |",
        f"| gate (3×TW-RT) | {result.get('gate')} bp |",
        f"| **Uitkomst** | **{result['outcome']}** |",
        "\nFAIL → STOP, geen trial. PASS → clustered-t / ftmo_ev.",
    ]
    (OUT_DIR / "cost_gate_vwap_pb_train.md").write_text("\n".join(md))
    print(f"VWAP_PB: N={result['N']} mean={result.get('mean_bruto')} gate={result.get('gate')} → {result['outcome']}")
    return result


if __name__ == "__main__":
    main()
