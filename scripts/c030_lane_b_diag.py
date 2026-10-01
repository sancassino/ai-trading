#!/usr/bin/env python3
"""C-030 — N80 absorb + Lane-B diagnostics N82–N86 (0 trials).

Diagnostic / D-092.1-style screens only. Not formal gates.
Reserve 2025+ untouched. DXYcash M5 starts 2024-11 → N83 uses Yahoo DXY daily proxy.
"""
from __future__ import annotations

import gzip
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/cto/c030_n80_absorb_n82_n86"
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
    return df[(df["time"] >= TRAIN_START) & (df["time"] <= TRAIN_END)].reset_index(
        drop=True
    )


def mid_bar(row) -> float:
    m = 0.5 * (float(row["high"]) + float(row["low"]))
    return m if m > 0 else float(row["close"])


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
    if n >= 150 and mean >= gate_bp:
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


def diag_n82():
    """XAG London AM-Fix Fade EOD-flat. Gate 15.21."""
    m5 = load_m5("data/m5gz/XAGUSD.csv.gz")
    m5["day"] = m5["time"].dt.normalize()
    pnls = []
    for day, g in m5.groupby("day"):
        b0 = first_bar_in(g, day, 8, 0, 15)
        b1 = first_bar_in(g, day, 10, 30, 15)
        if b0 is None or b1 is None:
            continue
        p0 = mid_bar(b0)
        if p0 <= 0:
            continue
        ext = 1e4 * (mid_bar(b1) / p0 - 1.0)
        if abs(ext) < 35:
            continue
        side = -1 if ext >= 35 else 1
        entry = float(b1["close"])
        exb = last_bar_le(g, day, 13, 0)
        if exb is None or exb["time"] <= b1["time"]:
            continue
        exit_px = float(exb["close"])
        pnls.append(side * 1e4 * (exit_px - entry) / entry)
    return trade_stats(pnls, 15.21, "N82_XAG_AM_FIX_FADE", "EOD-flat; RT gate 15.21")


def diag_n83():
    """DXY overnight → US100 opposite intradag. Gate 1.98.
    DXYcash M5 starts 2024-11 → use Yahoo daily/DXY.csv open/prior-close as gap proxy.
    """
    dxy = pd.read_csv(ROOT / "data/daily/DXY.csv", sep=";", comment="#")
    dxy["date"] = pd.to_datetime(dxy["date"])
    dxy = dxy.sort_values("date")
    dxy = dxy[(dxy["date"] >= TRAIN_START) & (dxy["date"] <= HARD_CUT)].reset_index(
        drop=True
    )
    dxy["gap_bp"] = 1e4 * (dxy["open"] / dxy["close"].shift(1) - 1.0)

    us = load_m5("data/m5gz/US100cash.csv.gz")
    us["day"] = us["time"].dt.normalize()
    by_day = {d: g for d, g in us.groupby("day")}
    pnls = []
    for _, row in dxy.iterrows():
        day = pd.Timestamp(row["date"]).normalize()
        if day < TRAIN_START or day > TRAIN_END.normalize():
            continue
        gap = row["gap_bp"]
        if not np.isfinite(gap) or abs(gap) < 15:
            continue
        g = by_day.get(day)
        if g is None:
            continue
        side = -1 if gap >= 15 else 1  # opposite US100
        ent = first_bar_in(g, day, 15, 30, 15)
        if ent is None:
            continue
        entry = float(ent["close"])
        exb = last_bar_le(g, day, 17, 30)
        if exb is None or exb["time"] <= ent["time"]:
            continue
        exit_px = float(exb["close"])
        pnls.append(side * 1e4 * (exit_px - entry) / entry)
    return trade_stats(
        pnls,
        1.98,
        "N83_DXY_OVN_US100_OPP",
        "signal=Yahoo DXY daily open/prior-close (DXYcash M5 from 2024-11 only)",
    )


def diag_n84():
    """AUDNZD rate-diff stretch fade EOD-flat. Gate 3.18 (est RT)."""
    m5 = load_m5("data/m5gz/AUDNZD.csv.gz")
    m5["day"] = m5["time"].dt.normalize()
    close_map = {}
    for day, g in m5.groupby("day"):
        ref = last_bar_le(g, day, 22, 0)
        if ref is not None:
            close_map[day] = float(ref["close"])
    days = sorted(close_map)
    closes = pd.Series({d: close_map[d] for d in days}).sort_index()
    ma20 = closes.rolling(20, min_periods=20).mean()
    by_day = {d: g for d, g in m5.groupby("day")}
    pnls = []
    for i, day in enumerate(days):
        if i < 20:
            continue
        if day < TRAIN_START or day > TRAIN_END.normalize():
            continue
        m = ma20.loc[day]
        if not np.isfinite(m) or m <= 0:
            continue
        g = by_day.get(day)
        if g is None:
            continue
        b0 = first_bar_in(g, day, 8, 0, 15)
        if b0 is None:
            continue
        stretch = 1e4 * (mid_bar(b0) / float(m) - 1.0)
        if abs(stretch) < 40:
            continue
        side = -1 if stretch >= 40 else 1
        entry = float(b0["close"])
        exb = last_bar_le(g, day, 16, 0)
        if exb is None or exb["time"] <= b0["time"]:
            continue
        exit_px = float(exb["close"])
        pnls.append(side * 1e4 * (exit_px - entry) / entry)
    return trade_stats(
        pnls, 3.18, "N84_AUDNZD_STRETCH_FADE", "RT est; not yet in COSTS_FTMO"
    )


def diag_n85():
    """US500 AM lead → US100 same-dir PM lag. Gate 1.98."""
    es = load_m5("data/m5gz/US500cash.csv.gz")
    nq = load_m5("data/m5gz/US100cash.csv.gz")
    es["day"] = es["time"].dt.normalize()
    nq["day"] = nq["time"].dt.normalize()
    es_close = {}
    for day, g in es.groupby("day"):
        ref = last_bar_le(g, day, 22, 0)
        if ref is not None:
            es_close[day] = float(ref["close"])
    es_by = {d: g for d, g in es.groupby("day")}
    nq_by = {d: g for d, g in nq.groupby("day")}
    days = sorted(set(es_by) & set(nq_by) & set(es_close))
    pnls = []
    for i, day in enumerate(days):
        if i == 0:
            continue
        prev = days[i - 1]
        cref = es_close.get(prev)
        if not cref or cref <= 0:
            continue
        ges = es_by[day]
        lead_bar = first_bar_in(ges, day, 15, 35, 15)
        if lead_bar is None:
            continue
        lead = 1e4 * (mid_bar(lead_bar) / cref - 1.0)
        if abs(lead) < 25:
            continue
        side = 1 if lead >= 25 else -1
        gnq = nq_by[day]
        ent = first_bar_in(gnq, day, 17, 0, 15)
        if ent is None:
            continue
        entry = float(ent["close"])
        exb = last_bar_le(gnq, day, 21, 0)
        if exb is None or exb["time"] <= ent["time"]:
            continue
        exit_px = float(exb["close"])
        pnls.append(side * 1e4 * (exit_px - entry) / entry)
    return trade_stats(pnls, 1.98, "N85_US500_LEAD_US100_LAG", "single-leg US100; no ratio")


def diag_n86():
    """XAU own RV-VoV → 3d MR. Gate 15.39 (worst-case long swap in gate)."""
    with gzip.open(ROOT / "data/m5gz/XAUUSD.csv.gz", "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df = df.dropna(subset=["close"]).sort_values("time")
    df = df[df["time"] <= HARD_CUT]
    df["day"] = df["time"].dt.normalize()
    # day close ≤22:00 CET proxy = last bar of day
    closes = df.groupby("day")["close"].last().sort_index()
    closes = closes[(closes.index >= pd.Timestamp("2020-01-01"))]
    r = np.log(closes / closes.shift(1))
    rv10 = np.sqrt((r**2).rolling(10, min_periods=10).sum())
    vov10 = rv10.rolling(10, min_periods=10).std()
    med60 = vov10.shift(1).rolling(60, min_periods=60).median()
    move3 = r.rolling(3, min_periods=3).sum()

    pnls = []
    dates = list(closes.index)
    i = 0
    while i < len(dates) - 4:
        d = dates[i]
        if d < TRAIN_START or d > TRAIN_END.normalize():
            i += 1
            continue
        vov, med, m3 = vov10.loc[d], med60.loc[d], move3.loc[d]
        if not (np.isfinite(vov) and np.isfinite(med) and np.isfinite(m3)):
            i += 1
            continue
        if not (vov > med and abs(m3) >= 0.008):
            i += 1
            continue
        # entry next close, exit t+3
        e_i, x_i = i + 1, i + 3
        if x_i >= len(dates):
            break
        # keep exit in train for fair screen
        if dates[x_i] > TRAIN_END.normalize():
            break
        side = -1 if m3 > 0 else 1
        e_px, x_px = float(closes.iloc[e_i]), float(closes.iloc[x_i])
        pnls.append(side * 1e4 * (x_px - e_px) / e_px)
        i = x_i  # non-overlap
    return trade_stats(
        pnls, 15.39, "N86_XAU_OWN_VOV_MR_3D", "≠ N78 VIX_TERM; own-asset VoV→XAU MR"
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [
        diag_n82(),
        diag_n83(),
        diag_n84(),
        diag_n85(),
        diag_n86(),
    ]
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "c030_family_diag.csv", index=False)
    board = {
        "c": "C-030",
        "when": "2026-10-01 ~13:35 Europe/Amsterdam",
        "absorb": {
            "N80": "FAIL_COST_GATE U2 454628f; counts_as_trial=false; TRIAL_COUNT 456; bar UKOIL OVN-gap clones",
            "N78": "already C-029 barred VIX_TERM",
        },
        "freeze": "OFF",
        "trial_count": 456,
        "trials_appended_by_cto": 0,
        "reserve_2025": "untouched",
        "results": rows,
        "promote_to_prereg": [
            r["label"] for r in rows if r["verdict"] == "DIAG_PASS"
        ],
    }
    (OUT / "c030_board.json").write_text(json.dumps(board, indent=2))
    lines = [
        "# C-030 — N80 absorb + Lane-B diag N82–N86 (0 trials)",
        "",
        f"**When:** {board['when']}. **TRIAL_COUNT:** 456. **FREEZE:** OFF.",
        "",
        "## Absorb",
        "",
        "- U2 `454628f` **N80** UKOIL OVN-gap cont → **FAIL_COST_GATE** (mean +7.56 < 8.13 with stop; geen trial).",
        "- Dead += N80. **Bar** UKOIL overnight-gap continuation / softer-gate / USOIL twin clones.",
        "- Faraday `6c9c1e5` filed NEW_FAMILY **N84–N86**; N82/N83 remain OPEN on main v81.",
        "",
        "## Lane-B diagnostic (train 2021–2023; ≤2024; 0 trials)",
        "",
        "| Idee | mean_bp | n | gate | day_t | Verdict |",
        "|------|--------:|--:|-----:|------:|---------|",
    ]
    for r in rows:
        lines.append(
            f"| {r['label']} | {r['mean_bp']} | {r['n']} | {r['gate_bp']} | {r['day_t']} | **{r['verdict']}** |"
        )
    lines += [
        "",
        "### Notes",
        "",
        "- N83: DXYcash M5 only from 2024-11 → Yahoo `data/daily/DXY.csv` open/prior-close used as overnight gap proxy (diagnostic honesty).",
        "- N84: AUDNZD RT est (not in COSTS_FTMO) — any DIAG_PASS still needs U2 RT land before PREREG.",
        "- N86: own-asset XAU VoV ≠ VIX_TERM (C-029 bar still holds for VIX→equity).",
        "",
        f"**Promote / freeze PREREG:** {board['promote_to_prereg'] or 'none'}.",
        "",
        "Reserve 2025+ untouched. No purchases / no FTMO signup.",
        "",
    ]
    (OUT / "c030_report.md").write_text("\n".join(lines))
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
