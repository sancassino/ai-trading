#!/usr/bin/env python3
"""N3 US100 Close-Drive Momentum cost gate — train 2021–2023. PREREG e39e9c6.
Times in PREREG are ET; m5gz clock treated as Amsterdam wall clock (UTC+2 summer / UTC+1 winter).
ET is always 6h behind Amsterdam -> offsets: 09:30 ET = 15:30 AMS, 11:00 ET = 17:00 AMS,
  14:30 ET = 20:30 AMS, 15:55 ET = 21:55 AMS.
"""
from __future__ import annotations
import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RT = 0.60   # PREREG §1: 0.60 bp (spread+comm); gate = 3×RT = 1.80 bp
GATE = 3 * RT
ATR_N = 14
TREND_FRAC = 0.003   # 0.30%
OUT_DIR = ROOT / "results" / "R2" / "n3_prep"


def load_m5() -> pd.DataFrame:
    path = ROOT / "data" / "m5gz" / "US100cash.csv.gz"
    with gzip.open(path, "rt") as f:
        for line in f:
            if not line.startswith("#"):
                break
        df = pd.read_csv(f, sep=";", names=["time", "open", "high", "low", "close", "spread"])
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["close"]).sort_values("time").reset_index(drop=True)
    # Train window only (no 2025+)
    return df[(df["time"] >= "2021-01-01") & (df["time"] <= "2023-12-31 23:59:59")]


def daily_atr(df: pd.DataFrame) -> dict:
    """ATR14 per calendar date using day OHLC."""
    day_df = df.set_index("time").resample("1D").agg(
        high=("high", "max"), low=("low", "min"), close=("close", "last")
    ).dropna()
    tr_list = []
    prev_close = None
    for _, row in day_df.iterrows():
        if prev_close is None:
            tr_list.append(row["high"] - row["low"])
        else:
            tr_list.append(max(row["high"] - row["low"],
                               abs(row["high"] - prev_close),
                               abs(row["low"] - prev_close)))
        prev_close = row["close"]
    day_df["tr"] = tr_list
    day_df["atr"] = day_df["tr"].rolling(ATR_N).mean()
    return day_df["atr"].dropna().to_dict()


def bar_at(group: pd.DataFrame, h: int, m: int) -> float | None:
    """Return close of bar at hour:minute."""
    mask = (group["time"].dt.hour == h) & (group["time"].dt.minute == m)
    rows = group[mask]
    return float(rows["close"].iloc[0]) if not rows.empty else None


def first_bar_in(group: pd.DataFrame, h: int, m: int) -> tuple[pd.Timestamp, float] | None:
    """First bar at or after h:m."""
    mask = (group["time"].dt.hour > h) | (
        (group["time"].dt.hour == h) & (group["time"].dt.minute >= m)
    )
    rows = group[mask]
    if rows.empty:
        return None
    row = rows.iloc[0]
    return row["time"], float(row["close"])


def sim_day(date: pd.Timestamp, group: pd.DataFrame, atr: float) -> float | None:
    """Return bruto bp for one trade, or None if no signal."""
    # Trend filter: close at 17:00 AMS vs open of 15:30 AMS bar
    c_1100 = bar_at(group, 17, 0)   # 11:00 ET = 17:00 AMS
    o_0930 = bar_at(group, 15, 30)  # 09:30 ET = 15:30 AMS (open of this bar)
    if c_1100 is None or o_0930 is None:
        return None
    # Use open of 09:30 bar as the "open" price; c_1100 is close at 11:00 bar
    if c_1100 > o_0930 * (1 + TREND_FRAC):
        side = 1   # Long
    elif c_1100 < o_0930 * (1 - TREND_FRAC):
        side = -1  # Short
    else:
        return None  # No signal

    # Entry at 14:30 ET (20:30 AMS) close
    entry_px = bar_at(group, 20, 30)
    if entry_px is None:
        return None

    # Stop: 1× ATR14 from entry
    stop_dist = atr  # price units
    stop_px = entry_px - side * stop_dist

    # Exit at 15:55 ET (21:55 AMS)
    exit_bar = bar_at(group, 21, 55)
    if exit_bar is None:
        # try 21:50 or last bar before 22:00
        mask = (group["time"].dt.hour == 21) & (group["time"].dt.minute >= 50)
        rows = group[mask]
        exit_bar = float(rows["close"].iloc[-1]) if not rows.empty else None
    if exit_bar is None:
        return None

    # Check stop hit during 20:30-21:55
    t_entry = group[(group["time"].dt.hour == 20) & (group["time"].dt.minute == 30)]
    if t_entry.empty:
        return None
    t_entry_ts = t_entry.iloc[0]["time"]
    hold = group[(group["time"] > t_entry_ts) &
                 ((group["time"].dt.hour < 21) |
                  ((group["time"].dt.hour == 21) & (group["time"].dt.minute <= 55)))]
    exit_px = exit_bar
    for _, row in hold.iterrows():
        if side == 1 and float(row["low"]) <= stop_px:
            exit_px = stop_px
            break
        elif side == -1 and float(row["high"]) >= stop_px:
            exit_px = stop_px
            break

    bruto_bp = side * 1e4 * (exit_px - entry_px) / entry_px
    return bruto_bp


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_m5()
    atr_map = daily_atr(df)
    trades = []
    for date, group in df.groupby(df["time"].dt.normalize()):
        # Need ATR from previous 14 days
        prior_atrs = {d: v for d, v in atr_map.items() if pd.Timestamp(d) < date}
        if len(prior_atrs) < ATR_N:
            continue
        atr_val = list(prior_atrs.values())[-1]
        if pd.isna(atr_val):
            continue
        b = sim_day(date, group.copy(), atr_val)
        if b is not None:
            trades.append({"date": str(date.date()), "bruto_bp": round(b, 4), "rt": RT})

    if not trades:
        result = {"N": 0, "mean_bruto": None, "gate": GATE, "outcome": "FAIL_NO_TRADES"}
    else:
        bruto = [t["bruto_bp"] for t in trades]
        mean_b = float(np.mean(bruto))
        result = {
            "N": len(trades),
            "mean_bruto": round(mean_b, 4),
            "gate": GATE,
            "outcome": "PASS" if mean_b >= GATE else "FAIL",
        }

    # Write outputs
    pd.DataFrame(trades).to_csv(OUT_DIR / "cost_gate_n3_train.csv", index=False)
    (OUT_DIR / "cost_gate_n3_train.json").write_text(json.dumps(result, indent=2))

    md_lines = [
        "# N3 US100 Close-Drive — kostenpoort TRAIN 2021–2023",
        f"\nDatum: 2026-10-01 | PREREG e39e9c6 | Geen 2025+ bars.",
        f"\n| Metriek | Waarde |",
        "|----|-----|",
        f"| N trades | {result['N']} |",
        f"| mean bruto | {result['mean_bruto']} bp |",
        f"| gate (3×{RT} bp) | {GATE} bp |",
        f"| **Uitkomst** | **{result['outcome']}** |",
        "\nDecisieregel: mean bruto ≥ 1,80 bp → kostenpoort PASS; anders STOP.",
    ]
    (OUT_DIR / "cost_gate_n3_train.md").write_text("\n".join(md_lines))

    print(f"N3 US100 Close-Drive: N={result['N']} mean={result['mean_bruto']} gate={GATE} → {result['outcome']}")
    return result


if __name__ == "__main__":
    main()
