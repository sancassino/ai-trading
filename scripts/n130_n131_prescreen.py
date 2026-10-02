#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N130 EQW breadth → US500 + N131 DXY → US500.

Freeze (no thr-grid):
  N130: SPX_EQW/SPX z40 thr±1.5 stress → US500cash 15:30→21:00 CET (NEW_FAMILY AY)
  N131: DXY daily z120+d20 INVERSE combo → US500cash 15:30→21:00 CET (NEW_FAMILY AZ)
        ≠ N110 (DXYcash M5 Lon-AM 08:00→12:00 same-dir continuation, trade DXYcash 13:00→17:00).
Gate: 3 × US500 RT 0.78 = 2.34 bp; N ≥ 150; train 2021–2023 only.
"""
from __future__ import annotations
import gzip, io, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n130_n131_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
MIN_N = 150
GATE = 2.34


def load_daily_close(sym: str) -> pd.Series:
    path = ROOT / "data" / "daily" / f"{sym}.csv"
    raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    body = [ln for ln in raw if not ln.startswith("#")]
    sep = ";" if body and ";" in body[0] else ","
    df = pd.read_csv(io.StringIO("\n".join(body)), sep=sep)
    cols = {c.lower().replace(" ", ""): c for c in df.columns}
    dc = cols.get("date") or cols.get("observation_date")
    cc = cols.get("adjclose") or cols.get("close")
    s = pd.Series(
        pd.to_numeric(df[cc], errors="coerce").values,
        index=pd.DatetimeIndex(
            pd.to_datetime(df[dc].astype(str).str.replace(".", "-", regex=False))
        ).normalize(),
        name=sym,
    )
    return s[~s.index.duplicated(keep="last")].sort_index().dropna()


def load_m5(sym: str) -> pd.DataFrame:
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
    return df[(df["time"] >= TRAIN_START) & (df["time"] <= TRAIN_END)].reset_index(drop=True)


def first_bar_at(g, day, h, m=0, span_min=15):
    t0 = day + pd.Timedelta(hours=h, minutes=m)
    t1 = t0 + pd.Timedelta(minutes=span_min)
    exact = g[g["time"] == t0]
    if len(exact):
        return exact.iloc[0]
    win = g[(g["time"] >= t0) & (g["time"] <= t1)]
    return win.iloc[0] if len(win) else None


def last_bar_le(g, day, h, m=0):
    t = day + pd.Timedelta(hours=h, minutes=m)
    win = g[g["time"] <= t]
    return win.iloc[-1] if len(win) else None


def session_flat_trade(us500_day_g, side: int):
    day = us500_day_g["day"].iloc[0]
    b_entry = first_bar_at(us500_day_g, day, 15, 30, 15)
    b_exit = last_bar_le(us500_day_g, day, 21, 0)
    if b_entry is None or b_exit is None:
        return None
    if b_exit["time"] <= b_entry["time"]:
        return None
    p0 = float(b_entry["close"])
    p1 = float(b_exit["close"])
    if p0 <= 0:
        return None
    return side * 1e4 * (p1 / p0 - 1.0)


def screen_inverse_combo_z120(sig: pd.Series, us500: pd.DataFrame):
    """N131 dollar-tightening: rich DXY → SHORT US500. Not N110 DXY CFD continuation."""
    sig = sig.sort_index()
    z120 = (sig - sig.rolling(120, min_periods=120).mean()) / sig.rolling(
        120, min_periods=120
    ).std(ddof=0).replace(0, np.nan)
    d20 = sig / sig.shift(20) - 1.0
    pos = pd.Series(0.0, index=sig.index)
    pos[(z120 > 0.5) & (d20 > 0)] = -1.0
    pos[(z120 < -0.5) & (d20 < 0)] = 1.0
    us = us500.copy()
    us["day"] = us["time"].dt.normalize()
    days = sorted(us["day"].unique())
    trades = []
    for day in days:
        prior = pos[pos.index < day]
        if prior.empty:
            continue
        side = float(prior.iloc[-1])
        if side == 0.0 or not np.isfinite(side):
            continue
        g = us[us["day"] == day]
        if g.empty:
            continue
        bruto = session_flat_trade(g, int(side))
        if bruto is None:
            continue
        trades.append(
            {
                "date": str(pd.Timestamp(day).date()),
                "side": int(side),
                "bruto_bp": bruto,
                "signal_day": str(prior.index[-1].date()),
            }
        )
    return trades


def screen_stress_z40(sig: pd.Series, us500: pd.DataFrame):
    sig = sig.sort_index()
    z40 = (sig - sig.rolling(40, min_periods=40).mean()) / sig.rolling(
        40, min_periods=40
    ).std(ddof=0).replace(0, np.nan)
    pos = pd.Series(0.0, index=sig.index)
    pos[z40 > 1.5] = -1.0
    pos[z40 < -1.5] = 1.0
    us = us500.copy()
    us["day"] = us["time"].dt.normalize()
    days = sorted(us["day"].unique())
    trades = []
    for day in days:
        prior = pos[pos.index < day]
        if prior.empty:
            continue
        side = float(prior.iloc[-1])
        if side == 0.0 or not np.isfinite(side):
            continue
        g = us[us["day"] == day]
        if g.empty:
            continue
        bruto = session_flat_trade(g, int(side))
        if bruto is None:
            continue
        trades.append(
            {
                "date": str(pd.Timestamp(day).date()),
                "side": int(side),
                "bruto_bp": bruto,
                "signal_day": str(prior.index[-1].date()),
            }
        )
    return trades


def verdict(trades, gate, label, instrument, notes=""):
    n = len(trades)
    if n == 0:
        return {
            "id": label,
            "instrument": instrument,
            "n": 0,
            "mean_bruto_bp": None,
            "gate_bp": gate,
            "verdict": "FAIL",
            "notes": notes,
        }
    arr = np.array([t["bruto_bp"] for t in trades], dtype=float)
    mean = float(arr.mean())
    if n >= MIN_N and mean >= gate:
        v = "PASS_may_PREREG"
    elif mean >= gate and n < MIN_N:
        v = "UNDERPOWERED"
    else:
        v = "FAIL"
    return {
        "id": label,
        "instrument": instrument,
        "n": n,
        "mean_bruto_bp": round(mean, 4),
        "median_bruto_bp": round(float(np.median(arr)), 4),
        "gate_bp": gate,
        "stress_gate_bp": round(gate * 1.5, 4),
        "stress_note": (
            "PASS_stress_informal"
            if mean >= gate * 1.5
            else "BELOW_stress_1.5x (info only; D-092.1 cost-gate is binding)"
        ),
        "verdict": v,
        "hit_rate": round(float((arr > 0).mean()), 4),
        "n_long": int(sum(1 for t in trades if t["side"] > 0)),
        "n_short": int(sum(1 for t in trades if t["side"] < 0)),
        "years": {
            str(y): round(
                float(np.mean([t["bruto_bp"] for t in trades if t["date"].startswith(str(y))])),
                4,
            )
            for y in (2021, 2022, 2023)
            if any(t["date"].startswith(str(y)) for t in trades)
        },
        "notes": notes,
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    eqw = load_daily_close("SPX_EQW")
    spx = load_daily_close("SPX")
    ratio = (eqw / spx).dropna()
    ratio.name = "SPX_EQW_over_SPX"
    dxy = load_daily_close("DXY")
    us500 = load_m5("US500cash")
    t130 = screen_stress_z40(ratio, us500)
    t131 = screen_inverse_combo_z120(dxy, us500)
    s130 = verdict(
        t130, GATE, "N130", "US500cash",
        "EQW_BREADTH SPX_EQW/SPX z40/thr1.5 stress; NEW_FAMILY AY; D-100 session-flat; ≠IWM/SECTOR_DISP/DEFENSIVE/N81",
    )
    s131 = verdict(
        t131, GATE, "N131", "US500cash",
        "DXY daily level inverse combo → US500 15:30-21:00; NEW_FAMILY AZ; ≠N110 DXYcash Lon-AM→EU-PM 13:00-17:00 same-dir",
    )
    pd.DataFrame(t130).to_csv(OUT / "n130_trades_train.csv", index=False)
    pd.DataFrame(t131).to_csv(OUT / "n131_trades_train.csv", index=False)
    summary = {"N130": s130, "N131": s131, "n131_vs_n110": "DISTINCT"}
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2))
    (OUT / "prescreen.md").write_text(
        "# D-092.1 N130/N131 pre-screen (train 2021–2023)\n\n"
        "N131 ≠ N110: daily Yahoo DXY z120+d20 inverse → US500cash 15:30–21:00 CET, "
        "not DXYcash M5 Lon-AM impulse traded 13:00–17:00 CET same-direction.\n\n"
        f"- **N130** EQW_BREADTH→US500: N={s130['n']} mean={s130['mean_bruto_bp']} "
        f"med={s130.get('median_bruto_bp')} gate={s130['gate_bp']} → **{s130['verdict']}** "
        f"years={s130.get('years')} long/short={s130.get('n_long')}/{s130.get('n_short')} "
        f"stress={s130.get('stress_note')}\n"
        f"- **N131** DXY_DOLLAR→US500: N={s131['n']} mean={s131['mean_bruto_bp']} "
        f"med={s131.get('median_bruto_bp')} gate={s131['gate_bp']} → **{s131['verdict']}** "
        f"years={s131.get('years')} long/short={s131.get('n_long')}/{s131.get('n_short')} "
        f"stress={s131.get('stress_note')}\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
