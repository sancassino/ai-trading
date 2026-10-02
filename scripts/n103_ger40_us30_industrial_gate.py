#!/usr/bin/env python3
"""PREREG_FTMO_N103 — cost-gate + formal train/test (for Uitvoerder-2).

Frozen rule: PREREG_FTMO_N103_GER40_US30_INDUSTRIAL.md (NEW_FAMILY Z).
GER40 Lon-AM impulse (|ger_am|≥40) → same-dir US30cash session-flat
15:30→21:00 CET. Swap=0. Reserve 2025+ untouched. No retune.
"""
from __future__ import annotations

import gzip
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n103_ger40_us30_industrial"

RT_BP = 0.45  # US30cash intradag RT
GATE_BP = 3.0 * RT_BP  # 1.35
STRESS_GATE_BP = 3.0 * RT_BP * 1.5  # 2.025
GER_AM_THR = 40.0  # |ger_am_bp| ≥ 40
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
TEST_START = pd.Timestamp("2024-01-01")
TEST_END = pd.Timestamp("2024-12-31 23:59:59")


def load_m5(sym: str) -> pd.DataFrame:
    with gzip.open(ROOT / "data/m5gz" / f"{sym}.csv.gz", "rt") as f:
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


def simulate(
    ger: pd.DataFrame, us30: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp
) -> pd.DataFrame:
    """GER Lon-AM impulse → US30 NY same-dir session-flat (≤1 trade/day)."""
    g_sub = ger[(ger["time"] >= start) & (ger["time"] <= end)].copy()
    u_sub = us30[(us30["time"] >= start) & (us30["time"] <= end)].copy()
    g_sub["day"] = g_sub["time"].dt.normalize()
    u_sub["day"] = u_sub["time"].dt.normalize()
    days = sorted(set(g_sub["day"]).intersection(set(u_sub["day"])))
    rows = []
    for day in days:
        g = g_sub[g_sub["day"] == day]
        u = u_sub[u_sub["day"] == day]
        if g.empty or u.empty:
            continue
        b08 = first_bar_in(g, day, 8, 0, 15)
        b12 = first_bar_in(g, day, 12, 0, 15)
        if b08 is None or b12 is None:
            continue
        c08 = float(b08["close"])
        c12 = float(b12["close"])
        if c08 <= 0:
            continue
        ger_am_bp = 1e4 * (c12 / c08 - 1.0)
        if abs(ger_am_bp) < GER_AM_THR:
            continue
        side = 1 if ger_am_bp >= GER_AM_THR else -1
        b_entry = first_bar_in(u, day, 15, 30, 15)
        b_exit = last_bar_le(u, day, 21, 0)
        if b_entry is None or b_exit is None:
            continue
        if b_exit["time"] <= b_entry["time"]:
            continue
        p0 = float(b_entry["close"])
        p1 = float(b_exit["close"])
        if p0 <= 0:
            continue
        hold = u[(u["time"] >= b_entry["time"]) & (u["time"] <= b_exit["time"])]
        if side > 0:
            trough = float(hold["low"].min()) if len(hold) else p1
            mae_bp = 1e4 * (p0 - trough) / p0
        else:
            peak = float(hold["high"].max()) if len(hold) else p1
            mae_bp = 1e4 * (peak - p0) / p0
        bruto = side * 1e4 * (p1 / p0 - 1.0)
        netto = bruto - RT_BP
        rows.append(
            {
                "day": day,
                "side": int(side),
                "ger_am_bp": ger_am_bp,
                "bruto_bp": bruto,
                "netto_bp": netto,
                "mae_bp": max(0.0, mae_bp),
                "entry": p0,
                "exit": p1,
            }
        )
    return pd.DataFrame(rows)


def year_split(df: pd.DataFrame) -> dict:
    if df.empty:
        return {}
    out = {}
    years = sorted({int(pd.Timestamp(d).year) for d in df["day"]})
    for y in years:
        sub = df[df["day"].map(lambda d: int(pd.Timestamp(d).year) == y)]
        if len(sub) == 0:
            continue
        out[str(y)] = {
            "n": int(len(sub)),
            "mean_bruto": round(float(sub["bruto_bp"].mean()), 4),
        }
    return out


def summarize(df: pd.DataFrame, label: str) -> dict:
    if df.empty:
        return {
            "label": label,
            "n": 0,
            "mean_bruto": None,
            "mean_netto": None,
            "t_netto": None,
            "t_nw5": None,
            "verdict_hint": "EMPTY",
            "years": {},
        }
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
        "n_long": int((df["side"] > 0).sum()),
        "n_short": int((df["side"] < 0).sum()),
        "hit_rate": round(float((b > 0).mean()), 4),
        "years": year_split(df),
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ger = load_m5("GER40cash")
    us30 = load_m5("US30cash")
    train = simulate(ger, us30, TRAIN_START, TRAIN_END)
    test = simulate(ger, us30, TEST_START, TEST_END)
    train.to_csv(OUT / "train_trades.csv", index=False)
    test.to_csv(OUT / "test_trades.csv", index=False)
    st = summarize(train, "train_2021_2023")
    te = summarize(test, "test_2024")

    cost_pass = st["n"] >= 150 and st["mean_bruto"] is not None and st["mean_bruto"] >= GATE_BP
    stress_pass = st["mean_bruto"] is not None and st["mean_bruto"] >= STRESS_GATE_BP
    if not cost_pass:
        verdict = "FAIL_COST_GATE"
        counts = False
    elif not stress_pass:
        verdict = "FAIL_STRESS"
        counts = False
    else:
        ok_tr = (
            st["t_nw5"] is not None
            and st["t_nw5"] >= 2.0
            and st["mean_netto"] is not None
            and st["mean_netto"] > 0
            and st["t_netto"] is not None
            and st["t_netto"] >= 2.0
        )
        ok_te = (
            te["n"] >= 1
            and te["t_nw5"] is not None
            and te["t_nw5"] >= 2.0
            and te["mean_netto"] is not None
            and te["mean_netto"] > 0
            and te["t_netto"] is not None
            and te["t_netto"] >= 2.0
        )
        verdict = "PASS" if (ok_tr and ok_te) else "FAIL_T"
        counts = True  # cost+stress PASS → formal t counts (N100/N101/N92)

    if verdict == "FAIL_COST_GATE":
        note = (
            "FAIL_COST_GATE → counts_as_trial=false (N78/N93). "
            "No thr-grid / no US100 substitute / no GER→US-open rewrite / no overnight. "
            "Dead += N103_GER40_US30_INDUSTRIAL. Reserve 2025 untouched."
        )
    elif verdict == "FAIL_STRESS":
        note = (
            "Cost PASS but stress FAIL (mean < 2.025). "
            "counts_as_trial=false (no formal t). No thr-grid / year-split reported. "
            "Dead += N103_GER40_US30_INDUSTRIAL. Reserve 2025 untouched."
        )
    elif verdict == "FAIL_T":
        note = (
            "FAIL_T after cost+stress PASS → counts_as_trial=true (N100/N101/N92). "
            "No retune. Dead += N103_GER40_US30_INDUSTRIAL. Reserve 2025 untouched."
        )
    else:
        note = "PASS. U2 owns TRIALS/TRIAL_COUNT append. Reserve 2025 untouched."

    board = {
        "prereg": "PREREG_FTMO_N103_GER40_US30_INDUSTRIAL",
        "new_family": "Z",
        "config": (
            "GER40 Lon-AM |ger_am|≥40 → same-dir US30cash session-flat "
            "15:30→21:00 CET; swap=0"
        ),
        "signal": "GER40cash",
        "instrument": "US30cash",
        "rt_bp": RT_BP,
        "gate_bp": GATE_BP,
        "stress_gate_bp": STRESS_GATE_BP,
        "swap_bp": 0.0,
        "ger_am_thr_bp": GER_AM_THR,
        "faraday_tip_sha": "7059c63eb39ac93a35fc29b64821cf16a745da03",
        "train": st,
        "test": te,
        "cost_pass": cost_pass,
        "stress_pass": stress_pass,
        "verdict": verdict,
        "counts_as_trial": counts,
        "reserve_2025": "untouched",
        "dead_label": "N103_GER40_US30_INDUSTRIAL",
        "note": note,
    }
    (OUT / "n103_gate_board.json").write_text(json.dumps(board, indent=2))
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
