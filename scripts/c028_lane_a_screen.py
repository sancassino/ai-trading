#!/usr/bin/env python3
"""C-028 Lane-A diagnostic mechanism screen (0 trials).

Three NEW_FAMILY mechanisms vs dead TSMOM / ORB / FX-med:
  1. OVERNIGHT_GAP_FADE — fade large overnight gaps on indices with RV filter
  2. FX_CARRY_TREND_RESIDUAL — FX carry orthogonalized vs medium-term trend
  3. XASSET_VOL_TIMING — cross-asset risk-on/off from VIX percentile

Hard rules:
  - Reserve 2025+: untouched (cut ≤ 2024-12-31)
  - No TRIALS.csv / TRIAL_COUNT
  - Free Yahoo / existing data/daily + FRED only
  - Bruto day-clustered t (before FTMO cost); promote if day_t >= 2
"""
from __future__ import annotations

import io

import csv
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/cto/c028_edge_upgrade"
CAL_END = pd.Timestamp("2024-12-31")
MIN_DAYS = 80
PROMOTE_T = 2.0


def day_t(x: np.ndarray) -> tuple[float, float, int]:
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    n = int(x.size)
    if n < 2:
        return float("nan"), float("nan"), n
    m = float(np.mean(x))
    s = float(np.std(x, ddof=1))
    if s <= 0:
        return m, float("nan"), n
    return m, m / (s / math.sqrt(n)), n


def load_ohlc(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";", comment="#")
    cols = {c.lower(): c for c in df.columns}
    # normalize
    rename = {}
    for want in ("date", "open", "high", "low", "close"):
        for c in df.columns:
            if c.lower().replace(" ", "") == want:
                rename[c] = want
                break
    df = df.rename(columns=rename)
    if "date" not in df.columns or "close" not in df.columns:
        raise ValueError(f"bad ohlc {path}")
    df["date"] = pd.to_datetime(df["date"].astype(str).str.replace(".", "-", regex=False))
    for c in ("open", "high", "low", "close"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["date", "close"]).sort_values("date")
    df = df[df["date"] <= CAL_END]
    return df.reset_index(drop=True)


def load_close(path: Path, date_col=None, close_col=None) -> pd.Series:
    # try ; then ,
    raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    # skip comment lines
    body = [ln for ln in raw if not ln.startswith("#")]
    text = "\n".join(body)
    sep = ";" if body and ";" in body[0] else ","
    df = pd.read_csv(io.StringIO(text), sep=sep)
    cols_l = {c.lower(): c for c in df.columns}
    dc = date_col or cols_l.get("date") or cols_l.get("observation_date")
    if close_col:
        cc = close_col
    else:
        for cand in ("adjclose", "close", "adj close", df.columns[-1].lower()):
            if cand in cols_l:
                cc = cols_l[cand]
                break
        else:
            cc = df.columns[-1]
    s = pd.Series(
        pd.to_numeric(df[cc], errors="coerce").values,
        index=pd.to_datetime(df[dc].astype(str).str.replace(".", "-", regex=False)),
        name=path.stem,
    )
    s = s[~s.index.duplicated(keep="last")].sort_index()
    s = s[s.index <= CAL_END].dropna()
    return s


def train_years(idx: pd.DatetimeIndex) -> float:
    if len(idx) < 2:
        return 0.0
    return float((idx.max() - idx.min()).days) / 365.25


# ---------------------------------------------------------------------------
# Family 1: OVERNIGHT_GAP_FADE
# ---------------------------------------------------------------------------
def screen_gap_fade() -> list[dict]:
    """Fade overnight gap when |gap| > k * RV20 and RV20 above median.

    PnL = -sign(gap) * (close/open - 1) * 1e4 bp when filter fires; else 0.
    Hold = same day (open→close). Lookback = RV window.
    """
    symbols = {
        "SPY": ROOT / "data/daily/SPY.csv",
        "NDX": ROOT / "data/daily/NDX.csv",
        "DAX": ROOT / "data/daily/DAX.csv",
        "CAC40": ROOT / "data/daily/CAC40.csv",
    }
    rows = []
    detail_rows = []
    for k_gap in (1.0, 1.5, 2.0):
        for rv_win in (10, 20):
            for sym, path in symbols.items():
                if not path.exists():
                    continue
                df = load_ohlc(path)
                if "open" not in df.columns:
                    continue
                df = df.copy()
                df["prev_close"] = df["close"].shift(1)
                df["gap"] = df["open"] / df["prev_close"] - 1.0
                df["ret_oc"] = df["close"] / df["open"] - 1.0
                df["ret_cc"] = df["close"].pct_change()
                df["rv"] = df["ret_cc"].rolling(rv_win).std()
                df["rv_med"] = df["rv"].rolling(252, min_periods=60).median()
                # need history; start after warm-up
                df = df.dropna(subset=["gap", "ret_oc", "rv", "rv_med"])
                # prefer ≥5y train ending 2024; use from 2010 or first avail
                start = max(df["date"].min(), pd.Timestamp("2005-01-01"))
                df = df[df["date"] >= start]
                fire = (df["gap"].abs() > k_gap * df["rv"]) & (df["rv"] > df["rv_med"])
                pnl = np.where(fire, -np.sign(df["gap"].values) * df["ret_oc"].values * 1e4, np.nan)
                # day returns only on fire days for t (trade-conditional)
                traded = pnl[np.isfinite(pnl)]
                m, t, n = day_t(traded)
                yrs = train_years(df["date"])
                short = yrs < 5.0
                promote = (
                    np.isfinite(t)
                    and t >= PROMOTE_T
                    and n >= MIN_DAYS
                    and yrs >= 5.0
                    and m > 0
                )
                row = {
                    "family": "OVERNIGHT_GAP_FADE",
                    "symbols": sym,
                    "lookback_hold": f"RV{rv_win}/k{k_gap}|hold=OC",
                    "train_years": round(yrs, 2),
                    "mean_bp": round(m, 3) if np.isfinite(m) else "",
                    "day_t": round(t, 3) if np.isfinite(t) else "",
                    "n_days": n,
                    "promote_to_lane_b": "yes" if promote else "no",
                    "notes": (
                        f"NEW_FAMILY; fade overnight gap when |gap|>k*RV & RV>med252; "
                        f"bruto trade-conditional; short={'yes' if short else 'no'}; ≤2024"
                    ),
                }
                rows.append(row)
                # save per-config detail
                detail_rows.append(
                    {
                        **row,
                        "k_gap": k_gap,
                        "rv_win": rv_win,
                        "fire_rate": float(fire.mean()) if len(fire) else 0.0,
                    }
                )
    # write family detail
    pd.DataFrame(detail_rows).to_csv(OUT / "family_overnight_gap_fade.csv", index=False)
    return rows


# ---------------------------------------------------------------------------
# Family 2: FX_CARRY_TREND_RESIDUAL
# ---------------------------------------------------------------------------
def screen_fx_carry_residual() -> list[dict]:
    """Long high-carry / short low-carry FX vs USD, residualized vs L60 trend.

    Carry proxy: FRED 3M interbank differential (monthly, ffilled).
    Signal = z(carry) - λ * z(L60 momentum); hold H days; rebalance every H.
    Universe: AUDUSD, NZDUSD, EURUSD, GBPUSD, USDJPY(inv), USDCHF(inv).
    """
    fx_files = {
        "AUDUSD": ROOT / "data/daily/AUDUSD.csv",
        "NZDUSD": ROOT / "data/daily/NZDUSD.csv",
        "EURUSD": ROOT / "data/daily/EURUSD.csv",
        "GBPUSD": ROOT / "data/daily/GBPUSD.csv",
        "USDJPY": ROOT / "data/daily/USDJPY.csv",
        "USDCHF": ROOT / "data/daily/USDCHF.csv",
    }
    # FRED monthly 3M rates (quote currency vs USD)
    rate_map = {
        "AUD": ROOT / "data/fred/IR3TIB01AUM156N.csv",
        "NZD": ROOT / "data/fred/IR3TIB01NZM156N.csv",
        "EUR": ROOT / "data/fred/IR3TIB01EZM156N.csv",
        "GBP": ROOT / "data/fred/IR3TIB01GBM156N.csv",
        "JPY": ROOT / "data/fred/IR3TIB01JPM156N.csv",
        "CHF": ROOT / "data/fred/IR3TIB01CHM156N.csv",
        "USD": ROOT / "data/fred/IR3TIB01USM156N.csv",
    }

    def load_rate(path: Path) -> pd.Series:
        df = pd.read_csv(path)
        s = pd.Series(
            pd.to_numeric(df.iloc[:, 1], errors="coerce").values,
            index=pd.to_datetime(df.iloc[:, 0]),
        ).dropna().sort_index()
        # monthly → daily ffill later
        return s[s.index <= CAL_END]

    rates = {k: load_rate(v) for k, v in rate_map.items() if v.exists()}
    if "USD" not in rates:
        pd.DataFrame().to_csv(OUT / "family_fx_carry_trend_residual.csv", index=False)
        return []

    # build USD-based FX panel (all quoted as XXXUSD; invert JPY/CHF)
    px = {}
    for sym, path in fx_files.items():
        if not path.exists():
            continue
        s = load_close(path)
        if sym in ("USDJPY", "USDCHF"):
            # invert → JPYUSD / CHFUSD
            s = 1.0 / s
            key = "JPYUSD" if sym == "USDJPY" else "CHFUSD"
        else:
            key = sym
        px[key] = s

    panel = pd.DataFrame(px).dropna(how="any")
    panel = panel[(panel.index >= "2005-01-01") & (panel.index <= CAL_END)]
    if panel.empty:
        pd.DataFrame().to_csv(OUT / "family_fx_carry_trend_residual.csv", index=False)
        return []

    # daily carry differential (foreign - USD), annualized % → daily expected ≈ diff/252
    ccy_of = {
        "AUDUSD": "AUD",
        "NZDUSD": "NZD",
        "EURUSD": "EUR",
        "GBPUSD": "GBP",
        "JPYUSD": "JPY",
        "CHFUSD": "CHF",
    }
    carry = {}
    usd_r = rates["USD"].reindex(panel.index, method="ffill")
    for col in panel.columns:
        ccy = ccy_of[col]
        if ccy not in rates:
            continue
        fr = rates[ccy].reindex(panel.index, method="ffill")
        carry[col] = (fr - usd_r) / 100.0  # decimal annualized
    carry_df = pd.DataFrame(carry).dropna(how="any")
    panel = panel.loc[carry_df.index]
    rets = panel.pct_change()

    rows = []
    detail = []
    for L in (60, 120):
        for H in (5, 10, 20):
            for lam in (0.5, 1.0):
                mom = panel.pct_change(L)
                # z-score cross-sectionally each day
                def xz(df):
                    mu = df.mean(axis=1)
                    sd = df.std(axis=1).replace(0, np.nan)
                    return df.sub(mu, axis=0).div(sd, axis=0)

                zc = xz(carry_df)
                zm = xz(mom.reindex(carry_df.index))
                sig = zc - lam * zm
                # long top 2 / short bottom 2 each rebalance day
                dates = carry_df.index
                reb = list(range(L + 5, len(dates), H))
                day_pnl = []
                day_idx = []
                for i in reb:
                    d = dates[i]
                    srow = sig.loc[d].dropna()
                    if len(srow) < 4:
                        continue
                    long = srow.nlargest(2).index.tolist()
                    short = srow.nsmallest(2).index.tolist()
                    # hold H days forward returns (sum daily equal-weight)
                    end = min(i + H, len(dates) - 1)
                    window = rets.iloc[i + 1 : end + 1]
                    if window.empty:
                        continue
                    long_r = window[long].mean(axis=1)
                    short_r = window[short].mean(axis=1)
                    # portfolio daily during hold
                    port = (long_r - short_r) * 1e4  # bp per day
                    for dt, v in port.items():
                        day_pnl.append(float(v))
                        day_idx.append(dt)
                # cluster by calendar day (already daily)
                m, t, n = day_t(np.array(day_pnl))
                # also trade-block mean for notes
                yrs = train_years(pd.DatetimeIndex(day_idx)) if day_idx else 0.0
                promote = (
                    np.isfinite(t)
                    and t >= PROMOTE_T
                    and n >= MIN_DAYS
                    and yrs >= 5.0
                    and m > 0
                )
                syms = ",".join(panel.columns)
                row = {
                    "family": "FX_CARRY_TREND_RESIDUAL",
                    "symbols": syms,
                    "lookback_hold": f"L{L}/H{H}/lam{lam}|LS2/S2",
                    "train_years": round(yrs, 2),
                    "mean_bp": round(m, 3) if np.isfinite(m) else "",
                    "day_t": round(t, 3) if np.isfinite(t) else "",
                    "n_days": n,
                    "promote_to_lane_b": "yes" if promote else "no",
                    "notes": (
                        "NEW_FAMILY; carry z − λ·mom z; FRED 3M diff; "
                        f"bruto daily port; short={'yes' if yrs < 5 else 'no'}; ≤2024"
                    ),
                }
                rows.append(row)
                detail.append({**row, "L": L, "H": H, "lam": lam})
    pd.DataFrame(detail).to_csv(OUT / "family_fx_carry_trend_residual.csv", index=False)
    return rows


# ---------------------------------------------------------------------------
# Family 3: XASSET_VOL_TIMING
# ---------------------------------------------------------------------------
def screen_xasset_vol_timing() -> list[dict]:
    """When VIX percentile high → long defensive (IEF/GLD), short/flat risk (SPY/DBC).

    Signal: VIX 252d percentile. If pct > thr → risk-off basket; else risk-on.
    Hold H days; lookback = percentile window.
    """
    paths = {
        "VIX": ROOT / "data/daily/VIX.csv",
        "SPY": ROOT / "data/daily/SPY.csv",
        "IEF": ROOT / "data/daily/IEF.csv",
        "GLD": ROOT / "data/daily/GLD.csv",
        "DBC": ROOT / "data/daily/DBC.csv",
        "HYG": ROOT / "data/daily/HYG.csv",
    }
    series = {}
    for k, p in paths.items():
        if p.exists():
            series[k] = load_close(p)
    need = ["VIX", "SPY", "IEF", "GLD"]
    if any(k not in series for k in need):
        pd.DataFrame().to_csv(OUT / "family_xasset_vol_timing.csv", index=False)
        return []

    panel = pd.DataFrame({k: series[k] for k in series}).dropna(how="any")
    panel = panel[(panel.index >= "2007-01-01") & (panel.index <= CAL_END)]
    rets = panel.pct_change()

    rows = []
    detail = []
    for win in (126, 252):
        for thr in (0.70, 0.80):
            for H in (5, 10, 20):
                vix = panel["VIX"]
                pct = vix.rolling(win).apply(
                    lambda x: pd.Series(x).rank(pct=True).iloc[-1], raw=False
                )
                # risk-off when high VIX pctile
                risk_off = pct > thr
                # baskets
                risk_on_ret = rets["SPY"]
                if "DBC" in rets.columns:
                    risk_on_ret = 0.7 * rets["SPY"] + 0.3 * rets["DBC"]
                def_ret = 0.6 * rets["IEF"] + 0.4 * rets["GLD"]
                # position: +1 risk-on / -1 risk-off; switch every day but hold signal lagged
                sig = np.where(risk_off, -1.0, 1.0)
                sig = pd.Series(sig, index=panel.index).shift(1)  # no peek
                # optional: hold H by sampling every H
                # use daily mark-to-market with lagged signal (standard timing)
                port = sig * (risk_on_ret - def_ret) * 1e4  # bp: long risk vs def when +1
                port = port.dropna()
                # also evaluate hold-H block version
                # primary = daily timing
                m, t, n = day_t(port.values)
                yrs = train_years(port.index)
                promote = (
                    np.isfinite(t)
                    and t >= PROMOTE_T
                    and n >= MIN_DAYS
                    and yrs >= 5.0
                    and m > 0
                )
                row = {
                    "family": "XASSET_VOL_TIMING",
                    "symbols": "SPY,DBC,IEF,GLD|VIX",
                    "lookback_hold": f"VIXpct{win}/thr{thr}|daily_vs_H{H}",
                    "train_years": round(yrs, 2),
                    "mean_bp": round(m, 3) if np.isfinite(m) else "",
                    "day_t": round(t, 3) if np.isfinite(t) else "",
                    "n_days": n,
                    "promote_to_lane_b": "yes" if promote else "no",
                    "notes": (
                        "NEW_FAMILY; VIX pctile → risk-on(SPY/DBC) vs def(IEF/GLD); "
                        f"bruto daily; short={'yes' if yrs < 5 else 'no'}; ≤2024"
                    ),
                }
                rows.append(row)
                # block-hold variant
                reb_pnl = []
                idx = list(range(win + 2, len(port), H))
                port_arr = port.values
                port_ix = port.index
                for i in idx:
                    sl = port_arr[i : i + H]
                    if len(sl) == 0:
                        continue
                    reb_pnl.append(float(np.nansum(sl)))  # bp over hold block
                mb, tb, nb = day_t(np.array(reb_pnl))
                row_b = {
                    "family": "XASSET_VOL_TIMING",
                    "symbols": "SPY,DBC,IEF,GLD|VIX",
                    "lookback_hold": f"VIXpct{win}/thr{thr}|blockH{H}",
                    "train_years": round(yrs, 2),
                    "mean_bp": round(mb, 3) if np.isfinite(mb) else "",
                    "day_t": round(tb, 3) if np.isfinite(tb) else "",
                    "n_days": nb,
                    "promote_to_lane_b": (
                        "yes"
                        if (
                            np.isfinite(tb)
                            and tb >= PROMOTE_T
                            and nb >= MIN_DAYS
                            and yrs >= 5.0
                            and mb > 0
                        )
                        else "no"
                    ),
                    "notes": (
                        "NEW_FAMILY; block-sum H days; VIX pctile timing; "
                        f"bruto; ≤2024"
                    ),
                }
                rows.append(row_b)
                detail.append({**row, "variant": "daily"})
                detail.append({**row_b, "variant": "block"})
    pd.DataFrame(detail).to_csv(OUT / "family_xasset_vol_timing.csv", index=False)
    return rows




def screen_gap_fade_pooled() -> list[dict]:
    """Pooled day-cluster overnight gap fade across indices."""
    symbols = {
        "SPY": ROOT / "data/daily/SPY.csv",
        "NDX": ROOT / "data/daily/NDX.csv",
        "DAX": ROOT / "data/daily/DAX.csv",
        "CAC40": ROOT / "data/daily/CAC40.csv",
    }
    rows = []
    detail = []
    for k_gap in (0.75, 1.0, 1.25):
        for rv_win in (10, 20):
            frames = []
            for sym, path in symbols.items():
                if not path.exists():
                    continue
                df = load_ohlc(path).copy()
                if "open" not in df.columns:
                    continue
                df["prev_close"] = df["close"].shift(1)
                df["gap"] = df["open"] / df["prev_close"] - 1.0
                df["ret_oc"] = df["close"] / df["open"] - 1.0
                df["ret_cc"] = df["close"].pct_change()
                df["rv"] = df["ret_cc"].rolling(rv_win).std()
                df["rv_med"] = df["rv"].rolling(252, min_periods=60).median()
                df = df.dropna(subset=["gap", "ret_oc", "rv", "rv_med"])
                df = df[df["date"] >= pd.Timestamp("2005-01-01")]
                fire = (df["gap"].abs() > k_gap * df["rv"]) & (df["rv"] > df["rv_med"])
                pnl = np.where(fire, -np.sign(df["gap"].values) * df["ret_oc"].values * 1e4, np.nan)
                frames.append(pd.Series(pnl, index=pd.to_datetime(df["date"]), name=sym))
            if not frames:
                continue
            panel = pd.concat(frames, axis=1, sort=True)
            day_means = panel.mean(axis=1, skipna=True).dropna()
            m, tstat, n = day_t(day_means.values)
            yrs = train_years(day_means.index)
            promote = (
                np.isfinite(tstat) and tstat >= PROMOTE_T and n >= MIN_DAYS and yrs >= 5.0 and m > 0
            )
            row = {
                "family": "OVERNIGHT_GAP_FADE",
                "symbols": "SPY+NDX+DAX+CAC40",
                "lookback_hold": f"RV{rv_win}/k{k_gap}|hold=OC|pooled",
                "train_years": round(yrs, 2),
                "mean_bp": round(m, 3) if np.isfinite(m) else "",
                "day_t": round(tstat, 3) if np.isfinite(tstat) else "",
                "n_days": n,
                "promote_to_lane_b": "yes" if promote else "no",
                "notes": "NEW_FAMILY; pooled day-cluster; bruto; ≤2024",
            }
            rows.append(row)
            detail.append(row)
    pd.DataFrame(detail).to_csv(OUT / "family_overnight_gap_fade_pooled.csv", index=False)
    return rows


def screen_commodity_seasonality() -> list[dict]:
    """Expanding month-of-year sign rule on commodity futures proxies."""
    comms = {
        "COFFEE_F": ROOT / "data/daily/COFFEE_F.csv",
        "CORN_F": ROOT / "data/daily/CORN_F.csv",
        "WTI_F": ROOT / "data/daily/WTI_F.csv",
        "COPPER_F": ROOT / "data/daily/COPPER_F.csv",
        "COCOA_F": ROOT / "data/daily/COCOA_F.csv",
        "CATTLE_F": ROOT / "data/daily/CATTLE_F.csv",
    }
    rows = []
    detail = []
    for sym, path in comms.items():
        if not path.exists():
            continue
        df = load_ohlc(path)
        df = df[df["date"] >= pd.Timestamp("2005-01-01")].copy()
        df["ret"] = df["close"].pct_change()
        df["month"] = df["date"].dt.month
        df["year"] = df["date"].dt.year
        df = df.dropna(subset=["ret"]).sort_values("date")
        years = sorted(df["year"].unique())
        pnl_days, dates = [], []
        for y in years:
            hist = df[df["year"] < y]
            if len(hist) < 252 * 3:
                continue
            mret = hist.groupby("month")["ret"].mean()
            cur = df[df["year"] == y]
            for _, r in cur.iterrows():
                sig = 1.0 if mret.get(r["month"], 0) > 0 else -1.0
                pnl_days.append(sig * r["ret"] * 1e4)
                dates.append(r["date"])
        m, tstat, n = day_t(np.array(pnl_days))
        yrs = train_years(pd.DatetimeIndex(dates)) if dates else 0.0
        promote = (
            np.isfinite(tstat) and tstat >= PROMOTE_T and n >= MIN_DAYS and yrs >= 5.0 and m > 0
        )
        row = {
            "family": "COMMODITY_SEASONALITY",
            "symbols": sym,
            "lookback_hold": "MoY_expanding|hold=1d",
            "train_years": round(yrs, 2),
            "mean_bp": round(m, 3) if np.isfinite(m) else "",
            "day_t": round(tstat, 3) if np.isfinite(tstat) else "",
            "n_days": n,
            "promote_to_lane_b": "yes" if promote else "no",
            "notes": "NEW_FAMILY; expanding month-of-year sign; bruto daily; ≤2024",
        }
        rows.append(row)
        detail.append(row)
    pd.DataFrame(detail).to_csv(OUT / "family_commodity_seasonality.csv", index=False)
    return rows


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    all_rows: list[dict] = []
    all_rows.extend(screen_gap_fade())
    all_rows.extend(screen_fx_carry_residual())
    all_rows.extend(screen_xasset_vol_timing())
    all_rows.extend(screen_gap_fade_pooled())
    all_rows.extend(screen_commodity_seasonality())

    # dedupe / rank: keep best day_t per family+symbols+lookback for shortlist clarity
    short = pd.DataFrame(all_rows)
    if short.empty:
        short = pd.DataFrame(
            columns=[
                "family",
                "symbols",
                "lookback_hold",
                "train_years",
                "mean_bp",
                "day_t",
                "n_days",
                "promote_to_lane_b",
                "notes",
            ]
        )
    else:
        short["day_t_num"] = pd.to_numeric(short["day_t"], errors="coerce")
        short = short.sort_values(["family", "day_t_num"], ascending=[True, False])

    cols = [
        "family",
        "symbols",
        "lookback_hold",
        "train_years",
        "mean_bp",
        "day_t",
        "n_days",
        "promote_to_lane_b",
        "notes",
    ]
    short[cols].to_csv(OUT / "lane_a_shortlist.csv", index=False)
    short[cols].to_csv(OUT / "lane_a_all_rows.csv", index=False)

    prom = short[short["promote_to_lane_b"] == "yes"] if not short.empty else short
    summary = {
        "c": "C-028",
        "when": "2026-10-01 Europe/Amsterdam",
        "n_rows": int(len(short)),
        "n_promote": int(len(prom)),
        "families": sorted(short["family"].unique().tolist()) if len(short) else [],
        "promote_rows": prom[cols].to_dict(orient="records") if len(prom) else [],
        "best_per_family": {},
    }
    if len(short):
        for fam, g in short.groupby("family"):
            g2 = g.dropna(subset=["day_t_num"]).head(1)
            if len(g2):
                summary["best_per_family"][fam] = g2[cols].iloc[0].to_dict()
    (OUT / "lane_a_screen_summary.json").write_text(
        json.dumps(summary, indent=2, default=str) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
