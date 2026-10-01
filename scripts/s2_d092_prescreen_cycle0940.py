#!/usr/bin/env python3
"""D-092.1 non-clones — Strateeg-2 ~09:40 Europe/Amsterdam (D-094 FREEZE OFF + D-097).

Tracks 2+4; independent of Faraday OPEN N45–N48 queue.
GBPJPY_EU_MOM formal FAIL_T (TRIAL 449) — closed; do not clone.

A) FRA40_AM_EXT_FADE — FRA40 09:00–11:30 |ext from 09:00|≥0.40×ATR → fade @11:30
   toward open; stop beyond morn extreme+0.15×range; flat 14:00.
   ≠ N6/N9/N11/N40 GER40 family; ≠ EU→US (N35/N41/N44); ≠ ORB.

B) NZDUSD_LON_SPIKE_FADE — NZDUSD 08:00–10:30 |ext|≥25 bp → fade @10:30 to open;
   stop spike extreme+0.15×range; flat 13:30.
   ≠ N46 EURGBP Lon-fix (Faraday); ≠ AUDUSD_ASIA_BO; ≠ N47 USDCHF cont.

C) AUDJPY_TOKYO_CONT — AUDJPY 01:00–04:00 |ret|≥25 bp → continue @04:00;
   stop 0.35×ATR / target 0.55×ATR; flat 07:00 (vóór EU).
   ≠ AUDUSD_ASIA_BO; ≠ JP_TOKYO_FADE (dead fail); ≠ S2-USDJPY handoff; ≠ N48.

D) EURCHF_LON_EXT_FADE — EURCHF 08:00–12:00 |ext|≥30 bp → fade @12:00 to open;
   flat 15:00.
   ≠ N47 USDCHF Asia→Lon cont (opposite family + pair); ≠ EUR_NY_FADE; ≠ N29.

E) XAU_ASIA_RANGE_BO — XAU 01:00–07:00 Asia range <0.45×ATR → breakout of Asia
   H/L after 07:00; stop mid-range; flat 11:00 (vóór London-AM fade family).
   ≠ XAU_AM_FADE (London AM fade watch); ≠ XAU overlap/N7/N8/N36; ≠ ORB.
"""
from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
M5 = ROOT / "data" / "m5gz"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
OUT = ROOT / "results" / "strateeg2_prescreen" / "cycle_0940"

RT = {
    "FRA40cash": 1.98,
    "NZDUSD": 1.85,
    "AUDJPY": 1.61,
    "EURCHF": 1.20,
    "XAUUSD": 0.83,
}


def load_m5(sym: str) -> pd.DataFrame:
    with gzip.open(M5 / f"{sym}.csv.gz", "rt") as f:
        first = f.readline()
        if first.startswith("#"):
            while True:
                pos = f.tell()
                line = f.readline()
                if not line.startswith("#"):
                    if "time" not in line.lower() and "open" not in line.lower():
                        f.seek(pos)
                    break
        else:
            f.seek(0)
        df = pd.read_csv(
            f, sep=";", header=None, names=["time", "open", "high", "low", "close", "spread"]
        )
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M", errors="coerce")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["time", "close"]).sort_values("time").reset_index(drop=True)
    return df[(df["time"] >= TRAIN_START) & (df["time"] <= TRAIN_END)].copy()


def d1_atr_map(df: pd.DataFrame, n: int = 14) -> dict:
    g = df.groupby(df["time"].dt.normalize())
    h, l, c = g["high"].max(), g["low"].min(), g["close"].last()
    prev_c = c.shift(1)
    tr = pd.concat([(h - l), (h - prev_c).abs(), (l - prev_c).abs()], axis=1).max(axis=1)
    atr = tr.rolling(n, min_periods=n).mean().shift(1)
    return {d: float(v) for d, v in atr.items() if pd.notna(v) and v > 0}


def bar_at(g, day0, hh, mm):
    t = day0 + pd.Timedelta(hours=hh, minutes=mm)
    b = g[(g["time"] >= t) & (g["time"] < t + pd.Timedelta(minutes=5))]
    return None if b.empty else b.iloc[0]


def walk_exit(after, side, stop, target=None):
    if after.empty:
        return None
    exit_px, reason = float(after.iloc[-1]["close"]), "time"
    for _, row in after.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        if side == 1:
            if lo <= stop:
                return stop, "stop"
            if target is not None and hi >= target:
                return target, "target"
        else:
            if hi >= stop:
                return stop, "stop"
            if target is not None and lo <= target:
                return target, "target"
    return exit_px, reason


def sim_fra40_am_ext_fade(g, atr_map):
    if len(g) < 30:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None or atr <= 0:
        return None
    b0 = bar_at(g, day0, 9, 0)
    b1130 = bar_at(g, day0, 11, 30)
    if b0 is None or b1130 is None:
        return None
    p_open = float(b0["open"])
    entry = float(b1130["open"])
    if p_open <= 0 or entry <= 0:
        return None
    ext = entry - p_open
    if abs(ext) < 0.40 * atr:
        return None
    win = g[
        (g["time"] >= day0 + pd.Timedelta(hours=9))
        & (g["time"] < day0 + pd.Timedelta(hours=11, minutes=30))
    ]
    if len(win) < 8:
        return None
    whi, wlo = float(win["high"].max()), float(win["low"].min())
    wr = whi - wlo
    if wr <= 0:
        return None
    side = -1 if ext > 0 else 1
    if side == 1:
        stop = wlo - 0.15 * wr
        target = p_open
    else:
        stop = whi + 0.15 * wr
        target = p_open
    after = g[
        (g["time"] > day0 + pd.Timedelta(hours=11, minutes=30))
        & (g["time"] <= day0 + pd.Timedelta(hours=14))
    ]
    walked = walk_exit(after, side, stop, target)
    if walked is None:
        return None
    exit_px, reason = walked
    bruto = 1e4 * side * (exit_px - entry) / entry
    return dict(day=str(day0.date()), side=side, entry=entry, exit=exit_px, reason=reason, bruto_bp=bruto)


def sim_nzdusd_lon_spike_fade(g, atr_map):
    if len(g) < 30:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None:
        return None
    b0 = bar_at(g, day0, 8, 0)
    b1030 = bar_at(g, day0, 10, 30)
    if b0 is None or b1030 is None:
        return None
    p_open = float(b0["open"])
    entry = float(b1030["open"])
    if p_open <= 0 or entry <= 0:
        return None
    ext_bp = 1e4 * (entry - p_open) / p_open
    if abs(ext_bp) < 25.0:
        return None
    win = g[
        (g["time"] >= day0 + pd.Timedelta(hours=8))
        & (g["time"] < day0 + pd.Timedelta(hours=10, minutes=30))
    ]
    if len(win) < 8:
        return None
    whi, wlo = float(win["high"].max()), float(win["low"].min())
    wr = whi - wlo
    if wr <= 0:
        return None
    side = -1 if ext_bp > 0 else 1
    if side == 1:
        stop = wlo - 0.15 * wr
        target = p_open
    else:
        stop = whi + 0.15 * wr
        target = p_open
    after = g[
        (g["time"] > day0 + pd.Timedelta(hours=10, minutes=30))
        & (g["time"] <= day0 + pd.Timedelta(hours=13, minutes=30))
    ]
    walked = walk_exit(after, side, stop, target)
    if walked is None:
        return None
    exit_px, reason = walked
    bruto = 1e4 * side * (exit_px - entry) / entry
    return dict(day=str(day0.date()), side=side, entry=entry, exit=exit_px, reason=reason, bruto_bp=bruto)


def sim_audjpy_tokyo_cont(g, atr_map):
    if len(g) < 30:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None or atr <= 0:
        return None
    b0 = bar_at(g, day0, 1, 0)
    b4 = bar_at(g, day0, 4, 0)
    if b0 is None or b4 is None:
        return None
    p_open = float(b0["open"])
    entry = float(b4["open"])
    if p_open <= 0 or entry <= 0:
        return None
    ret_bp = 1e4 * (entry - p_open) / p_open
    if abs(ret_bp) < 25.0:
        return None
    side = 1 if ret_bp > 0 else -1
    if side == 1:
        stop = entry - 0.35 * atr
        target = entry + 0.55 * atr
    else:
        stop = entry + 0.35 * atr
        target = entry - 0.55 * atr
    after = g[
        (g["time"] > day0 + pd.Timedelta(hours=4))
        & (g["time"] <= day0 + pd.Timedelta(hours=7))
    ]
    walked = walk_exit(after, side, stop, target)
    if walked is None:
        return None
    exit_px, reason = walked
    bruto = 1e4 * side * (exit_px - entry) / entry
    return dict(day=str(day0.date()), side=side, entry=entry, exit=exit_px, reason=reason, bruto_bp=bruto)


def sim_eurchf_lon_ext_fade(g, atr_map):
    if len(g) < 30:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None:
        return None
    b0 = bar_at(g, day0, 8, 0)
    b12 = bar_at(g, day0, 12, 0)
    if b0 is None or b12 is None:
        return None
    p_open = float(b0["open"])
    entry = float(b12["open"])
    if p_open <= 0 or entry <= 0:
        return None
    ext_bp = 1e4 * (entry - p_open) / p_open
    if abs(ext_bp) < 30.0:
        return None
    win = g[
        (g["time"] >= day0 + pd.Timedelta(hours=8))
        & (g["time"] < day0 + pd.Timedelta(hours=12))
    ]
    if len(win) < 10:
        return None
    whi, wlo = float(win["high"].max()), float(win["low"].min())
    wr = whi - wlo
    if wr <= 0:
        return None
    side = -1 if ext_bp > 0 else 1
    if side == 1:
        stop = wlo - 0.15 * wr
        target = p_open
    else:
        stop = whi + 0.15 * wr
        target = p_open
    after = g[
        (g["time"] > day0 + pd.Timedelta(hours=12))
        & (g["time"] <= day0 + pd.Timedelta(hours=15))
    ]
    walked = walk_exit(after, side, stop, target)
    if walked is None:
        return None
    exit_px, reason = walked
    bruto = 1e4 * side * (exit_px - entry) / entry
    return dict(day=str(day0.date()), side=side, entry=entry, exit=exit_px, reason=reason, bruto_bp=bruto)


def sim_xau_asia_range_bo(g, atr_map):
    if len(g) < 40:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None or atr <= 0:
        return None
    asia = g[
        (g["time"] >= day0 + pd.Timedelta(hours=1))
        & (g["time"] < day0 + pd.Timedelta(hours=7))
    ]
    if len(asia) < 20:
        return None
    ahi, alo = float(asia["high"].max()), float(asia["low"].min())
    ar = ahi - alo
    if ar <= 0 or ar >= 0.45 * atr:
        return None
    b7 = bar_at(g, day0, 7, 0)
    if b7 is None:
        return None
    # Wait for first break of Asia H/L after 07:00, enter next bar open
    after_asia = g[
        (g["time"] >= day0 + pd.Timedelta(hours=7))
        & (g["time"] <= day0 + pd.Timedelta(hours=11))
    ]
    if len(after_asia) < 4:
        return None
    side = None
    entry = None
    entry_t = None
    for i in range(len(after_asia) - 1):
        row = after_asia.iloc[i]
        hi, lo = float(row["high"]), float(row["low"])
        nxt = after_asia.iloc[i + 1]
        if hi >= ahi and side is None:
            side = 1
            entry = float(nxt["open"])
            entry_t = nxt["time"]
            break
        if lo <= alo and side is None:
            side = -1
            entry = float(nxt["open"])
            entry_t = nxt["time"]
            break
    if side is None or entry is None or entry <= 0:
        return None
    mid = 0.5 * (ahi + alo)
    if side == 1:
        stop = mid
        target = entry + (entry - mid)  # 1R to mid distance
    else:
        stop = mid
        target = entry - (mid - entry)
    after = g[
        (g["time"] > entry_t) & (g["time"] <= day0 + pd.Timedelta(hours=11))
    ]
    walked = walk_exit(after, side, stop, target)
    if walked is None:
        return None
    exit_px, reason = walked
    bruto = 1e4 * side * (exit_px - entry) / entry
    return dict(day=str(day0.date()), side=side, entry=entry, exit=exit_px, reason=reason, bruto_bp=bruto)


def summarize(name, trades, rt):
    if not trades:
        return dict(
            idea=name, n=0, mean_bruto=None, median=None, gate=3 * rt, rt=rt,
            outcome="FAIL", stop_share=None, skew=None,
        )
    arr = np.array([t["bruto_bp"] for t in trades], dtype=float)
    stop_share = float(np.mean([t["reason"] == "stop" for t in trades]))
    mean = float(arr.mean())
    med = float(np.median(arr))
    gate = 3 * rt
    skew = (
        float(((arr - mean) ** 3).mean() / (arr.std(ddof=0) ** 3 + 1e-12))
        if len(arr) > 2
        else None
    )
    if mean >= gate and len(arr) >= 150:
        outcome = "PASS"
    elif mean >= gate and len(arr) < 150:
        outcome = "PASS_underpowered"
    else:
        outcome = "FAIL"
    return dict(
        idea=name,
        n=int(len(arr)),
        mean_bruto=round(mean, 4),
        median=round(med, 4),
        gate=round(gate, 4),
        rt=rt,
        outcome=outcome,
        stop_share=round(stop_share, 4),
        skew=None if skew is None else round(skew, 4),
    )


def run_one(name, sym, sim_fn):
    df = load_m5(sym)
    atr = d1_atr_map(df)
    trades = []
    for day0, g in df.groupby(df["time"].dt.normalize()):
        t = sim_fn(g, atr)
        if t:
            t["symbol"] = sym
            trades.append(t)
    s = summarize(name, trades, RT[sym])
    pd.DataFrame(trades).to_csv(OUT / f"{name}_trades.csv", index=False)
    return s, trades


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    specs = [
        ("FRA40_AM_EXT_FADE", "FRA40cash", sim_fra40_am_ext_fade),
        ("NZDUSD_LON_SPIKE_FADE", "NZDUSD", sim_nzdusd_lon_spike_fade),
        ("AUDJPY_TOKYO_CONT", "AUDJPY", sim_audjpy_tokyo_cont),
        ("EURCHF_LON_EXT_FADE", "EURCHF", sim_eurchf_lon_ext_fade),
        ("XAU_ASIA_RANGE_BO", "XAUUSD", sim_xau_asia_range_bo),
    ]
    results = []
    for name, sym, fn in specs:
        s, _ = run_one(name, sym, fn)
        results.append(s)
        print(json.dumps(s), flush=True)

    (OUT / "prescreen.json").write_text(json.dumps(results, indent=2))
    sym_map = {n: s for n, s, _ in specs}
    lines = [
        "# S2 D-092.1 cycle_0940 (D-094 FREEZE OFF + D-097)",
        "",
        "| Idee | Symbool | N | mean bruto | gate | outcome | skew |",
        "|------|---------|--:|----------:|-----:|---------|------|",
    ]
    for r in results:
        lines.append(
            f"| {r['idea']} | {sym_map[r['idea']]} | {r['n']} | {r['mean_bruto']} | {r['gate']} | **{r['outcome']}** | {r['skew']} |"
        )
    (OUT / "prescreen.md").write_text("\n".join(lines) + "\n")
    print("---SUMMARY---")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
