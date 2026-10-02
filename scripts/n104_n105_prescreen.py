#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N104 GBPCHF LO 5d + N105 JP225 Tokyo-AM→Lon cont."""
from __future__ import annotations
import gzip, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n104_n105_prescreen"
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


def screen_n104(m5):
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


def screen_n105(jp: pd.DataFrame):
    """JP225 Tokyo-AM impulse → Lon same-dir session-flat (entry 08:00, flat 14:00 CET)."""
    jp = jp.copy()
    jp["day"] = jp["time"].dt.normalize()
    days = sorted(set(jp["day"]))
    trades = []
    for day in days:
        g = jp[jp["day"] == day]
        if g.empty:
            continue
        # Asia open: 00:00±15; FTMO JP225 often starts ~01:00 CET → fallback [00:00, 01:15]
        b00 = first_bar_at(g, day, 0, 0, 15)
        if b00 is None:
            b00 = first_bar_in(g, day, 0, 0, 1, 15)
        b06 = first_bar_at(g, day, 6, 0, 15)
        if b00 is None or b06 is None:
            continue
        c00 = float(b00["close"])
        c06 = float(b06["close"])
        if c00 <= 0:
            continue
        jp_am_bp = 1e4 * (c06 / c00 - 1.0)
        if abs(jp_am_bp) < 40:
            continue
        side = 1 if jp_am_bp >= 40 else -1
        entry_bar = first_bar_at(g, day, 8, 0, 15)
        if entry_bar is None:
            continue
        entry = float(entry_bar["close"])
        exit_win = g[
            (g["time"] >= day + pd.Timedelta(hours=14))
            & (g["time"] <= day + pd.Timedelta(hours=14, minutes=15))
        ]
        if exit_win.empty:
            before = g[g["time"] <= day + pd.Timedelta(hours=14)]
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
                "jp_am_bp": jp_am_bp,
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
    t104 = screen_n104(load_m5("GBPCHF"))
    t105 = screen_n105(load_m5("JP225cash"))
    s104 = verdict(t104, 4.53, "N104", "GBPCHF")
    s105 = verdict(t105, 4.53, "N105", "JP225cash")
    pd.DataFrame(t104).to_csv(OUT / "n104_trades_train.csv", index=False)
    pd.DataFrame(t105).to_csv(OUT / "n105_trades_train.csv", index=False)
    summary = {"N104": s104, "N105": s105}
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2))
    (OUT / "prescreen.md").write_text(
        "# D-092.1 N104/N105 pre-screen (train 2021–2023)\n\n"
        f"- **N104** GBPCHF LO 5d: N={s104['n']} mean={s104['mean_bruto_bp']} "
        f"med={s104.get('median_bruto_bp')} gate={s104['gate_bp']} → **{s104['verdict']}** "
        f"years={s104.get('years')}\n"
        f"- **N105** JP225 Tokyo→Lon cont: N={s105['n']} mean={s105['mean_bruto_bp']} "
        f"med={s105.get('median_bruto_bp')} gate={s105['gate_bp']} → **{s105['verdict']}** "
        f"years={s105.get('years')}\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
