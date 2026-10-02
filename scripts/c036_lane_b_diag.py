#!/usr/bin/env python3
"""C-036 — absorb main v90 + Faraday N104–N109 + Lane-B diag N110/N111 (0 CTO trials).

Faraday already D-092.1'd N104–N109 (no PASS→PREREG). OPEN N110/N111 NEW_FAMILY AG/AH.
Diagnostic screens only until DIAG_PASS → PREREG freeze.
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
OUT = ROOT / "results/cto/c036_absorb_v90_n104_n111"
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


def diag_n110():
    """DXYcash Lon-AM → EU-afternoon continuation session-flat; |am|≥25; flat 17:00."""
    dxy = load_m5("data/m5gz/DXYcash.csv.gz")
    dxy = dxy[(dxy["time"] >= TRAIN_START) & (dxy["time"] <= TRAIN_END)].copy()
    dxy["day"] = dxy["time"].dt.normalize()
    pnls = []
    for day, g in dxy.groupby("day"):
        b0800 = first_bar_in(g, day, 8, 0, 15)
        b1200 = first_bar_in(g, day, 12, 0, 15)
        if b0800 is None or b1200 is None:
            continue
        p0 = float(b0800["close"])
        p1 = float(b1200["close"])
        if p0 <= 0:
            continue
        dxy_am_bp = 1e4 * (p1 / p0 - 1.0)
        if not np.isfinite(dxy_am_bp) or abs(dxy_am_bp) < 25.0:
            continue
        side = 1 if dxy_am_bp >= 25.0 else -1
        bent = first_bar_in(g, day, 13, 0, 15)
        if bent is None:
            continue
        entry = float(bent["close"])
        if entry <= 0:
            continue
        exb = last_bar_le(g, day, 17, 0)
        if exb is None or exb["time"] <= bent["time"]:
            continue
        exit_px = float(exb["close"])
        pnls.append(side * 1e4 * (exit_px - entry) / entry)
    return trade_stats(
        pnls,
        7.86,
        "N110_DXY_LON_AM_EU_PM_CONT",
        "NEW_FAMILY AG; DXY Lon-AM→EU-PM same-dir; |am|≥25; session-flat 17:00; gate=3×RT 2.62=7.86; ≠ N108/N105 Asia→Lon equity",
    )


def diag_n111():
    """GBPAUD LO 5d GBP-AUD carry+mom; gate 4.38 bp (3×RT 1.46); swap earn→0 (D-100)."""
    return diag_lo_5d(
        "data/m5gz/GBPAUD.csv.gz",
        4.38,
        "N111_GBPAUD_LO_GBP_AUD_CARRY_MOM_5D",
        "NEW_FAMILY AH; long-only; gate=3×RT 1.46; swap earn→0 in gate (D-100); ≠ N97 AUDCAD / N104 GBPCHF / N106 EURNZD",
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [diag_n110(), diag_n111()]
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "c036_family_diag.csv", index=False)

    faraday_absorb = [
        {"id": "N104", "verdict": "UNDERPOWERED", "n": 98, "mean_bp": 10.62, "gate_bp": 4.53, "note": "GBPCHF LO 5d; Faraday 7d2d48a"},
        {"id": "N105", "verdict": "FAIL", "n": 392, "mean_bp": -2.77, "gate_bp": 4.53, "note": "JP225 Tokyo→Lon; Faraday 7d2d48a"},
        {"id": "N106", "verdict": "FAIL", "n": 103, "mean_bp": 3.45, "gate_bp": 4.11, "note": "EURNZD LO; Faraday 107e502"},
        {"id": "N107", "verdict": "FAIL", "n": 255, "mean_bp": 3.94, "gate_bp": 5.94, "note": "UK100→FRA40; Faraday 107e502"},
        {"id": "N108", "verdict": "FAIL", "n": 242, "mean_bp": -4.86, "gate_bp": 4.38, "note": "AUS200 Asia→Lon; Faraday 107e502"},
        {"id": "N109", "verdict": "UNDERPOWERED", "n": 122, "mean_bp": 19.69, "gate_bp": 4.23, "note": "CHFJPY LO 5d; Faraday 107e502"},
    ]

    board = {
        "c": "C-036",
        "when": "2026-10-02 ~22:35 Europe/Amsterdam",
        "absorb": {
            "main": "b7b8004 NEXT_STEPS v90 — C-035 + N102 DIAG_FAIL / N103 FAIL_STRESS; TRIAL 460; OPEN N104/N105",
            "faraday": "107e502 N106–N109 D-092.1 + OPEN N110/N111; prior 7d2d48a N104 UNDERPOWERED / N105 FAIL",
            "u2": "a70dc8b IDLE absorb v90; hold N110/N111; prior b9af560 N103 FAIL_STRESS (TRIAL 460 unchanged)",
            "prior_cto": "f7af392 C-035 N102 DIAG_FAIL / N103 DIAG_PASS→PREREG (U2 then FAIL_STRESS)",
        },
        "faraday_prescreen": faraday_absorb,
        "freeze": "OFF",
        "trial_count": 460,
        "trials_appended_by_cto": 0,
        "reserve_2025": "untouched",
        "track_3": "PAUSED",
        "results": rows,
        "promote_to_prereg": [r["label"] for r in rows if r["verdict"] == "DIAG_PASS"],
        "kill_circuit_note": (
            "cost-PASS→FAIL_T streak N87→N92→N100→N101 (4 formal); N103 cost-PASS→FAIL_STRESS; "
            "pivot ON; bar N104–N109 families + EURNZD-LO / UK→FRA40 / AUS Asia→Lon / GBPCHF-LO / JP225 Tokyo→Lon / CHFJPY-LO clones"
        ),
    }
    (OUT / "c036_board.json").write_text(json.dumps(board, indent=2))
    lines = [
        "# C-036 — absorb main v90 + Faraday N104–N109 + Lane-B diag N110/N111 (0 CTO trials)",
        "",
        f"**When:** {board['when']}. **TRIAL_COUNT:** 460. **FREEZE:** OFF. **Track-3:** PAUSED.",
        "",
        "## Absorb",
        "",
        "- `origin/main` `b7b8004` NEXT_STEPS **v90** (Manager ~22:10): C-035; N102 DIAG_FAIL / N103 FAIL_STRESS; formal OPEN N104/N105; TRIAL **460**.",
        "- U2 `b9af560` N103 FAIL_STRESS (geen trial); `a70dc8b` IDLE absorb v90; hold N110/N111.",
        "- Faraday `7d2d48a`: N104 UNDERPOWERED (N=98) / N105 FAIL → OPEN N106/N107.",
        "- Faraday `107e502`: N106–N108 FAIL / N109 UNDERPOWERED → OPEN **N110/N111** NEW_FAMILY AG/AH. **No PREREG.**",
        "- Prior CTO C-035 `f7af392` (N103 PREREG → U2 FAIL_STRESS). Reserve 2025+ untouched.",
        "",
        "## Faraday D-092.1 (already committed; CTO absorb only — 0 CTO trials)",
        "",
        "| Idee | mean_bp | n | gate | Verdict |",
        "|------|--------:|--:|-----:|---------|",
        "| N104 GBPCHF LO 5d | +10.62 | 98 | 4.53 | **UNDERPOWERED** |",
        "| N105 JP225 Tokyo→Lon | −2.77 | 392 | 4.53 | **FAIL** |",
        "| N106 EURNZD LO | +3.45 | 103 | 4.11 | **FAIL** |",
        "| N107 UK→FRA40 | +3.94 | 255 | 5.94 | **FAIL** |",
        "| N108 AUS Asia→Lon | −4.86 | 242 | 4.38 | **FAIL** |",
        "| N109 CHFJPY LO 5d | +19.69 | 122 | 4.23 | **UNDERPOWERED** |",
        "",
        "## Lane-B diagnostic N110/N111 (train 2021–2023; ≤2024; 0 CTO trials)",
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
        "- N110: DXYcash 08→12 CET impulse |bp|≥25 → same-dir entry 13:00 → flat 17:00; gate=3×RT 2.62=7.86.",
        "- N111: GBPAUD dayclose ≤22:00; ret5>0 → long; hold 5d non-overlap; swap earn not credited (D-100); gate=3×RT 1.46=4.38.",
        "- DIAG_PASS → CTO freezes PREREG for U2 (C-031/C-035 precedent); else drop / replace NEW_FAMILY (D-094).",
        "- No thr-grid / no EURUSD twin / no GBPCHF twin / no Asia→Lon rewrite / no soft gate / no n-inflate on UNDERPOWERED.",
        "- Kill: bar N104–N109 families + EURNZD-LO / UK→FRA40 / AUS Asia→Lon / GBPCHF-LO / JP225 Tokyo→Lon / CHFJPY-LO + prior N75–N103 / EMB / CRACK / …",
        "",
        f"**Promote candidates (DIAG_PASS):** {board['promote_to_prereg'] or 'none'}.",
        "",
        "Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.",
        "",
    ]
    (OUT / "c036_report.md").write_text("\n".join(lines))
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
