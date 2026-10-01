#!/usr/bin/env python3
"""N6 GER40 Pre-Close Conditional Momentum cost gate — train 2021–2023.
PREREG_FTMO_N6_GER40_CLOSE.md (Strateeg cb786f1 / C-007).
m5gz treated as Amsterdam wall clock (same as N3/N4 U2 convention).
Times CET in PREREG = AMS wall: trend 13:30→15:30, entry 17:30, exit 17:55.
Reserve 2025→ untouched. FAIL → STOP, no TRIALS.
"""
from __future__ import annotations
import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RT = 1.40  # PREREG §1 frozen (not COSTS CSV 0.72)
GATE = 3 * RT  # 4.20 bp
ATR_N = 14
TREND_FRAC = 0.002  # 0.20%
STOP_ATR = 0.75
OUT_DIR = ROOT / "results" / "R2" / "n6_prep"


def load_m5() -> pd.DataFrame:
    path = ROOT / "data" / "m5gz" / "GER40cash.csv.gz"
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


def bar_at(group: pd.DataFrame, h: int, m: int, field: str = "close") -> float | None:
    mask = (group["time"].dt.hour == h) & (group["time"].dt.minute == m)
    rows = group[mask]
    return float(rows[field].iloc[0]) if not rows.empty else None


def sim_day(group: pd.DataFrame, atr: float) -> float | None:
    # Trend: close 15:30 vs open 13:30
    c_1530 = bar_at(group, 15, 30, "close")
    o_1330 = bar_at(group, 13, 30, "open")
    if c_1530 is None or o_1330 is None or o_1330 == 0:
        return None
    if c_1530 > o_1330 * (1 + TREND_FRAC):
        side = 1
    elif c_1530 < o_1330 * (1 - TREND_FRAC):
        side = -1
    else:
        return None

    entry_px = bar_at(group, 17, 30, "close")
    if entry_px is None:
        return None

    stop_dist = STOP_ATR * atr
    stop_px = entry_px - side * stop_dist

    exit_bar = bar_at(group, 17, 55, "close")
    if exit_bar is None:
        mask = (group["time"].dt.hour == 17) & (group["time"].dt.minute >= 50)
        rows = group[mask]
        exit_bar = float(rows["close"].iloc[-1]) if not rows.empty else None
    if exit_bar is None:
        return None

    t_entry = group[(group["time"].dt.hour == 17) & (group["time"].dt.minute == 30)]
    if t_entry.empty:
        return None
    t_entry_ts = t_entry.iloc[0]["time"]
    hold = group[(group["time"] > t_entry_ts) &
                 ((group["time"].dt.hour < 17) |
                  ((group["time"].dt.hour == 17) & (group["time"].dt.minute <= 55)))]
    exit_px = exit_bar
    for _, row in hold.iterrows():
        if side == 1 and float(row["low"]) <= stop_px:
            exit_px = stop_px
            break
        if side == -1 and float(row["high"]) >= stop_px:
            exit_px = stop_px
            break

    return side * 1e4 * (exit_px - entry_px) / entry_px


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
        if pd.isna(atr_val) or atr_val <= 0:
            continue
        # Need enough intraday bars (skip daily-only sparse 2021 months)
        if len(group) < 20:
            continue
        b = sim_day(group.copy(), atr_val)
        if b is not None:
            trades.append({"date": str(date.date()), "bruto_bp": round(b, 4), "rt": RT})

    if not trades:
        result = {"N": 0, "mean_bruto": None, "gate": GATE, "rt": RT, "outcome": "FAIL_NO_TRADES"}
    else:
        bruto = [t["bruto_bp"] for t in trades]
        mean_b = float(np.mean(bruto))
        result = {
            "N": len(trades),
            "mean_bruto": round(mean_b, 4),
            "median_bruto": round(float(np.median(bruto)), 4),
            "gate": GATE,
            "rt": RT,
            "outcome": "PASS" if mean_b >= GATE else "FAIL",
        }

    pd.DataFrame(trades).to_csv(OUT_DIR / "cost_gate_n6_train.csv", index=False)
    (OUT_DIR / "cost_gate_n6_train.json").write_text(json.dumps(result, indent=2))
    md = [
        "# N6 GER40 Pre-Close — kostenpoort TRAIN 2021–2023",
        "\nDatum: 2026-10-01 ~01:21 CEST | PREREG_FTMO_N6_GER40_CLOSE | Geen 2025+ bars.",
        "\n| Metriek | Waarde |",
        "|----|-----|",
        f"| N trades | {result['N']} |",
        f"| mean bruto | {result['mean_bruto']} bp |",
        f"| gate (3×{RT} bp) | {GATE} bp |",
        f"| **Uitkomst** | **{result['outcome']}** |",
        "\nDecisieregel: mean bruto ≥ 4,20 bp → PASS; anders STOP, geen trial.",
    ]
    (OUT_DIR / "cost_gate_n6_train.md").write_text("\n".join(md))
    print(f"N6 GER40 Close: N={result['N']} mean={result['mean_bruto']} gate={GATE} → {result['outcome']}")
    return result


if __name__ == "__main__":
    main()
