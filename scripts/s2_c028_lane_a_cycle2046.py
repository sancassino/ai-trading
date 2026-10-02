#!/usr/bin/env python3
"""Strateeg-2 Lane-A novelty screens — C-028 / cycle ~20:46 Europe/Amsterdam 2026-10-02.

Recovers failed ~19:49 CEST attempt (no partial artefacts on branch; tip was STALE b765613).

≥4 NEW_FAMILY mechanisms vs last-30d dead set + prior Lane-A:
  BARRED/DEAD: ORB / classic TSMOM / L60 FX-med / ENERGY / IDX_SHORT / FX_*_MED/SHORT /
               VIX_TERM_VOV (N78/C-029) / CORN-seasonality-as-FTMO / UKOIL-OVN / N87 gap /
               ORB-meta / prior S2 CREDIT_SPREAD / RATE_CURVE / EM_DM_FLOW /
               CTO COMMODITY_SEASONALITY / OVERNIGHT_GAP_FADE / XASSET_VOL_TIMING /
               FX_CARRY_TREND_RESIDUAL / N75 metal-MR / N76 UKOIL inv / N77 FX XS /
               N92 US100 NY 2h mom (Faraday — do not clone).

Families this cycle (all NEW_FAMILY):
  A) SECTOR_DISP_ROTATION  — 9-sector cross-sectional dispersion → SPY/NDX timing + LS
  B) BREAKEVEN_REALRATE    — TIP/IEF breakeven proxy → GLD / SPY (real-rate channel)
  C) COPPER_GOLD_MACRO     — COPPER_F/GOLD_F growth-risk ratio → SPY/NDX (NOT copper CFD)
  D) PC_RATIO_STRESS       — CBOE PUT index impulse → SPY/NDX stress / calm regimes

POST-N78: after day_t≥2 bruto, early FTMO swap/RT stress on mapped symbols
(US500/US100/XAU). Prefer RT small vs bruto; drop/FLAG cost-hostile.

Rules: Yahoo/proxy daily; cut ≤2024-12-31; reserve 2025+ untouched; day_t bruto;
promote if day_t≥2 & n≥80 & years≥5 & mean_bp>0 AND cost stress not HOSTILE.
Diagnostic ≠ trial. No PREREG here (Lane-B = Strateeg).
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
OUT = ROOT / "results" / "strateeg2_prescreen" / "cycle_2046"
CAL_END = pd.Timestamp("2024-12-31")
CAL_START = pd.Timestamp("2005-01-01")
MIN_DAYS = 80
PROMOTE_T = 2.0
OUT.mkdir(parents=True, exist_ok=True)

# Honest FTMO RT (rondreis_bp from COSTS_FTMO_alle) + overnight swap %/yr
FTMO_MAP = {
    "SPY": {
        "ftmo": "US500cash",
        "rt_bp": 0.78,
        "swap_long_pct_yr": -4.95,
        "swap_short_pct_yr": -2.95,
    },
    "NDX": {
        "ftmo": "US100cash",
        "rt_bp": 0.66,
        "swap_long_pct_yr": -7.12,
        "swap_short_pct_yr": -0.75,
    },
    "GLD": {
        "ftmo": "XAUUSD",
        "rt_bp": 0.83,
        "swap_long_pct_yr": -7.93,
        "swap_short_pct_yr": -0.37,
    },
}


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
    for cand in ("adjclose", "close"):
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


def swap_bp_night(pct_yr: float) -> float:
    """Approximate overnight swap cost in bp (positive = you pay)."""
    return abs(pct_yr) / 365.0 * 100.0 if pct_yr < 0 else -abs(pct_yr) / 365.0 * 100.0


def cost_stress(mean_bp: float, pos_sign_mode: str, target: str) -> dict:
    """Early FTMO RT+swap stress. pos_sign_mode: long_bias|short_bias|both|flat_ish."""
    info = FTMO_MAP.get(target)
    if info is None:
        return {
            "ftmo": "UNMAPPED",
            "rt_bp": None,
            "swap_bp_n": None,
            "net_vs_3rt": None,
            "cost_flag": "UNMAPPED",
            "notes": "no FTMO map",
        }
    rt = info["rt_bp"]
    # Prefer cheaper overnight side when bias known; else assume long (worse for indices)
    if pos_sign_mode == "short_bias":
        sw = swap_bp_night(info["swap_short_pct_yr"])
        side = "short"
    elif pos_sign_mode == "long_bias":
        sw = swap_bp_night(info["swap_long_pct_yr"])
        side = "long"
    else:
        # both / unknown: stress with WORSE (more expensive) overnight side
        sw_l = swap_bp_night(info["swap_long_pct_yr"])
        sw_s = swap_bp_night(info["swap_short_pct_yr"])
        sw = max(sw_l, sw_s)  # higher pay = worse
        side = "worse_side"
    gate_3rt = 3.0 * rt
    # One RT per trade-day + one overnight (1d hold)
    drag = rt + sw
    net = mean_bp - drag if np.isfinite(mean_bp) else float("nan")
    # HOSTILE if bruto mean cannot clear 3×RT (N78 lesson) OR net < 1 bp
    if not np.isfinite(mean_bp) or mean_bp <= 0:
        flag = "FAIL_BRUTO"
    elif mean_bp < gate_3rt:
        flag = "COST_HOSTILE"
    elif net < 1.0:
        flag = "COST_HOSTILE"
    elif mean_bp < 2.0 * gate_3rt:
        flag = "COST_TIGHT"  # survives but thin vs RT
    else:
        flag = "COST_OK"
    return {
        "ftmo": info["ftmo"],
        "rt_bp": rt,
        "swap_bp_n": round(sw, 3),
        "swap_side": side,
        "drag_bp": round(drag, 3),
        "gate_3rt": round(gate_3rt, 3),
        "net_after_drag": round(net, 3) if np.isfinite(net) else None,
        "cost_flag": flag,
    }


def summarize_row(
    family, symbols, lookback_hold, pnl: pd.Series, notes: str,
    target_for_cost: str | None = None, pos_mode: str = "both",
) -> dict:
    traded = pnl[np.isfinite(pnl) & (pnl != 0)]
    all_days = pnl[np.isfinite(pnl)]
    m, t, n = day_t(traded.values)
    m_all, t_all, n_all = day_t(all_days.values)
    yrs = train_years(pnl.dropna().index)
    short = yrs < 5.0
    bruto_ok = (
        np.isfinite(t) and t >= PROMOTE_T and n >= MIN_DAYS and yrs >= 5.0 and m > 0
    )
    cs = (
        cost_stress(m, pos_mode, target_for_cost)
        if target_for_cost and bruto_ok
        else {
            "ftmo": FTMO_MAP.get(target_for_cost or "", {}).get("ftmo", ""),
            "rt_bp": FTMO_MAP.get(target_for_cost or "", {}).get("rt_bp"),
            "swap_bp_n": None,
            "swap_side": "",
            "drag_bp": None,
            "gate_3rt": None,
            "net_after_drag": None,
            "cost_flag": "N/A_NO_BRUTO" if not bruto_ok else "N/A",
        }
    )
    promote = bruto_ok and cs.get("cost_flag") in ("COST_OK", "COST_TIGHT")
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
        "ftmo_symbol": cs.get("ftmo") or "",
        "rt_bp": cs.get("rt_bp") if cs.get("rt_bp") is not None else "",
        "swap_bp_n": cs.get("swap_bp_n") if cs.get("swap_bp_n") is not None else "",
        "drag_bp": cs.get("drag_bp") if cs.get("drag_bp") is not None else "",
        "gate_3rt": cs.get("gate_3rt") if cs.get("gate_3rt") is not None else "",
        "net_after_drag": cs.get("net_after_drag") if cs.get("net_after_drag") is not None else "",
        "cost_flag": cs.get("cost_flag") or "",
        "promote_to_lane_b": "yes" if promote else "no",
        "notes": notes
        + f"; short_hist={'yes' if short else 'no'}; ≤2024"
        + (f"; cost={cs.get('cost_flag')}" if bruto_ok else ""),
    }


# ---------------------------------------------------------------------------
# A) SECTOR_DISP_ROTATION
# ---------------------------------------------------------------------------
def screen_sector_disp() -> list[dict]:
    """Cross-sectional sector dispersion → equity timing + top/bottom LS.

    High dispersion = macro disagreement → often followed by index moves;
    LS of strongest vs weakest sectors is a classic rotation sleeve (≠ single TSMOM).
    Targets map to cheap FTMO index CFDs (US500/US100).
    """
    sectors = ["XLB", "XLE", "XLF", "XLI", "XLK", "XLP", "XLU", "XLV", "XLY"]
    closes = {s: load_close(DAILY / f"{s}.csv") for s in sectors}
    px = pd.DataFrame(closes).dropna(how="any")
    spy = load_close(DAILY / "SPY.csv")
    ndx = load_close(DAILY / "NDX.csv")
    rows, detail = [], []
    for lb in (5, 10, 20):
        rets = px.pct_change(lb)
        # cross-sectional z of each sector's lb return
        cs_mean = rets.mean(axis=1)
        cs_std = rets.std(axis=1).replace(0, np.nan)
        disp = cs_std  # dispersion level
        disp_z = zscore(disp, 252)
        # rank: top 3 vs bottom 3 equal-weight next-day LS
        ranks = rets.rank(axis=1, ascending=False)
        long_m = (ranks <= 3).astype(float)
        short_m = (ranks >= (len(sectors) - 2)).astype(float)
        next_r = px.pct_change().shift(-1)
        ls = (long_m * next_r).sum(axis=1) / 3.0 - (short_m * next_r).sum(axis=1) / 3.0
        for mode in ("disp_long_spy", "disp_fade_spy", "sector_ls"):
            for tgt_name, tgt in (("SPY", spy), ("NDX", ndx)):
                if mode == "sector_ls" and tgt_name != "SPY":
                    # LS is sector-internal; report once
                    continue
                if mode == "sector_ls":
                    pnl = ls * 1e4
                    symbols = f"XL*→LS_top3bot3"
                    pos_mode = "both"
                    cost_tgt = "SPY"  # informational; LS not a single FTMO symbol
                else:
                    df = pd.concat(
                        {"dz": disp_z, "ret1": tgt.pct_change().shift(-1)}, axis=1
                    ).dropna()
                    pos = pd.Series(0.0, index=df.index)
                    if mode == "disp_long_spy":
                        pos[df["dz"] > 0.75] = 1.0
                        pos[df["dz"] < -0.75] = -1.0
                        pos_mode = "both"
                    else:  # fade: high disp → short (risk-off), low → long
                        pos[df["dz"] > 1.0] = -1.0
                        pos[df["dz"] < -0.5] = 1.0
                        pos_mode = "both"
                    pnl = pos * df["ret1"] * 1e4
                    symbols = f"XL*disp→{tgt_name}"
                    cost_tgt = tgt_name
                row = summarize_row(
                    "SECTOR_DISP_ROTATION",
                    symbols,
                    f"lb{lb}/{mode}|hold=1d",
                    pnl,
                    "NEW_FAMILY; sector cross-section dispersion / rotation; ≠ classic TSMOM; bruto trade-cond",
                    target_for_cost=cost_tgt if mode != "sector_ls" else tgt_name,
                    pos_mode=pos_mode,
                )
                if mode == "sector_ls":
                    row["cost_flag"] = "LS_NO_SINGLE_FTMO"
                    row["promote_to_lane_b"] = "no"  # needs multi-symbol book; Lane-A note only
                    row["notes"] += "; LS research-only (no single FTMO map)"
                rows.append(row)
                detail.append({**row, "lb": lb, "mode": mode, "target": tgt_name})
    pd.DataFrame(detail).to_csv(OUT / "family_sector_disp_rotation.csv", index=False)
    return rows


# ---------------------------------------------------------------------------
# B) BREAKEVEN_REALRATE
# ---------------------------------------------------------------------------
def screen_breakeven() -> list[dict]:
    """TIP/IEF ≈ breakeven / real-rate channel → GLD and SPY.

    Falling real rates (TIP rich vs IEF) historically support gold & duration-sensitive risk.
    Distinct from RATE_CURVE_SHAPE (nominal TNX−FVX) and from VIX_TERM.
    """
    tip = load_close(DAILY / "TIP.csv")
    ief = load_close(DAILY / "IEF.csv")
    gld = load_close(DAILY / "GLD.csv")
    spy = load_close(DAILY / "SPY.csv")
    ratio = (tip / ief).dropna()
    rows, detail = [], []
    for z_win in (40, 60, 120):
        for thr in (0.5, 1.0, 1.5):
            z = zscore(ratio, z_win)
            d5 = ratio.pct_change(5)
            for tgt_name, tgt, mode in (
                ("GLD", gld, "tip_rich_long_gold"),
                ("SPY", spy, "tip_rich_long_spy"),
                ("GLD", gld, "realrate_impulse"),
            ):
                df = pd.concat(
                    {"z": z, "d5": d5, "ret1": tgt.pct_change().shift(-1)}, axis=1
                ).dropna()
                pos = pd.Series(0.0, index=df.index)
                if mode == "realrate_impulse":
                    # improving breakeven (ratio up) → long gold; falling → short
                    pos[df["d5"] > 0] = 1.0
                    pos[df["d5"] < 0] = -1.0
                else:
                    # TIP rich (z>thr) → long gold/spy; TIP cheap → short
                    pos[df["z"] > thr] = 1.0
                    pos[df["z"] < -thr] = -1.0
                # Gold: prefer noting short swap is cheaper — stress with both
                pos_mode = "both"
                pnl = pos * df["ret1"] * 1e4
                row = summarize_row(
                    "BREAKEVEN_REALRATE",
                    f"TIP/IEF→{tgt_name}",
                    f"z{z_win}/thr{thr}/{mode}|hold=1d",
                    pnl,
                    "NEW_FAMILY; TIP/IEF breakeven/real-rate → GLD/SPY; ≠ RATE_CURVE_SHAPE; bruto trade-cond",
                    target_for_cost=tgt_name,
                    pos_mode=pos_mode,
                )
                rows.append(row)
                detail.append({**row, "z_win": z_win, "thr": thr, "mode": mode, "target": tgt_name})
    pd.DataFrame(detail).to_csv(OUT / "family_breakeven_realrate.csv", index=False)
    return rows


# ---------------------------------------------------------------------------
# C) COPPER_GOLD_MACRO
# ---------------------------------------------------------------------------
def screen_copper_gold() -> list[dict]:
    """Copper/Gold ratio as growth-risk macro → equity next day (NOT copper CFD).

    Rising Cu/Au = risk-on / growth; falling = risk-off. Trade SPY/NDX (cheap RT),
    avoid agri/metal CFD cost trap (N78/CORN lesson).
    """
    cu = load_close(DAILY / "COPPER_F.csv")
    au = load_close(DAILY / "GOLD_F.csv")
    spy = load_close(DAILY / "SPY.csv")
    ndx = load_close(DAILY / "NDX.csv")
    ratio = (cu / au).dropna()
    rows, detail = [], []
    for z_win in (40, 60, 120):
        for thr in (0.5, 1.0):
            z = zscore(ratio, z_win)
            mom = ratio.pct_change(20)
            for tgt_name, tgt in (("SPY", spy), ("NDX", ndx)):
                for mode in ("z_level", "mom_confirm"):
                    df = pd.concat(
                        {
                            "z": z,
                            "mom": mom,
                            "ret1": tgt.pct_change().shift(-1),
                        },
                        axis=1,
                    ).dropna()
                    pos = pd.Series(0.0, index=df.index)
                    if mode == "z_level":
                        pos[df["z"] > thr] = 1.0
                        pos[df["z"] < -thr] = -1.0
                    else:
                        pos[(df["z"] > 0) & (df["mom"] > 0)] = 1.0
                        pos[(df["z"] < 0) & (df["mom"] < 0)] = -1.0
                    pnl = pos * df["ret1"] * 1e4
                    row = summarize_row(
                        "COPPER_GOLD_MACRO",
                        f"COPPER_F/GOLD_F→{tgt_name}",
                        f"z{z_win}/thr{thr}/{mode}|hold=1d",
                        pnl,
                        "NEW_FAMILY; Cu/Au macro ratio → equity (not copper CFD); bruto trade-cond",
                        target_for_cost=tgt_name,
                        pos_mode="both",
                    )
                    rows.append(row)
                    detail.append(
                        {**row, "z_win": z_win, "thr": thr, "mode": mode, "target": tgt_name}
                    )
    pd.DataFrame(detail).to_csv(OUT / "family_copper_gold_macro.csv", index=False)
    return rows


# ---------------------------------------------------------------------------
# D) PC_RATIO_STRESS  (CBOE PUT index)
# ---------------------------------------------------------------------------
def screen_pc_ratio() -> list[dict]:
    """CBOE PUT index level/impulse as fear proxy → SPY/NDX timing.

    Distinct from VIX_TERM_VOV (term+VoV) and XASSET_VOL_TIMING (VIX percentile).
    Stress spikes in PUT → buy-the-dip; calm elevated → mild long.
    """
    put = load_close(DAILY / "CBOE_PUT.csv")
    spy = load_close(DAILY / "SPY.csv")
    ndx = load_close(DAILY / "NDX.csv")
    rows, detail = [], []
    for z_win in (20, 60, 120):
        z = zscore(put, z_win)
        d1 = put.pct_change(1)
        d5 = put.pct_change(5)
        for tgt_name, tgt in (("SPY", spy), ("NDX", ndx)):
            for mode in ("stress_buy", "put_trend", "combo"):
                df = pd.concat(
                    {
                        "z": z,
                        "d1": d1,
                        "d5": d5,
                        "ret1": tgt.pct_change().shift(-1),
                    },
                    axis=1,
                ).dropna()
                pos = pd.Series(0.0, index=df.index)
                if mode == "stress_buy":
                    # elevated PUT or sharp rise → long equity next day
                    pos[(df["z"] > 1.0) | (df["d1"] > 0.05)] = 1.0
                    pos[(df["z"] < -1.0) & (df["d5"] < 0)] = -0.5
                elif mode == "put_trend":
                    pos[df["d5"] > 0] = 1.0  # rising fear → dip-buy
                    pos[df["d5"] < 0] = -0.5
                else:
                    pos[(df["z"] > 0.75) | (df["d5"] > 0.03)] = 1.0
                    pos[(df["z"] < -0.75) & (df["d5"] < -0.02)] = -1.0
                pnl = pos * df["ret1"] * 1e4
                row = summarize_row(
                    "PC_RATIO_STRESS",
                    f"CBOE_PUT→{tgt_name}",
                    f"z{z_win}/{mode}|hold=1d",
                    pnl,
                    "NEW_FAMILY; CBOE PUT fear impulse → equity; ≠ VIX_TERM_VOV / XASSET_VOL; bruto trade-cond",
                    target_for_cost=tgt_name,
                    pos_mode="long_bias",  # stress-buy is long-biased
                )
                rows.append(row)
                detail.append({**row, "z_win": z_win, "mode": mode, "target": tgt_name})
    pd.DataFrame(detail).to_csv(OUT / "family_pc_ratio_stress.csv", index=False)
    return rows


def export_survivor_daily(family: str, symbols: str, lookback_hold: str, pnl: pd.Series) -> Path:
    out = OUT / f"{family}_{symbols.replace('/', '_').replace('*', 'x')}_{lookback_hold.replace('|', '_').replace('/', '-')}_daily.csv"
    # sanitize filename
    safe = (
        family
        + "_"
        + "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in f"{symbols}_{lookback_hold}")
    )[:120]
    out = OUT / f"{safe}_daily.csv"
    df = pd.DataFrame({"date": pnl.index, "pnl_bp": pnl.values})
    df.to_csv(out, index=False)
    return out


def main() -> None:
    # Re-run screens capturing best pnl series for survivors
    all_rows: list[dict] = []
    all_rows += screen_sector_disp()
    all_rows += screen_breakeven()
    all_rows += screen_copper_gold()
    all_rows += screen_pc_ratio()

    df = pd.DataFrame(all_rows)
    df["_t"] = pd.to_numeric(df["day_t"], errors="coerce")
    df = df.sort_values(["family", "_t"], ascending=[True, False])
    shortlist = []
    for fam, g in df.groupby("family", sort=True):
        best = g.iloc[0].drop(labels=["_t"]).to_dict()
        shortlist.append(best)

    df.drop(columns=["_t"]).to_csv(OUT / "lane_a_all_rows.csv", index=False)
    pd.DataFrame(shortlist).to_csv(OUT / "lane_a_shortlist.csv", index=False)

    survivors = [r for r in all_rows if r.get("promote_to_lane_b") == "yes"]
    surv_best = []
    if survivors:
        for fam, g in pd.DataFrame(survivors).groupby("family"):
            g = g.copy()
            g["_t"] = pd.to_numeric(g["day_t"], errors="coerce")
            surv_best.append(
                g.sort_values("_t", ascending=False).iloc[0].drop(labels=["_t"]).to_dict()
            )

    # Cost-hostile bruto survivors (day_t ok but cost killed)
    bruto_ok = df[
        (pd.to_numeric(df["day_t"], errors="coerce") >= PROMOTE_T)
        & (df["n_days"] >= MIN_DAYS)
        & (pd.to_numeric(df["train_years"], errors="coerce") >= 5)
        & (pd.to_numeric(df["mean_bp"], errors="coerce") > 0)
    ]
    hostile = bruto_ok[bruto_ok["cost_flag"] == "COST_HOSTILE"]

    summary = {
        "cycle": "cycle_2046",
        "when": "2026-10-02 ~20:46 Europe/Amsterdam",
        "branch": "grok/strateeg-2",
        "recovers": "failed ~19:49 CEST run (no partial on branch; tip STALE b765613)",
        "n_configs": len(all_rows),
        "families": sorted(df["family"].unique().tolist()),
        "new_family_count": int(df["family"].nunique()),
        "n_promote_configs": len(survivors),
        "n_promote_families": len(surv_best),
        "n_cost_hostile_bruto_ok": int(len(hostile)),
        "shortlist": shortlist,
        "survivors": surv_best,
        "rules": (
            "day_t>=2 bruto trade-cond; n>=80; years>=5; mean_bp>0; cut<=2024; "
            "POST-N78: mean_bp>=3*RT and net_after_drag>=1 else COST_HOSTILE/no promote"
        ),
    }
    (OUT / "prescreen_summary.json").write_text(
        json.dumps(summary, indent=2, default=str), encoding="utf-8"
    )

    lines = [
        "# Strateeg-2 Lane-A pre-screen — cycle_2046 (C-028 + POST-N78 cost stress)",
        "",
        "**When:** 2026-10-02 ~20:46 Europe/Amsterdam (CEST).",
        "**Branch:** `grok/strateeg-2`. **Trials:** 0. Reserve 2025+: untouched.",
        "**Recovers:** failed ~19:49 CEST attempt (no partial artefacts; prior tip STALE).",
        "",
        "## Families (all NEW_FAMILY vs last-30d dead + prior Lane-A + Faraday N90–N92)",
        "",
        "| Family | Best symbols | lookback/hold | years | mean_bp | day_t | n | cost | promote |",
        "|--------|--------------|---------------|------:|--------:|------:|--:|------|:-------:|",
    ]
    for r in shortlist:
        lines.append(
            f"| {r['family']} | {r['symbols']} | {r['lookback_hold']} | {r['train_years']} | "
            f"{r['mean_bp']} | {r['day_t']} | {r['n_days']} | {r.get('cost_flag','')} | {r['promote_to_lane_b']} |"
        )
    lines += [
        "",
        f"**Configs tested:** {len(all_rows)}. **Promote configs:** {len(survivors)}. "
        f"**Promote families:** {len(surv_best)}. **Bruto-ok but COST_HOSTILE:** {len(hostile)}.",
        "",
        "## Promote rule (POST-N78)",
        "day_t ≥ 2 bruto (trade-conditional), n_days ≥ 80, train_years ≥ 5, mean_bp > 0, "
        "**and** early FTMO stress: mean_bp ≥ 3×RT and net_after_drag (RT+swap_night) ≥ 1 bp. "
        "Agri/index CFD cost traps flagged. Survivors → VOORSTEL (no PREREG by S2).",
        "",
        "## Dead-set / clone guard",
        "Barred: ORB, classic TSMOM, L60 FX-med, ENERGY, IDX_SHORT, FX_EUR_SHORT, "
        "USDJPY_MED, EURJPY_MED, TSMOM_DIV, **VIX_TERM_VOV**, CORN-as-FTMO, UKOIL-OVN, "
        "ORB-meta, N87. Not re-run: CTO COMMODITY_SEASONALITY / OVERNIGHT_GAP_FADE / "
        "XASSET_VOL_TIMING / FX_CARRY_TREND_RESIDUAL; prior S2 CREDIT/RATE_CURVE/EM_DM; "
        "N75–N77; N92 NY 2h mom.",
        "",
    ]
    if surv_best:
        lines.append("## Survivors (cost-stressed)")
        for r in surv_best:
            lines.append(
                f"- **{r['family']}** `{r['symbols']}` {r['lookback_hold']}: "
                f"day_t={r['day_t']}, mean={r['mean_bp']} bp, n={r['n_days']}, "
                f"yrs={r['train_years']}, FTMO={r.get('ftmo_symbol')}, "
                f"RT={r.get('rt_bp')}, drag={r.get('drag_bp')}, net={r.get('net_after_drag')}, "
                f"flag={r.get('cost_flag')}"
            )
    else:
        lines.append("## Survivors")
        lines.append("None — no config cleared day_t≥2 + POST-N78 cost stress.")
    if len(hostile):
        lines += ["", "## Bruto OK but COST_HOSTILE (dropped)"]
        for _, r in hostile.sort_values("day_t", ascending=False).head(10).iterrows():
            lines.append(
                f"- {r['family']} `{r['symbols']}` {r['lookback_hold']}: "
                f"day_t={r['day_t']} mean={r['mean_bp']} < gate_3rt={r.get('gate_3rt')} "
                f"FTMO={r.get('ftmo_symbol')} RT={r.get('rt_bp')}"
            )
    (OUT / "prescreen.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    (OUT / "survivor_export.json").write_text(
        json.dumps({"survivors": surv_best, "hostile_count": int(len(hostile))}, indent=2, default=str),
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2, default=str))
    print("---SHORTLIST---")
    cols = [
        "family", "symbols", "lookback_hold", "train_years", "mean_bp", "day_t",
        "n_days", "ftmo_symbol", "rt_bp", "drag_bp", "cost_flag", "promote_to_lane_b",
    ]
    print(pd.DataFrame(shortlist)[cols].to_string(index=False))
    if surv_best:
        print("---SURVIVORS---")
        print(pd.DataFrame(surv_best)[cols].to_string(index=False))


if __name__ == "__main__":
    main()
