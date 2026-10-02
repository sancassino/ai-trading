#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N94 NZDJPY LO 5d + N95 XAU Lon→NY cont session-flat."""
from __future__ import annotations
import gzip, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n94_n95_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
MIN_N = 150


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
    df = df.dropna(subset=["open", "high", "low", "close"]).sort_values("time")
    return df[(df["time"] >= TRAIN_START) & (df["time"] <= TRAIN_END)].reset_index(drop=True)


def daily_close(m5: pd.DataFrame) -> pd.Series:
    m5 = m5.copy()
    m5["day"] = m5["time"].dt.normalize()
    rows = []
    for day, g in m5.groupby("day"):
        ref = g[g["time"] <= day + pd.Timedelta(hours=22)]
        if len(ref):
            rows.append((day, float(ref.iloc[-1]["close"])))
    s = pd.Series({d: c for d, c in rows}).sort_index()
    s.index = pd.DatetimeIndex(s.index).normalize()
    return s


def screen_n94(m5):
    dc = daily_close(m5)
    dates = list(dc.index)
    trades = []
    i = 5
    while i + 5 < len(dates):
        c_t = float(dc.iloc[i])
        c_lb = float(dc.iloc[i - 5])
        if c_lb <= 0 or c_t <= 0:
            i += 1
            continue
        ret5 = c_t / c_lb - 1.0
        if ret5 <= 0:
            i += 1
            continue
        c_exit = float(dc.iloc[i + 5])
        if c_exit <= 0:
            i += 1
            continue
        bruto = 1e4 * (c_exit - c_t) / c_t
        trades.append({"date": str(dates[i].date()), "side": 1, "bruto_bp": bruto, "ret5": ret5})
        i += 5
    return trades


def first_bar_at(g, day, h, m=0, span_min=15):
    t0 = day + pd.Timedelta(hours=h, minutes=m)
    t1 = t0 + pd.Timedelta(minutes=span_min)
    after = g[(g["time"] >= t0) & (g["time"] <= t1)]
    if after.empty:
        return None
    return after.iloc[0]


def screen_n95(m5):
    m5 = m5.copy()
    m5["day"] = m5["time"].dt.normalize()
    trades = []
    for day, g in m5.groupby("day"):
        b08 = first_bar_at(g, day, 8, 0)
        b11 = first_bar_at(g, day, 11, 0)
        b1530 = first_bar_at(g, day, 15, 30)
        exit_cut = day + pd.Timedelta(hours=21)
        path = g[g["time"] <= exit_cut]
        if b08 is None or b11 is None or b1530 is None or path.empty:
            continue
        p08 = float(b08["close"])
        p11 = float(b11["close"])
        if p08 <= 0:
            continue
        am_bp = 1e4 * (p11 / p08 - 1.0)
        if abs(am_bp) < 25:
            continue
        side = 1 if am_bp >= 25 else -1
        entry = float(b1530["close"])
        after = path[path["time"] >= b1530["time"]]
        if after.empty:
            continue
        exit_px = float(after.iloc[-1]["close"])
        if entry <= 0 or exit_px <= 0:
            continue
        bruto = side * 1e4 * (exit_px - entry) / entry
        trades.append({"date": str(day.date()), "side": side, "am_bp": am_bp, "bruto_bp": bruto})
    return trades


def verdict(trades, gate, label, instrument):
    n = len(trades)
    if n == 0:
        return {
            "id": label,
            "instrument": instrument,
            "n": 0,
            "mean_bruto_bp": None,
            "gate_bp": gate,
            "verdict": "FAIL",
        }
    arr = np.array([t["bruto_bp"] for t in trades], dtype=float)
    mean = float(arr.mean())
    if n >= MIN_N and mean >= gate:
        v = "PASS_may_PREREG"
    elif mean >= gate and n < MIN_N:
        v = "UNDERPOWERED"
    else:
        v = "FAIL"
    return {
        "id": label,
        "instrument": instrument,
        "n": n,
        "mean_bruto_bp": round(mean, 4),
        "median_bruto_bp": round(float(np.median(arr)), 4),
        "gate_bp": gate,
        "verdict": v,
        "hit_rate": round(float((arr > 0).mean()), 4),
        "years": {
            str(y): round(float(np.mean([t["bruto_bp"] for t in trades if t["date"].startswith(str(y))])), 4)
            for y in (2021, 2022, 2023)
            if any(t["date"].startswith(str(y)) for t in trades)
        },
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    t94 = screen_n94(load_m5("NZDJPY"))
    t95 = screen_n95(load_m5("XAUUSD"))
    s94 = verdict(t94, 6.00, "N94", "NZDJPY")
    s95 = verdict(t95, 2.49, "N95", "XAUUSD")
    pd.DataFrame(t94).to_csv(OUT / "n94_trades_train.csv", index=False)
    pd.DataFrame(t95).to_csv(OUT / "n95_trades_train.csv", index=False)
    summary = {"N94": s94, "N95": s95}
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2))
    (OUT / "prescreen.md").write_text(
        "# D-092.1 N94/N95 pre-screen (train 2021–2023)\n\n"
        f"- **N94** NZDJPY LO 5d: N={s94['n']} mean={s94['mean_bruto_bp']} "
        f"med={s94.get('median_bruto_bp')} gate={s94['gate_bp']} → **{s94['verdict']}** "
        f"years={s94.get('years')}\n"
        f"- **N95** XAU Lon→NY cont: N={s95['n']} mean={s95['mean_bruto_bp']} "
        f"med={s95.get('median_bruto_bp')} gate={s95['gate_bp']} → **{s95['verdict']}** "
        f"years={s95.get('years')}\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
