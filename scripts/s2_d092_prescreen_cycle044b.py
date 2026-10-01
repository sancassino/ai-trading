#!/usr/bin/env python3
"""D-092.1 extra non-clones — Strateeg-2 ~04:50 Europe/Amsterdam.

E) USDCAD_LONDON_FADE — same London fade-to-open as USDCHF idea but USDCAD (RT 0.80).
   ≠ LONDON_WIDE_NY_FADE (EUR/GBP; that faded into NY).

F) AUDUSD_ASIA_BO — Asia 00–08 range; break Asia high/low 09:00–11:00 continuation;
   stop mid-Asia; flat 14:00. ≠ GS02 fade, ≠ A5 EUR/GBP ORB, ≠ USDJPY_HANDOFF.

G) FAILED_PDH — US30/US100: pierce prior-day high/low in 15:30–16:00 then close back
   inside by 16:15 → fade the failed break; target PDH/PDL; stop 0.20×ATR beyond pierce;
   flat 19:00. ≠ Failed-OR (OR-based), ≠ N5 gap-fill.

H) BTC_LONDON_FADE — BTC 09:00–14:00 London range ≥0.70×ATR + close outer quintile
   → fade to London mid @14:00; stop extreme+0.15×range; flat 17:00.
   ≠ BTC_ASIA_FADE (other session), ≠ BTC_USOPEN.
"""
from __future__ import annotations
import gzip, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
M5 = ROOT / "data" / "m5gz"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
OUT = ROOT / "results" / "strateeg2_prescreen" / "cycle_0440b"
RT = {
    "US30cash": 0.45,
    "US100cash": 0.66,
    "USDCAD": 0.80,
    "AUDUSD": 1.22,
    "BTCUSD": 1.25,
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
        df = pd.read_csv(f, sep=";", header=None, names=["time", "open", "high", "low", "close", "spread"])
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


def prior_hl(df: pd.DataFrame) -> dict:
    g = df.groupby(df["time"].dt.normalize())
    h, l = g["high"].max(), g["low"].min()
    # map day -> prior day hl
    days = sorted(h.index)
    out = {}
    for i, d in enumerate(days):
        if i == 0:
            continue
        prev = days[i - 1]
        out[d] = (float(h.loc[prev]), float(l.loc[prev]))
    return out


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


def sim_london_fade(g, atr_map):
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None:
        return None
    b0 = bar_at(g, day0, 8, 0)
    b_entry = bar_at(g, day0, 11, 0)
    if b0 is None or b_entry is None:
        return None
    p_open = float(b0["open"])
    entry = float(b_entry["close"])
    if p_open <= 0:
        return None
    win = g[(g["time"] >= day0 + pd.Timedelta(hours=8)) &
            (g["time"] <= day0 + pd.Timedelta(hours=11))]
    if len(win) < 10:
        return None
    whi, wlo = float(win["high"].max()), float(win["low"].min())
    wr = whi - wlo
    if abs(entry - p_open) < 0.45 * atr:
        return None
    side = -1 if entry > p_open else 1
    if side == 1:
        stop = wlo - 0.15 * wr
        target = p_open
    else:
        stop = whi + 0.15 * wr
        target = p_open
    after = g[(g["time"] > day0 + pd.Timedelta(hours=11)) &
              (g["time"] <= day0 + pd.Timedelta(hours=14))]
    walked = walk_exit(after, side, stop, target)
    if walked is None:
        return None
    exit_px, reason = walked
    return dict(day=str(day0.date()), side=side, entry=entry, exit=exit_px, reason=reason,
                bruto_bp=1e4 * side * (exit_px - entry) / entry)


def sim_aud_asia_bo(g, atr_map):
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None:
        return None
    asia = g[(g["time"] >= day0) & (g["time"] < day0 + pd.Timedelta(hours=8))]
    if len(asia) < 20:
        return None
    ahi, alo = float(asia["high"].max()), float(asia["low"].min())
    ar = ahi - alo
    if ar < 0.35 * atr or ar <= 0:
        return None
    mid = 0.5 * (ahi + alo)
    # look for break 09:00–11:00
    window = g[(g["time"] >= day0 + pd.Timedelta(hours=9)) &
               (g["time"] <= day0 + pd.Timedelta(hours=11))]
    if window.empty:
        return None
    entry = entry_t = side = None
    for _, row in window.iterrows():
        hi, lo, cl = float(row["high"]), float(row["low"]), float(row["close"])
        if hi > ahi and cl > ahi:
            side, entry, entry_t = 1, cl, row["time"]
            break
        if lo < alo and cl < alo:
            side, entry, entry_t = -1, cl, row["time"]
            break
    if entry is None:
        return None
    stop = mid
    after = g[(g["time"] > entry_t) & (g["time"] <= day0 + pd.Timedelta(hours=14))]
    walked = walk_exit(after, side, stop, target=None)
    if walked is None:
        return None
    exit_px, reason = walked
    return dict(day=str(day0.date()), side=side, entry=entry, exit=exit_px, reason=reason,
                bruto_bp=1e4 * side * (exit_px - entry) / entry)


def sim_failed_pdh(g, atr_map, pdhl):
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    levels = pdhl.get(day0)
    if atr is None or levels is None:
        return None
    pdh, pdl = levels
    first = g[(g["time"] >= day0 + pd.Timedelta(hours=15, minutes=30)) &
              (g["time"] < day0 + pd.Timedelta(hours=16, minutes=0))]
    b_confirm = bar_at(g, day0, 16, 15)
    if first.empty or b_confirm is None:
        return None
    fhi, flo = float(first["high"].max()), float(first["low"].min())
    c15 = float(b_confirm["close"])
    side = None
    pierce = None
    if fhi > pdh and c15 < pdh:
        side = -1  # failed upside break → short
        pierce = fhi
        target = pdh
        stop = pierce + 0.20 * atr
    elif flo < pdl and c15 > pdl:
        side = 1
        pierce = flo
        target = pdl
        stop = pierce - 0.20 * atr
    else:
        return None
    entry = c15
    after = g[(g["time"] > day0 + pd.Timedelta(hours=16, minutes=15)) &
              (g["time"] <= day0 + pd.Timedelta(hours=19, minutes=0))]
    walked = walk_exit(after, side, stop, target)
    if walked is None:
        return None
    exit_px, reason = walked
    return dict(day=str(day0.date()), side=side, entry=entry, exit=exit_px, reason=reason,
                bruto_bp=1e4 * side * (exit_px - entry) / entry)


def sim_btc_london_fade(g, atr_map):
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None:
        return None
    lon = g[(g["time"] >= day0 + pd.Timedelta(hours=9)) &
            (g["time"] <= day0 + pd.Timedelta(hours=14))]
    if len(lon) < 20:
        return None
    lhi, llo = float(lon["high"].max()), float(lon["low"].min())
    lr = lhi - llo
    if lr < 0.70 * atr or lr <= 0:
        return None
    lclose = float(lon.iloc[-1]["close"])
    mid = 0.5 * (lhi + llo)
    q1 = llo + 0.20 * lr
    q4 = llo + 0.80 * lr
    if lclose >= q4:
        side = -1
    elif lclose <= q1:
        side = 1
    else:
        return None
    entry = lclose
    if side == 1:
        stop = llo - 0.15 * lr
        target = mid
    else:
        stop = lhi + 0.15 * lr
        target = mid
    after = g[(g["time"] > day0 + pd.Timedelta(hours=14)) &
              (g["time"] <= day0 + pd.Timedelta(hours=17))]
    walked = walk_exit(after, side, stop, target)
    if walked is None:
        return None
    exit_px, reason = walked
    return dict(day=str(day0.date()), side=side, entry=entry, exit=exit_px, reason=reason,
                bruto_bp=1e4 * side * (exit_px - entry) / entry)


def summarize(name, trades, rt):
    if not trades:
        return dict(idea=name, n=0, mean_bruto=None, median=None, gate=3 * rt, rt=rt, outcome="FAIL", stop_share=None, skew=None)
    arr = np.array([t["bruto_bp"] for t in trades], dtype=float)
    stop_share = float(np.mean([t["reason"] == "stop" for t in trades]))
    mean = float(arr.mean())
    med = float(np.median(arr))
    gate = 3 * rt
    skew = float(((arr - mean) ** 3).mean() / (arr.std(ddof=0) ** 3 + 1e-12)) if len(arr) > 2 else None
    outcome = "PASS" if (len(arr) >= 150 and mean >= gate) else (
        "PASS_underpowered" if (mean >= gate and len(arr) < 150) else "FAIL"
    )
    return dict(
        idea=name, n=int(len(arr)), mean_bruto=round(mean, 4), median=round(med, 4),
        gate=round(gate, 4), rt=rt, outcome=outcome, stop_share=round(stop_share, 4),
        skew=None if skew is None else round(skew, 4),
    )


def run_day_sim(df, atr, fn, **kw):
    trades = []
    for day0, g in df.groupby(df["time"].dt.normalize()):
        t = fn(g, atr, **kw) if kw else fn(g, atr)
        if t:
            trades.append(t)
    return trades


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    results = []

    # E USDCAD
    df = load_m5("USDCAD")
    atr = d1_atr_map(df)
    trades = run_day_sim(df, atr, sim_london_fade)
    for t in trades:
        t["symbol"] = "USDCAD"
    results.append(summarize("USDCAD_LONDON_FADE", trades, RT["USDCAD"]))
    pd.DataFrame(trades).to_csv(OUT / "USDCAD_LONDON_FADE_trades.csv", index=False)

    # F AUDUSD Asia BO
    df = load_m5("AUDUSD")
    atr = d1_atr_map(df)
    trades = run_day_sim(df, atr, sim_aud_asia_bo)
    for t in trades:
        t["symbol"] = "AUDUSD"
    results.append(summarize("AUDUSD_ASIA_BO", trades, RT["AUDUSD"]))
    pd.DataFrame(trades).to_csv(OUT / "AUDUSD_ASIA_BO_trades.csv", index=False)

    # G FAILED_PDH pooled
    trades_g = []
    for sym in ("US30cash", "US100cash"):
        df = load_m5(sym)
        atr = d1_atr_map(df)
        pdhl = prior_hl(df)
        for day0, g in df.groupby(df["time"].dt.normalize()):
            t = sim_failed_pdh(g, atr, pdhl)
            if t:
                t["symbol"] = sym
                trades_g.append(t)
        pd.DataFrame([t for t in trades_g if t["symbol"] == sym]).to_csv(
            OUT / f"FAILED_PDH_{sym}_trades.csv", index=False
        )
    rt_g = float(np.mean([RT[t["symbol"]] for t in trades_g])) if trades_g else 0.555
    results.append(summarize("FAILED_PDH_US30_US100", trades_g, rt_g))
    pd.DataFrame(trades_g).to_csv(OUT / "FAILED_PDH_pooled_trades.csv", index=False)

    # H BTC London fade
    df = load_m5("BTCUSD")
    atr = d1_atr_map(df)
    trades = run_day_sim(df, atr, sim_btc_london_fade)
    for t in trades:
        t["symbol"] = "BTCUSD"
    results.append(summarize("BTC_LONDON_FADE", trades, RT["BTCUSD"]))
    pd.DataFrame(trades).to_csv(OUT / "BTC_LONDON_FADE_trades.csv", index=False)

    (OUT / "prescreen.json").write_text(json.dumps(results, indent=2))
    lines = ["# S2 D-092.1 cycle_0440b", "",
             "| Idee | N | mean bruto | gate | outcome | skew |",
             "|------|--:|----------:|-----:|---------|------|"]
    for r in results:
        lines.append(
            f"| {r['idea']} | {r['n']} | {r['mean_bruto']} | {r['gate']} | **{r['outcome']}** | {r['skew']} |"
        )
    (OUT / "prescreen.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
