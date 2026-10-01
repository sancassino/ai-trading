#!/usr/bin/env python3
"""Strateeg-2 Lane-A novelty screens — C-028 / cycle ~12:40 Europe/Amsterdam 2026-10-01.

≥3 NEW_FAMILY mechanisms vs last-30d dead set (ORB / classic TSMOM / L60 FX-med /
ENERGY / IDX_SHORT / FX_EUR_SHORT / FX_USDJPY_MED / FX_EURJPY_MED) and vs CTO C-028
already-screened (COMMODITY_SEASONALITY, OVERNIGHT_GAP_FADE, XASSET_VOL_TIMING,
FX_CARRY_TREND_RESIDUAL) and vs Strateeg OPEN N75–N77 (metal-pair MR, UKOIL inventory,
FX XS rank-rev).

Families this cycle (all NEW_FAMILY):
  A) CREDIT_SPREAD_PROXY  — HYG/LQD credit impulse → SPY / NDX / TLT timing
  B) RATE_CURVE_SHAPE     — TNX−FVX (10s5s) slope level+Δ → SPY / TLT
  C) VIX_TERM_VOV         — VIX9D/VIX3M term + |ΔVIX| VoV regime → SPY
  D) EM_DM_FLOW_ROTATION  — EEM/EFA relative + DXY filter (equity geo rotation)

Rules: Yahoo/proxy daily; cut ≤2024-12-31; reserve 2025+ untouched; day_t bruto;
promote if day_t≥2 & n≥80 & years≥5 & mean_bp>0. Diagnostic ≠ trial. No PREREG here.
"""
from __future__ import annotations

import io
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DAILY = ROOT / "data" / "daily"
OUT = ROOT / "results" / "strateeg2_prescreen" / "cycle_1240"
CAL_END = pd.Timestamp("2024-12-31")
CAL_START = pd.Timestamp("2005-01-01")
MIN_DAYS = 80
PROMOTE_T = 2.0
OUT.mkdir(parents=True, exist_ok=True)


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


def load_close(path: Path) -> pd.Series:
    raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    body = [ln for ln in raw if not ln.startswith("#")]
    sep = ";" if body and ";" in body[0] else ","
    df = pd.read_csv(io.StringIO("\n".join(body)), sep=sep)
    cols_l = {c.lower().replace(" ", ""): c for c in df.columns}
    dc = cols_l.get("date") or cols_l.get("observation_date")
    for cand in ("adjclose", "close", "adjclose"):
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
    s = s[(s.index >= CAL_START) & (s.index <= CAL_END)].dropna()
    return s


def train_years(idx: pd.DatetimeIndex) -> float:
    if len(idx) < 2:
        return 0.0
    return float((idx.max() - idx.min()).days) / 365.25


def zscore(s: pd.Series, win: int) -> pd.Series:
    mu = s.rolling(win, min_periods=max(20, win // 3)).mean()
    sd = s.rolling(win, min_periods=max(20, win // 3)).std(ddof=0)
    return (s - mu) / sd.replace(0, np.nan)


def summarize_row(family, symbols, lookback_hold, pnl: pd.Series, notes: str) -> dict:
    # trade-conditional: only days with non-zero position pnl recorded as finite
    traded = pnl[np.isfinite(pnl) & (pnl != 0)]
    # also compute all-days (incl flat=0) for robustness note
    all_days = pnl[np.isfinite(pnl)]
    m, t, n = day_t(traded.values)
    m_all, t_all, n_all = day_t(all_days.values)
    yrs = train_years(pnl.dropna().index)
    short = yrs < 5.0
    promote = (
        np.isfinite(t)
        and t >= PROMOTE_T
        and n >= MIN_DAYS
        and yrs >= 5.0
        and m > 0
    )
    return {
        "family": family,
        "symbols": symbols,
        "lookback_hold": lookback_hold,
        "train_years": round(yrs, 2),
        "mean_bp": round(m, 3) if np.isfinite(m) else "",
        "day_t": round(t, 3) if np.isfinite(t) else "",
        "n_days": n,
        "mean_bp_alldays": round(m_all, 3) if np.isfinite(m_all) else "",
        "day_t_alldays": round(t_all, 3) if np.isfinite(t_all) else "",
        "n_alldays": n_all,
        "promote_to_lane_b": "yes" if promote else "no",
        "notes": notes + (f"; short_hist={'yes' if short else 'no'}; ≤2024"),
    }


# ---------------------------------------------------------------------------
# A) CREDIT_SPREAD_PROXY
# ---------------------------------------------------------------------------
def screen_credit_spread() -> list[dict]:
    """HYG/LQD = credit risk-on proxy. Improve → long risk asset next day.

    Mechanism: credit spreads compress → risk appetite ↑ → equities/credit beta.
    NOT single-asset TSMOM; NOT FX-med; NOT ORB.
    """
    hyg = load_close(DAILY / "HYG.csv")
    lqd = load_close(DAILY / "LQD.csv")
    targets = {
        "SPY": load_close(DAILY / "SPY.csv"),
        "NDX": load_close(DAILY / "NDX.csv") if (DAILY / "NDX.csv").exists() else None,
        "TLT": load_close(DAILY / "TLT.csv"),  # defensive: opposite sign expected
        "IWM": load_close(DAILY / "IWM.csv"),
    }
    ratio = (hyg / lqd).dropna()
    rows = []
    detail = []
    for z_win in (40, 60, 90):
        for thr in (0.5, 1.0, 1.5):
            z = zscore(ratio, z_win)
            for tgt_name, tgt in targets.items():
                if tgt is None:
                    continue
                df = pd.concat(
                    {"z": z, "px": tgt, "ret1": tgt.pct_change().shift(-1)},
                    axis=1,
                ).dropna()
                # risk-on when z>thr (HYG rich vs LQD); risk-off when z<-thr
                # For TLT: flip (credit improve → bonds lag)
                sign = -1.0 if tgt_name == "TLT" else 1.0
                pos = pd.Series(0.0, index=df.index)
                pos[df["z"] > thr] = sign
                pos[df["z"] < -thr] = -sign
                pnl = pos * df["ret1"] * 1e4  # bp
                # zero days stay 0 — summarize uses non-zero only for trade-cond t
                row = summarize_row(
                    "CREDIT_SPREAD_PROXY",
                    f"HYG/LQD→{tgt_name}",
                    f"z{z_win}/thr{thr}|hold=1d",
                    pnl,
                    "NEW_FAMILY; HYG/LQD z-impulse → next-day asset; bruto trade-cond",
                )
                rows.append(row)
                detail.append({**row, "z_win": z_win, "thr": thr, "target": tgt_name})
    pd.DataFrame(detail).to_csv(OUT / "family_credit_spread_proxy.csv", index=False)
    return rows


# ---------------------------------------------------------------------------
# B) RATE_CURVE_SHAPE
# ---------------------------------------------------------------------------
def screen_rate_curve() -> list[dict]:
    """10Y−5Y (TNX−FVX) curve shape: steepener → risk-on SPY; flattener → TLT.

    Distinct from FX carry residual and from classic yield TSMOM.
    """
    tnx = load_close(DAILY / "TNX_10Y.csv")
    fvx = load_close(DAILY / "FVX_5Y.csv")
    tyx = load_close(DAILY / "TYX_30Y.csv")
    spy = load_close(DAILY / "SPY.csv")
    tlt = load_close(DAILY / "TLT.csv")
    slope_10_5 = (tnx - fvx).dropna()
    slope_30_10 = (tyx - tnx).dropna()
    rows = []
    detail = []
    configs = [
        ("TNX-FVX", slope_10_5),
        ("TYX-TNX", slope_30_10),
    ]
    for slope_name, slope in configs:
        for lvl_win in (60, 120):
            for d_win in (5, 10):
                z_lvl = zscore(slope, lvl_win)
                d_slope = slope.diff(d_win)
                z_d = zscore(d_slope, lvl_win)
                for tgt_name, tgt, mode in (
                    ("SPY", spy, "steep_long"),
                    ("TLT", tlt, "flat_long"),
                ):
                    df = pd.concat(
                        {
                            "z_lvl": z_lvl,
                            "z_d": z_d,
                            "ret1": tgt.pct_change().shift(-1),
                        },
                        axis=1,
                    ).dropna()
                    pos = pd.Series(0.0, index=df.index)
                    # Combined: level steep (z_lvl>0.5) OR steepening impulse (z_d>0.75)
                    steep = (df["z_lvl"] > 0.5) | (df["z_d"] > 0.75)
                    flat = (df["z_lvl"] < -0.5) | (df["z_d"] < -0.75)
                    if mode == "steep_long":
                        pos[steep] = 1.0
                        pos[flat] = -1.0
                    else:  # TLT prefers flattening / recession curve
                        pos[flat] = 1.0
                        pos[steep] = -1.0
                    pnl = pos * df["ret1"] * 1e4
                    row = summarize_row(
                        "RATE_CURVE_SHAPE",
                        f"{slope_name}→{tgt_name}",
                        f"lvl{lvl_win}/d{d_win}|hold=1d",
                        pnl,
                        "NEW_FAMILY; Treasury curve shape z + Δz → next-day; bruto trade-cond",
                    )
                    rows.append(row)
                    detail.append(
                        {
                            **row,
                            "slope": slope_name,
                            "lvl_win": lvl_win,
                            "d_win": d_win,
                            "target": tgt_name,
                        }
                    )
    pd.DataFrame(detail).to_csv(OUT / "family_rate_curve_shape.csv", index=False)
    return rows


# ---------------------------------------------------------------------------
# C) VIX_TERM_VOV  (vol-of-vol + term structure; ≠ XASSET_VOL_TIMING percentile)
# ---------------------------------------------------------------------------
def screen_vix_term_vov() -> list[dict]:
    """Front/back VIX term (VIX9D/VIX3M) + VoV (|ΔVIX| rolling std) → SPY timing.

    Backwardation / high VoV → short-term equity mean-reversion long (buy stress);
    deep contango + low VoV → mild long trend; else flat.
    Distinct from XASSET_VOL_TIMING (VIX percentile risk-on/off).
    """
    vix = load_close(DAILY / "VIX.csv")
    v9 = load_close(DAILY / "VIX9D.csv")
    v3 = load_close(DAILY / "VIX3M.csv")
    spy = load_close(DAILY / "SPY.csv")
    ndx = load_close(DAILY / "NDX.csv") if (DAILY / "NDX.csv").exists() else None
    term = (v9 / v3).dropna()
    dvix = vix.diff().abs()
    rows = []
    detail = []
    for vov_win in (10, 20):
        vov = dvix.rolling(vov_win, min_periods=5).mean()
        vov_z = zscore(vov, 252)
        for tgt_name, tgt in (("SPY", spy), ("NDX", ndx)):
            if tgt is None:
                continue
            for mode in ("stress_mr", "contango_trend", "combo"):
                df = pd.concat(
                    {
                        "term": term,
                        "vov_z": vov_z,
                        "ret1": tgt.pct_change().shift(-1),
                    },
                    axis=1,
                ).dropna()
                pos = pd.Series(0.0, index=df.index)
                if mode == "stress_mr":
                    # buy equity when term inverted (term>1.0) OR VoV spike
                    pos[(df["term"] > 1.0) | (df["vov_z"] > 1.0)] = 1.0
                elif mode == "contango_trend":
                    # long when deep contango + calm VoV
                    pos[(df["term"] < 0.92) & (df["vov_z"] < 0.0)] = 1.0
                    pos[(df["term"] > 1.05) & (df["vov_z"] > 0.5)] = -1.0
                else:  # combo
                    pos[(df["term"] > 1.0) | (df["vov_z"] > 1.25)] = 1.0
                    pos[(df["term"] < 0.90) & (df["vov_z"] < -0.25)] = 0.5
                pnl = pos * df["ret1"] * 1e4
                row = summarize_row(
                    "VIX_TERM_VOV",
                    f"VIX9D/VIX3M+VoV→{tgt_name}",
                    f"vov{vov_win}/{mode}|hold=1d",
                    pnl,
                    "NEW_FAMILY; VIX term structure + vol-of-vol regime; ≠ XASSET_VOL_TIMING; bruto trade-cond",
                )
                rows.append(row)
                detail.append({**row, "vov_win": vov_win, "mode": mode, "target": tgt_name})
    pd.DataFrame(detail).to_csv(OUT / "family_vix_term_vov.csv", index=False)
    return rows


# ---------------------------------------------------------------------------
# D) EM_DM_FLOW_ROTATION
# ---------------------------------------------------------------------------
def screen_em_dm_rotation() -> list[dict]:
    """EEM vs EFA relative strength with DXY filter — geo equity flow rotation.

    Long EEM / short EFA when rel-mom positive AND DXY weakening (risk/EM flow).
    ≠ classic single-asset TSMOM; ≠ FX-med; ≠ N77 FX XS rev.
    """
    eem = load_close(DAILY / "EEM.csv")
    efa = load_close(DAILY / "EFA.csv")
    dxy = load_close(DAILY / "DXY.csv")
    rows = []
    detail = []
    rel = (eem / efa).dropna()
    for lb in (20, 60, 120):
        for dxy_lb in (20, 60):
            rel_mom = rel.pct_change(lb)
            dxy_mom = dxy.pct_change(dxy_lb)
            # next-day relative return of long EEM short EFA
            eem_r = eem.pct_change().shift(-1)
            efa_r = efa.pct_change().shift(-1)
            df = pd.concat(
                {"rm": rel_mom, "dm": dxy_mom, "spread": eem_r - efa_r},
                axis=1,
            ).dropna()
            pos = pd.Series(0.0, index=df.index)
            # long EM-DM when rel_mom>0 and DXY falling
            pos[(df["rm"] > 0) & (df["dm"] < 0)] = 1.0
            pos[(df["rm"] < 0) & (df["dm"] > 0)] = -1.0
            pnl = pos * df["spread"] * 1e4
            row = summarize_row(
                "EM_DM_FLOW_ROTATION",
                "EEM/EFA+DXY",
                f"rel{lb}/dxy{dxy_lb}|hold=1d_LS",
                pnl,
                "NEW_FAMILY; EM vs DM equity flow with DXY filter; bruto trade-cond LS",
            )
            rows.append(row)
            detail.append({**row, "lb": lb, "dxy_lb": dxy_lb})
    pd.DataFrame(detail).to_csv(OUT / "family_em_dm_flow_rotation.csv", index=False)
    return rows


def main() -> None:
    all_rows: list[dict] = []
    all_rows += screen_credit_spread()
    all_rows += screen_rate_curve()
    all_rows += screen_vix_term_vov()
    all_rows += screen_em_dm_rotation()

    df = pd.DataFrame(all_rows)
    # best per family by day_t
    df["_t"] = pd.to_numeric(df["day_t"], errors="coerce")
    df = df.sort_values(["family", "_t"], ascending=[True, False])
    shortlist = []
    for fam, g in df.groupby("family", sort=True):
        best = g.iloc[0].drop(labels=["_t"]).to_dict()
        shortlist.append(best)

    df.drop(columns=["_t"]).to_csv(OUT / "lane_a_all_rows.csv", index=False)
    pd.DataFrame(shortlist).to_csv(OUT / "lane_a_shortlist.csv", index=False)

    survivors = [r for r in all_rows if r.get("promote_to_lane_b") == "yes"]
    # unique family survivors (best per family)
    surv_best = []
    for fam, g in pd.DataFrame(survivors).groupby("family") if survivors else []:
        g = g.copy()
        g["_t"] = pd.to_numeric(g["day_t"], errors="coerce")
        surv_best.append(g.sort_values("_t", ascending=False).iloc[0].drop(labels=["_t"]).to_dict())

    summary = {
        "cycle": "cycle_1240",
        "when": "2026-10-01 ~12:45 Europe/Amsterdam",
        "branch": "grok/strateeg-2",
        "n_configs": len(all_rows),
        "families": sorted(df["family"].unique().tolist()),
        "new_family_count": len(df["family"].unique()),
        "n_promote_configs": len(survivors),
        "n_promote_families": len(surv_best),
        "shortlist": shortlist,
        "survivors": surv_best,
        "rules": "day_t>=2 bruto trade-cond; n>=80; years>=5; mean>0; cut<=2024; no FTMO cost yet",
    }
    (OUT / "prescreen_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = [
        "# Strateeg-2 Lane-A pre-screen — cycle_1240 (C-028)",
        "",
        "**When:** 2026-10-01 ~12:45 Europe/Amsterdam (CEST).",
        "**Branch:** `grok/strateeg-2`. **Trials:** 0. Reserve 2025+: untouched.",
        "",
        "## Families (all NEW_FAMILY vs last-30d dead + CTO C-028 set + N75–N77)",
        "",
        "| Family | Best symbols | lookback/hold | years | mean_bp | day_t | n | promote |",
        "|--------|--------------|---------------|------:|--------:|------:|--:|:-------:|",
    ]
    for r in shortlist:
        lines.append(
            f"| {r['family']} | {r['symbols']} | {r['lookback_hold']} | {r['train_years']} | "
            f"{r['mean_bp']} | {r['day_t']} | {r['n_days']} | {r['promote_to_lane_b']} |"
        )
    lines += [
        "",
        f"**Configs tested:** {len(all_rows)}. **Promote configs:** {len(survivors)}. "
        f"**Promote families:** {len(surv_best)}.",
        "",
        "## Promote rule",
        "day_t ≥ 2 bruto (trade-conditional), n_days ≥ 80, train_years ≥ 5, mean_bp > 0. "
        "No FTMO cost gate here (Lane A). Survivors → VOORSTEL for Strateeg Lane-B.",
        "",
        "## Dead-set / clone guard",
        "Barred: ORB, classic TSMOM, L60 FX-med, ENERGY, IDX_SHORT, FX_EUR_SHORT, "
        "USDJPY_MED, EURJPY_MED, TSMOM_DIV. Not re-run: CTO COMMODITY_SEASONALITY / "
        "OVERNIGHT_GAP_FADE / XASSET_VOL_TIMING / FX_CARRY_TREND_RESIDUAL. Not clone: "
        "N75 metal-pair MR, N76 UKOIL inventory, N77 FX XS rank-rev.",
        "",
    ]
    if surv_best:
        lines.append("## Survivors")
        for r in surv_best:
            lines.append(
                f"- **{r['family']}** `{r['symbols']}` {r['lookback_hold']}: "
                f"day_t={r['day_t']}, mean={r['mean_bp']} bp, n={r['n_days']}, yrs={r['train_years']}"
            )
    else:
        lines.append("## Survivors")
        lines.append("None — no config cleared day_t≥2 with n≥80.")
    (OUT / "prescreen.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2))
    print("---SHORTLIST---")
    print(pd.DataFrame(shortlist)[
        ["family", "symbols", "lookback_hold", "train_years", "mean_bp", "day_t", "n_days", "promote_to_lane_b"]
    ].to_string(index=False))


if __name__ == "__main__":
    main()
