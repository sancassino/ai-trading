#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N96 CADJPY LO 5d + N97 AUDCAD LO 5d commodity-XS mom."""
from __future__ import annotations
import gzip, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n96_n97_prescreen"
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


def screen_lo5d(m5):
    """Long-only non-overlapping 5d momentum (ret5>0 → long hold 5d)."""
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
    t96 = screen_lo5d(load_m5("CADJPY"))
    t97 = screen_lo5d(load_m5("AUDCAD"))
    s96 = verdict(t96, 4.80, "N96", "CADJPY")
    s97 = verdict(t97, 4.50, "N97", "AUDCAD")
    pd.DataFrame(t96).to_csv(OUT / "n96_trades_train.csv", index=False)
    pd.DataFrame(t97).to_csv(OUT / "n97_trades_train.csv", index=False)
    summary = {"N96": s96, "N97": s97}
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2))
    (OUT / "prescreen.md").write_text(
        "# D-092.1 N96/N97 pre-screen (train 2021–2023)\n\n"
        f"- **N96** CADJPY LO 5d: N={s96['n']} mean={s96['mean_bruto_bp']} "
        f"med={s96.get('median_bruto_bp')} gate={s96['gate_bp']} → **{s96['verdict']}** "
        f"years={s96.get('years')}\n"
        f"- **N97** AUDCAD LO 5d XS: N={s97['n']} mean={s97['mean_bruto_bp']} "
        f"med={s97.get('median_bruto_bp')} gate={s97['gate_bp']} → **{s97['verdict']}** "
        f"years={s97.get('years')}\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
