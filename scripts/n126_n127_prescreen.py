#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N126 DBA→US500 + N127 EWZ→US500.

Freeze (no thr-grid):
  N126: DBA z120 + d20 combo → US500cash 15:30→21:00 CET (NEW_FAMILY AU)
  N127: EWZ z40/thr1.5 stress_buy → US500cash 15:30→21:00 CET (NEW_FAMILY AV)
Gate: 3 × US500 RT 0.78 = 2.34 bp; N ≥ 150; train 2021–2023 only.
"""
from __future__ import annotations
import gzip, io, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n126_n127_prescreen"
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


def screen_combo_z120(sig: pd.Series, us500: pd.DataFrame):
    sig = sig.sort_index()
    z120 = (sig - sig.rolling(120, min_periods=120).mean()) / sig.rolling(
        120, min_periods=120
    ).std(ddof=0).replace(0, np.nan)
    d20 = sig / sig.shift(20) - 1.0
    pos = pd.Series(0.0, index=sig.index)
    pos[(z120 > 0.5) & (d20 > 0)] = 1.0
    pos[(z120 < -0.5) & (d20 < 0)] = -1.0
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
    dba = load_daily_close("DBA")
    ewz = load_daily_close("EWZ")
    us500 = load_m5("US500cash")
    t126 = screen_combo_z120(dba, us500)
    t127 = screen_stress_z40(ewz, us500)
    s126 = verdict(
        t126, GATE, "N126", "US500cash",
        "DBA_AG_STRESS z120+d20 combo; NEW_FAMILY AU; D-100 session-flat; ≠DBC",
    )
    s127 = verdict(
        t127, GATE, "N127", "US500cash",
        "EWZ_BRAZIL_STRESS z40/thr1.5 stress_buy; NEW_FAMILY AV; D-100 session-flat; ≠EEM/EMB/EFA",
    )
    pd.DataFrame(t126).to_csv(OUT / "n126_trades_train.csv", index=False)
    pd.DataFrame(t127).to_csv(OUT / "n127_trades_train.csv", index=False)
    summary = {"N126": s126, "N127": s127}
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2))
    (OUT / "prescreen.md").write_text(
        "# D-092.1 N126/N127 pre-screen (train 2021–2023)\n\n"
        f"- **N126** DBA_AG_STRESS→US500: N={s126['n']} mean={s126['mean_bruto_bp']} "
        f"med={s126.get('median_bruto_bp')} gate={s126['gate_bp']} → **{s126['verdict']}** "
        f"years={s126.get('years')} long/short={s126.get('n_long')}/{s126.get('n_short')} "
        f"stress={s126.get('stress_note')}\n"
        f"- **N127** EWZ_BRAZIL_STRESS→US500: N={s127['n']} mean={s127['mean_bruto_bp']} "
        f"med={s127.get('median_bruto_bp')} gate={s127['gate_bp']} → **{s127['verdict']}** "
        f"years={s127.get('years')} long/short={s127.get('n_long')}/{s127.get('n_short')} "
        f"stress={s127.get('stress_note')}\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
