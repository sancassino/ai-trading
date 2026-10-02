#!/usr/bin/env python3
"""C-038 — absorb main v95 + Faraday N118/N120–N123 + Lane-B diag N122/N123 (0 CTO trials).

Faraday 47e0eab: N118 FAIL_T sync; N120/N121 D-092.1 FAIL; OPEN N122/N123 NEW_FAMILY AQ/AR.
Manager v95 still lists OPEN N120/N121 (stale vs Faraday tip).
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
OUT = ROOT / "results/cto/c038_absorb_v95_n118_n123"
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
    cc = cols.get("close") or cols.get("adjclose") or df.columns[-1]
    s = pd.Series(
        pd.to_numeric(df[cc], errors="coerce").values,
        index=pd.DatetimeIndex(
            pd.to_datetime(df[dc].astype(str).str.replace(".", "-", regex=False))
        ).normalize(),
        name=sym,
    )
    s = s[~s.index.duplicated(keep="last")].sort_index().dropna()
    return s[s.index <= HARD_CUT]


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
    years = {
        y: round(float(np.mean(v)), 3) for y, v in by_year.items() if v
    }
    return pnls, years


def diag_n122():
    """DBC z120/d20 combo → US500cash session-flat; gate 2.34; NEW_FAMILY AQ."""
    dbc = load_daily_close("DBC")
    z120 = (dbc - dbc.rolling(120, min_periods=120).mean()) / dbc.rolling(
        120, min_periods=120
    ).std(ddof=0).replace(0, np.nan)
    d20 = dbc / dbc.shift(20) - 1.0
    pos = pd.Series(0.0, index=dbc.index, dtype=float)
    pos[(z120 > 0.5) & (d20 > 0)] = 1.0
    pos[(z120 < -0.5) & (d20 < 0)] = -1.0

    us = load_m5("data/m5gz/US500cash.csv.gz")
    us = us[(us["time"] >= TRAIN_START) & (us["time"] <= TRAIN_END)]
    pnls, years = session_flat_pnls(pos, us)
    return trade_stats(
        pnls,
        GATE_US500,
        "N122_DBC_COMMODITY_STRESS_US500_SESSION",
        "NEW_FAMILY AQ; DBC z120/d20 combo → US500 15:30→21:00; gate=3×RT 0.78=2.34; ≠ CPER/GAS/SILVER/CRACK",
        years=years,
    )


def diag_n123():
    """EFA z40 stress_buy → US500cash session-flat; gate 2.34; NEW_FAMILY AR."""
    efa = load_daily_close("EFA")
    z40 = (efa - efa.rolling(40, min_periods=40).mean()) / efa.rolling(
        40, min_periods=40
    ).std(ddof=0).replace(0, np.nan)
    pos = pd.Series(0.0, index=efa.index, dtype=float)
    pos[z40 > 1.5] = -1.0
    pos[z40 < -1.5] = 1.0

    us = load_m5("data/m5gz/US500cash.csv.gz")
    us = us[(us["time"] >= TRAIN_START) & (us["time"] <= TRAIN_END)]
    pnls, years = session_flat_pnls(pos, us)
    return trade_stats(
        pnls,
        GATE_US500,
        "N123_EFA_DM_EXUS_STRESS_US500_SESSION",
        "NEW_FAMILY AR; EFA z40 stress_buy → US500 15:30→21:00; gate=3×RT 0.78=2.34; ≠ EEM/EMB/IWM",
        years=years,
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [diag_n122(), diag_n123()]
    # Flatten years for CSV
    flat = []
    for r in rows:
        row = {k: v for k, v in r.items() if k != "years"}
        for y, v in (r.get("years") or {}).items():
            row[f"y{y}"] = v
        flat.append(row)
    pd.DataFrame(flat).to_csv(OUT / "c038_family_diag.csv", index=False)

    board = {
        "c": "C-038",
        "when": "2026-10-02 ~23:30 Europe/Amsterdam",
        "absorb": {
            "main": "6665e3e NEXT_STEPS v95 — N118 FAIL_T; TRIAL 464; OPEN N120/N121 (stale vs Faraday)",
            "faraday": "47e0eab N118 FAIL_T sync; N120/N121 D-092.1 FAIL; OPEN N122/N123 NEW_FAMILY AQ/AR",
            "u2": "7834a1a IDLE/HOLD post-N118 FAIL_T (TRIAL 464); tip 9e928af material 9a00524",
            "prior_cto": "696b4c0 C-037 N114 PREREG / N115 DIAG_FAIL",
        },
        "faraday_prescreen": {
            "N120": {"n": 342, "mean_bp": -0.38, "gate_bp": 2.34, "verdict": "FAIL"},
            "N121": {"n": 172, "mean_bp": 0.08, "gate_bp": 2.34, "verdict": "FAIL"},
            "N118": {
                "verdict": "FAIL_T",
                "trial": 464,
                "note": "TIP_REALRATE_STRESS; cost+stress PASS; t/NW 0.99; test −4.20",
            },
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
            "N103+N117 FAIL_STRESS; N113 FAIL_COST_GATE; "
            "bar TIP/IWM/VNQ/EEM→US500 + TLT/CPER/HYG/EURUSD Lon-AM + GAS/SILVER + prior"
        ),
    }
    (OUT / "c038_board.json").write_text(json.dumps(board, indent=2))
    lines = [
        "# C-038 — absorb main v95 + Faraday N118/N120–N123 + Lane-B diag N122/N123 (0 CTO trials)",
        "",
        f"**When:** {board['when']}. **TRIAL_COUNT:** 464. **FREEZE:** OFF. **Track-3:** PAUSED. **Live PREREG:** none.",
        "",
        "## Absorb",
        "",
        "- `origin/main` `6665e3e` NEXT_STEPS **v95** (Manager ~23:22): N118 FAIL_T; TRIAL **464**; formal OPEN **N120/N121** (stale — Faraday already screened).",
        "- Faraday `47e0eab` (~23:23): N118 FAIL_T sync; **N120/N121 D-092.1 FAIL**; OPEN **N122/N123** NEW_FAMILY AQ/AR.",
        "- U2 `7834a1a` IDLE/HOLD post-N118 (material `9a00524`→`9e928af`); TRIAL **464**.",
        "- Prior CTO C-037 `696b4c0` (N114 later FAIL_T @ U2 / absorbed into main v93+). Reserve 2025+ untouched.",
        "",
        "## Faraday D-092.1 already closed (absorb only — 0 CTO trials)",
        "",
        "| Idee | mean_bp | n | gate | Verdict |",
        "|------|--------:|--:|-----:|---------|",
        "| N118 TIP_REALRATE_STRESS | +5.38 (train) | 359 | 2.34 | **FAIL_T** (trial **464**) |",
        "| N120 VNQ_REIT→US500 | −0.38 | 342 | 2.34 | **FAIL** (geen PREREG) |",
        "| N121 EEM_EM_EQUITY→US500 | +0.08 | 172 | 2.34 | **FAIL** (geen PREREG) |",
        "",
        "## Lane-B diagnostic N122/N123 (train 2021–2023; ≤2024; 0 CTO trials)",
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
        "- N122: DBC close z120/d20 combo (z>±0.5 ∧ d20 same sign) day t → US500 session-flat 15:30→21:00 CET day t+1; gate=3×RT 0.78=2.34; ≠ CPER/GAS/SILVER/CRACK.",
        "- N123: EFA close z40 stress_buy (z>+1.5 → SHORT; z<−1.5 → LONG) day t → US500 session-flat 15:30→21:00; gate=3×RT 0.78=2.34; ≠ EEM/EMB/IWM.",
        "- DIAG_PASS → CTO freezes PREREG for U2 (C-031/C-035/C-037 precedent); else drop / replace NEW_FAMILY (D-094).",
        "- No thr-grid / no CPER rewrite / no EEM rewrite / no overnight / no soft gate.",
        "- Kill: bar TIP/IWM/VNQ/EEM→US500 + TLT/CPER/HYG/EURUSD Lon-AM + GAS/SILVER + N75–N121; keep DBC≠CPER; EFA≠EEM.",
        "",
        f"**Promote candidates (DIAG_PASS):** {board['promote_to_prereg'] or 'none'}.",
        "",
        "Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.",
        "",
    ]
    (OUT / "c038_report.md").write_text("\n".join(lines))
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
