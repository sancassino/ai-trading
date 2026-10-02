#!/usr/bin/env python3
"""C-033 — absorb main v87 + Lane-B diag N96/N97 (0 trials).

Diagnostic / D-092.1-style screens only until DIAG_PASS → PREREG freeze.
Reserve 2025+ untouched. Train 2021–2023; hard cut ≤2024-12-31.
Faraday filed VOORSTEL N96/N97 OPEN; no D-092.1 results yet → CTO runs Lane-B.
"""
from __future__ import annotations

import gzip
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/cto/c033_absorb_v87_n96_n97"
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


def diag_n96():
    """CADJPY LO 5d carry+mom; gate 4.80 bp (3×RT 1.60); swap earn→0 in gate (D-100)."""
    return diag_lo_5d(
        "data/m5gz/CADJPY.csv.gz",
        4.80,
        "N96_CADJPY_LO_CARRY_MOM_5D",
        "NEW_FAMILY U; long-only; gate=3×RT 1.60; swap earn→0 in gate (D-100); ≠ N94 NZDJPY",
    )


def diag_n97():
    """AUDCAD LO 5d commodity-XS mom; gate 4.50 bp (3×RT 1.50); swap→0 in gate."""
    return diag_lo_5d(
        "data/m5gz/AUDCAD.csv.gz",
        4.50,
        "N97_AUDCAD_LO_COMMODITY_XS_MOM_5D",
        "NEW_FAMILY V; long-only; gate=3×RT 1.50; swap earn/neutral→0; ≠ N84/N91/N94/N96",
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [diag_n96(), diag_n97()]
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "c033_family_diag.csv", index=False)
    board = {
        "c": "C-033",
        "when": "2026-10-02 ~21:15 Europe/Amsterdam",
        "absorb": {
            "main": "6775e28 NEXT_STEPS v87 — C-032 + N94/N95 DIAG_FAIL; N96/N97 OPEN; TRIAL 458",
            "faraday": "b2ab614 N96/N97 VOORSTEL OPEN; no D-092.1 results yet for N96/N97",
            "u2": "b382307 IDLE after N93 FAIL_COST_GATE; TRIAL_COUNT 458",
            "prior_cto": "f6b0c60 C-032 N94/N95 DIAG_FAIL",
        },
        "freeze": "OFF",
        "trial_count": 458,
        "trials_appended_by_cto": 0,
        "reserve_2025": "untouched",
        "results": rows,
        "promote_to_prereg": [r["label"] for r in rows if r["verdict"] == "DIAG_PASS"],
        "kill_circuit_note": "No new cost-PASS→FAIL_T this cycle; pivot remains ON from prior streak",
    }
    (OUT / "c033_board.json").write_text(json.dumps(board, indent=2))
    lines = [
        "# C-033 — absorb main v87 + Lane-B diag N96/N97 (0 trials)",
        "",
        f"**When:** {board['when']}. **TRIAL_COUNT:** 458. **FREEZE:** OFF.",
        "",
        "## Absorb",
        "",
        "- Merged `origin/main` @ `6775e28` (NEXT_STEPS **v87** — C-032 + N94/N95 DIAG_FAIL; N96/N97 OPEN; TRIAL **458**).",
        "- Faraday `b2ab614` VOORSTEL N96/N97 OPEN; **no** prior D-092.1 results for N96/N97 → CTO Lane-B diag.",
        "- U2 `b382307` IDLE/HOLD after N93 FAIL_COST_GATE. Track-3 PAUSED. Reserve 2025+ untouched.",
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
        "- N96: CADJPY dayclose ≤22:00; ret5>0 → long; hold 5d non-overlap; swap earn not credited in gate (D-100).",
        "- N97: AUDCAD dayclose ≤22:00; ret5>0 → long; hold 5d non-overlap; swap earn/neutral → 0 in gate.",
        "- DIAG_PASS → CTO freezes PREREG for U2 (C-031 precedent); else drop / replace NEW_FAMILY (D-094).",
        "- No retune lookback / no NZDJPY twin / no fade rewrite.",
        "",
        f"**Promote candidates (DIAG_PASS):** {board['promote_to_prereg'] or 'none'}.",
        "",
        "Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.",
        "",
    ]
    (OUT / "c033_report.md").write_text("\n".join(lines))
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
