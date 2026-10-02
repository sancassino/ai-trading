#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N106 EURNZD LO 5d + N107 UK100→FRA40 cont."""
from __future__ import annotations
import gzip, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n106_n107_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
MIN_N = 150


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


def daily_close(m5: pd.DataFrame) -> pd.Series:
    m5 = m5.copy()
    m5["day"] = m5["time"].dt.normalize()
    rows = []
    for day, g in m5.groupby("day"):
        ref = g[g["time"] <= day + pd.Timedelta(hours=22)]
        if len(ref):
            rows.append((day, float(ref.iloc[-1]["close"])))
    s = pd.Series({d: c for d, c in rows}).sort_index()
    s.index = pd.DatetimeIndex(s.index).normalize()
    return s


def screen_n106(m5):
    """Long-only non-overlapping 5d momentum (ret5>0 → long hold 5d)."""
    dc = daily_close(m5)
    dates = list(dc.index)
    trades = []
    i = 5
    while i + 5 < len(dates):
        c_t = float(dc.iloc[i])
        c_lb = float(dc.iloc[i - 5])
        if c_lb <= 0 or c_t <= 0:
            i += 1
            continue
        ret5 = c_t / c_lb - 1.0
        if ret5 <= 0:
            i += 1
            continue
        c_exit = float(dc.iloc[i + 5])
        if c_exit <= 0:
            i += 1
            continue
        bruto = 1e4 * (c_exit - c_t) / c_t
        trades.append({"date": str(dates[i].date()), "side": 1, "bruto_bp": bruto, "ret5": ret5})
        i += 5
    return trades


def first_bar_at(g, day, h, m=0, span_min=15):
    t0 = day + pd.Timedelta(hours=h, minutes=m)
    t1 = t0 + pd.Timedelta(minutes=span_min)
    after = g[(g["time"] >= t0) & (g["time"] <= t1)]
    if after.empty:
        return None
    return after.iloc[0]


def first_bar_in(g, day, h0, m0, h1, m1):
    t0 = day + pd.Timedelta(hours=h0, minutes=m0)
    t1 = day + pd.Timedelta(hours=h1, minutes=m1)
    after = g[(g["time"] >= t0) & (g["time"] <= t1)]
    if after.empty:
        return None
    return after.iloc[0]


def screen_n107(uk: pd.DataFrame, fra: pd.DataFrame):
    """UK100 Lon-AM impulse → FRA40 afternoon same-dir session-flat."""
    uk = uk.copy()
    fra = fra.copy()
    uk["day"] = uk["time"].dt.normalize()
    fra["day"] = fra["time"].dt.normalize()
    days = sorted(set(uk["day"]).intersection(set(fra["day"])))
    trades = []
    for day in days:
        g = uk[uk["day"] == day]
        f = fra[fra["day"] == day]
        if g.empty or f.empty:
            continue
        b08 = first_bar_at(g, day, 8, 0, 15)
        if b08 is None:
            b08 = first_bar_in(g, day, 8, 0, 8, 30)
        b12 = first_bar_at(g, day, 12, 0, 15)
        if b08 is None or b12 is None:
            continue
        c08 = float(b08["close"])
        c12 = float(b12["close"])
        if c08 <= 0:
            continue
        uk_am_bp = 1e4 * (c12 / c08 - 1.0)
        if abs(uk_am_bp) < 40:
            continue
        side = 1 if uk_am_bp >= 40 else -1
        entry_bar = first_bar_in(f, day, 13, 0, 13, 15)
        if entry_bar is None:
            continue
        entry = float(entry_bar["close"])
        exit_win = f[
            (f["time"] >= day + pd.Timedelta(hours=17, minutes=30))
            & (f["time"] <= day + pd.Timedelta(hours=17, minutes=45))
        ]
        if exit_win.empty:
            before = f[f["time"] <= day + pd.Timedelta(hours=17, minutes=30)]
            if before.empty:
                continue
            exit_px = float(before.iloc[-1]["close"])
        else:
            exit_px = float(exit_win.iloc[0]["close"])
        if entry <= 0 or exit_px <= 0:
            continue
        bruto = side * 1e4 * (exit_px - entry) / entry
        trades.append(
            {
                "date": str(day.date()),
                "side": side,
                "uk_am_bp": uk_am_bp,
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
    t106 = screen_n106(load_m5("EURNZD"))
    t107 = screen_n107(load_m5("UK100cash"), load_m5("FRA40cash"))
    s106 = verdict(t106, 4.11, "N106", "EURNZD")
    s107 = verdict(t107, 5.94, "N107", "FRA40cash")
    pd.DataFrame(t106).to_csv(OUT / "n106_trades_train.csv", index=False)
    pd.DataFrame(t107).to_csv(OUT / "n107_trades_train.csv", index=False)
    summary = {"N106": s106, "N107": s107}
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2))
    (OUT / "prescreen.md").write_text(
        "# D-092.1 N106/N107 pre-screen (train 2021–2023)\n\n"
        f"- **N106** EURNZD LO 5d: N={s106['n']} mean={s106['mean_bruto_bp']} "
        f"med={s106.get('median_bruto_bp')} gate={s106['gate_bp']} → **{s106['verdict']}** "
        f"years={s106.get('years')}\n"
        f"- **N107** UK100→FRA40 afternoon cont: N={s107['n']} mean={s107['mean_bruto_bp']} "
        f"med={s107.get('median_bruto_bp')} gate={s107['gate_bp']} → **{s107['verdict']}** "
        f"years={s107.get('years')}\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
