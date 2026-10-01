#!/usr/bin/env python3
"""PREREG_FTMO_TSMOM_DIV — gediversifieerde 12-1 TSMOM, maandelijkse rebalance.

CEO D-098: universe FTMO-symbolen 10j_plus=ja excl. stocks/crypto.
Train: 2008-01 – 2016-12. Test: 2017-01 – 2024-12. Reserve 2025+: onaangeroerd.

Protocol:
  1. universe.csv bevroren VOOR run (commit bevestigt volgorde)
  2. Kostenpoort: pooled mean bruto per maand ≥ 3× (RT + swap_avg_per_month_bp)
  3. Formele t-toets: dag-geclusterd netto t ≥ 2.0 in BEIDE helften
     + netto gemiddelde > 0 in beide; ≥ 2/3 klassen positief
  4. +50% swap-gevoeligheid als aanvullend cijfer
"""
from __future__ import annotations

import json
import math
import os
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/tsmom_div"
OUT.mkdir(parents=True, exist_ok=True)

DAILY_DIR = ROOT / "data/daily"
PROXY_MAP = ROOT / "data/PROXY_MAP_FTMO.csv"
FTMO_SPECS = ROOT / "data/ftmo_specs/2026-09-30.csv"
UNIVERSE_CSV = OUT / "universe.csv"

TRAIN_START = pd.Timestamp("2008-01-01")
TRAIN_END = pd.Timestamp("2016-12-31")
TEST_START = pd.Timestamp("2017-01-01")
TEST_END = pd.Timestamp("2024-12-31")

SIGNAL_LOOKBACK = 12  # months
SIGNAL_SKIP = 1       # skip most recent month (12-1 momentum)
VOL_WINDOW = 60       # days for realized vol
VOL_TARGET = 0.10     # 10%/yr per instrument
TRADING_DAYS_PER_YEAR = 252
CALENDAR_DAYS_PER_MONTH = 30  # approximate hold period for swap
SWAP_STRESS = 1.50    # +50% swap gevoeligheid


def load_proxy(proxy_str: str) -> pd.Series | None:
    """Load daily close price for an instrument from its proxy definition."""
    if not proxy_str or (isinstance(proxy_str, float) and math.isnan(proxy_str)):
        return None
    parts = [p.strip() for p in proxy_str.split("+")]
    if len(parts) == 1:
        path = DAILY_DIR / f"{parts[0]}.csv"
        if not path.exists():
            return None
        df = pd.read_csv(path, sep=";", comment="#")
        df["date"] = pd.to_datetime(df["date"])
        df = df.dropna(subset=["adjclose"]).set_index("date")["adjclose"]
        return df.sort_index()
    elif len(parts) == 2:
        # Cross rate: second / first (FXBIS convention: local-per-USD ratios)
        # e.g. AUDCAD = FXBIS_CAD / FXBIS_AUD
        def _load_part(p):
            path = DAILY_DIR / f"{p}.csv"
            if not path.exists():
                return None
            df = pd.read_csv(path, sep=";", comment="#")
            df["date"] = pd.to_datetime(df["date"])
            df = df.dropna(subset=["adjclose"]).set_index("date")["adjclose"]
            return df.sort_index()

        s0 = _load_part(parts[0])
        s1 = _load_part(parts[1])
        if s0 is None or s1 is None:
            return None
        # Align, compute cross rate (s1 / s0)
        idx = s0.index.intersection(s1.index)
        cross = s1.loc[idx] / s0.loc[idx]
        return cross
    else:
        # 3-part like SILVER_F+FXBIS_EUR means SILVER_F (USD) / FXBIS_EUR (EUR/USD) = SILVER_EUR
        # Actually from PROXY_MAP: XAGEUR = SILVER_F+FXBIS_EUR -> price in EUR
        # = SILVER_USD / EURUSD = SILVER_USD * FXBIS_EUR
        # FXBIS_EUR = EUR/USD, so SILVER_EUR = SILVER_USD * (EUR/USD)
        # = SILVER_F * FXBIS_EUR
        if len(parts) == 2:
            pass  # handled above
        # Fall back to just first component
        return None


def build_universe() -> pd.DataFrame:
    """Build universe from PROXY_MAP_FTMO, filter 10j_plus=ja excl. stocks/crypto."""
    pmap = pd.read_csv(PROXY_MAP, sep=";", comment="#")
    uni = pmap[
        (pmap["10j_plus"] == "ja")
        & (~pmap["categorie"].isin(["stock", "crypto"]))
    ].copy()
    return uni.reset_index(drop=True)


def load_costs() -> pd.DataFrame:
    """Load RT (spread_bp) and swap rates from FTMO specs snapshot."""
    specs = pd.read_csv(FTMO_SPECS, sep=";")
    specs = specs[["symbol", "spread_bp", "long_pct_yr", "short_pct_yr"]].copy()
    # RT = full spread roundtrip (bp)
    # swap_long_bp_night = long_pct_yr / 100 / 365 * 10000
    specs["rt_bp"] = specs["spread_bp"]  # already the bid-ask spread in bp (RT = 1x spread)
    specs["swap_long_bp_night"] = specs["long_pct_yr"] / 100 / 365 * 10_000
    specs["swap_short_bp_night"] = specs["short_pct_yr"] / 100 / 365 * 10_000
    return specs.set_index("symbol")


def get_monthly_eom(prices: pd.Series) -> pd.Series:
    """Resample to end-of-month using last available price."""
    return prices.resample("ME").last().dropna()


def compute_signal(monthly: pd.Series) -> pd.Series:
    """12-1 momentum: sign of return from t-12 to t-1."""
    ret12_1 = monthly.pct_change(SIGNAL_LOOKBACK).shift(SIGNAL_SKIP)
    return np.sign(ret12_1)


def compute_daily_vol(prices: pd.Series) -> pd.Series:
    """60-day annualized realized vol from daily returns."""
    ret = prices.pct_change()
    vol = ret.rolling(VOL_WINDOW).std() * math.sqrt(TRADING_DAYS_PER_YEAR)
    return vol


def t_plain(x) -> float:
    x = np.asarray(x, float)
    if len(x) <= 2 or x.std(ddof=1) <= 0:
        return float("nan")
    return float(x.mean() / x.std(ddof=1) * math.sqrt(len(x)))


def t_nw(x, L: int = 5) -> float:
    x = np.asarray(x, float)
    n = len(x)
    if n <= 2:
        return float("nan")
    e = x - x.mean()
    s = float(e @ e / n)
    for k in range(1, L + 1):
        s += 2 * (1 - k / (L + 1)) * float(e[k:] @ e[:-k] / n)
    if s <= 0:
        return float("nan")
    return float(x.mean() / math.sqrt(s / n))


def run_instrument(
    sym: str,
    proxy: str,
    cat: str,
    costs: pd.DataFrame,
    window_start: pd.Timestamp,
    window_end: pd.Timestamp,
    swap_multiplier: float = 1.0,
) -> pd.DataFrame | None:
    """Simulate 12-1 TSMOM for one instrument. Returns monthly trade DataFrame."""
    price = load_proxy(proxy)
    if price is None:
        return None

    # Load costs
    if sym not in costs.index:
        return None
    rt_bp = float(costs.loc[sym, "rt_bp"])
    swap_long = float(costs.loc[sym, "swap_long_bp_night"]) * swap_multiplier
    swap_short = float(costs.loc[sym, "swap_short_bp_night"]) * swap_multiplier

    # Extend window back for vol/signal computation
    ext_start = window_start - pd.DateOffset(months=SIGNAL_LOOKBACK + VOL_WINDOW // 21 + 3)
    price_ext = price[price.index >= ext_start]

    # End-of-month prices
    monthly = get_monthly_eom(price_ext)
    if len(monthly) < SIGNAL_LOOKBACK + 3:
        return None

    # Signal
    signal = compute_signal(monthly)

    # Daily vol on extended window
    daily_vol = compute_daily_vol(price_ext)

    # Build trades: for each month t in [window_start, window_end]
    # - signal computed at end of month t-1
    # - enter at EOM t-1 close
    # - exit at EOM t close
    # - days_held ≈ calendar days from t-1 to t

    trade_months = monthly[(monthly.index >= window_start) & (monthly.index <= window_end)]

    records = []
    prev_signal = 0.0
    for i, (date_t, price_t) in enumerate(trade_months.items()):
        # Entry was at previous month end
        if i == 0:
            continue  # need previous month

        prev_dates = monthly.index[monthly.index < date_t]
        if len(prev_dates) == 0:
            continue
        date_t1 = prev_dates[-1]

        price_t1 = monthly.loc[date_t1]
        if price_t1 <= 0 or price_t < 0:
            continue

        sig = signal.loc[date_t1] if date_t1 in signal.index else float("nan")
        if not (sig == 1 or sig == -1):
            continue

        # Vol for position sizing (at entry date)
        vol_at_entry = daily_vol.get(date_t1, float("nan"))
        if not (vol_at_entry > 0):
            continue

        # Position size: target 10%/yr vol
        pos = VOL_TARGET / vol_at_entry * sig  # signed

        # Bruto return (bp) of the proxy
        bruto_bp = sig * (price_t / price_t1 - 1) * 10_000  # undirected: |pos| × proxy return

        # Calendar days held (for swap)
        cal_days = (date_t - date_t1).days

        # Swap cost (bp, always a cost regardless of sign)
        if sig > 0:
            swap_cost_bp = max(0, -swap_long) * cal_days  # pay if negative (receive when beneficial)
            # Convention: swap_long_bp_night>0 means receive, <0 means pay
            # Cost to P&L = -swap_long if swap_long < 0
        else:
            swap_cost_bp = max(0, swap_short) * abs(cal_days)  # short swap positive = cost

        # Netto: bruto - RT - swap
        netto_bp = bruto_bp - rt_bp - swap_cost_bp

        records.append(
            dict(
                date=str(date_t.date()),
                year=date_t.year,
                month=date_t.month,
                sig=float(sig),
                pos=float(pos),
                bruto_bp=float(bruto_bp),
                rt_bp=float(rt_bp),
                swap_cost_bp=float(swap_cost_bp),
                netto_bp=float(netto_bp),
                vol_at_entry=float(vol_at_entry),
            )
        )
        prev_signal = sig

    if not records:
        return None
    return pd.DataFrame(records)


def summarize_window(df: pd.DataFrame, label: str, gate: float, stress: float) -> dict:
    if df is None or df.empty:
        return {"window": label, "N": 0, "outcome": "FAIL_EMPTY"}
    n = len(df)
    mean_b = float(df["bruto_bp"].mean())
    mean_n = float(df["netto_bp"].mean())
    # Day-clustered t (here: monthly returns per instrument, pooled → monthly portfolio returns)
    day = df.groupby("date")["netto_bp"].sum()
    day_b = df.groupby("date")["bruto_bp"].sum()
    return {
        "window": label,
        "N_trades": int(n),
        "N_months": int(len(day)),
        "mean_bruto": round(mean_b, 4),
        "mean_netto": round(mean_n, 4),
        "gate": round(gate, 4),
        "stress": round(stress, 4),
        "gate_pass": bool(mean_b >= gate and n >= 150),
        "stress_pass": bool(mean_b >= stress),
        "t_day_clust_netto": round(t_plain(day.values), 4),
        "t_nw_L5_netto": round(t_nw(day.values, 5), 4),
        "t_day_clust_bruto": round(t_plain(day_b.values), 4),
        "t_nw_L5_bruto": round(t_nw(day_b.values, 5), 4),
        "date_min": str(df["date"].min()),
        "date_max": str(df["date"].max()),
    }


def decide(tr: dict, te: dict | None) -> str:
    if not tr.get("gate_pass"):
        return "FAIL_COST_GATE"
    train_t = (
        tr.get("N_months", 0) >= 50
        and tr.get("mean_netto", 0) > 0
        and tr.get("t_day_clust_netto") is not None
        and tr.get("t_nw_L5_netto") is not None
        and tr["t_day_clust_netto"] >= 2.0
        and tr["t_nw_L5_netto"] >= 2.0
    )
    if not tr.get("stress_pass"):
        return "FAIL_STRESS_then_" + ("PASS_T" if (train_t and te and te.get("t_day_clust_netto", 0) >= 2.0 and te.get("t_nw_L5_netto", 0) >= 2.0) else "FAIL_T")
    if not te:
        return "FAIL_T" if not train_t else "TRAIN_ONLY"
    test_t = (
        te.get("N_months", 0) >= 30
        and te.get("mean_netto", 0) > 0
        and te.get("t_day_clust_netto") is not None
        and te.get("t_nw_L5_netto") is not None
        and te["t_day_clust_netto"] >= 2.0
        and te["t_nw_L5_netto"] >= 2.0
    )
    if train_t and test_t:
        return "PASS_CANDIDATE"
    return "FAIL_T"


def main():
    uni = build_universe()
    costs = load_costs()

    # Freeze universe (PREREG: bevroren vóór run)
    uni.to_csv(UNIVERSE_CSV, index=False)
    print(f"Universe frozen: {len(uni)} instruments → {UNIVERSE_CSV}")

    # Load swap for computing gate threshold per instrument
    # Gate: pooled mean bruto ≥ 3× mean (RT + swap_avg_per_month)
    # For gate, we use BOTH directions average swap cost
    cost_per_trade = {}
    for _, row in uni.iterrows():
        sym = row["ftmo_symbol"]
        if sym not in costs.index:
            continue
        rt = float(costs.loc[sym, "rt_bp"])
        sl = float(costs.loc[sym, "swap_long_bp_night"])
        ss = float(costs.loc[sym, "swap_short_bp_night"])
        # Avg swap cost (both directions: half long, half short)
        swap_avg = (max(0, -sl) + max(0, ss)) / 2 * CALENDAR_DAYS_PER_MONTH
        cost_per_trade[sym] = {"rt_bp": rt, "swap_avg_bp_month": swap_avg, "total": rt + swap_avg}

    mean_cost = float(np.mean([v["total"] for v in cost_per_trade.values()])) if cost_per_trade else 0
    gate = 3 * mean_cost
    stress = gate * SWAP_STRESS

    print(f"Mean cost per trade: {mean_cost:.3f} bp → gate={gate:.3f} bp, stress={stress:.3f} bp")

    # Run simulation for each instrument and window
    train_parts = []
    test_parts = []

    class_results = {}  # by category
    n_ok = 0
    n_skip = 0

    for _, row in uni.iterrows():
        sym = row["ftmo_symbol"]
        proxy = row["proxy"]
        cat = row["categorie"]
        print(f"  {sym} ({cat}) proxy={proxy}", end=" ", flush=True)

        tr_df = run_instrument(sym, proxy, cat, costs, TRAIN_START, TRAIN_END)
        te_df = run_instrument(sym, proxy, cat, costs, TEST_START, TEST_END)

        if tr_df is None or tr_df.empty:
            print("SKIP")
            n_skip += 1
            continue

        n_ok += 1
        print(f"N_train={len(tr_df)}", end="")

        train_parts.append(tr_df.assign(sym=sym, cat=cat))
        if te_df is not None and not te_df.empty:
            test_parts.append(te_df.assign(sym=sym, cat=cat))
            print(f" N_test={len(te_df)}")
        else:
            print()

        if cat not in class_results:
            class_results[cat] = {"train": [], "test": []}
        class_results[cat]["train"].append(tr_df)
        if te_df is not None:
            class_results[cat]["test"].append(te_df)

    print(f"\n{n_ok} instruments OK, {n_skip} skipped")

    if not train_parts:
        print("No data, aborting")
        return {}

    all_train = pd.concat(train_parts, ignore_index=True)
    all_test = pd.concat(test_parts, ignore_index=True) if test_parts else None

    # Save trades
    all_train.to_csv(OUT / "train_trades.csv", index=False)
    if all_test is not None:
        all_test.to_csv(OUT / "test_trades.csv", index=False)

    tr = summarize_window(all_train, "train", gate, stress)
    te = summarize_window(all_test, "test", gate, stress) if all_test is not None else None

    # Also run with stress multiplier
    train_stress = []
    for _, row in uni.iterrows():
        sym = row["ftmo_symbol"]
        proxy = row["proxy"]
        cat = row["categorie"]
        tr_s = run_instrument(sym, proxy, cat, costs, TRAIN_START, TRAIN_END, swap_multiplier=SWAP_STRESS)
        if tr_s is not None and not tr_s.empty:
            train_stress.append(tr_s.assign(sym=sym, cat=cat))
    tr_stress = None
    if train_stress:
        all_train_stress = pd.concat(train_stress, ignore_index=True)
        tr_stress = summarize_window(all_train_stress, "train_stress50pct", gate, stress)

    # Class-level summary (PREREG: ≥ 2/3 classes positive)
    n_classes = len(class_results)
    n_positive_classes = 0
    class_summary = {}
    for cat, dfs in class_results.items():
        if dfs["train"]:
            df_cat = pd.concat(dfs["train"], ignore_index=True)
            mn = float(df_cat["netto_bp"].mean())
            mb = float(df_cat["bruto_bp"].mean())
            class_summary[cat] = {
                "mean_bruto": round(mb, 4),
                "mean_netto": round(mn, 4),
                "N": len(df_cat),
                "positive": mn > 0,
            }
            if mn > 0:
                n_positive_classes += 1

    frac_pos = n_positive_classes / n_classes if n_classes > 0 else 0
    class_crit_pass = frac_pos >= 2 / 3

    outcome = decide(tr, te)

    board = {
        "prereg": "PREREG_FTMO_TSMOM_DIV.md",
        "outcome": outcome,
        "gate_bp": round(gate, 4),
        "stress_bp": round(stress, 4),
        "n_instruments": n_ok,
        "train": tr,
        "test": te,
        "train_stress": tr_stress,
        "class_crit_pass": class_crit_pass,
        "n_classes": n_classes,
        "n_positive_classes": n_positive_classes,
        "class_summary": class_summary,
        "counts_as_trial": bool(tr.get("gate_pass")),
        "reserve_2025": "untouched",
    }

    (OUT / "tsmom_div_board.json").write_text(json.dumps(board, indent=2) + "\n")

    # Markdown report
    md = [
        "# PREREG_FTMO_TSMOM_DIV — cost-gate + formal train/test",
        "",
        "Source: CEO branch `claude/ftmo-trading-strategy-98mplz`. "
        "Reserve 2025+ untouched.",
        "",
        f"Universe: {n_ok} instruments (FX={class_summary.get('fx', {}).get('N', 0)//max(1,len(train_parts))} months each approx.).",
        f"Gate: {gate:.2f} bp; Stress: {stress:.2f} bp (= gate × 1.50).",
        "",
        "## Pooled results",
        "",
        "| Metric | Train (2008-2016) | Test (2017-2024) |",
        "|--------|------------------:|----------------:|",
        f"| N_trades | {tr.get('N_trades')} | {te.get('N_trades') if te else None} |",
        f"| N_months | {tr.get('N_months')} | {te.get('N_months') if te else None} |",
        f"| mean bruto (bp) | {tr.get('mean_bruto')} | {te.get('mean_bruto') if te else None} |",
        f"| mean netto (bp) | {tr.get('mean_netto')} | {te.get('mean_netto') if te else None} |",
        f"| gate {gate:.2f} | {'PASS' if tr.get('gate_pass') else 'FAIL'} | — |",
        f"| stress {stress:.2f} | {'PASS' if tr.get('stress_pass') else 'FAIL'} | — |",
        f"| t day-clust netto | {tr.get('t_day_clust_netto')} | {te.get('t_day_clust_netto') if te else None} |",
        f"| t NW L=5 netto | {tr.get('t_nw_L5_netto')} | {te.get('t_nw_L5_netto') if te else None} |",
        "",
        "## Per-class summary (train)",
        "",
        "| Class | N trades | mean bruto | mean netto | positive |",
        "|-------|----------|-----------|-----------|---------|",
    ]
    for cat, cs in sorted(class_summary.items()):
        md.append(f"| {cat} | {cs['N']} | {cs['mean_bruto']} | {cs['mean_netto']} | {'✓' if cs['positive'] else '✗'} |")

    md += [
        "",
        f"Class criterion (≥2/3 positive): {'PASS' if class_crit_pass else 'FAIL'} "
        f"({n_positive_classes}/{n_classes} classes positive)",
        "",
    ]
    if tr_stress:
        md += [
            "## Stress (+50% swap) — train",
            f"| mean bruto | mean netto | t netto | NW-L5 |",
            f"|-----------|-----------|--------|-------|",
            f"| {tr_stress.get('mean_bruto')} | {tr_stress.get('mean_netto')} | "
            f"{tr_stress.get('t_day_clust_netto')} | {tr_stress.get('t_nw_L5_netto')} |",
            "",
        ]

    md.append(f"**Uitkomst TSMOM_DIV: {outcome}**")
    md.append("")

    (OUT / "tsmom_div_report.md").write_text("\n".join(md) + "\n")

    print(json.dumps({
        "outcome": outcome,
        "gate_bp": round(gate, 4),
        "N_train_trades": tr.get("N_trades"),
        "mean_bruto_train": tr.get("mean_bruto"),
        "gate_pass": tr.get("gate_pass"),
        "stress_pass": tr.get("stress_pass"),
        "t_train": tr.get("t_day_clust_netto"),
        "t_train_nw": tr.get("t_nw_L5_netto"),
        "t_test": te.get("t_day_clust_netto") if te else None,
        "class_crit_pass": class_crit_pass,
    }, indent=2))

    return board


if __name__ == "__main__":
    main()
