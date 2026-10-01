#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen N32–N34."""
from __future__ import annotations
import gzip, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n32_n34_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
ATR_N, MIN_N = 14, 150
GATES = {"n32": (0.45, 1.35), "n33": (0.80, 2.40), "n34": (0.83, 2.49)}

def load_m5(rel):
    with gzip.open(ROOT / rel, "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna().sort_values("time")
    return df[(df["time"] >= TRAIN_START) & (df["time"] <= TRAIN_END)].reset_index(drop=True)

def atr_map(m5):
    g = m5.set_index("time").resample("1D").agg({"open":"first","high":"max","low":"min","close":"last"}).dropna()
    tr = pd.concat([g["high"]-g["low"], (g["high"]-g["close"].shift()).abs(), (g["low"]-g["close"].shift()).abs()], axis=1).max(axis=1)
    g["atr"] = tr.rolling(ATR_N).mean()
    return g["atr"]

def prior_atr(atr, day):
    for k in range(1, 10):
        a = atr.get(day - pd.Timedelta(days=k), np.nan)
        if a == a:
            return float(a)
    return float("nan")

def bar_at(g, day0, h, m=0):
    t = day0 + pd.Timedelta(hours=h, minutes=m)
    rows = g[g["time"] == t]
    return None if rows.empty else rows.iloc[0]

def bp_ret(entry, exit_px, side):
    return side * 1e4 * (exit_px - entry) / entry

def manage(g, day0, entry_t, entry, side, stop, flat_h, flat_m=0):
    flat_t = day0 + pd.Timedelta(hours=flat_h, minutes=flat_m)
    path = g[(g["time"] > entry_t) & (g["time"] <= flat_t)]
    exit_px = float(path.iloc[-1]["close"]) if len(path) else entry
    for _, row in path.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        if side == 1 and lo <= stop:
            return stop, "stop"
        if side == -1 and hi >= stop:
            return stop, "stop"
    return exit_px, "time"

def sim_n32(g, atr_price):
    if not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    ib = g[(g["time"] > day0 + pd.Timedelta(hours=15, minutes=30)) & (g["time"] <= day0 + pd.Timedelta(hours=16, minutes=30))]
    if len(ib) < 5:
        return None
    ib_hi, ib_lo = float(ib["high"].max()), float(ib["low"].min())
    ib_mid = 0.5 * (ib_hi + ib_lo)
    after = g[g["time"] > day0 + pd.Timedelta(hours=16, minutes=30)].sort_values("time")
    side = None
    entry = entry_t = None
    for _, row in after.iterrows():
        c = float(row["close"])
        if c > ib_hi:
            side, entry, entry_t = 1, c, row["time"]
            break
        if c < ib_lo:
            side, entry, entry_t = -1, c, row["time"]
            break
    if side is None:
        return None
    stop_ib = ib_mid
    stop_atr = entry - side * atr_price
    # use the stop closer to entry in adverse direction (= stricter)
    if side == 1:
        stop = max(stop_ib, stop_atr)
    else:
        stop = min(stop_ib, stop_atr)
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 18, 30)
    return {"date": str(day0.date()), "side": side, "entry": entry, "exit": exit_px, "hit": hit,
            "ib_hi": ib_hi, "ib_lo": ib_lo, "bruto_bp": bp_ret(entry, exit_px, side)}

def sim_n33(g, atr_price):
    if not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b0, b1 = bar_at(g, day0, 9, 0), bar_at(g, day0, 15, 30)
    if b0 is None or b1 is None:
        return None
    p0, p1 = float(b0["close"]), float(b1["close"])
    if p0 <= 0:
        return None
    lon = 1e4 * (p1 - p0) / p0
    if lon >= 35:
        side = 1
    elif lon <= -35:
        side = -1
    else:
        return None
    entry, entry_t = p1, b1["time"]
    stop = entry - side * atr_price
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 18, 30)
    return {"date": str(day0.date()), "side": side, "lon_bp": round(lon, 4), "entry": entry, "exit": exit_px,
            "hit": hit, "bruto_bp": bp_ret(entry, exit_px, side)}

def sim_n34(g, atr_price):
    if not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b0, b1 = bar_at(g, day0, 8, 0), bar_at(g, day0, 13, 0)
    if b0 is None or b1 is None:
        return None
    p0, p1 = float(b0["close"]), float(b1["close"])
    if p0 <= 0:
        return None
    dev = 1e4 * (p1 - p0) / p0
    if dev >= 40:
        side = -1
    elif dev <= -40:
        side = 1
    else:
        return None
    entry, entry_t = p1, b1["time"]
    stop = entry - side * atr_price
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 15, 0)
    return {"date": str(day0.date()), "side": side, "dev_bp": round(dev, 4), "entry": entry, "exit": exit_px,
            "hit": hit, "bruto_bp": bp_ret(entry, exit_px, side)}

def summarize(idea, trades, rt, gate):
    base = {"idea": idea, "rt_bp": rt, "gate_3x_rt": gate, "reserve_2025": "untouched"}
    if not trades:
        base.update({"n": 0, "mean_bruto_bp": None, "pass": False, "decision": "NO_PREREG_screen_fail_empty"})
        return base
    arr = np.array([t["bruto_bp"] for t in trades], float)
    mean, n = float(arr.mean()), len(arr)
    gate_ok, n_ok = mean >= gate, n >= MIN_N
    decision = "PASS_may_PREREG" if gate_ok and n_ok else ("NO_PREREG_underpowered" if gate_ok else "NO_PREREG_screen_fail")
    base.update({"n": n, "mean_bruto_bp": round(mean, 4), "median_bruto_bp": round(float(np.median(arr)), 4),
                 "pass_gate": bool(gate_ok), "n_ok": bool(n_ok), "pass": bool(gate_ok and n_ok),
                 "date_min": trades[0]["date"], "date_max": trades[-1]["date"], "decision": decision})
    return base

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    us30 = load_m5("data/m5gz/US30cash.csv.gz")
    usdcad = load_m5("data/m5gz/USDCAD.csv.gz")
    xau = load_m5("data/m5gz/XAUUSD.csv.gz")
    atr30, atrcad, atrx = atr_map(us30), atr_map(usdcad), atr_map(xau)
    n32 = n33 = n34 = []
    n32, n33, n34 = [], [], []
    for day, g in us30.groupby(us30["time"].dt.normalize()):
        t = sim_n32(g.sort_values("time"), prior_atr(atr30, day))
        if t: n32.append(t)
    for day, g in usdcad.groupby(usdcad["time"].dt.normalize()):
        t = sim_n33(g.sort_values("time"), prior_atr(atrcad, day))
        if t: n33.append(t)
    for day, g in xau.groupby(xau["time"].dt.normalize()):
        t = sim_n34(g.sort_values("time"), prior_atr(atrx, day))
        if t: n34.append(t)
    s32 = summarize("N32_US30_IB_CONT", n32, *GATES["n32"])
    s33 = summarize("N33_USDCAD_LON_NY", n33, *GATES["n33"])
    s34 = summarize("N34_XAU_POSTFIX_MR", n34, *GATES["n34"])
    board = {"n32": s32, "n33": s33, "n34": s34, "train": "2021-01-01..2023-12-31", "reserve_2025": "untouched",
             "runner": "Strateeg faraday scripts/n32_n34_prescreen.py"}
    for name, rows in [("n32", n32), ("n33", n33), ("n34", n34)]:
        pd.DataFrame(rows).to_csv(OUT / f"{name}_trades_train.csv", index=False)
    (OUT / "prescreen.json").write_text(json.dumps(board, indent=2) + "\n")
    md = ["# D-092.1 N32–N34 pre-screen", "",
          f"| N32 US30 IB cont | n={s32['n']} mean={s32['mean_bruto_bp']} gate=1.35 | {s32['decision']} |",
          f"| N33 USDCAD Lon→NY | n={s33['n']} mean={s33['mean_bruto_bp']} gate=2.40 | {s33['decision']} |",
          f"| N34 XAU postfix MR | n={s34['n']} mean={s34['mean_bruto_bp']} gate=2.49 | {s34['decision']} |", ""]
    (OUT / "prescreen.md").write_text("\n".join(md) + "\n")
    print(json.dumps(board, indent=2))

if __name__ == "__main__":
    main()
