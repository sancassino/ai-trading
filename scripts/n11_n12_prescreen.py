#!/usr/bin/env python3
"""D-092.1 free pre-screen (Uitvoerder-2): Strateeg VOORSTEL N11 (GER40 XETRA ORB)
and N12 (XAU NY-Open Continuation).

Train 2021-01-01 .. 2023-12-31 only. Reserve 2025+ untouched.
No PREREG / no TRIALS — FAIL or N<150 → no PREREG; PASS + N≥150 → Strateeg may freeze PREREG.

Source: VOORSTEL_PRESCREEN_N11.md / N12.md @ Strateeg b374f0a.
m5gz clock = Europe/Amsterdam wall (U2 AMS convention).
"""
from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
ATR_N = 14
OUT = ROOT / "results/R2/n11_n12_prescreen"
MIN_N_PREREG = 150

# VOORSTEL gates (Strateeg stated).
N11_RT = 1.40  # Strateeg stated → gate 4.20 (N6/N9 GER40 convention)
N11_GATE = 3.0 * N11_RT
N11_RT_COSTS = 0.72  # COSTS_FTMO.csv roundtrip_intraday_bp
N11_GATE_COSTS = 3.0 * N11_RT_COSTS
N12_RT = 0.83
N12_GATE = 3.0 * N12_RT  # 2.49
MIN_ORB_FRAC = 0.001  # 0.10%


def load_m5(rel: str) -> pd.DataFrame:
    path = ROOT / rel
    with gzip.open(path, "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna().sort_values("time")
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


def bp_ret(entry: float, exit_px: float, side: int) -> float:
    return side * 1e4 * (exit_px - entry) / entry


def bar_at(g: pd.DataFrame, day0: pd.Timestamp, h: int, m: int = 0):
    t = day0 + pd.Timedelta(hours=h, minutes=m)
    rows = g[g["time"] == t]
    if rows.empty:
        return None
    return rows.iloc[0]


def sim_n11_day(g: pd.DataFrame):
    """GER40 XETRA Opening Range Breakout (VOORSTEL_N11)."""
    day0 = g["time"].dt.normalize().iloc[0]
    # ORB window: 09:00–09:30 inclusive (6 M5 bars: 09:00,05,10,15,20,25)
    orb = g[
        (g["time"] >= day0 + pd.Timedelta(hours=9))
        & (g["time"] < day0 + pd.Timedelta(hours=9, minutes=30))
    ]
    if len(orb) < 4:
        return None
    orb_hi = float(orb["high"].max())
    orb_lo = float(orb["low"].min())
    orb_mid = 0.5 * (orb_hi + orb_lo)
    orb_range = orb_hi - orb_lo
    if orb_mid <= 0 or orb_range <= 0:
        return None
    if orb_range / orb_mid < MIN_ORB_FRAC:
        return None

    # First close after 09:30 that breaks ORB (OCO, max 1 trade/day)
    after_orb = g[
        (g["time"] >= day0 + pd.Timedelta(hours=9, minutes=30))
        & (g["time"] < day0 + pd.Timedelta(hours=13))
    ]
    if after_orb.empty:
        return None

    side = 0
    entry = None
    entry_t = None
    for _, row in after_orb.iterrows():
        c = float(row["close"])
        if c > orb_hi:
            side, entry, entry_t = 1, c, row["time"]
            break
        if c < orb_lo:
            side, entry, entry_t = -1, c, row["time"]
            break
    if side == 0 or entry is None:
        return None

    stop = orb_lo if side == 1 else orb_hi
    path = g[(g["time"] > entry_t) & (g["time"] <= day0 + pd.Timedelta(hours=13))]
    exit_px = float(path.iloc[-1]["close"]) if len(path) else entry
    hit = "time"
    for _, row in path.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        if side == 1:
            if lo <= stop:
                exit_px, hit = stop, "stop"
                break
        else:
            if hi >= stop:
                exit_px, hit = stop, "stop"
                break

    return {
        "date": str(day0.date()),
        "side": side,
        "entry": entry,
        "exit": exit_px,
        "hit": hit,
        "orb_hi": orb_hi,
        "orb_lo": orb_lo,
        "orb_frac_bp": round(1e4 * orb_range / orb_mid, 4),
        "entry_hhmm": f"{entry_t.hour:02d}:{entry_t.minute:02d}",
        "bruto_bp": bp_ret(entry, exit_px, side),
    }


def sim_n12_day(g: pd.DataFrame, atr_price: float):
    """XAU NY-Open Continuation (VOORSTEL_N12)."""
    if not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b_1430 = bar_at(g, day0, 14, 30)
    b_1530 = bar_at(g, day0, 15, 30)
    if b_1430 is None or b_1530 is None:
        return None
    p_1430 = float(b_1430["close"])
    p_1530 = float(b_1530["close"])
    if p_1430 <= 0:
        return None
    handoff_bp = 1e4 * (p_1530 - p_1430) / p_1430
    if handoff_bp >= 20.0:
        side = 1
    elif handoff_bp <= -20.0:
        side = -1
    else:
        return None

    entry = p_1530
    entry_t = b_1530["time"]
    stop = entry - side * atr_price  # 1.0 × ATR14 daily from entry
    path = g[(g["time"] > entry_t) & (g["time"] <= day0 + pd.Timedelta(hours=17))]
    exit_px = float(path.iloc[-1]["close"]) if len(path) else entry
    hit = "time"
    for _, row in path.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        if side == 1:
            if lo <= stop:
                exit_px, hit = stop, "stop"
                break
        else:
            if hi >= stop:
                exit_px, hit = stop, "stop"
                break

    return {
        "date": str(day0.date()),
        "side": side,
        "entry": entry,
        "exit": exit_px,
        "hit": hit,
        "handoff_bp": round(handoff_bp, 4),
        "atr": atr_price,
        "bruto_bp": bp_ret(entry, exit_px, side),
    }


def summarize(idea: str, trades: list[dict], rt: float, gate: float) -> dict:
    if not trades:
        return {
            "idea": idea,
            "n": 0,
            "mean_bruto_bp": None,
            "rt_bp": rt,
            "gate_3x_rt": gate,
            "pass_gate": False,
            "n_ok": False,
            "pass": False,
            "decision": "NO_PREREG_screen_fail_empty",
        }
    arr = np.array([t["bruto_bp"] for t in trades], dtype=float)
    mean = float(arr.mean())
    n = int(len(arr))
    gate_ok = mean >= gate
    n_ok = n >= MIN_N_PREREG
    ok = gate_ok and n_ok
    if not gate_ok:
        decision = "NO_PREREG_screen_fail"
    elif not n_ok:
        decision = "NO_PREREG_underpowered"
    else:
        decision = "PASS_may_PREREG"
    return {
        "idea": idea,
        "n": n,
        "mean_bruto_bp": round(mean, 4),
        "median_bruto_bp": round(float(np.median(arr)), 4),
        "p25": round(float(np.percentile(arr, 25)), 4),
        "p75": round(float(np.percentile(arr, 75)), 4),
        "stop_share": round(float(np.mean([t["hit"] == "stop" for t in trades])), 4),
        "time_share": round(float(np.mean([t["hit"] == "time" for t in trades])), 4),
        "rt_bp": rt,
        "gate_3x_rt": gate,
        "pass_gate": bool(gate_ok),
        "n_ok": bool(n_ok),
        "pass": bool(ok),
        "date_min": trades[0]["date"],
        "date_max": trades[-1]["date"],
        "decision": decision,
        "reserve_2025": "untouched",
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # --- N11 GER40 XETRA ORB ---
    ger = load_m5("data/m5gz/GER40cash.csv.gz")
    n11 = []
    for day, g in ger.groupby(ger["time"].dt.normalize()):
        g = g.sort_values("time")
        t = sim_n11_day(g)
        if t:
            n11.append(t)

    s11_v = summarize("N11_GER40_XETRA_ORB", n11, N11_RT, N11_GATE)
    s11_c = summarize("N11_GER40_XETRA_ORB_costsRT", n11, N11_RT_COSTS, N11_GATE_COSTS)

    # --- N12 XAU NY-Open Continuation ---
    xau = load_m5("data/m5gz/XAUUSD.csv.gz")
    atr_x = atr_map(xau)
    n12 = []
    for day, g in xau.groupby(xau["time"].dt.normalize()):
        g = g.sort_values("time")
        a = prior_atr(atr_x, day)
        t = sim_n12_day(g, a)
        if t:
            n12.append(t)

    s12 = summarize("N12_XAU_NYOPEN_CONT", n12, N12_RT, N12_GATE)

    board = {
        "n11": s11_v,
        "n11_costs_rt_sensitivity": s11_c,
        "n12": s12,
        "source": "VOORSTEL_PRESCREEN_N11/N12 @ b374f0a",
        "binding_gates": {
            "n11": N11_GATE,
            "n11_note": "Strateeg VOORSTEL RT=1.40→4.20 (N6/N9 GER40 convention); COSTS_FTMO RT=0.72→2.16 sensitivity only",
            "n12": N12_GATE,
            "min_n": MIN_N_PREREG,
        },
        "reserve_2025": "untouched",
    }

    pd.DataFrame(n11).to_csv(OUT / "n11_trades_train.csv", index=False)
    pd.DataFrame(n12).to_csv(OUT / "n12_trades_train.csv", index=False)
    (OUT / "prescreen.json").write_text(json.dumps(board, indent=2) + "\n")

    def label(s: dict) -> str:
        if s["pass"]:
            return "PASS"
        if s.get("pass_gate") and not s.get("n_ok"):
            return "FAIL_N (underpowered)"
        return "FAIL"

    md = [
        "# D-092.1 U2 pre-screen — N11 / N12 (train 2021–2023)",
        "",
        "Source: Strateeg `VOORSTEL_PRESCREEN_N11.md` / `N12.md` @ `b374f0a`.",
        "Data: `data/m5gz/GER40cash.csv.gz`, `data/m5gz/XAUUSD.csv.gz`.",
        "Reserve 2025+ untouched. No TRIALS. No PREREG claimed by this screen.",
        f"PREREG requires gate PASS **and** N≥{MIN_N_PREREG}.",
        "",
        "| Idee | N | mean bruto | gate | Uitkomst |",
        "|------|---|------------|------|----------|",
        f"| N11 GER40 XETRA ORB (VOORSTEL gate) | {s11_v['n']} | {s11_v['mean_bruto_bp']} bp | {N11_GATE} bp | **{label(s11_v)}** |",
        f"| N11 GER40 (COSTS RT sens.) | {s11_c['n']} | {s11_c['mean_bruto_bp']} bp | {N11_GATE_COSTS} bp | **{label(s11_c)}** (sens.) |",
        f"| N12 XAU NY-Open Continuation | {s12['n']} | {s12['mean_bruto_bp']} bp | {N12_GATE} bp | **{label(s12)}** |",
        "",
        f"- N11 binding decision (VOORSTEL gate 4.20, N≥{MIN_N_PREREG}): `{s11_v['decision']}`",
        f"- N11 COSTS sensitivity (gate 2.16): `{s11_c['decision']}`",
        f"- N12 decision: `{s12['decision']}`",
        "",
    ]
    (OUT / "prescreen.md").write_text("\n".join(md) + "\n")
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
