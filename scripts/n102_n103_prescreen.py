#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N102 USDCHF LO 5d + N103 GER40→US30 industrial lag."""
from __future__ import annotations
import gzip, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n102_n103_prescreen"
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


def screen_n102(m5):
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


def screen_n103(ger: pd.DataFrame, us30: pd.DataFrame):
    """GER Lon-AM impulse → US30 NY same-dir session-flat."""
    ger = ger.copy()
    us30 = us30.copy()
    ger["day"] = ger["time"].dt.normalize()
    us30["day"] = us30["time"].dt.normalize()
    days = sorted(set(ger["day"]).intersection(set(us30["day"])))
    trades = []
    for day in days:
        g = ger[ger["day"] == day]
        u = us30[us30["day"] == day]
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
        ger_am_bp = 1e4 * (c12 / c08 - 1.0)
        if abs(ger_am_bp) < 40:
            continue
        side = 1 if ger_am_bp >= 40 else -1
        entry_bar = first_bar_at(u, day, 15, 30, 15)
        if entry_bar is None:
            continue
        entry = float(entry_bar["close"])
        exit_win = u[
            (u["time"] >= day + pd.Timedelta(hours=21))
            & (u["time"] <= day + pd.Timedelta(hours=21, minutes=15))
        ]
        if exit_win.empty:
            # fallback: last bar <= 21:00
            before = u[u["time"] <= day + pd.Timedelta(hours=21)]
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
                "ger_am_bp": ger_am_bp,
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
    t102 = screen_n102(load_m5("USDCHF"))
    t103 = screen_n103(load_m5("GER40cash"), load_m5("US30cash"))
    s102 = verdict(t102, 3.03, "N102", "USDCHF")
    s103 = verdict(t103, 1.35, "N103", "US30cash")
    pd.DataFrame(t102).to_csv(OUT / "n102_trades_train.csv", index=False)
    pd.DataFrame(t103).to_csv(OUT / "n103_trades_train.csv", index=False)
    summary = {"N102": s102, "N103": s103}
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2))
    (OUT / "prescreen.md").write_text(
        "# D-092.1 N102/N103 pre-screen (train 2021–2023)\n\n"
        f"- **N102** USDCHF LO 5d: N={s102['n']} mean={s102['mean_bruto_bp']} "
        f"med={s102.get('median_bruto_bp')} gate={s102['gate_bp']} → **{s102['verdict']}** "
        f"years={s102.get('years')}\n"
        f"- **N103** GER40→US30 industrial lag: N={s103['n']} mean={s103['mean_bruto_bp']} "
        f"med={s103.get('median_bruto_bp')} gate={s103['gate_bp']} → **{s103['verdict']}** "
        f"years={s103.get('years')}\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
