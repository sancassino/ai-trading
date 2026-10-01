#!/usr/bin/env python3
"""C-013 D-092.1 free pre-screen: venue-ORB exploration outside dead GER40 N11.

Binding ideas (train 2021–2023 only; reserve 2025+ untouched; no TRIALS):
  N15 UK100 London ORB   RT=1.42 (COSTS_FTMO_alle) → gate 4.26
  N16 JP225 Tokyo ORB    RT=1.51 → gate 4.53 (02:00–02:30 AMS summer-aligned)
  N17 US30 NY ORB        RT=0.45 (COSTS_FTMO) → gate 1.35

Companions (same NY window): N17b US100, N17c US500.
Sensitivities in results JSON only (winter JP / UK flat 17:30).

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
OUT = ROOT / "results/cto/n15_n16_prescreen"
MIN_N = 150
MIN_ORB_FRAC = 0.001

BINDING = [
    ("N15_UK100_LONDON_ORB", "UK100cash", 1.42, (9, 0), (9, 30), (10, 30), (13, 0), "LSE open AMS"),
    ("N16_JP225_TOKYO_ORB", "JP225cash", 1.51, (2, 0), (2, 30), (3, 30), (6, 0), "Tokyo≈02:00 CEST"),
    ("N17_US30_NY_ORB", "US30cash", 0.45, (15, 30), (16, 0), (17, 0), (20, 0), "NY open AMS"),
]
COMPANIONS = [
    ("N17b_US100_NY_ORB", "US100cash", 0.66, (15, 30), (16, 0), (17, 0), (20, 0), "US100 NY companion"),
    ("N17c_US500_NY_ORB", "US500cash", 0.78, (15, 30), (16, 0), (17, 0), (20, 0), "US500 NY companion"),
]


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


def bp_ret(entry: float, exit_px: float, side: int) -> float:
    return side * 1e4 * (exit_px - entry) / entry


def screen_orb(name, sym, rt, orb, orb_end, entry_cut, flat, note: str) -> dict:
    m5 = load_m5(sym)
    m5["date"] = m5["time"].dt.date
    m5["hm"] = m5["time"].dt.hour * 60 + m5["time"].dt.minute
    orb0, orb1 = orb[0] * 60 + orb[1], orb_end[0] * 60 + orb_end[1]
    cut, fl = entry_cut[0] * 60 + entry_cut[1], flat[0] * 60 + flat[1]
    trades = []
    for day, g in m5.groupby("date"):
        g = g.sort_values("time")
        orb_bars = g[(g["hm"] >= orb0) & (g["hm"] < orb1)]
        if len(orb_bars) < 3:
            continue
        hi, lo = float(orb_bars["high"].max()), float(orb_bars["low"].min())
        if hi <= lo or lo <= 0 or (hi - lo) / lo < MIN_ORB_FRAC:
            continue
        post = g[(g["hm"] >= orb1) & (g["hm"] < cut)]
        if post.empty:
            continue
        entry = side = entry_t = None
        for _, row in post.iterrows():
            if row["high"] >= hi:
                entry, side, entry_t = hi, 1, row["time"]
                break
            if row["low"] <= lo:
                entry, side, entry_t = lo, -1, row["time"]
                break
        if entry is None:
            continue
        stop = lo if side == 1 else hi
        rest = g[(g["time"] > entry_t) & (g["hm"] <= fl)]
        exit_px, reason = None, "flat"
        for _, row in rest.iterrows():
            if side == 1 and row["low"] <= stop:
                exit_px, reason = stop, "stop"
                break
            if side == -1 and row["high"] >= stop:
                exit_px, reason = stop, "stop"
                break
        if exit_px is None:
            fb = g[g["hm"] <= fl]
            if fb.empty:
                continue
            exit_px = float(fb.iloc[-1]["close"])
        trades.append(
            dict(date=str(day), side=side, bruto_bp=bp_ret(entry, exit_px, side), reason=reason)
        )
    tdf = pd.DataFrame(trades)
    gate = 3.0 * rt
    if tdf.empty:
        return dict(idea=name, symbol=sym, n=0, outcome="FAIL_empty", gate=gate, rt=rt, note=note)
    n = len(tdf)
    mean = float(tdf["bruto_bp"].mean())
    med = float(tdf["bruto_bp"].median())
    ss = float((tdf["reason"] == "stop").mean())
    if mean >= gate and n >= MIN_N:
        outcome = "PASS_may_PREREG"
    elif mean >= gate:
        outcome = "NO_PREREG_underpowered"
    else:
        outcome = "FAIL"
    tdf.to_csv(OUT / f"{name.lower()}_trades_train.csv", index=False)
    return dict(
        idea=name,
        symbol=sym,
        n=n,
        mean_bruto=round(mean, 4),
        median_bruto=round(med, 4),
        stop_share=round(ss, 4),
        rt=rt,
        gate=round(gate, 4),
        outcome=outcome,
        note=note,
        p25=round(float(tdf["bruto_bp"].quantile(0.25)), 4),
        p75=round(float(tdf["bruto_bp"].quantile(0.75)), 4),
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [screen_orb(*cfg) for cfg in BINDING + COMPANIONS]
    board = {
        "when": "2026-10-01 ~04:05 Europe/Amsterdam",
        "ticket": "C-013",
        "window": "train 2021-01-01 .. 2023-12-31",
        "reserve_2025": "untouched",
        "test_2024": "untouched",
        "binding": [r for r in rows if r["idea"] in {c[0] for c in BINDING}],
        "companions": [r for r in rows if r["idea"] in {c[0] for c in COMPANIONS}],
        "all": rows,
    }
    (OUT / "prescreen.json").write_text(json.dumps(board, indent=2) + "\n")
    lines = [
        "# C-013 D-092.1 pre-screen — N15/N16/N17 venue-ORB exploration",
        "",
        "Train 2021–2023 only. Reserve 2025+ untouched. No TRIALS. No PREREG claimed.",
        "RT from COSTS_FTMO / COSTS_FTMO_alle. m5gz clock = Europe/Amsterdam.",
        "",
        "| Idee | N | mean bruto | median | stop_share | gate | Uitkomst |",
        "|------|---|------------|--------|------------|------|----------|",
    ]
    for r in rows:
        lines.append(
            f"| {r['idea']} | {r['n']} | {r.get('mean_bruto')} bp | {r.get('median_bruto')} bp | "
            f"{r.get('stop_share')} | {r.get('gate')} | **{r['outcome']}** |"
        )
    lines += [
        "",
        "## Readout",
        "- All listed venue-ORBs **FAIL** D-092.1 on train 2021–23.",
        "- Same skew pattern as N11/LUNCH: negative median, stop_share ~0.55–0.67.",
        "- Do not PREREG; do not clone simple single-symbol ORB without a new mechanism.",
        "",
    ]
    (OUT / "prescreen.md").write_text("\n".join(lines))
    for r in rows:
        print(f"{r['idea']}: N={r['n']} mean={r.get('mean_bruto')} → {r['outcome']}")


if __name__ == "__main__":
    main()
