#!/usr/bin/env python3
"""D-092.1 free pre-screen: Strateeg VOORSTEL N7 (Pre-London Range Breakout)
and N8 (Post-AM-Fix Continuation) on XAUUSD.

Train 2021-01-01 .. 2023-12-31 only. Reserve 2025+ untouched.
No PREREG / no TRIALS — FAIL → no PREREG; PASS → Strateeg may freeze PREREG.

Source rules: VOORSTEL_PRESCREEN_N7.md / N8.md @ Strateeg 988cbde.
m5gz clock treated as Europe/Amsterdam wall (same convention as s2_xau_am_fade_gate).
"""
from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RT_BP = 0.83
GATE = 3.0 * RT_BP  # 2.49
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
ATR_N = 14
OUT = ROOT / "results/cto/n7_n8_xau_prescreen"


def load_m5() -> pd.DataFrame:
    path = ROOT / "data/m5gz/XAUUSD.csv.gz"
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


def bp_ret(entry: float, exit_px: float, side: int) -> float:
    return side * 1e4 * (exit_px - entry) / entry


def sim_n7_day(g: pd.DataFrame):
    """Pre-London Range Breakout (VOORSTEL_N7)."""
    day0 = g["time"].dt.normalize().iloc[0]
    plr = g[
        (g["time"] >= day0 + pd.Timedelta(hours=6))
        & (g["time"] <= day0 + pd.Timedelta(hours=8, minutes=55))
    ]
    if len(plr) < 10:
        return None
    plr_hi = float(plr["high"].max())
    plr_lo = float(plr["low"].min())
    mid = 0.5 * (plr_hi + plr_lo)
    if mid <= 0:
        return None
    width_pct = (plr_hi - plr_lo) / mid
    if width_pct < 0.001:  # 0.10%
        return None

    session = g[
        (g["time"] > day0 + pd.Timedelta(hours=8, minutes=55))
        & (g["time"] <= day0 + pd.Timedelta(hours=11))
    ]
    if session.empty:
        return None

    side = None
    entry = None
    entry_t = None
    for _, row in session.iterrows():
        c = float(row["close"])
        if c > plr_hi:
            side, entry, entry_t = 1, c, row["time"]
            break
        if c < plr_lo:
            side, entry, entry_t = -1, c, row["time"]
            break
    if side is None:
        return None

    stop = plr_lo if side == 1 else plr_hi
    after = g[(g["time"] > entry_t) & (g["time"] <= day0 + pd.Timedelta(hours=11))]
    exit_px = float(after.iloc[-1]["close"]) if len(after) else entry
    hit = "time"
    for _, row in after.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        if side == 1 and lo <= stop:
            exit_px, hit = stop, "stop"
            break
        if side == -1 and hi >= stop:
            exit_px, hit = stop, "stop"
            break

    return {
        "date": str(day0.date()),
        "side": side,
        "entry": entry,
        "exit": exit_px,
        "hit": hit,
        "width_pct": width_pct,
        "bruto_bp": bp_ret(entry, exit_px, side),
    }


def bar_at(g: pd.DataFrame, day0: pd.Timestamp, h: int, m: int = 0):
    t = day0 + pd.Timedelta(hours=h, minutes=m)
    rows = g[g["time"] == t]
    if rows.empty:
        return None
    return rows.iloc[0]


def sim_n8_day(g: pd.DataFrame, atr_price: float):
    """Post-AM-Fix Continuation (VOORSTEL_N8)."""
    if not (atr_price == atr_price) or atr_price <= 0:
        return None
    day0 = g["time"].dt.normalize().iloc[0]
    b0900 = bar_at(g, day0, 9, 0)
    b1030 = bar_at(g, day0, 10, 30)
    if b0900 is None or b1030 is None:
        return None
    o0900 = float(b0900["open"])
    c1030 = float(b1030["close"])
    move = (c1030 - o0900) / o0900
    if move >= 0.002:
        side = 1
    elif move <= -0.002:
        side = -1
    else:
        return None

    entry = c1030
    entry_t = b1030["time"]
    stop = entry - side * atr_price  # 1.0 × ATR14 daily
    after = g[(g["time"] > entry_t) & (g["time"] <= day0 + pd.Timedelta(hours=12, minutes=30))]
    exit_px = float(after.iloc[-1]["close"]) if len(after) else entry
    hit = "time"
    for _, row in after.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        if side == 1 and lo <= stop:
            exit_px, hit = stop, "stop"
            break
        if side == -1 and hi >= stop:
            exit_px, hit = stop, "stop"
            break

    return {
        "date": str(day0.date()),
        "side": side,
        "entry": entry,
        "exit": exit_px,
        "hit": hit,
        "move_pct": move * 100,
        "atr": atr_price,
        "bruto_bp": bp_ret(entry, exit_px, side),
    }


def summarize(idea: str, trades: list[dict]) -> dict:
    if not trades:
        return {
            "idea": idea,
            "n": 0,
            "mean_bruto_bp": None,
            "rt_bp": RT_BP,
            "gate_3x_rt": GATE,
            "pass": False,
            "decision": "NO_PREREG_screen_fail_empty",
        }
    arr = np.array([t["bruto_bp"] for t in trades], dtype=float)
    mean = float(arr.mean())
    ok = mean >= GATE
    return {
        "idea": idea,
        "n": int(len(arr)),
        "mean_bruto_bp": round(mean, 4),
        "median_bruto_bp": round(float(np.median(arr)), 4),
        "p25": round(float(np.percentile(arr, 25)), 4),
        "p75": round(float(np.percentile(arr, 75)), 4),
        "stop_share": round(float(np.mean([t["hit"] == "stop" for t in trades])), 4),
        "rt_bp": RT_BP,
        "gate_3x_rt": GATE,
        "pass": bool(ok),
        "date_min": trades[0]["date"],
        "date_max": trades[-1]["date"],
        "decision": "PASS_may_PREREG" if ok else "NO_PREREG_screen_fail",
        "reserve_2025": "untouched",
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    m5 = load_m5()
    atr = atr_map(m5)
    n7, n8 = [], []
    for day, g in m5.groupby(m5["time"].dt.normalize()):
        g = g.sort_values("time")
        t7 = sim_n7_day(g)
        if t7:
            n7.append(t7)
        # ATR from prior completed days: use atr as-of previous calendar day
        prev = day - pd.Timedelta(days=1)
        # walk back to last available atr
        a = atr.get(day, np.nan)
        if not (a == a):
            # try lookback up to 5 days
            for k in range(1, 6):
                a = atr.get(day - pd.Timedelta(days=k), np.nan)
                if a == a:
                    break
        # Prefer yesterday's ATR (no lookahead of same-day range)
        a_y = atr.get(prev, np.nan)
        if not (a_y == a_y):
            for k in range(2, 8):
                a_y = atr.get(day - pd.Timedelta(days=k), np.nan)
                if a_y == a_y:
                    break
        t8 = sim_n8_day(g, float(a_y) if a_y == a_y else float("nan"))
        if t8:
            n8.append(t8)

    s7 = summarize("N7_XAU_PRELONDON_RANGE_BO", n7)
    s8 = summarize("N8_XAU_POST_AMFIX_CONT", n8)
    board = {"n7": s7, "n8": s8, "source": "VOORSTEL_PRESCREEN_N7/N8 @ 988cbde"}

    pd.DataFrame(n7).to_csv(OUT / "n7_trades_train.csv", index=False)
    pd.DataFrame(n8).to_csv(OUT / "n8_trades_train.csv", index=False)
    (OUT / "prescreen.json").write_text(json.dumps(board, indent=2) + "\n")

    md = [
        "# D-092.1 CTO pre-screen — N7 / N8 XAU (train 2021–2023)",
        "",
        f"Source: Strateeg `VOORSTEL_PRESCREEN_N7.md` / `N8.md` @ `988cbde`.",
        f"Data: `data/m5gz/XAUUSD.csv.gz`. RT={RT_BP} bp → gate 3×RT={GATE} bp.",
        "Reserve 2025+ untouched. No TRIALS. No PREREG claimed by this screen.",
        "",
        "| Idee | N | mean bruto | gate | Uitkomst |",
        "|------|---|------------|------|----------|",
        f"| N7 Pre-London Range BO | {s7['n']} | {s7['mean_bruto_bp']} bp | {GATE} bp | **{'PASS' if s7['pass'] else 'FAIL'}** |",
        f"| N8 Post-AM-Fix Cont | {s8['n']} | {s8['mean_bruto_bp']} bp | {GATE} bp | **{'PASS' if s8['pass'] else 'FAIL'}** |",
        "",
        f"- N7 decision: `{s7['decision']}`",
        f"- N8 decision: `{s8['decision']}`",
        "",
    ]
    (OUT / "prescreen.md").write_text("\n".join(md) + "\n")
    print(json.dumps(board, indent=2))


if __name__ == "__main__":
    main()
