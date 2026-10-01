#!/usr/bin/env python3
"""PREREG_FTMO_N40 + N41 — cost-gate (+stress) + formal train/test day-clust t.

Frozen rules from origin/claude/trusting-faraday-34tsmg @ 6ef46a7
(identical to scripts/n38_n40_prescreen.py sim_n40 / n41_n43_prescreen.py sim_n41).

Train 2021–2023; test 2024; reserve 2025→ untouched.
TRIAL_COUNT append on formal t-test (PREREG §Formele test / U2 instructie).
"""
from __future__ import annotations

import gzip
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n40_n41_prep"
ATR_N = 14

SPECS = {
    "N40": {
        "sym": "GER40cash",
        "rt": 0.72,
        "gate": 2.16,
        "stress": 3.24,
        "prereg": "PREREG_FTMO_N40.md",
    },
    "N41": {
        "sym": "US30cash",
        "rt": 0.45,
        "gate": 1.35,
        "stress": 2.025,
        "prereg": "PREREG_FTMO_N41.md",
    },
}

WINDOWS = {
    "train": (pd.Timestamp("2021-01-01"), pd.Timestamp("2023-12-31 23:59:59")),
    "test": (pd.Timestamp("2024-01-01"), pd.Timestamp("2024-12-31 23:59:59")),
}


def load_m5(sym: str, start, end) -> pd.DataFrame:
    path = ROOT / "data" / "m5gz" / f"{sym}.csv.gz"
    with gzip.open(path, "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["open", "high", "low", "close"]).sort_values("time")
    df = df[df["time"].dt.year < 2025]
    return df[(df["time"] >= start) & (df["time"] <= end)].reset_index(drop=True)


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


def bar_at(g, day0, h, m=0):
    t = day0 + pd.Timedelta(hours=h, minutes=m)
    rows = g[g["time"] == t]
    return None if rows.empty else rows.iloc[0]


def manage(g, day0, entry_t, entry, side, stop, flat_h, flat_m=0):
    flat_t = day0 + pd.Timedelta(hours=flat_h, minutes=flat_m)
    path = g[(g["time"] > entry_t) & (g["time"] <= flat_t)]
    if path.empty:
        return entry, "empty"
    exit_px = float(path.iloc[-1]["close"])
    hit = "time"
    for _, row in path.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        if side == 1 and lo <= stop:
            return float(stop), "stop"
        if side == -1 and hi >= stop:
            return float(stop), "stop"
    return exit_px, hit


def sim_n40(g, atr_price):
    """GER40 mid-morning 09:30→12:00 |mom|≥40 → continue 12:00→14:00."""
    if not (atr_price == atr_price) or atr_price <= 0:
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
    if abs(mom) < 40.0:
        return None
    side = 1 if mom > 0 else -1
    entry = c1200
    entry_t = b1200["time"]
    stop = entry - side * atr_price
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 14, 0)
    return dict(
        date=str(day0.date()),
        year=int(day0.year),
        side=side,
        signal_bp=round(mom, 4),
        entry=entry,
        exit=exit_px,
        hit=hit,
        bruto_bp=side * 1e4 * (exit_px - entry) / entry,
    )


def sim_n41(g, atr_price):
    """US30 Europe→US open: eu 09:00→15:00 |eu|≥40 → continue 15:30→17:00."""
    if not (atr_price == atr_price) or atr_price <= 0:
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
    eu_bp = 1e4 * (c1500 - c0900) / c0900
    if abs(eu_bp) < 40.0:
        return None
    side = 1 if eu_bp > 0 else -1
    entry = float(b1530["close"])
    entry_t = b1530["time"]
    stop = entry - side * atr_price
    exit_px, hit = manage(g, day0, entry_t, entry, side, stop, 17, 0)
    return dict(
        date=str(day0.date()),
        year=int(day0.year),
        side=side,
        signal_bp=round(eu_bp, 4),
        entry=entry,
        exit=exit_px,
        hit=hit,
        bruto_bp=side * 1e4 * (exit_px - entry) / entry,
    )


SIMS = {"N40": sim_n40, "N41": sim_n41}


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


def run_sleeve(name: str, start, end, atr_load_start=None):
    spec = SPECS[name]
    load_start = atr_load_start if atr_load_start is not None else start
    m5_all = load_m5(spec["sym"], load_start, end)
    atr = atr_map(m5_all)
    m5 = m5_all[(m5_all["time"] >= start) & (m5_all["time"] <= end)]
    sim = SIMS[name]
    trades = []
    for day, g in m5.groupby(m5["time"].dt.date):
        day0 = pd.Timestamp(day)
        atr_v = prior_atr(atr, day0)
        g = g.sort_values("time")
        r = sim(g, atr_v)
        if r is None:
            continue
        r["netto_bp"] = r["bruto_bp"] - spec["rt"]
        r["rt"] = spec["rt"]
        trades.append(r)
    return pd.DataFrame(trades)


def summarize(df: pd.DataFrame, spec: dict, label: str) -> dict:
    if df is None or df.empty:
        return {"window": label, "N": 0, "outcome_hint": "FAIL_EMPTY"}
    n = len(df)
    mean_b = float(df["bruto_bp"].mean())
    mean_n = float(df["netto_bp"].mean())
    day = df.groupby("date")["netto_bp"].sum()
    day_b = df.groupby("date")["bruto_bp"].sum()
    years = {
        str(int(y)): {
            "N": int(len(sub)),
            "mean_bruto": round(float(sub["bruto_bp"].mean()), 4),
        }
        for y, sub in df.groupby("year")
    }
    return {
        "window": label,
        "N": int(n),
        "mean_bruto": round(mean_b, 4),
        "median_bruto": round(float(df["bruto_bp"].median()), 4),
        "mean_netto": round(mean_n, 4),
        "gate": spec["gate"],
        "stress": spec["stress"],
        "gate_pass": bool(mean_b >= spec["gate"] and n >= 150),
        "stress_pass": bool(mean_b >= spec["stress"]),
        "cost_share": round(spec["rt"] / mean_b, 4) if mean_b > 0 else None,
        "t_day_clust_netto": round(t_plain(day.values), 4),
        "t_nw_L5_netto": round(t_nw(day.values, 5), 4),
        "t_day_clust_bruto": round(t_plain(day_b.values), 4),
        "t_nw_L5_bruto": round(t_nw(day_b.values, 5), 4),
        "stop_share": round(float((df["hit"] == "stop").mean()), 4),
        "n_long": int((df["side"] == 1).sum()),
        "n_short": int((df["side"] == -1).sum()),
        "date_min": df["date"].min(),
        "date_max": df["date"].max(),
        "years": years,
    }


def decide(tr, te):
    if not tr.get("gate_pass"):
        return "FAIL_COST_GATE"
    train_t = (
        tr.get("N", 0) >= 150
        and tr.get("mean_netto", 0) > 0
        and tr.get("t_day_clust_netto") is not None
        and tr.get("t_nw_L5_netto") is not None
        and tr["t_day_clust_netto"] >= 2.0
        and tr["t_nw_L5_netto"] >= 2.0
    )
    test_t = (
        te
        and te.get("N", 0) >= 30
        and te.get("mean_netto", 0) > 0
        and te.get("t_day_clust_netto") is not None
        and te.get("t_nw_L5_netto") is not None
        and te["t_day_clust_netto"] >= 2.0
        and te["t_nw_L5_netto"] >= 2.0
    )
    if not tr.get("stress_pass"):
        return "FAIL_STRESS_then_" + ("PASS_T" if (train_t and test_t) else "FAIL_T")
    if train_t and test_t:
        return "PASS_CANDIDATE"
    return "FAIL_T"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    board = {}
    md = [
        "# PREREG_FTMO_N40 + N41 — cost-gate + formal train/test",
        "",
        "Source: `origin/claude/trusting-faraday-34tsmg` @ `6ef46a7`. "
        "Reserve 2025→ untouched. Frozen rules = n38_n40 / n41_n43 prescreen sims.",
        "",
    ]
    for name in ("N40", "N41"):
        spec = SPECS[name]
        print(f"{name}: train…", flush=True)
        train = run_sleeve(name, *WINDOWS["train"])
        train.to_csv(OUT / f"{name.lower()}_train.csv", index=False)
        tr = summarize(train, spec, "train")
        te = None
        if tr.get("gate_pass"):
            print(f"{name}: test 2024…", flush=True)
            test = run_sleeve(
                name,
                WINDOWS["test"][0],
                WINDOWS["test"][1],
                atr_load_start=pd.Timestamp("2020-10-01"),
            )
            test.to_csv(OUT / f"{name.lower()}_test.csv", index=False)
            te = summarize(test, spec, "test")
        outcome = decide(tr, te)
        board[name] = {
            "prereg": spec["prereg"],
            "sym": spec["sym"],
            "outcome": outcome,
            "train": tr,
            "test": te,
            "reserve_2025": "untouched",
            "counts_as_trial": bool(tr.get("gate_pass")),
        }
        md += [
            f"## {name} ({spec['sym']})",
            "",
            "| Metric | Train | Test |",
            "|--------|------:|-----:|",
            f"| N | {tr.get('N')} | {None if not te else te.get('N')} |",
            f"| mean bruto | {tr.get('mean_bruto')} | {None if not te else te.get('mean_bruto')} |",
            f"| mean netto | {tr.get('mean_netto')} | {None if not te else te.get('mean_netto')} |",
            f"| gate {spec['gate']} | {'PASS' if tr.get('gate_pass') else 'FAIL'} | — |",
            f"| stress {spec['stress']} | {'PASS' if tr.get('stress_pass') else 'FAIL'} | — |",
            f"| t day-clust netto | {tr.get('t_day_clust_netto')} | {None if not te else te.get('t_day_clust_netto')} |",
            f"| t NW L=5 netto | {tr.get('t_nw_L5_netto')} | {None if not te else te.get('t_nw_L5_netto')} |",
            f"| stop share | {tr.get('stop_share')} | {None if not te else te.get('stop_share')} |",
            "",
            "Year-split train mean bruto: "
            + ", ".join(
                f"{y}: n={s['N']} +{s['mean_bruto']}"
                for y, s in sorted((tr.get("years") or {}).items())
            ),
            "",
            f"**Uitkomst {name}: {outcome}**",
            "",
        ]
        print(
            json.dumps(
                {
                    "name": name,
                    "outcome": outcome,
                    "train_N": tr.get("N"),
                    "mean_bruto": tr.get("mean_bruto"),
                    "median_bruto": tr.get("median_bruto"),
                    "gate_pass": tr.get("gate_pass"),
                    "stress_pass": tr.get("stress_pass"),
                    "t_train": tr.get("t_day_clust_netto"),
                    "t_train_nw": tr.get("t_nw_L5_netto"),
                    "t_test": None if not te else te.get("t_day_clust_netto"),
                },
                indent=2,
            ),
            flush=True,
        )

    (OUT / "n40_n41_board.json").write_text(json.dumps(board, indent=2) + "\n")
    (OUT / "n40_n41_report.md").write_text("\n".join(md) + "\n")
    return board


if __name__ == "__main__":
    main()
