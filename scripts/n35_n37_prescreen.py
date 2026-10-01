#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: Strateeg VOORSTEL N35–N37 (D-094 tracks 2+4).

Train 2021–2023 only. Reserve 2025+ untouched. No PREREG / no TRIALS on FAIL.
Source: VOORSTEL_PRESCREEN_N35..N37 @ Strateeg 7ede6d0 / 782e6b8.
m5gz clock = Europe/Amsterdam wall (U2 AMS convention).
"""
from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n35_n37_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
ATR_N = 14
MIN_N = 150

N35_RT, N35_GATE = 0.66, 1.98  # US100cash
N36_RT, N36_GATE = 0.83, 2.49  # XAUUSD
N37_RT, N37_GATE = 0.63, 1.89  # EURUSD


def load_m5(sym: str) -> pd.DataFrame:
    path = ROOT / "data" / "m5gz" / f"{sym}.csv.gz"
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


def manage(g, day0, entry_t, entry, side, stop, flat_h, flat_m=0, use_stop=True):
    flat_t = day0 + pd.Timedelta(hours=flat_h, minutes=flat_m)
    path = g[(g["time"] > entry_t) & (g["time"] <= flat_t)]
    exit_px = float(path.iloc[-1]["close"]) if len(path) else entry
    hit = "time"
    if use_stop and stop == stop:
        for _, row in path.iterrows():
            hi, lo = float(row["high"]), float(row["low"])
            if side == 1 and lo <= stop:
                return stop, "stop"
            if side == -1 and hi >= stop:
                return stop, "stop"
    return exit_px, hit


def sim_n35(g, atr_price):
    """US100 EU mom 09:00→15:00 |eu|≥40 → continue 15:30→17:00 CET."""
    if not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b0900 = bar_at(g, day0, 9, 0)
    b1500 = bar_at(g, day0, 15, 0)
    b1530 = bar_at(g, day0, 15, 30)
    if b0900 is None or b1500 is None or b1530 is None:
        return None
    c0900 = float(b0900["close"])
    c1500 = float(b1500["close"])
    if c0900 <= 0:
        return None
    eu_bp = 1e4 * (c1500 - c0900) / c0900
    if abs(eu_bp) < 40.0:
        return None
    side = 1 if eu_bp > 0 else -1
    entry = float(b1530["close"])
    entry_t = b1530["time"]
    stop = entry - side * atr_price
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 17, 0)
    return {
        "date": str(day0.date()),
        "side": side,
        "eu_bp": eu_bp,
        "entry": entry,
        "exit": exit_px,
        "hit": hit,
        "gross_bp": side * 1e4 * (exit_px - entry) / entry,
    }


def sim_n36(g, atr_price):
    """XAU NY-open drive 15:30→16:00 |drive|≥25 → continue 16:00→17:00 CET."""
    if not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b1530 = bar_at(g, day0, 15, 30)
    b1600 = bar_at(g, day0, 16, 0)
    if b1530 is None or b1600 is None:
        return None
    c1530 = float(b1530["close"])
    c1600 = float(b1600["close"])
    if c1530 <= 0:
        return None
    drive = 1e4 * (c1600 - c1530) / c1530
    if abs(drive) < 25.0:
        return None
    side = 1 if drive > 0 else -1
    entry = c1600
    entry_t = b1600["time"]
    stop = entry - side * atr_price
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 17, 0)
    return {
        "date": str(day0.date()),
        "side": side,
        "drive_bp": drive,
        "entry": entry,
        "exit": exit_px,
        "hit": hit,
        "gross_bp": side * 1e4 * (exit_px - entry) / entry,
    }


def sim_n37(m5: pd.DataFrame):
    """EURUSD H4 SMA20 slope trend-follow: signal at 12:00 CET bar, exit 16:00 close."""
    # Resample to H4 on CET wall clock (already AMS in m5gz)
    h4 = (
        m5.set_index("time")
        .resample("4h", label="left", closed="left")
        .agg({"open": "first", "high": "max", "low": "min", "close": "last"})
        .dropna()
    )
    h4["sma20"] = h4["close"].rolling(20).mean()
    h4["sma20_prev"] = h4["sma20"].shift(1)
    rows = []
    for ts, row in h4.iterrows():
        if ts.hour != 12 or ts.minute != 0:
            continue
        if ts < TRAIN_START or ts > TRAIN_END:
            continue
        sma, sma_p, c = row["sma20"], row["sma20_prev"], row["close"]
        if not (sma == sma and sma_p == sma_p and c == c):
            continue
        if c > sma and sma > sma_p:
            side = 1
        elif c < sma and sma < sma_p:
            side = -1
        else:
            continue
        exit_ts = ts + pd.Timedelta(hours=4)  # 16:00 bar start → use that bar's close
        # Prefer exact 16:00 close from m5
        exit_bar = m5[m5["time"] == exit_ts]
        if exit_bar.empty:
            # last m5 at/before 16:00
            win = m5[(m5["time"] > ts) & (m5["time"] <= exit_ts)]
            if win.empty:
                continue
            exit_px = float(win.iloc[-1]["close"])
        else:
            exit_px = float(exit_bar.iloc[0]["close"])
        entry = float(c)
        rows.append(
            {
                "date": str(ts.date()),
                "side": side,
                "entry": entry,
                "exit": exit_px,
                "hit": "time",
                "gross_bp": side * 1e4 * (exit_px - entry) / entry,
            }
        )
    return pd.DataFrame(rows)


def run_day_sleeve(m5, atr, sim_fn, name):
    trades = []
    for day, g in m5.groupby(m5["time"].dt.normalize()):
        a = prior_atr(atr, day)
        r = sim_fn(g, a)
        if r:
            trades.append(r)
    df = pd.DataFrame(trades)
    df.to_csv(OUT / f"{name}_trades_train.csv", index=False)
    return df


def summarize(name, df, gate, rt):
    n = len(df)
    mean_g = float(df["gross_bp"].mean()) if n else float("nan")
    med_g = float(df["gross_bp"].median()) if n else float("nan")
    power = n >= MIN_N
    gate_ok = bool(mean_g == mean_g and mean_g >= gate)
    verdict = "PASS" if (power and gate_ok) else "FAIL"
    return {
        "sleeve": name,
        "n": n,
        "mean_gross_bp": mean_g,
        "median_gross_bp": med_g,
        "gate_bp": gate,
        "rt_bp": rt,
        "power_n_ge_150": power,
        "gate_ok": gate_ok,
        "verdict": verdict,
        "date_min": str(df["date"].min()) if n else None,
        "date_max": str(df["date"].max()) if n else None,
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    results = []

    us100 = load_m5("US100cash")
    atr_u = atr_map(us100)
    df35 = run_day_sleeve(us100, atr_u, sim_n35, "n35")
    results.append(summarize("N35", df35, N35_GATE, N35_RT))
    print("N35", results[-1])

    xau = load_m5("XAUUSD")
    atr_x = atr_map(xau)
    df36 = run_day_sleeve(xau, atr_x, sim_n36, "n36")
    results.append(summarize("N36", df36, N36_GATE, N36_RT))
    print("N36", results[-1])

    eurusd = load_m5("EURUSD")
    # Need SMA warm-up: load a bit earlier for rolling — reload without train clip for warm-up
    path = ROOT / "data/m5gz/EURUSD.csv.gz"
    with gzip.open(path, "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        raw = pd.read_csv(f, sep=";")
    raw["time"] = pd.to_datetime(raw["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        raw[c] = pd.to_numeric(raw[c], errors="coerce")
    raw = raw.dropna().sort_values("time")
    raw = raw[(raw["time"] >= pd.Timestamp("2020-10-01")) & (raw["time"] <= TRAIN_END)]
    # exclude 2025+ already by TRAIN_END
    df37 = sim_n37(raw.reset_index(drop=True))
    df37.to_csv(OUT / "n37_trades_train.csv", index=False)
    results.append(summarize("N37", df37, N37_GATE, N37_RT))
    print("N37", results[-1])

    summary = {
        "window": "2021-01-01..2023-12-31",
        "source": "VOORSTEL_PRESCREEN_N35..N37 @ Strateeg 782e6b8",
        "reserve_2025_touched": False,
        "sleeves": results,
    }
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [
        "# D-092.1 pre-screen N35–N37 TRAIN 2021–2023",
        "",
        f"Source: Strateeg VOORSTEL N35–N37 (`782e6b8`). Reserve 2025→ onaangeraakt.",
        "",
        "| Sleeve | N | mean bruto | gate | Uitkomst |",
        "|--------|---|------------|------|----------|",
    ]
    for r in results:
        lines.append(
            f"| **{r['sleeve']}** | {r['n']} | {r['mean_gross_bp']:+.2f} bp | {r['gate_bp']:.2f} | **{r['verdict']}** |"
        )
    lines += ["", "No PREREG on FAIL. No TRIALS append.", ""]
    (OUT / "prescreen.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
