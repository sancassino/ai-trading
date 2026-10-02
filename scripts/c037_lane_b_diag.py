#!/usr/bin/env python3
"""C-037 — absorb main v92 + U2 N112/N113 + Lane-B diag N114/N115 (0 CTO trials).

Faraday 791a17c PREREG'd N112/N113 (both died at U2) + OPEN N114/N115 NEW_FAMILY AI/AJ.
Diagnostic screens only until DIAG_PASS → PREREG freeze.
Reserve 2025+ untouched. Train 2021–2023; hard cut ≤2024-12-31.
"""
from __future__ import annotations

import gzip
import io
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/cto/c037_absorb_v92_n112_n115"
DAILY = ROOT / "data/daily"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
HARD_CUT = pd.Timestamp("2024-12-31")
RT_US500 = 0.78
GATE_US500 = 3.0 * RT_US500  # 2.34


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


def load_hyg_close() -> pd.Series:
    path = DAILY / "HYG.csv"
    raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    body = [ln for ln in raw if not ln.startswith("#")]
    sep = ";" if body and ";" in body[0] else ","
    df = pd.read_csv(io.StringIO("\n".join(body)), sep=sep)
    cols_l = {c.lower().replace(" ", ""): c for c in df.columns}
    dc = cols_l.get("date") or cols_l.get("observation_date")
    cc = cols_l.get("close") or cols_l.get("adjclose") or df.columns[-1]
    s = pd.Series(
        pd.to_numeric(df[cc], errors="coerce").values,
        index=pd.to_datetime(df[dc].astype(str).str.replace(".", "-", regex=False)),
        name="HYG",
    )
    s = s[~s.index.duplicated(keep="last")].sort_index()
    s = s[s.index <= HARD_CUT].dropna()
    return s


def zscore(s: pd.Series, win: int) -> pd.Series:
    mu = s.rolling(win, min_periods=win).mean()
    sd = s.rolling(win, min_periods=win).std(ddof=0)
    return (s - mu) / sd.replace(0, np.nan)


def diag_n114():
    """HYG z120/combo → US500cash session-flat 15:30→21:00 CET; gate 2.34."""
    hyg = load_hyg_close()
    z120 = zscore(hyg, 120)
    d20 = hyg / hyg.shift(20) - 1.0
    pos = pd.Series(0.0, index=hyg.index, dtype=float)
    pos[(z120 > 0.5) & (d20 > 0)] = 1.0
    pos[(z120 < -0.5) & (d20 < 0)] = -1.0
    pos.index = pd.to_datetime(pos.index).normalize()
    pos = pos[~pos.index.duplicated(keep="last")].sort_index()

    us = load_m5("data/m5gz/US500cash.csv.gz")
    us = us[(us["time"] >= TRAIN_START) & (us["time"] <= TRAIN_END)].copy()
    us["day"] = us["time"].dt.normalize()
    pnls = []
    for day in sorted(us["day"].unique()):
        prior = pos[pos.index < day]
        if prior.empty:
            continue
        side = float(prior.iloc[-1])
        if side == 0.0 or not np.isfinite(side):
            continue
        g = us[us["day"] == day]
        bent = first_bar_in(g, day, 15, 30, 15)
        bex = last_bar_le(g, day, 21, 0)
        if bent is None or bex is None or bex["time"] <= bent["time"]:
            continue
        p0 = float(bent["close"])
        p1 = float(bex["close"])
        if p0 <= 0:
            continue
        pnls.append(side * 1e4 * (p1 / p0 - 1.0))
    return trade_stats(
        pnls,
        GATE_US500,
        "N114_HYG_CREDIT_STRESS_US500_SESSION",
        "NEW_FAMILY AI; HYG z120/combo → US500 15:30→21:00; gate=3×RT 0.78=2.34; ≠ N100 EMB; session-flat",
    )


def diag_n115():
    """EURUSD Lon-AM |bp|≥25 → same-dir US500 15:30→21:00 CET; gate 2.34."""
    eurusd = load_m5("data/m5gz/EURUSD.csv.gz")
    us = load_m5("data/m5gz/US500cash.csv.gz")
    eurusd = eurusd[(eurusd["time"] >= TRAIN_START) & (eurusd["time"] <= TRAIN_END)].copy()
    us = us[(us["time"] >= TRAIN_START) & (us["time"] <= TRAIN_END)].copy()
    eurusd["day"] = eurusd["time"].dt.normalize()
    us["day"] = us["time"].dt.normalize()
    us_days = {d: g for d, g in us.groupby("day")}
    pnls = []
    for day, g in eurusd.groupby("day"):
        b0800 = first_bar_in(g, day, 8, 0, 15)
        b1200 = first_bar_in(g, day, 12, 0, 15)
        if b0800 is None or b1200 is None:
            continue
        p0 = float(b0800["close"])
        p1 = float(b1200["close"])
        if p0 <= 0:
            continue
        eur_am_bp = 1e4 * (p1 / p0 - 1.0)
        if not np.isfinite(eur_am_bp) or abs(eur_am_bp) < 25.0:
            continue
        side = 1.0 if eur_am_bp >= 25.0 else -1.0
        ug = us_days.get(day)
        if ug is None:
            continue
        bent = first_bar_in(ug, day, 15, 30, 15)
        bex = last_bar_le(ug, day, 21, 0)
        if bent is None or bex is None or bex["time"] <= bent["time"]:
            continue
        e0 = float(bent["close"])
        e1 = float(bex["close"])
        if e0 <= 0:
            continue
        pnls.append(side * 1e4 * (e1 / e0 - 1.0))
    return trade_stats(
        pnls,
        GATE_US500,
        "N115_EURUSD_LON_AM_US500_NY_MACRO",
        "NEW_FAMILY AJ; EURUSD Lon-AM |bp|≥25 → same-dir US500 15:30→21:00; gate=3×RT 0.78=2.34; ≠ N110 DXY Lon→EU / N83 opposite",
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [diag_n114(), diag_n115()]
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "c037_family_diag.csv", index=False)

    u2_absorb = [
        {
            "id": "N112",
            "verdict": "FAIL_T",
            "n_train": 188,
            "mean_bp": 7.827,
            "gate_bp": 2.34,
            "trial": 461,
            "note": "GAS_EQUITY_MACRO; U2 d1dd863; cost/stress PASS; formal t<2; TRIAL 460→461",
        },
        {
            "id": "N113",
            "verdict": "FAIL_COST_GATE",
            "n_train": 305,
            "mean_bp": 1.601,
            "gate_bp": 2.34,
            "trial": 461,
            "note": "SILVER_GOLD_RATIO; U2 954680a; mean < gate; geen trial; TRIAL blijft 461",
        },
    ]

    board = {
        "c": "C-037",
        "when": "2026-10-02 ~23:05 Europe/Amsterdam",
        "absorb": {
            "main": "e988749 NEXT_STEPS v92 — N112 FAIL_T + N113 FAIL_COST_GATE; TRIAL 461; OPEN N114/N115",
            "faraday": "791a17c PREREG N112/N113 + OPEN N114/N115 NEW_FAMILY AI/AJ",
            "u2": "d1dd863 N112 FAIL_T (TRIAL 461); 954680a N113 FAIL_COST_GATE (TRIAL stays 461); IDLE/HOLD",
            "s2": "35e38ac cycle_2240 GAS+SILVER promote → died at U2",
            "prior_cto": "f3cf632 C-036 N110/N111 DIAG_FAIL",
        },
        "u2_results": u2_absorb,
        "freeze": "OFF",
        "trial_count": 461,
        "trials_appended_by_cto": 0,
        "reserve_2025": "untouched",
        "track_3": "PAUSED",
        "results": rows,
        "promote_to_prereg": [r["label"] for r in rows if r["verdict"] == "DIAG_PASS"],
        "kill_circuit_note": (
            "cost-PASS→FAIL_T streak N87→N92→N100→N101→N112 (≥5); pivot ON; "
            "N103 cost-PASS→FAIL_STRESS; N113 FAIL_COST_GATE; "
            "bar GAS_EQUITY / SILVER_GOLD / N75–N113 + prior clones; keep HYG≠EMB; EURUSD→US500 ≠ DXY Lon→EU / N83"
        ),
    }
    (OUT / "c037_board.json").write_text(json.dumps(board, indent=2))
    lines = [
        "# C-037 — absorb main v92 + U2 N112/N113 + Lane-B diag N114/N115 (0 CTO trials)",
        "",
        f"**When:** {board['when']}. **TRIAL_COUNT:** 461. **FREEZE:** OFF. **Track-3:** PAUSED.",
        "",
        "## Absorb",
        "",
        "- `origin/main` `e988749` NEXT_STEPS **v92** (Manager ~23:05): N112 FAIL_T + N113 FAIL_COST_GATE; TRIAL **461**; formal OPEN **N114/N115**.",
        "- Faraday `791a17c`: PREREG N112/N113 from S2 cycle_2240; OPEN N114/N115 NEW_FAMILY AI/AJ.",
        "- U2 `d1dd863` N112 GAS_EQUITY_MACRO **FAIL_T** (TRIAL 460→461); `954680a` N113 SILVER_GOLD_RATIO **FAIL_COST_GATE** (geen trial).",
        "- S2 `35e38ac` cycle_2240 GAS+SILVER promote → both died. Prior CTO C-036 `f3cf632`. Reserve 2025+ untouched.",
        "",
        "## U2 formal (already committed; CTO absorb only — 0 CTO trials)",
        "",
        "| Idee | mean_bp | n | gate | Verdict | Trial |",
        "|------|--------:|--:|-----:|---------|------:|",
        "| N112 GAS_EQUITY_MACRO | +7.83 | 188 | 2.34 | **FAIL_T** | **461** |",
        "| N113 SILVER_GOLD_RATIO | +1.60 | 305 | 2.34 | **FAIL_COST_GATE** | 461 (no bump) |",
        "",
        "## Lane-B diagnostic N114/N115 (train 2021–2023; ≤2024; 0 CTO trials)",
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
        "- N114: HYG close z120/combo (z>±0.5 ∧ d20 same sign) day t → US500 session-flat 15:30→21:00 CET day t+1; gate=3×RT 0.78=2.34; ≠ N100 EMB.",
        "- N115: EURUSD Lon-AM 08→12 CET |bp|≥25 → same-dir US500 @15:30 → flat 21:00; gate=3×RT 0.78=2.34; ≠ N110 DXY Lon→EU / N83 opposite fade.",
        "- DIAG_PASS → CTO freezes PREREG for U2 (C-031/C-035 precedent); else drop / replace NEW_FAMILY (D-094).",
        "- No thr-grid / no LQD twin / no EMB rewrite / no DXY substitute / no US100 rewrite / no overnight / no soft gate.",
        "- Kill: bar GAS_EQUITY / SILVER_GOLD / N75–N113 + prior; keep HYG≠EMB (N114); EURUSD→US500 ≠ DXY Lon→EU / N83 (N115).",
        "",
        f"**Promote candidates (DIAG_PASS):** {board['promote_to_prereg'] or 'none'}.",
        "",
        "Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.",
        "",
    ]
    (OUT / "c037_report.md").write_text("\n".join(lines))
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
