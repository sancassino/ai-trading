#!/usr/bin/env python3
"""D-092.1 free pre-screen: Strateeg VOORSTEL N9 (GER40 Ochtend-Fade → XETRA-open)
and N10 (XAU Mid-London Fade → AM-Fix).

Train 2021-01-01 .. 2023-12-31 only. Reserve 2025+ untouched.
No PREREG / no TRIALS — FAIL → no PREREG; PASS → Strateeg may freeze PREREG.

Source: VOORSTEL_PRESCREEN_N9.md / N10.md @ Strateeg bbcd232.
m5gz clock = Europe/Amsterdam wall (U2 AMS convention).
"""
from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
ATR_N = 14
OUT = ROOT / "results/cto/n9_n10_prescreen"

# VOORSTEL gates (Strateeg stated). Also report COSTS_FTMO 3×RT for GER40.
N9_RT_VOORSTEL = 1.40  # Strateeg stated → gate 4.20
N9_GATE_VOORSTEL = 3.0 * N9_RT_VOORSTEL
N9_RT_COSTS = 0.72  # COSTS_FTMO.csv roundtrip_intraday_bp
N9_GATE_COSTS = 3.0 * N9_RT_COSTS
N10_RT = 0.83
N10_GATE = 3.0 * N10_RT  # 2.49


def load_m5(rel: str) -> pd.DataFrame:
    path = ROOT / rel
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


def bp_ret(entry: float, exit_px: float, side: int) -> float:
    return side * 1e4 * (exit_px - entry) / entry


def bar_at(g: pd.DataFrame, day0: pd.Timestamp, h: int, m: int = 0):
    t = day0 + pd.Timedelta(hours=h, minutes=m)
    rows = g[g["time"] == t]
    if rows.empty:
        return None
    return rows.iloc[0]


def first_bar_at_or_after(g: pd.DataFrame, day0: pd.Timestamp, h: int, m: int = 0):
    t = day0 + pd.Timedelta(hours=h, minutes=m)
    rows = g[g["time"] >= t]
    if rows.empty:
        return None
    # stay on same day, within 30 min of target
    row = rows.iloc[0]
    if row["time"].normalize() != day0:
        return None
    if row["time"] > t + pd.Timedelta(minutes=30):
        return None
    return row


def sim_n9_day(g: pd.DataFrame, atr_price: float):
    """GER40 Ochtend-Fade naar XETRA-Open (VOORSTEL_N9)."""
    if not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b_open = first_bar_at_or_after(g, day0, 9, 0)
    b_entry = bar_at(g, day0, 10, 30)
    if b_open is None or b_entry is None:
        return None
    p_open = float(b_open["open"])
    if p_open <= 0:
        return None
    p_entry = float(b_entry["close"])
    morn_bp = 1e4 * (p_entry - p_open) / p_open
    atr_bp = 1e4 * atr_price / p_open
    thr = 0.40 * atr_bp
    if morn_bp >= thr:
        side = -1  # SHORT fade
    elif morn_bp <= -thr:
        side = 1  # LONG fade
    else:
        return None

    morn = g[
        (g["time"] >= day0 + pd.Timedelta(hours=9))
        & (g["time"] <= day0 + pd.Timedelta(hours=10, minutes=30))
    ]
    if morn.empty:
        return None
    morn_hi = float(morn["high"].max())
    morn_lo = float(morn["low"].min())
    morn_rng = morn_hi - morn_lo
    if morn_rng <= 0:
        return None
    buf = 0.15 * morn_rng
    # stop beyond morning extreme + buffer
    if side == -1:  # short: stop above morn high
        stop = morn_hi + buf
    else:  # long: stop below morn low
        stop = morn_lo - buf

    target = p_open
    entry_t = b_entry["time"]
    after = g[(g["time"] > entry_t) & (g["time"] <= day0 + pd.Timedelta(hours=12))]
    exit_px = float(after.iloc[-1]["close"]) if len(after) else p_entry
    hit = "time"
    for _, row in after.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        if side == 1:
            if lo <= stop:
                exit_px, hit = stop, "stop"
                break
            if hi >= target:
                exit_px, hit = target, "target"
                break
        else:
            if hi >= stop:
                exit_px, hit = stop, "stop"
                break
            if lo <= target:
                exit_px, hit = target, "target"
                break

    return {
        "date": str(day0.date()),
        "side": side,
        "entry": p_entry,
        "exit": exit_px,
        "hit": hit,
        "morn_bp": round(morn_bp, 4),
        "atr_bp": round(atr_bp, 4),
        "thr_bp": round(thr, 4),
        "bruto_bp": bp_ret(p_entry, exit_px, side),
    }


def sim_n10_day(g: pd.DataFrame, atr_price: float):
    """XAU Mid-London Fade naar AM-Fix (VOORSTEL_N10)."""
    if not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b_am = bar_at(g, day0, 10, 30)
    b_entry = bar_at(g, day0, 12, 0)
    if b_am is None or b_entry is None:
        return None
    p_am = float(b_am["close"])
    p_entry = float(b_entry["close"])
    if p_am <= 0:
        return None
    mid_bp = 1e4 * (p_entry - p_am) / p_am
    if mid_bp >= 20.0:
        side = -1
    elif mid_bp <= -20.0:
        side = 1
    else:
        return None

    entry = p_entry
    entry_t = b_entry["time"]
    stop = entry - side * atr_price  # 1.0 × ATR14 daily from entry
    target = p_am
    after = g[(g["time"] > entry_t) & (g["time"] <= day0 + pd.Timedelta(hours=14, minutes=30))]
    exit_px = float(after.iloc[-1]["close"]) if len(after) else entry
    hit = "time"
    for _, row in after.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        if side == 1:
            if lo <= stop:
                exit_px, hit = stop, "stop"
                break
            if hi >= target:
                exit_px, hit = target, "target"
                break
        else:
            if hi >= stop:
                exit_px, hit = stop, "stop"
                break
            if lo <= target:
                exit_px, hit = target, "target"
                break

    return {
        "date": str(day0.date()),
        "side": side,
        "entry": entry,
        "exit": exit_px,
        "hit": hit,
        "mid_bp": round(mid_bp, 4),
        "atr": atr_price,
        "bruto_bp": bp_ret(entry, exit_px, side),
    }


def summarize(idea: str, trades: list[dict], rt: float, gate: float) -> dict:
    if not trades:
        return {
            "idea": idea,
            "n": 0,
            "mean_bruto_bp": None,
            "rt_bp": rt,
            "gate_3x_rt": gate,
            "pass": False,
            "decision": "NO_PREREG_screen_fail_empty",
        }
    arr = np.array([t["bruto_bp"] for t in trades], dtype=float)
    mean = float(arr.mean())
    ok = mean >= gate
    return {
        "idea": idea,
        "n": int(len(arr)),
        "mean_bruto_bp": round(mean, 4),
        "median_bruto_bp": round(float(np.median(arr)), 4),
        "p25": round(float(np.percentile(arr, 25)), 4),
        "p75": round(float(np.percentile(arr, 75)), 4),
        "stop_share": round(float(np.mean([t["hit"] == "stop" for t in trades])), 4),
        "target_share": round(float(np.mean([t["hit"] == "target" for t in trades])), 4),
        "rt_bp": rt,
        "gate_3x_rt": gate,
        "pass": bool(ok),
        "date_min": trades[0]["date"],
        "date_max": trades[-1]["date"],
        "decision": "PASS_may_PREREG" if ok else "NO_PREREG_screen_fail",
        "reserve_2025": "untouched",
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # --- N9 GER40 ---
    ger = load_m5("data/m5gz/GER40cash.csv.gz")
    atr_g = atr_map(ger)
    n9 = []
    for day, g in ger.groupby(ger["time"].dt.normalize()):
        g = g.sort_values("time")
        a = prior_atr(atr_g, day)
        t = sim_n9_day(g, a)
        if t:
            n9.append(t)

    s9_v = summarize("N9_GER40_OCHTEND_FADE", n9, N9_RT_VOORSTEL, N9_GATE_VOORSTEL)
    s9_c = summarize("N9_GER40_OCHTEND_FADE_costsRT", n9, N9_RT_COSTS, N9_GATE_COSTS)
    # Binding decision uses VOORSTEL gate (stricter / stated by Strateeg).
    # If VOORSTEL FAIL but COSTS PASS → still NO_PREREG under stated gate;
    # note sensitivity for Manager/CEO.

    # --- N10 XAU ---
    xau = load_m5("data/m5gz/XAUUSD.csv.gz")
    atr_x = atr_map(xau)
    n10 = []
    for day, g in xau.groupby(xau["time"].dt.normalize()):
        g = g.sort_values("time")
        a = prior_atr(atr_x, day)
        t = sim_n10_day(g, a)
        if t:
            n10.append(t)

    s10 = summarize("N10_XAU_MIDLONDON_FADE", n10, N10_RT, N10_GATE)

    board = {
        "n9": s9_v,
        "n9_costs_rt_sensitivity": s9_c,
        "n10": s10,
        "source": "VOORSTEL_PRESCREEN_N9/N10 @ bbcd232",
        "binding_gates": {
            "n9": N9_GATE_VOORSTEL,
            "n9_note": "Strateeg VOORSTEL RT=1.40→4.20 (matches N6 GER40 convention); COSTS_FTMO RT=0.72→2.16 reported as sensitivity only",
            "n10": N10_GATE,
        },
        "reserve_2025": "untouched",
    }

    pd.DataFrame(n9).to_csv(OUT / "n9_trades_train.csv", index=False)
    pd.DataFrame(n10).to_csv(OUT / "n10_trades_train.csv", index=False)
    (OUT / "prescreen.json").write_text(json.dumps(board, indent=2) + "\n")

    md = [
        "# D-092.1 CTO pre-screen — N9 / N10 (train 2021–2023)",
        "",
        "Source: Strateeg `VOORSTEL_PRESCREEN_N9.md` / `N10.md` @ `bbcd232`.",
        f"Data: `data/m5gz/GER40cash.csv.gz`, `data/m5gz/XAUUSD.csv.gz`.",
        "Reserve 2025+ untouched. No TRIALS. No PREREG claimed by this screen.",
        "",
        "| Idee | N | mean bruto | gate | Uitkomst |",
        "|------|---|------------|------|----------|",
        f"| N9 GER40 Ochtend-Fade (VOORSTEL gate) | {s9_v['n']} | {s9_v['mean_bruto_bp']} bp | {N9_GATE_VOORSTEL} bp | **{'PASS' if s9_v['pass'] else 'FAIL'}** |",
        f"| N9 GER40 (COSTS RT sens.) | {s9_c['n']} | {s9_c['mean_bruto_bp']} bp | {N9_GATE_COSTS} bp | **{'PASS' if s9_c['pass'] else 'FAIL'}** (sens.) |",
        f"| N10 XAU Mid-London Fade | {s10['n']} | {s10['mean_bruto_bp']} bp | {N10_GATE} bp | **{'PASS' if s10['pass'] else 'FAIL'}** |",
        "",
        f"- N9 binding decision (VOORSTEL gate 4.20): `{s9_v['decision']}`",
        f"- N9 COSTS sensitivity (gate 2.16): `{s9_c['decision']}`",
        f"- N10 decision: `{s10['decision']}`",
        "",
    ]
    (OUT / "prescreen.md").write_text("\n".join(md) + "\n")
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
