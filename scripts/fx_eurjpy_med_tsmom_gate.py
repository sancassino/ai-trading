#!/usr/bin/env python3
"""PREREG_FTMO_FX_EURJPY_MED_TSMOM — cost-gate + formal train/test.

Frozen rule: PREREG_FTMO_FX_EURJPY_MED_TSMOM.md (CTO C-027 / D-100 / D-097).
EURJPY long-only L60/H10 (cheap overnight long side).
Bruto-prijs gate: mean bruto ≥ 3× (RT + swap_gate) per trade.
Train 2000–2016 / test 2017–2024. Reserve 2025→ untouched.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/fx_eurjpy_med_tsmom"

LOOKBACK = 60
HOLD = 10
VOL_WINDOW = 20
VOL_TARGET = 0.10

TRAIN_START = pd.Timestamp("2003-01-23")
TRAIN_END = pd.Timestamp("2016-12-31")
TEST_START = pd.Timestamp("2017-01-01")
TEST_END = pd.Timestamp("2024-12-31")

SWAP_STRESS = 1.50


def load_eurjpy() -> pd.Series:
    path = ROOT / "data" / "daily" / "EURJPY.csv"
    df = pd.read_csv(path, sep=";", comment="#")
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").dropna(subset=["close"])
    df = df[df["date"].dt.year < 2025]
    return df.set_index("date")["close"].astype(float)


def load_costs() -> dict:
    path = ROOT / "COSTS_FTMO.csv"
    df = pd.read_csv(path, sep=";", comment="#")
    row = df[df["symbol"] == "EURJPY"].iloc[0]
    return {
        "rt_bp": float(row["roundtrip_intraday_bp"]),
        "swap_long_bp_night": float(row["swap_long_bp_per_nacht"]),
    }


def realized_vol_series(prices: pd.Series) -> pd.Series:
    return prices.pct_change().rolling(VOL_WINDOW).std() * math.sqrt(252)


def simulate(
    prices: pd.Series,
    costs: dict,
    window_start: pd.Timestamp,
    window_end: pd.Timestamp,
    swap_multiplier: float = 1.0,
) -> pd.DataFrame:
    rv = realized_vol_series(prices)
    mom = prices.pct_change(LOOKBACK)
    all_dates = prices.index
    mask = (all_dates >= window_start) & (all_dates <= window_end)
    window_dates = all_dates[mask].tolist()

    trades = []
    skip_before: pd.Timestamp | None = None

    for day_t in window_dates:
        if skip_before is not None and day_t < skip_before:
            continue

        sig = mom.get(day_t, np.nan)
        if not (sig == sig) or sig <= 0:
            continue

        loc = all_dates.get_loc(day_t)
        if isinstance(loc, slice):
            continue
        entry_loc = int(loc) + 1
        exit_loc = int(loc) + 1 + HOLD
        if exit_loc >= len(all_dates):
            break

        entry_day = all_dates[entry_loc]
        exit_day = all_dates[exit_loc]
        if exit_day > TEST_END:
            break

        entry_px = float(prices.iloc[entry_loc])
        exit_px = float(prices.iloc[exit_loc])
        if entry_px <= 0:
            skip_before = exit_day
            continue

        vol_at_entry = rv.get(day_t, np.nan)
        cal_nights = (exit_day - entry_day).days

        swap_night_signed = costs["swap_long_bp_night"] * swap_multiplier
        swap_cost_bp = swap_night_signed * cal_nights
        swap_gate_bp = max(costs["swap_long_bp_night"], 0.0) * cal_nights
        if swap_multiplier != 1.0:
            swap_gate_bp = max(costs["swap_long_bp_night"], 0.0) * cal_nights * swap_multiplier

        bruto_bp = (exit_px / entry_px - 1.0) * 10000.0
        netto_bp = bruto_bp - costs["rt_bp"] - swap_cost_bp

        pos = (
            (VOL_TARGET / float(vol_at_entry))
            if (vol_at_entry == vol_at_entry and vol_at_entry > 0)
            else np.nan
        )

        trades.append(
            {
                "signal_date": str(day_t.date()),
                "entry_date": str(entry_day.date()),
                "exit_date": str(exit_day.date()),
                "year": int(entry_day.year),
                "cal_nights": int(cal_nights),
                "entry_px": round(entry_px, 6),
                "exit_px": round(exit_px, 6),
                "bruto_bp": round(bruto_bp, 4),
                "rt_bp": round(costs["rt_bp"], 4),
                "swap_cost_bp": round(swap_cost_bp, 4),
                "swap_gate_bp": round(swap_gate_bp, 4),
                "netto_bp": round(netto_bp, 4),
                "pos_size": round(pos, 4) if pos == pos else None,
            }
        )
        skip_before = exit_day

    return pd.DataFrame(trades)


def t_plain(x) -> float:
    x = np.asarray(x, float)
    if len(x) <= 2 or x.std(ddof=1) <= 0:
        return float("nan")
    return float(x.mean() / x.std(ddof=1) * math.sqrt(len(x)))


def t_nw(x, L: int = 5) -> float:
    x = np.asarray(x, float)
    n = len(x)
    if n <= 2:
        return float("nan")
    e = x - x.mean()
    s = float(e @ e / n)
    for k in range(1, L + 1):
        s += 2 * (1 - k / (L + 1)) * float(e[k:] @ e[:-k] / n)
    if s <= 0:
        return float("nan")
    return float(x.mean() / math.sqrt(s / n))


def summarize(df: pd.DataFrame, label: str) -> dict:
    if df is None or df.empty:
        return {"label": label, "N": 0, "gate_3x": False}

    n = int(len(df))
    mean_bruto = float(df["bruto_bp"].mean())
    mean_netto = float(df["netto_bp"].mean())
    mean_rt = float(df["rt_bp"].mean())
    mean_swap_gate = float(df["swap_gate_bp"].mean())
    mean_cost = mean_rt + mean_swap_gate
    gate_thresh = 3.0 * mean_cost
    gate_3x = bool(mean_bruto >= gate_thresh)

    daily_netto = df.groupby("entry_date")["netto_bp"].sum()
    daily_bruto = df.groupby("entry_date")["bruto_bp"].sum()

    dates_sorted = sorted(df["entry_date"].unique())
    mid = len(dates_sorted) // 2
    h1_set = set(dates_sorted[:mid])
    h2_set = set(dates_sorted[mid:])
    h1 = df[df["entry_date"].isin(h1_set)]
    h2 = df[df["entry_date"].isin(h2_set)]

    def safe_mean(df2, col):
        return round(float(df2[col].mean()), 4) if len(df2) > 0 else None

    return {
        "label": label,
        "N": n,
        "mean_bruto_bp": round(mean_bruto, 4),
        "mean_netto_bp": round(mean_netto, 4),
        "mean_rt_bp": round(mean_rt, 4),
        "mean_swap_gate_bp": round(mean_swap_gate, 4),
        "mean_cost_bp": round(mean_cost, 4),
        "gate_3x_threshold": round(gate_thresh, 4),
        "gate_3x": gate_3x,
        "t_day_clust_netto": round(t_plain(daily_netto.values), 4),
        "t_nw_L5_netto": round(t_nw(daily_netto.values, 5), 4),
        "t_day_clust_bruto": round(t_plain(daily_bruto.values), 4),
        "mean_h1_bruto": safe_mean(h1, "bruto_bp"),
        "mean_h2_bruto": safe_mean(h2, "bruto_bp"),
        "mean_h1_netto": safe_mean(h1, "netto_bp"),
        "mean_h2_netto": safe_mean(h2, "netto_bp"),
    }


def decide(tr: dict, te: dict | None) -> str:
    if not tr.get("gate_3x"):
        return "FAIL_COST_GATE"

    def both_ok(s: dict, min_n: int) -> bool:
        return (
            s.get("N", 0) >= min_n
            and (s.get("mean_netto_bp") or -1) > 0
            and (s.get("t_day_clust_netto") or 0) >= 2.0
            and (s.get("mean_h1_bruto") or -1) > 0
            and (s.get("mean_h2_bruto") or -1) > 0
            and (s.get("mean_h1_netto") or -1) > 0
            and (s.get("mean_h2_netto") or -1) > 0
        )

    # PREREG §4: train N≥150; test N≥100 solo FX
    train_ok = both_ok(tr, 150)
    test_ok = te is not None and both_ok(te, 100) and (te.get("mean_bruto_bp") or -1) >= 0
    if train_ok and test_ok:
        return "PASS_CANDIDATE"
    return "FAIL_T"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    costs = load_costs()
    prices = load_eurjpy()

    train_df = simulate(prices, costs, TRAIN_START, TRAIN_END)
    test_df = simulate(prices, costs, TEST_START, TEST_END)
    stress_df = simulate(prices, costs, TRAIN_START, TRAIN_END, swap_multiplier=SWAP_STRESS)

    train_df.to_csv(OUT / "train_EURJPY.csv", index=False)
    test_df.to_csv(OUT / "test_EURJPY.csv", index=False)

    tr = summarize(train_df, "train")
    te = summarize(test_df, "test")
    st = summarize(stress_df, "train_stress")
    outcome = decide(tr, te)

    board = {
        "prereg": "PREREG_FTMO_FX_EURJPY_MED_TSMOM.md",
        "decision": "D-100",
        "c": "C-027",
        "universe": ["EURJPY"],
        "rule": "L60/H10 long-only; cheap overnight (swap_long)",
        "outcome": outcome,
        "counts_as_trial": outcome != "FAIL_COST_GATE",
        "reserve_2025": "untouched",
        "costs_source": "COSTS_FTMO.csv EURJPY",
        "train": tr,
        "train_stress": st,
        "test": te,
    }
    (OUT / "fx_eurjpy_med_tsmom_board.json").write_text(json.dumps(board, indent=2) + "\n")

    lines = [
        "# PREREG_FTMO_FX_EURJPY_MED_TSMOM — cost-gate + formal train/test",
        "",
        "PREREG: `PREREG_FTMO_FX_EURJPY_MED_TSMOM.md` (CTO C-027 / D-100).",
        "Rule: L60/H10 **long-only**; EURJPY.",
        "Costs: COSTS_FTMO RT + swap_long (credits→0 in gate). Alfa = bruto prijs.",
        "Train 2000–2016 / test 2017–2024. Reserve 2025→ **untouched**.",
        "",
        f"**Uitkomst: {outcome}** (counts_as_trial={board['counts_as_trial']})",
        "",
        "## Train 2000–2016",
        "",
        f"| Metric | Waarde |",
        f"|--------|-------:|",
        f"| N_trades | {tr.get('N')} |",
        f"| mean bruto bp | {tr.get('mean_bruto_bp')} |",
        f"| mean cost bp | {tr.get('mean_cost_bp')} |",
        f"| gate 3× | {tr.get('gate_3x_threshold')} | **{'PASS' if tr.get('gate_3x') else 'FAIL'}** |",
        f"| t day-clust netto | {tr.get('t_day_clust_netto')} |",
        f"| t NW L=5 netto | {tr.get('t_nw_L5_netto')} |",
        f"| h1/h2 bruto | {tr.get('mean_h1_bruto')} / {tr.get('mean_h2_bruto')} |",
        "",
        f"Train_stress +50% swap gate_3x: {'PASS' if st.get('gate_3x') else 'FAIL'}",
        "",
        "## Test 2017–2024",
        "",
        f"| Metric | Waarde |",
        f"|--------|-------:|",
        f"| N_trades | {te.get('N')} |",
        f"| mean bruto bp | {te.get('mean_bruto_bp')} |",
        f"| mean netto bp | {te.get('mean_netto_bp')} |",
        f"| t day-clust netto | {te.get('t_day_clust_netto')} |",
        f"| h1/h2 bruto | {te.get('mean_h1_bruto')} / {te.get('mean_h2_bruto')} |",
        "",
    ]
    (OUT / "fx_eurjpy_med_tsmom_report.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"outcome": outcome, "train_N": tr.get("N"), "train_bruto": tr.get("mean_bruto_bp"),
                      "gate": tr.get("gate_3x"), "test_N": te.get("N"), "test_bruto": te.get("mean_bruto_bp")}, indent=2))


if __name__ == "__main__":
    main()
