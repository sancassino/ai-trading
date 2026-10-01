#!/usr/bin/env python3
"""S2 LUNCH_OPEN cost gate — train 2021–2023. PREREG_S2_LUNCH_OPEN.md.

US lunch open-anchor fade on US30/US100.
m5gz = Amsterdam wall clock; session open 15:30; entry 17:00; hard flat 19:00.
Reserve 2025→ untouched. Same-bar target+stop → stop wins (PREREG §1).
"""
from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
M5 = ROOT / "data" / "m5gz"
RT = {"US30cash": 0.45, "US100cash": 0.66}
ATR_N = 14
WIDTH_K = 0.40
STOP_BUF = 0.15
OPEN_H, OPEN_M = 15, 30
ENTRY_H, ENTRY_M = 17, 0
FLAT_H, FLAT_M = 19, 0
OUT_DIR = ROOT / "results" / "R2" / "lunch_open_prep"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")


def load_m5(sym: str) -> pd.DataFrame:
    with gzip.open(M5 / f"{sym}.csv.gz", "rt") as f:
        for line in f:
            if not line.startswith("#"):
                break
        df = pd.read_csv(
            f, sep=";", names=["time", "open", "high", "low", "close", "spread"]
        )
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["close"]).sort_values("time").reset_index(drop=True)
    return df[(df["time"] >= TRAIN_START) & (df["time"] <= TRAIN_END)]


def daily_atr_prior_map(df: pd.DataFrame) -> dict:
    g = df.groupby(df["time"].dt.normalize())
    h = g["high"].max()
    l = g["low"].min()
    c = g["close"].last()
    prev_c = c.shift(1)
    tr = pd.concat([(h - l), (h - prev_c).abs(), (l - prev_c).abs()], axis=1).max(axis=1)
    atr = tr.rolling(ATR_N, min_periods=ATR_N).mean()
    atr_prior = atr.shift(1)
    return {d: float(v) for d, v in atr_prior.items() if pd.notna(v) and v > 0}


def bar_at(g: pd.DataFrame, day0, hh, mm):
    t = day0 + pd.Timedelta(hours=hh, minutes=mm)
    b = g[(g["time"] >= t) & (g["time"] < t + pd.Timedelta(minutes=5))]
    return None if b.empty else b.iloc[0]


def sim_day(g: pd.DataFrame, atr_price: float, rt: float):
    if len(g) < 30 or not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b_open = bar_at(g, day0, OPEN_H, OPEN_M)
    b_entry = bar_at(g, day0, ENTRY_H, ENTRY_M)
    if b_open is None or b_entry is None:
        return None
    p_open = float(b_open["open"])
    entry = float(b_entry["close"])
    entry_time = b_entry["time"]
    if p_open <= 0:
        return None
    morn_bp = 1e4 * (entry - p_open) / p_open
    atr_bp = 1e4 * atr_price / p_open
    if abs(morn_bp) < WIDTH_K * atr_bp:
        return None
    side = -1 if morn_bp > 0 else 1  # fade morning move
    t_open = day0 + pd.Timedelta(hours=OPEN_H, minutes=OPEN_M)
    t_entry = day0 + pd.Timedelta(hours=ENTRY_H, minutes=ENTRY_M)
    t_flat = day0 + pd.Timedelta(hours=FLAT_H, minutes=FLAT_M)
    morn = g[(g["time"] >= t_open) & (g["time"] <= t_entry)]
    if morn.empty:
        return None
    mhi, mlo = float(morn["high"].max()), float(morn["low"].min())
    mr = mhi - mlo
    if mr <= 0:
        return None
    target_px = p_open
    if side == 1:
        stop_px = mlo - STOP_BUF * mr
    else:
        stop_px = mhi + STOP_BUF * mr

    after = g[(g["time"] > entry_time) & (g["time"] <= t_flat)]
    if after.empty:
        return None
    exit_px = float(after.iloc[-1]["close"])
    reason = "time"
    for _, row in after.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        hit_s = (side == 1 and lo <= stop_px) or (side == -1 and hi >= stop_px)
        hit_t = (side == 1 and hi >= target_px) or (side == -1 and lo <= target_px)
        if hit_s and hit_t:
            exit_px = stop_px
            reason = "stop_samebar"
            break
        if hit_s:
            exit_px = stop_px
            reason = "stop"
            break
        if hit_t:
            exit_px = target_px
            reason = "target"
            break

    bruto = side * 1e4 * (exit_px - entry) / entry
    return {
        "bruto_bp": bruto,
        "rt": rt,
        "side": side,
        "morn_bp": morn_bp,
        "atr_bp": atr_bp,
        "reason": reason,
    }


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    trades = []
    for sym, rt in RT.items():
        m5 = load_m5(sym)
        atr = daily_atr_prior_map(m5)
        for day, g in m5.groupby(m5["time"].dt.normalize()):
            atr_val = atr.get(day)
            if atr_val is None or atr_val <= 0:
                continue
            r = sim_day(g, atr_val, rt)
            if r is not None:
                trades.append(
                    {
                        "date": str(day.date()),
                        "sym": sym,
                        **{
                            k: (round(v, 4) if isinstance(v, float) else v)
                            for k, v in r.items()
                        },
                    }
                )

    if not trades:
        result = {
            "N": 0,
            "mean_bruto": None,
            "tw_rt": None,
            "gate": None,
            "outcome": "FAIL_NO_TRADES",
        }
    else:
        bruto = np.array([t["bruto_bp"] for t in trades], dtype=float)
        rts = np.array([t["rt"] for t in trades], dtype=float)
        mean_b = float(bruto.mean())
        tw_rt = float(rts.mean())
        gate = 3 * tw_rt
        gate_stress = 3 * tw_rt * 1.5
        by_sym = {}
        for sym in RT:
            sub = [t for t in trades if t["sym"] == sym]
            if sub:
                by_sym[sym] = {
                    "N": len(sub),
                    "mean_bruto": round(float(np.mean([t["bruto_bp"] for t in sub])), 4),
                    "rt": RT[sym],
                    "gate_sym": round(3 * RT[sym], 4),
                }
        reasons = {}
        for t in trades:
            reasons[t["reason"]] = reasons.get(t["reason"], 0) + 1
        # Formal PASS requires base gate AND +50% RT stress (PREREG §2/§4)
        base_ok = mean_b >= gate
        stress_ok = mean_b >= gate_stress
        if base_ok and stress_ok:
            outcome = "PASS"
        else:
            outcome = "FAIL"
        result = {
            "N": len(trades),
            "mean_bruto": round(mean_b, 4),
            "median_bruto": round(float(np.median(bruto)), 4),
            "skew": round(float(pd.Series(bruto).skew()), 4),
            "tw_rt": round(tw_rt, 4),
            "gate": round(gate, 4),
            "gate_stress50": round(gate_stress, 4),
            "base_pass": base_ok,
            "stress50_pass": stress_ok,
            "outcome": outcome,
            "by_sym": by_sym,
            "reasons": reasons,
            "date_min": min(t["date"] for t in trades),
            "date_max": max(t["date"] for t in trades),
            "n_long": sum(1 for t in trades if t["side"] == 1),
            "n_short": sum(1 for t in trades if t["side"] == -1),
        }

    pd.DataFrame(trades).to_csv(OUT_DIR / "cost_gate_lunch_open_train.csv", index=False)
    (OUT_DIR / "cost_gate_lunch_open_train.json").write_text(json.dumps(result, indent=2))
    md = [
        "# S2 LUNCH_OPEN — kostenpoort TRAIN 2021–2023",
        "\nDatum: 2026-10-01 ~02:52 CEST | PREREG_S2_LUNCH_OPEN | Geen 2025+ bars.",
        "\n| Metriek | Waarde |",
        "|----|-----|",
        f"| N trades | {result['N']} |",
        f"| mean bruto | {result.get('mean_bruto')} bp |",
        f"| TW-RT | {result.get('tw_rt')} bp |",
        f"| gate (3×TW-RT) | {result.get('gate')} bp |",
        f"| gate +50% stress | {result.get('gate_stress50')} bp |",
        f"| **Uitkomst** | **{result['outcome']}** |",
        "\nFAIL → STOP, geen trial / geen TRIALS-append. PASS → clustered-t / ftmo_ev (N≥150).",
    ]
    (OUT_DIR / "cost_gate_lunch_open_train.md").write_text("\n".join(md))
    print(
        f"LUNCH_OPEN: N={result['N']} mean={result.get('mean_bruto')} "
        f"gate={result.get('gate')} stress={result.get('gate_stress50')} "
        f"→ {result['outcome']}"
    )
    if result.get("by_sym"):
        print("by_sym:", json.dumps(result["by_sym"]))
    if result.get("reasons"):
        print("reasons:", json.dumps(result["reasons"]))
    return result


if __name__ == "__main__":
    main()
