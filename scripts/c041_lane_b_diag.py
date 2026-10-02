#!/usr/bin/env python3
"""C-041 — absorb main v102 + Faraday e1bf004 + Lane-B diag N142/N143 (0 CTO trials).

Manager NEXT_STEPS v102 still lists Faraday tip f5523fb / OPEN N138/N139, but Faraday
e1bf004 (~00:56) already closed N138–N141 and filed OPEN N142 US30_US500_XS /
N143 XLE_ENERGY_EQUITY_STRESS. U2 IDLE/HOLD TRIAL 470; no live PREREG.
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
OUT = ROOT / "results/cto/c041_absorb_v102_n142_n143"
DAILY = ROOT / "data/daily"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
HARD_CUT = pd.Timestamp("2024-12-31")
RT_US30 = 0.45
RT_US500 = 0.78
GATE_142 = 3.0 * (RT_US30 + RT_US500)  # 3.69
GATE_143 = 3.0 * RT_US500  # 2.34
MIN_N = 150
THR_142 = 1.5
THR_143 = 1.0  # fade_extreme frozen from S2
ZWIN = 40


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
    mu = s.rolling(win, min_periods=win).mean()
    sd = s.rolling(win, min_periods=win).std(ddof=0)
    return (s - mu) / sd.replace(0, np.nan)


def load_m5(rel: str) -> pd.DataFrame:
    with gzip.open(ROOT / rel, "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["close"]).sort_values("time")
    df = df[(df["time"] >= TRAIN_START) & (df["time"] <= TRAIN_END)]
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


def daily_close_22(df: pd.DataFrame) -> pd.Series:
    d = df.copy()
    d["day"] = d["time"].dt.normalize()
    cut = d["day"] + pd.Timedelta(hours=22)
    sub = d[d["time"] <= cut]
    s = sub.groupby("day")["close"].last().sort_index()
    return s[s > 0]


def by_day(df: pd.DataFrame) -> dict:
    d = df.copy()
    d["day"] = d["time"].dt.normalize()
    return {day: g for day, g in d.groupby("day", sort=False)}


def leg_ret_bp(g, day, side: int, h0=15, m0=30, h1=21, m1=0):
    b0 = first_bar_in(g, day, h0, m0, 15)
    b1 = last_bar_le(g, day, h1, m1)
    if b0 is None or b1 is None:
        return None
    if b1["time"] <= b0["time"]:
        return None
    p0 = float(b0["close"])
    p1 = float(b1["close"])
    if p0 <= 0 or p1 <= 0:
        return None
    return side * 1e4 * (p1 / p0 - 1.0)


def trade_stats(pnls_bp, gate_bp, label, notes="", years=None, n_long=None, n_short=None):
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
        "n_long": n_long,
        "n_short": n_short,
        "gate_bp": gate_bp,
        "verdict": verdict,
        "years": years or {},
        "notes": notes,
    }


def diag_n142():
    """US30/US500 cash-index ratio z40 thr±1.5 basis fade, both legs session-flat."""
    us30 = load_m5("data/m5gz/US30cash.csv.gz")
    us500 = load_m5("data/m5gz/US500cash.csv.gz")
    ca = daily_close_22(us30)
    cb = daily_close_22(us500)
    both = pd.concat([ca.rename("a"), cb.rename("b")], axis=1).dropna()
    ratio = (both["a"] / both["b"]).rename("ratio")
    z40 = zscore(ratio, ZWIN)
    pos = pd.Series(0.0, index=ratio.index)
    # z>+thr → SHORT US30 + LONG US500 (Dow rich); z<-thr → LONG US30 + SHORT US500
    pos[z40 > THR_142] = -1.0
    pos[z40 < -THR_142] = 1.0
    ga = by_day(us30)
    gb = by_day(us500)
    pnls = []
    sides = []
    by_year: dict[str, list[float]] = {"2021": [], "2022": [], "2023": []}
    days = list(pos.index)
    for i in range(1, len(days)):
        sig_day = days[i - 1]
        day = days[i]
        if day < TRAIN_START or day > TRAIN_END:
            continue
        side = float(pos.loc[sig_day])
        if side == 0.0 or not np.isfinite(side):
            continue
        gda = ga.get(day)
        gdb = gb.get(day)
        if gda is None or gdb is None:
            continue
        r_a = leg_ret_bp(gda, day, int(side))
        r_b = leg_ret_bp(gdb, day, int(-side))
        if r_a is None or r_b is None:
            continue
        pnl = r_a + r_b
        pnls.append(pnl)
        sides.append(side)
        y = str(pd.Timestamp(day).year)
        if y in by_year:
            by_year[y].append(pnl)
    years = {y: round(float(np.mean(v)), 3) for y, v in by_year.items() if v}
    n_long = int(sum(1 for s in sides if s > 0))
    n_short = int(sum(1 for s in sides if s < 0))
    return trade_stats(
        pnls,
        GATE_142,
        "N142_US30_US500_XS_SESSION",
        (
            f"NEW_FAMILY BK; US30/US500 ratio z{ZWIN}/thr{THR_142} basis fade both legs "
            f"15:30→21:00; gate=3×(0.45+0.78)=3.69; ≠ N81/N138/N143/IDX_SHORT/N87"
        ),
        years=years,
        n_long=n_long,
        n_short=n_short,
    )


def diag_n143():
    """XLE level z40 thr±1.0 fade_extreme → US500 session-flat (S2 cycle_0047 map)."""
    px = load_daily_close("XLE")
    z = zscore(px, ZWIN)
    pos = pd.Series(0.0, index=px.index, dtype=float)
    # fade_extreme: z>+1 → SHORT US500; z<-1 → LONG US500
    pos[z > THR_143] = -1.0
    pos[z < -THR_143] = 1.0

    us = load_m5("data/m5gz/US500cash.csv.gz")
    us = us.copy()
    us["day"] = us["time"].dt.normalize()
    pos = pos.copy()
    pos.index = pd.to_datetime(pos.index).normalize()
    pos = pos[~pos.index.duplicated(keep="last")].sort_index()
    pnls = []
    sides = []
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
        sides.append(side)
        y = str(pd.Timestamp(day).year)
        if y in by_year:
            by_year[y].append(pnl)
    years = {y: round(float(np.mean(v)), 3) for y, v in by_year.items() if v}
    n_long = int(sum(1 for s in sides if s > 0))
    n_short = int(sum(1 for s in sides if s < 0))
    return trade_stats(
        pnls,
        GATE_143,
        "N143_XLE_ENERGY_EQUITY_STRESS_US500_SESSION",
        (
            f"NEW_FAMILY BL; XLE z{ZWIN}/thr{THR_143} fade_extreme → US500 15:30→21:00; "
            f"gate=3×RT 0.78=2.34; S2 5a21939 cycle_0047; ≠ GAS/CRACK/N98/N134/N140/N142"
        ),
        years=years,
        n_long=n_long,
        n_short=n_short,
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [diag_n142(), diag_n143()]
    flat = []
    for r in rows:
        row = {k: v for k, v in r.items() if k != "years"}
        for y, v in (r.get("years") or {}).items():
            row[f"y{y}"] = v
        flat.append(row)
    pd.DataFrame(flat).to_csv(OUT / "c041_family_diag.csv", index=False)

    board = {
        "c": "C-041",
        "when": "2026-10-03 ~01:03 Europe/Amsterdam",
        "absorb": {
            "main": "cb1b8d1 tip (NEXT_STEPS v102 at b0b20ac — N134–N137 FAIL; OPEN N138/N139 stale vs Faraday; TRIAL 470; FREEZE OFF) + forward P1 daily",
            "faraday": "e1bf004 — N140 FAIL / N141 FAIL_CLONE; prior N138 FAIL_CLONE / N139 FAIL; OPEN N142 US30_US500_XS / N143 XLE→US500 (Manager v102 still had tip f5523fb / OPEN N138/N139)",
            "u2": "78775a2 IDLE/HOLD absorb v102; TRIAL 470; OPEN N138/N139 no PREREG (stale vs Faraday e1bf004)",
            "s2": "5a21939 cycle_0047 XLE_ENERGY_EQUITY_STRESS (Lane-A feed for N143)",
            "prior_cto": "659d6c6 C-040 N134/N135 DIAG_FAIL (0 CTO trials)",
        },
        "freeze": "OFF",
        "trial_count": 470,
        "trials_appended_by_cto": 0,
        "reserve_2025": "untouched",
        "track_3": "PAUSED",
        "live_prereg": None,
        "results": rows,
        "promote_to_prereg": [r["label"] for r in rows if r["verdict"] == "DIAG_PASS"],
        "kill_circuit_note": (
            "cost-PASS→FAIL_T streak N100+N101+N112+N114+N116+N118+N124+N125+N127+N128+N130+N131 (≥5); "
            "pivot ON; bar N75–N141 + XLF/QUAL/BRENT_WTI/USDMXN/GER40_UK/JP_HK/XAU_UKOIL/XAG_UKOIL + prior; "
            "N142/N143 = NEW_FAMILY BK/BL (US cash-index basis / XLE→US500 — not clones of dead ETF-stress or EU XS)"
        ),
    }
    (OUT / "c041_board.json").write_text(json.dumps(board, indent=2))
    lines = [
        "# C-041 — absorb main v102 + Faraday e1bf004 + Lane-B diag N142/N143 (0 CTO trials)",
        "",
        f"**When:** {board['when']}. **TRIAL_COUNT:** 470. **FREEZE:** OFF. **Track-3:** PAUSED. **Live PREREG:** none (pending diag).",
        "",
        "## Absorb",
        "",
        "- `origin/main` tip `cb1b8d1` (NEXT_STEPS **v102** @ `b0b20ac` ~00:44): N134–N137 FAIL; OPEN **N138/N139** (stale vs Faraday); TRIAL **470**; FREEZE **OFF**; C-040 absorbed.",
        "- Faraday `e1bf004` (~00:56): N140 FAIL / N141 FAIL_CLONE; prior N138 FAIL_CLONE / N139 FAIL; OPEN **N142 US30_US500_XS** / **N143 XLE→US500**; no PREREG.",
        "- U2 `78775a2` IDLE/HOLD absorb v102; TRIAL **470**.",
        "- S2 `5a21939` cycle_0047 XLE_ENERGY_EQUITY_STRESS — Lane-A feed for N143.",
        "- Prior CTO C-040 `659d6c6`. Absorbed Faraday N132–N141 FAIL chain. Reserve 2025+ untouched.",
        "",
        "## Lane-B diagnostic N142/N143 (train 2021–2023; ≤2024; 0 CTO trials)",
        "",
        "| Idee | mean_bp | n | gate | day_t | h1 | h2 | L/S | years | Verdict |",
        "|------|--------:|--:|-----:|------:|---:|---:|----:|-------|---------|",
    ]
    for r in rows:
        years = r.get("years") or {}
        ystr = "/".join(f"{y}:{years[y]}" for y in ("2021", "2022", "2023") if y in years)
        ls = f"{r.get('n_long')}/{r.get('n_short')}"
        lines.append(
            f"| {r['label']} | {r['mean_bp']} | {r['n']} | {r['gate_bp']} | {r['day_t']} | "
            f"{r['h1_mean_bp']} | {r['h2_mean_bp']} | {ls} | {ystr or '—'} | **{r['verdict']}** |"
        )
    lines += [
        "",
        "### Notes",
        "",
        "- N142: US30cash/US500cash ratio z40 thr1.5 basis fade (z>+1.5→SHORT US30+LONG US500; z<−1.5→LONG US30+SHORT US500) day t → both legs session-flat 15:30→21:00 CET day t+1; gate=3×(0.45+0.78)=3.69; ≠ N81/N138/N143/IDX_SHORT/N87.",
        "- N143: XLE level z40 thr1.0 fade_extreme (z>+1→SHORT; z<−1→LONG) day t → US500 session-flat 15:30→21:00 CET day t+1; gate=3×RT 0.78=2.34; S2 5a21939 cycle_0047; ≠ GAS/CRACK/N98/N134/N140/N142.",
        "- Also absorb Faraday N138 FAIL_CLONE / N139 FAIL / N140 FAIL / N141 FAIL_CLONE — no re-run.",
        "- DIAG_PASS → CTO freezes PREREG for U2; else drop / replace NEW_FAMILY (D-094).",
        "- No thr-grid / no overnight / no soft gate / no US100 remap / no XLE CFD / no GER/UK rewrite.",
        "- Kill: bar N75–N141 + prior; N142/N143 novelty BK/BL.",
        "",
        f"**Promote candidates (DIAG_PASS):** {board['promote_to_prereg'] or 'none'}.",
        "",
        "Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.",
        "",
    ]
    (OUT / "c041_report.md").write_text("\n".join(lines))
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
