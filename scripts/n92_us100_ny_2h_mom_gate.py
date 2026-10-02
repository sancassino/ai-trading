#!/usr/bin/env python3
"""PREREG_FTMO_N92 — cost-gate + formal train/test (for Uitvoerder-2).

Frozen rule: PREREG_FTMO_N92.md (CTO C-031 / NEW_FAMILY Q).
US100cash NY 15:30–17:30 direction → hold to 22:00; intradag-flat.
Reserve 2025+ untouched. Do not retune windows/thresholds/symbols.
"""
from __future__ import annotations

import gzip
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n92_us100_ny_2h_mom"

RT_BP = 0.66
GATE_BP = 3.0 * RT_BP  # 1.98
STRESS_GATE_BP = 3.0 * RT_BP * 1.5  # 2.97
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
TEST_START = pd.Timestamp("2024-01-01")
TEST_END = pd.Timestamp("2024-12-31 23:59:59")


def load_m5() -> pd.DataFrame:
    with gzip.open(ROOT / "data/m5gz/US100cash.csv.gz", "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["open", "high", "low", "close"]).sort_values("time")
    return df[df["time"] <= TEST_END].reset_index(drop=True)


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


def nw_t(x: np.ndarray, lags: int = 5) -> float:
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    n = len(x)
    if n < 3:
        return float("nan")
    mean = float(x.mean())
    xc = x - mean
    gamma0 = float(np.dot(xc, xc) / n)
    if gamma0 <= 0:
        return float("nan")
    var = gamma0
    for L in range(1, min(lags, n - 1) + 1):
        w = 1.0 - L / (lags + 1.0)
        cov = float(np.dot(xc[L:], xc[:-L]) / n)
        var += 2.0 * w * cov
    se = math.sqrt(max(var, 0.0) / n)
    return mean / se if se > 0 else float("nan")


def simulate(m5: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    sub = m5[(m5["time"] >= start) & (m5["time"] <= end)].copy()
    sub["day"] = sub["time"].dt.normalize()
    rows = []
    for day, g in sub.groupby("day"):
        b0 = first_bar_in(g, day, 15, 30, 15)
        b1 = first_bar_in(g, day, 17, 30, 15)
        if b0 is None or b1 is None:
            continue
        p0, p1 = float(b0["close"]), float(b1["close"])
        if p0 <= 0:
            continue
        ret2h = p1 / p0 - 1.0
        if ret2h == 0 or not np.isfinite(ret2h):
            continue
        side = 1 if ret2h > 0 else -1
        exb = last_bar_le(g, day, 22, 0)
        if exb is None or exb["time"] <= b1["time"]:
            continue
        exit_px = float(exb["close"])
        hold = g[(g["time"] >= b1["time"]) & (g["time"] <= exb["time"])]
        # adverse excursion in bp vs entry (for lat-B intradag-DD)
        if side > 0:
            trough = float(hold["low"].min()) if len(hold) else exit_px
            mae_bp = 1e4 * (p1 - trough) / p1
        else:
            peak = float(hold["high"].max()) if len(hold) else exit_px
            mae_bp = 1e4 * (peak - p1) / p1
        bruto = side * 1e4 * (exit_px - p1) / p1
        netto = bruto - RT_BP
        rows.append(
            {
                "day": day,
                "side": side,
                "bruto_bp": bruto,
                "netto_bp": netto,
                "mae_bp": max(0.0, mae_bp),
            }
        )
    return pd.DataFrame(rows)


def summarize(df: pd.DataFrame, label: str) -> dict:
    if df.empty:
        return {"label": label, "n": 0, "mean_bruto": None, "mean_netto": None,
                "t_netto": None, "t_nw5": None, "verdict_hint": "EMPTY"}
    b = df["bruto_bp"].to_numpy(float)
    n_ = df["netto_bp"].to_numpy(float)
    n = len(b)
    mean_b = float(b.mean())
    mean_n = float(n_.mean())
    if n >= 2 and n_.std(ddof=1) > 0:
        t = mean_n / (n_.std(ddof=1) / math.sqrt(n))
    else:
        t = float("nan")
    t_nw = nw_t(n_)
    return {
        "label": label,
        "n": n,
        "mean_bruto": round(mean_b, 4),
        "mean_netto": round(mean_n, 4),
        "t_netto": round(t, 4) if np.isfinite(t) else None,
        "t_nw5": round(t_nw, 4) if np.isfinite(t_nw) else None,
        "median_bruto": round(float(np.median(b)), 4),
        "mean_mae_bp": round(float(df["mae_bp"].mean()), 4),
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    m5 = load_m5()
    train = simulate(m5, TRAIN_START, TRAIN_END)
    test = simulate(m5, TEST_START, TEST_END)
    train.to_csv(OUT / "train_trades.csv", index=False)
    test.to_csv(OUT / "test_trades.csv", index=False)
    st = summarize(train, "train_2021_2023")
    te = summarize(test, "test_2024")

    cost_pass = st["n"] >= 150 and st["mean_bruto"] is not None and st["mean_bruto"] >= GATE_BP
    stress_pass = st["mean_bruto"] is not None and st["mean_bruto"] >= STRESS_GATE_BP
    if not cost_pass:
        verdict = "FAIL_COST_GATE"
    elif not stress_pass:
        verdict = "FAIL_STRESS"
    else:
        # formal: both windows t_NW>=2 and mean_netto>0
        ok_tr = (
            st["t_nw5"] is not None and st["t_nw5"] >= 2.0 and st["mean_netto"] is not None and st["mean_netto"] > 0
        )
        ok_te = (
            te["n"] >= 1
            and te["t_nw5"] is not None
            and te["t_nw5"] >= 2.0
            and te["mean_netto"] is not None
            and te["mean_netto"] > 0
        )
        verdict = "PASS" if (ok_tr and ok_te) else "FAIL_T"

    board = {
        "prereg": "PREREG_FTMO_N92",
        "rt_bp": RT_BP,
        "gate_bp": GATE_BP,
        "stress_gate_bp": STRESS_GATE_BP,
        "train": st,
        "test": te,
        "cost_pass": cost_pass,
        "stress_pass": stress_pass,
        "verdict": verdict,
        "reserve_2025": "untouched",
        "note": "U2 owns TRIALS/TRIAL_COUNT append. CTO C-031 frozen this script; do not retune.",
    }
    (OUT / "n92_gate_board.json").write_text(json.dumps(board, indent=2))
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
