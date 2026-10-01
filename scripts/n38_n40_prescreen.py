#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: Strateeg VOORSTEL N38–N40 (D-094 tracks 2).

Train 2021–2023 only. Reserve 2025+ untouched. No PREREG / no TRIALS on FAIL.
"""
from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n38_n40_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
ATR_N = 14
MIN_N = 150

N38_RT, N38_GATE = 0.70, 2.10  # GBPUSD
N39_RT, N39_GATE = 1.25, 3.75  # BTCUSD
N40_RT, N40_GATE = 0.72, 2.16  # GER40cash


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


def bar_at(g: pd.DataFrame, day0, h, m=0, field="close"):
    t = day0 + pd.Timedelta(hours=h, minutes=m)
    rows = g[g["time"] == t]
    if rows.empty:
        return None
    return rows.iloc[0]


def manage(g, day0, entry_t, entry, side, stop, flat_h, flat_m=0):
    flat_t = day0 + pd.Timedelta(hours=flat_h, minutes=flat_m)
    path = g[(g["time"] > entry_t) & (g["time"] <= flat_t)]
    exit_px = float(path.iloc[-1]["close"]) if len(path) else entry
    hit = "time"
    if stop == stop:
        for _, row in path.iterrows():
            hi, lo = float(row["high"]), float(row["low"])
            if side == 1 and lo <= stop:
                return stop, "stop"
            if side == -1 and hi >= stop:
                return stop, "stop"
    return exit_px, hit


def sim_n38(g, atr_price):
    """GBPUSD Lon mom 08:00→11:30 |ret|≥30 → continue 11:30→14:30."""
    if not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b0800 = bar_at(g, day0, 8, 0)
    b1130 = bar_at(g, day0, 11, 30)
    if b0800 is None or b1130 is None:
        return None
    o0800 = float(b0800["open"])
    o1130 = float(b1130["open"])
    if o0800 <= 0:
        return None
    ret = 1e4 * (o1130 - o0800) / o0800
    if abs(ret) < 30:
        return None
    side = 1 if ret > 0 else -1
    entry = o1130
    entry_t = day0 + pd.Timedelta(hours=11, minutes=30)
    stop = entry - side * 0.5 * atr_price
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 14, 30)
    pnl = side * 1e4 * (exit_px - entry) / entry
    return {"date": str(day0.date()), "side": side, "ret_sig": ret, "gross_bp": pnl, "exit": hit}


def sim_n39(g, atr_price):
    """BTCUSD Asia 00:00→08:00 |asia|≥80 → continue 08:00→12:00."""
    if not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b0000 = bar_at(g, day0, 0, 0)
    b0800 = bar_at(g, day0, 8, 0)
    if b0000 is None or b0800 is None:
        return None
    c0000 = float(b0000["close"])
    c0800 = float(b0800["close"])
    if c0000 <= 0:
        return None
    asia = 1e4 * (c0800 - c0000) / c0000
    if abs(asia) < 80:
        return None
    side = 1 if asia > 0 else -1
    entry = c0800
    entry_t = day0 + pd.Timedelta(hours=8, minutes=0)
    stop = entry - side * 1.0 * atr_price
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 12, 0)
    pnl = side * 1e4 * (exit_px - entry) / entry
    return {"date": str(day0.date()), "side": side, "ret_sig": asia, "gross_bp": pnl, "exit": hit}


def sim_n40(g, atr_price):
    """GER40 mid-morning 09:30→12:00 |mom|≥40 → continue 12:00→14:00."""
    if not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b0930 = bar_at(g, day0, 9, 30)
    b1200 = bar_at(g, day0, 12, 0)
    if b0930 is None or b1200 is None:
        return None
    c0930 = float(b0930["close"])
    c1200 = float(b1200["close"])
    if c0930 <= 0:
        return None
    mom = 1e4 * (c1200 - c0930) / c0930
    if abs(mom) < 40:
        return None
    side = 1 if mom > 0 else -1
    entry = c1200
    entry_t = day0 + pd.Timedelta(hours=12, minutes=0)
    stop = entry - side * 1.0 * atr_price
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 14, 0)
    pnl = side * 1e4 * (exit_px - entry) / entry
    return {"date": str(day0.date()), "side": side, "ret_sig": mom, "gross_bp": pnl, "exit": hit}


def run_sleeve(sym, sim_fn, rt, gate, label):
    m5 = load_m5(sym)
    atr = atr_map(m5)
    trades = []
    for day, g in m5.groupby(m5["time"].dt.normalize()):
        if len(g) < 10:
            continue
        a = prior_atr(atr, day)
        r = sim_fn(g, a)
        if r:
            trades.append(r)
    df = pd.DataFrame(trades)
    if df.empty:
        return {
            "sleeve": label,
            "symbol": sym,
            "n": 0,
            "mean_gross_bp": None,
            "median_gross_bp": None,
            "gate_bp": gate,
            "rt_bp": rt,
            "power_n_ge_150": False,
            "gate_ok": False,
            "verdict": "FAIL",
            "date_min": None,
            "date_max": None,
        }, df
    mean = float(df["gross_bp"].mean())
    med = float(df["gross_bp"].median())
    n = int(len(df))
    ok = mean >= gate and n >= MIN_N
    return {
        "sleeve": label,
        "symbol": sym,
        "n": n,
        "mean_gross_bp": mean,
        "median_gross_bp": med,
        "gate_bp": gate,
        "rt_bp": rt,
        "power_n_ge_150": n >= MIN_N,
        "gate_ok": mean >= gate,
        "verdict": "PASS" if ok else "FAIL",
        "date_min": df["date"].min(),
        "date_max": df["date"].max(),
    }, df


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    specs = [
        ("GBPUSD", sim_n38, N38_RT, N38_GATE, "N38"),
        ("BTCUSD", sim_n39, N39_RT, N39_GATE, "N39"),
        ("GER40cash", sim_n40, N40_RT, N40_GATE, "N40"),
    ]
    rows = []
    for sym, fn, rt, gate, lab in specs:
        meta, df = run_sleeve(sym, fn, rt, gate, lab)
        rows.append(meta)
        if not df.empty:
            df.to_csv(OUT / f"{lab.lower()}_trades_train.csv", index=False)
        print(lab, meta["verdict"], "N=", meta["n"], "mean=", meta["mean_gross_bp"], "gate=", gate)
    summary = {
        "window": "2021-01-01..2023-12-31",
        "source": "VOORSTEL_PRESCREEN_N38..N40",
        "reserve_2025_touched": False,
        "sleeves": rows,
    }
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2))
    lines = [
        "# D-092.1 pre-screen N38–N40 TRAIN 2021–2023",
        "",
        "Source: Strateeg VOORSTEL N38–N40. Reserve 2025→ onaangeraakt.",
        "",
        "| Sleeve | N | mean bruto | gate | Uitkomst |",
        "|--------|---|------------|------|----------|",
    ]
    for r in rows:
        mean = "n/a" if r["mean_gross_bp"] is None else f"{r['mean_gross_bp']:+.2f} bp"
        lines.append(
            f"| **{r['sleeve']}** | {r['n']} | {mean} | {r['gate_bp']} | **{r['verdict']}** |"
        )
    lines.append("")
    lines.append("No PREREG on FAIL. No TRIALS append.")
    (OUT / "prescreen.md").write_text("\n".join(lines) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
