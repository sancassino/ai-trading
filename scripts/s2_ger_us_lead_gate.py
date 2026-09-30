#!/usr/bin/env python3
"""S2 GER_US_LEAD cost gate — train 2021–2023. PREREG_S2_GER_US_LEAD.md (C-007).
GER40 09:00–15:15 AMS impulse → US100/US500 at US cash-open (~15:30 AMS).
m5gz = Amsterdam wall clock (U2 N3/N4 convention). Reserve 2025→ untouched.
"""
from __future__ import annotations
import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
M5 = ROOT / "data" / "m5gz"
RT = {"US100cash": 0.66, "US500cash": 0.78}
ATR_N = 14
GER_K = 0.40
TARGET_ATR = 1.0
STOP_ATR = 0.75
OUT_DIR = ROOT / "results" / "R2" / "ger_us_lead_prep"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")


def load_m5(sym: str) -> pd.DataFrame:
    with gzip.open(M5 / f"{sym}.csv.gz", "rt") as f:
        for line in f:
            if not line.startswith("#"):
                break
        df = pd.read_csv(f, sep=";", names=["time", "open", "high", "low", "close", "spread"])
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["close"]).sort_values("time").reset_index(drop=True)
    return df[(df["time"] >= TRAIN_START) & (df["time"] <= TRAIN_END)]


def daily_atr_map(df: pd.DataFrame) -> dict:
    day_df = df.set_index("time").resample("1D").agg(
        high=("high", "max"), low=("low", "min"), close=("close", "last")
    ).dropna()
    tr_list, prev = [], None
    for _, row in day_df.iterrows():
        if prev is None:
            tr_list.append(row["high"] - row["low"])
        else:
            tr_list.append(max(row["high"] - row["low"],
                               abs(row["high"] - prev), abs(row["low"] - prev)))
        prev = row["close"]
    day_df["atr"] = pd.Series(tr_list, index=day_df.index).rolling(ATR_N).mean()
    return day_df["atr"].dropna().to_dict()


def px_at(g: pd.DataFrame, h: int, m: int, field: str = "close") -> float | None:
    rows = g[(g["time"].dt.hour == h) & (g["time"].dt.minute == m)]
    return float(rows[field].iloc[0]) if not rows.empty else None


def first_at_or_after(g: pd.DataFrame, h: int, m: int):
    mask = (g["time"].dt.hour > h) | ((g["time"].dt.hour == h) & (g["time"].dt.minute >= m))
    rows = g[mask]
    if rows.empty:
        return None
    return rows.iloc[0]


def sim_day(ger: pd.DataFrame, us: pd.DataFrame, atr_ger: float, atr_us: float, rt: float):
    if len(ger) < 20 or len(us) < 20:
        return None
    p_ger_0900 = px_at(ger, 9, 0, "close")
    if p_ger_0900 is None:
        # try open of first bar >= 09:00
        row = first_at_or_after(ger, 9, 0)
        p_ger_0900 = float(row["open"]) if row is not None else None
    p_ger_1515 = px_at(ger, 15, 15, "close")
    if p_ger_0900 is None or p_ger_1515 is None or p_ger_0900 == 0:
        return None
    ger_bp = 1e4 * (p_ger_1515 - p_ger_0900) / p_ger_0900
    atr_ger_bp = 1e4 * atr_ger / p_ger_0900
    if atr_ger_bp <= 0:
        return None
    if ger_bp >= GER_K * atr_ger_bp:
        side = 1
    elif ger_bp <= -GER_K * atr_ger_bp:
        side = -1
    else:
        return None

    entry_row = first_at_or_after(us, 15, 30)
    if entry_row is None:
        return None
    # Prefer exact 15:30 close
    exact = us[(us["time"].dt.hour == 15) & (us["time"].dt.minute == 30)]
    if not exact.empty:
        entry_row = exact.iloc[0]
    entry = float(entry_row["close"])
    atr_us_bp = 1e4 * atr_us / entry
    if atr_us_bp <= 0:
        return None
    target_bp = TARGET_ATR * atr_us_bp
    stop_bp = STOP_ATR * atr_us_bp
    target_px = entry * (1 + side * target_bp / 1e4)
    stop_px = entry * (1 - side * stop_bp / 1e4)

    after = us[(us["time"] > entry_row["time"]) &
               ((us["time"].dt.hour < 20) |
                ((us["time"].dt.hour == 20) & (us["time"].dt.minute == 0)))]
    # Also include bars up to 20:00
    after = us[(us["time"] > entry_row["time"]) & (us["time"] <= entry_row["time"].normalize() + pd.Timedelta(hours=20))]
    if after.empty:
        return None
    exit_px = float(after.iloc[-1]["close"])
    for _, row in after.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        hit_s = (side == 1 and lo <= stop_px) or (side == -1 and hi >= stop_px)
        hit_t = (side == 1 and hi >= target_px) or (side == -1 and lo <= target_px)
        if hit_s and hit_t:
            exit_px = stop_px  # same-bar → stop wins
            break
        if hit_s:
            exit_px = stop_px
            break
        if hit_t:
            exit_px = target_px
            break
    bruto = side * 1e4 * (exit_px - entry) / entry
    return {"bruto_bp": bruto, "rt": rt, "side": side, "ger_bp": ger_bp}


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ger_all = load_m5("GER40cash")
    atr_ger = daily_atr_map(ger_all)
    ger_by = {d: g for d, g in ger_all.groupby(ger_all["time"].dt.normalize())}
    trades = []
    for sym, rt in RT.items():
        us_all = load_m5(sym)
        atr_us = daily_atr_map(us_all)
        for day, us_g in us_all.groupby(us_all["time"].dt.normalize()):
            if day not in ger_by:
                continue
            prior_g = {d: v for d, v in atr_ger.items() if pd.Timestamp(d) < day}
            prior_u = {d: v for d, v in atr_us.items() if pd.Timestamp(d) < day}
            if len(prior_g) < ATR_N or len(prior_u) < ATR_N:
                continue
            ag = list(prior_g.values())[-1]
            au = list(prior_u.values())[-1]
            if pd.isna(ag) or pd.isna(au) or ag <= 0 or au <= 0:
                continue
            r = sim_day(ger_by[day], us_g, ag, au, rt)
            if r is not None:
                trades.append({"date": str(day.date()), "sym": sym, **{k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()}})

    if not trades:
        result = {"N": 0, "mean_bruto": None, "tw_rt": None, "gate": None, "outcome": "FAIL_NO_TRADES"}
    else:
        bruto = np.array([t["bruto_bp"] for t in trades], dtype=float)
        rts = np.array([t["rt"] for t in trades], dtype=float)
        mean_b = float(bruto.mean())
        tw_rt = float(rts.mean())  # trade-weighted mean RT
        gate = 3 * tw_rt
        by_sym = {}
        for sym in RT:
            sub = [t for t in trades if t["sym"] == sym]
            if sub:
                by_sym[sym] = {"N": len(sub), "mean_bruto": round(float(np.mean([t["bruto_bp"] for t in sub])), 4)}
        result = {
            "N": len(trades),
            "mean_bruto": round(mean_b, 4),
            "tw_rt": round(tw_rt, 4),
            "gate": round(gate, 4),
            "gate_stress50": round(3 * tw_rt * 1.5, 4),
            "outcome": "PASS" if mean_b >= gate else "FAIL",
            "by_sym": by_sym,
        }

    pd.DataFrame(trades).to_csv(OUT_DIR / "cost_gate_ger_us_lead_train.csv", index=False)
    (OUT_DIR / "cost_gate_ger_us_lead_train.json").write_text(json.dumps(result, indent=2))
    md = [
        "# S2 GER_US_LEAD — kostenpoort TRAIN 2021–2023",
        "\nDatum: 2026-10-01 ~01:21 CEST | PREREG_S2_GER_US_LEAD | Geen 2025+ bars.",
        "\n| Metriek | Waarde |",
        "|----|-----|",
        f"| N trades | {result['N']} |",
        f"| mean bruto | {result.get('mean_bruto')} bp |",
        f"| TW-RT | {result.get('tw_rt')} bp |",
        f"| gate (3×TW-RT) | {result.get('gate')} bp |",
        f"| **Uitkomst** | **{result['outcome']}** |",
        "\nFAIL → STOP, geen trial. PASS → clustered-t / ftmo_ev.",
    ]
    (OUT_DIR / "cost_gate_ger_us_lead_train.md").write_text("\n".join(md))
    print(f"GER_US_LEAD: N={result['N']} mean={result.get('mean_bruto')} gate={result.get('gate')} → {result['outcome']}")
    return result


if __name__ == "__main__":
    main()
