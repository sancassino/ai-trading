#!/usr/bin/env python3
"""D-092.1 non-clones — Strateeg-2 ~11:45 Europe/Amsterdam (D-094 FREEZE OFF + D-097/D-100).

≥2/3 D-097/D-100 families B/C/D (FX cheap-side, metals +bruto, non-oil).
Do NOT clone: IDX_SHORT / ENERGY / TSMOM_DIV / FX_EUR_SHORT / N58–N68 / CORN/WHEAT/XCU/HK50/GBPAUD
prior S2 fails / dead A/B/ORB/N1–N65.

A) SOY_SHORT_TSMOM — SOYBEAN.c short-only L20/H10 (D-100 cheap overnight short).
   ≠ CORN_PLANT long-season; ≠ ENERGY oil.

B) COFFEE_LONG_TSMOM — COFFEE.c long-only L20/H10 (D-100 cheap overnight long).
   ≠ CORN/WHEAT seasons; ≠ oil ENERGY.

C) USDCHF_LONG_TSMOM — USDCHF long-only L20/H10 (D-100 family B cheap long).
   ≠ N47 intradag BARRED; ≠ N67 USDJPY; ≠ FX_EUR_SHORT EUR-shorts.

D) XAU_SHORT_TSMOM — XAUUSD short-only L20/H10 (D-100 family C cheap short).
   ≠ N51 long+SMA200; ≠ N60/N65 XAG; ≠ N36 intradag.

E) USDCAD_LONG_TSMOM — USDCAD long-only L20/H10 (D-100 family B cheap long).
   ≠ N33 intradag; ≠ EURCAD; ≠ FX_EUR_SHORT.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DAILY = ROOT / "data" / "daily"
OUT = ROOT / "results" / "strateeg2_prescreen" / "cycle_1140"
TRAIN_START = pd.Timestamp("2010-01-01")
TRAIN_END = pd.Timestamp("2023-12-31")
# 2024 held for formal test if PREREG; 2025+ sealed

RT = {
    "SOYBEAN.c": 15.817,  # ftmo_specs spread_bp
    "COFFEE.c": 10.443,
    "USDCHF": 1.01,       # COSTS_FTMO_alle RT
    "XAUUSD": 0.83,
    "USDCAD": 0.80,
}


def load_daily(name: str) -> pd.DataFrame:
    path = DAILY / f"{name}.csv"
    df = pd.read_csv(path, sep=";", comment="#")
    df["date"] = pd.to_datetime(df["date"])
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df = df.dropna(subset=["date", "close"]).sort_values("date").reset_index(drop=True)
    return df[(df["date"] >= TRAIN_START) & (df["date"] <= TRAIN_END)].copy()


def walk_hold(closes: np.ndarray, i_entry: int, side: int, hold: int):
    j = min(i_entry + hold, len(closes) - 1)
    if j <= i_entry:
        return None
    entry = float(closes[i_entry])
    exit_px = float(closes[j])
    if entry <= 0 or exit_px <= 0:
        return None
    bruto = 1e4 * side * (exit_px - entry) / entry
    return bruto, j


def summarize(name, trades, rt, d097=True):
    gate = max(3.0 * rt, 50.0) if d097 else 3.0 * rt
    if not trades:
        return dict(
            idea=name, n=0, mean_bruto=None, median=None, gate=round(gate, 4),
            rt=rt, outcome="FAIL", skew=None, hit=None,
        )
    arr = np.array([t["bruto_bp"] for t in trades], dtype=float)
    mean = float(arr.mean())
    med = float(np.median(arr))
    skew = (
        float(((arr - mean) ** 3).mean() / (arr.std(ddof=0) ** 3 + 1e-12))
        if len(arr) > 2
        else None
    )
    hit = float((arr > 0).mean())
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
        skew=None if skew is None else round(skew, 4),
        hit=round(hit, 4),
    )


def sim_tsmom_side(df: pd.DataFrame, lb: int, hold: int, side_only: int):
    """side_only: +1 long-only when ret>0; -1 short-only when ret<0."""
    df = df.reset_index(drop=True)
    c = df["close"].values
    ret = df["close"].pct_change(lb)
    trades, busy_until = [], -1
    for i in range(lb + 1, len(df) - hold):
        if i <= busy_until:
            continue
        r = ret.iloc[i]
        if not pd.notna(r):
            continue
        if side_only > 0 and not (r > 0):
            continue
        if side_only < 0 and not (r < 0):
            continue
        side = 1 if side_only > 0 else -1
        ie = i + 1
        walked = walk_hold(c, ie, side, hold)
        if walked is None:
            continue
        bruto, j = walked
        trades.append(
            dict(
                day=str(df["date"].iloc[ie].date()),
                side=side,
                entry=float(c[ie]),
                exit=float(c[j]),
                reason="time",
                bruto_bp=bruto,
            )
        )
        busy_until = j
    return trades


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    specs = []

    soy = load_daily("SOY_F")
    t = sim_tsmom_side(soy, lb=20, hold=10, side_only=-1)
    s = summarize("SOY_SHORT_TSMOM", t, RT["SOYBEAN.c"], d097=True)
    pd.DataFrame(t).to_csv(OUT / "SOY_SHORT_TSMOM_trades.csv", index=False)
    specs.append((s, "SOYBEAN.c / SOY_F"))
    print(json.dumps(s), flush=True)

    coffee = load_daily("COFFEE_F")
    t = sim_tsmom_side(coffee, lb=20, hold=10, side_only=1)
    s = summarize("COFFEE_LONG_TSMOM", t, RT["COFFEE.c"], d097=True)
    pd.DataFrame(t).to_csv(OUT / "COFFEE_LONG_TSMOM_trades.csv", index=False)
    specs.append((s, "COFFEE.c / COFFEE_F"))
    print(json.dumps(s), flush=True)

    # Prefer FRED long history for USDCHF mechanism (D-094a b)
    chf = load_daily("FX_USDCHF")
    if len(chf) < 500:
        chf = load_daily("USDCHF")
    t = sim_tsmom_side(chf, lb=20, hold=10, side_only=1)
    s = summarize("USDCHF_LONG_TSMOM", t, RT["USDCHF"], d097=True)
    pd.DataFrame(t).to_csv(OUT / "USDCHF_LONG_TSMOM_trades.csv", index=False)
    specs.append((s, "USDCHF / FX_USDCHF"))
    print(json.dumps(s), flush=True)

    xau = load_daily("GOLD_F")
    t = sim_tsmom_side(xau, lb=20, hold=10, side_only=-1)
    s = summarize("XAU_SHORT_TSMOM", t, RT["XAUUSD"], d097=True)
    pd.DataFrame(t).to_csv(OUT / "XAU_SHORT_TSMOM_trades.csv", index=False)
    specs.append((s, "XAUUSD / GOLD_F"))
    print(json.dumps(s), flush=True)

    cad = load_daily("FX_USDCAD")
    if len(cad) < 500:
        cad = load_daily("USDCAD") if (DAILY / "USDCAD.csv").exists() else load_daily("FX_USDCAD")
    t = sim_tsmom_side(cad, lb=20, hold=10, side_only=1)
    s = summarize("USDCAD_LONG_TSMOM", t, RT["USDCAD"], d097=True)
    pd.DataFrame(t).to_csv(OUT / "USDCAD_LONG_TSMOM_trades.csv", index=False)
    specs.append((s, "USDCAD / FX_USDCAD"))
    print(json.dumps(s), flush=True)

    results = [s for s, _ in specs]
    (OUT / "prescreen.json").write_text(json.dumps(results, indent=2))
    lines = [
        "# S2 D-092.1 cycle_1140 (D-094 FREEZE OFF + D-097/D-100)",
        "",
        "Train proxy daily 2010-01-01 → 2023-12-31; 2024 holdout unused; 2025+ sealed.",
        "D-097 gate = max(3×RT, 50 bp). Non-overlapping holds. Overnight = D-100 cheap side only.",
        "",
        "| Idee | Symbool | N | mean bruto | gate | outcome | skew | hit |",
        "|------|---------|--:|----------:|-----:|---------|------|-----|",
    ]
    for s, sym in specs:
        lines.append(
            f"| {s['idea']} | {sym} | {s['n']} | {s['mean_bruto']} | {s['gate']} | **{s['outcome']}** | {s['skew']} | {s['hit']} |"
        )
    (OUT / "prescreen.md").write_text("\n".join(lines) + "\n")
    print("---SUMMARY---")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
