#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: Strateeg VOORSTEL N20–N23 (D-094 track 2/4).

Train 2021–2023 only. Reserve 2025+ untouched. No PREREG / no TRIALS.
Source: VOORSTEL_PRESCREEN_N20..N23 @ Strateeg f54ad28.
m5gz clock = Europe/Amsterdam wall (U2 AMS convention).
"""
from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n20_n23_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
ATR_N = 14
MIN_N = 150

# Gates from Strateeg VOORSTEL / COSTS_FTMO (3× RT or RT_effective).
N20_RT, N20_GATE = 0.45, 1.35   # US30cash
N21_RT, N21_GATE = 0.72, 2.16   # GER40cash
N22_RT, N22_GATE = 2.71, 8.13   # UKOILcash
N23_RT_EFF, N23_GATE = 4.56, 13.68  # US100cash: RT 0.66 + 2×swap_long 1.95


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


def bar_at(g: pd.DataFrame, day0, h, m=0):
    t = day0 + pd.Timedelta(hours=h, minutes=m)
    rows = g[g["time"] == t]
    return None if rows.empty else rows.iloc[0]


def bp_ret(entry, exit_px, side):
    return side * 1e4 * (exit_px - entry) / entry


def manage(g, day0, entry_t, entry, side, stop, flat_h, flat_m=0):
    flat_t = day0 + pd.Timedelta(hours=flat_h, minutes=flat_m)
    path = g[(g["time"] > entry_t) & (g["time"] <= flat_t)]
    exit_px = float(path.iloc[-1]["close"]) if len(path) else entry
    hit = "time"
    for _, row in path.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        if side == 1 and lo <= stop:
            return stop, "stop"
        if side == -1 and hi >= stop:
            return stop, "stop"
    return exit_px, hit


def sim_n20(g, atr_price):
    """US30 AM-trend → PM continuation 18:00→21:00 CET."""
    if not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b_open = bar_at(g, day0, 15, 30)
    b_1800 = bar_at(g, day0, 18, 0)
    if b_open is None or b_1800 is None:
        return None
    p_open = float(b_open["close"])
    p_1800 = float(b_1800["close"])
    if p_open <= 0:
        return None
    am_bp = 1e4 * (p_1800 - p_open) / p_open
    if am_bp >= 30.0:
        side = 1
    elif am_bp <= -30.0:
        side = -1
    else:
        return None
    entry = p_1800
    entry_t = b_1800["time"]
    stop = entry - side * atr_price
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 21, 0)
    return {
        "date": str(day0.date()),
        "side": side,
        "am_bp": round(am_bp, 4),
        "entry": entry,
        "exit": exit_px,
        "hit": hit,
        "atr": atr_price,
        "bruto_bp": bp_ret(entry, exit_px, side),
    }


def sim_n21(g, atr_price):
    """GER40 afternoon deviation fade 16:30→17:30 CET."""
    if not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b_open = bar_at(g, day0, 9, 0)
    b_1630 = bar_at(g, day0, 16, 30)
    if b_open is None or b_1630 is None:
        return None
    p_open = float(b_open["close"])
    p_1630 = float(b_1630["close"])
    if p_open <= 0:
        return None
    dev_bp = 1e4 * (p_1630 - p_open) / p_open
    if dev_bp >= 50.0:
        side = -1  # fade
    elif dev_bp <= -50.0:
        side = 1
    else:
        return None
    entry = p_1630
    entry_t = b_1630["time"]
    stop = entry - side * atr_price
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 17, 30)
    return {
        "date": str(day0.date()),
        "side": side,
        "dev_bp": round(dev_bp, 4),
        "entry": entry,
        "exit": exit_px,
        "hit": hit,
        "atr": atr_price,
        "bruto_bp": bp_ret(entry, exit_px, side),
    }


def sim_n22(g, atr_price):
    """UKOIL London-AM ±40 bp → fade 15:30→18:30 CET."""
    if not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b_open = bar_at(g, day0, 9, 0)
    b_1200 = bar_at(g, day0, 12, 0)
    b_1530 = bar_at(g, day0, 15, 30)
    if b_open is None or b_1200 is None or b_1530 is None:
        return None
    p_open = float(b_open["close"])
    p_1200 = float(b_1200["close"])
    if p_open <= 0:
        return None
    lon_bp = 1e4 * (p_1200 - p_open) / p_open
    if lon_bp >= 40.0:
        side = -1  # fade
    elif lon_bp <= -40.0:
        side = 1
    else:
        return None
    entry = float(b_1530["close"])
    entry_t = b_1530["time"]
    stop = entry - side * atr_price
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 18, 30)
    return {
        "date": str(day0.date()),
        "side": side,
        "lon_bp": round(lon_bp, 4),
        "entry": entry,
        "exit": exit_px,
        "hit": hit,
        "atr": atr_price,
        "bruto_bp": bp_ret(entry, exit_px, side),
    }


def d1_from_m5(m5: pd.DataFrame) -> pd.DataFrame:
    """Resample M5 → D1 close: prefer 22:00 CET bar, else last bar of calendar day."""
    rows = []
    for day, g in m5.groupby(m5["time"].dt.normalize()):
        g = g.sort_values("time")
        b22 = g[g["time"] == day + pd.Timedelta(hours=22)]
        if not b22.empty:
            close = float(b22.iloc[0]["close"])
            t = b22.iloc[0]["time"]
        else:
            close = float(g.iloc[-1]["close"])
            t = g.iloc[-1]["time"]
        hi = float(g["high"].max())
        lo = float(g["low"].min())
        op = float(g.iloc[0]["open"])
        rows.append({"date": day, "time": t, "open": op, "high": hi, "low": lo, "close": close})
    return pd.DataFrame(rows).sort_values("date").reset_index(drop=True)


def sim_n23(d1: pd.DataFrame):
    """US100 2d TSMOM non-overlapping; no stop; exit close_{t+2}."""
    d1 = d1.copy()
    d1["ret20"] = d1["close"] / d1["close"].shift(20) - 1.0
    trades = []
    i = 20  # need ret20
    n = len(d1)
    while i < n - 2:
        ret20 = float(d1.iloc[i]["ret20"])
        if not (ret20 == ret20) or ret20 == 0.0:
            i += 1
            continue
        side = 1 if ret20 > 0 else -1
        entry = float(d1.iloc[i]["close"])
        exit_px = float(d1.iloc[i + 2]["close"])
        if entry <= 0:
            i += 1
            continue
        trades.append(
            {
                "date": str(d1.iloc[i]["date"].date()),
                "exit_date": str(d1.iloc[i + 2]["date"].date()),
                "side": side,
                "ret20": round(ret20, 6),
                "entry": entry,
                "exit": exit_px,
                "hit": "time",
                "bruto_bp": bp_ret(entry, exit_px, side),
            }
        )
        i += 2  # non-overlap: wait until exit before new entry
    return trades


def summarize(idea, trades, rt, gate, extra=None):
    base = {
        "idea": idea,
        "rt_bp": rt,
        "gate_3x_rt": gate,
        "reserve_2025": "untouched",
    }
    if extra:
        base.update(extra)
    if not trades:
        base.update(
            {
                "n": 0,
                "mean_bruto_bp": None,
                "pass_gate": False,
                "n_ok": False,
                "pass": False,
                "decision": "NO_PREREG_screen_fail_empty",
            }
        )
        return base
    arr = np.array([t["bruto_bp"] for t in trades], float)
    mean = float(arr.mean())
    n = len(arr)
    gate_ok = mean >= gate
    n_ok = n >= MIN_N
    if not gate_ok:
        decision = "NO_PREREG_screen_fail"
    elif not n_ok:
        decision = "NO_PREREG_underpowered"
    else:
        decision = "PASS_may_PREREG"
    sides = np.array([t["side"] for t in trades])
    long_m = float(arr[sides == 1].mean()) if (sides == 1).any() else None
    short_m = float(arr[sides == -1].mean()) if (sides == -1).any() else None
    base.update(
        {
            "n": n,
            "n_long": int((sides == 1).sum()),
            "n_short": int((sides == -1).sum()),
            "mean_bruto_bp": round(mean, 4),
            "mean_bruto_long_bp": None if long_m is None else round(long_m, 4),
            "mean_bruto_short_bp": None if short_m is None else round(short_m, 4),
            "median_bruto_bp": round(float(np.median(arr)), 4),
            "p25": round(float(np.percentile(arr, 25)), 4),
            "p75": round(float(np.percentile(arr, 75)), 4),
            "stop_share": round(float(np.mean([t.get("hit") == "stop" for t in trades])), 4),
            "pass_gate": bool(gate_ok),
            "n_ok": bool(n_ok),
            "pass": bool(gate_ok and n_ok),
            "date_min": trades[0]["date"],
            "date_max": trades[-1]["date"],
            "decision": decision,
        }
    )
    return base


def lab(s):
    if s["pass"]:
        return "PASS"
    if s.get("pass_gate") and not s.get("n_ok"):
        return "FAIL_N (underpowered)"
    return "FAIL"


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    us30 = load_m5("data/m5gz/US30cash.csv.gz")
    ger = load_m5("data/m5gz/GER40cash.csv.gz")
    ukoil = load_m5("data/m5gz/UKOILcash.csv.gz")
    us100 = load_m5("data/m5gz/US100cash.csv.gz")

    atr_us30 = atr_map(us30)
    atr_ger = atr_map(ger)
    atr_ukoil = atr_map(ukoil)

    n20, n21, n22 = [], [], []
    for day, g in us30.groupby(us30["time"].dt.normalize()):
        t = sim_n20(g.sort_values("time"), prior_atr(atr_us30, day))
        if t:
            n20.append(t)
    for day, g in ger.groupby(ger["time"].dt.normalize()):
        t = sim_n21(g.sort_values("time"), prior_atr(atr_ger, day))
        if t:
            n21.append(t)
    for day, g in ukoil.groupby(ukoil["time"].dt.normalize()):
        t = sim_n22(g.sort_values("time"), prior_atr(atr_ukoil, day))
        if t:
            n22.append(t)

    d1 = d1_from_m5(us100)
    n23 = sim_n23(d1)

    s20 = summarize("N20_US30_AM_PM_CONT", n20, N20_RT, N20_GATE)
    s21 = summarize("N21_GER40_DEV_FADE", n21, N21_RT, N21_GATE)
    s22 = summarize("N22_UKOIL_LON_AM_FADE", n22, N22_RT, N22_GATE)
    s23 = summarize(
        "N23_US100_2D_TSMOM",
        n23,
        N23_RT_EFF,
        N23_GATE,
        extra={"note": "gate uses RT_eff=RT+2*swap_long; bruto unadjusted; non-overlap"},
    )

    board = {
        "n20": s20,
        "n21": s21,
        "n22": s22,
        "n23": s23,
        "source": "VOORSTEL_PRESCREEN_N20..N23 @ f54ad28",
        "min_n": MIN_N,
        "train": "2021-01-01 .. 2023-12-31",
        "reserve_2025": "untouched",
        "no_prereg_written": True,
    }

    pd.DataFrame(n20).to_csv(OUT / "n20_trades_train.csv", index=False)
    pd.DataFrame(n21).to_csv(OUT / "n21_trades_train.csv", index=False)
    pd.DataFrame(n22).to_csv(OUT / "n22_trades_train.csv", index=False)
    pd.DataFrame(n23).to_csv(OUT / "n23_trades_train.csv", index=False)
    d1.to_csv(OUT / "n23_d1_resample_train.csv", index=False)
    (OUT / "prescreen.json").write_text(json.dumps(board, indent=2) + "\n")

    md = [
        "# D-092.1 U2 pre-screen — N20–N23 (train 2021–2023)",
        "",
        "Source: Strateeg `VOORSTEL_PRESCREEN_N20..N23` @ `f54ad28` (D-094).",
        "Reserve 2025+ untouched. No TRIALS. No PREREG written by U2 (Strateeg on PASS).",
        f"PASS = mean bruto ≥ gate **and** N≥{MIN_N} → `PASS_may_PREREG`.",
        "",
        "| Idee | Instrument | N | mean bruto | gate | Uitkomst | decision |",
        "|------|------------|---|------------|------|----------|----------|",
        f"| N20 AM→PM cont | US30cash | {s20['n']} | {s20['mean_bruto_bp']} bp | {N20_GATE} bp | **{lab(s20)}** | `{s20['decision']}` |",
        f"| N21 afternoon fade | GER40cash | {s21['n']} | {s21['mean_bruto_bp']} bp | {N21_GATE} bp | **{lab(s21)}** | `{s21['decision']}` |",
        f"| N22 London-AM fade | UKOILcash | {s22['n']} | {s22['mean_bruto_bp']} bp | {N22_GATE} bp | **{lab(s22)}** | `{s22['decision']}` |",
        f"| N23 2d TSMOM | US100cash | {s23['n']} | {s23['mean_bruto_bp']} bp | {N23_GATE} bp | **{lab(s23)}** | `{s23['decision']}` |",
        "",
        "### Side split (esp. N23)",
        f"- N20 long/short mean: {s20.get('mean_bruto_long_bp')} / {s20.get('mean_bruto_short_bp')} (n={s20.get('n_long')}/{s20.get('n_short')})",
        f"- N21 long/short mean: {s21.get('mean_bruto_long_bp')} / {s21.get('mean_bruto_short_bp')} (n={s21.get('n_long')}/{s21.get('n_short')})",
        f"- N22 long/short mean: {s22.get('mean_bruto_long_bp')} / {s22.get('mean_bruto_short_bp')} (n={s22.get('n_long')}/{s22.get('n_short')})",
        f"- N23 long/short mean: {s23.get('mean_bruto_long_bp')} / {s23.get('mean_bruto_short_bp')} (n={s23.get('n_long')}/{s23.get('n_short')})",
        "",
        "### Notes",
        "- N20–N22: stop = 1.0×ATR14 (prior day); swap=0 (intraday flat).",
        "- N23: pure close-to-close 2d; non-overlapping; gate RT_eff = 0.66+2×1.95 = 4.56 → 13.68 bp; bruto unadjusted.",
        "- D-094a: train 2021–23 as specified by Strateeg; reason (b) deferred to PREREG if PASS.",
        "",
    ]
    (OUT / "prescreen.md").write_text("\n".join(md) + "\n")
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
