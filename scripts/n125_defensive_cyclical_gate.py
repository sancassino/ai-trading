#!/usr/bin/env python3
"""PREREG_FTMO_N125 — cost-gate + formal train/test (for Uitvoerder-2).

Frozen rule: PREREG_FTMO_N125_DEFENSIVE_CYCLICAL.md (NEW_FAMILY DEFENSIVE_CYCLICAL).
XLU/XLI z40/thr0.5 defensive_high → US500cash session-flat 15:30→21:00 CET. Swap=0.
≠ SECTOR_DISP. Prefer US500 twin. Reserve 2025+ untouched. No retune.
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
OUT = ROOT / "results/R2/n125_defensive_cyclical"
DAILY = ROOT / "data/daily"

RT_BP = 0.78
GATE_BP = 3.0 * RT_BP  # 2.34
STRESS_GATE_BP = 3.0 * RT_BP * 1.5  # 3.51
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
TEST_START = pd.Timestamp("2024-01-01")
TEST_END = pd.Timestamp("2024-12-31 23:59:59")
CAL_END = pd.Timestamp("2024-12-31")
Z_WIN = 40
Z_THR = 0.5


def load_close(sym: str) -> pd.Series:
    path = DAILY / f"{sym}.csv"
    raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    body = [ln for ln in raw if not ln.startswith("#")]
    sep = ";" if body and ";" in body[0] else ","
    df = pd.read_csv(io.StringIO("\n".join(body)), sep=sep)
    cols_l = {c.lower().replace(" ", ""): c for c in df.columns}
    dc = cols_l.get("date") or cols_l.get("observation_date")
    cc = cols_l.get("adjclose") or cols_l.get("close") or df.columns[-1]
    s = pd.Series(
        pd.to_numeric(df[cc], errors="coerce").values,
        index=pd.to_datetime(df[dc].astype(str).str.replace(".", "-", regex=False)),
        name=sym,
    )
    s = s[~s.index.duplicated(keep="last")].sort_index()
    return s[s.index <= CAL_END].dropna()


def zscore(s: pd.Series, win: int) -> pd.Series:
    mu = s.rolling(win, min_periods=max(20, win // 3)).mean()
    sd = s.rolling(win, min_periods=max(20, win // 3)).std(ddof=0)
    return (s - mu) / sd.replace(0, np.nan)


def build_signal() -> pd.Series:
    xlu = load_close("XLU")
    xli = load_close("XLI")
    rel = (xlu / xli).dropna()
    z = zscore(rel, Z_WIN)
    pos = pd.Series(0.0, index=rel.index, dtype=float)
    pos[z > Z_THR] = -1.0
    pos[z < -Z_THR] = 1.0
    return pos.rename("pos")


def load_m5() -> pd.DataFrame:
    with gzip.open(ROOT / "data/m5gz/US500cash.csv.gz", "rt") as f:
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


def simulate(m5: pd.DataFrame, signal: pd.Series, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    sub = m5[(m5["time"] >= start) & (m5["time"] <= end)].copy()
    sub["day"] = sub["time"].dt.normalize()
    sig = signal.copy()
    sig.index = pd.to_datetime(sig.index).normalize()
    sig = sig[~sig.index.duplicated(keep="last")].sort_index()
    rows = []
    for day in sorted(sub["day"].unique()):
        prior = sig[sig.index < day]
        if prior.empty:
            continue
        side = float(prior.iloc[-1])
        if side == 0.0 or not np.isfinite(side):
            continue
        g = sub[sub["day"] == day]
        b_entry = first_bar_in(g, day, 15, 30, 15)
        b_exit = last_bar_le(g, day, 21, 0)
        if b_entry is None or b_exit is None or b_exit["time"] <= b_entry["time"]:
            continue
        p0 = float(b_entry["close"])
        p1 = float(b_exit["close"])
        if p0 <= 0:
            continue
        hold = g[(g["time"] >= b_entry["time"]) & (g["time"] <= b_exit["time"])]
        if side > 0:
            trough = float(hold["low"].min()) if len(hold) else p1
            mae_bp = 1e4 * (p0 - trough) / p0
        else:
            peak = float(hold["high"].max()) if len(hold) else p1
            mae_bp = 1e4 * (peak - p0) / p0
        bruto = side * 1e4 * (p1 / p0 - 1.0)
        rows.append(
            {
                "day": day,
                "signal_day": prior.index[-1],
                "side": int(side),
                "bruto_bp": bruto,
                "netto_bp": bruto - RT_BP,
                "mae_bp": max(0.0, mae_bp),
                "entry": p0,
                "exit": p1,
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
    t = mean_n / (n_.std(ddof=1) / math.sqrt(n)) if n >= 2 and n_.std(ddof=1) > 0 else float("nan")
    t_nw = nw_t(n_)
    return {
        "label": label, "n": n,
        "mean_bruto": round(mean_b, 4), "mean_netto": round(mean_n, 4),
        "t_netto": round(t, 4) if np.isfinite(t) else None,
        "t_nw5": round(t_nw, 4) if np.isfinite(t_nw) else None,
        "median_bruto": round(float(np.median(b)), 4),
        "mean_mae_bp": round(float(df["mae_bp"].mean()), 4),
        "n_long": int((df["side"] > 0).sum()), "n_short": int((df["side"] < 0).sum()),
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    signal = build_signal()
    sig_train = signal[(signal.index >= TRAIN_START) & (signal.index <= TRAIN_END)]
    n_sig = int((sig_train != 0).sum())
    m5 = load_m5()
    train = simulate(m5, signal, TRAIN_START, TRAIN_END)
    test = simulate(m5, signal, TEST_START, TEST_END)
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
        ok_tr = (st["t_nw5"] is not None and st["t_nw5"] >= 2.0
                 and st["mean_netto"] is not None and st["mean_netto"] > 0
                 and st["t_netto"] is not None and st["t_netto"] >= 2.0)
        ok_te = (te["n"] >= 1 and te["t_nw5"] is not None and te["t_nw5"] >= 2.0
                 and te["mean_netto"] is not None and te["mean_netto"] > 0
                 and te["t_netto"] is not None and te["t_netto"] >= 2.0)
        verdict = "PASS" if (ok_tr and ok_te) else "FAIL_T"
    board = {
        "prereg": "PREREG_FTMO_N125_DEFENSIVE_CYCLICAL",
        "new_family": "DEFENSIVE_CYCLICAL",
        "config": "XLU/XLI z40/thr0.5 defensive_high → US500cash session-flat 15:30→21:00 CET",
        "rt_bp": RT_BP, "gate_bp": GATE_BP, "stress_gate_bp": STRESS_GATE_BP, "swap_bp": 0.0,
        "n_signal_days_train_nonzero": n_sig, "train": st, "test": te,
        "cost_pass": cost_pass, "stress_pass": stress_pass, "verdict": verdict,
        "reserve_2025": "untouched", "s2_tip_sha": "13fe10c", "cto_c": "C-039",
        "diag": "mean+5.479 n=478 DIAG_PASS",
        "note": "U2 owns TRIALS/TRIAL_COUNT append. FAIL_COST_GATE/FAIL_STRESS → no bump. FAIL_T → bump +1. No retune. Prefer US500 twin.",
    }
    (OUT / "n125_gate_board.json").write_text(json.dumps(board, indent=2))
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
