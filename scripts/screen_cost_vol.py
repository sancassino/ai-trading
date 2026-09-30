#!/usr/bin/env python3
"""D-091 prio 2: cost/vol screen over data/m5gz → results/screen_cost_vol.csv
Discovery window 2021-01-01 .. 2024-12-31. No strategy, no 2025+ bars used.
"""
from __future__ import annotations

import csv
import gzip
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
M5DIR = ROOT / "data" / "m5gz"
COSTS = ROOT / "COSTS_FTMO.csv"
OUT = ROOT / "results" / "screen_cost_vol.csv"
START = pd.Timestamp("2021-01-01")
END = pd.Timestamp("2024-12-31 23:59:59")


def load_costs() -> dict[str, float]:
    """symbol -> roundtrip_intraday_bp."""
    out: dict[str, float] = {}
    with COSTS.open() as f:
        # skip comment lines starting with #
        lines = [ln for ln in f if ln.strip() and not ln.startswith("#")]
    reader = csv.DictReader(lines, delimiter=";")
    for row in reader:
        sym = row["symbol"].strip()
        try:
            out[sym] = float(row["roundtrip_intraday_bp"])
        except (KeyError, ValueError):
            continue
    return out


def load_m5(path: Path) -> pd.DataFrame | None:
    with gzip.open(path, "rt") as f:
        # first line may be # meta
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    if df.empty or "time" not in df.columns:
        return None
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M", errors="coerce")
    df = df.dropna(subset=["time"])
    df = df[(df["time"] >= START) & (df["time"] <= END)]
    if df.empty:
        return None
    for c in ("open", "high", "low", "close"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["open", "high", "low", "close"])
    return df


def metrics(df: pd.DataFrame) -> dict:
    mid = (df["high"] + df["low"]) / 2.0
    bar_range_bp = (df["high"] - df["low"]) / mid.replace(0, np.nan) * 1e4
    med_m5 = float(np.nanmedian(bar_range_bp.to_numpy()))

    day = df.set_index("time")
    ohlc = day.resample("1D").agg({"open": "first", "high": "max", "low": "min", "close": "last"})
    ohlc = ohlc.dropna()
    if ohlc.empty:
        med_day = float("nan")
        n_days = 0
    else:
        day_range_bp = (ohlc["high"] - ohlc["low"]) / ohlc["open"].replace(0, np.nan) * 1e4
        med_day = float(np.nanmedian(day_range_bp.to_numpy()))
        n_days = int(len(ohlc))
    return {
        "n_bars": int(len(df)),
        "n_days": n_days,
        "median_m5_range_bp": med_m5,
        "median_day_range_bp": med_day,
        "start": str(df["time"].min().date()),
        "end": str(df["time"].max().date()),
    }


def main() -> None:
    costs = load_costs()
    rows = []
    files = sorted(M5DIR.glob("*.csv.gz"))
    for path in files:
        sym = path.name.replace(".csv.gz", "")
        df = load_m5(path)
        if df is None:
            rows.append(
                {
                    "symbol": sym,
                    "rt_intraday_bp": costs.get(sym, float("nan")),
                    "n_bars": 0,
                    "n_days": 0,
                    "median_day_range_bp": float("nan"),
                    "median_m5_range_bp": float("nan"),
                    "rt_over_day": float("nan"),
                    "rt_over_m5": float("nan"),
                    "cost_in_costs_ftmo": sym in costs,
                    "start": "",
                    "end": "",
                    "note": "no_bars_in_window",
                }
            )
            continue
        m = metrics(df)
        rt = costs.get(sym, float("nan"))
        day = m["median_day_range_bp"]
        m5 = m["median_m5_range_bp"]
        rows.append(
            {
                "symbol": sym,
                "rt_intraday_bp": rt,
                "n_bars": m["n_bars"],
                "n_days": m["n_days"],
                "median_day_range_bp": round(day, 4) if day == day else float("nan"),
                "median_m5_range_bp": round(m5, 4) if m5 == m5 else float("nan"),
                "rt_over_day": round(rt / day, 6) if day and day == day and day > 0 else float("nan"),
                "rt_over_m5": round(rt / m5, 6) if m5 and m5 == m5 and m5 > 0 else float("nan"),
                "cost_in_costs_ftmo": sym in costs,
                "start": m["start"],
                "end": m["end"],
                "note": "" if sym in costs else "missing_from_COSTS_FTMO",
            }
        )
        print(f"ok {sym} n_days={m['n_days']} rt={rt} day={day:.2f} m5={m5:.2f}", flush=True)

    out = pd.DataFrame(rows)
    # Rank: lower rt_over_day = cheaper vs vol (better); missing costs last
    out["rank_day"] = out["rt_over_day"].rank(method="min", na_option="bottom")
    out["rank_m5"] = out["rt_over_m5"].rank(method="min", na_option="bottom")
    out = out.sort_values(["rank_day", "rank_m5", "symbol"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)
    print(f"Wrote {OUT} rows={len(out)}", flush=True)


if __name__ == "__main__":
    main()
