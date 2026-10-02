#!/usr/bin/env python3
"""C-034 — absorb Faraday N98/N99 + Lane-B diag (0 trials).

Diagnostic / D-092.1-style screens only until DIAG_PASS → PREREG freeze.
Reserve 2025+ untouched. Train 2021–2023; hard cut ≤2024-12-31.
Faraday 4a5ec7c: N96 UNDERPOWERED + N97 FAIL; OPEN N98/N99 NEW_FAMILY W/X.
No D-092.1 results for N98/N99 yet → CTO runs Lane-B.
"""
from __future__ import annotations

import gzip
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/cto/c034_absorb_n98_n99"
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


def diag_lo_5d(rel: str, gate_bp: float, label: str, notes: str):
    """Long-only 5d momentum; non-overlapping; dayclose ≤22:00; train 2021–2023."""
    m5 = load_m5(rel)
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
    return trade_stats(pnls, gate_bp, label, notes)


def diag_n98():
    """USOILcash Lon-AM → US100cash NY risk-on lead-lag; |oil_am|≥40; flat 21:00."""
    oil = load_m5("data/m5gz/USOILcash.csv.gz")
    us100 = load_m5("data/m5gz/US100cash.csv.gz")
    oil = oil[(oil["time"] >= TRAIN_START) & (oil["time"] <= TRAIN_END)].copy()
    us100 = us100[(us100["time"] >= TRAIN_START) & (us100["time"] <= TRAIN_END)].copy()
    oil["day"] = oil["time"].dt.normalize()
    us100["day"] = us100["time"].dt.normalize()
    us_by_day = {d: g for d, g in us100.groupby("day")}
    pnls = []
    for day, g in oil.groupby("day"):
        b0800 = first_bar_in(g, day, 8, 0, 15)
        b1200 = first_bar_in(g, day, 12, 0, 15)
        if b0800 is None or b1200 is None:
            continue
        p0 = float(b0800["close"])
        p1 = float(b1200["close"])
        if p0 <= 0:
            continue
        oil_am_bp = 1e4 * (p1 / p0 - 1.0)
        if not np.isfinite(oil_am_bp) or abs(oil_am_bp) < 40.0:
            continue
        side = 1 if oil_am_bp >= 40.0 else -1
        ug = us_by_day.get(day)
        if ug is None:
            continue
        bent = first_bar_in(ug, day, 15, 30, 15)
        if bent is None:
            continue
        entry = float(bent["close"])
        if entry <= 0:
            continue
        exb = last_bar_le(ug, day, 21, 0)
        if exb is None or exb["time"] <= bent["time"]:
            continue
        exit_px = float(exb["close"])
        pnls.append(side * 1e4 * (exit_px - entry) / entry)
    return trade_stats(
        pnls,
        1.98,
        "N98_USOIL_LON_AM_US100_NY_RISKON",
        "NEW_FAMILY W; oil→equity same-day; |am|≥40; session-flat 21:00; ≠ N85/N80/UKOIL-OVN",
    )


def diag_n99():
    """CADCHF LO 5d oil-CHF carry+mom; gate 6.81 bp (3×RT 2.27); swap earn→0 (D-100)."""
    return diag_lo_5d(
        "data/m5gz/CADCHF.csv.gz",
        6.81,
        "N99_CADCHF_LO_OIL_CHF_CARRY_MOM_5D",
        "NEW_FAMILY X; long-only; gate=3×RT 2.27; swap earn→0 in gate (D-100); ≠ N96 CADJPY",
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [diag_n98(), diag_n99()]
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "c034_family_diag.csv", index=False)
    board = {
        "c": "C-034",
        "when": "2026-10-02 ~21:32 Europe/Amsterdam",
        "absorb": {
            "main": "6775e28 NEXT_STEPS v87 — still tip (Manager not yet v88); TRIAL 458",
            "faraday": "4a5ec7c N96 UNDERPOWERED + N97 FAIL; OPEN N98/N99 NEW_FAMILY W/X; no D-092.1 for N98/N99",
            "u2": "83d6331 IDLE absorb v87; hold until N96/N97 PASS→PREREG (none); TRIAL_COUNT 458",
            "prior_cto": "9536912 C-033 N96 UNDERPOWERED / N97 DIAG_FAIL",
        },
        "freeze": "OFF",
        "trial_count": 458,
        "trials_appended_by_cto": 0,
        "reserve_2025": "untouched",
        "results": rows,
        "promote_to_prereg": [r["label"] for r in rows if r["verdict"] == "DIAG_PASS"],
        "kill_circuit_note": "No new cost-PASS→FAIL_T this cycle; pivot remains ON from prior streak",
    }
    (OUT / "c034_board.json").write_text(json.dumps(board, indent=2))
    lines = [
        "# C-034 — absorb Faraday N98/N99 + Lane-B diag (0 trials)",
        "",
        f"**When:** {board['when']}. **TRIAL_COUNT:** 458. **FREEZE:** OFF.",
        "",
        "## Absorb",
        "",
        "- `origin/main` still `6775e28` (NEXT_STEPS **v87**; Manager not yet bumped for C-033).",
        "- Faraday `4a5ec7c` N96 UNDERPOWERED + N97 FAIL D-092.1; filed **N98/N99** NEW_FAMILY W/X; **no** D-092.1 for N98/N99 → CTO Lane-B.",
        "- U2 `83d6331` IDLE/HOLD after v87 absorb. Track-3 PAUSED. Reserve 2025+ untouched.",
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
        "- N98: USOILcash 08→12 CET impulse |bp|≥40 → same-dir US100 @15:30 → flat 21:00; gate=3×RT 0.66=1.98.",
        "- N99: CADCHF dayclose ≤22:00; ret5>0 → long; hold 5d non-overlap; swap earn not credited in gate (D-100); gate=3×RT 2.27=6.81.",
        "- DIAG_PASS → CTO freezes PREREG for U2 (C-031 precedent); else drop / replace NEW_FAMILY (D-094).",
        "- No thr-grid / no UKOIL twin / no overnight oil rewrite / no CADJPY twin / no soft gate.",
        "",
        f"**Promote candidates (DIAG_PASS):** {board['promote_to_prereg'] or 'none'}.",
        "",
        "Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.",
        "",
    ]
    (OUT / "c034_report.md").write_text("\n".join(lines))
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
