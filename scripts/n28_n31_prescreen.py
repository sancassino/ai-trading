#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: Strateeg VOORSTEL N28–N31 (D-094 replacements)."""
from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n28_n31_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
ATR_N = 14
MIN_N = 150

N28_RT, N28_GATE = 1.10, 3.30
N29_RT, N29_GATE = 0.70, 2.10
N30_RT, N30_GATE = 1.61, 4.83
N31_RT, N31_GATE = 0.83, 2.49


def load_m5(rel: str) -> pd.DataFrame:
    path = ROOT / rel
    with gzip.open(path, "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna().sort_values("time")
    return df[(df["time"] >= TRAIN_START) & (df["time"] <= TRAIN_END)].reset_index(drop=True)


def atr_map(m5: pd.DataFrame) -> pd.Series:
    g = (
        m5.set_index("time")
        .resample("1D")
        .agg({"open": "first", "high": "max", "low": "min", "close": "last"})
        .dropna()
    )
    tr = pd.concat(
        [
            g["high"] - g["low"],
            (g["high"] - g["close"].shift()).abs(),
            (g["low"] - g["close"].shift()).abs(),
        ],
        axis=1,
    ).max(axis=1)
    g["atr"] = tr.rolling(ATR_N).mean()
    return g["atr"]


def prior_atr(atr: pd.Series, day: pd.Timestamp) -> float:
    for k in range(1, 10):
        a = atr.get(day - pd.Timedelta(days=k), np.nan)
        if a == a:
            return float(a)
    return float("nan")


def bar_at(g: pd.DataFrame, day0, h, m=0):
    t = day0 + pd.Timedelta(hours=h, minutes=m)
    rows = g[g["time"] == t]
    return None if rows.empty else rows.iloc[0]


def first_bar_at_or_after(g: pd.DataFrame, day0, h, m=0):
    t = day0 + pd.Timedelta(hours=h, minutes=m)
    rows = g[g["time"] >= t]
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


def sim_n28(g, atr_price):
    if not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b0 = bar_at(g, day0, 9, 0)
    b1 = bar_at(g, day0, 15, 30)
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
    return {
        "date": str(day0.date()),
        "side": side,
        "lon_bp": round(lon, 4),
        "entry": entry,
        "exit": exit_px,
        "hit": hit,
        "bruto_bp": bp_ret(entry, exit_px, side),
    }


def sim_n29(g, atr_price):
    if not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b0 = bar_at(g, day0, 9, 0)
    b1 = bar_at(g, day0, 12, 0)
    if b0 is None or b1 is None:
        return None
    p0, p1 = float(b0["close"]), float(b1["close"])
    if p0 <= 0:
        return None
    dev = 1e4 * (p1 - p0) / p0
    if dev >= 30:
        side = -1
    elif dev <= -30:
        side = 1
    else:
        return None
    entry, entry_t = p1, b1["time"]
    stop = entry - side * atr_price
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 15, 0)
    return {
        "date": str(day0.date()),
        "side": side,
        "dev_bp": round(dev, 4),
        "entry": entry,
        "exit": exit_px,
        "hit": hit,
        "bruto_bp": bp_ret(entry, exit_px, side),
    }


def close_near_2200(g: pd.DataFrame, day0):
    b22 = bar_at(g, day0, 22, 0)
    if b22 is not None:
        return float(b22["close"])
    if g.empty:
        return None
    return float(g.sort_values("time").iloc[-1]["close"])


def sim_n30(frames: dict[str, pd.DataFrame]):
    closes = {}
    for sym, m5 in frames.items():
        dmap = {}
        for day, g in m5.groupby(m5["time"].dt.normalize()):
            c = close_near_2200(g.sort_values("time"), day)
            if c is not None and c > 0:
                dmap[day] = c
        closes[sym] = dmap
    all_days = sorted(set().union(*[set(d.keys()) for d in closes.values()]))
    trades = []
    for i in range(6, len(all_days)):
        day_tm1 = all_days[i - 1]
        day_tm6 = all_days[i - 6]
        day_t = all_days[i]
        rets = {}
        ok = True
        for sym, dmap in closes.items():
            c1 = dmap.get(day_tm1)
            c0 = dmap.get(day_tm6)
            if c1 is None or c0 is None or c0 <= 0:
                ok = False
                break
            rets[sym] = 1e4 * (c1 - c0) / c0
        if not ok or len(rets) < 5:
            continue
        long_sym = max(rets, key=rets.get)
        short_sym = min(rets, key=rets.get)
        if long_sym == short_sym:
            continue
        if sum(1 for s, v in rets.items() if v == rets[long_sym]) > 1:
            continue
        if sum(1 for s, v in rets.items() if v == rets[short_sym]) > 1:
            continue
        legs = []
        for sym, side in ((long_sym, 1), (short_sym, -1)):
            g = frames[sym]
            gd = g[g["time"].dt.normalize() == day_t].sort_values("time")
            if gd.empty:
                legs = None
                break
            b_e = bar_at(gd, day_t, 15, 30)
            b_x = bar_at(gd, day_t, 21, 0)
            if b_e is None or b_x is None:
                legs = None
                break
            entry = float(b_e["close"])
            exit_px = float(b_x["close"])
            if entry <= 0:
                legs = None
                break
            legs.append(bp_ret(entry, exit_px, side))
        if not legs:
            continue
        trades.append(
            {
                "date": str(day_t.date()),
                "long_sym": long_sym,
                "short_sym": short_sym,
                "ret5_long": round(rets[long_sym], 4),
                "ret5_short": round(rets[short_sym], 4),
                "leg_long_bp": round(legs[0], 4),
                "leg_short_bp": round(legs[1], 4),
                "side": 1,
                "bruto_bp": 0.5 * (legs[0] + legs[1]),
                "hit": "time",
            }
        )
    return trades


def sim_n31(g, atr_price):
    if not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b0 = first_bar_at_or_after(g, day0, 0, 0)
    b1 = bar_at(g, day0, 8, 0)
    if b0 is None or b1 is None:
        return None
    # require Asia anchor reasonably near midnight (avoid late starts)
    if b0["time"] > day0 + pd.Timedelta(hours=1):
        return None
    p0, p1 = float(b0["close"]), float(b1["close"])
    if p0 <= 0:
        return None
    asia = 1e4 * (p1 - p0) / p0
    if asia >= 40:
        side = 1
    elif asia <= -40:
        side = -1
    else:
        return None
    entry, entry_t = p1, b1["time"]
    stop = entry - side * atr_price
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 12, 0)
    return {
        "date": str(day0.date()),
        "side": side,
        "asia_bp": round(asia, 4),
        "entry": entry,
        "exit": exit_px,
        "hit": hit,
        "bruto_bp": bp_ret(entry, exit_px, side),
    }


def summarize(idea, trades, rt, gate, extra=None):
    base = {"idea": idea, "rt_bp": rt, "gate_3x_rt": gate, "reserve_2025": "untouched"}
    if extra:
        base.update(extra)
    if not trades:
        base.update(
            {
                "n": 0,
                "mean_bruto_bp": None,
                "pass_gate": False,
                "n_ok": False,
                "pass": False,
                "decision": "NO_PREREG_screen_fail_empty",
            }
        )
        return base
    arr = np.array([t["bruto_bp"] for t in trades], float)
    mean = float(arr.mean())
    n = len(arr)
    gate_ok = mean >= gate
    n_ok = n >= MIN_N
    decision = (
        "PASS_may_PREREG"
        if gate_ok and n_ok
        else ("NO_PREREG_underpowered" if gate_ok else "NO_PREREG_screen_fail")
    )
    sides = np.array([t.get("side", 1) for t in trades])
    long_m = float(arr[sides == 1].mean()) if (sides == 1).any() else None
    short_m = float(arr[sides == -1].mean()) if (sides == -1).any() else None
    base.update(
        {
            "n": n,
            "n_long": int((sides == 1).sum()),
            "n_short": int((sides == -1).sum()),
            "mean_bruto_bp": round(mean, 4),
            "mean_bruto_long_bp": None if long_m is None else round(long_m, 4),
            "mean_bruto_short_bp": None if short_m is None else round(short_m, 4),
            "median_bruto_bp": round(float(np.median(arr)), 4),
            "pass_gate": bool(gate_ok),
            "n_ok": bool(n_ok),
            "pass": bool(gate_ok and n_ok),
            "date_min": trades[0]["date"],
            "date_max": trades[-1]["date"],
            "decision": decision,
        }
    )
    return base


def lab(s):
    if s["pass"]:
        return "PASS"
    if s.get("pass_gate") and not s.get("n_ok"):
        return "FAIL_N"
    return "FAIL"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    eurusd_jpy = load_m5("data/m5gz/EURJPY.csv.gz")
    gbpusd = load_m5("data/m5gz/GBPUSD.csv.gz")
    xau = load_m5("data/m5gz/XAUUSD.csv.gz")
    us100 = load_m5("data/m5gz/US100cash.csv.gz")
    us30 = load_m5("data/m5gz/US30cash.csv.gz")
    us500 = load_m5("data/m5gz/US500cash.csv.gz")
    ger = load_m5("data/m5gz/GER40cash.csv.gz")

    atr_ej = atr_map(eurusd_jpy)
    atr_gb = atr_map(gbpusd)
    atr_xau = atr_map(xau)

    n28, n29, n31 = [], [], []
    for day, g in eurusd_jpy.groupby(eurusd_jpy["time"].dt.normalize()):
        t = sim_n28(g.sort_values("time"), prior_atr(atr_ej, day))
        if t:
            n28.append(t)
    for day, g in gbpusd.groupby(gbpusd["time"].dt.normalize()):
        t = sim_n29(g.sort_values("time"), prior_atr(atr_gb, day))
        if t:
            n29.append(t)
    for day, g in xau.groupby(xau["time"].dt.normalize()):
        t = sim_n31(g.sort_values("time"), prior_atr(atr_xau, day))
        if t:
            n31.append(t)

    n30 = sim_n30(
        {
            "US100cash": us100,
            "US30cash": us30,
            "US500cash": us500,
            "GER40cash": ger,
            "XAUUSD": xau,
        }
    )

    s28 = summarize("N28_EURJPY_LON_NY_MOM", n28, N28_RT, N28_GATE)
    s29 = summarize("N29_GBPUSD_MIDDAY_FADE", n29, N29_RT, N29_GATE)
    s30 = summarize("N30_XS_5D_MOM", n30, N30_RT, N30_GATE)
    s31 = summarize("N31_XAU_ASIA_LON_CONT", n31, N31_RT, N31_GATE)

    board = {
        "n28": s28,
        "n29": s29,
        "n30": s30,
        "n31": s31,
        "source": "VOORSTEL_PRESCREEN_N28..N31",
        "min_n": MIN_N,
        "train": "2021-01-01 .. 2023-12-31",
        "reserve_2025": "untouched",
        "runner": "Strateeg faraday scripts/n28_n31_prescreen.py",
    }
    pd.DataFrame(n28).to_csv(OUT / "n28_trades_train.csv", index=False)
    pd.DataFrame(n29).to_csv(OUT / "n29_trades_train.csv", index=False)
    pd.DataFrame(n30).to_csv(OUT / "n30_trades_train.csv", index=False)
    pd.DataFrame(n31).to_csv(OUT / "n31_trades_train.csv", index=False)
    (OUT / "prescreen.json").write_text(json.dumps(board, indent=2) + "\n")
    md = [
        "# D-092.1 Strateeg pre-screen — N28–N31 (train 2021–2023)",
        "",
        "Replacements after N24–N27 FAIL. Reserve 2025+ untouched.",
        "",
        "| Idee | N | mean bruto | gate | Uitkomst | decision |",
        "|------|---|------------|------|----------|----------|",
        f"| N28 EURJPY Lon→NY mom | {s28['n']} | {s28['mean_bruto_bp']} | {N28_GATE} | **{lab(s28)}** | `{s28['decision']}` |",
        f"| N29 GBPUSD midday fade | {s29['n']} | {s29['mean_bruto_bp']} | {N29_GATE} | **{lab(s29)}** | `{s29['decision']}` |",
        f"| N30 XS 5d mom | {s30['n']} | {s30['mean_bruto_bp']} | {N30_GATE} | **{lab(s30)}** | `{s30['decision']}` |",
        f"| N31 XAU Asia→Lon cont | {s31['n']} | {s31['mean_bruto_bp']} | {N31_GATE} | **{lab(s31)}** | `{s31['decision']}` |",
        "",
    ]
    (OUT / "prescreen.md").write_text("\n".join(md) + "\n")
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
