#!/usr/bin/env python3
"""PREREG_FTMO_N93 — cost-gate + formal train/test (for Uitvoerder-2).

Frozen rule: PREREG_FTMO_N93_SECTOR_DISP_ROTATION.md (NEW_FAMILY R).
XL* sector dispersion (lb=10 / disp_fade thr +1.0/−0.5) → US100cash
session-flat 15:30→21:00 CET. Swap=0. Reserve 2025+ untouched. No retune.
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
OUT = ROOT / "results/R2/n93_sector_disp_rotation"
DAILY = ROOT / "data/daily"

RT_BP = 0.66
GATE_BP = 3.0 * RT_BP  # 1.98
STRESS_GATE_BP = 3.0 * RT_BP * 1.5  # 2.97
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
TEST_START = pd.Timestamp("2024-01-01")
TEST_END = pd.Timestamp("2024-12-31 23:59:59")
CAL_END = pd.Timestamp("2024-12-31")  # reserve 2025+ untouched
SECTORS = ["XLB", "XLE", "XLF", "XLI", "XLK", "XLP", "XLU", "XLV", "XLY"]
LB = 10
DISP_Z_SHORT = 1.0  # disp_z > +1.0 → SHORT
DISP_Z_LONG = -0.5  # disp_z < −0.5 → LONG
Z_WIN = 252


def load_close(path: Path) -> pd.Series:
    raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    body = [ln for ln in raw if not ln.startswith("#")]
    sep = ";" if body and ";" in body[0] else ","
    df = pd.read_csv(io.StringIO("\n".join(body)), sep=sep)
    cols_l = {c.lower().replace(" ", ""): c for c in df.columns}
    dc = cols_l.get("date") or cols_l.get("observation_date")
    for cand in ("adjclose", "close"):
        if cand in cols_l:
            cc = cols_l[cand]
            break
    else:
        cc = df.columns[-1]
    s = pd.Series(
        pd.to_numeric(df[cc], errors="coerce").values,
        index=pd.to_datetime(df[dc].astype(str).str.replace(".", "-", regex=False)),
        name=path.stem,
    )
    s = s[~s.index.duplicated(keep="last")].sort_index()
    s = s[s.index <= CAL_END].dropna()
    return s


def zscore(s: pd.Series, win: int) -> pd.Series:
    mu = s.rolling(win, min_periods=max(20, win // 3)).mean()
    sd = s.rolling(win, min_periods=max(20, win // 3)).std(ddof=0)
    return (s - mu) / sd.replace(0, np.nan)


def build_signal() -> pd.Series:
    """disp_z on day t → position for next session (t+1). Index = signal day t."""
    closes = {s: load_close(DAILY / f"{s}.csv") for s in SECTORS}
    px = pd.DataFrame(closes).dropna(how="any")
    rets = px.pct_change(LB)
    disp = rets.std(axis=1).replace(0, np.nan)
    disp_z = zscore(disp, Z_WIN)
    pos = pd.Series(0.0, index=disp_z.index, dtype=float)
    pos[disp_z > DISP_Z_SHORT] = -1.0
    pos[disp_z < DISP_Z_LONG] = 1.0
    return pos.rename("pos")


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


def simulate(m5: pd.DataFrame, signal: pd.Series, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    """Signal on day t (normalized) → trade on next calendar M5 day with bars."""
    sub = m5[(m5["time"] >= start) & (m5["time"] <= end)].copy()
    sub["day"] = sub["time"].dt.normalize()
    # map signal day → next trade day: for each M5 day D, use signal from prior signal index ≤ D-1
    sig = signal.copy()
    sig.index = pd.to_datetime(sig.index).normalize()
    sig = sig[~sig.index.duplicated(keep="last")].sort_index()

    rows = []
    days = sorted(sub["day"].unique())
    for day in days:
        # prior signal day: last XL close date strictly before this M5 day
        prior = sig[sig.index < day]
        if prior.empty:
            continue
        side = float(prior.iloc[-1])
        if side == 0.0 or not np.isfinite(side):
            continue
        g = sub[sub["day"] == day]
        b_entry = first_bar_in(g, day, 15, 30, 15)
        b_exit = last_bar_le(g, day, 21, 0)
        if b_entry is None or b_exit is None:
            continue
        if b_exit["time"] <= b_entry["time"]:
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
        netto = bruto - RT_BP
        rows.append(
            {
                "day": day,
                "signal_day": prior.index[-1],
                "side": int(side),
                "disp_z_side": side,
                "bruto_bp": bruto,
                "netto_bp": netto,
                "mae_bp": max(0.0, mae_bp),
                "entry": p0,
                "exit": p1,
            }
        )
    return pd.DataFrame(rows)


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
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    signal = build_signal()
    # diagnostic: how many non-flat signal days in train/test calendar
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
        ok_tr = (
            st["t_nw5"] is not None
            and st["t_nw5"] >= 2.0
            and st["mean_netto"] is not None
            and st["mean_netto"] > 0
        )
        ok_te = (
            te["n"] >= 1
            and te["t_nw5"] is not None
            and te["t_nw5"] >= 2.0
            and te["mean_netto"] is not None
            and te["mean_netto"] > 0
        )
        # also require plain day-clust t >= 2 on both (PREREG §4)
        ok_tr = ok_tr and st["t_netto"] is not None and st["t_netto"] >= 2.0
        ok_te = ok_te and te["t_netto"] is not None and te["t_netto"] >= 2.0
        verdict = "PASS" if (ok_tr and ok_te) else "FAIL_T"

    board = {
        "prereg": "PREREG_FTMO_N93_SECTOR_DISP_ROTATION",
        "new_family": "R",
        "config": "lb=10 / disp_fade +1.0/−0.5 / XL*→US100cash session-flat 15:30→21:00 CET",
        "rt_bp": RT_BP,
        "gate_bp": GATE_BP,
        "stress_gate_bp": STRESS_GATE_BP,
        "swap_bp": 0.0,
        "n_signal_days_train_nonzero": n_sig,
        "train": st,
        "test": te,
        "cost_pass": cost_pass,
        "stress_pass": stress_pass,
        "verdict": verdict,
        "reserve_2025": "untouched",
        "note": "U2 owns TRIALS/TRIAL_COUNT append. FAIL_COST_GATE → no bump (N78/N80). No retune.",
    }
    (OUT / "n93_gate_board.json").write_text(json.dumps(board, indent=2))
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
