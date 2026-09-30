#!/usr/bin/env python3
"""DIAGNOSTIC ONLY — XAU_AM_FADE power-pad.

Frozen PREREG rule unchanged: 0.60× ATR, entry 11:30, flat 14:00 Europe/Amsterdam.
Does NOT append TRIALS. Does NOT use 2025+ for any gate/decision.
Reproduces U2 train N=12 and reports whether N≥120 is reachable without retuning.
"""
from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EXT_K = 0.60
ATR_N = 14
OUT = ROOT / "results/cto/xau_am_fade_power"


def load_m5() -> tuple[pd.DataFrame, Path]:
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
    return df, path


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


def sim_day(g: pd.DataFrame, atr_price: float):
    day0 = g["time"].dt.normalize().iloc[0]
    asia = g[(g["time"] >= day0) & (g["time"] < day0 + pd.Timedelta(hours=8))]
    london = g[
        (g["time"] >= day0 + pd.Timedelta(hours=8))
        & (g["time"] <= day0 + pd.Timedelta(hours=11, minutes=30))
    ]
    win = g[
        (g["time"] >= day0 + pd.Timedelta(hours=8, minutes=30))
        & (g["time"] <= day0 + pd.Timedelta(hours=11, minutes=30))
    ]
    entry_rows = g[g["time"] == day0 + pd.Timedelta(hours=11, minutes=30)]
    b0800 = g[g["time"] == day0 + pd.Timedelta(hours=8)]
    if b0800.empty:
        b0800 = g[g["time"] >= day0 + pd.Timedelta(hours=8)].head(1)
    diag = {
        "date": str(day0.date()),
        "n_asia": len(asia),
        "n_london": len(london),
        "n_win": len(win),
        "has_1130": len(entry_rows) > 0,
        "has_0800": len(b0800) > 0,
        "up": None,
        "dn": None,
        "atr_bp": None,
        "trigger": None,
        "side": None,
    }
    if (
        asia.empty
        or london.empty
        or not (atr_price == atr_price)
        or win.empty
        or entry_rows.empty
        or b0800.empty
    ):
        diag["trigger"] = "NO_WINDOW"
        return None, diag
    asia_hi, asia_lo = float(asia["high"].max()), float(asia["low"].min())
    h = float(win["high"].max())
    l = float(win["low"].min())
    up = 1e4 * (h - asia_hi) / asia_hi if h > asia_hi else 0.0
    dn = 1e4 * (asia_lo - l) / asia_lo if l < asia_lo else 0.0
    p0800 = float(b0800.iloc[0]["open"])
    atr_bp = 1e4 * atr_price / p0800
    diag.update({"up": up, "dn": dn, "atr_bp": atr_bp})
    entry = float(entry_rows.iloc[0]["close"])
    if up >= EXT_K * atr_bp and up > dn:
        side, ext = -1, up
        diag["trigger"] = "SHORT"
    elif dn >= EXT_K * atr_bp and dn > up:
        side, ext = 1, dn
        diag["trigger"] = "LONG"
    else:
        diag["trigger"] = "NO_EXT"
        return None, diag
    diag["side"] = side
    asia_mid = 0.5 * (asia_hi + asia_lo)
    target = asia_mid
    stop = entry + (-side) * (ext / 1e4) * entry
    after = g[
        (g["time"] > entry_rows.iloc[0]["time"])
        & (g["time"] <= day0 + pd.Timedelta(hours=14))
    ]
    exit_px = float(after.iloc[-1]["close"]) if len(after) else entry
    for _, row in after.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        if side == 1:
            hit_t, hit_s = hi >= target, lo <= stop
        else:
            hit_t, hit_s = lo <= target, hi >= stop
        if hit_t and hit_s:
            exit_px = stop
            break
        if hit_s:
            exit_px = stop
            break
        if hit_t:
            exit_px = target
            break
    bruto = side * 1e4 * (exit_px - entry) / entry
    return bruto, diag


def count_k(sub: pd.DataFrame, atr: pd.Series, k: float) -> int:
    n = 0
    for day, g in sub.groupby(sub["time"].dt.normalize()):
        prior = atr[atr.index < day].dropna()
        if prior.empty:
            continue
        day0 = g["time"].dt.normalize().iloc[0]
        asia = g[(g["time"] >= day0) & (g["time"] < day0 + pd.Timedelta(hours=8))]
        win = g[
            (g["time"] >= day0 + pd.Timedelta(hours=8, minutes=30))
            & (g["time"] <= day0 + pd.Timedelta(hours=11, minutes=30))
        ]
        entry_rows = g[g["time"] == day0 + pd.Timedelta(hours=11, minutes=30)]
        b0800 = g[g["time"] == day0 + pd.Timedelta(hours=8)]
        if b0800.empty:
            b0800 = g[g["time"] >= day0 + pd.Timedelta(hours=8)].head(1)
        if asia.empty or win.empty or entry_rows.empty or b0800.empty:
            continue
        asia_hi, asia_lo = float(asia["high"].max()), float(asia["low"].min())
        h = float(win["high"].max())
        l = float(win["low"].min())
        up = 1e4 * (h - asia_hi) / asia_hi if h > asia_hi else 0.0
        dn = 1e4 * (asia_lo - l) / asia_lo if l < asia_lo else 0.0
        p0800 = float(b0800.iloc[0]["open"])
        atr_bp = 1e4 * float(prior.iloc[-1]) / p0800
        if (up >= k * atr_bp and up > dn) or (dn >= k * atr_bp and dn > up):
            n += 1
    return n


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    m5, path = load_m5()
    tmin, tmax = m5["time"].min(), m5["time"].max()
    year_cov = (
        m5.assign(year=m5["time"].dt.year)
        .groupby("year")
        .agg(n_bars=("time", "count"), t0=("time", "min"), t1=("time", "max"))
    )
    year_cov_rec = year_cov.assign(
        t0=year_cov["t0"].astype(str), t1=year_cov["t1"].astype(str)
    ).to_dict("index")

    atr = atr_map(m5)
    windows = {
        "2018-2020": (pd.Timestamp("2018-01-01"), pd.Timestamp("2020-12-31 23:59:59")),
        "2021-2023_train": (
            pd.Timestamp("2021-01-01"),
            pd.Timestamp("2023-12-31 23:59:59"),
        ),
        "2024_test": (pd.Timestamp("2024-01-01"), pd.Timestamp("2024-12-31 23:59:59")),
        "2025plus_present_NOT_FOR_DECISION": (
            pd.Timestamp("2025-01-01"),
            pd.Timestamp("2099-01-01"),
        ),
    }
    results = {}
    all_diags = []
    for label, (a, b) in windows.items():
        sub = m5[(m5["time"] >= a) & (m5["time"] <= b)]
        if sub.empty:
            results[label] = {
                "n_bars": 0,
                "n_days_with_m5": 0,
                "n_eligible_windows": 0,
                "n_signals": 0,
                "mean_bruto_bp": None,
                "note": "NO_DATA",
            }
            continue
        trades = []
        eligible = no_ext = no_win = 0
        for day, g in sub.groupby(sub["time"].dt.normalize()):
            prior = atr[atr.index < day].dropna()
            atr_p = float(prior.iloc[-1]) if not prior.empty else np.nan
            bruto, diag = sim_day(g.copy(), atr_p)
            diag["window"] = label
            all_diags.append(diag)
            if diag["trigger"] == "NO_WINDOW":
                no_win += 1
                continue
            eligible += 1
            if diag["trigger"] == "NO_EXT":
                no_ext += 1
                continue
            if bruto is not None:
                trades.append(bruto)
        results[label] = {
            "n_bars": int(len(sub)),
            "n_days_with_m5": int(sub["time"].dt.normalize().nunique()),
            "n_eligible_windows": eligible,
            "n_no_window": no_win,
            "n_no_ext": no_ext,
            "n_signals": len(trades),
            "mean_bruto_bp": float(np.mean(trades)) if trades else None,
            "hit_rate_vs_eligible": (len(trades) / eligible) if eligible else None,
            "note": (
                "DIAGNOSTIC_ONLY — 2025+ not for decision"
                if "2025" in label
                else "DIAGNOSTIC_ONLY"
            ),
        }

    train = m5[
        (m5["time"] >= pd.Timestamp("2021-01-01"))
        & (m5["time"] <= pd.Timestamp("2023-12-31 23:59:59"))
    ]
    sens = {str(k): count_k(train, atr, k) for k in (0.45, 0.60, 0.75)}

    ratios = [
        max(d["up"] or 0, d["dn"] or 0) / d["atr_bp"]
        for d in all_diags
        if d.get("window") == "2021-2023_train" and d.get("atr_bp")
    ]
    pct = {}
    if ratios:
        arr = np.array(ratios)
        for p in (50, 75, 90, 95, 99):
            pct[f"p{p}"] = float(np.percentile(arr, p))
        pct["max"] = float(arr.max())
        pct["frac_ge_0.60"] = float((arr >= 0.60).mean())
        pct["frac_ge_0.45"] = float((arr >= 0.45).mean())
        pct["frac_ge_0.30"] = float((arr >= 0.30).mean())
        pct["n_eligible"] = int(len(arr))

    n_train = results["2021-2023_train"]["n_signals"]
    conclusion = (
        f"STRUCTURAL underpower: m5gz/XAUUSD.csv.gz starts {tmin.date()} — no 2018–2020. "
        f"Train 2021–2023 N={n_train} under frozen 0.60× (≪120). "
        f"Eligible={results['2021-2023_train']['n_eligible_windows']}; "
        f"hit_rate={results['2021-2023_train']['hit_rate_vs_eligible']}. "
        f"Not a TZ/filter bug (windows present). "
        f"Watch-only; new PREREG if N≥120 needed. Do NOT loosen 0.60×."
    )
    summary = {
        "label": "DIAGNOSTIC_ONLY_XAU_AM_FADE_POWER",
        "frozen_rule": "0.60×ATR, 11:30, 14:00 Europe/Amsterdam — UNCHANGED",
        "data_file": str(path.relative_to(ROOT)),
        "data_span": {"min": str(tmin), "max": str(tmax)},
        "year_coverage": year_cov_rec,
        "windows": results,
        "report_only_threshold_N_train_2021_2023": sens,
        "ext_vs_atr_distribution_eligible_train": pct,
        "conclusion": conclusion,
    }
    (OUT / "power_summary.json").write_text(json.dumps(summary, indent=2, default=str))
    pd.DataFrame(all_diags).to_csv(OUT / "day_diag.csv", index=False)
    (OUT / "README.md").write_text(
        f"""# XAU_AM_FADE power-pad — DIAGNOSTIC ONLY

**Not a trial. Frozen thresholds unchanged (0.60× ATR, 11:30 entry, 14:00 flat).**
**Reserve 2025+ not used for any gate/decision.**

## Finding
{conclusion}

## N breakdown
| Window | N signals | Eligible days | Note |
|--------|-----------|---------------|------|
| 2018–2020 | {results['2018-2020']['n_signals']} | {results['2018-2020'].get('n_eligible_windows', 0)} | {results['2018-2020'].get('note')} |
| 2021–2023 train | {results['2021-2023_train']['n_signals']} | {results['2021-2023_train'].get('n_eligible_windows', 0)} | matches U2 gate N=12 |
| 2024 test | {results['2024_test']['n_signals']} | {results['2024_test'].get('n_eligible_windows', 0)} | report only |

Report-only threshold sensitivity N(train): {sens}
ext/ATR distribution (eligible train): {pct}

## Recommendation
Keep sleeve **watch-only**. Ask Strateeg for a *new* PREREG with different mechanism if N cannot reach 120 without post-hoc threshold change. **Do not loosen 0.60×.** No formal `ftmo_ev`.

Reproduce: `/workspace/venv-u2/bin/python scripts/xau_am_fade_power_diag.py`
"""
    )
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
