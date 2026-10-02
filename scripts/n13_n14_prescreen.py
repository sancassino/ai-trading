#!/usr/bin/env python3
"""D-092.1 free pre-screen: Strateeg VOORSTEL N13 (GER40 US-Open Sync)
and N14 (US100 NY-Open Pre-Market Momentum).

Train 2021–2023 only. Reserve 2025+ untouched. No PREREG / no TRIALS.
Source: VOORSTEL_PRESCREEN_N13/N14 @ Strateeg e8f261f.
m5gz clock = Europe/Amsterdam wall.
"""
from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n13_n14_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
ATR_N = 14
MIN_N = 150
N13_RT, N13_GATE = 0.72, 2.16
N14_RT, N14_GATE = 0.60, 1.80


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


def bp_ret(entry, exit_px, side):
    return side * 1e4 * (exit_px - entry) / entry


def manage(g, day0, entry_t, entry, side, stop, flat_h=17):
    path = g[(g["time"] > entry_t) & (g["time"] <= day0 + pd.Timedelta(hours=flat_h))]
    exit_px = float(path.iloc[-1]["close"]) if len(path) else entry
    hit = "time"
    for _, row in path.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        if side == 1 and lo <= stop:
            return stop, "stop"
        if side == -1 and hi >= stop:
            return stop, "stop"
    return exit_px, hit


def sim_n13(ger_day, us_day, atr_price):
    if not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = ger_day["time"].dt.normalize().iloc[0]
    b1525 = bar_at(us_day, day0, 15, 25)
    b1530_us = bar_at(us_day, day0, 15, 30)
    b1530_ger = bar_at(ger_day, day0, 15, 30)
    if b1525 is None or b1530_us is None or b1530_ger is None:
        return None
    p1525 = float(b1525["close"])
    p1530 = float(b1530_us["close"])
    if p1525 <= 0:
        return None
    us_open_bp = 1e4 * (p1530 - p1525) / p1525
    if us_open_bp >= 15.0:
        side = 1
    elif us_open_bp <= -15.0:
        side = -1
    else:
        return None
    entry = float(b1530_ger["close"])
    entry_t = b1530_ger["time"]
    stop = entry - side * atr_price
    exit_px, hit = manage(ger_day, day0, entry_t, entry, side, stop, 17)
    return {
        "date": str(day0.date()),
        "side": side,
        "us_open_bp": round(us_open_bp, 4),
        "entry": entry,
        "exit": exit_px,
        "hit": hit,
        "atr": atr_price,
        "bruto_bp": bp_ret(entry, exit_px, side),
    }


def sim_n14(g, atr_price):
    if not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b1430 = bar_at(g, day0, 14, 30)
    b1530 = bar_at(g, day0, 15, 30)
    if b1430 is None or b1530 is None:
        return None
    p1430 = float(b1430["close"])
    p1530 = float(b1530["close"])
    if p1430 <= 0:
        return None
    pm_bp = 1e4 * (p1530 - p1430) / p1430
    if pm_bp >= 25.0:
        side = 1
    elif pm_bp <= -25.0:
        side = -1
    else:
        return None
    entry = p1530
    entry_t = b1530["time"]
    stop = entry - side * atr_price
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 17)
    return {
        "date": str(day0.date()),
        "side": side,
        "pm_bp": round(pm_bp, 4),
        "entry": entry,
        "exit": exit_px,
        "hit": hit,
        "atr": atr_price,
        "bruto_bp": bp_ret(entry, exit_px, side),
    }


def summarize(idea, trades, rt, gate):
    if not trades:
        return {
            "idea": idea, "n": 0, "mean_bruto_bp": None, "rt_bp": rt,
            "gate_3x_rt": gate, "pass_gate": False, "n_ok": False, "pass": False,
            "decision": "NO_PREREG_screen_fail_empty",
        }
    arr = np.array([t["bruto_bp"] for t in trades], float)
    mean = float(arr.mean())
    n = len(arr)
    gate_ok = mean >= gate
    n_ok = n >= MIN_N
    if not gate_ok:
        decision = "NO_PREREG_screen_fail"
    elif not n_ok:
        decision = "NO_PREREG_underpowered"
    else:
        decision = "PASS_may_PREREG"
    return {
        "idea": idea,
        "n": n,
        "mean_bruto_bp": round(mean, 4),
        "median_bruto_bp": round(float(np.median(arr)), 4),
        "p25": round(float(np.percentile(arr, 25)), 4),
        "p75": round(float(np.percentile(arr, 75)), 4),
        "stop_share": round(float(np.mean([t["hit"] == "stop" for t in trades])), 4),
        "rt_bp": rt,
        "gate_3x_rt": gate,
        "pass_gate": bool(gate_ok),
        "n_ok": bool(n_ok),
        "pass": bool(gate_ok and n_ok),
        "date_min": trades[0]["date"],
        "date_max": trades[-1]["date"],
        "decision": decision,
        "reserve_2025": "untouched",
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ger = load_m5("data/m5gz/GER40cash.csv.gz")
    us500 = load_m5("data/m5gz/US500cash.csv.gz")
    us100 = load_m5("data/m5gz/US100cash.csv.gz")
    atr_ger = atr_map(ger)
    atr_us100 = atr_map(us100)

    us_by = {d: g.sort_values("time") for d, g in us500.groupby(us500["time"].dt.normalize())}
    n13 = []
    for day, g in ger.groupby(ger["time"].dt.normalize()):
        ug = us_by.get(day)
        if ug is None:
            continue
        t = sim_n13(g.sort_values("time"), ug, prior_atr(atr_ger, day))
        if t:
            n13.append(t)

    n14 = []
    for day, g in us100.groupby(us100["time"].dt.normalize()):
        t = sim_n14(g.sort_values("time"), prior_atr(atr_us100, day))
        if t:
            n14.append(t)

    s13 = summarize("N13_GER40_USOPEN_SYNC", n13, N13_RT, N13_GATE)
    s14 = summarize("N14_US100_NYOPEN_PM", n14, N14_RT, N14_GATE)
    board = {
        "n13": s13,
        "n14": s14,
        "source": "VOORSTEL_PRESCREEN_N13/N14 @ e8f261f",
        "min_n": MIN_N,
        "reserve_2025": "untouched",
    }
    pd.DataFrame(n13).to_csv(OUT / "n13_trades_train.csv", index=False)
    pd.DataFrame(n14).to_csv(OUT / "n14_trades_train.csv", index=False)
    (OUT / "prescreen.json").write_text(json.dumps(board, indent=2) + "\n")

    def lab(s):
        if s["pass"]:
            return "PASS"
        if s.get("pass_gate") and not s.get("n_ok"):
            return "FAIL_N (underpowered)"
        return "FAIL"

    md = [
        "# D-092.1 U2 pre-screen — N13 / N14 (train 2021–2023)",
        "",
        "Source: Strateeg `VOORSTEL_PRESCREEN_N13.md` / `N14.md` @ `e8f261f`.",
        "Reserve 2025+ untouched. No TRIALS. No PREREG claimed by this screen.",
        f"PREREG requires gate PASS **and** N≥{MIN_N}.",
        "",
        "| Idee | N | mean bruto | gate | Uitkomst |",
        "|------|---|------------|------|----------|",
        f"| N13 GER40 US-Open Sync | {s13['n']} | {s13['mean_bruto_bp']} bp | {N13_GATE} bp | **{lab(s13)}** |",
        f"| N14 US100 NY-Open PM Mom | {s14['n']} | {s14['mean_bruto_bp']} bp | {N14_GATE} bp | **{lab(s14)}** |",
        "",
        f"- N13 decision: `{s13['decision']}`",
        f"- N14 decision: `{s14['decision']}`",
        "",
    ]
    (OUT / "prescreen.md").write_text("\n".join(md) + "\n")
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
