#!/usr/bin/env python3
"""C-039 — absorb main v96 + S2 cycle_2346 + Lane-B diag N124/N125 (0 CTO trials).

Pipeline starved (OPEN empty after C-038 N122/N123 DIAG_FAIL). S2 13fe10c promoted
YIELD_CURVE_2S10S + DEFENSIVE_CYCLICAL (cycle_2346). Faraday tip still 47e0eab.
CTO picks up S2 survivors as NEW_FAMILY AS/AT → session-flat Lane-B (C-031/C-037 precedent).
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
OUT = ROOT / "results/cto/c039_absorb_v96_n124_n125"
DAILY = ROOT / "data/daily"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
HARD_CUT = pd.Timestamp("2024-12-31")
RT_US500 = 0.78
GATE_US500 = 3.0 * RT_US500  # 2.34
MIN_N = 150


def load_daily_close(sym: str) -> pd.Series:
    path = DAILY / f"{sym}.csv"
    raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    body = [ln for ln in raw if not ln.startswith("#")]
    sep = ";" if body and ";" in body[0] else ","
    df = pd.read_csv(io.StringIO("\n".join(body)), sep=sep)
    cols = {c.lower().replace(" ", ""): c for c in df.columns}
    dc = cols.get("date") or cols.get("observation_date")
    cc = cols.get("adjclose") or cols.get("close") or df.columns[-1]
    s = pd.Series(
        pd.to_numeric(df[cc], errors="coerce").values,
        index=pd.DatetimeIndex(
            pd.to_datetime(df[dc].astype(str).str.replace(".", "-", regex=False))
        ).normalize(),
        name=sym,
    )
    s = s[~s.index.duplicated(keep="last")].sort_index().dropna()
    return s[s.index <= HARD_CUT]


def zscore(s: pd.Series, win: int) -> pd.Series:
    mu = s.rolling(win, min_periods=max(20, win // 3)).mean()
    sd = s.rolling(win, min_periods=max(20, win // 3)).std(ddof=0)
    return (s - mu) / sd.replace(0, np.nan)


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


def trade_stats(pnls_bp, gate_bp, label, notes="", years=None):
    arr = np.asarray(pnls_bp, dtype=float)
    arr = arr[np.isfinite(arr)]
    n = len(arr)
    mean = float(np.mean(arr)) if n else float("nan")
    med = float(np.median(arr)) if n else float("nan")
    if n >= 2 and float(np.std(arr, ddof=1)) > 0:
        t = mean / (float(np.std(arr, ddof=1)) / math.sqrt(n))
    else:
        t = float("nan")
    half = n // 2
    m1 = float(np.mean(arr[:half])) if half else float("nan")
    m2 = float(np.mean(arr[half:])) if n - half else float("nan")
    if n >= MIN_N and np.isfinite(mean) and mean >= gate_bp:
        verdict = "DIAG_PASS"
    elif n < MIN_N and np.isfinite(mean) and mean >= gate_bp:
        verdict = "UNDERPOWERED"
    else:
        verdict = "DIAG_FAIL"
    return {
        "label": label,
        "n": n,
        "mean_bp": round(mean, 3) if n else None,
        "median_bp": round(med, 3) if n else None,
        "day_t": round(t, 3) if n >= 2 else None,
        "h1_mean_bp": round(m1, 3) if half else None,
        "h2_mean_bp": round(m2, 3) if n - half else None,
        "gate_bp": gate_bp,
        "verdict": verdict,
        "years": years or {},
        "notes": notes,
    }


def session_flat_pnls(pos: pd.Series, us: pd.DataFrame):
    """pos indexed by signal day; trade US500 session-flat next day 15:30→21:00."""
    pos = pos.copy()
    pos.index = pd.to_datetime(pos.index).normalize()
    pos = pos[~pos.index.duplicated(keep="last")].sort_index()
    us = us.copy()
    us["day"] = us["time"].dt.normalize()
    pnls = []
    by_year: dict[str, list[float]] = {"2021": [], "2022": [], "2023": []}
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
        pnl = side * 1e4 * (p1 / p0 - 1.0)
        pnls.append(pnl)
        y = str(pd.Timestamp(day).year)
        if y in by_year:
            by_year[y].append(pnl)
    years = {y: round(float(np.mean(v)), 3) for y, v in by_year.items() if v}
    return pnls, years


def diag_n124():
    """10Y-3M z60/thr1.5 flatten_fade → US500cash session-flat; gate 2.34; NEW_FAMILY AS."""
    y10 = load_daily_close("YLD_US10Y")
    y3m = load_daily_close("YLD_US3M")
    slope = (y10 - y3m).dropna()
    z = zscore(slope, 60)
    pos = pd.Series(0.0, index=slope.index, dtype=float)
    # flatten_fade: extreme steep (z>thr) → SHORT; extreme flatten (z<-thr) → LONG
    pos[z > 1.5] = -1.0
    pos[z < -1.5] = 1.0

    us = load_m5("data/m5gz/US500cash.csv.gz")
    us = us[(us["time"] >= TRAIN_START) & (us["time"] <= TRAIN_END)]
    pnls, years = session_flat_pnls(pos, us)
    return trade_stats(
        pnls,
        GATE_US500,
        "N124_YIELD_CURVE_2S10S_US500_SESSION",
        "NEW_FAMILY AS; 10Y-3M z60/thr1.5 flatten_fade → US500 15:30→21:00; gate=3×RT 0.78=2.34; ≠ TLT/TIP/REIT_RATE/RATE_CURVE",
        years=years,
    )


def diag_n125():
    """XLU/XLI z40/thr0.5 defensive_high → US500cash session-flat; gate 2.34; NEW_FAMILY AT.
    Prefer US500 twin (S2 NDX short-bias survivor; POST-N78 prefer US500).
    """
    xlu = load_daily_close("XLU")
    xli = load_daily_close("XLI")
    rel = (xlu / xli).dropna()
    z = zscore(rel, 40)
    pos = pd.Series(0.0, index=rel.index, dtype=float)
    # defensive_high: defensive outperformance (z>thr) → SHORT equity; underperf → LONG
    pos[z > 0.5] = -1.0
    pos[z < -0.5] = 1.0

    us = load_m5("data/m5gz/US500cash.csv.gz")
    us = us[(us["time"] >= TRAIN_START) & (us["time"] <= TRAIN_END)]
    pnls, years = session_flat_pnls(pos, us)
    return trade_stats(
        pnls,
        GATE_US500,
        "N125_DEFENSIVE_CYCLICAL_US500_SESSION",
        "NEW_FAMILY AT; XLU/XLI z40/thr0.5 defensive_high → US500 15:30→21:00; gate=3×RT 0.78=2.34; ≠ SECTOR_DISP; prefer US500 twin vs NDX",
        years=years,
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [diag_n124(), diag_n125()]
    flat = []
    for r in rows:
        row = {k: v for k, v in r.items() if k != "years"}
        for y, v in (r.get("years") or {}).items():
            row[f"y{y}"] = v
        flat.append(row)
    pd.DataFrame(flat).to_csv(OUT / "c039_family_diag.csv", index=False)

    board = {
        "c": "C-039",
        "when": "2026-10-02 ~23:56 Europe/Amsterdam",
        "absorb": {
            "main": "d6b9867 NEXT_STEPS v96 — absorb C-038; TRIAL 464; OPEN empty; FREEZE OFF",
            "faraday": "47e0eab (unchanged) — N122/N123 OPEN died at C-038 DIAG_FAIL; no new OPEN",
            "u2": "6ed73cf IDLE/HOLD absorb v96; TRIAL 464; no live PREREG",
            "s2": "13fe10c cycle_2346 PROMOTE YIELD_CURVE_2S10S + DEFENSIVE_CYCLICAL",
            "prior_cto": "1a22e81 C-038 N122/N123 DIAG_FAIL",
        },
        "freeze": "OFF",
        "trial_count": 464,
        "trials_appended_by_cto": 0,
        "reserve_2025": "untouched",
        "track_3": "PAUSED",
        "live_prereg": None,
        "results": rows,
        "promote_to_prereg": [r["label"] for r in rows if r["verdict"] == "DIAG_PASS"],
        "kill_circuit_note": (
            "cost-PASS→FAIL_T streak N100+N101+N112+N114+N116+N118 (≥5); pivot ON; "
            "bar TIP/IWM/VNQ/EEM/DBC/EFA→US500 + TLT/CPER/HYG/EURUSD Lon-AM + GAS/SILVER + N75–N123; "
            "N124/N125 = NEW_FAMILY AS/AT (yield-curve slope / defensive-cyclical relative — not ETF→US500 stress clones)"
        ),
    }
    (OUT / "c039_board.json").write_text(json.dumps(board, indent=2))
    lines = [
        "# C-039 — absorb main v96 + S2 cycle_2346 + Lane-B diag N124/N125 (0 CTO trials)",
        "",
        f"**When:** {board['when']}. **TRIAL_COUNT:** 464. **FREEZE:** OFF. **Track-3:** PAUSED. **Live PREREG:** none (pending diag).",
        "",
        "## Absorb",
        "",
        "- `origin/main` `d6b9867` NEXT_STEPS **v96** (Manager ~23:39): absorb C-038; N120/N121 FAIL; N122/N123 DIAG_FAIL; TRIAL **464**; formal OPEN **empty**.",
        "- Faraday `47e0eab` (unchanged): no new OPEN after AQ/AR died.",
        "- U2 `6ed73cf` IDLE/HOLD absorb v96; TRIAL **464**.",
        "- S2 `13fe10c` (~23:53): Lane-A PROMOTE **YIELD_CURVE_2S10S** + **DEFENSIVE_CYCLICAL** (cycle_2346).",
        "- Prior CTO C-038 `1a22e81`. Reserve 2025+ untouched. Pipeline starved → CTO picks up S2 survivors as N124/N125.",
        "",
        "## Lane-B diagnostic N124/N125 (train 2021–2023; ≤2024; 0 CTO trials)",
        "",
        "| Idee | mean_bp | n | gate | day_t | h1 | h2 | years | Verdict |",
        "|------|--------:|--:|-----:|------:|---:|---:|-------|---------|",
    ]
    for r in rows:
        years = r.get("years") or {}
        ystr = "/".join(f"{y}:{years[y]}" for y in ("2021", "2022", "2023") if y in years)
        lines.append(
            f"| {r['label']} | {r['mean_bp']} | {r['n']} | {r['gate_bp']} | {r['day_t']} | "
            f"{r['h1_mean_bp']} | {r['h2_mean_bp']} | {ystr or '—'} | **{r['verdict']}** |"
        )
    lines += [
        "",
        "### Notes",
        "",
        "- N124: 10Y−3M slope z60 thr1.5 flatten_fade (z>+1.5→SHORT; z<−1.5→LONG) day t → US500 session-flat 15:30→21:00 CET day t+1; gate=3×RT 0.78=2.34; ≠ TLT/TIP/REIT_RATE/RATE_CURVE.",
        "- N125: XLU/XLI relative z40 thr0.5 defensive_high (z>+0.5→SHORT; z<−0.5→LONG) day t → US500 session-flat 15:30→21:00; gate=3×RT 0.78=2.34; ≠ SECTOR_DISP; US500 twin preferred over NDX short-bias.",
        "- DIAG_PASS → CTO freezes PREREG for U2 (C-031/C-035/C-037 precedent); else drop / replace NEW_FAMILY (D-094).",
        "- No thr-grid / no overnight / no soft gate / no TLT rewrite / no SECTOR_DISP rewrite.",
        "- Kill: bar TIP/IWM/VNQ/EEM/DBC/EFA→US500 + TLT/CPER/HYG/EURUSD Lon-AM + GAS/SILVER + N75–N123; N124/N125 novelty AS/AT.",
        "",
        f"**Promote candidates (DIAG_PASS):** {board['promote_to_prereg'] or 'none'}.",
        "",
        "Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.",
        "",
    ]
    (OUT / "c039_report.md").write_text("\n".join(lines))
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
