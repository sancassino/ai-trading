#!/usr/bin/env python3
"""S2 MIDDAY_VWAP cost gate — train 2021–2023. PREREG 1b2e975."""
from __future__ import annotations
import gzip
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
M5 = ROOT / "data" / "m5gz"
DAILY = ROOT / "data" / "daily"
SYMBOLS = {"US100cash": 0.66, "US30cash": 0.45}
TRAIN_START, TRAIN_END = pd.Timestamp("2021-01-01"), pd.Timestamp("2023-12-31 23:59:59")
OPEN_H, OPEN_M, CLOSE_H = 9, 30, 16
ENTRY_START, ENTRY_END, FLAT_MIN = 150, 210, 330
DEV_K = 0.75
ATR_N = 14


def load_m5(sym):
    with gzip.open(M5 / f"{sym}.csv.gz", "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna().sort_values("time")
    return df[(df["time"] >= TRAIN_START) & (df["time"] <= TRAIN_END)]


def atr_series(sym, m5):
    path = DAILY / f"{sym}.csv"
    if path.exists():
        raw = [ln for ln in path.read_text().splitlines() if ln.strip() and not ln.startswith("#")]
        d1 = pd.read_csv(pd.io.common.StringIO("\n".join(raw)), sep=";")
        d1["date"] = pd.to_datetime(d1["date"]).dt.normalize()
    else:
        g = m5.set_index("time").between_time("09:30", "16:00").resample("1D").agg(
            {"open": "first", "high": "max", "low": "min", "close": "last"}
        ).dropna()
        d1 = g.reset_index().rename(columns={"time": "date"})
        d1["date"] = d1["date"].dt.normalize()
    for c in ("high", "low", "close"):
        d1[c] = pd.to_numeric(d1[c], errors="coerce")
    tr = pd.concat([d1["high"] - d1["low"], (d1["high"] - d1["close"].shift()).abs(), (d1["low"] - d1["close"].shift()).abs()], axis=1).max(axis=1)
    d1["atr"] = tr.rolling(ATR_N).mean()
    return d1.set_index("date")["atr"]


def sim_day(g, atr_price, rt):
    day0 = g["time"].dt.normalize().iloc[0]
    t0 = day0 + pd.Timedelta(hours=OPEN_H, minutes=OPEN_M)
    t_close = day0 + pd.Timedelta(hours=CLOSE_H)
    t_flat = t0 + pd.Timedelta(minutes=FLAT_MIN)
    sess = g[(g["time"] >= t0) & (g["time"] <= t_close)].copy()
    if sess.empty or not (atr_price == atr_price):
        return None
    # typical price VWAP proxy
    sess["tp"] = (sess["high"] + sess["low"] + sess["close"]) / 3.0
    sess["vwap"] = sess["tp"].expanding().mean()
    window = sess[(sess["time"] >= t0 + pd.Timedelta(minutes=ENTRY_START)) & (sess["time"] <= t0 + pd.Timedelta(minutes=ENTRY_END))]
    if window.empty:
        return None
    p_open = float(sess.iloc[0]["open"])
    atr_bp = 1e4 * atr_price / p_open
    entry_row = None
    side = None
    for _, row in window.iterrows():
        vwap = float(row["vwap"])
        if vwap <= 0:
            continue
        dev = 1e4 * (float(row["close"]) - vwap) / vwap
        if dev >= DEV_K * atr_bp:
            side, entry_row = -1, row
            break
        if dev <= -DEV_K * atr_bp:
            side, entry_row = 1, row
            break
    if entry_row is None:
        return None
    entry = float(entry_row["close"])
    vwap_e = float(entry_row["vwap"])
    dev_bp = 1e4 * (entry - vwap_e) / vwap_e
    stop = entry - side * abs(entry - vwap_e)  # 1×|dev| further from VWAP
    # actually: stop = entry + (-side direction away from vwap)
    # if short (side=-1), further above = entry + |dev_price|
    stop = entry + (-side) * abs(entry - vwap_e)
    target = vwap_e
    after = sess[sess["time"] > entry_row["time"]]
    after = after[after["time"] <= min(t_flat, t_close)]
    exit_px = float(after.iloc[-1]["close"]) if len(after) else entry
    for _, row in after.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        if side == 1:
            hit_t = lo <= target
            hit_s = hi >= stop
        else:
            hit_t = hi >= target
            hit_s = lo <= stop
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
    trades = []
    for sym, rt in SYMBOLS.items():
        m5 = load_m5(sym)
        atr = atr_series(sym, m5)
        for day, g in m5.groupby(m5["time"].dt.normalize()):
            prior = atr[atr.index < day].dropna()
            if prior.empty:
                continue
            b = sim_day(g.copy(), float(prior.iloc[-1]), rt)
            if b is None:
                continue
            trades.append({"symbol": sym, "date": day.date(), "bruto_bp": b, "rt": rt})
        print(sym, sum(1 for t in trades if t["symbol"] == sym), flush=True)
    df = pd.DataFrame(trades)
    if df.empty:
        print("NO_TRADES FAIL")
        Path("results/s2_midday_vwap_summary.txt").write_text("N=0 FAIL\n")
        return
    mean_b = float(df["bruto_bp"].mean())
    w_rt = float(df["rt"].mean())
    gate = 3 * w_rt
    print(f"N={len(df)} mean={mean_b:.4f} rt={w_rt:.4f} gate={gate:.4f} {'PASS' if mean_b>=gate else 'FAIL'}")
    df.to_csv("results/s2_midday_vwap_train.csv", index=False)
    Path("results/s2_midday_vwap_summary.txt").write_text(
        f"MIDDAY_VWAP\nN={len(df)}\nmean_bruto={mean_b}\nmean_rt={w_rt}\ngate={gate}\nresult={'PASS' if mean_b>=gate else 'FAIL'}\n"
    )


if __name__ == "__main__":
    main()
