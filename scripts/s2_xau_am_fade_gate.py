#!/usr/bin/env python3
"""S2 XAU_AM_FADE cost gate — train 2021–2023. PREREG 1b2e975.
Times in PREREG are Europe/Amsterdam; m5gz clock for XAU treated as that wall clock.
"""
from __future__ import annotations
import gzip
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RT = 0.83
TRAIN_START, TRAIN_END = pd.Timestamp("2021-01-01"), pd.Timestamp("2023-12-31 23:59:59")
EXT_K = 0.60
ATR_N = 14


def load_m5():
    with gzip.open(ROOT / "data/m5gz/XAUUSD.csv.gz", "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna().sort_values("time")
    return df[(df["time"] >= TRAIN_START) & (df["time"] <= TRAIN_END)]


def atr_map(m5):
    g = m5.set_index("time").resample("1D").agg({"open": "first", "high": "max", "low": "min", "close": "last"}).dropna()
    tr = pd.concat([g["high"] - g["low"], (g["high"] - g["close"].shift()).abs(), (g["low"] - g["close"].shift()).abs()], axis=1).max(axis=1)
    g["atr"] = tr.rolling(ATR_N).mean()
    return g["atr"]


def sim_day(g, atr_price):
    day0 = g["time"].dt.normalize().iloc[0]
    asia = g[(g["time"] >= day0) & (g["time"] < day0 + pd.Timedelta(hours=8))]
    london = g[(g["time"] >= day0 + pd.Timedelta(hours=8)) & (g["time"] <= day0 + pd.Timedelta(hours=11, minutes=30))]
    if asia.empty or london.empty or not (atr_price == atr_price):
        return None
    asia_hi, asia_lo = float(asia["high"].max()), float(asia["low"].min())
    # 08:30–11:30 window for extension extremes
    win = g[(g["time"] >= day0 + pd.Timedelta(hours=8, minutes=30)) & (g["time"] <= day0 + pd.Timedelta(hours=11, minutes=30))]
    if win.empty:
        return None
    h = float(win["high"].max())
    l = float(win["low"].min())
    up = 1e4 * (h - asia_hi) / asia_hi if h > asia_hi else 0.0
    dn = 1e4 * (asia_lo - l) / asia_lo if l < asia_lo else 0.0
    # P_0800
    b0800 = g[g["time"] == day0 + pd.Timedelta(hours=8)]
    if b0800.empty:
        b0800 = g[g["time"] >= day0 + pd.Timedelta(hours=8)].head(1)
    if b0800.empty:
        return None
    p0800 = float(b0800.iloc[0]["open"])
    atr_bp = 1e4 * atr_price / p0800
    entry_rows = g[g["time"] == day0 + pd.Timedelta(hours=11, minutes=30)]
    if entry_rows.empty:
        return None
    entry = float(entry_rows.iloc[0]["close"])
    if up >= EXT_K * atr_bp and up > dn:
        side = -1
        ext = up
    elif dn >= EXT_K * atr_bp and dn > up:
        side = 1
        ext = dn
    else:
        return None
    asia_mid = 0.5 * (asia_hi + asia_lo)
    target = asia_mid
    stop = entry + (-side) * (ext / 1e4) * entry  # 1× max ext in price
    after = g[(g["time"] > entry_rows.iloc[0]["time"]) & (g["time"] <= day0 + pd.Timedelta(hours=14))]
    exit_px = float(after.iloc[-1]["close"]) if len(after) else entry
    for _, row in after.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        if side == 1:
            hit_t, hit_s = hi >= target, lo <= stop
        else:
            hit_t, hit_s = lo <= target, hi >= stop
        if hit_t and hit_s:
            exit_px = stop
            break
        if hit_s:
            exit_px = stop
            break
        if hit_t:
            exit_px = target
            break
    return side * 1e4 * (exit_px - entry) / entry


def main():
    m5 = load_m5()
    atr = atr_map(m5)
    trades = []
    for day, g in m5.groupby(m5["time"].dt.normalize()):
        prior = atr[atr.index < day].dropna()
        if prior.empty:
            continue
        b = sim_day(g.copy(), float(prior.iloc[-1]))
        if b is None:
            continue
        trades.append({"date": day.date(), "bruto_bp": b, "rt": RT})
    df = pd.DataFrame(trades)
    if df.empty:
        print("NO_TRADES FAIL")
        Path("results/s2_xau_am_fade_summary.txt").write_text("N=0 FAIL\n")
        return
    mean_b = float(df["bruto_bp"].mean())
    gate = 3 * RT
    print(f"N={len(df)} mean={mean_b:.4f} gate={gate:.4f} {'PASS' if mean_b>=gate else 'FAIL'}")
    df.to_csv("results/s2_xau_am_fade_train.csv", index=False)
    Path("results/s2_xau_am_fade_summary.txt").write_text(
        f"XAU_AM_FADE\nN={len(df)}\nmean_bruto={mean_b}\ngate={gate}\nresult={'PASS' if mean_b>=gate else 'FAIL'}\n"
    )


if __name__ == "__main__":
    main()
