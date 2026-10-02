#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen N80 UKOIL OVN-gap continuation EOD-flat."""
from __future__ import annotations
import gzip, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n80_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
GATE, MIN_N, GAP_TH = 8.13, 150, 40.0


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


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    m5 = load_m5("data/m5gz/UKOILcash.csv.gz")
    m5["day"] = m5["time"].dt.normalize()
    close_map = {}
    for day, g in m5.groupby("day"):
        ref = g[g["time"] <= day + pd.Timedelta(hours=22)]
        if len(ref):
            close_map[day] = float(ref.iloc[-1]["close"])
    trades = []
    days = sorted(m5["day"].unique())
    for i, day in enumerate(days):
        if i == 0:
            continue
        c_ref = close_map.get(days[i - 1])
        if not c_ref or c_ref <= 0:
            continue
        g = m5[m5["day"] == day]
        bar = g[g["time"] == day + pd.Timedelta(hours=8)]
        if bar.empty:
            after = g[(g["time"] >= day + pd.Timedelta(hours=8)) & (g["time"] <= day + pd.Timedelta(hours=8, minutes=15))]
            if after.empty:
                continue
            b = after.iloc[0]
        else:
            b = bar.iloc[0]
        mid = 0.5 * (float(b["high"]) + float(b["low"])) or float(b["close"])
        gap_bp = 1e4 * (mid / c_ref - 1.0)
        if abs(gap_bp) < GAP_TH:
            continue
        side = 1 if gap_bp >= GAP_TH else -1
        entry, entry_t = float(b["close"]), b["time"]
        path = g[(g["time"] > entry_t) & (g["time"] <= day + pd.Timedelta(hours=17))]
        if path.empty:
            continue
        exit_px = float(path.iloc[-1]["close"])
        bruto = side * 1e4 * (exit_px - entry) / entry
        trades.append({"day": str(day.date()), "side": side, "gap_bp": gap_bp, "bruto_bp": bruto})
    td = pd.DataFrame(trades)
    n = len(td)
    mean = float(td["bruto_bp"].mean()) if n else float("nan")
    if n >= MIN_N and mean >= GATE:
        verdict = "PASS_may_PREREG"
    elif mean == mean and mean >= GATE and n < MIN_N:
        verdict = "UNDERPOWERED"
    else:
        verdict = "FAIL"
    td.to_csv(OUT / "n80_trades_train.csv", index=False)
    summary = {
        "idea": "N80",
        "instrument": "UKOILcash",
        "n": n,
        "mean_bruto_bp": mean,
        "gate_bp": GATE,
        "verdict": verdict,
        "long_n": int((td["side"] == 1).sum()) if n else 0,
        "short_n": int((td["side"] == -1).sum()) if n else 0,
    }
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2))
    (OUT / "prescreen.md").write_text(
        f"# D-092.1 N80\n\nN={n} mean={mean:.4f} gate={GATE} → **{verdict}**\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
