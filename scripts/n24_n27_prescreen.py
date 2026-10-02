#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: Strateeg VOORSTEL N24–N27 (D-094 track 2/4).

Train 2021–2023 only. Reserve 2025+ untouched. No PREREG / no TRIALS.
Source: VOORSTEL_PRESCREEN_N24..N27 @ Strateeg b6e8c1e.
m5gz clock = Europe/Amsterdam wall (U2 AMS convention).
"""
from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n24_n27_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
ATR_N = 14
MIN_N = 150

# Gates from Strateeg VOORSTEL / COSTS_FTMO (3× RT).
N24_RT, N24_GATE = 0.78, 2.34   # US500cash
N25_RT, N25_GATE = 0.83, 2.49   # XAUUSD
N26_RT, N26_GATE = 1.61, 4.83   # worst-case pair XAU+US500
N27_RT, N27_GATE = 1.22, 3.66   # AUDUSD


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


def manage(g, day0, entry_t, entry, side, stop, flat_h, flat_m=0, use_stop=True):
    flat_t = day0 + pd.Timedelta(hours=flat_h, minutes=flat_m)
    path = g[(g["time"] > entry_t) & (g["time"] <= flat_t)]
    exit_px = float(path.iloc[-1]["close"]) if len(path) else entry
    hit = "time"
    if use_stop and stop == stop:
        for _, row in path.iterrows():
            hi, lo = float(row["high"]), float(row["low"])
            if side == 1 and lo <= stop:
                return stop, "stop"
            if side == -1 and hi >= stop:
                return stop, "stop"
    return exit_px, hit


def sim_n24(g, atr_price):
    """US500 AM impulse 15:30→18:00 ≥±40 bp → fade 18:00→20:30 CET."""
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
    if am_bp >= 40.0:
        side = -1  # fade
    elif am_bp <= -40.0:
        side = 1
    else:
        return None
    entry = p_1800
    entry_t = b_1800["time"]
    stop = entry - side * atr_price
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 20, 30)
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


def sim_n25(g, atr_price):
    """XAU NY-open deviation at 18:00 ≥±35 bp → fade 18:00→20:30 CET."""
    if not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b_ny = bar_at(g, day0, 15, 30)
    b_1800 = bar_at(g, day0, 18, 0)
    if b_ny is None or b_1800 is None:
        return None
    p_ny = float(b_ny["close"])
    p_1800 = float(b_1800["close"])
    if p_ny <= 0:
        return None
    dev_bp = 1e4 * (p_1800 - p_ny) / p_ny
    if dev_bp >= 35.0:
        side = -1
    elif dev_bp <= -35.0:
        side = 1
    else:
        return None
    entry = p_1800
    entry_t = b_1800["time"]
    stop = entry - side * atr_price
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 20, 30)
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


def day_close_2200(m5: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for day, g in m5.groupby(m5["time"].dt.normalize()):
        g = g.sort_values("time")
        b22 = g[g["time"] == day + pd.Timedelta(hours=22)]
        if not b22.empty:
            close = float(b22.iloc[0]["close"])
        else:
            close = float(g.iloc[-1]["close"])
        rows.append({"date": day, "close": close})
    return pd.DataFrame(rows).sort_values("date").reset_index(drop=True)


def bar_map(m5: pd.DataFrame) -> dict:
    """time -> (open,high,low,close) for exact timestamps."""
    out = {}
    for _, r in m5.iterrows():
        out[r["time"]] = (float(r["open"]), float(r["high"]), float(r["low"]), float(r["close"]))
    return out


def sim_n26(closes: dict[str, pd.DataFrame], maps: dict[str, dict]):
    """XS 1d reversal: long prev-day loser / short winner; 15:30→17:25 CET equal-weight."""
    symbols = sorted(closes.keys())
    # Align on calendar union
    all_dates = sorted(set().union(*[set(df["date"]) for df in closes.values()]))
    close_by = {s: dict(zip(df["date"], df["close"])) for s, df in closes.items()}
    trades = []
    for i in range(2, len(all_dates)):
        d_tm2 = all_dates[i - 2]
        d_tm1 = all_dates[i - 1]
        d_t = all_dates[i]
        rets = {}
        ok = True
        for s in symbols:
            c1 = close_by[s].get(d_tm1)
            c0 = close_by[s].get(d_tm2)
            if c1 is None or c0 is None or c0 <= 0:
                ok = False
                break
            rets[s] = 1e4 * (c1 - c0) / c0
        if not ok or len(rets) < 5:
            continue
        # unique ranks
        ranked = sorted(rets.items(), key=lambda x: x[1])
        if ranked[0][1] == ranked[1][1] or ranked[-1][1] == ranked[-2][1]:
            continue
        long_sym = ranked[0][0]
        short_sym = ranked[-1][0]
        if long_sym == short_sym:
            continue
        t_entry = d_t + pd.Timedelta(hours=15, minutes=30)
        t_exit = d_t + pd.Timedelta(hours=17, minutes=25)
        e_l = maps[long_sym].get(t_entry)
        x_l = maps[long_sym].get(t_exit)
        e_s = maps[short_sym].get(t_entry)
        x_s = maps[short_sym].get(t_exit)
        if None in (e_l, x_l, e_s, x_s):
            continue
        entry_l, exit_l = e_l[3], x_l[3]
        entry_s, exit_s = e_s[3], x_s[3]
        if entry_l <= 0 or entry_s <= 0:
            continue
        long_bp = bp_ret(entry_l, exit_l, 1)
        short_bp = bp_ret(entry_s, exit_s, -1)
        combined = 0.5 * (long_bp + short_bp)
        trades.append(
            {
                "date": str(d_t.date()),
                "long_sym": long_sym,
                "short_sym": short_sym,
                "ret_long_prev": round(rets[long_sym], 4),
                "ret_short_prev": round(rets[short_sym], 4),
                "long_bp": long_bp,
                "short_bp": short_bp,
                "bruto_bp": combined,
                "hit": "time",
            }
        )
    return trades


def h4_from_m5(m5: pd.DataFrame) -> pd.DataFrame:
    """CET-aligned H4: buckets 00/04/08/12/16/20."""
    x = m5.copy()
    x = x.set_index("time")
    # floor to 4h
    h4 = x.resample("4h", label="left", closed="left").agg(
        {"open": "first", "high": "max", "low": "min", "close": "last"}
    ).dropna()
    h4 = h4.reset_index()
    # keep only CET-aligned hours
    h4 = h4[h4["time"].dt.hour.isin([0, 4, 8, 12, 16, 20])].reset_index(drop=True)
    return h4


def sim_n27(h4: pd.DataFrame):
    """AUDUSD H4 MR: |dev| vs SMA20 ≥40 bp at 12:00 → fade; exit 16:00 close. Pure hold."""
    h4 = h4.copy()
    h4["sma20"] = h4["close"].rolling(20).mean()
    trades = []
    # index by time for exit lookup
    by_t = {r["time"]: r for _, r in h4.iterrows()}
    for _, r in h4.iterrows():
        if r["time"].hour != 12:
            continue
        sma = r["sma20"]
        if not (sma == sma) or sma <= 0:
            continue
        close = float(r["close"])
        dev_bp = 1e4 * (close - sma) / sma
        if dev_bp >= 40.0:
            side = -1
        elif dev_bp <= -40.0:
            side = 1
        else:
            continue
        exit_t = r["time"] + pd.Timedelta(hours=4)
        ex = by_t.get(exit_t)
        if ex is None:
            continue
        # train window filter on entry date
        if r["time"] < TRAIN_START or r["time"] > TRAIN_END:
            continue
        exit_px = float(ex["close"])
        trades.append(
            {
                "date": str(r["time"].date()),
                "side": side,
                "dev_bp": round(dev_bp, 4),
                "entry": close,
                "exit": exit_px,
                "sma20": float(sma),
                "hit": "time",
                "bruto_bp": bp_ret(close, exit_px, side),
            }
        )
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
                "median_bruto_bp": None,
                "pass_gate": False,
                "n_ok": False,
                "pass": False,
                "decision": "NO_PREREG_screen_fail_empty",
            }
        )
        return base
    arr = np.array([t["bruto_bp"] for t in trades], float)
    mean = float(arr.mean())
    med = float(np.median(arr))
    n = int(len(arr))
    n_ok = n >= MIN_N
    pass_gate = mean >= gate
    ok = n_ok and pass_gate
    base.update(
        {
            "n": n,
            "mean_bruto_bp": round(mean, 4),
            "median_bruto_bp": round(med, 4),
            "pass_gate": pass_gate,
            "n_ok": n_ok,
            "pass": ok,
            "decision": "PASS_may_PREREG" if ok else "NO_PREREG_screen_fail",
            "date_min": trades[0]["date"],
            "date_max": trades[-1]["date"],
            "side_long_n": int(sum(1 for t in trades if t.get("side", 0) == 1)),
            "side_short_n": int(sum(1 for t in trades if t.get("side", 0) == -1)),
            "stop_hits": int(sum(1 for t in trades if t.get("hit") == "stop")),
        }
    )
    return base


def run_day_loop(m5, atr, sim_fn):
    trades = []
    for day, g in m5.groupby(m5["time"].dt.normalize()):
        g = g.sort_values("time")
        a = prior_atr(atr, day)
        tr = sim_fn(g, a)
        if tr is not None:
            trades.append(tr)
    return trades


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    results = []

    # N24 US500
    print("N24 US500cash…", flush=True)
    m24 = load_m5("data/m5gz/US500cash.csv.gz")
    a24 = atr_map(m24)
    t24 = run_day_loop(m24, a24, sim_n24)
    pd.DataFrame(t24).to_csv(OUT / "n24_trades_train.csv", index=False)
    r24 = summarize("N24", t24, N24_RT, N24_GATE, {"symbol": "US500cash", "track": 2})
    results.append(r24)
    print(r24, flush=True)

    # N25 XAU
    print("N25 XAUUSD…", flush=True)
    m25 = load_m5("data/m5gz/XAUUSD.csv.gz")
    a25 = atr_map(m25)
    t25 = run_day_loop(m25, a25, sim_n25)
    pd.DataFrame(t25).to_csv(OUT / "n25_trades_train.csv", index=False)
    r25 = summarize("N25", t25, N25_RT, N25_GATE, {"symbol": "XAUUSD", "track": 2})
    results.append(r25)
    print(r25, flush=True)

    # N26 XS basket
    print("N26 XS basket…", flush=True)
    pool = ["US100cash", "US30cash", "US500cash", "GER40cash", "XAUUSD"]
    closes = {}
    maps = {}
    for s in pool:
        m = load_m5(f"data/m5gz/{s}.csv.gz")
        closes[s] = day_close_2200(m)
        maps[s] = bar_map(m)
        print(f"  loaded {s} bars={len(m)}", flush=True)
    t26 = sim_n26(closes, maps)
    pd.DataFrame(t26).to_csv(OUT / "n26_trades_train.csv", index=False)
    r26 = summarize(
        "N26",
        t26,
        N26_RT,
        N26_GATE,
        {"symbol": "+".join(pool), "track": 4, "pnl_def": "0.5*(long_bp+short_bp)"},
    )
    results.append(r26)
    print(r26, flush=True)

    # N27 AUDUSD H4
    print("N27 AUDUSD H4…", flush=True)
    # Need SMA warm-up: load a bit more history before train for SMA20, then filter trades
    path = ROOT / "data/m5gz/AUDUSD.csv.gz"
    with gzip.open(path, "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna().sort_values("time")
    # warm-up from 2020-10 for SMA20 on H4 (~20*4h)
    warm = df[(df["time"] >= pd.Timestamp("2020-10-01")) & (df["time"] <= TRAIN_END)].reset_index(drop=True)
    h4 = h4_from_m5(warm)
    t27 = sim_n27(h4)
    # ensure train-only (sim already filters)
    t27 = [t for t in t27 if TRAIN_START.date().isoformat() <= t["date"] <= "2023-12-31"]
    pd.DataFrame(t27).to_csv(OUT / "n27_trades_train.csv", index=False)
    r27 = summarize("N27", t27, N27_RT, N27_GATE, {"symbol": "AUDUSD", "track": 4, "tf": "H4"})
    results.append(r27)
    print(r27, flush=True)

    summary = {
        "source_strateeg": "b6e8c1e",
        "window": "2021-01-01..2023-12-31",
        "reserve_2025": "untouched",
        "results": results,
    }
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [
        "# N24–N27 D-092.1 train pre-screen (2021–2023)",
        "",
        f"Source Strateeg `b6e8c1e`. Reserve 2025→ untouched. No PREREG/TRIALS.",
        "",
        "| Idea | N | mean bruto | gate | decision |",
        "|------|---|------------|------|----------|",
    ]
    for r in results:
        lines.append(
            f"| {r['idea']} | {r['n']} | {r.get('mean_bruto_bp')} | {r['gate_3x_rt']} | **{r['decision']}** |"
        )
    (OUT / "prescreen.md").write_text("\n".join(lines) + "\n")
    print("DONE", json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
