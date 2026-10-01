#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N58 redesign, N60, N61, N62 (D-100 cycle ~11:20)."""
from __future__ import annotations
import gzip, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n58_n62_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
MIN_N = 150
GATE50 = 50.0

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

def daily_ohlc(m5: pd.DataFrame) -> pd.DataFrame:
    g = (
        m5.set_index("time")
        .resample("1D")
        .agg({"open": "first", "high": "max", "low": "min", "close": "last"})
        .dropna()
    )
    g.index = g.index.normalize()
    return g

def summarize(trades, gate, label):
    if not trades:
        return {
            "id": label,
            "n": 0,
            "mean_bruto_bp": None,
            "median_bruto_bp": None,
            "gate_bp": gate,
            "pass": False,
            "reason": "n=0",
        }
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

def screen_tsmom(m5: pd.DataFrame, lookback: int, hold: int, side_mode: str):
    """side_mode: long_only | short_only | both"""
    dc = daily_ohlc(m5)["close"]
    if len(dc) < lookback + hold + 5:
        return []
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
        ret = c_t / c_lb - 1.0
        if side_mode == "long_only":
            if ret <= 0:
                i += 1
                continue
            side = 1
        elif side_mode == "short_only":
            if ret >= 0:
                i += 1
                continue
            side = -1
        else:
            if ret > 0:
                side = 1
            elif ret < 0:
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
        i += hold
    return trades

def screen_n60_xag(m5: pd.DataFrame):
    """XAGUSD 5d bi-dir TSMOM with 1.5×ATR14 stop (VOORSTEL_N60)."""
    ohlc = daily_ohlc(m5)
    if len(ohlc) < 40:
        return []
    tr = pd.concat(
        [
            ohlc["high"] - ohlc["low"],
            (ohlc["high"] - ohlc["close"].shift()).abs(),
            (ohlc["low"] - ohlc["close"].shift()).abs(),
        ],
        axis=1,
    ).max(axis=1)
    atr = tr.rolling(14).mean()
    close = ohlc["close"]
    dates = list(close.index)
    lookback, hold = 5, 5
    trades = []
    i = max(lookback, 14)
    while i + hold < len(dates):
        c_t = float(close.iloc[i])
        c_lb = float(close.iloc[i - lookback])
        a = float(atr.iloc[i])
        if c_lb <= 0 or c_t <= 0 or not (a == a) or a <= 0:
            i += 1
            continue
        ret = c_t / c_lb - 1.0
        if ret > 0:
            side = 1
        elif ret < 0:
            side = -1
        else:
            i += 1
            continue
        entry = c_t
        stop = entry - side * 1.5 * a
        exit_px = float(close.iloc[i + hold])
        hit = "time"
        for j in range(1, hold + 1):
            hi = float(ohlc["high"].iloc[i + j])
            lo = float(ohlc["low"].iloc[i + j])
            if side == 1 and lo <= stop:
                exit_px, hit = stop, "stop"
                break
            if side == -1 and hi >= stop:
                exit_px, hit = stop, "stop"
                break
        trades.append(
            {
                "date": str(dates[i].date()),
                "side": side,
                "gross_bp": side * 1e4 * (exit_px - entry) / entry,
                "exit": hit,
            }
        )
        i += hold
    return trades

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    results = []

    # N58 AUDJPY L20/H10 long-only; gate 50
    t58 = screen_tsmom(load_m5("AUDJPY"), 20, 10, "long_only")
    r58 = summarize(t58, GATE50, "N58")
    results.append(r58)
    pd.DataFrame(t58).to_csv(OUT / "N58_trades.csv", index=False)

    # N60 XAGUSD 5d bi-dir + ATR stop; gate 53.01
    t60 = screen_n60_xag(load_m5("XAGUSD"))
    r60 = summarize(t60, 53.01, "N60")
    results.append(r60)
    pd.DataFrame(t60).to_csv(OUT / "N60_trades.csv", index=False)

    # N61 AUS200 short-only L20/H10; gate 50
    t61 = screen_tsmom(load_m5("AUS200cash"), 20, 10, "short_only")
    r61 = summarize(t61, GATE50, "N61")
    results.append(r61)
    pd.DataFrame(t61).to_csv(OUT / "N61_trades.csv", index=False)

    # N62 GBPJPY L20/H10 long-only; gate 50
    t62 = screen_tsmom(load_m5("GBPJPY"), 20, 10, "long_only")
    r62 = summarize(t62, GATE50, "N62")
    results.append(r62)
    pd.DataFrame(t62).to_csv(OUT / "N62_trades.csv", index=False)

    board = {
        "when": "2026-10-01 ~11:20 CEST",
        "train": "2021-01-01..2023-12-31",
        "min_n": MIN_N,
        "binding": "D-094 FREEZE OFF + D-094a + D-097 + D-098 + D-100 / C-024",
        "n59": "BARRED ENERGY clone — not screened",
        "results": results,
    }
    (OUT / "prescreen.json").write_text(json.dumps(board, indent=2))
    lines = [
        "# N58/N60/N61/N62 D-092.1 pre-screen (train 2021–2023; D-100)",
        "",
        "- N59: **BARRED** (ENERGY clone) — not screened.",
        "",
    ]
    for r in results:
        lines.append(
            f"- **{r['id']}**: n={r['n']} mean={r['mean_bruto_bp']} med={r['median_bruto_bp']} "
            f"gate={r['gate_bp']} → **{r['reason']}** (pass={r['pass']})"
        )
    (OUT / "prescreen.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(board, indent=2))

if __name__ == "__main__":
    main()
