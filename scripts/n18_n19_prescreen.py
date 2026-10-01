#!/usr/bin/env python3
"""C-014 D-092.1 free pre-screen: Strateeg VOORSTEL N18/N19 (non-ORB).

N18 US500 Overnight Gap Continuation — train 2021–23, gate 2.34 (3×0.78).
N19 XAU Overnight Gap Fill (pre-London) — train 2021–23, gate 2.49 (3×0.83).

Reserve 2025+ untouched. No TRIALS. m5gz clock = Europe/Amsterdam wall.
Source: VOORSTEL_PRESCREEN_N18/N19 @ Strateeg 50561ab.
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
MIN_N = 150
OUT = ROOT / "results/cto/n18_n19_prescreen"


def load_m5(sym: str) -> pd.DataFrame:
    path = ROOT / f"data/m5gz/{sym}.csv.gz"
    with gzip.open(path, "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["open", "high", "low", "close"]).sort_values("time")
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
    row = rows.iloc[0]
    if row["time"].normalize() != day0:
        return None
    if row["time"] > t + pd.Timedelta(minutes=30):
        return None
    return row


def bp_ret(entry: float, exit_px: float, side: int) -> float:
    return side * 1e4 * (exit_px - entry) / entry


def prior_close_2200(m5_by_date: dict, day: pd.Timestamp) -> float | None:
    """M5 close of 22:00 AMS bar on previous calendar trading day with that bar."""
    for k in range(1, 10):
        prev = day - pd.Timedelta(days=k)
        g = m5_by_date.get(prev.date())
        if g is None or g.empty:
            continue
        b = bar_at(g, prev.normalize(), 22, 0)
        if b is not None:
            return float(b["close"])
        # fallback: last bar at/before 22:00 same day
        cand = g[g["time"] <= prev.normalize() + pd.Timedelta(hours=22)]
        if not cand.empty and cand.iloc[-1]["time"].hour >= 15:
            return float(cand.iloc[-1]["close"])
    return None


def simulate_path(
    g: pd.DataFrame,
    entry_t: pd.Timestamp,
    entry: float,
    side: int,
    stop: float,
    flat_h: int,
    flat_m: int,
    target: float | None = None,
) -> tuple[float, str] | None:
    fl = entry_t.normalize() + pd.Timedelta(hours=flat_h, minutes=flat_m)
    rest = g[(g["time"] > entry_t) & (g["time"] <= fl)]
    if rest.empty:
        return None
    for _, row in rest.iterrows():
        if target is not None:
            if side == 1 and row["high"] >= target:
                return float(target), "target"
            if side == -1 and row["low"] <= target:
                return float(target), "target"
        if side == 1 and row["low"] <= stop:
            return float(stop), "stop"
        if side == -1 and row["high"] >= stop:
            return float(stop), "stop"
    return float(rest.iloc[-1]["close"]), "flat"


def screen_n18(m5: pd.DataFrame, atr: pd.Series) -> pd.DataFrame:
    """US500 overnight gap continuation ≥ ±50 bp; entry 15:30; flat 18:30; stop 1.5 ATR."""
    m5 = m5.copy()
    m5["date"] = m5["time"].dt.date
    by_date = {d: g.sort_values("time") for d, g in m5.groupby("date")}
    trades = []
    for day, g in by_date.items():
        day0 = pd.Timestamp(day)
        atr_v = prior_atr(atr, day0)
        if not (atr_v == atr_v) or atr_v <= 0:
            continue
        p_prior = prior_close_2200(by_date, day0)
        if p_prior is None or p_prior <= 0:
            continue
        open_bar = bar_at(g, day0, 15, 30)
        if open_bar is None:
            open_bar = first_bar_at_or_after(g, day0, 15, 30)
        if open_bar is None:
            continue
        p_open = float(open_bar["close"])
        gap_bp = 1e4 * (p_open - p_prior) / p_prior
        if gap_bp >= 50.0:
            side = 1
        elif gap_bp <= -50.0:
            side = -1
        else:
            continue
        entry = p_open
        entry_t = open_bar["time"]
        stop = entry - side * 1.5 * atr_v
        sim = simulate_path(g, entry_t, entry, side, stop, 18, 30)
        if sim is None:
            continue
        exit_px, reason = sim
        trades.append(
            dict(
                date=str(day),
                side=side,
                gap_bp=gap_bp,
                bruto_bp=bp_ret(entry, exit_px, side),
                reason=reason,
                atr=atr_v,
            )
        )
    return pd.DataFrame(trades)


def screen_n19(m5: pd.DataFrame, atr: pd.Series) -> pd.DataFrame:
    """XAU overnight gap fill ≥ ±30 bp; fade entry 08:00; target prior close; stop 1.0 ATR; flat 10:30."""
    m5 = m5.copy()
    m5["date"] = m5["time"].dt.date
    by_date = {d: g.sort_values("time") for d, g in m5.groupby("date")}
    trades = []
    for day, g in by_date.items():
        day0 = pd.Timestamp(day)
        atr_v = prior_atr(atr, day0)
        if not (atr_v == atr_v) or atr_v <= 0:
            continue
        p_prior = prior_close_2200(by_date, day0)
        if p_prior is None or p_prior <= 0:
            continue
        pre = bar_at(g, day0, 8, 0)
        if pre is None:
            pre = first_bar_at_or_after(g, day0, 8, 0)
        if pre is None:
            continue
        p_pre = float(pre["close"])
        gap_bp = 1e4 * (p_pre - p_prior) / p_prior
        if gap_bp >= 30.0:
            side = -1  # fade up-gap
        elif gap_bp <= -30.0:
            side = 1  # fade down-gap
        else:
            continue
        entry = p_pre
        entry_t = pre["time"]
        stop = entry - side * 1.0 * atr_v
        sim = simulate_path(g, entry_t, entry, side, stop, 10, 30, target=p_prior)
        if sim is None:
            continue
        exit_px, reason = sim
        trades.append(
            dict(
                date=str(day),
                side=side,
                gap_bp=gap_bp,
                bruto_bp=bp_ret(entry, exit_px, side),
                reason=reason,
                atr=atr_v,
            )
        )
    return pd.DataFrame(trades)


def summarize(name: str, sym: str, rt: float, tdf: pd.DataFrame, note: str) -> dict:
    gate = 3.0 * rt
    if tdf.empty:
        return dict(
            idea=name,
            symbol=sym,
            n=0,
            mean_bruto_bp=None,
            median_bruto_bp=None,
            stop_share=None,
            gate=gate,
            rt=rt,
            outcome="FAIL_empty",
            note=note,
        )
    n = len(tdf)
    mean = float(tdf["bruto_bp"].mean())
    med = float(tdf["bruto_bp"].median())
    ss = float((tdf["reason"] == "stop").mean())
    tgt = float((tdf["reason"] == "target").mean()) if "target" in tdf["reason"].values else 0.0
    if mean >= gate and n >= MIN_N:
        outcome = "PASS_may_PREREG"
    elif mean >= gate:
        outcome = "NO_PREREG_underpowered"
    else:
        outcome = "FAIL"
    skew_fragile = bool(med < 0 and ss > 0.45)
    return dict(
        idea=name,
        symbol=sym,
        n=n,
        mean_bruto_bp=round(mean, 4),
        median_bruto_bp=round(med, 4),
        stop_share=round(ss, 4),
        target_share=round(tgt, 4),
        gate=gate,
        rt=rt,
        outcome=outcome,
        skew_fragile=skew_fragile,
        note=note,
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    results = []

    print("Loading US500cash…")
    us500 = load_m5("US500cash")
    atr500 = atr_map(us500)
    t18 = screen_n18(us500, atr500)
    if not t18.empty:
        t18.to_csv(OUT / "n18_us500_gap_cont_trades_train.csv", index=False)
    r18 = summarize(
        "N18_US500_OVN_GAP_CONT",
        "US500cash",
        0.78,
        t18,
        "gap≥±50bp vs prior 22:00; cont@15:30; stop1.5ATR; flat18:30; ≠N5 fade",
    )
    results.append(r18)
    print(json.dumps(r18, indent=2))

    print("Loading XAUUSD…")
    xau = load_m5("XAUUSD")
    atrx = atr_map(xau)
    t19 = screen_n19(xau, atrx)
    if not t19.empty:
        t19.to_csv(OUT / "n19_xau_ovn_gap_fill_trades_train.csv", index=False)
    r19 = summarize(
        "N19_XAU_OVN_GAP_FILL",
        "XAUUSD",
        0.83,
        t19,
        "gap≥±30bp vs prior 22:00; fade@08:00→prior; stop1.0ATR; flat10:30; ≠N5/XAU_AM",
    )
    results.append(r19)
    print(json.dumps(r19, indent=2))

    board = {
        "cycle": "C-014",
        "when": "2026-10-01 ~04:25 Europe/Amsterdam",
        "window": "2021-01-01..2023-12-31",
        "reserve_2025": "untouched",
        "source_voorstel": "Strateeg 50561ab VOORSTEL_PRESCREEN_N18/N19",
        "min_n": MIN_N,
        "results": results,
    }
    (OUT / "prescreen.json").write_text(json.dumps(board, indent=2) + "\n")
    print("OUT", OUT)


if __name__ == "__main__":
    main()
