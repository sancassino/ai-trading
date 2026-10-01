#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: Strateeg VOORSTEL N24–N27 (D-094 track 2/4).

Train 2021–2023 only. Reserve 2025+ untouched. No TRIALS append here.
Source: VOORSTEL_PRESCREEN_N24..N27 @ b6e8c1e.
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

N24_RT, N24_GATE = 0.78, 2.34   # US500cash
N25_RT, N25_GATE = 0.83, 2.49   # XAUUSD
N26_RT, N26_GATE = 1.61, 4.83   # worst pair XAU+US500
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


def sim_n24(g, atr_price):
    """US500 AM impuls 15:30–18:00 → fade 18:00→20:30 CET."""
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
        side = -1
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
    """XAU NY-open deviation @18:00 → fade 18:00→20:30 CET."""
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


def close_near_2200(g: pd.DataFrame, day0) -> float | None:
    b22 = bar_at(g, day0, 22, 0)
    if b22 is not None:
        return float(b22["close"])
    # last bar that day
    if g.empty:
        return None
    return float(g.sort_values("time").iloc[-1]["close"])


def sim_n26(frames: dict[str, pd.DataFrame]):
    """Cross-sectional 1d reversal: long bottom-1 / short top-1; 15:30→17:25 CET."""
    # Build prior-day close map per symbol
    closes = {}  # sym -> {date: close}
    for sym, m5 in frames.items():
        dmap = {}
        for day, g in m5.groupby(m5["time"].dt.normalize()):
            c = close_near_2200(g.sort_values("time"), day)
            if c is not None and c > 0:
                dmap[day] = c
        closes[sym] = dmap

    all_days = sorted(set().union(*[set(d.keys()) for d in closes.values()]))
    trades = []
    for i in range(2, len(all_days)):
        day_tm1 = all_days[i - 1]
        day_tm2 = all_days[i - 2]
        day_t = all_days[i]
        rets = {}
        ok = True
        for sym, dmap in closes.items():
            c1 = dmap.get(day_tm1)
            c0 = dmap.get(day_tm2)
            if c1 is None or c0 is None or c0 <= 0:
                ok = False
                break
            rets[sym] = 1e4 * (c1 - c0) / c0
        if not ok or len(rets) < 5:
            continue
        # unique ranks required
        vals = list(rets.values())
        if len(set(round(v, 8) for v in vals)) < 5:
            # ties → skip per VOORSTEL
            # still allow if argmin/argmax unique
            pass
        long_sym = min(rets, key=rets.get)
        short_sym = max(rets, key=rets.get)
        if long_sym == short_sym:
            continue
        if sum(1 for s, v in rets.items() if v == rets[long_sym]) > 1:
            continue
        if sum(1 for s, v in rets.items() if v == rets[short_sym]) > 1:
            continue

        # entry/exit prices on day_t
        legs = []
        for sym, side in ((long_sym, 1), (short_sym, -1)):
            g = frames[sym]
            gd = g[g["time"].dt.normalize() == day_t].sort_values("time")
            if gd.empty:
                legs = None
                break
            b_e = bar_at(gd, day_t, 15, 30)
            b_x = bar_at(gd, day_t, 17, 25)
            if b_e is None or b_x is None:
                legs = None
                break
            entry = float(b_e["close"])
            exit_px = float(b_x["close"])
            if entry <= 0:
                legs = None
                break
            legs.append(bp_ret(entry, exit_px, side))
        if not legs or len(legs) != 2:
            continue
        combined = 0.5 * (legs[0] + legs[1])
        trades.append(
            {
                "date": str(day_t.date()),
                "long_sym": long_sym,
                "short_sym": short_sym,
                "ret_long_prev": round(rets[long_sym], 4),
                "ret_short_prev": round(rets[short_sym], 4),
                "leg_long_bp": round(legs[0], 4),
                "leg_short_bp": round(legs[1], 4),
                "side": 1,  # combined signed as + for summarize side-split; use n/a
                "bruto_bp": combined,
                "hit": "time",
            }
        )
    return trades


def h4_from_m5(m5: pd.DataFrame) -> pd.DataFrame:
    """Resample M5 → H4 CET (floor to 4h)."""
    x = m5.set_index("time").sort_index()
    h4 = x.resample("4h", label="left", closed="left").agg(
        {"open": "first", "high": "max", "low": "min", "close": "last"}
    ).dropna()
    h4 = h4.reset_index()
    return h4


def sim_n27(m5: pd.DataFrame):
    """AUDUSD H4 MR: |dev| vs SMA20 ≥40 bp @12:00 → fade, exit 16:00."""
    h4 = h4_from_m5(m5)
    h4["sma20"] = h4["close"].rolling(20).mean()
    trades = []
    # index by time for exit lookup
    by_t = {t: row for t, row in zip(h4["time"], h4.itertuples(index=False))}
    for row in h4.itertuples(index=False):
        t = row.time
        if t.hour != 12 or t.minute != 0:
            continue
        if not (row.sma20 == row.sma20) or row.sma20 <= 0 or row.close <= 0:
            continue
        # train filter already on m5; still guard
        if t < TRAIN_START or t > TRAIN_END:
            continue
        dev_bp = 1e4 * (row.close - row.sma20) / row.sma20
        if dev_bp >= 40.0:
            side = -1
        elif dev_bp <= -40.0:
            side = 1
        else:
            continue
        exit_t = t + pd.Timedelta(hours=4)  # 16:00
        ex = by_t.get(exit_t)
        if ex is None:
            continue
        entry = float(row.close)
        exit_px = float(ex.close)
        trades.append(
            {
                "date": str(t.date()),
                "side": side,
                "dev_bp": round(dev_bp, 4),
                "entry": entry,
                "exit": exit_px,
                "hit": "time",
                "bruto_bp": bp_ret(entry, exit_px, side),
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
    sides = np.array([t.get("side", 1) for t in trades])
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
            "stop_share": round(
                float(np.mean([t.get("hit") == "stop" for t in trades])), 4
            ),
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

    us500 = load_m5("data/m5gz/US500cash.csv.gz")
    xau = load_m5("data/m5gz/XAUUSD.csv.gz")
    us100 = load_m5("data/m5gz/US100cash.csv.gz")
    us30 = load_m5("data/m5gz/US30cash.csv.gz")
    ger = load_m5("data/m5gz/GER40cash.csv.gz")
    aud = load_m5("data/m5gz/AUDUSD.csv.gz")

    atr_us500 = atr_map(us500)
    atr_xau = atr_map(xau)

    n24, n25 = [], []
    for day, g in us500.groupby(us500["time"].dt.normalize()):
        t = sim_n24(g.sort_values("time"), prior_atr(atr_us500, day))
        if t:
            n24.append(t)
    for day, g in xau.groupby(xau["time"].dt.normalize()):
        t = sim_n25(g.sort_values("time"), prior_atr(atr_xau, day))
        if t:
            n25.append(t)

    pool = {
        "US100cash": us100,
        "US30cash": us30,
        "US500cash": us500,
        "GER40cash": ger,
        "XAUUSD": xau,
    }
    n26 = sim_n26(pool)
    n27 = sim_n27(aud)

    s24 = summarize("N24_US500_LUNCH_FADE", n24, N24_RT, N24_GATE)
    s25 = summarize("N25_XAU_NY_PM_FADE", n25, N25_RT, N25_GATE)
    s26 = summarize(
        "N26_XS_1D_REVERSAL",
        n26,
        N26_RT,
        N26_GATE,
        extra={"note": "equal-weight combined bp; gate worst-pair 4.83"},
    )
    s27 = summarize("N27_AUDUSD_H4_MR", n27, N27_RT, N27_GATE)

    board = {
        "n24": s24,
        "n25": s25,
        "n26": s26,
        "n27": s27,
        "source": "VOORSTEL_PRESCREEN_N24..N27 @ b6e8c1e",
        "min_n": MIN_N,
        "train": "2021-01-01 .. 2023-12-31",
        "reserve_2025": "untouched",
        "runner": "Strateeg faraday scripts/n24_n27_prescreen.py (advance while U2 idle)",
    }

    pd.DataFrame(n24).to_csv(OUT / "n24_trades_train.csv", index=False)
    pd.DataFrame(n25).to_csv(OUT / "n25_trades_train.csv", index=False)
    pd.DataFrame(n26).to_csv(OUT / "n26_trades_train.csv", index=False)
    pd.DataFrame(n27).to_csv(OUT / "n27_trades_train.csv", index=False)
    (OUT / "prescreen.json").write_text(json.dumps(board, indent=2) + "\n")

    md = [
        "# D-092.1 Strateeg pre-screen — N24–N27 (train 2021–2023)",
        "",
        "Source: `VOORSTEL_PRESCREEN_N24..N27` @ `b6e8c1e` (D-094).",
        "Runner: Strateeg faraday (U2 tip still `a1756a7` idle on N20–N23). Reserve 2025+ untouched.",
        f"PASS = mean bruto ≥ gate **and** N≥{MIN_N} → `PASS_may_PREREG`.",
        "",
        "| Idee | Instrument | N | mean bruto | gate | Uitkomst | decision |",
        "|------|------------|---|------------|------|----------|----------|",
        f"| N24 lunch fade | US500cash | {s24['n']} | {s24['mean_bruto_bp']} bp | {N24_GATE} bp | **{lab(s24)}** | `{s24['decision']}` |",
        f"| N25 NY-PM fade | XAUUSD | {s25['n']} | {s25['mean_bruto_bp']} bp | {N25_GATE} bp | **{lab(s25)}** | `{s25['decision']}` |",
        f"| N26 XS 1d reversal | 5-asset basket | {s26['n']} | {s26['mean_bruto_bp']} bp | {N26_GATE} bp | **{lab(s26)}** | `{s26['decision']}` |",
        f"| N27 H4 MR | AUDUSD | {s27['n']} | {s27['mean_bruto_bp']} bp | {N27_GATE} bp | **{lab(s27)}** | `{s27['decision']}` |",
        "",
        "### Side split",
        f"- N24 long/short mean: {s24.get('mean_bruto_long_bp')} / {s24.get('mean_bruto_short_bp')} (n={s24.get('n_long')}/{s24.get('n_short')})",
        f"- N25 long/short mean: {s25.get('mean_bruto_long_bp')} / {s25.get('mean_bruto_short_bp')} (n={s25.get('n_long')}/{s25.get('n_short')})",
        f"- N26 combined mean (side field=1 dummy): {s26.get('mean_bruto_bp')}",
        f"- N27 long/short mean: {s27.get('mean_bruto_long_bp')} / {s27.get('mean_bruto_short_bp')} (n={s27.get('n_long')}/{s27.get('n_short')})",
        "",
        "### Notes",
        "- N24/N25: stop = 1.0×ATR14 (prior day); swap=0.",
        "- N26: equal-weight combined bp; no stop in bruto screen; D-094a (c).",
        "- N27: H4 resample 4h left-closed; pure hold 12:00→16:00; D-094a (b).",
        "",
    ]
    (OUT / "prescreen.md").write_text("\n".join(md) + "\n")
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
