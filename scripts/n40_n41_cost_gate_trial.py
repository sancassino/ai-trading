#!/usr/bin/env python3
"""N40 (GER40cash mid-morning mom) + N41 (US30cash EU→US cont) formal cost-gate/stress/t.
PREREG 1f84693. Train 2021-2023. Times = Amsterdam wall clock.
N40: mom=(C_1200-C_0930)/C_0930 ×1e4; |mom|≥40 → entry 12:00 close; stop 1×ATR14; flat 14:00 CET.
N41: eu=(C_1500-C_0900)/C_0900 ×1e4; |eu|≥40 → entry 15:30 close; stop 1×ATR14; flat 17:00 CET.
"""
from __future__ import annotations
import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R2" / "n40_n41_prep"
ATR_N = 14
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")


def load_m5(symbol: str) -> pd.DataFrame:
    path = ROOT / "data" / "m5gz" / f"{symbol}.csv.gz"
    with gzip.open(path, "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    if "time" not in df.columns:
        with gzip.open(path, "rt") as f:
            for line in f:
                if not line.startswith("#"):
                    break
            df = pd.read_csv(f, sep=";", names=["time", "open", "high", "low", "close", "spread"])
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["close"]).sort_values("time")
    return df[(df["time"] >= TRAIN_START) & (df["time"] <= TRAIN_END)].reset_index(drop=True)


def atr_series(m5: pd.DataFrame) -> pd.Series:
    g = m5.set_index("time").resample("1D").agg(
        high=("high", "max"), low=("low", "min"), close=("close", "last")
    ).dropna()
    tr = pd.concat([
        g["high"] - g["low"],
        (g["high"] - g["close"].shift()).abs(),
        (g["low"] - g["close"].shift()).abs(),
    ], axis=1).max(axis=1)
    g["atr"] = tr.rolling(ATR_N).mean()
    return g["atr"]


def prior_atr(atr: pd.Series, day: pd.Timestamp) -> float:
    for k in range(1, 10):
        a = atr.get(day - pd.Timedelta(days=k), float("nan"))
        if not pd.isna(a):
            return float(a)
    return float("nan")


def bar_at(g: pd.DataFrame, day0: pd.Timestamp, h: int, m: int = 0):
    t = day0 + pd.Timedelta(hours=h, minutes=m)
    rows = g[g["time"] == t]
    return None if rows.empty else rows.iloc[0]


def manage(g: pd.DataFrame, day0: pd.Timestamp, entry_t: pd.Timestamp,
           entry: float, side: int, stop: float, flat_h: int, flat_m: int = 0):
    flat_t = day0 + pd.Timedelta(hours=flat_h, minutes=flat_m)
    path = g[(g["time"] > entry_t) & (g["time"] <= flat_t)]
    exit_px = float(path.iloc[-1]["close"]) if len(path) else entry
    if not pd.isna(stop):
        for _, row in path.iterrows():
            hi, lo = float(row["high"]), float(row["low"])
            if side == 1 and lo <= stop:
                return stop, "stop"
            if side == -1 and hi >= stop:
                return stop, "stop"
    return exit_px, "time"


def sim_n40(g: pd.DataFrame, atr: float):
    if pd.isna(atr) or atr <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b0930 = bar_at(g, day0, 9, 30)
    b1200 = bar_at(g, day0, 12, 0)
    if b0930 is None or b1200 is None:
        return None
    c0930 = float(b0930["close"])
    c1200 = float(b1200["close"])
    if c0930 <= 0:
        return None
    mom = 1e4 * (c1200 - c0930) / c0930
    if abs(mom) < 40:
        return None
    side = 1 if mom > 0 else -1
    entry = c1200
    entry_t = day0 + pd.Timedelta(hours=12, minutes=0)
    stop = entry - side * atr
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 14, 0)
    pnl = side * 1e4 * (exit_px - entry) / entry
    return {"date": str(day0.date()), "bruto_bp": round(pnl, 4), "side": side}


def sim_n41(g: pd.DataFrame, atr: float):
    if pd.isna(atr) or atr <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b0900 = bar_at(g, day0, 9, 0)
    b1500 = bar_at(g, day0, 15, 0)
    b1530 = bar_at(g, day0, 15, 30)
    if b0900 is None or b1500 is None or b1530 is None:
        return None
    c0900 = float(b0900["close"])
    c1500 = float(b1500["close"])
    if c0900 <= 0:
        return None
    eu = 1e4 * (c1500 - c0900) / c0900
    if abs(eu) < 40:
        return None
    side = 1 if eu > 0 else -1
    entry = float(b1530["close"])
    entry_t = day0 + pd.Timedelta(hours=15, minutes=30)
    stop = entry - side * atr
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 17, 0)
    pnl = side * 1e4 * (exit_px - entry) / entry
    return {"date": str(day0.date()), "bruto_bp": round(pnl, 4), "side": side}


def nw_t(values: list[float], dates: list[str], L: int = 5) -> float:
    day_df = pd.DataFrame({"date": dates, "x": values})
    day_means = day_df.groupby("date")["x"].mean().values
    n = len(day_means)
    if n < 2:
        return 0.0
    mu = float(np.mean(day_means))
    diffs = day_means - mu
    gamma0 = float(np.mean(diffs ** 2))
    nw_var = gamma0
    for l in range(1, L + 1):
        if l >= n:
            break
        gamma_l = float(np.mean(diffs[l:] * diffs[: n - l]))
        nw_var += 2 * (1 - l / (L + 1)) * gamma_l
    if nw_var <= 0:
        return 0.0
    se = float(np.sqrt(max(nw_var / n, 1e-30)))
    return mu / se if se > 0 else 0.0


def run_sleeve(name: str, symbol: str, rt: float, sim_fn) -> dict:
    m5 = load_m5(symbol)
    atr = atr_series(m5)
    gate = 3 * rt
    stress_gate = 3 * rt * 1.5

    trades = []
    for day, g in m5.groupby(m5["time"].dt.normalize()):
        if len(g) < 5:
            continue
        a = prior_atr(atr, day)
        r = sim_fn(g.copy(), a)
        if r:
            r["rt"] = rt
            trades.append(r)

    N = len(trades)
    if N == 0:
        return {"sleeve": name, "N": 0, "mean_bruto": None, "gate": gate,
                "stress_gate": stress_gate, "verdict": "FAIL_NO_TRADES", "trades": []}

    bruto = [t["bruto_bp"] for t in trades]
    net = [b - 2 * rt for b in bruto]
    mean_b = float(np.mean(bruto))

    gate_ok = mean_b >= gate
    if not gate_ok:
        return {"sleeve": name, "N": N, "mean_bruto": round(mean_b, 4), "rt": rt,
                "gate": gate, "stress_gate": stress_gate, "gate_ok": False,
                "t_nw": None, "verdict": "FAIL_GATE", "trades": trades}

    stress_ok = mean_b >= stress_gate

    # Always compute t once cost-gate passes (stress is advisory; trial counted either way)
    dates = [t["date"] for t in trades]
    t_stat = round(nw_t(net, dates), 4)
    t_ok = t_stat >= 2.0

    if not stress_ok:
        verdict = "FAIL_STRESS_then_FAIL_T" if not t_ok else "FAIL_STRESS_then_PASS_T"
    else:
        verdict = "PASS" if t_ok else "FAIL_T"

    return {"sleeve": name, "N": N, "mean_bruto": round(mean_b, 4), "rt": rt,
            "gate": gate, "stress_gate": stress_gate, "gate_ok": True,
            "stress_ok": stress_ok, "t_nw": t_stat, "verdict": verdict, "trades": trades}


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    configs = [
        ("N40", "GER40cash", 0.72, sim_n40),
        ("N41", "US30cash", 0.45, sim_n41),
    ]

    all_results = {}
    for name, sym, rt, fn in configs:
        print(f"Running {name} ({sym})...")
        r = run_sleeve(name, sym, rt, fn)
        trades = r.pop("trades")
        all_results[name] = r
        pd.DataFrame(trades).to_csv(OUT_DIR / f"{name.lower()}_train.csv", index=False)
        print(f"  N={r['N']} mean={r['mean_bruto']} gate={r['gate']} "
              f"stress={r['stress_gate']} t={r.get('t_nw')} → {r['verdict']}")

    (OUT_DIR / "n40_n41_board.json").write_text(json.dumps(all_results, indent=2))

    md = [
        "# N40 + N41 Formal Cost-Gate / Stress / t — Train 2021–2023",
        f"\nPREREG 1f84693 | 2021-01-01…2023-12-31 | Reserve 2025→ onaangeroerd.\n",
        "| Sleeve | Instrument | N | mean bruto | gate | stress gate | NW-t (L=5) | Uitkomst |",
        "|--------|------------|--:|----------:|-----:|------------:|-----------:|----------|",
    ]
    for name, r in all_results.items():
        sym = {"N40": "GER40cash", "N41": "US30cash"}[name]
        t_str = str(r.get("t_nw", "—")) if r.get("t_nw") is not None else "—"
        md.append(f"| **{name}** | {sym} | {r['N']} | {r['mean_bruto']} bp | "
                  f"{r['gate']} | {r['stress_gate']} | {t_str} | **{r['verdict']}** |")
    (OUT_DIR / "n40_n41_report.md").write_text("\n".join(md))

    return all_results


if __name__ == "__main__":
    main()
