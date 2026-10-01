#!/usr/bin/env python3
"""PREREG_FTMO_N80 — UKOIL OVN-gap continuation EOD-flat cost-gate + formal.

Frozen rule: PREREG_FTMO_N80.md (Strateeg Faraday 23c3741 / D-092.1 PASS).
UKOILcash; |gap|≥40 bp @08:00 vs prior ≤22:00 close → continuation; flat 17:00 CET.
Stop (formal/gate re-measure): 1.5 × ATR14(H1). Swap=0 (same-day flat).
Gate: 3× RT 2.71 = 8.13 bp. Stress: 1.5×8.13 = 12.20 bp.
Train 2021–2023 / test 2024 if cost-gate PASS. Reserve 2025+ untouched.
FAIL_COST_GATE ≠ trial (C-029 / N78 erratum). No retune.
"""
from __future__ import annotations

import gzip
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n80_prep"

RT = 2.71
GATE = 3.0 * RT          # 8.13
GATE_STRESS = 1.5 * GATE  # 12.195 → 12.20
GAP_TH = 40.0
ATR_N = 14
STOP_MULT = 1.5

TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
TEST_START = pd.Timestamp("2024-01-01")
TEST_END = pd.Timestamp("2024-12-31 23:59:59")
RESERVE_CUT = pd.Timestamp("2025-01-01")
# Warmup for H1 ATR before train
ATR_WARMUP = pd.Timestamp("2020-10-01")


def load_m5(start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    path = ROOT / "data/m5gz/UKOILcash.csv.gz"
    with gzip.open(path, "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["open", "high", "low", "close"]).sort_values("time")
    # hard cut: never use 2025+
    df = df[df["time"] < RESERVE_CUT]
    return df[(df["time"] >= start) & (df["time"] <= end)].reset_index(drop=True)


def h1_atr_series(m5: pd.DataFrame) -> pd.Series:
    """ATR14 on H1 bars from M5; index = H1 bar end time; value usable after bar close."""
    h1 = (
        m5.set_index("time")
        .resample("1h", label="left", closed="left")
        .agg({"open": "first", "high": "max", "low": "min", "close": "last"})
        .dropna()
    )
    tr = pd.concat(
        [
            h1["high"] - h1["low"],
            (h1["high"] - h1["close"].shift()).abs(),
            (h1["low"] - h1["close"].shift()).abs(),
        ],
        axis=1,
    ).max(axis=1)
    atr = tr.rolling(ATR_N, min_periods=ATR_N).mean()
    # shift 1 so ATR at time t uses only completed H1 bars before t
    return atr.shift(1)


def prior_atr_h1(atr: pd.Series, entry_t: pd.Timestamp) -> float:
    """Last available H1 ATR strictly before entry."""
    avail = atr[atr.index < entry_t].dropna()
    if avail.empty:
        return float("nan")
    return float(avail.iloc[-1])


def close_map_le_2200(m5: pd.DataFrame) -> dict:
    """Prior reference: last M5 close ≤ 22:00 CET per calendar day."""
    m5 = m5.copy()
    m5["day"] = m5["time"].dt.normalize()
    out = {}
    for day, g in m5.groupby("day"):
        ref = g[g["time"] <= day + pd.Timedelta(hours=22)]
        if len(ref):
            out[day] = float(ref.iloc[-1]["close"])
    return out


def simulate_path(
    g: pd.DataFrame,
    entry_t: pd.Timestamp,
    side: int,
    stop: float,
    flat_h: int = 17,
) -> tuple[float, str] | None:
    fl = entry_t.normalize() + pd.Timedelta(hours=flat_h)
    rest = g[(g["time"] > entry_t) & (g["time"] <= fl)]
    if rest.empty:
        return None
    for _, row in rest.iterrows():
        if side == 1 and float(row["low"]) <= stop:
            return float(stop), "stop"
        if side == -1 and float(row["high"]) >= stop:
            return float(stop), "stop"
    return float(rest.iloc[-1]["close"]), "flat"


def sim_n80(m5: pd.DataFrame, atr_h1: pd.Series) -> pd.DataFrame:
    """Frozen N80: gap cont @08:00; stop 1.5×ATR14(H1); flat 17:00; ≤1 trade/day."""
    m5 = m5.copy()
    m5["day"] = m5["time"].dt.normalize()
    cmap = close_map_le_2200(m5)
    days = sorted(m5["day"].unique())
    trades = []
    for i, day in enumerate(days):
        if i == 0:
            continue
        c_ref = cmap.get(days[i - 1])
        if not c_ref or c_ref <= 0:
            continue
        g = m5[m5["day"] == day]
        bar = g[g["time"] == day + pd.Timedelta(hours=8)]
        if bar.empty:
            after = g[
                (g["time"] >= day + pd.Timedelta(hours=8))
                & (g["time"] <= day + pd.Timedelta(hours=8, minutes=15))
            ]
            if after.empty:
                continue
            b = after.iloc[0]
        else:
            b = bar.iloc[0]
        mid = 0.5 * (float(b["high"]) + float(b["low"])) or float(b["close"])
        gap_bp = 1e4 * (mid / c_ref - 1.0)
        if abs(gap_bp) < GAP_TH:
            continue
        side = 1 if gap_bp >= GAP_TH else -1
        entry = float(b["close"])
        entry_t = b["time"]
        atr_v = prior_atr_h1(atr_h1, entry_t)
        if not (atr_v == atr_v) or atr_v <= 0:
            continue
        stop = entry - side * STOP_MULT * atr_v
        sim = simulate_path(g, entry_t, side, stop, 17)
        if sim is None:
            continue
        exit_px, reason = sim
        bruto = side * 1e4 * (exit_px - entry) / entry
        trades.append(
            {
                "date": str(day.date()),
                "year": int(day.year),
                "side": side,
                "gap_bp": round(gap_bp, 4),
                "entry": entry,
                "exit": exit_px,
                "hit": reason,
                "atr_h1": atr_v,
                "bruto_bp": bruto,
                "netto_bp": bruto - RT,
                "rt": RT,
            }
        )
    return pd.DataFrame(trades)


def t_plain(x) -> float:
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if len(x) <= 2 or x.std(ddof=1) <= 0:
        return float("nan")
    return float(x.mean() / x.std(ddof=1) * math.sqrt(len(x)))


def t_nw(x, L: int = 5) -> float:
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
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


def summarize(df: pd.DataFrame, label: str) -> dict:
    if df is None or df.empty:
        return {"window": label, "N": 0, "gate_pass": False, "mean_bruto": None}
    n = int(len(df))
    mean_b = float(df["bruto_bp"].mean())
    mean_n = float(df["netto_bp"].mean())
    day = df.groupby("date")["netto_bp"].sum()
    day_b = df.groupby("date")["bruto_bp"].sum()
    # chronological halves (PREREG: beide helften mean > 0)
    mid = n // 2
    h1 = df.iloc[:mid]
    h2 = df.iloc[mid:]
    years = {
        str(int(y)): {
            "N": int(len(sub)),
            "mean_bruto": round(float(sub["bruto_bp"].mean()), 4),
        }
        for y, sub in df.groupby("year")
    }
    return {
        "window": label,
        "N": n,
        "mean_bruto": round(mean_b, 4),
        "median_bruto": round(float(df["bruto_bp"].median()), 4),
        "mean_netto": round(mean_n, 4),
        "gate": GATE,
        "stress": round(GATE_STRESS, 4),
        "gate_pass": bool(mean_b >= GATE and n >= 150),
        "stress_pass": bool(mean_b >= GATE_STRESS),
        "t_day_clust_netto": round(t_plain(day.values), 4),
        "t_nw_L5_netto": round(t_nw(day.values, 5), 4),
        "t_day_clust_bruto": round(t_plain(day_b.values), 4),
        "t_nw_L5_bruto": round(t_nw(day_b.values, 5), 4),
        "mean_h1_bruto": round(float(h1["bruto_bp"].mean()), 4) if len(h1) else None,
        "mean_h2_bruto": round(float(h2["bruto_bp"].mean()), 4) if len(h2) else None,
        "mean_h1_netto": round(float(h1["netto_bp"].mean()), 4) if len(h1) else None,
        "mean_h2_netto": round(float(h2["netto_bp"].mean()), 4) if len(h2) else None,
        "stop_share": round(float((df["hit"] == "stop").mean()), 4),
        "n_long": int((df["side"] == 1).sum()),
        "n_short": int((df["side"] == -1).sum()),
        "date_min": df["date"].min(),
        "date_max": df["date"].max(),
        "years": years,
    }


def decide(tr: dict, te: dict | None) -> str:
    if not tr.get("gate_pass"):
        return "FAIL_COST_GATE"
    halves_ok = (
        (tr.get("mean_h1_bruto") or 0) > 0
        and (tr.get("mean_h2_bruto") or 0) > 0
    )
    train_t = (
        tr.get("N", 0) >= 150
        and tr.get("mean_netto", 0) > 0
        and halves_ok
        and tr.get("t_day_clust_netto") is not None
        and tr.get("t_nw_L5_netto") is not None
        and tr["t_day_clust_netto"] >= 2.0
        and tr["t_nw_L5_netto"] >= 2.0
    )
    test_t = (
        te is not None
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


def run_window(start, end, atr_load_start=None) -> pd.DataFrame:
    load_start = atr_load_start or start
    m5_all = load_m5(load_start, end)
    atr = h1_atr_series(m5_all)
    m5 = m5_all[(m5_all["time"] >= start) & (m5_all["time"] <= end)].reset_index(drop=True)
    return sim_n80(m5, atr)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("N80: train 2021–2023…", flush=True)
    train = run_window(TRAIN_START, TRAIN_END, atr_load_start=ATR_WARMUP)
    train.to_csv(OUT / "n80_train.csv", index=False)
    tr = summarize(train, "train")

    te = None
    if tr.get("gate_pass"):
        print("N80: test 2024…", flush=True)
        test = run_window(TEST_START, TEST_END, atr_load_start=pd.Timestamp("2023-10-01"))
        test.to_csv(OUT / "n80_test.csv", index=False)
        te = summarize(test, "test")

    outcome = decide(tr, te)
    # C-029: only cost-gate PASS counts as formal trial
    counts_as_trial = bool(tr.get("gate_pass"))

    board = {
        "idea": "N80_UKOIL_OVN_GAP_CONT",
        "prereg": "PREREG_FTMO_N80.md",
        "source_strateeg": "23c3741",
        "branch_source": "claude/trusting-faraday-34tsmg",
        "instrument": "UKOILcash",
        "rt_bp": RT,
        "gate_bp": GATE,
        "stress_bp": round(GATE_STRESS, 4),
        "outcome": outcome,
        "counts_as_trial": counts_as_trial,
        "train": tr,
        "test": te,
        "reserve_2025": "untouched",
        "no_retune": True,
        "note": "pre-screen D-092.1 omitted stop (mean +12.26); gate re-measure includes 1.5×ATR14(H1)",
    }
    (OUT / "n80_board.json").write_text(json.dumps(board, indent=2) + "\n")

    md = [
        "# PREREG_FTMO_N80 — cost-gate + formal train/test",
        "",
        "PREREG: `PREREG_FTMO_N80.md` (Strateeg Faraday `23c3741` / D-092.1 PASS).",
        "Rule: UKOIL |gap|≥40 bp @08:00 vs prior ≤22:00 → continuation; stop 1.5×ATR14(H1); flat 17:00 CET; swap=0.",
        f"Gate: 3× RT {RT} = **{GATE} bp**. Stress = **{GATE_STRESS:.2f} bp**.",
        "Train 2021–2023 / test 2024 (if gate PASS). Reserve 2025→ **untouched**. No retune.",
        "D-092.1 pre-screen (no stop) mean +12.26 bp — **not** automatic PASS; re-measure with stop.",
        "",
        f"**Uitkomst: {outcome}** (counts_as_trial={counts_as_trial})",
        "",
        "| Metric | Train | Test |",
        "|--------|------:|-----:|",
        f"| N | {tr.get('N')} | {None if not te else te.get('N')} |",
        f"| mean bruto | {tr.get('mean_bruto')} | {None if not te else te.get('mean_bruto')} |",
        f"| mean netto | {tr.get('mean_netto')} | {None if not te else te.get('mean_netto')} |",
        f"| gate {GATE} | {'PASS' if tr.get('gate_pass') else 'FAIL'} | — |",
        f"| stress {GATE_STRESS:.2f} | {'PASS' if tr.get('stress_pass') else 'FAIL'} | — |",
        f"| t day-clust netto | {tr.get('t_day_clust_netto')} | {None if not te else te.get('t_day_clust_netto')} |",
        f"| t NW L=5 netto | {tr.get('t_nw_L5_netto')} | {None if not te else te.get('t_nw_L5_netto')} |",
        f"| t day-clust bruto | {tr.get('t_day_clust_bruto')} | {None if not te else te.get('t_day_clust_bruto')} |",
        f"| mean h1/h2 bruto | {tr.get('mean_h1_bruto')}/{tr.get('mean_h2_bruto')} | — |",
        f"| stop share | {tr.get('stop_share')} | {None if not te else te.get('stop_share')} |",
        f"| long/short n | {tr.get('n_long')}/{tr.get('n_short')} | — |",
        "",
        "Year-split train mean bruto: "
        + ", ".join(
            f"{y}: n={s['N']} {s['mean_bruto']:+.4f}"
            for y, s in sorted((tr.get("years") or {}).items())
        ),
        "",
        "C-029: FAIL_COST_GATE ≠ trial (N78 erratum). Append TRIALS / bump TRIAL_COUNT only if counts_as_trial.",
        "",
    ]
    (OUT / "n80_report.md").write_text("\n".join(md) + "\n")
    print(json.dumps(board, indent=2), flush=True)
    return board


if __name__ == "__main__":
    main()
