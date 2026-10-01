#!/usr/bin/env python3
"""PREREG_FTMO_N11 — GER40 XETRA ORB cost-gate + formal train t (Uitvoerder-2).

Frozen rule from PREREG_FTMO_N11.md @ 564ee5e (Strateeg e8f261f).
Train 2021–2023 only. Test 2024 and reserve 2025+ untouched (PREREG §4/§5).

Cost-gate: mean bruto ≥ 2.16 bp (3× RT 0.72); stress 3.24 bp (+50% RT).
Formal: day-clustered t + Newey-West L=5 on day-sum netto_bp; threshold t≥2.0.
"""
from __future__ import annotations

import gzip
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "R2" / "n11_prep"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
RT = 0.72
GATE = 3.0 * RT          # 2.16
GATE_STRESS = 3.0 * 1.08  # 3.24 (+50% RT)
MIN_ORB_FRAC = 0.001      # 0.10%
ENTRY_CUTOFF_H, ENTRY_CUTOFF_M = 10, 30
FLAT_H = 13


def load_m5(rel: str) -> pd.DataFrame:
    path = ROOT / rel
    with gzip.open(path, "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna().sort_values("time")
    return df[(df["time"] >= TRAIN_START) & (df["time"] <= TRAIN_END)].reset_index(drop=True)


def bp_ret(entry: float, exit_px: float, side: int) -> float:
    return side * 1e4 * (exit_px - entry) / entry


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


def sim_n11_day(g: pd.DataFrame):
    """PREREG §2: ORB 09:00–09:30, entry after 09:30 before 10:30, flat 13:00."""
    day0 = g["time"].dt.normalize().iloc[0]
    orb = g[
        (g["time"] >= day0 + pd.Timedelta(hours=9))
        & (g["time"] < day0 + pd.Timedelta(hours=9, minutes=30))
    ]
    if len(orb) < 4:
        return None
    orb_hi = float(orb["high"].max())
    orb_lo = float(orb["low"].min())
    orb_mid = 0.5 * (orb_hi + orb_lo)
    orb_range = orb_hi - orb_lo
    if orb_mid <= 0 or orb_range <= 0:
        return None
    if orb_range / orb_mid < MIN_ORB_FRAC:
        return None

    # Entry window: [09:30, 10:30) — PREREG "geen breakout vóór 10:30 → geen trade"
    after_orb = g[
        (g["time"] >= day0 + pd.Timedelta(hours=9, minutes=30))
        & (g["time"] < day0 + pd.Timedelta(hours=ENTRY_CUTOFF_H, minutes=ENTRY_CUTOFF_M))
    ]
    if after_orb.empty:
        return None

    side = 0
    entry = None
    entry_t = None
    for _, row in after_orb.iterrows():
        c = float(row["close"])
        if c > orb_hi:
            side, entry, entry_t = 1, c, row["time"]
            break
        if c < orb_lo:
            side, entry, entry_t = -1, c, row["time"]
            break
    if side == 0 or entry is None:
        return None

    stop = orb_lo if side == 1 else orb_hi
    path = g[(g["time"] > entry_t) & (g["time"] <= day0 + pd.Timedelta(hours=FLAT_H))]
    exit_px = float(path.iloc[-1]["close"]) if len(path) else entry
    hit = "time"
    for _, row in path.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        if side == 1 and lo <= stop:
            exit_px, hit = stop, "stop"
            break
        if side == -1 and hi >= stop:
            exit_px, hit = stop, "stop"
            break

    bruto = bp_ret(entry, exit_px, side)
    return {
        "date": str(day0.date()),
        "side": side,
        "entry": entry,
        "exit": exit_px,
        "hit": hit,
        "orb_hi": orb_hi,
        "orb_lo": orb_lo,
        "orb_frac_bp": round(1e4 * orb_range / orb_mid, 4),
        "entry_hhmm": f"{entry_t.hour:02d}:{entry_t.minute:02d}",
        "bruto_bp": bruto,
        "netto_bp": bruto - RT,
        "rt": RT,
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ger = load_m5("data/m5gz/GER40cash.csv.gz")
    trades = []
    for _, g in ger.groupby(ger["time"].dt.normalize()):
        t = sim_n11_day(g.sort_values("time"))
        if t:
            trades.append(t)

    df = pd.DataFrame(trades)
    df.to_csv(OUT / "cost_gate_n11_train.csv", index=False)

    n = len(df)
    if n == 0:
        board = {
            "n": 0,
            "outcome": "FAIL_EMPTY",
            "gate": GATE,
            "gate_stress": GATE_STRESS,
            "reserve_2025": "untouched",
            "test_2024": "untouched",
        }
        (OUT / "n11_board.json").write_text(json.dumps(board, indent=2) + "\n")
        print(json.dumps(board, indent=2))
        return board

    mean_bruto = float(df["bruto_bp"].mean())
    median_bruto = float(df["bruto_bp"].median())
    mean_netto = float(df["netto_bp"].mean())
    stop_share = float((df["hit"] == "stop").mean())
    gate_pass = mean_bruto >= GATE
    stress_pass = mean_bruto >= GATE_STRESS

    # Day-clustered series (one trade/day max → day sum = trade)
    day = df.groupby("date")["netto_bp"].sum()
    day_bruto = df.groupby("date")["bruto_bp"].sum()
    t_day = t_plain(day.values)
    t_nw5 = t_nw(day.values, L=5)
    t_day_bruto = t_plain(day_bruto.values)
    t_nw5_bruto = t_nw(day_bruto.values, L=5)

    # Formal: PREREG §5 step 3 — day-clust / NW L=5, threshold ≥ 2.0
    # Use netto day series (after RT) as primary; also report bruto.
    t_ok = (
        t_nw5 == t_nw5
        and t_day == t_day
        and t_nw5 >= 2.0
        and t_day >= 2.0
        and mean_netto > 0
        and n >= 150
    )

    if not gate_pass:
        outcome = "FAIL_COST_GATE"
    elif not stress_pass:
        # PREREG: stress FAIL → vermelding; optioneel formele t — we still run t
        outcome = "FAIL_STRESS_then_" + ("PASS_T" if t_ok else "FAIL_T")
    elif t_ok:
        outcome = "PASS_CANDIDATE"
    else:
        outcome = "FAIL_T"

    board = {
        "idea": "N11_GER40_XETRA_ORB",
        "prereg": "PREREG_FTMO_N11.md",
        "prereg_sha_local": "564ee5e",
        "source_strateeg": "e8f261f",
        "n": n,
        "mean_bruto_bp": round(mean_bruto, 4),
        "median_bruto_bp": round(median_bruto, 4),
        "mean_netto_bp": round(mean_netto, 4),
        "p25_bruto": round(float(np.percentile(df["bruto_bp"], 25)), 4),
        "p75_bruto": round(float(np.percentile(df["bruto_bp"], 75)), 4),
        "stop_share": round(stop_share, 4),
        "rt_bp": RT,
        "gate_3x_rt": GATE,
        "gate_stress": GATE_STRESS,
        "pass_gate": bool(gate_pass),
        "pass_stress": bool(stress_pass),
        "N_days": int(len(day)),
        "t_day_clustered_netto": None if t_day != t_day else round(float(t_day), 4),
        "t_nw_L5_netto": None if t_nw5 != t_nw5 else round(float(t_nw5), 4),
        "t_day_clustered_bruto": None if t_day_bruto != t_day_bruto else round(float(t_day_bruto), 4),
        "t_nw_L5_bruto": None if t_nw5_bruto != t_nw5_bruto else round(float(t_nw5_bruto), 4),
        "mean_day_netto_bp": round(float(day.mean()), 4),
        "skew_day_netto": round(float(day.skew()), 4),
        "t_ok": bool(t_ok),
        "outcome": outcome,
        "entry_cutoff": "10:30 CET (PREREG §2; stricter than prior VOORSTEL screen)",
        "date_min": df["date"].iloc[0],
        "date_max": df["date"].iloc[-1],
        "reserve_2025": "untouched",
        "test_2024": "untouched",
    }

    (OUT / "n11_board.json").write_text(json.dumps(board, indent=2) + "\n")
    md = [
        "# PREREG_FTMO_N11 — cost-gate + formal train t",
        "",
        f"PREREG landed `564ee5e` (Strateeg `e8f261f`). Train 2021–2023 only.",
        "Rule: ORB 09:00–09:30, breakout entry before **10:30**, stop=ORB opposite, flat 13:00.",
        "RT=0.72 → gate 2.16 / stress 3.24. Test 2024 + reserve 2025→ untouched.",
        "",
        "| Metric | Value |",
        "|--------|------:|",
        f"| N | {n} |",
        f"| mean bruto | {mean_bruto:.4f} bp |",
        f"| median bruto | {median_bruto:.4f} bp |",
        f"| mean netto | {mean_netto:.4f} bp |",
        f"| gate 3×RT | {GATE:.2f} bp | **{'PASS' if gate_pass else 'FAIL'}** |",
        f"| stress +50% | {GATE_STRESS:.2f} bp | **{'PASS' if stress_pass else 'FAIL'}** |",
        f"| t day-clust netto | {board['t_day_clustered_netto']} |",
        f"| t NW L=5 netto | {board['t_nw_L5_netto']} |",
        f"| t day-clust bruto | {board['t_day_clustered_bruto']} |",
        f"| t NW L=5 bruto | {board['t_nw_L5_bruto']} |",
        f"| stop share | {stop_share:.4f} |",
        f"| skew day netto | {board['skew_day_netto']} |",
        "",
        f"## **Uitkomst: {outcome}**",
        "",
        "t_ok requires day-clust ≥2.0 AND NW L=5 ≥2.0 AND mean netto>0 AND N≥150 (train).",
        "",
    ]
    # Fix markdown table - I mixed formats. Rewrite cleanly.
    md = [
        "# PREREG_FTMO_N11 — cost-gate + formal train t",
        "",
        f"PREREG landed `564ee5e` (Strateeg `e8f261f`). Train 2021–2023 only.",
        "Rule: ORB 09:00–09:30, breakout entry before **10:30**, stop=ORB opposite, flat 13:00.",
        "RT=0.72 → gate 2.16 / stress 3.24. Test 2024 + reserve 2025→ untouched.",
        "",
        "| Metric | Value |",
        "|--------|------:|",
        f"| N | {n} |",
        f"| mean bruto bp | {mean_bruto:.4f} |",
        f"| median bruto bp | {median_bruto:.4f} |",
        f"| mean netto bp | {mean_netto:.4f} |",
        f"| gate 3×RT (2.16) | {'PASS' if gate_pass else 'FAIL'} |",
        f"| stress +50% (3.24) | {'PASS' if stress_pass else 'FAIL'} |",
        f"| t day-clust netto | {board['t_day_clustered_netto']} |",
        f"| t NW L=5 netto | {board['t_nw_L5_netto']} |",
        f"| t day-clust bruto | {board['t_day_clustered_bruto']} |",
        f"| t NW L=5 bruto | {board['t_nw_L5_bruto']} |",
        f"| stop share | {stop_share:.4f} |",
        f"| skew day netto | {board['skew_day_netto']} |",
        "",
        f"## **Uitkomst: {outcome}**",
        "",
        "t_ok = day-clust≥2.0 AND NW L=5≥2.0 AND mean netto>0 AND N≥150 (train only).",
        "",
    ]
    (OUT / "n11_report.md").write_text("\n".join(md) + "\n")
    print(json.dumps(board, indent=2))
    return board


if __name__ == "__main__":
    main()
