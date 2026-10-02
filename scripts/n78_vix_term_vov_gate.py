#!/usr/bin/env python3
"""PREREG_FTMO_N78_VIX_TERM_VOV — cost-gate + formal train/test (Uitvoerder-2).

Frozen rule: PREREG_FTMO_N78_VIX_TERM_VOV.md (Lane-B Faraday 6c9cdca / S2 b765613c).
US100cash only; vov10 / combo; hold 1 trading day (1 overnight long).
Gate D-100: 3 × (0.66 + 1×1.95) = 7.83 bp (bruto mean; swap in threshold).
Train 2021–2023 / test 2024. Reserve 2025+ untouched. No retune.
"""
from __future__ import annotations

import io
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/vix_term_vov_n78"
DAILY = ROOT / "data" / "daily"

# Frozen costs (COSTS_FTMO.csv US100cash)
RT_BP = 0.66
SWAP_LONG_BP = 1.95  # cost per overnight (hostile)
N_NIGHTS = 1
COST_PER_FULL = RT_BP + N_NIGHTS * SWAP_LONG_BP  # 2.61
GATE_BP = 3.0 * COST_PER_FULL  # 7.83
GATE_STRESS_BP = 1.5 * GATE_BP  # 11.745 ≈ 11.75

TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31")
TEST_START = pd.Timestamp("2024-01-01")
TEST_END = pd.Timestamp("2024-12-31")
RESERVE_CUT = pd.Timestamp("2025-01-01")

VOV_WIN = 10
Z_WIN = 252


def load_close(path: Path) -> pd.Series:
    raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    body = [ln for ln in raw if not ln.startswith("#")]
    sep = ";" if body and ";" in body[0] else ","
    df = pd.read_csv(io.StringIO("\n".join(body)), sep=sep)
    cols_l = {c.lower().replace(" ", ""): c for c in df.columns}
    dc = cols_l.get("date") or cols_l.get("observation_date")
    for cand in ("adjclose", "close"):
        if cand in cols_l:
            cc = cols_l[cand]
            break
    else:
        cc = df.columns[-1]
    s = pd.Series(
        pd.to_numeric(df[cc], errors="coerce").values,
        index=pd.to_datetime(df[dc].astype(str).str.replace(".", "-", regex=False)),
        name=path.stem,
    )
    s = s[~s.index.duplicated(keep="last")].sort_index().dropna()
    # hard cut: never use 2025+ for signals or PnL
    s = s[s.index < RESERVE_CUT]
    return s


def zscore(s: pd.Series, win: int) -> pd.Series:
    mu = s.rolling(win, min_periods=max(20, win // 3)).mean()
    sd = s.rolling(win, min_periods=max(20, win // 3)).std(ddof=0)
    return (s - mu) / sd.replace(0, np.nan)


def build_positions() -> pd.DataFrame:
    """Signal from Yahoo VIX*; PnL on FTMO US100cash. Combo / vov10 frozen."""
    v9 = load_close(DAILY / "VIX9D.csv")
    v3 = load_close(DAILY / "VIX3M.csv")
    vix = load_close(DAILY / "VIX.csv")
    px = load_close(DAILY / "US100cash.csv")

    term = (v9 / v3).dropna()
    dvix = vix.diff().abs()
    vov = dvix.rolling(VOV_WIN, min_periods=5).mean()
    vov_z = zscore(vov, Z_WIN)

    df = pd.concat(
        {
            "term": term,
            "vov_z": vov_z,
            "close": px,
            "ret1": px.pct_change().shift(-1),
        },
        axis=1,
        sort=True,
    ).dropna()

    pos = pd.Series(0.0, index=df.index)
    stress = (df["term"] > 1.0) | (df["vov_z"] > 1.25)
    calm = (df["term"] < 0.90) & (df["vov_z"] < -0.25)
    pos[stress] = 1.0
    pos[calm & ~stress] = 0.5
    df["position"] = pos
    df["bruto_bp"] = df["position"] * df["ret1"] * 1e4
    # costs scale with |position|; 1 overnight long
    abs_pos = df["position"].abs()
    df["rt_bp"] = abs_pos * RT_BP
    df["swap_cost_bp"] = abs_pos * SWAP_LONG_BP * N_NIGHTS
    df["cost_bp"] = df["rt_bp"] + df["swap_cost_bp"]
    df["netto_bp"] = df["bruto_bp"] - df["cost_bp"]
    df["year"] = df.index.year
    return df


def window_slice(df: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    m = (df.index >= start) & (df.index <= end) & (df["position"] != 0)
    return df.loc[m].copy()


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
        return {"label": label, "N": 0, "gate_3x": False, "mean_bruto_bp": None}

    n = int(len(df))
    mean_bruto = float(df["bruto_bp"].mean())
    mean_netto = float(df["netto_bp"].mean())
    mean_cost = float(df["cost_bp"].mean())
    gate_3x = bool(mean_bruto >= GATE_BP and n >= 150)

    # day-clustered: already 1 trade/day; series = trade days in order
    daily_bruto = df["bruto_bp"].values
    daily_netto = df["netto_bp"].values

    dates = list(df.index)
    mid = len(dates) // 2
    h1 = df.iloc[:mid]
    h2 = df.iloc[mid:]

    by_year = {
        str(y): round(float(g["bruto_bp"].mean()), 4)
        for y, g in df.groupby("year")
    }

    def safe_mean(part, col):
        return round(float(part[col].mean()), 4) if len(part) > 0 else None

    return {
        "label": label,
        "N": n,
        "mean_bruto_bp": round(mean_bruto, 4),
        "mean_netto_bp": round(mean_netto, 4),
        "mean_cost_bp": round(mean_cost, 4),
        "gate_threshold_bp": GATE_BP,
        "gate_3x": gate_3x,
        "stress_threshold_bp": round(GATE_STRESS_BP, 4),
        "stress_pass": bool(mean_bruto >= GATE_STRESS_BP),
        "t_day_clust_bruto": round(t_plain(daily_bruto), 4),
        "t_nw_L5_bruto": round(t_nw(daily_bruto, 5), 4),
        "t_day_clust_netto": round(t_plain(daily_netto), 4),
        "t_nw_L5_netto": round(t_nw(daily_netto, 5), 4),
        "mean_h1_bruto": safe_mean(h1, "bruto_bp"),
        "mean_h2_bruto": safe_mean(h2, "bruto_bp"),
        "mean_h1_netto": safe_mean(h1, "netto_bp"),
        "mean_h2_netto": safe_mean(h2, "netto_bp"),
        "by_year_bruto": by_year,
        "frac_full": round(float((df["position"] == 1.0).mean()), 4),
        "frac_half": round(float((df["position"] == 0.5).mean()), 4),
    }


def decide(tr: dict, te: dict | None) -> str:
    if tr.get("N", 0) < 150 or not tr.get("gate_3x"):
        return "FAIL_COST_GATE"
    # stress is informational / soft stop per PREREG; still run formal t if gate PASS
    # Formal: day-clust t AND NW ≥ 2.0 on netto (U2 standard)
    t_ok = (
        (tr.get("t_day_clust_netto") or 0) >= 2.0
        and (tr.get("t_nw_L5_netto") or 0) >= 2.0
        and (tr.get("mean_netto_bp") or -1) > 0
    )
    if not t_ok:
        return "FAIL_T"
    if te is not None:
        te_ok = (
            te.get("N", 0) >= 50
            and (te.get("t_day_clust_netto") or 0) >= 2.0
            and (te.get("mean_netto_bp") or -1) > 0
            and (te.get("mean_bruto_bp") or -1) >= 0
        )
        if not te_ok:
            return "FAIL_T"
    return "PASS_CANDIDATE"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    full = build_positions()
    train = window_slice(full, TRAIN_START, TRAIN_END)
    test = window_slice(full, TEST_START, TEST_END)

    # export trade rows
    for label, part in (("train", train), ("test", test)):
        out = part.reset_index().rename(columns={"date": "signal_date"})
        out["signal_date"] = out["signal_date"].dt.strftime("%Y-%m-%d")
        cols = [
            "signal_date",
            "year",
            "term",
            "vov_z",
            "position",
            "close",
            "ret1",
            "bruto_bp",
            "rt_bp",
            "swap_cost_bp",
            "cost_bp",
            "netto_bp",
        ]
        out[cols].to_csv(OUT / f"{label}_US100cash.csv", index=False)

    tr = summarize(train, "train")
    te = summarize(test, "test")
    outcome = decide(tr, te)

    # If gate failed, stop before claiming formal; still record metrics
    board = {
        "prereg": "PREREG_FTMO_N78_VIX_TERM_VOV.md",
        "decision": "D-100",
        "c": "C-028",
        "family": "VIX_TERM_VOV",
        "universe": ["US100cash"],
        "rule": "vov10/combo; term=VIX9D/VIX3M; pos +1 if term>1 OR vov_z>1.25 else +0.5 if term<0.90 AND vov_z<-0.25; hold=1d",
        "signal_source": "Yahoo VIX9D/VIX3M/VIX via data/daily/ (Lane-A/C-028 proxy OK)",
        "pnl_source": "FTMO US100cash D1 data/daily/US100cash.csv",
        "gate_bp": GATE_BP,
        "gate_stress_bp": round(GATE_STRESS_BP, 4),
        "costs": {"rt_bp": RT_BP, "swap_long_bp": SWAP_LONG_BP, "n_nights": N_NIGHTS},
        "outcome": outcome,
        "counts_as_trial": True,  # cost-gate STOP still 1 trial (A4/B1; assignment append)
        "reserve_2025": "untouched",
        "train": tr,
        "test": te,
        "d094a": "(b) VIX term/VoV equity timing literature/proxy ≥10y; FTMO US100 tests cost+swap+execution",
        "lane_a_note": "Lane-A NDX bruto 6.80 / day_t 2.91 is NOT a PASS; this run re-measures FTMO US100",
    }
    (OUT / "vix_term_vov_n78_board.json").write_text(json.dumps(board, indent=2) + "\n")

    lines = [
        "# PREREG_FTMO_N78_VIX_TERM_VOV — cost-gate + formal train/test",
        "",
        "PREREG: `PREREG_FTMO_N78_VIX_TERM_VOV.md` (Lane-B Faraday `6c9cdca` / S2 `b765613c`; C-028).",
        "Rule: **vov10 / combo**; US100cash; hold 1d / 1 overnight long.",
        f"Gate D-100: 3×(0.66+1×1.95) = **{GATE_BP} bp**. Stress = **{GATE_STRESS_BP:.2f} bp**.",
        "Train 2021–2023 / test 2024. Reserve 2025→ **untouched**. No retune.",
        "Signal: Yahoo VIX9D/VIX3M/VIX (`data/daily/`). PnL: FTMO US100cash D1.",
        "D-094a (b): proxy history OK for novelty; FTMO re-measure for cost/formal.",
        "",
        f"**Uitkomst: {outcome}** (counts_as_trial={board['counts_as_trial']})",
        "",
        "## Train 2021–2023",
        "",
        "| Metric | Waarde |",
        "|--------|-------:|",
        f"| N (nonzero pos) | {tr.get('N')} |",
        f"| mean bruto bp | {tr.get('mean_bruto_bp')} |",
        f"| mean netto bp | {tr.get('mean_netto_bp')} |",
        f"| mean cost bp | {tr.get('mean_cost_bp')} |",
        f"| gate 7.83 | **{'PASS' if tr.get('gate_3x') else 'FAIL'}** |",
        f"| stress 11.75 | **{'PASS' if tr.get('stress_pass') else 'FAIL'}** |",
        f"| t day-clust bruto / NW | {tr.get('t_day_clust_bruto')} / {tr.get('t_nw_L5_bruto')} |",
        f"| t day-clust netto / NW | {tr.get('t_day_clust_netto')} / {tr.get('t_nw_L5_netto')} |",
        f"| h1/h2 bruto | {tr.get('mean_h1_bruto')} / {tr.get('mean_h2_bruto')} |",
        f"| frac full/half | {tr.get('frac_full')} / {tr.get('frac_half')} |",
        f"| by year bruto | {tr.get('by_year_bruto')} |",
        "",
        "## Test 2024",
        "",
        "| Metric | Waarde |",
        "|--------|-------:|",
        f"| N | {te.get('N')} |",
        f"| mean bruto bp | {te.get('mean_bruto_bp')} |",
        f"| mean netto bp | {te.get('mean_netto_bp')} |",
        f"| t day-clust netto / NW | {te.get('t_day_clust_netto')} / {te.get('t_nw_L5_netto')} |",
        f"| h1/h2 bruto | {te.get('mean_h1_bruto')} / {te.get('mean_h2_bruto')} |",
        "",
    ]
    (OUT / "vix_term_vov_n78_report.md").write_text("\n".join(lines) + "\n")
    print(
        json.dumps(
            {
                "outcome": outcome,
                "train_N": tr.get("N"),
                "train_bruto": tr.get("mean_bruto_bp"),
                "train_netto": tr.get("mean_netto_bp"),
                "gate": tr.get("gate_3x"),
                "stress": tr.get("stress_pass"),
                "t_day_netto": tr.get("t_day_clust_netto"),
                "t_nw_netto": tr.get("t_nw_L5_netto"),
                "t_day_bruto": tr.get("t_day_clust_bruto"),
                "test_N": te.get("N"),
                "test_bruto": te.get("mean_bruto_bp"),
                "test_t_netto": te.get("t_day_clust_netto"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
