#!/usr/bin/env python3
"""N4 XAU Pre-NY Range Breakout cost gate — train 2021–2023. PREREG e39e9c6.
Times in PREREG are Amsterdam wall clock; m5gz clock treated as Amsterdam wall clock.
PNR window: 13:00-14:55 AMS. Entry: first bar >= 15:00 with close outside PNR.
Stop: opposite PNR side. Exit: 17:30 AMS.
"""
from __future__ import annotations
import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RT = 0.83   # PREREG §1: 0.83 bp (spread+comm); gate = 3×RT = 2.49 bp
GATE = 3 * RT
ATR_N = 14
MIN_PNR_FRAC = 0.001   # 0.10% minimum PNR width
OUT_DIR = ROOT / "results" / "R2" / "n4_prep"


def load_m5() -> pd.DataFrame:
    path = ROOT / "data" / "m5gz" / "XAUUSD.csv.gz"
    with gzip.open(path, "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    if "time" not in df.columns:
        # re-read with header detection
        with gzip.open(path, "rt") as f:
            for line in f:
                if not line.startswith("#"):
                    break
            df = pd.read_csv(f, sep=";", names=["time", "open", "high", "low", "close", "spread"])
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["close"]).sort_values("time").reset_index(drop=True)
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


def sim_day(date: pd.Timestamp, group: pd.DataFrame, atr: float) -> float | None:
    """Return bruto bp for one trade, or None if no signal."""
    day0 = date.normalize()

    # PNR window: 13:00-14:55 AMS (bars starting AT 13:00 through bar AT 14:55)
    pnr = group[
        (group["time"].dt.hour >= 13) &
        ((group["time"].dt.hour < 14) | ((group["time"].dt.hour == 14) & (group["time"].dt.minute <= 55)))
    ]
    if pnr.empty:
        return None

    pnr_high = float(pnr["high"].max())
    pnr_low = float(pnr["low"].min())
    pnr_mid = 0.5 * (pnr_high + pnr_low)

    # Min PNR width: 0.10% of midpoint
    if pnr_mid == 0 or (pnr_high - pnr_low) / pnr_mid < MIN_PNR_FRAC:
        return None

    # Entry: first bar at or after 15:00 with close outside PNR
    after_1500 = group[
        (group["time"].dt.hour >= 15) &
        (group["time"].dt.hour < 17)
    ]
    if after_1500.empty:
        return None

    entry_row = None
    side = None
    for _, row in after_1500.iterrows():
        c = float(row["close"])
        if c > pnr_high:
            entry_row = row
            side = 1   # Long (breakout up)
            break
        elif c < pnr_low:
            entry_row = row
            side = -1  # Short (breakout down)
            break

    if entry_row is None or side is None:
        return None

    entry_px = float(entry_row["close"])
    entry_ts = entry_row["time"]

    # Stop: opposite PNR side
    if side == 1:
        stop_px = pnr_low
    else:
        stop_px = pnr_high

    # Exit: 17:30 AMS
    exit_bar_rows = group[(group["time"].dt.hour == 17) & (group["time"].dt.minute == 30)]
    if not exit_bar_rows.empty:
        exit_bar = float(exit_bar_rows.iloc[0]["close"])
    else:
        # Last bar before 17:30
        mask = (group["time"] > entry_ts) & (
            (group["time"].dt.hour < 17) |
            ((group["time"].dt.hour == 17) & (group["time"].dt.minute <= 30))
        )
        rows = group[mask]
        exit_bar = float(rows["close"].iloc[-1]) if not rows.empty else None

    if exit_bar is None:
        return None

    # Check stop hit during hold period (after entry up to 17:30)
    hold = group[
        (group["time"] > entry_ts) &
        (
            (group["time"].dt.hour < 17) |
            ((group["time"].dt.hour == 17) & (group["time"].dt.minute <= 30))
        )
    ]
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

    pd.DataFrame(trades).to_csv(OUT_DIR / "cost_gate_n4_train.csv", index=False)
    (OUT_DIR / "cost_gate_n4_train.json").write_text(json.dumps(result, indent=2))

    md_lines = [
        "# N4 XAU Pre-NY Breakout — kostenpoort TRAIN 2021–2023",
        f"\nDatum: 2026-10-01 | PREREG e39e9c6 | Geen 2025+ bars.",
        f"\n| Metriek | Waarde |",
        "|----|-----|",
        f"| N trades | {result['N']} |",
        f"| mean bruto | {result['mean_bruto']} bp |",
        f"| gate (3×{RT} bp) | {GATE} bp |",
        f"| **Uitkomst** | **{result['outcome']}** |",
        "\nDecisieregel: mean bruto ≥ 2,49 bp → kostenpoort PASS; anders STOP.",
    ]
    (OUT_DIR / "cost_gate_n4_train.md").write_text("\n".join(md_lines))

    print(f"N4 XAU Pre-NY Breakout: N={result['N']} mean={result['mean_bruto']} gate={GATE} → {result['outcome']}")
    return result


if __name__ == "__main__":
    main()
