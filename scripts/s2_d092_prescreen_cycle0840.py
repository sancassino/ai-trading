#!/usr/bin/env python3
"""D-092.1 non-clones — Strateeg-2 ~08:40 Europe/Amsterdam (D-094 FREEZE OFF).

Tracks 2+4; independent of Faraday N35–N37 queue.

A) EURGBP_LON_SPIKE_FADE — London 08:00–10:00 |ext|≥22 bp → fade to open @10:00;
   stop beyond spike extreme; flat 13:00.
   ≠ N29 GBPUSD midday, ≠ A5/GS02 ORB, ≠ EUR_NY_FADE.

B) AUS200_ASIA_RANGE_BO — Asia 01:00–04:00 CET range <0.55×ATR → breakout of Asia
   H/L after 04:00; stop mid-range; flat 07:30 (vóór EU open).
   ≠ AUDUSD_ASIA_BO, ≠ simple venue-ORB (N15–17), ≠ overnight month.

C) UK100_AM_MOM_CONT — 09:00–12:00 |ret|≥40 bp → CONTINUE @12:00 (not fade);
   stop 0.35×ATR; target 0.55×ATR; flat 15:00 vóór US.
   ≠ UK_AM_FADE (opposite), ≠ N24 US lunch fade, ≠ ORB.

D) EURAUD_LON_EXT_FADE — London 08:00–12:00 |ext from 08:00 open|≥35 bp → fade
   @12:00 toward open; flat 15:00.
   ≠ EUR_NY_FADE / AUDUSD_ASIA_BO / N27 AUDUSD H4 MR / N29.

E) GBPJPY_EU_MOM — 08:00–11:30 |ret|≥30 bp → continue @11:30; flat 14:30
   (vóór NY Lon→NY handoff family).
   ≠ N28 EURJPY Lon→NY (entry 15:30), ≠ N33 USDCAD, ≠ N37 EURUSD H4.
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
OUT = ROOT / "results" / "strateeg2_prescreen" / "cycle_0840"

# RT from COSTS_FTMO (+ alle for indices not in core file)
RT = {
    "EURGBP": 1.04,
    "AUS200cash": 1.36,
    "UK100cash": 1.42,
    "EURAUD": 1.11,
    "GBPJPY": 1.11,
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


def sim_eurgbp_lon_spike_fade(g, atr_map):
    if len(g) < 30:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None:
        return None
    b0 = bar_at(g, day0, 8, 0)
    b10 = bar_at(g, day0, 10, 0)
    if b0 is None or b10 is None:
        return None
    p_open = float(b0["open"])
    entry = float(b10["open"])
    if p_open <= 0 or entry <= 0:
        return None
    ext_bp = 1e4 * (entry - p_open) / p_open
    if abs(ext_bp) < 22.0:
        return None
    win = g[
        (g["time"] >= day0 + pd.Timedelta(hours=8))
        & (g["time"] < day0 + pd.Timedelta(hours=10))
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
        (g["time"] > day0 + pd.Timedelta(hours=10))
        & (g["time"] <= day0 + pd.Timedelta(hours=13))
    ]
    walked = walk_exit(after, side, stop, target)
    if walked is None:
        return None
    exit_px, reason = walked
    bruto = 1e4 * side * (exit_px - entry) / entry
    return dict(day=str(day0.date()), side=side, entry=entry, exit=exit_px, reason=reason, bruto_bp=bruto)


def sim_aus200_asia_range_bo(g, atr_map):
    if len(g) < 40:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None:
        return None
    asia = g[
        (g["time"] >= day0 + pd.Timedelta(hours=1))
        & (g["time"] < day0 + pd.Timedelta(hours=4))
    ]
    if len(asia) < 12:
        return None
    ahi, alo = float(asia["high"].max()), float(asia["low"].min())
    ar = ahi - alo
    if ar <= 0 or ar >= 0.55 * atr:
        return None  # need compression
    mid = 0.5 * (ahi + alo)
    # breakout hunt 04:00–07:00
    hunt = g[
        (g["time"] >= day0 + pd.Timedelta(hours=4))
        & (g["time"] < day0 + pd.Timedelta(hours=7))
    ]
    if hunt.empty:
        return None
    entry = None
    entry_t = None
    side = None
    for _, row in hunt.iterrows():
        hi, lo, cl = float(row["high"]), float(row["low"]), float(row["close"])
        if hi > ahi and cl > ahi:
            entry, entry_t, side = cl, row["time"], 1
            break
        if lo < alo and cl < alo:
            entry, entry_t, side = cl, row["time"], -1
            break
    if entry is None or entry <= 0:
        return None
    if side == 1:
        stop = mid
        target = entry + 0.70 * atr
    else:
        stop = mid
        target = entry - 0.70 * atr
    after = g[
        (g["time"] > entry_t) & (g["time"] <= day0 + pd.Timedelta(hours=7, minutes=30))
    ]
    walked = walk_exit(after, side, stop, target)
    if walked is None:
        return None
    exit_px, reason = walked
    bruto = 1e4 * side * (exit_px - entry) / entry
    return dict(day=str(day0.date()), side=side, entry=entry, exit=exit_px, reason=reason, bruto_bp=bruto)


def sim_uk100_am_mom_cont(g, atr_map):
    if len(g) < 40:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None:
        return None
    b0 = bar_at(g, day0, 9, 0)
    b12 = bar_at(g, day0, 12, 0)
    if b0 is None or b12 is None:
        return None
    p_open = float(b0["open"])
    entry = float(b12["open"])
    if p_open <= 0 or entry <= 0:
        return None
    morn_bp = 1e4 * (entry - p_open) / p_open
    if abs(morn_bp) < 40.0:
        return None
    side = 1 if morn_bp > 0 else -1
    if side == 1:
        stop = entry - 0.35 * atr
        target = entry + 0.55 * atr
    else:
        stop = entry + 0.35 * atr
        target = entry - 0.55 * atr
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


def sim_euraud_lon_ext_fade(g, atr_map):
    if len(g) < 40:
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
    if abs(ext_bp) < 35.0:
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
        stop = min(wlo, entry) - 0.15 * wr
        target = p_open
    else:
        stop = max(whi, entry) + 0.15 * wr
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


def sim_gbpjpy_eu_mom(g, atr_map):
    if len(g) < 40:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None:
        return None
    b0 = bar_at(g, day0, 8, 0)
    b1130 = bar_at(g, day0, 11, 30)
    if b0 is None or b1130 is None:
        return None
    p_open = float(b0["open"])
    entry = float(b1130["open"])
    if p_open <= 0 or entry <= 0:
        return None
    ret_bp = 1e4 * (entry - p_open) / p_open
    if abs(ret_bp) < 30.0:
        return None
    side = 1 if ret_bp > 0 else -1
    if side == 1:
        stop = entry - 0.40 * atr
        target = entry + 0.60 * atr
    else:
        stop = entry + 0.40 * atr
        target = entry - 0.60 * atr
    after = g[
        (g["time"] > day0 + pd.Timedelta(hours=11, minutes=30))
        & (g["time"] <= day0 + pd.Timedelta(hours=14, minutes=30))
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
        ("EURGBP_LON_SPIKE_FADE", "EURGBP", sim_eurgbp_lon_spike_fade),
        ("AUS200_ASIA_RANGE_BO", "AUS200cash", sim_aus200_asia_range_bo),
        ("UK100_AM_MOM_CONT", "UK100cash", sim_uk100_am_mom_cont),
        ("EURAUD_LON_EXT_FADE", "EURAUD", sim_euraud_lon_ext_fade),
        ("GBPJPY_EU_MOM", "GBPJPY", sim_gbpjpy_eu_mom),
    ]
    results = []
    for name, sym, fn in specs:
        s, _ = run_one(name, sym, fn)
        results.append(s)
        print(json.dumps(s), flush=True)

    (OUT / "prescreen.json").write_text(json.dumps(results, indent=2))
    lines = [
        "# S2 D-092.1 cycle_0840 (D-094 FREEZE OFF)",
        "",
        "| Idee | Symbool | N | mean bruto | gate | outcome | skew |",
        "|------|---------|--:|----------:|-----:|---------|------|",
    ]
    for r in results:
        sym = {
            "EURGBP_LON_SPIKE_FADE": "EURGBP",
            "AUS200_ASIA_RANGE_BO": "AUS200cash",
            "UK100_AM_MOM_CONT": "UK100cash",
            "EURAUD_LON_EXT_FADE": "EURAUD",
            "GBPJPY_EU_MOM": "GBPJPY",
        }[r["idea"]]
        lines.append(
            f"| {r['idea']} | {sym} | {r['n']} | {r['mean_bruto']} | {r['gate']} | **{r['outcome']}** | {r['skew']} |"
        )
    (OUT / "prescreen.md").write_text("\n".join(lines) + "\n")
    print("---SUMMARY---")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
