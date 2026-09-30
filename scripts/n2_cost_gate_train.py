#!/usr/bin/env python3
"""N2 REL_FLAT cost gate — train 2021–2023. PREREG 474a33c."""
from __future__ import annotations

import gzip
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
M5 = ROOT / "data" / "m5gz"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
OPEN_H, OPEN_M = 9, 30
CLOSE_H, CLOSE_M = 16, 0
T_MIN = 60
SIG_K = 1.25
PAIR_RT = 0.66 + 0.78  # 1.44


def load_m5(sym: str) -> pd.DataFrame:
    with gzip.open(M5 / f"{sym}.csv.gz", "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna().sort_values("time")
    return df[(df["time"] >= TRAIN_START) & (df["time"] <= TRAIN_END)].reset_index(drop=True)


def session_ret(df: pd.DataFrame, minutes: int) -> pd.Series:
    """Per-day return open→T+minutes in bp; index=date."""
    out = {}
    for day, g in df.groupby(df["time"].dt.normalize()):
        t0 = day + pd.Timedelta(hours=OPEN_H, minutes=OPEN_M)
        t1 = t0 + pd.Timedelta(minutes=minutes)
        if not ((g["time"] == t0).any() and (g["time"] == t1).any()):
            continue
        p0 = float(g.loc[g["time"] == t0, "open"].iloc[0])
        p1 = float(g.loc[g["time"] == t1, "close"].iloc[0])
        out[day] = 1e4 * (p1 - p0) / p0
    return pd.Series(out).sort_index()


def eod_ret_from_entry(df: pd.DataFrame, minutes: int) -> pd.Series:
    """Return from T+minutes close to session close, bp."""
    out = {}
    for day, g in df.groupby(df["time"].dt.normalize()):
        t0 = day + pd.Timedelta(hours=OPEN_H, minutes=OPEN_M)
        t1 = t0 + pd.Timedelta(minutes=minutes)
        tc = day + pd.Timedelta(hours=CLOSE_H, minutes=CLOSE_M)
        if not ((g["time"] == t1).any()):
            continue
        p1 = float(g.loc[g["time"] == t1, "close"].iloc[0])
        if (g["time"] == tc).any():
            pc = float(g.loc[g["time"] == tc, "close"].iloc[0])
        else:
            sess = g[(g["time"] >= t0) & (g["time"] <= tc)]
            if sess.empty:
                continue
            pc = float(sess.iloc[-1]["close"])
        out[day] = 1e4 * (pc - p1) / p1
    return pd.Series(out).sort_index()


def main() -> None:
    u100 = load_m5("US100cash")
    u500 = load_m5("US500cash")
    r100 = session_ret(u100, T_MIN)
    r500 = session_ret(u500, T_MIN)
    e100 = eod_ret_from_entry(u100, T_MIN)
    e500 = eod_ret_from_entry(u500, T_MIN)
    common = r100.index.intersection(r500.index).intersection(e100.index).intersection(e500.index)
    diff = (r100.loc[common] - r500.loc[common]).sort_index()
    # rolling 20-session stdev of prior diffs only
    rows = []
    diffs = []
    for d in common:
        hist = diff.loc[diff.index < d].tail(20)
        if len(hist) < 20:
            diffs.append(float(diff.loc[d]))
            continue
        sigma = float(hist.std(ddof=1))
        dlt = float(diff.loc[d])
        if sigma <= 0:
            continue
        if dlt >= SIG_K * sigma:
            # short 100 / long 500: pnl = -e100 + e500 (equal risk each leg)
            bruto = -float(e100.loc[d]) + float(e500.loc[d])
            side = "short100_long500"
        elif dlt <= -SIG_K * sigma:
            bruto = float(e100.loc[d]) - float(e500.loc[d])
            side = "long100_short500"
        else:
            continue
        rows.append({"date": d.date(), "diff": dlt, "sigma": sigma, "bruto_bp": bruto, "side": side})
    df = pd.DataFrame(rows)
    if df.empty:
        print("NO_TRADES FAIL")
        return
    mean_b = float(df["bruto_bp"].mean())
    gate = 3.0 * PAIR_RT
    print(f"N={len(df)} mean_bruto={mean_b:.4f} pair_rt={PAIR_RT} gate_3x={gate:.4f}")
    print("PASS" if mean_b >= gate else "FAIL")
    out = ROOT / "results" / "n2_cost_gate_train.csv"
    df.to_csv(out, index=False)
    (ROOT / "results" / "n2_cost_gate_summary.txt").write_text(
        f"N2 REL_FLAT train gate\nN={len(df)}\nmean_bruto_bp={mean_b}\npair_rt={PAIR_RT}\ngate_3x={gate}\n"
        f"result={'PASS' if mean_b >= gate else 'FAIL'}\n"
    )
    print("wrote", out)


if __name__ == "__main__":
    main()
