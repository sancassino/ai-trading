#!/usr/bin/env python3
"""PREREG_FTMO_IDX_SHORT_TSMOM — cost-gate + formal train/test.

Frozen rule: PREREG_FTMO_IDX_SHORT_TSMOM.md (CTO C-024 / D-100).
US100.cash + US30.cash, L20/H10 short-only (cheap overnight side).
Bruto-prijs gate: mean bruto ≥ 3× (RT + swap_gate) per trade.
Train 2010–2016 / test 2017–2024. Reserve 2025→ untouched.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/idx_short_tsmom"

LOOKBACK = 20
HOLD = 10
VOL_WINDOW = 20
VOL_TARGET = 0.10

TRAIN_START = pd.Timestamp("2010-01-01")
TRAIN_END = pd.Timestamp("2016-12-31")
TEST_START = pd.Timestamp("2017-01-01")
TEST_END = pd.Timestamp("2024-12-31")

SWAP_STRESS = 1.50

INSTRUMENTS = {
    "US100.cash": {"proxy": "NDX", "costs_sym": "US100cash"},
    "US30.cash": {"proxy": "DJI", "costs_sym": "US30cash"},
}


def load_proxy(proxy: str) -> pd.Series:
    path = ROOT / "data" / "daily" / f"{proxy}.csv"
    df = pd.read_csv(path, sep=";", comment="#")
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").dropna(subset=["close"])
    df = df[df["date"].dt.year < 2025]
    return df.set_index("date")["close"].astype(float)


def load_costs(costs_sym: str) -> dict:
    """COSTS_FTMO.csv: kosten per nacht; negatief = je ontvangt (credit)."""
    path = ROOT / "COSTS_FTMO.csv"
    df = pd.read_csv(path, sep=";", comment="#")
    row = df[df["symbol"] == costs_sym].iloc[0]
    rt_bp = float(row["roundtrip_intraday_bp"])
    swap_short = float(row["swap_short_bp_per_nacht"])
    return {"rt_bp": rt_bp, "swap_short_bp_night": swap_short}


def realized_vol_series(prices: pd.Series) -> pd.Series:
    return prices.pct_change().rolling(VOL_WINDOW).std() * math.sqrt(252)


def simulate(
    prices: pd.Series,
    costs: dict,
    window_start: pd.Timestamp,
    window_end: pd.Timestamp,
    swap_multiplier: float = 1.0,
) -> pd.DataFrame:
    """L20/H10 short-only simulation.

    Signal at close of t: s = sign(P_t/P_{t-20}-1); short only if s < 0.
    Entry at close of t+1. Exit at close of t+1+HOLD.
    No overlapping trades; after exit, flat until next short signal.
    Bruto = price P&L of short = (entry/exit - 1) in bp.
    """
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
        if not (sig == sig) or sig >= 0:
            continue

        loc = all_dates.get_loc(day_t)
        entry_loc = loc + 1
        exit_loc = loc + 1 + HOLD
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

        # Signed swap: positive = pay, negative = credit (COSTS_FTMO).
        swap_night_signed = costs["swap_short_bp_night"] * swap_multiplier
        swap_cost_bp = swap_night_signed * cal_nights
        # Gate: credits → 0
        swap_gate_bp = max(costs["swap_short_bp_night"], 0.0) * cal_nights * (
            1.0 if swap_multiplier == 1.0 else swap_multiplier
        )
        # For stress: inflate the paying side only
        if swap_multiplier != 1.0:
            swap_gate_bp = max(costs["swap_short_bp_night"], 0.0) * cal_nights * swap_multiplier

        # Short bruto price return
        bruto_bp = (entry_px / exit_px - 1.0) * 10000.0
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
                "entry_px": round(entry_px, 4),
                "exit_px": round(exit_px, 4),
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


def summarize_pool(df_map: dict[str, pd.DataFrame], label: str) -> dict:
    sym_stats: dict[str, dict] = {}
    frames = []
    for sym, df in df_map.items():
        if df is None or df.empty:
            sym_stats[sym] = {"N": 0}
            continue
        sym_stats[sym] = {
            "N": int(len(df)),
            "mean_bruto": round(float(df["bruto_bp"].mean()), 4),
            "mean_netto": round(float(df["netto_bp"].mean()), 4),
        }
        frames.append(df)

    if not frames:
        return {"label": label, "N": 0, "gate_3x": False, "sym": sym_stats}

    pool = pd.concat(frames, ignore_index=True)
    n = int(len(pool))
    mean_bruto = float(pool["bruto_bp"].mean())
    mean_netto = float(pool["netto_bp"].mean())
    mean_rt = float(pool["rt_bp"].mean())
    mean_swap_gate = float(pool["swap_gate_bp"].mean())
    mean_cost = mean_rt + mean_swap_gate
    gate_thresh = 3.0 * mean_cost
    # PREREG cost-gate: mean bruto ≥ 3× cost (N≥150 required for formal toets)
    gate_3x = bool(mean_bruto >= gate_thresh)

    daily_netto = pool.groupby("entry_date")["netto_bp"].sum()
    daily_bruto = pool.groupby("entry_date")["bruto_bp"].sum()

    dates_sorted = sorted(pool["entry_date"].unique())
    mid = len(dates_sorted) // 2
    h1_set = set(dates_sorted[:mid])
    h2_set = set(dates_sorted[mid:])
    h1 = pool[pool["entry_date"].isin(h1_set)]
    h2 = pool[pool["entry_date"].isin(h2_set)]

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
        "sym": sym_stats,
    }


def decide(tr: dict, te: dict | None) -> str:
    if not tr.get("gate_3x"):
        return "FAIL_COST_GATE"

    def both_ok(s: dict) -> bool:
        return (
            s.get("N", 0) >= 5
            and (s.get("mean_netto_bp") or -1) > 0
            and (s.get("t_day_clust_netto") or 0) >= 2.0
            and (s.get("mean_h1_bruto") or -1) > 0
            and (s.get("mean_h2_bruto") or -1) > 0
            and (s.get("mean_h1_netto") or -1) > 0
            and (s.get("mean_h2_netto") or -1) > 0
        )

    train_ok = tr.get("N", 0) >= 150 and both_ok(tr)

    test_ok = te is not None and te.get("N", 0) >= 150 and both_ok(te) and all(
        (v.get("mean_bruto") or -1) >= 0
        for v in te.get("sym", {}).values()
        if v.get("N", 0) > 0
    )

    if train_ok and test_ok:
        return "PASS_CANDIDATE"
    return "FAIL_T"


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    prices: dict[str, pd.Series] = {}
    costs_map: dict[str, dict] = {}
    for sym, meta in INSTRUMENTS.items():
        prices[sym] = load_proxy(meta["proxy"])
        costs_map[sym] = load_costs(meta["costs_sym"])
        c = costs_map[sym]
        print(
            f"{sym}: {len(prices[sym])} bars  RT={c['rt_bp']:.3f} bp  "
            f"swap_short={c['swap_short_bp_night']:.3f} bp/night",
            flush=True,
        )

    print("Train 2010–2016…", flush=True)
    train_df: dict[str, pd.DataFrame] = {}
    train_stress_df: dict[str, pd.DataFrame] = {}
    for sym in INSTRUMENTS:
        train_df[sym] = simulate(prices[sym], costs_map[sym], TRAIN_START, TRAIN_END, 1.0)
        train_stress_df[sym] = simulate(
            prices[sym], costs_map[sym], TRAIN_START, TRAIN_END, SWAP_STRESS
        )
        print(f"  {sym} train={len(train_df[sym])} trades", flush=True)

    tr = summarize_pool(train_df, "train")
    tr_stress = summarize_pool(train_stress_df, "train_stress")

    for sym, df in train_df.items():
        df.to_csv(OUT / f"train_{sym.replace('.', '_')}.csv", index=False)

    te = None
    if tr.get("gate_3x"):
        print("Gate PASS — test 2017–2024…", flush=True)
        test_df: dict[str, pd.DataFrame] = {}
        for sym in INSTRUMENTS:
            test_df[sym] = simulate(prices[sym], costs_map[sym], TEST_START, TEST_END, 1.0)
            print(f"  {sym} test={len(test_df[sym])} trades", flush=True)
        te = summarize_pool(test_df, "test")
        for sym, df in test_df.items():
            df.to_csv(OUT / f"test_{sym.replace('.', '_')}.csv", index=False)
    else:
        print("Gate FAIL — skipping test window.", flush=True)

    outcome = decide(tr, te)
    counts_trial = outcome != "FAIL_COST_GATE"

    board = {
        "prereg": "PREREG_FTMO_IDX_SHORT_TSMOM.md",
        "decision": "D-100",
        "c": "C-024",
        "universe": list(INSTRUMENTS.keys()),
        "rule": "L20/H10 short-only; cheap overnight (swap_short)",
        "outcome": outcome,
        "counts_as_trial": counts_trial,
        "reserve_2025": "untouched",
        "costs_source": "COSTS_FTMO.csv",
        "train": tr,
        "train_stress": tr_stress,
        "test": te,
    }
    (OUT / "idx_short_tsmom_board.json").write_text(json.dumps(board, indent=2) + "\n")

    def fmt(v):
        return str(v) if v is not None else "—"

    md_lines = [
        "# PREREG_FTMO_IDX_SHORT_TSMOM — cost-gate + formal train/test",
        "",
        "PREREG: `PREREG_FTMO_IDX_SHORT_TSMOM.md` (CTO C-024 / D-100).",
        "Rule: L20/H10 **short-only**; US100.cash + US30.cash via NDX/DJI.",
        "Costs: `COSTS_FTMO.csv` RT + swap_short (credits→0 in gate). Alfa = bruto prijs.",
        "Train 2010–2016 / test 2017–2024. Reserve 2025→ **untouched**.",
        "",
        f"**Uitkomst: {outcome}** (counts_as_trial={counts_trial})",
        "",
        "## Train 2010–2016",
        "",
        "| Metric | Waarde |",
        "|--------|-------:|",
        f"| N_trades | {fmt(tr.get('N'))} |",
        f"| mean bruto bp | {fmt(tr.get('mean_bruto_bp'))} |",
        f"| mean RT bp | {fmt(tr.get('mean_rt_bp'))} |",
        f"| mean swap bp (gate) | {fmt(tr.get('mean_swap_gate_bp'))} |",
        f"| mean cost bp | {fmt(tr.get('mean_cost_bp'))} |",
        f"| gate 3× = {fmt(tr.get('gate_3x_threshold'))} | {'**PASS**' if tr.get('gate_3x') else '**FAIL**'} |",
        f"| mean netto bp | {fmt(tr.get('mean_netto_bp'))} |",
        f"| t day-clust netto | {fmt(tr.get('t_day_clust_netto'))} |",
        f"| t NW L=5 netto | {fmt(tr.get('t_nw_L5_netto'))} |",
        f"| h1 bruto / h2 bruto | {fmt(tr.get('mean_h1_bruto'))} / {fmt(tr.get('mean_h2_bruto'))} |",
        f"| h1 netto / h2 netto | {fmt(tr.get('mean_h1_netto'))} / {fmt(tr.get('mean_h2_netto'))} |",
        "",
        "Train_stress +50% swap gate_3x: "
        + ("PASS" if tr_stress.get("gate_3x") else "FAIL"),
        "",
        "Symbol breakdown (train):",
        "",
        "| Symbol | N | mean bruto | mean netto |",
        "|--------|---|------------|------------|",
    ]
    for sym, s in tr.get("sym", {}).items():
        md_lines.append(
            f"| {sym} | {s.get('N')} | {fmt(s.get('mean_bruto'))} | {fmt(s.get('mean_netto'))} |"
        )

    if te:
        md_lines += [
            "",
            "## Test 2017–2024",
            "",
            "| Metric | Waarde |",
            "|--------|-------:|",
            f"| N_trades | {fmt(te.get('N'))} |",
            f"| mean bruto bp | {fmt(te.get('mean_bruto_bp'))} |",
            f"| mean netto bp | {fmt(te.get('mean_netto_bp'))} |",
            f"| t day-clust netto | {fmt(te.get('t_day_clust_netto'))} |",
            f"| t NW L=5 netto | {fmt(te.get('t_nw_L5_netto'))} |",
            f"| h1 bruto / h2 bruto | {fmt(te.get('mean_h1_bruto'))} / {fmt(te.get('mean_h2_bruto'))} |",
            f"| h1 netto / h2 netto | {fmt(te.get('mean_h1_netto'))} / {fmt(te.get('mean_h2_netto'))} |",
            "",
            "Symbol breakdown (test):",
            "",
            "| Symbol | N | mean bruto | mean netto |",
            "|--------|---|------------|------------|",
        ]
        for sym, s in te.get("sym", {}).items():
            md_lines.append(
                f"| {sym} | {s.get('N')} | {fmt(s.get('mean_bruto'))} | {fmt(s.get('mean_netto'))} |"
            )

    (OUT / "idx_short_tsmom_report.md").write_text("\n".join(md_lines) + "\n")

    summary = {
        "outcome": outcome,
        "N_train": tr.get("N"),
        "mean_bruto_train": tr.get("mean_bruto_bp"),
        "mean_cost_train": tr.get("mean_cost_bp"),
        "gate_3x_threshold": tr.get("gate_3x_threshold"),
        "gate_3x": tr.get("gate_3x"),
        "t_clust_train": tr.get("t_day_clust_netto"),
        "t_clust_test": te.get("t_day_clust_netto") if te else None,
        "counts_as_trial": counts_trial,
    }
    print(json.dumps(summary, indent=2), flush=True)
    return board


if __name__ == "__main__":
    main()
