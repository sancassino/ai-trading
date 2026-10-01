#!/usr/bin/env python3
"""PREREG_FTMO_N18 — US500 OVN Gap Cont cost-gate + formal train t (Uitvoerder-2).

Frozen rule from PREREG_FTMO_N18.md @ c715e06 (CTO aaaecad / Strateeg 50561ab).
Train 2021–2023 only. Test 2024 and reserve 2025+ untouched (PREREG §4/§5).

Cost-gate: mean bruto ≥ 2.34 bp (3× RT 0.78); stress 3.51 bp (+50% RT).
Formal: day-clustered t + Newey-West L=5 on day-sum netto_bp; threshold t≥2.0.
"""
from __future__ import annotations

import gzip
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "R2" / "n18_prep"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
RT = 0.78
GATE = 3.0 * RT           # 2.34
GATE_STRESS = 3.0 * 1.17  # 3.51 (+50% RT)
ATR_N = 14
GAP_THR = 50.0


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
    for k in range(1, 10):
        prev = day - pd.Timedelta(days=k)
        g = m5_by_date.get(prev.date())
        if g is None or g.empty:
            continue
        b = bar_at(g, prev.normalize(), 22, 0)
        if b is not None:
            return float(b["close"])
        cand = g[g["time"] <= prev.normalize() + pd.Timedelta(hours=22)]
        if not cand.empty and cand.iloc[-1]["time"].hour >= 15:
            return float(cand.iloc[-1]["close"])
    return None


def simulate_path(
    g: pd.DataFrame,
    entry_t: pd.Timestamp,
    side: int,
    stop: float,
    flat_h: int,
    flat_m: int,
) -> tuple[float, str] | None:
    fl = entry_t.normalize() + pd.Timedelta(hours=flat_h, minutes=flat_m)
    rest = g[(g["time"] > entry_t) & (g["time"] <= fl)]
    if rest.empty:
        return None
    for _, row in rest.iterrows():
        if side == 1 and row["low"] <= stop:
            return float(stop), "stop"
        if side == -1 and row["high"] >= stop:
            return float(stop), "stop"
    return float(rest.iloc[-1]["close"]), "flat"


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


def sim_n18(m5: pd.DataFrame, atr: pd.Series) -> pd.DataFrame:
    """PREREG §2: gap ≥ ±50 bp vs prior 22:00; cont @15:30; stop 1.5 ATR; flat 18:30."""
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
        if gap_bp >= GAP_THR:
            side = 1
        elif gap_bp <= -GAP_THR:
            side = -1
        else:
            continue
        entry = p_open
        entry_t = open_bar["time"]
        stop = entry - side * 1.5 * atr_v
        sim = simulate_path(g, entry_t, side, stop, 18, 30)
        if sim is None:
            continue
        exit_px, reason = sim
        bruto = bp_ret(entry, exit_px, side)
        trades.append(
            dict(
                date=str(day),
                year=day0.year,
                side=side,
                gap_bp=round(gap_bp, 4),
                entry=entry,
                exit=exit_px,
                hit=reason,
                atr=atr_v,
                bruto_bp=bruto,
                netto_bp=bruto - RT,
                rt=RT,
            )
        )
    return pd.DataFrame(trades)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("Loading US500cash…")
    us500 = load_m5("US500cash")
    atr = atr_map(us500)
    df = sim_n18(us500, atr)
    df.to_csv(OUT / "cost_gate_n18_train.csv", index=False)

    n = len(df)
    if n == 0:
        board = {
            "n": 0,
            "outcome": "FAIL_EMPTY",
            "gate": GATE,
            "gate_stress": GATE_STRESS,
            "reserve_2025": "untouched",
            "test_2024": "untouched",
        }
        (OUT / "n18_board.json").write_text(json.dumps(board, indent=2) + "\n")
        print(json.dumps(board, indent=2))
        return board

    mean_bruto = float(df["bruto_bp"].mean())
    median_bruto = float(df["bruto_bp"].median())
    mean_netto = float(df["netto_bp"].mean())
    stop_share = float((df["hit"] == "stop").mean())
    gate_pass = mean_bruto >= GATE
    stress_pass = mean_bruto >= GATE_STRESS

    day = df.groupby("date")["netto_bp"].sum()
    day_bruto = df.groupby("date")["bruto_bp"].sum()
    t_day = t_plain(day.values)
    t_nw5 = t_nw(day.values, L=5)
    t_day_bruto = t_plain(day_bruto.values)
    t_nw5_bruto = t_nw(day_bruto.values, L=5)

    t_ok = (
        t_nw5 == t_nw5
        and t_day == t_day
        and t_nw5 >= 2.0
        and t_day >= 2.0
        and mean_netto > 0
        and n >= 150
    )

    if not gate_pass:
        outcome = "FAIL_COST_GATE"
    elif not stress_pass:
        outcome = "FAIL_STRESS_then_" + ("PASS_T" if t_ok else "FAIL_T")
    elif t_ok:
        outcome = "PASS_CANDIDATE"
    else:
        outcome = "FAIL_T"

    year_split = {}
    for y, g in df.groupby("year"):
        year_split[str(int(y))] = {
            "n": int(len(g)),
            "mean_bruto_bp": round(float(g["bruto_bp"].mean()), 4),
            "median_bruto_bp": round(float(g["bruto_bp"].median()), 4),
        }

    board = {
        "idea": "N18_US500_OVN_GAP_CONT",
        "prereg": "PREREG_FTMO_N18.md",
        "prereg_sha_local": "c715e06",
        "source_cto": "aaaecad",
        "source_strateeg": "50561ab",
        "n": n,
        "mean_bruto_bp": round(mean_bruto, 4),
        "median_bruto_bp": round(median_bruto, 4),
        "mean_netto_bp": round(mean_netto, 4),
        "p25_bruto": round(float(np.percentile(df["bruto_bp"], 25)), 4),
        "p75_bruto": round(float(np.percentile(df["bruto_bp"], 75)), 4),
        "stop_share": round(stop_share, 4),
        "rt_bp": RT,
        "gate_3x_rt": GATE,
        "gate_stress": GATE_STRESS,
        "pass_gate": bool(gate_pass),
        "pass_stress": bool(stress_pass),
        "N_days": int(len(day)),
        "t_day_clustered_netto": None if t_day != t_day else round(float(t_day), 4),
        "t_nw_L5_netto": None if t_nw5 != t_nw5 else round(float(t_nw5), 4),
        "t_day_clustered_bruto": None if t_day_bruto != t_day_bruto else round(float(t_day_bruto), 4),
        "t_nw_L5_bruto": None if t_nw5_bruto != t_nw5_bruto else round(float(t_nw5_bruto), 4),
        "mean_day_netto_bp": round(float(day.mean()), 4),
        "skew_day_netto": round(float(day.skew()), 4),
        "t_ok": bool(t_ok),
        "outcome": outcome,
        "year_split_mean_bruto": year_split,
        "date_min": df["date"].iloc[0],
        "date_max": df["date"].iloc[-1],
        "reserve_2025": "untouched",
        "test_2024": "untouched",
    }

    (OUT / "n18_board.json").write_text(json.dumps(board, indent=2) + "\n")
    md = [
        "# PREREG_FTMO_N18 — cost-gate + formal train t",
        "",
        f"PREREG landed `c715e06` (CTO `aaaecad` / Strateeg `50561ab`). Train 2021–2023 only.",
        "Rule: overnight gap ≥ ±50 bp vs prior 22:00 CET → continuation @15:30; stop 1.5×ATR14; flat 18:30.",
        "RT=0.78 → gate 2.34 / stress 3.51. Test 2024 + reserve 2025→ untouched.",
        "",
        "| Metric | Value |",
        "|--------|------:|",
        f"| N | {n} |",
        f"| mean bruto bp | {mean_bruto:.4f} |",
        f"| median bruto bp | {median_bruto:.4f} |",
        f"| mean netto bp | {mean_netto:.4f} |",
        f"| gate 3×RT (2.34) | {'PASS' if gate_pass else 'FAIL'} |",
        f"| stress +50% (3.51) | {'PASS' if stress_pass else 'FAIL'} |",
        f"| t day-clust netto | {board['t_day_clustered_netto']} |",
        f"| t NW L=5 netto | {board['t_nw_L5_netto']} |",
        f"| t day-clust bruto | {board['t_day_clustered_bruto']} |",
        f"| t NW L=5 bruto | {board['t_nw_L5_bruto']} |",
        f"| stop share | {stop_share:.4f} |",
        f"| skew day netto | {board['skew_day_netto']} |",
        "",
        "### Year-split mean bruto (caveat PREREG)",
        "",
        "| Year | N | mean bruto | median |",
        "|------|---|------------|--------|",
    ]
    for y, info in sorted(year_split.items()):
        md.append(
            f"| {y} | {info['n']} | {info['mean_bruto_bp']:.4f} | {info['median_bruto_bp']:.4f} |"
        )
    md += [
        "",
        f"## **Uitkomst: {outcome}**",
        "",
        "t_ok = day-clust≥2.0 AND NW L=5≥2.0 AND mean netto>0 AND N≥150 (train only).",
        "",
    ]
    (OUT / "n18_report.md").write_text("\n".join(md) + "\n")
    print(json.dumps(board, indent=2))
    return board


if __name__ == "__main__":
    main()
