#!/usr/bin/env python3
"""C-035 — absorb U2 N100/N101 FAIL_T + Faraday N102/N103 Lane-B diag (0 CTO trials).

Diagnostic / D-092.1-style screens only until DIAG_PASS → PREREG freeze.
Reserve 2025+ untouched. Train 2021–2023; hard cut ≤2024-12-31.
Faraday edbd2ee: PREREG N100/N101 (U2 already FAIL_T) + OPEN N102/N103 NEW_FAMILY Y/Z.
"""
from __future__ import annotations

import gzip
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/cto/c035_absorb_n100_n103"
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


def diag_n102():
    """USDCHF LO 5d USD-CHF carry+mom; gate 3.03 bp (3×RT 1.01); swap earn→0 (D-100)."""
    return diag_lo_5d(
        "data/m5gz/USDCHF.csv.gz",
        3.03,
        "N102_USDCHF_LO_USD_CHF_CARRY_MOM_5D",
        "NEW_FAMILY Y; long-only; gate=3×RT 1.01; swap earn→0 in gate (D-100); ≠ N99 CADCHF / N74 L60",
    )


def diag_n103():
    """GER40 Lon-AM → US30 NY industrial lead-lag; |ger_am|≥40; flat 21:00."""
    ger = load_m5("data/m5gz/GER40cash.csv.gz")
    us30 = load_m5("data/m5gz/US30cash.csv.gz")
    ger = ger[(ger["time"] >= TRAIN_START) & (ger["time"] <= TRAIN_END)].copy()
    us30 = us30[(us30["time"] >= TRAIN_START) & (us30["time"] <= TRAIN_END)].copy()
    ger["day"] = ger["time"].dt.normalize()
    us30["day"] = us30["time"].dt.normalize()
    us_by_day = {d: g for d, g in us30.groupby("day")}
    pnls = []
    for day, g in ger.groupby("day"):
        b0800 = first_bar_in(g, day, 8, 0, 15)
        b1200 = first_bar_in(g, day, 12, 0, 15)
        if b0800 is None or b1200 is None:
            continue
        p0 = float(b0800["close"])
        p1 = float(b1200["close"])
        if p0 <= 0:
            continue
        ger_am_bp = 1e4 * (p1 / p0 - 1.0)
        if not np.isfinite(ger_am_bp) or abs(ger_am_bp) < 40.0:
            continue
        side = 1 if ger_am_bp >= 40.0 else -1
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
        1.35,
        "N103_GER40_LON_AM_US30_NY_INDUSTRIAL",
        "NEW_FAMILY Z; GER→US30 same-day; |am|≥40; session-flat 21:00; ≠ N98 oil→tech / S2-GER_US / N85",
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [diag_n102(), diag_n103()]
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "c035_family_diag.csv", index=False)
    board = {
        "c": "C-035",
        "when": "2026-10-02 ~22:05 Europe/Amsterdam",
        "absorb": {
            "main": "1e06371 NEXT_STEPS v88 — C-033+C-034; TRIAL 458 at Manager write",
            "faraday": "edbd2ee PREREG N100/N101 from S2 67a9be1 + OPEN N102/N103 NEW_FAMILY Y/Z",
            "u2": "d09d00a N101 FAIL_T TRIAL 460 (prior 2ffb9af N100 FAIL_T TRIAL 459); no live PREREG",
            "s2": "67a9be1 Lane-A EMB_CREDIT_STRESS + CRACK_SPREAD_MACRO promote (both now FAIL_T)",
            "prior_cto": "3ebdea2 C-034 N98/N99 DIAG_FAIL",
        },
        "u2_formal": [
            {
                "id": "N100",
                "family": "EMB_CREDIT_STRESS",
                "verdict": "FAIL_T",
                "trial": 459,
                "train_t": "0.3726/0.3799 NW",
                "note": "cost-gate PASS mean +2.97 ≥ 1.98; stress PASS; t≪2",
            },
            {
                "id": "N101",
                "family": "CRACK_SPREAD_MACRO",
                "verdict": "FAIL_T",
                "trial": 460,
                "train_t": "1.0535/1.2064 NW",
                "note": "cost-gate PASS mean +6.30 ≥ 1.98; stress PASS; t≪2; test mean −5.0",
            },
        ],
        "freeze": "OFF",
        "trial_count": 460,
        "trials_appended_by_cto": 0,
        "reserve_2025": "untouched",
        "results": rows,
        "promote_to_prereg": [r["label"] for r in rows if r["verdict"] == "DIAG_PASS"],
        "kill_circuit_note": (
            "cost-PASS→FAIL_T streak continues: N87→N92→N100→N101 (4 formal); "
            "prior EURJPY_MED/N41 also FAIL_T; pivot ON; bar EMB_CREDIT / CRACK_SPREAD clones"
        ),
    }
    (OUT / "c035_board.json").write_text(json.dumps(board, indent=2))
    lines = [
        "# C-035 — absorb U2 N100/N101 FAIL_T + Faraday N102/N103 Lane-B diag (0 CTO trials)",
        "",
        f"**When:** {board['when']}. **TRIAL_COUNT:** 460. **FREEZE:** OFF.",
        "",
        "## Absorb",
        "",
        "- `origin/main` `1e06371` (NEXT_STEPS **v88**; Manager @21:42 still TRIAL 458 / U2 IDLE — stale vs U2).",
        "- Faraday `edbd2ee` ~21:57: PREREG **N100/N101** from S2 `67a9be1` + OPEN **N102/N103** NEW_FAMILY Y/Z.",
        "- U2 `2ffb9af` N100 EMB_CREDIT_STRESS **FAIL_T** (TRIAL **459**); `d09d00a` N101 CRACK_SPREAD_MACRO **FAIL_T** (TRIAL **460**).",
        "- No live PREREG. Track-3 PAUSED. Reserve 2025+ untouched.",
        "",
        "## U2 formal (already committed; CTO absorb only)",
        "",
        "| Idee | Family | Trial | Verdict | Notes |",
        "|------|--------|------:|---------|-------|",
        "| N100 | EMB_CREDIT_STRESS | 459 | **FAIL_T** | cost PASS +2.97≥1.98; t 0.37; test −2.57 |",
        "| N101 | CRACK_SPREAD_MACRO | 460 | **FAIL_T** | cost PASS +6.30≥1.98; t 1.05; test −5.00 |",
        "",
        "## Lane-B diagnostic N102/N103 (train 2021–2023; ≤2024; 0 CTO trials)",
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
        "- N102: USDCHF dayclose ≤22:00; ret5>0 → long; hold 5d non-overlap; swap earn not credited (D-100); gate=3×RT 1.01=3.03.",
        "- N103: GER40cash 08→12 CET impulse |bp|≥40 → same-dir US30 @15:30 → flat 21:00; gate=3×RT 0.45=1.35.",
        "- DIAG_PASS → CTO freezes PREREG for U2 (C-031 precedent); else drop / replace NEW_FAMILY (D-094).",
        "- No thr-grid / no CADCHF twin / no L60 rewrite / no GER→US-open rewrite / no US100 substitute / no soft gate.",
        "- Kill: bar EMB_CREDIT_STRESS / CRACK_SPREAD_MACRO clones; skip N75–N101 + prior bars.",
        "",
        f"**Promote candidates (DIAG_PASS):** {board['promote_to_prereg'] or 'none'}.",
        "",
        "Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.",
        "",
    ]
    (OUT / "c035_report.md").write_text("\n".join(lines))
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
