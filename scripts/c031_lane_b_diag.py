#!/usr/bin/env python3
"""C-031 — N87 FAIL_T absorb + Lane-B diagnostics N90–N92 (0 trials).

Diagnostic / D-092.1-style screens only. Not formal gates / not PREREG freeze.
Reserve 2025+ untouched. Train 2021–2023; hard cut ≤2024-12-31.
"""
from __future__ import annotations

import gzip
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/cto/c031_n87_absorb_n90_n92"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
HARD_CUT = pd.Timestamp("2024-12-31")


def load_m5(rel: str) -> pd.DataFrame:
    with gzip.open(ROOT / rel, "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["open", "high", "low", "close"]).sort_values("time")
    df = df[df["time"] <= HARD_CUT]
    return df.reset_index(drop=True)


def day_closes_le(m5: pd.DataFrame, hour: int = 22, minute: int = 0) -> pd.Series:
    """Last M5 close on/before hour:minute each calendar day (CET proxy)."""
    m5 = m5.copy()
    m5["day"] = m5["time"].dt.normalize()
    cut = m5["time"].dt.hour * 60 + m5["time"].dt.minute
    thr = hour * 60 + minute
    sub = m5[cut <= thr]
    if sub.empty:
        return pd.Series(dtype=float)
    return sub.groupby("day")["close"].last().sort_index()


def first_bar_in(g: pd.DataFrame, day, h: int, m0: int = 0, span_min: int = 15):
    t0 = day + pd.Timedelta(hours=h, minutes=m0)
    t1 = t0 + pd.Timedelta(minutes=span_min)
    exact = g[g["time"] == t0]
    if len(exact):
        return exact.iloc[0]
    win = g[(g["time"] >= t0) & (g["time"] <= t1)]
    return win.iloc[0] if len(win) else None


def last_bar_le(g: pd.DataFrame, day, h: int, m0: int = 0):
    t = day + pd.Timedelta(hours=h, minutes=m0)
    win = g[g["time"] <= t]
    return win.iloc[-1] if len(win) else None


def trade_stats(pnls_bp, gate_bp, label, notes=""):
    arr = np.asarray(pnls_bp, dtype=float)
    arr = arr[np.isfinite(arr)]
    n = len(arr)
    mean = float(np.mean(arr)) if n else float("nan")
    if n >= 2 and float(np.std(arr, ddof=1)) > 0:
        t = mean / (float(np.std(arr, ddof=1)) / math.sqrt(n))
    else:
        t = float("nan")
    half = n // 2
    m1 = float(np.mean(arr[:half])) if half else float("nan")
    m2 = float(np.mean(arr[half:])) if n - half else float("nan")
    if n >= 150 and np.isfinite(mean) and mean >= gate_bp:
        verdict = "DIAG_PASS"
    elif n < 150 and np.isfinite(mean) and mean >= gate_bp:
        verdict = "UNDERPOWERED"
    else:
        verdict = "DIAG_FAIL"
    return {
        "label": label,
        "n": n,
        "mean_bp": round(mean, 3) if n else None,
        "day_t": round(t, 3) if n >= 2 else None,
        "h1_mean_bp": round(m1, 3) if half else None,
        "h2_mean_bp": round(m2, 3) if n - half else None,
        "gate_bp": gate_bp,
        "verdict": verdict,
        "notes": notes,
    }


def diag_carry_mom_5d(rel: str, gate_bp: float, label: str, notes: str):
    """N90/N91: ret5>0 → LONG close_t → exit close_{t+5}; non-overlapping; train only."""
    m5 = load_m5(rel)
    closes = day_closes_le(m5, 22, 0)
    # need lookback before train for ret5; keep from 2020
    closes = closes[closes.index >= pd.Timestamp("2020-01-01")]
    dates = list(closes.index)
    px = closes.values.astype(float)
    pnls = []
    i = 5
    while i < len(dates) - 5:
        d = dates[i]
        if d < TRAIN_START or d > TRAIN_END.normalize():
            i += 1
            continue
        ret5 = px[i] / px[i - 5] - 1.0
        if not np.isfinite(ret5) or ret5 <= 0:
            i += 1
            continue
        x_i = i + 5
        if dates[x_i] > TRAIN_END.normalize():
            break
        e_px, x_px = float(px[i]), float(px[x_i])
        if e_px <= 0:
            i += 1
            continue
        pnls.append(1e4 * (x_px - e_px) / e_px)  # long-only
        i = x_i  # non-overlap
    return trade_stats(pnls, gate_bp, label, notes)


def diag_n92():
    """US100cash NY-open 2h momentum → hold 17:30–22:00 CET; bilateral; intradag-flat."""
    m5 = load_m5("data/m5gz/US100cash.csv.gz")
    m5 = m5[(m5["time"] >= TRAIN_START) & (m5["time"] <= TRAIN_END)].copy()
    m5["day"] = m5["time"].dt.normalize()
    pnls = []
    for day, g in m5.groupby("day"):
        b0 = first_bar_in(g, day, 15, 30, 15)
        b1 = first_bar_in(g, day, 17, 30, 15)
        if b0 is None or b1 is None:
            continue
        p0 = float(b0["close"])
        p1 = float(b1["close"])
        if p0 <= 0:
            continue
        ret2h = p1 / p0 - 1.0
        if ret2h == 0 or not np.isfinite(ret2h):
            continue
        side = 1 if ret2h > 0 else -1
        entry = p1
        exb = last_bar_le(g, day, 22, 0)
        if exb is None or exb["time"] <= b1["time"]:
            continue
        exit_px = float(exb["close"])
        pnls.append(side * 1e4 * (exit_px - entry) / entry)
    return trade_stats(
        pnls,
        1.98,
        "N92_US100_NY_2H_MOM",
        "NEW_FAMILY Q; intradag-flat; ≠ ORB / N87 / N89",
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [
        diag_carry_mom_5d(
            "data/m5gz/GBPJPY.csv.gz",
            2.16,
            "N90_GBPJPY_CARRY_MOM_5D",
            "NEW_FAMILY O; long-only; gate=3×RT 0.72; swap earn→0 in gate (D-100)",
        ),
        diag_carry_mom_5d(
            "data/m5gz/AUDUSD.csv.gz",
            1.35,
            "N91_AUDUSD_CARRY_MOM_5D",
            "NEW_FAMILY P; long-only; gate=3×RT 0.45; swap earn→0 in gate (D-100)",
        ),
        diag_n92(),
    ]
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "c031_family_diag.csv", index=False)
    board = {
        "c": "C-031",
        "when": "2026-10-02 ~20:31 Europe/Amsterdam",
        "absorb": {
            "main": "054a8eb NEXT_STEPS v83 D-101…D-104 + N87 FAIL_T; TRIAL 457",
            "N87": "FAIL_T U2 3a9108e; counts_as_trial=true; TRIAL_COUNT 457; dead+=N87_US30_GAP_FADE",
            "D-101": "lat A (t≥2) or B (lit premie + ftmo_ev EV>0 / surv≥0.5 + intradag-DD + forward)",
            "D-102": "RISK-REACTIVE course",
            "D-103": "SHOCK ML program",
            "D-104": "ORB-meta reserve FAIL; ORB-as-robust-edge closed",
        },
        "freeze": "OFF",
        "trial_count": 457,
        "trials_appended_by_cto": 0,
        "reserve_2025": "untouched",
        "results": rows,
        "promote_to_prereg": [
            r["label"] for r in rows if r["verdict"] == "DIAG_PASS"
        ],
        "kill_circuit_note": "N87 cost-PASS→FAIL_T increments streak; pivot already ON",
    }
    (OUT / "c031_board.json").write_text(json.dumps(board, indent=2))
    lines = [
        "# C-031 — N87 FAIL_T absorb + Lane-B diag N90–N92 (0 trials)",
        "",
        f"**When:** {board['when']}. **TRIAL_COUNT:** 457. **FREEZE:** OFF.",
        "",
        "## Absorb",
        "",
        "- Merged `origin/main` @ `054a8eb` (NEXT_STEPS **v83** — D-101…D-104 + N87 FAIL_T; TRIAL **457**).",
        "- U2 `3a9108e` **N87** US30 opening-gap fade → **FAIL_T** (t_NW 1.63; test −17.71 bp). Dead += `N87_US30_GAP_FADE`.",
        "- **D-104** ORB-meta reserve FAIL → ORB-as-robust-edge closed. No ORB-meta / ORB-index-ext clones.",
        "- U2 tip `6f6ef86` IDLE/HOLD until PASS→PREREG. Track-3 PAUSED. Reserve 2025+ untouched.",
        "",
        "## Lane-B diagnostic (train 2021–2023; ≤2024; 0 trials)",
        "",
        "| Idee | mean_bp | n | gate | day_t | h1 | h2 | Verdict |",
        "|------|--------:|--:|-----:|------:|---:|---:|---------|",
    ]
    for r in rows:
        lines.append(
            f"| {r['label']} | {r['mean_bp']} | {r['n']} | {r['gate_bp']} | {r['day_t']} | {r['h1_mean_bp']} | {r['h2_mean_bp']} | **{r['verdict']}** |"
        )
    lines += [
        "",
        "### Notes",
        "",
        "- N90/N91: dayclose ≤22:00 from M5; ret5>0 → long; hold 5d non-overlap; swap earn not credited in gate (D-100).",
        "- N92: NY 15:30–17:30 CET direction → hold to 22:00; bilateral; intradag-flat (≠ ORB breakout).",
        "- DIAG_PASS → Strateeg may freeze PREREG; DIAG_FAIL/UNDERPOWERED → drop / replace with NEW_FAMILY (D-094).",
        "- CTO does **not** freeze PREREG here (Lane-B ownership = Strateeg); diagnostic only to unblock drought.",
        "",
        f"**Promote candidates (DIAG_PASS):** {board['promote_to_prereg'] or 'none'}.",
        "",
        "Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.",
        "",
    ]
    (OUT / "c031_report.md").write_text("\n".join(lines))
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
