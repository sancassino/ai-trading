#!/usr/bin/env python3
"""C-029 — Lane-B diagnostics for N75–N77 / N79 / N81 + CORN demote audit.

0 trials. Not a formal gate. Reserve 2025+ untouched.
"""
from __future__ import annotations

import gzip
import json
import math
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/cto/c029_n78_absorb_lane_b"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31")
HARD_CUT = pd.Timestamp("2024-12-31")


def m5_daily_close(path: Path) -> pd.Series:
    with gzip.open(path, "rt") as f:
        rows = [ln for ln in f if not ln.startswith("#") and ln.strip()]
    df = pd.read_csv(StringIO("".join(rows)), sep=";")
    df.columns = [c.strip().lower() for c in df.columns]
    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values("time")
    df["date"] = df["time"].dt.normalize()
    g = df.groupby("date", sort=True).tail(1)
    s = g.set_index("date")["close"].astype(float)
    return s[s.index <= HARD_CUT]


def daily_csv(path: Path) -> pd.Series:
    df = pd.read_csv(path, sep=";", comment="#")
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").dropna(subset=["close"])
    s = df.set_index("date")["close"].astype(float)
    return s[s.index <= HARD_CUT]


def trade_stats(pnls_bp, gate_bp, label):
    arr = np.asarray(pnls_bp, dtype=float)
    arr = arr[np.isfinite(arr)]
    n = len(arr)
    mean = float(np.mean(arr)) if n else float("nan")
    if n >= 2 and float(np.std(arr, ddof=1)) > 0:
        t = mean / (float(np.std(arr, ddof=1)) / math.sqrt(n))
    else:
        t = float("nan")
    half = n // 2
    m1 = float(np.mean(arr[:half])) if half else float("nan")
    m2 = float(np.mean(arr[half:])) if n - half else float("nan")
    if n >= 150 and mean >= gate_bp:
        verdict = "DIAG_PASS"
    elif n < 150 and mean >= gate_bp:
        verdict = "UNDERPOWERED"
    else:
        verdict = "DIAG_FAIL"
    return {
        "label": label,
        "n": n,
        "mean_bp": round(mean, 3) if n else None,
        "day_t": round(t, 3) if n >= 2 else None,
        "h1_mean_bp": round(m1, 3) if half else None,
        "h2_mean_bp": round(m2, 3) if n - half else None,
        "gate_bp": gate_bp,
        "verdict": verdict,
    }


def diag_n75():
    xau = m5_daily_close(ROOT / "data/m5gz/XAUUSD.csv.gz")
    xag = m5_daily_close(ROOT / "data/m5gz/XAGUSD.csv.gz")
    idx = xau.index.intersection(xag.index)
    px = pd.DataFrame({"xau": xau.loc[idx], "xag": xag.loc[idx]}).sort_index()
    px = px[(px.index >= TRAIN_START) & (px.index <= TRAIN_END)]
    lnR = np.log(px["xau"] / px["xag"])
    z = (lnR - lnR.rolling(20, min_periods=20).mean()) / lnR.rolling(
        20, min_periods=20
    ).std()
    pnls = []
    i = 20
    dates = list(px.index)
    while i < len(dates) - 3:
        zi = z.loc[dates[i]]
        if np.isfinite(zi) and zi < -1.0:
            e, x = i + 1, i + 3
            if x >= len(dates):
                break
            r_xau = (px["xau"].iloc[x] / px["xau"].iloc[e] - 1) * 1e4
            r_xag = (px["xag"].iloc[x] / px["xag"].iloc[e] - 1) * 1e4
            pnls.append(0.5 * (r_xau - r_xag))
            i = x
        else:
            i += 1
    return trade_stats(pnls, 30.60, "N75_XAU_XAG_ratio_MR_3d")


def diag_n76():
    uk = m5_daily_close(ROOT / "data/m5gz/UKOILcash.csv.gz")
    uk = uk[(uk.index >= TRAIN_START) & (uk.index <= TRAIN_END)]
    dfu = uk.to_frame("close")
    dfu["wd"] = dfu.index.weekday
    pnls = []
    for mon in dfu.index[dfu["wd"] == 0]:
        week = dfu.loc[mon : mon + pd.Timedelta(days=5)]
        thurs = week.index[week["wd"] == 3]
        if len(thurs) == 0:
            fri = week.index[week["wd"] == 4]
            if len(fri) == 0:
                continue
            ex = fri[0]
        else:
            ex = thurs[0]
        if ex <= mon:
            continue
        pnls.append((dfu.loc[ex, "close"] / dfu.loc[mon, "close"] - 1) * 1e4)
    return trade_stats(pnls, 50.00, "N76_UKOIL_MonThu_long")


def diag_n77():
    syms = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF"]
    series = {s: m5_daily_close(ROOT / f"data/m5gz/{s}.csv.gz") for s in syms}
    common = None
    for ser in series.values():
        common = ser.index if common is None else common.intersection(ser.index)
    px = pd.DataFrame({s: series[s].loc[common] for s in syms}).sort_index()
    px = px[
        (px.index >= TRAIN_START - pd.Timedelta(days=120)) & (px.index <= TRAIN_END)
    ]
    ret5 = px / px.shift(5) - 1
    disp = ret5.std(axis=1)
    med60 = disp.rolling(60, min_periods=60).median().shift(1)
    pnls = []
    dates = list(px.index)
    i = 60
    while i < len(dates) - 5:
        d = dates[i]
        if d < TRAIN_START or d > TRAIN_END:
            i += 1
            continue
        if not np.isfinite(disp.loc[d]) or not np.isfinite(med60.loc[d]):
            i += 1
            continue
        if disp.loc[d] <= med60.loc[d]:
            i += 1
            continue
        row = ret5.loc[d]
        if row.isna().any():
            i += 1
            continue
        long_sym, short_sym = row.idxmin(), row.idxmax()
        if long_sym == short_sym:
            i += 1
            continue
        e, x = i + 1, i + 5
        if x >= len(dates):
            break
        r_l = (px[long_sym].iloc[x] / px[long_sym].iloc[e] - 1) * 1e4
        r_s = (px[short_sym].iloc[x] / px[short_sym].iloc[e] - 1) * 1e4
        pnls.append(0.5 * (r_l - r_s))
        i = x
    return trade_stats(pnls, 46.29, "N77_FX_XS_rankrev_5d")


def diag_n79():
    y10 = daily_csv(ROOT / "data/daily/YLD_US10Y.csv")
    y2 = daily_csv(ROOT / "data/daily/YLD_US2Y.csv")
    uk = m5_daily_close(ROOT / "data/m5gz/UKOILcash.csv.gz")
    idx = y10.index.intersection(y2.index).intersection(uk.index)
    df = pd.DataFrame(
        {"y10": y10.loc[idx], "y2": y2.loc[idx], "uk": uk.loc[idx]}
    ).sort_index()
    df["curve"] = df["y10"] - df["y2"]
    df["dcurve5"] = df["curve"] - df["curve"].shift(5)
    df = df[(df.index >= TRAIN_START) & (df.index <= TRAIN_END)]
    pnls = []
    i = 5
    dates = list(df.index)
    while i < len(dates) - 5:
        row = df.iloc[i]
        if row["dcurve5"] > 0 and row["curve"] > 0:
            e, x = i + 1, i + 5
            if x >= len(dates):
                break
            pnls.append((df["uk"].iloc[x] / df["uk"].iloc[e] - 1) * 1e4)
            i = x
        else:
            i += 1
    return trade_stats(pnls, 50.00, "N79_curve_steepener_UKOIL_5d")


def diag_n81():
    u100 = m5_daily_close(ROOT / "data/m5gz/US100cash.csv.gz")
    u500 = m5_daily_close(ROOT / "data/m5gz/US500cash.csv.gz")
    idx = u100.index.intersection(u500.index)
    px = pd.DataFrame({"a": u100.loc[idx], "b": u500.loc[idx]}).sort_index()
    px = px[(px.index >= TRAIN_START) & (px.index <= TRAIN_END)]
    lnR = np.log(px["a"] / px["b"])
    z = (lnR - lnR.rolling(20, min_periods=20).mean()) / lnR.rolling(
        20, min_periods=20
    ).std()
    pnls = []
    i = 20
    dates = list(px.index)
    while i < len(dates) - 3:
        zi = z.loc[dates[i]]
        if np.isfinite(zi) and zi > 1.0:
            e, x = i + 1, i + 3
            if x >= len(dates):
                break
            r_a = (px["a"].iloc[x] / px["a"].iloc[e] - 1) * 1e4
            r_b = (px["b"].iloc[x] / px["b"].iloc[e] - 1) * 1e4
            pnls.append(0.5 * ((-r_a) + r_b))
            i = x
        else:
            i += 1
    return trade_stats(pnls, 13.74, "N81_US100_US500_pair_RV_3d")


def corn_audit():
    raw, prices = [], []
    path = ROOT / "data/m5gz/CORN.c.csv.gz"
    with gzip.open(path, "rt") as f:
        hdr = None
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            if hdr is None:
                hdr = True
                continue
            p = line.strip().split(";")
            try:
                c, sp = float(p[4]), float(p[5])
            except (ValueError, IndexError):
                continue
            if sp > 0 and c > 0:
                raw.append(sp)
                prices.append(c)
    bp = sorted((sp * 0.01 / c) * 1e4 for sp, c in zip(raw, prices))
    n = len(bp)
    med = bp[n // 2] if n else None
    p90 = bp[int(n * 0.9)] if n else None
    return {
        "label": "CORN_F_COMMODITY_SEASONALITY",
        "lane_a_mean_bp": 5.979,
        "lane_a_day_t": 2.111,
        "lane_a_n": 4022,
        "ftmo_symbol": "CORN.c",
        "in_COSTS_FTMO": False,
        "m5gz_present": path.exists(),
        "m5gz_spread_nonzero": n,
        "point_size": 0.01,
        "spread_med_bp_honest": round(med, 2) if med else None,
        "spread_p90_bp_honest": round(p90, 2) if p90 else None,
        "gate_3x_rt_bp": round(3 * med, 2) if med else None,
        "d097_commodity_floor_bp": 50.0,
        "verdict": "DEMOTE_LANE_B",
        "reason": "Lane-A mean 5.98 bp << honest 3xRT (~62) and D-097 floor 50; no COSTS/swap row.",
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [diag_n75(), diag_n76(), diag_n77(), diag_n79(), diag_n81()]
    corn = corn_audit()
    rows.append(
        {
            "label": corn["label"],
            "n": corn["lane_a_n"],
            "mean_bp": corn["lane_a_mean_bp"],
            "day_t": corn["lane_a_day_t"],
            "h1_mean_bp": None,
            "h2_mean_bp": None,
            "gate_bp": corn.get("gate_3x_rt_bp") or 50.0,
            "verdict": corn["verdict"],
        }
    )
    pd.DataFrame(rows).to_csv(OUT / "c029_family_diag.csv", index=False)
    board = {
        "c": "C-029",
        "title": "N78 VIX_TERM_VOV FAIL_COST_GATE absorb + Lane-B diag + CORN demote",
        "when": "2026-10-01 ~12:55 Europe/Amsterdam (CEST / UTC+2)",
        "branch": "grok/cto-1",
        "trials_appended": 0,
        "trial_count_book": 456,
        "reserve_2025": "untouched",
        "spend": "none",
        "diag": rows,
        "corn_audit": corn,
        "prereg_frozen": None,
    }
    (OUT / "c029_board.json").write_text(json.dumps(board, indent=2) + "\n")
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
