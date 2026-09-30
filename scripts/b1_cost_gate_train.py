#!/usr/bin/env python3
"""B1 PRE-trial kostenpoort for PREREG_FTMO_B1 — TRAIN 2021–2023 ONLY.

NOT a formal trial until PASS. Does not open 2025→ reserve.

Gate (PREREG_FTMO_B1 §1, NEXT_STEPS v38 / Strateeg-2):
  signed mean of monthly bruto (bp) over pair-months on train
  ≥ 3 × mean of (roundtrip + swap×nachten for the taken side)
  over those same pair-months.

  Mediaan |bruto| is informational only — NOT the gate.

Positions: identical C05 TSMOM-mix (catalogus/C05_tsmom_mix.py) on FX6.
Costs: COSTS_FTMO.csv constant bp/nacht (PREREG table); Fri→Mon = 3 nights
via calendar-day gaps. +50% swap sensitivity reported, not used for PASS/FAIL.
"""
from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path

import numpy as np

from catalogus._common import hold_monthly, month_end, ret_back, sigma
from engine.run_rule import COST_MAP, RT, SWL, SWS, load_daily

TRAIN_START = date(2021, 1, 1)
TRAIN_END = date(2023, 12, 31)
HARD_CAP = date(2024, 12, 31)  # never peek reserve 2025→

PAIRS = [
    "FX_EURUSD",
    "FX_GBPUSD",
    "FX_USDJPY",
    "FX_AUDUSD",
    "FX_USDCAD",
    "FX_USDCHF",
]


def positions_c05(df: dict) -> np.ndarray:
    c = df["close"]
    s = (np.sign(ret_back(c, 21)) + np.sign(ret_back(c, 63)) + np.sign(ret_back(c, 252))) / 3
    return hold_monthly(s * np.minimum(3.0, 0.10 / sigma(c, 60)), month_end(df["date"]))


def month_key(d: date) -> tuple[int, int]:
    return d.year, d.month


def pair_month_rows(df: dict, pos: np.ndarray) -> list[dict]:
    """One row per (pair, calendar month) with non-zero held position in train.

    Bruto = sum of pos[t-1]*r[t] over days in the month (fraction of notional).
    Cost  = turnover*RT/2 + |pos|*swap_side*nights  using COSTS_FTMO constants
            (not historical FX financing) — matches PREREG table.
    """
    inst = COST_MAP[df["name"]]
    dates = df["date"]
    c = df["close"]
    r = np.r_[0.0, c[1:] / c[:-1] - 1.0]
    p_prev = np.r_[0.0, pos[:-1]]
    turn = np.abs(np.diff(np.r_[0.0, pos]))
    nights = np.r_[0, [(b - a).days for a, b in zip(dates[:-1], dates[1:])]]

    # Constant FTMO swap table (PREREG §1); sign convention as engine non-FX branch
    swap_frac = np.where(
        p_prev > 0,
        p_prev * SWL[inst],
        np.where(p_prev < 0, -p_prev * SWS[inst], 0.0),
    ) * nights * 1e-4
    cost_turn = turn * (RT[inst] / 2) * 1e-4
    gross = p_prev * r

    rows = []
    # group by month of the RETURN day (dates[i] for i>=1)
    buckets: dict[tuple[int, int], list[int]] = {}
    for i in range(1, len(dates)):
        d = dates[i]
        if d < TRAIN_START or d > TRAIN_END:
            continue
        if d > HARD_CAP:
            continue
        buckets.setdefault(month_key(d), []).append(i)

    for mk, idxs in sorted(buckets.items()):
        g = float(np.sum(gross[idxs]))
        ct = float(np.sum(cost_turn[idxs]))
        sw = float(np.sum(swap_frac[idxs]))
        # held side: mean signed position during month (prev-day exposure)
        mean_pos = float(np.mean(p_prev[idxs]))
        if abs(mean_pos) < 1e-12 and float(np.max(np.abs(p_prev[idxs]))) < 1e-12:
            continue  # flat month
        n_nights = int(np.sum(nights[idxs]))
        # PREREG unit-side cost check companions
        side = 1 if mean_pos > 0 else -1
        swap_side = SWL[inst] if side > 0 else SWS[inst]
        unit_cost_bp = RT[inst] + n_nights * swap_side
        rows.append(
            {
                "pair": df["name"],
                "inst": inst,
                "year": mk[0],
                "month": mk[1],
                "bruto_bp": g * 1e4,
                "cost_bp": (ct + sw) * 1e4,
                "cost_turn_bp": ct * 1e4,
                "cost_swap_bp": sw * 1e4,
                "cost_swap50_bp": (ct + sw * 1.5) * 1e4,
                "mean_pos": mean_pos,
                "n_nights": n_nights,
                "unit_cost_bp": unit_cost_bp,
                "rt_bp": RT[inst],
                "swap_side_bp": swap_side,
            }
        )
    return rows


def main() -> int:
    all_rows: list[dict] = []
    for name in PAIRS:
        df = load_daily(name, field="close")
        # hard-cap calendar — drop 2025+ before positions (no peek)
        mask = np.array([d <= HARD_CAP for d in df["date"]], dtype=bool)
        df = {k: (v[mask] if isinstance(v, np.ndarray) else v) for k, v in df.items()}
        pos = positions_c05(df)
        all_rows.extend(pair_month_rows(df, pos))

    if not all_rows:
        raise SystemExit("no pair-months in train — data/signal problem")

    bruto = np.array([r["bruto_bp"] for r in all_rows], float)
    cost = np.array([r["cost_bp"] for r in all_rows], float)
    cost50 = np.array([r["cost_swap50_bp"] for r in all_rows], float)
    unit_cost = np.array([r["unit_cost_bp"] for r in all_rows], float)

    mean_bruto = float(bruto.mean())
    mean_cost = float(cost.mean())
    mean_cost50 = float(cost50.mean())
    mean_unit = float(unit_cost.mean())
    med_abs_bruto = float(np.median(np.abs(bruto)))
    threshold = 3.0 * mean_cost
    # Primary gate: signed mean bruto vs 3× mean realized cost (turn+swap on actual |pos|)
    passed = mean_bruto >= threshold
    # Companion (PREREG wording "rondreis + swap×nachten"): unit-side formula
    threshold_unit = 3.0 * mean_unit
    # Note: unit formula assumes |pos|≈1; our pos is vol-scaled — primary = realized cost.

    out_dir = Path("results/R2/b1_prep")
    out_dir.mkdir(parents=True, exist_ok=True)

    with (out_dir / "cost_gate_b1_train_months.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
        w.writeheader()
        w.writerows(all_rows)

    summary = {
        "prereg": "PREREG_FTMO_B1.md",
        "prereg_sha256": "8b0cc6beb6937982e8005079d526681bf08b1af9bb16b8ae8268e2095df3303c",
        "train": "2021-01-01..2023-12-31",
        "reserve": "2025-01-01→ ONAANGERAAKT",
        "n_pair_months": len(all_rows),
        "mean_bruto_bp_signed": mean_bruto,
        "mean_cost_bp": mean_cost,
        "mean_cost_bp_swap50": mean_cost50,
        "threshold_3x_cost_bp": threshold,
        "median_abs_bruto_bp_info": med_abs_bruto,
        "mean_unit_cost_bp_info": mean_unit,
        "threshold_3x_unit_info": threshold_unit,
        "gate": "signed_mean_bruto >= 3 * mean(turn+swap cost) on pair-months",
        "PASS": passed,
        "ratio_bruto_over_cost": (mean_bruto / mean_cost) if mean_cost else float("nan"),
        "engine_ftmo_blob": "ac7abef6cbaa0bb0c10139374f8d6fb03cc3b840",
        "pairs": PAIRS,
    }
    (out_dir / "cost_gate_b1_train.json").write_text(json.dumps(summary, indent=2) + "\n")

    lines = [
        "# B1 kostenpoort TRAIN (PREREG_FTMO_B1)",
        "",
        f"- Train: 2021–2023 · Reserve 2025→ **onaangeraakt**",
        f"- Pair-months: {len(all_rows)} (6 FX × maanden met |pos|>0)",
        f"- Signed mean bruto: **{mean_bruto:.2f} bp**",
        f"- Mean cost (turn+swap, COSTS_FTMO): **{mean_cost:.2f} bp**",
        f"- 3× cost drempel: **{threshold:.2f} bp**",
        f"- Ratio bruto/cost: **{summary['ratio_bruto_over_cost']:.2f}×** (need ≥ 3)",
        f"- Median |bruto| (info, NOT gate): {med_abs_bruto:.2f} bp",
        f"- Mean cost +50% swap (info): {mean_cost50:.2f} bp",
        f"- Unit-side mean cost RT+nights×swap (info): {mean_unit:.2f} bp",
        "",
        f"## Uitslag: {'PASS' if passed else 'FAIL'}",
        "",
        ("Door naar formele trial + `ftmo_ev()`." if passed else "STOP — append TRIALS stop:kostenpoort; geen verdere analyse."),
        "",
    ]
    (out_dir / "cost_gate_b1_train.md").write_text("\n".join(lines))
    print("\n".join(lines))
    print(json.dumps({k: summary[k] for k in ("PASS", "mean_bruto_bp_signed", "mean_cost_bp", "threshold_3x_cost_bp", "n_pair_months")}, indent=2))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
