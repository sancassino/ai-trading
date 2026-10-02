#!/usr/bin/env python3
"""C-032 — N92 FAIL_T + N93 FAIL_COST_GATE absorb + Lane-B diag N94/N95 (0 trials).

Diagnostic / D-092.1-style screens only until DIAG_PASS → PREREG freeze.
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
OUT = ROOT / "results/cto/c032_n92_n93_absorb_n94_n95"
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


def diag_n94():
    """NZDJPY LO 5d carry+mom; gate 6.00 bp (3×RT 2.00); swap earn→0 in gate (D-100)."""
    m5 = load_m5("data/m5gz/NZDJPY.csv.gz")
    closes = day_closes_le(m5, 22, 0)
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
        pnls.append(1e4 * (x_px - e_px) / e_px)
        i = x_i
    return trade_stats(
        pnls,
        6.00,
        "N94_NZDJPY_LO_CARRY_MOM_5D",
        "NEW_FAMILY S; long-only; gate=3×RT 2.00; swap earn→0 in gate (D-100)",
    )


def diag_n95():
    """XAU London AM 08–11 → NY 15:30 entry → flat 21:00; |am_bp|≥25; bilateral."""
    m5 = load_m5("data/m5gz/XAUUSD.csv.gz")
    m5 = m5[(m5["time"] >= TRAIN_START) & (m5["time"] <= TRAIN_END)].copy()
    m5["day"] = m5["time"].dt.normalize()
    pnls = []
    for day, g in m5.groupby("day"):
        b0800 = first_bar_in(g, day, 8, 0, 15)
        b1100 = first_bar_in(g, day, 11, 0, 15)
        if b0800 is None or b1100 is None:
            continue
        p0 = float(b0800["close"])
        p1 = float(b1100["close"])
        if p0 <= 0:
            continue
        am_bp = 1e4 * (p1 / p0 - 1.0)
        if not np.isfinite(am_bp) or abs(am_bp) < 25.0:
            continue
        side = 1 if am_bp >= 25.0 else -1
        bent = first_bar_in(g, day, 15, 30, 15)
        if bent is None:
            continue
        entry = float(bent["close"])
        if entry <= 0:
            continue
        exb = last_bar_le(g, day, 21, 0)
        if exb is None or exb["time"] <= bent["time"]:
            continue
        exit_px = float(exb["close"])
        pnls.append(side * 1e4 * (exit_px - entry) / entry)
    return trade_stats(
        pnls,
        2.49,
        "N95_XAU_LON_AM_NY_CONT",
        "NEW_FAMILY T; session-flat 21:00; |am|≥25; ≠ S2-XAU_AM_FADE / N36",
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [diag_n94(), diag_n95()]
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "c032_family_diag.csv", index=False)
    board = {
        "c": "C-032",
        "when": "2026-10-02 ~21:05 Europe/Amsterdam",
        "absorb": {
            "main": "615b9af NEXT_STEPS v86 — N93 FAIL_COST_GATE; TRIAL 458; N94/N95 OPEN",
            "N92": "FAIL_T U2 b5b59e0; counts_as_trial=true; TRIAL_COUNT 458; dead+=N92_US100_NY_2H_MOM",
            "N93": "FAIL_COST_GATE U2 b382307; geen trial; TRIAL blijft 458; dead+=N93_SECTOR_DISP_ROTATION",
        },
        "freeze": "OFF",
        "trial_count": 458,
        "trials_appended_by_cto": 0,
        "reserve_2025": "untouched",
        "results": rows,
        "promote_to_prereg": [r["label"] for r in rows if r["verdict"] == "DIAG_PASS"],
        "kill_circuit_note": "N92 cost-PASS→FAIL_T increments streak; N93 cost-gate STOP (no streak++); pivot ON",
    }
    (OUT / "c032_board.json").write_text(json.dumps(board, indent=2))
    lines = [
        "# C-032 — N92 FAIL_T + N93 FAIL_COST_GATE absorb + Lane-B diag N94/N95 (0 trials)",
        "",
        f"**When:** {board['when']}. **TRIAL_COUNT:** 458. **FREEZE:** OFF.",
        "",
        "## Absorb",
        "",
        "- Merged `origin/main` @ `615b9af` (NEXT_STEPS **v86** — N93 FAIL_COST_GATE; TRIAL **458**; N94/N95 OPEN).",
        "- U2 `b5b59e0` **N92** US100 NY 2h mom → **FAIL_T** (t_NW 1.56; test t 0.51). Dead += `N92_US100_NY_2H_MOM`. TRIAL **458**.",
        "- U2 `b382307` **N93** SECTOR_DISP_ROTATION → **FAIL_COST_GATE** (mean +0.99 ≪ 1.98; geen trial). Dead += `N93_SECTOR_DISP_ROTATION`.",
        "- U2 tip IDLE/HOLD until next PASS→PREREG. Track-3 PAUSED. Reserve 2025+ untouched.",
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
        "- N94: NZDJPY dayclose ≤22:00; ret5>0 → long; hold 5d non-overlap; swap earn not credited in gate (D-100).",
        "- N95: XAU |am_bp 08–11|≥25 → side at 15:30 → flat 21:00; bilateral; intradag-flat.",
        "- DIAG_PASS → CTO freezes PREREG for U2 (C-031 precedent); else drop / replace NEW_FAMILY (D-094).",
        "",
        f"**Promote candidates (DIAG_PASS):** {board['promote_to_prereg'] or 'none'}.",
        "",
        "Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.",
        "",
    ]
    (OUT / "c032_report.md").write_text("\n".join(lines))
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
