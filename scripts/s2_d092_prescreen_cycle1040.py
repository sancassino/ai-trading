#!/usr/bin/env python3
"""D-092.1 non-clones — Strateeg-2 ~10:40 Europe/Amsterdam (D-094 FREEZE OFF + D-097/D-099).

≥2/3 D-097 (swing / season / regime / other markets). Intraday FX/idx clones barred.
Do NOT clone: ENERGY_TSMOM (UKOIL+USOIL L20/H10), N58 AUDUSD/USDJPY carry, N59 UKOIL+ATR,
N45–N57, TSMOM_DIV, dead A/B/ORB/N1–N44/S2 fades.

A) XCU_HV_TSMOM — Copper (COPPER_F→XCUUSD) high-vol regime + 20d TSMOM LO, hold 10d.
   atr14 > median(atr14,60); ≠ oil ENERGY/N50/N59.

B) CORN_PLANT_MOM — CORN_F Mar–Jul planting window + 40d mom >0 LO, hold 15d.
   D-097 commodities-season; ≠ oil/energy family.

C) WHEAT_WINTER_MOM — WHEAT_F Nov–Mar + 40d mom >0 LO, hold 15d.
   Distinct season from CORN; ≠ N49–N57.

D) HK50_SWING_TSMOM — HSI→HK50cash 20d TSMOM LO, hold 10d (Asia index swing).
   ≠ US/GER ORB/fade dead set; ≠ AUS200 Asia BO intradag.

E) GBPAUD_SWING20 — GBPAUD (BIS cross) signed 20d TSMOM, hold 5d.
   ≠ N58 AUDUSD/USDJPY; ≠ GBPJPY_EU_MOM intradag; ≠ N46 EURGBP barred.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DAILY = ROOT / "data" / "daily"
OUT = ROOT / "results" / "strateeg2_prescreen" / "cycle_1040"
TRAIN_START = pd.Timestamp("2010-01-01")
TRAIN_END = pd.Timestamp("2023-12-31")
# 2024 held for formal test if PREREG; 2025+ sealed (never read into trades)

RT = {
    "XCUUSD": 9.74,       # ftmo_specs spread_bp
    "CORN.c": 21.57,
    "WHEAT.c": 18.87,
    "HK50cash": 2.63,     # COSTS_FTMO_alle RT
    "GBPAUD": 1.18,       # COSTS_FTMO_alle RT
}


def load_daily(name: str) -> pd.DataFrame:
    path = DAILY / f"{name}.csv"
    df = pd.read_csv(path, sep=";", comment="#")
    df["date"] = pd.to_datetime(df["date"])
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df = df.dropna(subset=["date", "close"]).sort_values("date").reset_index(drop=True)
    return df[(df["date"] >= TRAIN_START) & (df["date"] <= TRAIN_END)].copy()


def load_gbpaud() -> pd.DataFrame:
    """GBPAUD = FXBIS_AUD / FXBIS_GBP (PROXY_MAP convention)."""
    a = pd.read_csv(DAILY / "FXBIS_AUD.csv", sep=";", comment="#")
    g = pd.read_csv(DAILY / "FXBIS_GBP.csv", sep=";", comment="#")
    a["date"] = pd.to_datetime(a["date"])
    g["date"] = pd.to_datetime(g["date"])
    # BIS files: value column may be 'close' or first numeric
    def px(df):
        for c in ("close", "value", "rate", "px"):
            if c in df.columns:
                return pd.to_numeric(df[c], errors="coerce")
        # fallback: last numeric col
        num = df.select_dtypes(include=[np.number]).columns
        return pd.to_numeric(df[num[-1]], errors="coerce")

    a = a.assign(aud=px(a))[["date", "aud"]]
    g = g.assign(gbp=px(g))[["date", "gbp"]]
    m = a.merge(g, on="date", how="inner")
    m["close"] = m["aud"] / m["gbp"]
    m = m.dropna(subset=["close"]).sort_values("date")
    return m[(m["date"] >= TRAIN_START) & (m["date"] <= TRAIN_END)][["date", "close"]].copy()


def atr14(df: pd.DataFrame) -> pd.Series:
    if not {"high", "low", "close"}.issubset(df.columns):
        # close-only proxy ATR via |Δclose| rolling
        c = df["close"]
        tr = c.diff().abs()
        return tr.rolling(14, min_periods=14).mean()
    h = pd.to_numeric(df["high"], errors="coerce")
    l = pd.to_numeric(df["low"], errors="coerce")
    c = df["close"]
    prev = c.shift(1)
    tr = pd.concat([(h - l), (h - prev).abs(), (l - prev).abs()], axis=1).max(axis=1)
    return tr.rolling(14, min_periods=14).mean()


def walk_hold(closes: np.ndarray, i_entry: int, side: int, hold: int):
    """Enter at closes[i_entry], exit at closes[i_entry+hold] (or last available)."""
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


def sim_xcu_hv_tsmom(df: pd.DataFrame):
    df = df.reset_index(drop=True)
    c = df["close"].values
    atr = atr14(df)
    atr_med = atr.rolling(60, min_periods=40).median()
    ret20 = df["close"].pct_change(20)
    trades, busy_until = [], -1
    for i in range(60, len(df) - 10):
        if i <= busy_until:
            continue
        a, am, r = atr.iloc[i], atr_med.iloc[i], ret20.iloc[i]
        if not (pd.notna(a) and pd.notna(am) and pd.notna(r)):
            continue
        if not (a > am and r > 0):
            continue
        # enter next day close
        ie = i + 1
        walked = walk_hold(c, ie, 1, 10)
        if walked is None:
            continue
        bruto, j = walked
        trades.append(
            dict(
                day=str(df["date"].iloc[ie].date()),
                side=1,
                entry=float(c[ie]),
                exit=float(c[j]),
                reason="time",
                bruto_bp=bruto,
            )
        )
        busy_until = j
    return trades


def sim_season_mom(df: pd.DataFrame, months: set[int], lb: int, hold: int):
    df = df.reset_index(drop=True)
    c = df["close"].values
    ret = df["close"].pct_change(lb)
    trades, busy_until = [], -1
    for i in range(lb + 1, len(df) - hold):
        if i <= busy_until:
            continue
        if df["date"].iloc[i].month not in months:
            continue
        r = ret.iloc[i]
        if not (pd.notna(r) and r > 0):
            continue
        ie = i + 1
        walked = walk_hold(c, ie, 1, hold)
        if walked is None:
            continue
        bruto, j = walked
        trades.append(
            dict(
                day=str(df["date"].iloc[ie].date()),
                side=1,
                entry=float(c[ie]),
                exit=float(c[j]),
                reason="time",
                bruto_bp=bruto,
            )
        )
        busy_until = j
    return trades


def sim_tsmom_lo(df: pd.DataFrame, lb: int, hold: int):
    df = df.reset_index(drop=True)
    c = df["close"].values
    ret = df["close"].pct_change(lb)
    trades, busy_until = [], -1
    for i in range(lb + 1, len(df) - hold):
        if i <= busy_until:
            continue
        r = ret.iloc[i]
        if not (pd.notna(r) and r > 0):
            continue
        ie = i + 1
        walked = walk_hold(c, ie, 1, hold)
        if walked is None:
            continue
        bruto, j = walked
        trades.append(
            dict(
                day=str(df["date"].iloc[ie].date()),
                side=1,
                entry=float(c[ie]),
                exit=float(c[j]),
                reason="time",
                bruto_bp=bruto,
            )
        )
        busy_until = j
    return trades


def sim_tsmom_signed(df: pd.DataFrame, lb: int, hold: int):
    df = df.reset_index(drop=True)
    c = df["close"].values
    ret = df["close"].pct_change(lb)
    trades, busy_until = [], -1
    for i in range(lb + 1, len(df) - hold):
        if i <= busy_until:
            continue
        r = ret.iloc[i]
        if not pd.notna(r) or abs(r) < 1e-12:
            continue
        side = 1 if r > 0 else -1
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

    xcu = load_daily("COPPER_F")
    t = sim_xcu_hv_tsmom(xcu)
    s = summarize("XCU_HV_TSMOM", t, RT["XCUUSD"], d097=True)
    pd.DataFrame(t).to_csv(OUT / "XCU_HV_TSMOM_trades.csv", index=False)
    specs.append((s, "XCUUSD / COPPER_F"))
    print(json.dumps(s), flush=True)

    corn = load_daily("CORN_F")
    t = sim_season_mom(corn, {3, 4, 5, 6, 7}, lb=40, hold=15)
    s = summarize("CORN_PLANT_MOM", t, RT["CORN.c"], d097=True)
    pd.DataFrame(t).to_csv(OUT / "CORN_PLANT_MOM_trades.csv", index=False)
    specs.append((s, "CORN.c / CORN_F"))
    print(json.dumps(s), flush=True)

    wheat = load_daily("WHEAT_F")
    t = sim_season_mom(wheat, {11, 12, 1, 2, 3}, lb=40, hold=15)
    s = summarize("WHEAT_WINTER_MOM", t, RT["WHEAT.c"], d097=True)
    pd.DataFrame(t).to_csv(OUT / "WHEAT_WINTER_MOM_trades.csv", index=False)
    specs.append((s, "WHEAT.c / WHEAT_F"))
    print(json.dumps(s), flush=True)

    hsi = load_daily("HSI")
    t = sim_tsmom_lo(hsi, lb=20, hold=10)
    s = summarize("HK50_SWING_TSMOM", t, RT["HK50cash"], d097=True)
    pd.DataFrame(t).to_csv(OUT / "HK50_SWING_TSMOM_trades.csv", index=False)
    specs.append((s, "HK50cash / HSI"))
    print(json.dumps(s), flush=True)

    gba = load_gbpaud()
    t = sim_tsmom_signed(gba, lb=20, hold=5)
    s = summarize("GBPAUD_SWING20", t, RT["GBPAUD"], d097=True)
    pd.DataFrame(t).to_csv(OUT / "GBPAUD_SWING20_trades.csv", index=False)
    specs.append((s, "GBPAUD / FXBIS"))
    print(json.dumps(s), flush=True)

    results = [s for s, _ in specs]
    (OUT / "prescreen.json").write_text(json.dumps(results, indent=2))
    lines = [
        "# S2 D-092.1 cycle_1040 (D-094 FREEZE OFF + D-097/D-099)",
        "",
        "Train proxy daily 2010-01-01 → 2023-12-31; 2024 holdout unused; 2025+ sealed.",
        "D-097 gate = max(3×RT, 50 bp). Non-overlapping holds.",
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
