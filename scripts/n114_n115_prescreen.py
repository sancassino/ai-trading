#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N114 HYG→US500 + N115 EURUSD Lon-AM→US500."""
from __future__ import annotations
import gzip, io, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n114_n115_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
MIN_N = 150
GATE = 2.34  # 3 × US500 RT 0.78


def load_daily_close(sym: str) -> pd.Series:
    path = ROOT / "data" / "daily" / f"{sym}.csv"
    raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    body = [ln for ln in raw if not ln.startswith("#")]
    sep = ";" if body and ";" in body[0] else ","
    df = pd.read_csv(io.StringIO("\n".join(body)), sep=sep)
    cols = {c.lower().replace(" ", ""): c for c in df.columns}
    dc = cols.get("date") or cols.get("observation_date")
    cc = cols.get("close") or cols.get("adjclose")
    s = pd.Series(
        pd.to_numeric(df[cc], errors="coerce").values,
        index=pd.DatetimeIndex(pd.to_datetime(df[dc].astype(str).str.replace(".", "-", regex=False))).normalize(),
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
    bruto = side * 1e4 * (p1 / p0 - 1.0)
    return bruto


def screen_n114(hyg: pd.Series, us500: pd.DataFrame):
    """HYG z120 + d20 combo → US500 session-flat next day."""
    hyg = hyg.sort_index()
    z120 = (hyg - hyg.rolling(120, min_periods=120).mean()) / hyg.rolling(
        120, min_periods=120
    ).std(ddof=0).replace(0, np.nan)
    d20 = hyg / hyg.shift(20) - 1.0
    pos = pd.Series(0.0, index=hyg.index)
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


def screen_n115(eur: pd.DataFrame, us500: pd.DataFrame):
    """EURUSD Lon-AM impulse → same-dir US500 NY session-flat."""
    eur = eur.copy()
    us500 = us500.copy()
    eur["day"] = eur["time"].dt.normalize()
    us500["day"] = us500["time"].dt.normalize()
    days = sorted(set(eur["day"]).intersection(set(us500["day"])))
    trades = []
    for day in days:
        g = eur[eur["day"] == day]
        u = us500[us500["day"] == day]
        if g.empty or u.empty:
            continue
        b08 = first_bar_at(g, day, 8, 0, 15)
        b12 = first_bar_at(g, day, 12, 0, 15)
        if b08 is None or b12 is None:
            continue
        c08 = float(b08["close"])
        c12 = float(b12["close"])
        if c08 <= 0:
            continue
        eur_am_bp = 1e4 * (c12 / c08 - 1.0)
        if abs(eur_am_bp) < 25:
            continue
        side = 1 if eur_am_bp >= 25 else -1
        bruto = session_flat_trade(u, side)
        if bruto is None:
            continue
        trades.append(
            {
                "date": str(pd.Timestamp(day).date()),
                "side": side,
                "eur_am_bp": eur_am_bp,
                "bruto_bp": bruto,
            }
        )
    return trades


def verdict(trades, gate, label, instrument):
    n = len(trades)
    if n == 0:
        return {
            "id": label,
            "instrument": instrument,
            "n": 0,
            "mean_bruto_bp": None,
            "gate_bp": gate,
            "verdict": "FAIL",
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
        "verdict": v,
        "hit_rate": round(float((arr > 0).mean()), 4),
        "years": {
            str(y): round(
                float(np.mean([t["bruto_bp"] for t in trades if t["date"].startswith(str(y))])),
                4,
            )
            for y in (2021, 2022, 2023)
            if any(t["date"].startswith(str(y)) for t in trades)
        },
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    hyg = load_daily_close("HYG")
    us500 = load_m5("US500cash")
    eur = load_m5("EURUSD")
    t114 = screen_n114(hyg, us500)
    t115 = screen_n115(eur, us500)
    s114 = verdict(t114, GATE, "N114", "US500cash")
    s115 = verdict(t115, GATE, "N115", "US500cash")
    pd.DataFrame(t114).to_csv(OUT / "n114_trades_train.csv", index=False)
    pd.DataFrame(t115).to_csv(OUT / "n115_trades_train.csv", index=False)
    summary = {"N114": s114, "N115": s115}
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2))
    (OUT / "prescreen.md").write_text(
        "# D-092.1 N114/N115 pre-screen (train 2021–2023)\n\n"
        f"- **N114** HYG_CREDIT_STRESS→US500: N={s114['n']} mean={s114['mean_bruto_bp']} "
        f"med={s114.get('median_bruto_bp')} gate={s114['gate_bp']} → **{s114['verdict']}** "
        f"years={s114.get('years')}\n"
        f"- **N115** EURUSD Lon-AM→US500: N={s115['n']} mean={s115['mean_bruto_bp']} "
        f"med={s115.get('median_bruto_bp')} gate={s115['gate_bp']} → **{s115['verdict']}** "
        f"years={s115.get('years')}\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
