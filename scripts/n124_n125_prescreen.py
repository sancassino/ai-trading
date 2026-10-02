#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N124 YIELD_CURVE_2S10S + N125 DEFENSIVE_CYCLICAL
(Lane-B session-flat US500 from S2 cycle_2346 @ 13fe10c).

Freeze (no thr-grid):
  N124: 10Y-3M slope z60/thr1.5/flatten_fade → US500cash 15:30→21:00 CET
  N125: XLU/XLI z40/thr0.5/defensive_high → US500cash 15:30→21:00 CET (US500 twin per S2 FLAG)
Gate: 3 × US500 RT 0.78 = 2.34 bp; N ≥ 150; train 2021–2023 only.
"""
from __future__ import annotations
import gzip, io, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n124_n125_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
MIN_N = 150
GATE = 2.34  # 3 × US500 RT 0.78


def load_daily(sym: str) -> pd.Series:
    path = ROOT / "data" / "daily" / f"{sym}.csv"
    raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    body = [ln for ln in raw if not ln.startswith("#")]
    sep = ";" if body and ";" in body[0] else ","
    df = pd.read_csv(io.StringIO("\n".join(body)), sep=sep)
    cols = {c.lower().replace(" ", ""): c for c in df.columns}
    dc = cols.get("date") or cols.get("observation_date")
    # prefer adjclose (S2 Lane-A load_close)
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


def zscore(s: pd.Series, win: int) -> pd.Series:
    # Match S2: min_periods = max(20, win // 3)
    mp = max(20, win // 3)
    mu = s.rolling(win, min_periods=mp).mean()
    sd = s.rolling(win, min_periods=mp).std(ddof=0)
    return (s - mu) / sd.replace(0, np.nan)


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


def screen_z_threshold(sig: pd.Series, us500: pd.DataFrame, win: int, thr: float, mode: str):
    """z-threshold → US500 session-flat next day.
    flatten_fade / defensive_high: z>+thr → SHORT; z<-thr → LONG.
    """
    sig = sig.sort_index()
    z = zscore(sig, win)
    pos = pd.Series(0.0, index=sig.index)
    if mode in ("flatten_fade", "defensive_high"):
        pos[z > thr] = -1.0
        pos[z < -thr] = 1.0
    else:
        raise ValueError(f"unsupported mode {mode}")

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
                "z": float(z.loc[prior.index[-1]]) if prior.index[-1] in z.index else None,
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
    y10 = load_daily("YLD_US10Y")
    y3m = load_daily("YLD_US3M")
    slope = (y10 - y3m).dropna()
    xlu = load_daily("XLU")
    xli = load_daily("XLI")
    ratio = (xlu / xli).dropna()
    us500 = load_m5("US500cash")

    t124 = screen_z_threshold(slope, us500, win=60, thr=1.5, mode="flatten_fade")
    t125 = screen_z_threshold(ratio, us500, win=40, thr=0.5, mode="defensive_high")
    s124 = verdict(
        t124,
        GATE,
        "N124",
        "US500cash",
        "YIELD_CURVE_2S10S 10Y-3M z60/thr1.5/flatten_fade; S2 13fe10c; D-100 session-flat",
    )
    s125 = verdict(
        t125,
        GATE,
        "N125",
        "US500cash",
        "DEFENSIVE_CYCLICAL XLU/XLI z40/thr0.5/defensive_high US500 twin (not US100); S2 FLAG; D-100 session-flat",
    )
    pd.DataFrame(t124).to_csv(OUT / "n124_trades_train.csv", index=False)
    pd.DataFrame(t125).to_csv(OUT / "n125_trades_train.csv", index=False)
    summary = {"N124": s124, "N125": s125, "source_s2": "13fe10c", "cycle": "cycle_2346"}
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2))
    (OUT / "prescreen.md").write_text(
        "# D-092.1 N124/N125 pre-screen (train 2021–2023; S2 cycle_2346 → Lane-B)\n\n"
        f"- **N124** YIELD_CURVE_2S10S→US500: N={s124['n']} mean={s124['mean_bruto_bp']} "
        f"med={s124.get('median_bruto_bp')} gate={s124['gate_bp']} → **{s124['verdict']}** "
        f"years={s124.get('years')} long/short={s124.get('n_long')}/{s124.get('n_short')} "
        f"stress={s124.get('stress_note')}\n"
        f"- **N125** DEFENSIVE_CYCLICAL→US500 twin: N={s125['n']} mean={s125['mean_bruto_bp']} "
        f"med={s125.get('median_bruto_bp')} gate={s125['gate_bp']} → **{s125['verdict']}** "
        f"years={s125.get('years')} long/short={s125.get('n_long')}/{s125.get('n_short')} "
        f"stress={s125.get('stress_note')}\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
