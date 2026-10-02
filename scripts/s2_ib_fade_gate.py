#!/usr/bin/env python3
"""S2 IB_FADE cost gate — train 2021–2023. PREREG_S2_IB_FADE.md (cyclus-4).

US cash Initial-Balance extreme fade on US30/US100.
m5gz = Amsterdam wall clock; IB 15:30–16:30 AMS; hard flat 20:00 AMS.
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
RT = {"US30cash": 0.45, "US100cash": 0.66}  # primary, secondary
ATR_N = 14
WIDTH_K = 0.55
POS_HI, POS_LO = 0.80, 0.20
STOP_BUF = 0.25
IB_START_H, IB_START_M = 15, 30
IB_END_H, IB_END_M = 16, 30
FLAT_H, FLAT_M = 20, 0
OUT_DIR = ROOT / "results" / "R2" / "ib_fade_prep"
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
    day_df = (
        df.set_index("time")
        .resample("1D")
        .agg(high=("high", "max"), low=("low", "min"), close=("close", "last"))
        .dropna()
    )
    tr_list, prev = [], None
    for _, row in day_df.iterrows():
        if prev is None:
            tr_list.append(row["high"] - row["low"])
        else:
            tr_list.append(
                max(
                    row["high"] - row["low"],
                    abs(row["high"] - prev),
                    abs(row["low"] - prev),
                )
            )
        prev = row["close"]
    day_df["atr"] = pd.Series(tr_list, index=day_df.index).rolling(ATR_N).mean()
    return day_df["atr"].dropna().to_dict()


def sim_day(g: pd.DataFrame, atr_price: float, rt: float):
    if len(g) < 12 or not (atr_price == atr_price) or atr_price <= 0:
        return None

    day0 = g["time"].dt.normalize().iloc[0]
    t_ib0 = day0 + pd.Timedelta(hours=IB_START_H, minutes=IB_START_M)
    t_ib1 = day0 + pd.Timedelta(hours=IB_END_H, minutes=IB_END_M)
    t_flat = day0 + pd.Timedelta(hours=FLAT_H, minutes=FLAT_M)

    # P_1530: open of 15:30 bar (or first bar at/after 15:30)
    open_bars = g[(g["time"].dt.hour == IB_START_H) & (g["time"].dt.minute == IB_START_M)]
    if open_bars.empty:
        after = g[g["time"] >= t_ib0]
        if after.empty:
            return None
        open_row = after.iloc[0]
        if open_row["time"] > t_ib0 + pd.Timedelta(minutes=30):
            return None
    else:
        open_row = open_bars.iloc[0]
    p_1530 = float(open_row["open"])
    if p_1530 <= 0:
        return None

    # IB window: bars with time in [15:30, 16:30)
    # PREREG: high/low of M5 in venster; close of 16:25–16:30 bar (or last in window)
    ib = g[(g["time"] >= t_ib0) & (g["time"] < t_ib1)]
    if ib.empty:
        return None
    # Prefer full IB coverage: need last bar near 16:25
    last_ib = ib.iloc[-1]
    if last_ib["time"] < t_ib1 - pd.Timedelta(minutes=10):
        # sparse/H1 early data — still allow if we have ≥2 bars spanning ≥45 min
        span_min = (last_ib["time"] - ib.iloc[0]["time"]).total_seconds() / 60.0
        if len(ib) < 2 or span_min < 45:
            return None

    ib_high = float(ib["high"].max())
    ib_low = float(ib["low"].min())
    if ib_high <= ib_low:
        return None
    ib_mid = 0.5 * (ib_high + ib_low)
    ib_range = ib_high - ib_low

    # P_IB_close: prefer 16:25 bar close, else last bar in IB window
    close_pref = ib[(ib["time"].dt.hour == 16) & (ib["time"].dt.minute == 25)]
    if not close_pref.empty:
        p_ib_close = float(close_pref.iloc[0]["close"])
        entry_time = close_pref.iloc[0]["time"]
    else:
        p_ib_close = float(last_ib["close"])
        entry_time = last_ib["time"]

    ib_range_bp = 1e4 * ib_range / p_1530
    atr_bp = 1e4 * atr_price / p_1530
    if ib_range_bp < WIDTH_K * atr_bp:
        return None

    pos = (p_ib_close - ib_low) / ib_range
    if pos >= POS_HI:
        side = -1  # SHORT fade upper
    elif pos <= POS_LO:
        side = 1  # LONG fade lower
    else:
        return None

    entry = p_ib_close
    target_px = ib_mid
    if side == -1:
        stop_px = ib_high + STOP_BUF * ib_range
    else:
        stop_px = ib_low - STOP_BUF * ib_range

    # Manage after entry bar through hard flat 20:00
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
            exit_px = stop_px
            reason = "stop_samebar"
            break
        if hit_s:
            exit_px = stop_px
            reason = "stop"
            break
        if hit_t:
            exit_px = target_px
            reason = "target"
            break

    bruto = side * 1e4 * (exit_px - entry) / entry
    return {
        "bruto_bp": bruto,
        "rt": rt,
        "side": side,
        "pos": pos,
        "ib_range_bp": ib_range_bp,
        "atr_bp": atr_bp,
        "reason": reason,
    }


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
                trades.append(
                    {
                        "date": str(day.date()),
                        "sym": sym,
                        **{
                            k: (round(v, 4) if isinstance(v, float) else v)
                            for k, v in r.items()
                        },
                    }
                )

    if not trades:
        result = {
            "N": 0,
            "mean_bruto": None,
            "tw_rt": None,
            "gate": None,
            "outcome": "FAIL_NO_TRADES",
        }
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
                by_sym[sym] = {
                    "N": len(sub),
                    "mean_bruto": round(float(np.mean([t["bruto_bp"] for t in sub])), 4),
                    "rt": RT[sym],
                    "gate_sym": round(3 * RT[sym], 4),
                }
        result = {
            "N": len(trades),
            "mean_bruto": round(mean_b, 4),
            "tw_rt": round(tw_rt, 4),
            "gate": round(gate, 4),
            "gate_stress50": round(3 * tw_rt * 1.5, 4),
            "outcome": "PASS" if mean_b >= gate else "FAIL",
            "by_sym": by_sym,
        }

    pd.DataFrame(trades).to_csv(OUT_DIR / "cost_gate_ib_fade_train.csv", index=False)
    (OUT_DIR / "cost_gate_ib_fade_train.json").write_text(json.dumps(result, indent=2))
    md = [
        "# S2 IB_FADE — kostenpoort TRAIN 2021–2023",
        "\nDatum: 2026-10-01 ~01:53 CEST | PREREG_S2_IB_FADE | Geen 2025+ bars.",
        "\n| Metriek | Waarde |",
        "|----|-----|",
        f"| N trades | {result['N']} |",
        f"| mean bruto | {result.get('mean_bruto')} bp |",
        f"| TW-RT | {result.get('tw_rt')} bp |",
        f"| gate (3×TW-RT) | {result.get('gate')} bp |",
        f"| **Uitkomst** | **{result['outcome']}** |",
        "\nFAIL → STOP, geen trial / geen TRIALS-append. PASS → clustered-t / ftmo_ev (N≥150).",
    ]
    (OUT_DIR / "cost_gate_ib_fade_train.md").write_text("\n".join(md))
    print(
        f"IB_FADE: N={result['N']} mean={result.get('mean_bruto')} "
        f"gate={result.get('gate')} → {result['outcome']}"
    )
    if result.get("by_sym"):
        print("by_sym:", json.dumps(result["by_sym"]))
    return result


if __name__ == "__main__":
    main()
