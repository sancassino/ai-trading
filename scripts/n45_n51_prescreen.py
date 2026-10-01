#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N45, N48, N49, N50, N51 (D-097 cycle 10:15)."""
from __future__ import annotations
import gzip, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n45_n51_prescreen"
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
    df = df.dropna().sort_values("time")
    return df[(df["time"] >= TRAIN_START) & (df["time"] <= TRAIN_END)].reset_index(drop=True)

def daily_close(m5: pd.DataFrame) -> pd.Series:
    g = m5.set_index("time").resample("1D")["close"].last().dropna()
    g.index = g.index.normalize()
    return g

def atr14_daily(m5: pd.DataFrame) -> pd.Series:
    g = m5.set_index("time").resample("1D").agg({"open": "first", "high": "max", "low": "min", "close": "last"}).dropna()
    tr = pd.concat(
        [g["high"] - g["low"], (g["high"] - g["close"].shift()).abs(), (g["low"] - g["close"].shift()).abs()],
        axis=1,
    ).max(axis=1)
    return tr.rolling(14).mean()

def bar_at(g: pd.DataFrame, day0, h, m=0):
    t = day0 + pd.Timedelta(hours=h, minutes=m)
    rows = g[g["time"] == t]
    return None if rows.empty else rows.iloc[0]

def summarize(trades, gate, label):
    if not trades:
        return {"id": label, "n": 0, "mean_bruto_bp": None, "median_bruto_bp": None, "gate_bp": gate, "pass": False, "reason": "n=0"}
    s = pd.Series([t["gross_bp"] for t in trades], dtype=float)
    mean = float(s.mean())
    med = float(s.median())
    n = int(len(s))
    ok = (mean >= gate) and (n >= MIN_N)
    reason = "PASS" if ok else ("FAIL_MEAN" if mean < gate else "FAIL_N")
    return {
        "id": label,
        "n": n,
        "mean_bruto_bp": round(mean, 4),
        "median_bruto_bp": round(med, 4),
        "gate_bp": gate,
        "pass": ok,
        "reason": reason,
        "hit_rate": round(float((s > 0).mean()), 4),
    }

def screen_n45(m5: pd.DataFrame):
    # ETH Asia→EU: asia 00:00–08:00 ≥300 bp → continue flat 12:00; gate 54
    atr = atr14_daily(m5)
    rows = []
    for day, g in m5.groupby(m5["time"].dt.normalize()):
        g = g.sort_values("time")
        b0 = bar_at(g, day, 0, 0)
        b8 = bar_at(g, day, 8, 0)
        b12 = bar_at(g, day, 12, 0)
        if b0 is None or b8 is None or b12 is None:
            continue
        c0, c8 = float(b0["close"]), float(b8["close"])
        if c0 <= 0:
            continue
        asia = 1e4 * (c8 - c0) / c0
        if abs(asia) < 300:
            continue
        side = 1 if asia > 0 else -1
        entry = c8
        a = atr.get(day - pd.Timedelta(days=1), np.nan)
        if not (a == a) or a <= 0:
            # fallback prior available
            for k in range(2, 10):
                a = atr.get(day - pd.Timedelta(days=k), np.nan)
                if a == a and a > 0:
                    break
        stop = entry - side * 2.0 * float(a) if (a == a and a > 0) else np.nan
        path = g[(g["time"] > day + pd.Timedelta(hours=8)) & (g["time"] <= day + pd.Timedelta(hours=12))]
        exit_px = float(b12["close"])
        hit = "time"
        if stop == stop and len(path):
            for _, row in path.iterrows():
                hi, lo = float(row["high"]), float(row["low"])
                if side == 1 and lo <= stop:
                    exit_px, hit = stop, "stop"
                    break
                if side == -1 and hi >= stop:
                    exit_px, hit = stop, "stop"
                    break
        rows.append({"date": str(day.date()), "side": side, "gross_bp": side * 1e4 * (exit_px - entry) / entry, "exit": hit})
    return rows

def screen_tsmom_hold(m5: pd.DataFrame, lookback: int, hold: int, long_only: bool, regime_sma: int | None = None):
    dc = daily_close(m5)
    if len(dc) < lookback + hold + 5:
        return []
    sma = dc.rolling(regime_sma).mean() if regime_sma else None
    dates = list(dc.index)
    trades = []
    i = lookback
    while i + hold < len(dates):
        t = dates[i]
        c_t = float(dc.iloc[i])
        c_lb = float(dc.iloc[i - lookback])
        if c_lb <= 0 or c_t <= 0:
            i += 1
            continue
        if regime_sma is not None:
            s = sma.iloc[i]
            if not (s == s) or c_t <= float(s):
                i += 1
                continue
        ret = c_t / c_lb - 1.0
        if ret > 0:
            side = 1
        elif ret < 0 and not long_only:
            side = -1
        else:
            i += 1
            continue
        c_exit = float(dc.iloc[i + hold])
        if c_exit <= 0:
            i += 1
            continue
        trades.append(
            {
                "date": str(t.date()),
                "side": side,
                "gross_bp": side * 1e4 * (c_exit - c_t) / c_t,
                "exit": "time",
            }
        )
        i += hold  # non-overlapping
    return trades

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    results = []

    # N45 ETH
    eth = load_m5("ETHUSD")
    t45 = screen_n45(eth)
    r45 = summarize(t45, 54.0, "N45")
    results.append(r45)
    pd.DataFrame(t45).to_csv(OUT / "N45_trades.csv", index=False)

    # N48 USDJPY 1d TSMOM ret10 hold1 bi-dir; gate 7.08
    ujy = load_m5("USDJPY")
    t48 = screen_tsmom_hold(ujy, lookback=10, hold=1, long_only=False)
    r48 = summarize(t48, 7.08, "N48")
    results.append(r48)
    pd.DataFrame(t48).to_csv(OUT / "N48_trades.csv", index=False)

    # N49 UKOIL L20/H10 long-only; gate max(50, 8.13)=50
    uk = load_m5("UKOILcash")
    t49 = screen_tsmom_hold(uk, lookback=20, hold=10, long_only=True)
    r49 = summarize(t49, 50.0, "N49")
    results.append(r49)
    pd.DataFrame(t49).to_csv(OUT / "N49_trades.csv", index=False)

    # N50 USOIL L20/H10 long-only; gate 50
    us = load_m5("USOILcash")
    t50 = screen_tsmom_hold(us, lookback=20, hold=10, long_only=True)
    r50 = summarize(t50, 50.0, "N50")
    results.append(r50)
    pd.DataFrame(t50).to_csv(OUT / "N50_trades.csv", index=False)

    # N51 XAU L20/H5 long-only + SMA200; gate 50
    xau = load_m5("XAUUSD")
    t51 = screen_tsmom_hold(xau, lookback=20, hold=5, long_only=True, regime_sma=200)
    r51 = summarize(t51, 50.0, "N51")
    results.append(r51)
    pd.DataFrame(t51).to_csv(OUT / "N51_trades.csv", index=False)

    board = {"when": "2026-10-01 ~10:15 CEST", "train": "2021-01-01..2023-12-31", "min_n": MIN_N, "results": results}
    (OUT / "prescreen.json").write_text(json.dumps(board, indent=2))
    lines = ["# N45/N48/N49/N50/N51 D-092.1 pre-screen (train 2021–2023)", ""]
    for r in results:
        lines.append(
            f"- **{r['id']}**: n={r['n']} mean={r['mean_bruto_bp']} med={r['median_bruto_bp']} "
            f"gate={r['gate_bp']} → **{r['reason']}** (pass={r['pass']})"
        )
    (OUT / "prescreen.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(board, indent=2))

if __name__ == "__main__":
    main()
