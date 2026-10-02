#!/usr/bin/env python3
"""C-042 — absorb Faraday aca4d2f + retract N143 FAIL_CLONE + Lane-B diag N150/N151 (0 CTO trials).

Faraday tip aca4d2f (~01:23 CEST): N148/N149 FAIL; OPEN N150 XAG/US30 (BS) / N151 EURJPY/USDCHF (BT).
Prior Faraday: N142 FAIL / N143 FAIL_CLONE of DBC_z40_thr1.0 (93cb002) — CTO C-041 raced and
PREREGed N143 without clone gate → retract this cycle. N144–N147 FAIL/FAIL_CLONE absorbed.
U2 IDLE TRIAL 470. Diagnostic screens only until DIAG_PASS → PREREG freeze.
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
OUT = ROOT / "results/cto/c042_absorb_faraday_n150_n151"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
HARD_CUT = pd.Timestamp("2024-12-31")
RT_XAG = 5.07
RT_US30 = 0.45
RT_EURJPY = 1.10
RT_USDCHF = 1.01
GATE_150 = 3.0 * (RT_XAG + RT_US30)  # 16.56
GATE_151 = 3.0 * (RT_EURJPY + RT_USDCHF)  # 6.33
MIN_N = 150
THR = 1.5
ZWIN = 40


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


def diag_two_leg_xs(rel_a: str, rel_b: str, gate: float, label: str, notes: str):
    """Ratio A/B z40 thr±1.5 basis fade, both legs session-flat 15:30→21:00."""
    a = load_m5(rel_a)
    b = load_m5(rel_b)
    ca = daily_close_22(a)
    cb = daily_close_22(b)
    both = pd.concat([ca.rename("a"), cb.rename("b")], axis=1).dropna()
    ratio = (both["a"] / both["b"]).rename("ratio")
    z40 = zscore(ratio, ZWIN)
    pos = pd.Series(0.0, index=ratio.index)
    # z>+thr → SHORT A + LONG B; z<-thr → LONG A + SHORT B
    pos[z40 > THR] = -1.0
    pos[z40 < -THR] = 1.0
    ga = by_day(a)
    gb = by_day(b)
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
        gate,
        label,
        notes,
        years=years,
        n_long=n_long,
        n_short=n_short,
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [
        diag_two_leg_xs(
            "data/m5gz/XAGUSD.csv.gz",
            "data/m5gz/US30cash.csv.gz",
            GATE_150,
            "N150_XAG_US30_METAL_INDUSTRIAL_XS_SESSION",
            (
                f"NEW_FAMILY BS; XAG/US30 ratio z{ZWIN}/thr{THR} basis fade both legs "
                f"15:30→21:00; gate=3×(5.07+0.45)=16.56; ≠ N148/N149/N146/N141/N142/N75"
            ),
        ),
        diag_two_leg_xs(
            "data/m5gz/EURJPY.csv.gz",
            "data/m5gz/USDCHF.csv.gz",
            GATE_151,
            "N151_EURJPY_USDCHF_FUNDING_XS_SESSION",
            (
                f"NEW_FAMILY BT; EURJPY/USDCHF ratio z{ZWIN}/thr{THR} basis fade both legs "
                f"15:30→21:00; gate=3×(1.10+1.01)=6.33; ≠ N148/N149/L60/N28/N47/N150"
            ),
        ),
    ]
    flat = []
    for r in rows:
        row = {k: v for k, v in r.items() if k != "years"}
        for y, v in (r.get("years") or {}).items():
            row[f"y{y}"] = v
        flat.append(row)
    pd.DataFrame(flat).to_csv(OUT / "c042_family_diag.csv", index=False)

    board = {
        "c": "C-042",
        "when": "2026-10-03 ~01:30 Europe/Amsterdam",
        "absorb": {
            "main": "cb1b8d1 tip unchanged (NEXT_STEPS v102; TRIAL 470; FREEZE OFF)",
            "faraday": "aca4d2f — N148 FAIL / N149 FAIL; OPEN N150/N151; prior N142 FAIL / N143 FAIL_CLONE(DBC) / N144–N147 FAIL",
            "u2": "78775a2 IDLE/HOLD absorb v102; TRIAL 470; no N143 run yet",
            "prior_cto": "7041e8a C-041 N142 DIAG_FAIL / N143 DIAG_PASS→PREREG (retracted this cycle)",
        },
        "n143_correction": {
            "prior": "C-041 DIAG_PASS→PREREG",
            "faraday_authoritative": "93cb002 D-092.1 FAIL_CLONE of DBC_z40_thr1.0 — no PREREG",
            "action": "RETRACT PREREG_FTMO_N143 → STOP FAIL_CLONE; U2 do not run",
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
            "cost-PASS→FAIL_T streak N100…N131 (≥5); pivot ON; "
            "bar N75–N149 + XLE→US500(DBC clone)/US30_US500/XPT_XPD/BTC_ETH/AUD_XAU/GBP_UKOIL/USDJPY_US100/EUR_GER40 + prior; "
            "N150/N151 = NEW_FAMILY BS/BT"
        ),
    }
    (OUT / "c042_board.json").write_text(json.dumps(board, indent=2))
    lines = [
        "# C-042 — absorb Faraday aca4d2f + retract N143 FAIL_CLONE + Lane-B diag N150/N151 (0 CTO trials)",
        "",
        f"**When:** {board['when']}. **TRIAL_COUNT:** 470. **FREEZE:** OFF. **Track-3:** PAUSED. **Live PREREG:** none.",
        "",
        "## Absorb / correction",
        "",
        "- Faraday `aca4d2f` (~01:23): N148 USDJPY/US100 FAIL (+3.31 < 4.32) / N149 EUR/GER40 FAIL (+2.05 < 4.05, N=140); OPEN **N150 XAG/US30 BS** / **N151 EURJPY/USDCHF BT**.",
        "- Faraday `93cb002`: **N143 XLE FAIL_CLONE of DBC_z40_thr1.0** (mean +7.86 ≥ gate but clone) — overrides C-041 DIAG_PASS→PREREG → **retract**.",
        "- Absorbed N142 FAIL / N144–N147 FAIL/FAIL_CLONE (no re-run).",
        "- Main tip `cb1b8d1` v102 unchanged. U2 `78775a2` IDLE TRIAL **470**. Reserve 2025+ untouched.",
        "",
        "## Lane-B diagnostic N150/N151 (train 2021–2023; ≤2024; 0 CTO trials)",
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
        "- N150: XAGUSD/US30cash ratio z40 thr1.5 basis fade both legs 15:30→21:00; gate=3×(5.07+0.45)=16.56; NEW_FAMILY BS.",
        "- N151: EURJPY/USDCHF ratio z40 thr1.5 basis fade both legs 15:30→21:00; gate=3×(1.10+1.01)=6.33; NEW_FAMILY BT.",
        "- N143 retract: Faraday D-092.1 FAIL_CLONE (DBC) is binding; PREREG_FTMO_N143 → STOP; U2 must not run.",
        "- DIAG_PASS → CTO freezes PREREG for U2; else drop / Strateeg refill ≥2 NEW_FAMILY (D-094).",
        "- No thr-grid / no overnight / no soft gate / no single-leg remap.",
        "",
        f"**Promote candidates (DIAG_PASS):** {board['promote_to_prereg'] or 'none'}.",
        "",
        "Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.",
        "",
    ]
    (OUT / "c042_report.md").write_text("\n".join(lines))
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
