#!/usr/bin/env python3
"""PREREG_S2_GBPJPY_EU_MOM — cost-gate (+50% RT stress) + formal train/test t.

Frozen rule from PREREG_S2_GBPJPY_EU_MOM.md @ origin/grok/strateeg-2 6444d30
(identical to scripts/s2_d092_prescreen_cycle0840.py sim_gbpjpy_eu_mom).

Train 2021–2023 cost-gate first. On PASS → formal day-clust t train + test 2024.
Reserve 2025→ ONAANGERAAKT. Same-bar target+stop → stop wins.
"""
from __future__ import annotations

import gzip
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
M5 = ROOT / "data" / "m5gz"
OUT = ROOT / "results" / "R2" / "gbpjpy_eu_mom_prep"
SYM = "GBPJPY"
RT = 1.11  # COSTS_FTMO_alle roundtrip_intraday_bp
GATE = 3.0 * RT  # 3.33
GATE_STRESS = 3.0 * (RT * 1.5)  # 4.995
ATR_N = 14
RISK = 0.0075
RET_THR = 30.0
STOP_K = 0.40
TGT_K = 0.60

WINDOWS = {
    "train": (pd.Timestamp("2021-01-01"), pd.Timestamp("2023-12-31 23:59:59")),
    "test": (pd.Timestamp("2024-01-01"), pd.Timestamp("2024-12-31 23:59:59")),
}


def load_m5(sym: str, start, end) -> pd.DataFrame:
    with gzip.open(M5 / f"{sym}.csv.gz", "rt") as f:
        first = f.readline()
        if first.startswith("#"):
            while True:
                pos = f.tell()
                line = f.readline()
                if not line.startswith("#"):
                    if "time" not in line.lower() and "open" not in line.lower():
                        f.seek(pos)
                    break
        else:
            f.seek(0)
        df = pd.read_csv(
            f, sep=";", header=None, names=["time", "open", "high", "low", "close", "spread"]
        )
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M", errors="coerce")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["time", "close"]).sort_values("time").reset_index(drop=True)
    # Hard skip 2025+ (reserve)
    df = df[df["time"].dt.year < 2025]
    return df[(df["time"] >= start) & (df["time"] <= end)].copy()


def d1_atr_map(df: pd.DataFrame, n: int = ATR_N) -> dict:
    g = df.groupby(df["time"].dt.normalize())
    h, l, c = g["high"].max(), g["low"].min(), g["close"].last()
    prev_c = c.shift(1)
    tr = pd.concat([(h - l), (h - prev_c).abs(), (l - prev_c).abs()], axis=1).max(axis=1)
    atr = tr.rolling(n, min_periods=n).mean().shift(1)
    return {d: float(v) for d, v in atr.items() if pd.notna(v) and v > 0}


def bar_at(g, day0, hh, mm):
    t = day0 + pd.Timedelta(hours=hh, minutes=mm)
    b = g[(g["time"] >= t) & (g["time"] < t + pd.Timedelta(minutes=5))]
    return None if b.empty else b.iloc[0]


def walk_exit(after, side, stop, target=None):
    """Stop checked before target → same-bar both-hit = stop wins (PREREG §1)."""
    if after.empty:
        return None
    exit_px, reason = float(after.iloc[-1]["close"]), "time"
    for _, row in after.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        if side == 1:
            hit_s = lo <= stop
            hit_t = target is not None and hi >= target
            if hit_s and hit_t:
                return stop, "stop_samebar"
            if hit_s:
                return stop, "stop"
            if hit_t:
                return target, "target"
        else:
            hit_s = hi >= stop
            hit_t = target is not None and lo <= target
            if hit_s and hit_t:
                return stop, "stop_samebar"
            if hit_s:
                return stop, "stop"
            if hit_t:
                return target, "target"
    return exit_px, reason


def sim_day(g, atr_map):
    if len(g) < 40:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    atr = atr_map.get(day0)
    if atr is None:
        return None
    b0 = bar_at(g, day0, 8, 0)
    b1130 = bar_at(g, day0, 11, 30)
    if b0 is None or b1130 is None:
        return None
    p_open = float(b0["open"])
    entry = float(b1130["open"])
    if p_open <= 0 or entry <= 0:
        return None
    ret_bp = 1e4 * (entry - p_open) / p_open
    if abs(ret_bp) < RET_THR:
        return None
    side = 1 if ret_bp > 0 else -1
    if side == 1:
        stop = entry - STOP_K * atr
        target = entry + TGT_K * atr
    else:
        stop = entry + STOP_K * atr
        target = entry - TGT_K * atr
    after = g[
        (g["time"] > day0 + pd.Timedelta(hours=11, minutes=30))
        & (g["time"] <= day0 + pd.Timedelta(hours=14, minutes=30))
    ]
    walked = walk_exit(after, side, stop, target)
    if walked is None:
        return None
    exit_px, reason = walked
    bruto = 1e4 * side * (exit_px - entry) / entry
    stop_dist = abs(entry - stop)
    # 0.75% risk → R-multiple on stop; daily account ret approx RISK * bruto/(stop_bp)
    stop_bp = 1e4 * stop_dist / entry if entry else np.nan
    r_mult = (bruto / stop_bp) if stop_bp and stop_bp > 0 else np.nan
    day_ret = RISK * r_mult if r_mult == r_mult else np.nan
    return dict(
        day=str(day0.date()),
        year=int(day0.year),
        side=side,
        ret_signal_bp=round(ret_bp, 4),
        entry=entry,
        exit=exit_px,
        reason=reason,
        atr=atr,
        stop_bp=round(float(stop_bp), 4) if stop_bp == stop_bp else None,
        bruto_bp=float(bruto),
        netto_bp=float(bruto - RT),
        day_ret=float(day_ret) if day_ret == day_ret else None,
    )


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


def run_window(name: str, start, end, atr_source_start=None):
    # Load from atr_source_start (or start) so ATR warm-up / prior days available
    load_start = atr_source_start if atr_source_start is not None else start
    df_all = load_m5(SYM, load_start, end)
    atr = d1_atr_map(df_all)
    df = df_all[(df_all["time"] >= start) & (df_all["time"] <= end)]
    trades = []
    for _, g in df.groupby(df["time"].dt.normalize()):
        r = sim_day(g, atr)
        if r is not None:
            trades.append(r)
    return pd.DataFrame(trades)


def summarize_window(df: pd.DataFrame, label: str) -> dict:
    if df is None or df.empty:
        return {"window": label, "N": 0, "outcome": "FAIL_EMPTY"}
    n = len(df)
    mean_bruto = float(df["bruto_bp"].mean())
    median_bruto = float(df["bruto_bp"].median())
    mean_netto = float(df["netto_bp"].mean())
    cost_share = (RT / mean_bruto) if mean_bruto > 0 else float("inf")
    stop_share = float(df["reason"].isin(["stop", "stop_samebar"]).mean())
    time_share = float((df["reason"] == "time").mean())
    skew = float(pd.Series(df["bruto_bp"]).skew()) if n > 2 else float("nan")
    day = df.groupby("day")["netto_bp"].sum()
    day_bruto = df.groupby("day")["bruto_bp"].sum()
    t_day = t_plain(day.values)
    t_nw5 = t_nw(day.values, L=5)
    t_day_b = t_plain(day_bruto.values)
    t_nw5_b = t_nw(day_bruto.values, L=5)
    # max day dip at 0.75% risk (account fraction)
    day_ret = df.groupby("day")["day_ret"].sum()
    max_dip = float(day_ret.min()) if len(day_ret) else float("nan")
    skew_day = float(day_ret.skew()) if len(day_ret) > 2 else float("nan")
    years = {}
    for y, sub in df.groupby("year"):
        years[str(int(y))] = {
            "N": int(len(sub)),
            "mean_bruto": round(float(sub["bruto_bp"].mean()), 4),
            "median_bruto": round(float(sub["bruto_bp"].median()), 4),
        }
    reasons = {k: int(v) for k, v in df["reason"].value_counts().to_dict().items()}
    return {
        "window": label,
        "N": int(n),
        "mean_bruto": round(mean_bruto, 4),
        "median_bruto": round(median_bruto, 4),
        "mean_netto": round(mean_netto, 4),
        "rt": RT,
        "gate": GATE,
        "gate_stress50": GATE_STRESS,
        "cost_share": round(cost_share, 4) if cost_share != float("inf") else None,
        "stop_share": round(stop_share, 4),
        "time_share": round(time_share, 4),
        "skew_bruto": round(skew, 4) if skew == skew else None,
        "t_day_clust_netto": round(t_day, 4) if t_day == t_day else None,
        "t_nw_L5_netto": round(t_nw5, 4) if t_nw5 == t_nw5 else None,
        "t_day_clust_bruto": round(t_day_b, 4) if t_day_b == t_day_b else None,
        "t_nw_L5_bruto": round(t_nw5_b, 4) if t_nw5_b == t_nw5_b else None,
        "max_day_dip_risk": round(max_dip, 6) if max_dip == max_dip else None,
        "skew_day_ret": round(skew_day, 4) if skew_day == skew_day else None,
        "n_long": int((df["side"] == 1).sum()),
        "n_short": int((df["side"] == -1).sum()),
        "date_min": df["day"].min(),
        "date_max": df["day"].max(),
        "years": years,
        "reasons": reasons,
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("GBPJPY_EU_MOM: loading train…")
    train = run_window("train", *WINDOWS["train"])
    train.to_csv(OUT / "cost_gate_gbpjpy_eu_mom_train.csv", index=False)
    tr = summarize_window(train, "train")

    gate_pass = tr["N"] >= 150 and tr.get("mean_bruto") is not None and tr["mean_bruto"] >= GATE
    stress_pass = (
        tr.get("mean_bruto") is not None and tr["mean_bruto"] >= GATE_STRESS
    )
    cost_share_ok = tr.get("cost_share") is not None and tr["cost_share"] < 0.50

    # Stress as +50% RT on cost share / mean netto under stressed RT
    rt_stress = RT * 1.5
    if tr["N"] > 0:
        mean_netto_stress = float(train["bruto_bp"].mean() - rt_stress)
        cost_share_stress = (
            rt_stress / float(train["bruto_bp"].mean())
            if float(train["bruto_bp"].mean()) > 0
            else float("inf")
        )
    else:
        mean_netto_stress = float("nan")
        cost_share_stress = float("inf")

    # Dual interpretation recorded; decision uses N18/lunch_open convention:
    # mean bruto ≥ 3×(RT×1.5). Also report cost-share-under-stress.
    tr["mean_netto_stress50"] = (
        round(mean_netto_stress, 4) if mean_netto_stress == mean_netto_stress else None
    )
    tr["cost_share_stress50"] = (
        round(cost_share_stress, 4) if cost_share_stress != float("inf") else None
    )
    tr["gate_pass"] = bool(gate_pass)
    tr["stress50_pass_bruto_vs_3x"] = bool(stress_pass)
    tr["cost_share_ok"] = bool(cost_share_ok)
    tr["cost_share_stress50_ok"] = bool(
        cost_share_stress != float("inf") and cost_share_stress < 0.50
    )

    # Formal windows only if base gate PASS (PREREG: FAIL → STOP, no TRIALS)
    # Stress FAIL still may be recorded as FAIL_STRESS (counts as attempted formal
    # only if base PASS — match N18: FAIL_STRESS_then_* still after base PASS).
    test_sum = None
    if gate_pass:
        print("Base gate PASS — loading test 2024 (ATR warm-up from 2021)…")
        # ATR prior days: load from 2020-ish via train start so 2024 has ATR
        test = run_window(
            "test",
            WINDOWS["test"][0],
            WINDOWS["test"][1],
            atr_source_start=pd.Timestamp("2020-10-01"),
        )
        # Re-run train with same ATR source for consistency of formal numbers
        # (train already computed). Save test trades.
        test.to_csv(OUT / "formal_gbpjpy_eu_mom_test.csv", index=False)
        test_sum = summarize_window(test, "test")

        def t_ok(s):
            return (
                s
                and s.get("N", 0) >= 150
                and s.get("mean_netto") is not None
                and s["mean_netto"] > 0
                and s.get("t_day_clust_netto") is not None
                and s.get("t_nw_L5_netto") is not None
                and s["t_day_clust_netto"] >= 2.0
                and s["t_nw_L5_netto"] >= 2.0
            )

        # Train N≥150 already; test N may be lower — PREREG §4.2 says N≥150 train;
        # for test require mean netto>0 + t≥2 both metrics (N flexible if <150 label underpowered)
        def t_ok_test(s):
            if not s or s.get("N", 0) < 30:
                return False
            return (
                s.get("mean_netto") is not None
                and s["mean_netto"] > 0
                and s.get("t_day_clust_netto") is not None
                and s.get("t_nw_L5_netto") is not None
                and s["t_day_clust_netto"] >= 2.0
                and s["t_nw_L5_netto"] >= 2.0
            )

        train_t = t_ok(tr)
        test_t = t_ok_test(test_sum)
        skew_or_dip = (
            (tr.get("skew_day_ret") is not None and tr["skew_day_ret"] > 0)
            or (
                tr.get("max_day_dip_risk") is not None
                and tr["max_day_dip_risk"] >= -0.015
            )
        )

        # ftmo_ev if we have day returns
        ftmo = None
        try:
            from engine.ftmo import ftmo_ev

            day_rets = (
                train.groupby("day")["day_ret"]
                .sum()
                .dropna()
                .values.astype(float)
            )
            if len(day_rets) >= 30:
                ftmo = ftmo_ev(day_rets, n_paths=2000, seed=42)
                # keep JSON-safe floats
                ftmo = {
                    k: (float(v) if isinstance(v, (int, float, np.floating)) else v)
                    for k, v in ftmo.items()
                    if k
                    in (
                        "p_pass_1",
                        "p_pass_2",
                        "p_survive",
                        "exp_payout_monthly",
                        "net_ev",
                        "fee",
                        "account",
                    )
                }
        except Exception as e:
            ftmo = {"error": str(e)}

        if not stress_pass:
            outcome = "FAIL_STRESS_then_" + (
                "PASS_T" if (train_t and test_t) else "FAIL_T"
            )
        elif train_t and test_t and cost_share_ok and skew_or_dip:
            outcome = "PASS_CANDIDATE"
        else:
            outcome = "FAIL_T"
    else:
        outcome = "FAIL_COST_GATE"
        ftmo = None
        train_t = False
        test_t = False
        skew_or_dip = None

    board = {
        "idea": "GBPJPY_EU_MOM",
        "prereg": "PREREG_S2_GBPJPY_EU_MOM.md",
        "prereg_source": "origin/grok/strateeg-2@6444d30",
        "outcome": outcome,
        "train": tr,
        "test": test_sum,
        "train_t_ok": bool(train_t) if gate_pass else False,
        "test_t_ok": bool(test_t) if gate_pass else False,
        "skew_or_dip_ok": skew_or_dip,
        "ftmo_ev_train": ftmo,
        "reserve_2025": "untouched",
        "trial_counts_if_base_gate_pass": bool(gate_pass),
    }
    (OUT / "gbpjpy_eu_mom_board.json").write_text(json.dumps(board, indent=2) + "\n")

    md = [
        "# PREREG_S2_GBPJPY_EU_MOM — cost-gate + formal train/test",
        "",
        f"PREREG from `grok/strateeg-2` @ `6444d30`. Frozen rule §1. "
        f"Train 2021–2023; test 2024; **reserve 2025→ untouched**.",
        f"RT={RT} → gate {GATE:.2f} / stress {GATE_STRESS:.3f}.",
        "",
        "## Train",
        "",
        "| Metric | Value |",
        "|--------|------:|",
        f"| N | {tr.get('N')} |",
        f"| mean bruto bp | {tr.get('mean_bruto')} |",
        f"| median bruto bp | {tr.get('median_bruto')} |",
        f"| mean netto bp | {tr.get('mean_netto')} |",
        f"| cost share | {tr.get('cost_share')} |",
        f"| gate 3×RT ({GATE:.2f}) | {'PASS' if gate_pass else 'FAIL'} |",
        f"| stress bruto≥3×(RT×1.5) ({GATE_STRESS:.3f}) | {'PASS' if stress_pass else 'FAIL'} |",
        f"| mean netto @ RT×1.5 | {tr.get('mean_netto_stress50')} |",
        f"| cost share @ RT×1.5 | {tr.get('cost_share_stress50')} |",
        f"| t day-clust netto | {tr.get('t_day_clust_netto')} |",
        f"| t NW L=5 netto | {tr.get('t_nw_L5_netto')} |",
        f"| stop share | {tr.get('stop_share')} |",
        f"| time share | {tr.get('time_share')} |",
        f"| skew day-ret | {tr.get('skew_day_ret')} |",
        f"| max day dip (0.75% risk) | {tr.get('max_day_dip_risk')} |",
        "",
        "### Year-split mean bruto",
        "",
        "| Year | N | mean bruto | median |",
        "|------|---|------------|--------|",
    ]
    for y, s in sorted((tr.get("years") or {}).items()):
        md.append(f"| {y} | {s['N']} | {s['mean_bruto']} | {s['median_bruto']} |")
    if test_sum:
        md += [
            "",
            "## Test 2024",
            "",
            "| Metric | Value |",
            "|--------|------:|",
            f"| N | {test_sum.get('N')} |",
            f"| mean bruto bp | {test_sum.get('mean_bruto')} |",
            f"| mean netto bp | {test_sum.get('mean_netto')} |",
            f"| t day-clust netto | {test_sum.get('t_day_clust_netto')} |",
            f"| t NW L=5 netto | {test_sum.get('t_nw_L5_netto')} |",
            f"| cost share | {test_sum.get('cost_share')} |",
        ]
    md += [
        "",
        f"## **Uitkomst: {outcome}**",
        "",
        "Base gate FAIL → STOP, geen TRIALS-append. Base PASS → trial counted "
        "(PASS_CANDIDATE / FAIL_T / FAIL_STRESS_then_*).",
        f"ftmo_ev train: {json.dumps(ftmo)}",
    ]
    (OUT / "gbpjpy_eu_mom_report.md").write_text("\n".join(md) + "\n")
    print(json.dumps({"outcome": outcome, "train_N": tr.get("N"),
                      "mean_bruto": tr.get("mean_bruto"),
                      "gate_pass": gate_pass, "stress_pass": stress_pass,
                      "test_N": None if not test_sum else test_sum.get("N"),
                      "train_t": tr.get("t_day_clust_netto"),
                      "test_t": None if not test_sum else test_sum.get("t_day_clust_netto")},
                     indent=2))
    return board


if __name__ == "__main__":
    main()
