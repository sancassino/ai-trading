#!/usr/bin/env python3
"""D-092.1 non-clones — Strateeg-2 ~04:44 Europe/Amsterdam.

A) WIDEOPEN_PB — US30/US100: first-90m range ≥0.65×ATR → 35% pullback toward open
   → continuation in morning direction; target morn extreme; flat 20:00.
   ≠ VWAP_PB (no VWAP), ≠ ORB, ≠ LUNCH_OPEN (cont ≠ fade), ≠ IB_FADE.

B) US30_LEAD_US100 — at 16:30: US30 |morn|≥0.40×ATR and US100 |morn|<0.25×ATR
   → trade US100 in US30 direction; stop 0.35×ATR_US100; flat 19:00.
   ≠ GER_US_LEAD (US→US), ≠ N2 (relative flat).

C) BTC_ASIA_FADE — Asia 00:00–08:00 range ≥0.80×ATR + close outer quartile
   → fade to Asia mid @09:00; stop Asia extreme+0.15×range; flat 13:00.
   ≠ S2-BTC US-open, ≠ N18/N19 gap.

D) USDCHF_LONDON_FADE — London 08:00–11:00 extension ≥0.45×ATR → fade to London open;
   stop morn extreme+0.15×range; flat 14:00 (vóór NY).
   ≠ A5/GS02/EUR/GBP LONDON_WIDE FAIL (other pair + fade-to-open not NY-fade).
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
OUT = ROOT / "results" / "strateeg2_prescreen" / "cycle_0440"
RT = {
    "US30cash": 0.45,
    "US100cash": 0.66,
    "BTCUSD": 1.25,
    "USDCHF": 1.01,
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


def sim_wideopen_pb(g, atr_map):
    """Wide first-90m → pullback continuation."""
    if len(g) < 40:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None:
        return None
    b0 = bar_at(g, day0, 15, 30)
    if b0 is None:
        return None
    p_open = float(b0["open"])
    if p_open <= 0:
        return None
    morn = g[(g["time"] >= day0 + pd.Timedelta(hours=15, minutes=30)) &
             (g["time"] < day0 + pd.Timedelta(hours=17, minutes=0))]
    if len(morn) < 10:
        return None
    mhi, mlo = float(morn["high"].max()), float(morn["low"].min())
    mr = mhi - mlo
    if mr < 0.65 * atr or mr <= 0:
        return None
    # morning direction from open to 17:00 close
    b90 = bar_at(g, day0, 16, 55)
    if b90 is None:
        b90 = morn.iloc[-1]
    p90 = float(b90["close"])
    if p90 >= p_open:
        side = 1
        extreme = mhi
    else:
        side = -1
        extreme = mlo
    # pullback: after 17:00, wait until price retraces ≥35% of morning range toward open
    after = g[(g["time"] >= day0 + pd.Timedelta(hours=17, minutes=0)) &
              (g["time"] <= day0 + pd.Timedelta(hours=20, minutes=0))]
    if after.empty:
        return None
    entry = None
    entry_t = None
    thresh = 0.35 * mr
    for _, row in after.iterrows():
        px = float(row["close"])
        if side == 1:
            # long: need pullback down from extreme toward open by ≥35% of range
            if (extreme - px) >= thresh and px > p_open:
                entry, entry_t = px, row["time"]
                break
        else:
            if (px - extreme) >= thresh and px < p_open:
                entry, entry_t = px, row["time"]
                break
    if entry is None:
        return None
    # stop beyond open; target morning extreme
    if side == 1:
        stop = p_open - 0.10 * mr
        target = extreme
    else:
        stop = p_open + 0.10 * mr
        target = extreme
    trail = after[after["time"] > entry_t]
    flat_cut = day0 + pd.Timedelta(hours=20, minutes=0)
    trail = trail[trail["time"] <= flat_cut]
    walked = walk_exit(trail, side, stop, target)
    if walked is None:
        return None
    exit_px, reason = walked
    bruto = 1e4 * side * (exit_px - entry) / entry
    return dict(day=str(day0.date()), side=side, entry=entry, exit=exit_px, reason=reason, bruto_bp=bruto)


def sim_us30_lead(g100, atr100, day_us30_signal):
    """Trade US100 following US30 morning when US100 quiet."""
    if len(g100) < 30:
        return None
    day0 = g100["time"].dt.normalize().iloc[0]
    sig = day_us30_signal.get(day0)
    if sig is None:
        return None
    atr = atr100.get(day0)
    if atr is None:
        return None
    b0 = bar_at(g100, day0, 15, 30)
    b60 = bar_at(g100, day0, 16, 30)
    if b0 is None or b60 is None:
        return None
    p_open = float(b0["open"])
    p60 = float(b60["close"])
    if p_open <= 0:
        return None
    morn_bp = 1e4 * (p60 - p_open) / p_open
    atr_bp = 1e4 * atr / p_open
    if abs(morn_bp) >= 0.25 * atr_bp:
        return None  # US100 not quiet
    side = sig  # direction of US30
    entry = p60
    stop_dist = 0.35 * atr
    if side == 1:
        stop = entry - stop_dist
        target = entry + 0.55 * atr
    else:
        stop = entry + stop_dist
        target = entry - 0.55 * atr
    after = g100[(g100["time"] > day0 + pd.Timedelta(hours=16, minutes=30)) &
                 (g100["time"] <= day0 + pd.Timedelta(hours=19, minutes=0))]
    walked = walk_exit(after, side, stop, target)
    if walked is None:
        return None
    exit_px, reason = walked
    bruto = 1e4 * side * (exit_px - entry) / entry
    return dict(day=str(day0.date()), side=side, entry=entry, exit=exit_px, reason=reason, bruto_bp=bruto)


def build_us30_signals(df30, atr30):
    """US30 morning direction if |move| ≥ 0.40×ATR at 16:30."""
    out = {}
    for day0, g in df30.groupby(df30["time"].dt.normalize()):
        atr = atr30.get(day0)
        if atr is None:
            continue
        b0 = bar_at(g, day0, 15, 30)
        b60 = bar_at(g, day0, 16, 30)
        if b0 is None or b60 is None:
            continue
        p_open = float(b0["open"])
        p60 = float(b60["close"])
        if p_open <= 0:
            continue
        move = p60 - p_open
        if abs(move) < 0.40 * atr:
            continue
        out[day0] = 1 if move > 0 else -1
    return out


def sim_btc_asia_fade(g, atr_map):
    if len(g) < 40:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None:
        return None
    asia = g[(g["time"] >= day0 + pd.Timedelta(hours=0)) &
             (g["time"] < day0 + pd.Timedelta(hours=8))]
    if len(asia) < 20:
        return None
    ahi, alo = float(asia["high"].max()), float(asia["low"].min())
    ar = ahi - alo
    if ar < 0.80 * atr or ar <= 0:
        return None
    aclose = float(asia.iloc[-1]["close"])
    mid = 0.5 * (ahi + alo)
    # outer quartile
    q1 = alo + 0.25 * ar
    q3 = alo + 0.75 * ar
    if aclose >= q3:
        side = -1  # fade up
    elif aclose <= q1:
        side = 1
    else:
        return None
    b_entry = bar_at(g, day0, 9, 0)
    if b_entry is None:
        return None
    entry = float(b_entry["close"])
    if side == 1:
        stop = alo - 0.15 * ar
        target = mid
    else:
        stop = ahi + 0.15 * ar
        target = mid
    after = g[(g["time"] > day0 + pd.Timedelta(hours=9, minutes=0)) &
              (g["time"] <= day0 + pd.Timedelta(hours=13, minutes=0))]
    walked = walk_exit(after, side, stop, target)
    if walked is None:
        return None
    exit_px, reason = walked
    bruto = 1e4 * side * (exit_px - entry) / entry
    return dict(day=str(day0.date()), side=side, entry=entry, exit=exit_px, reason=reason, bruto_bp=bruto)


def sim_usdchf_london_fade(g, atr_map):
    if len(g) < 40:
        return None
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
    ext = entry - p_open
    if abs(ext) < 0.45 * atr:
        return None
    side = -1 if ext > 0 else 1  # fade
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
    bruto = 1e4 * side * (exit_px - entry) / entry
    return dict(day=str(day0.date()), side=side, entry=entry, exit=exit_px, reason=reason, bruto_bp=bruto)


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


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    results = []

    # A WIDEOPEN_PB pooled
    trades_a = []
    for sym in ("US30cash", "US100cash"):
        df = load_m5(sym)
        atr = d1_atr_map(df)
        for day0, g in df.groupby(df["time"].dt.normalize()):
            t = sim_wideopen_pb(g, atr)
            if t:
                t["symbol"] = sym
                trades_a.append(t)
        pd.DataFrame([t for t in trades_a if t["symbol"] == sym]).to_csv(OUT / f"WIDEOPEN_PB_{sym}_trades.csv", index=False)
    rt_a = float(np.mean([RT[t["symbol"]] for t in trades_a])) if trades_a else 0.555
    s_a = summarize("WIDEOPEN_PB_US30_US100", trades_a, rt_a)
    results.append(s_a)
    pd.DataFrame(trades_a).to_csv(OUT / "WIDEOPEN_PB_pooled_trades.csv", index=False)

    # B US30 lead US100
    df30 = load_m5("US30cash")
    atr30 = d1_atr_map(df30)
    sigs = build_us30_signals(df30, atr30)
    df100 = load_m5("US100cash")
    atr100 = d1_atr_map(df100)
    trades_b = []
    for day0, g in df100.groupby(df100["time"].dt.normalize()):
        t = sim_us30_lead(g, atr100, sigs)
        if t:
            t["symbol"] = "US100cash"
            trades_b.append(t)
    s_b = summarize("US30_LEAD_US100", trades_b, RT["US100cash"])
    results.append(s_b)
    pd.DataFrame(trades_b).to_csv(OUT / "US30_LEAD_US100_trades.csv", index=False)

    # C BTC Asia fade
    dfb = load_m5("BTCUSD")
    atrb = d1_atr_map(dfb)
    trades_c = []
    for day0, g in dfb.groupby(dfb["time"].dt.normalize()):
        t = sim_btc_asia_fade(g, atrb)
        if t:
            t["symbol"] = "BTCUSD"
            trades_c.append(t)
    s_c = summarize("BTC_ASIA_FADE", trades_c, RT["BTCUSD"])
    results.append(s_c)
    pd.DataFrame(trades_c).to_csv(OUT / "BTC_ASIA_FADE_trades.csv", index=False)

    # D USDCHF London fade
    dfc = load_m5("USDCHF")
    atrc = d1_atr_map(dfc)
    trades_d = []
    for day0, g in dfc.groupby(dfc["time"].dt.normalize()):
        t = sim_usdchf_london_fade(g, atrc)
        if t:
            t["symbol"] = "USDCHF"
            trades_d.append(t)
    s_d = summarize("USDCHF_LONDON_FADE", trades_d, RT["USDCHF"])
    results.append(s_d)
    pd.DataFrame(trades_d).to_csv(OUT / "USDCHF_LONDON_FADE_trades.csv", index=False)

    (OUT / "prescreen.json").write_text(json.dumps(results, indent=2))
    lines = ["# S2 D-092.1 cycle_0440", "", "| Idee | N | mean bruto | gate | outcome | skew |",
             "|------|--:|----------:|-----:|---------|------|"]
    for r in results:
        lines.append(
            f"| {r['idea']} | {r['n']} | {r['mean_bruto']} | {r['gate']} | **{r['outcome']}** | {r['skew']} |"
        )
    (OUT / "prescreen.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
