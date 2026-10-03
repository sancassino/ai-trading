#!/usr/bin/env python3
"""Strateeg-2 Lane-A novelty screens — C-028 / cycle_0046 ~00:46 Europe/Amsterdam 2026-10-04.

≥4 NEW_FAMILY mechanisms vs last-30d dead set (incl. LQD → N166 FAIL_CLONE,
EWY → N167 FAIL, XLK → N161 FAIL_T, XLE → N143 FAIL_CLONE, XLY fail day_t,
YIELD_CURVE/DEFENSIVE → N124/N125, GAS/SILVER → N112/N113, EMB/CRACK,
EQW/DXY/MTUM/GLD/XLF/QUAL → N130–N135, BRENT_WTI/USDMXN → N136/N137,
GER40_UK100…EUR_CAD → N138–N153, N154–N175 session fades / XS / NY-impulse /
London-haven / Europe inventory / London-fix / coffee/cocoa / USOIL swing /
USDCAD continuation, N75–N175, CEO T5–T16, FX-LO carries).
Formal OPEN empty — no OPEN ids to avoid.
POST-N78/N93 cost stress. Multi-day holds use NON-OVERLAPPING trades + swap×hold nights.
Rules: Yahoo/proxy daily; cut ≤2024-12-31; reserve 2025+ untouched.
No PREREG (Lane-B = Strateeg; HOLD per NEXT_STEPS v113 until CTO adds COSTS symbol).
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
OUT = ROOT / "results" / "strateeg2_prescreen" / "cycle_0046"
CAL_END = pd.Timestamp("2024-12-31")
CAL_START = pd.Timestamp("2005-01-01")
MIN_DAYS = 80
PROMOTE_T = 2.0
OUT.mkdir(parents=True, exist_ok=True)

FTMO_MAP = {
    "SPY": {"ftmo": "US500cash", "rt_bp": 0.78, "swap_long_pct_yr": -4.95, "swap_short_pct_yr": -2.95},
    "NDX": {"ftmo": "US100cash", "rt_bp": 0.66, "swap_long_pct_yr": -7.12, "swap_short_pct_yr": -0.75},
    "EURUSD": {"ftmo": "EURUSD", "rt_bp": 0.63, "swap_long_pct_yr": -4.12, "swap_short_pct_yr": 0.51},
    "GBPUSD": {"ftmo": "GBPUSD", "rt_bp": 0.70, "swap_long_pct_yr": -1.68, "swap_short_pct_yr": -1.10},
}

DEAD_NOTE = (
    "ORB/TSMOM/L60/ENERGY_TSMOM/VIX_TERM/CORN/UKOIL-OVN/ORB-meta/SECTOR_DISP/"
    "EMB/CRACK/GAS/SILVER/HYG/TLT/TIP/CPER/VNQ/EEM/DBC/EFA/IWM/"
    "YIELD_CURVE_2S10S/DEFENSIVE_CYCLICAL/EWZ/DBA/BWX/PPLT/EQW/DXY/MTUM/GLD/XLF/QUAL/"
    "BRENT_WTI/USDMXN/XLE/VLUE/XLB/EURJPY_RISK/SOFTS_RATIO/XLK/XLV/COCOA/AUDUSD_COMMODITY_FX/"
    "LQD/EWY/XLY/"
    "N75-N175/CEO-T5-T16/FX-LO/GER40_UK100/JP225_HK50/XAU_UKOIL/US30_US500/"
    "BTC_ETH/AUD_XAU/GBP_UKOIL/USDJPY_US100/EUR_GER40/XAG_US30/"
    "EURJPY_USDCHF/GBP_NZD/EUR_CAD/US100_GER40/US30_UKOIL/XAU_GER40/XAU_US100/"
    "USOIL_NY/GER40_EU_CLOSE/XAG_NY/US500_CASH_CLOSE/AUD_NY/NZD_SAME/"
    "US2000_NY/EURCHF_LONDON/GBPCHF_USDCHF_AUDCHF_LONDON/"
    "US30_EU_INV/GBP_LONDON_FIX/FRA40_US_OPEN/BTC_EU_MORNING/"
    "USOIL_SWING/USDCAD_CONT/COFFEE/COCOA_OH; OPEN empty — no clone"
)


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
    return s[(s.index >= CAL_START) & (s.index <= CAL_END)].dropna()


def train_years(idx: pd.DatetimeIndex) -> float:
    if len(idx) < 2:
        return 0.0
    return float((idx.max() - idx.min()).days) / 365.25


def zscore(s: pd.Series, win: int) -> pd.Series:
    mu = s.rolling(win, min_periods=max(20, win // 3)).mean()
    sd = s.rolling(win, min_periods=max(20, win // 3)).std(ddof=0)
    return (s - mu) / sd.replace(0, np.nan)


def swap_bp_night(pct_yr: float) -> float:
    # Negative pct_yr = you PAY (cost). Positive = you RECEIVE (benefit → negative cost).
    return abs(pct_yr) / 365.0 * 100.0 if pct_yr < 0 else -abs(pct_yr) / 365.0 * 100.0


def cost_stress(mean_bp: float, pos_sign_mode: str, target: str, hold_days: int = 1) -> dict:
    info = FTMO_MAP.get(target)
    if info is None:
        return {"ftmo": "UNMAPPED", "rt_bp": None, "swap_bp_n": None, "cost_flag": "UNMAPPED"}
    rt = info["rt_bp"]
    if pos_sign_mode == "short_bias":
        sw1 = swap_bp_night(info["swap_short_pct_yr"]); side = "short"
    elif pos_sign_mode == "long_bias":
        sw1 = swap_bp_night(info["swap_long_pct_yr"]); side = "long"
    else:
        sw1 = max(swap_bp_night(info["swap_long_pct_yr"]), swap_bp_night(info["swap_short_pct_yr"]))
        side = "worse_side"
    hold_days = max(1, int(hold_days))
    sw = sw1 * hold_days
    gate_3rt = 3.0 * rt
    drag = rt + sw
    net = mean_bp - drag if np.isfinite(mean_bp) else float("nan")
    if not np.isfinite(mean_bp) or mean_bp <= 0:
        flag = "FAIL_BRUTO"
    elif mean_bp < gate_3rt or net < 1.0:
        flag = "COST_HOSTILE"
    elif mean_bp < 2.0 * gate_3rt:
        flag = "COST_TIGHT"
    else:
        flag = "COST_OK"
    return {
        "ftmo": info["ftmo"], "rt_bp": rt, "swap_bp_n": round(sw, 3), "swap_side": side,
        "drag_bp": round(drag, 3), "gate_3rt": round(gate_3rt, 3),
        "net_after_drag": round(net, 3) if np.isfinite(net) else None, "cost_flag": flag,
    }


def summarize_row(family, symbols, lookback_hold, pnl, notes, target_for_cost=None, pos_mode="both", hold_days=1):
    traded = pnl[np.isfinite(pnl) & (pnl != 0)]
    all_days = pnl[np.isfinite(pnl)]
    m, t, n = day_t(traded.values)
    m_all, t_all, n_all = day_t(all_days.values)
    yrs = train_years(pnl.dropna().index)
    short = yrs < 5.0
    bruto_ok = np.isfinite(t) and t >= PROMOTE_T and n >= MIN_DAYS and yrs >= 5.0 and m > 0
    if target_for_cost and bruto_ok:
        cs = cost_stress(m, pos_mode, target_for_cost, hold_days=hold_days)
    else:
        cs = {
            "ftmo": FTMO_MAP.get(target_for_cost or "", {}).get("ftmo", ""),
            "rt_bp": FTMO_MAP.get(target_for_cost or "", {}).get("rt_bp"),
            "swap_bp_n": None, "swap_side": "", "drag_bp": None, "gate_3rt": None,
            "net_after_drag": None, "cost_flag": "N/A_NO_BRUTO" if not bruto_ok else "N/A",
        }
    promote = bruto_ok and cs.get("cost_flag") == "COST_OK"
    return {
        "family": family, "symbols": symbols, "lookback_hold": lookback_hold,
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
        "notes": notes + f"; short_hist={'yes' if short else 'no'}; <=2024; nonoverlap_hold"
        + (f"; cost={cs.get('cost_flag')}" if bruto_ok else ""),
    }


def fwd_ret(tgt: pd.Series, hold: int) -> pd.Series:
    return tgt.pct_change(hold).shift(-hold)


def nonoverlap_pnl(pos: pd.Series, ret_h: pd.Series, hold: int) -> pd.Series:
    df = pd.concat({"pos": pos, "ret": ret_h}, axis=1).dropna()
    out = pd.Series(0.0, index=df.index)
    i, n = 0, len(df)
    while i < n:
        p = float(df["pos"].iloc[i])
        if p != 0.0 and np.isfinite(df["ret"].iloc[i]):
            out.iloc[i] = p * float(df["ret"].iloc[i]) * 1e4
            i += max(1, hold)
        else:
            i += 1
    return out


def _grid_z_signal(
    family: str,
    signal: pd.Series,
    signal_label: str,
    targets: dict,
    modes: tuple,
    note: str,
    family_csv: str,
    mode_pos: dict | None = None,
):
    """Shared z-level / fade / stress / mom grid over targets."""
    rows, detail, pnl_store = [], [], {}
    mode_pos = mode_pos or {}
    for z_win in (40, 60, 120):
        for thr in (0.5, 1.0, 1.5):
            z = zscore(signal, z_win)
            if (signal <= 0).any():
                d20 = signal.diff(20)
            else:
                d20 = signal.pct_change(20)
            for hold in (1, 3, 5):
                for tgt_name, tgt in targets.items():
                    for mode in modes:
                        ret = fwd_ret(tgt, hold)
                        df = pd.concat({"z": z, "d20": d20, "ret": ret}, axis=1).dropna()
                        pos = pd.Series(0.0, index=df.index)
                        if mode == "z_level":
                            pos[df["z"] > thr] = 1.0
                            pos[df["z"] < -thr] = -1.0
                        elif mode == "fade_extreme":
                            pos[df["z"] > thr] = -1.0
                            pos[df["z"] < -thr] = 1.0
                        elif mode == "stress_buy":
                            pos[df["z"] < -thr] = 1.0
                            pos[df["z"] > thr] = -1.0
                        elif mode == "stress_sell":
                            pos[df["z"] > thr] = -1.0
                            pos[df["z"] < -thr] = 1.0
                        elif mode == "mom_confirm":
                            pos[(df["z"] > thr) & (df["d20"] > 0)] = 1.0
                            pos[(df["z"] < -thr) & (df["d20"] < 0)] = -1.0
                        elif mode == "risk_on_high":
                            pos[df["z"] > thr] = 1.0
                            pos[df["z"] < -thr] = -1.0
                        elif mode == "risk_off_high":
                            pos[df["z"] > thr] = -1.0
                            pos[df["z"] < -thr] = 1.0
                        else:
                            continue
                        pnl = nonoverlap_pnl(pos, df["ret"], hold)
                        lbh = f"z{z_win}/thr{thr}/{mode}|hold={hold}d"
                        pmode = mode_pos.get(mode, "both")
                        if tgt_name == "NDX" and pmode == "both" and mode in (
                            "fade_extreme", "stress_sell", "risk_off_high", "stress_buy"
                        ):
                            if mode in ("fade_extreme", "stress_sell", "risk_off_high"):
                                pmode = "short_bias"
                        row = summarize_row(
                            family, f"{signal_label}->{tgt_name}", lbh, pnl, note,
                            target_for_cost=tgt_name, pos_mode=pmode, hold_days=hold,
                        )
                        rows.append(row)
                        detail.append({
                            **row, "z_win": z_win, "thr": thr, "mode": mode,
                            "hold": hold, "target": tgt_name,
                        })
                        pnl_store[f"{signal_label}->{tgt_name}|{lbh}"] = pnl
    pd.DataFrame(detail).to_csv(OUT / family_csv, index=False)
    return rows, pnl_store


def screen_xlp_staples():
    """XLP_STAPLES_STRESS: XLP.csv z → SPY/NDX.
    ≠ XLY discretionary / XLV health / DEFENSIVE XLU-XLI ratio.
    """
    xlp = load_close(DAILY / "XLP.csv")
    spy = load_close(DAILY / "SPY.csv")
    ndx = load_close(DAILY / "NDX.csv")
    return _grid_z_signal(
        "XLP_STAPLES_STRESS",
        xlp,
        "XLP",
        {"SPY": spy, "NDX": ndx},
        ("z_level", "fade_extreme", "stress_buy", "stress_sell", "mom_confirm"),
        f"NEW_FAMILY; XLP staples-sector z->equity; != XLY/XLV/DEFENSIVE XLU-XLI; {DEAD_NOTE}",
        "family_xlp_staples_stress.csv",
        mode_pos={"stress_buy": "long_bias", "stress_sell": "short_bias", "fade_extreme": "short_bias"},
    )


def screen_xli_industrials():
    """XLI_INDUSTRIALS_STRESS: XLI.csv alone z → SPY/NDX.
    ≠ DEFENSIVE XLU/XLI ratio; single-sector industrials.
    """
    xli = load_close(DAILY / "XLI.csv")
    spy = load_close(DAILY / "SPY.csv")
    ndx = load_close(DAILY / "NDX.csv")
    return _grid_z_signal(
        "XLI_INDUSTRIALS_STRESS",
        xli,
        "XLI",
        {"SPY": spy, "NDX": ndx},
        ("z_level", "fade_extreme", "stress_buy", "stress_sell", "mom_confirm"),
        f"NEW_FAMILY; XLI industrials-sector alone z->equity; != DEFENSIVE XLU/XLI ratio; {DEAD_NOTE}",
        "family_xli_industrials_stress.csv",
        mode_pos={"stress_buy": "long_bias", "stress_sell": "short_bias", "fade_extreme": "short_bias"},
    )


def screen_ewa_australia():
    """EWA_AUSTRALIA_STRESS: EWA.csv z → SPY/EURUSD.
    ≠ AUD NY fade / AUD-XAU / AUDUSD commodity FX.
    """
    ewa = load_close(DAILY / "EWA.csv")
    spy = load_close(DAILY / "SPY.csv")
    eurusd = load_close(DAILY / "EURUSD.csv")
    return _grid_z_signal(
        "EWA_AUSTRALIA_STRESS",
        ewa,
        "EWA",
        {"SPY": spy, "EURUSD": eurusd},
        ("z_level", "fade_extreme", "stress_buy", "stress_sell", "mom_confirm"),
        f"NEW_FAMILY; EWA Australia country z->equity/FX; != AUD_NY/AUD_XAU/AUDUSD_COMMODITY; {DEAD_NOTE}",
        "family_ewa_australia_stress.csv",
        mode_pos={"stress_buy": "long_bias", "stress_sell": "short_bias", "fade_extreme": "short_bias"},
    )


def screen_ewc_canada():
    """EWC_CANADA_STRESS: EWC.csv z → SPY/EURUSD.
    ≠ USDCAD continuation N173 / EUR-CAD XS N153.
    """
    ewc = load_close(DAILY / "EWC.csv")
    spy = load_close(DAILY / "SPY.csv")
    eurusd = load_close(DAILY / "EURUSD.csv")
    return _grid_z_signal(
        "EWC_CANADA_STRESS",
        ewc,
        "EWC",
        {"SPY": spy, "EURUSD": eurusd},
        ("z_level", "fade_extreme", "stress_buy", "stress_sell", "mom_confirm"),
        f"NEW_FAMILY; EWC Canada country z->equity/FX; != USDCAD_CONT N173 / EUR_CAD XS N153; {DEAD_NOTE}",
        "family_ewc_canada_stress.csv",
        mode_pos={"stress_buy": "long_bias", "stress_sell": "short_bias", "fade_extreme": "short_bias"},
    )


def screen_xlu_utilities():
    """XLU_UTILITIES_STRESS: XLU.csv alone z → SPY.
    ≠ DEFENSIVE XLU/XLI ratio.
    """
    xlu = load_close(DAILY / "XLU.csv")
    spy = load_close(DAILY / "SPY.csv")
    return _grid_z_signal(
        "XLU_UTILITIES_STRESS",
        xlu,
        "XLU",
        {"SPY": spy},
        ("z_level", "fade_extreme", "stress_buy", "stress_sell", "mom_confirm"),
        f"NEW_FAMILY; XLU utilities alone z->SPY; != DEFENSIVE XLU/XLI ratio; {DEAD_NOTE}",
        "family_xlu_utilities_stress.csv",
        mode_pos={"stress_buy": "long_bias", "stress_sell": "short_bias", "fade_extreme": "short_bias"},
    )


def export_survivor_daily(family, symbols, lookback_hold, pnl):
    safe = family + "_" + "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in f"{symbols}_{lookback_hold}")
    out = OUT / f"{safe[:120]}_daily.csv"
    pd.DataFrame({"date": pnl.index, "pnl_bp": pnl.values}).to_csv(out, index=False)
    return out


def write_voorstel(surv, shortlist, n_configs, n_surv_cfg):
    fam = surv["family"]
    path = OUT / f"VOORSTEL_S2_{fam}.md"
    n_fam = len({r["family"] for r in shortlist})
    lines = [
        f"# VOORSTEL S2 — {fam} (Lane-A survivor, C-028 + POST-N78/N93)",
        "",
        "**When:** 2026-10-04 ~00:46 Europe/Amsterdam (CEST)",
        "**Author:** Strateeg-2 (`grok/strateeg-2`) — Lane-A novelty researcher",
        "**Status:** Lane-A **promote** (day_t>=2 bruto **and** early FTMO RT/swap stress COST_OK). **Not** a PREREG. "
        "Strateeg Lane-B = **HOLD** per NEXT_STEPS v113 until CTO adds authorized COSTS_FTMO.csv symbol — pack for later.",
        "**Trials:** 0. Reserve 2025+: **untouched**.",
        "",
        "## Family tag",
        "",
        f"`NEW_FAMILY: {fam}`",
        "",
        "**Distinct from dead / barred:** ORB / TSMOM / L60 FX-med / ENERGY_TSMOM / VIX_TERM_VOV /",
        "CORN / UKOIL-OVN / ORB-meta / **SECTOR_DISP** / PC_RATIO / BREAKEVEN / COPPER_GOLD /",
        "CREDIT HYG-LQD / RATE_CURVE / EM_DM / **EMB_CREDIT_STRESS** / **CRACK_SPREAD_MACRO** /",
        "**GAS_EQUITY_MACRO** / **SILVER_GOLD_RATIO** / REIT_RATE / PGM / HYG / TLT / TIP / CPER /",
        "VNQ / EEM / DBC / EFA / IWM→US500 / **YIELD_CURVE_2S10S** / **DEFENSIVE_CYCLICAL** /",
        "EWZ / DBA / BWX / PPLT / EQW / DXY / MTUM / GLD / XLF / QUAL / BRENT_WTI / USDMXN /",
        "**XLE_ENERGY_EQUITY_STRESS** / VLUE / XLB / EURJPY_RISK / SOFTS_RATIO /",
        "**XLK_TECH_SECTOR_STRESS** / XLV / COCOA / AUDUSD_COMMODITY_FX /",
        "**LQD_IG_CREDIT_STRESS** / **EWY_KOREA_STRESS** / XLY_DISCRETIONARY /",
        "N75–N175 / CEO T5–T16 / FX LO carry / AUD–XAU / GBP–UKOIL / BTC–ETH /",
        "US2000 NY-impulse / EURCHF London-haven / US500 cash-close / AUD NY-fade /",
        "USDCAD continuation / EUR-CAD XS / coffee/cocoa / USOIL swing / London-fix /",
        "Europe inventory / Formal OPEN empty (not cloned).",
        "",
        "## Lane-A screen (bruto <=2024-12-31, non-overlapping holds) + POST-N78/N93",
        "",
        "| Target | FTMO | Config | mean_bp | day_t | n | years | RT | drag | net | cost |",
        "|--------|------|--------|--------:|------:|--:|------:|---:|-----:|----:|------|",
        (
            f"| {surv['symbols']} | {surv.get('ftmo_symbol')} | {surv['lookback_hold']} | "
            f"**{surv['mean_bp']}** | **{surv['day_t']}** | {surv['n_days']} | {surv['train_years']} | "
            f"{surv.get('rt_bp')} | {surv.get('drag_bp')} | **{surv.get('net_after_drag')}** | "
            f"**{surv.get('cost_flag')}** |"
        ),
        "",
        f"**Notes:** {surv.get('notes','')}",
        "",
        "Drag = RT + (swap_night × hold_days) on stressed overnight side (POST-N78 honesty).",
        "Multi-day holds use **non-overlapping** trade sampling (no inflated overlapping t).",
        "",
        "**FLAG:** US100 overnight long swap expensive — prefer session-flat / short-bias / D-100 when long-heavy.",
        "Prefer US500 or EURUSD majors when mapping. No agri CFD mapping. No unauthorized alle-only symbols.",
        "",
        f"Artefacts: `results/strateeg2_prescreen/cycle_0046/`. Script: `scripts/s2_c028_lane_a_cycle0046.py`.",
        "",
        "## Suggested Lane-B mapping (Strateeg — not filed by S2; HOLD per v113)",
        "",
        f"- **Symbol:** {surv.get('ftmo_symbol')}",
        "- Prefer session-flat when long index; D-100 swap-aware if overnight.",
        "- Freeze lookback/thresholds before any 2025+ touch.",
        "- Lane-A bruto day_t + early RT stress ≠ formal PASS.",
        "- Pack only — do not ask PREREG while Strateeg Lane-B HOLD.",
        "",
        "## Same-cycle family bests",
        "",
        "| Family | Best symbols | day_t | mean_bp | cost | promote |",
        "|--------|--------------|------:|--------:|------|:-------:|",
    ]
    for r in shortlist:
        lines.append(
            f"| {r['family']} | {r['symbols']} | {r['day_t']} | {r['mean_bp']} | "
            f"{r.get('cost_flag','')} | {r['promote_to_lane_b']} |"
        )
    lines += ["", f"Novelty: **{n_fam}/{n_fam} NEW_FAMILY**. Configs: {n_configs}. Promote configs: {n_surv_cfg}.", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main():
    for old in OUT.glob("*"):
        if old.is_file():
            old.unlink()

    all_rows, pnl_all = [], {}
    for fn in (
        screen_xlp_staples,
        screen_xli_industrials,
        screen_ewa_australia,
        screen_ewc_canada,
        screen_xlu_utilities,
    ):
        rows, store = fn()
        all_rows += rows
        pnl_all.update(store)

    df = pd.DataFrame(all_rows)
    df["_t"] = pd.to_numeric(df["day_t"], errors="coerce")
    df = df.sort_values(["family", "_t"], ascending=[True, False])
    shortlist = [g.iloc[0].drop(labels=["_t"]).to_dict() for _, g in df.groupby("family", sort=True)]
    df.drop(columns=["_t"]).to_csv(OUT / "lane_a_all_rows.csv", index=False)
    pd.DataFrame(shortlist).to_csv(OUT / "lane_a_shortlist.csv", index=False)

    survivors = [r for r in all_rows if r.get("promote_to_lane_b") == "yes"]
    surv_best = []
    if survivors:
        for fam, g in pd.DataFrame(survivors).groupby("family"):
            g = g.copy(); g["_t"] = pd.to_numeric(g["day_t"], errors="coerce")
            surv_best.append(g.sort_values("_t", ascending=False).iloc[0].drop(labels=["_t"]).to_dict())

    bruto_ok = df[
        (pd.to_numeric(df["day_t"], errors="coerce") >= PROMOTE_T)
        & (df["n_days"] >= MIN_DAYS)
        & (pd.to_numeric(df["train_years"], errors="coerce") >= 5)
        & (pd.to_numeric(df["mean_bp"], errors="coerce") > 0)
    ]
    hostile = bruto_ok[bruto_ok["cost_flag"] == "COST_HOSTILE"]
    tight = bruto_ok[bruto_ok["cost_flag"] == "COST_TIGHT"]

    exported = []
    for r in surv_best:
        key = f"{r['symbols']}|{r['lookback_hold']}"
        pnl = pnl_all.get(key)
        if pnl is None:
            for k, v in pnl_all.items():
                if r["symbols"] in k and r["lookback_hold"] in k:
                    pnl = v; break
        if pnl is not None:
            exported.append(str(export_survivor_daily(r["family"], r["symbols"], r["lookback_hold"], pnl).relative_to(ROOT)))
        if "NDX" in r["symbols"]:
            twin_key_part = r["symbols"].replace("NDX", "SPY")
            twin_cfg = r["lookback_hold"]
            for k, v in pnl_all.items():
                if twin_key_part in k and twin_cfg in k:
                    twin_rows = [
                        x for x in all_rows
                        if x["family"] == r["family"]
                        and twin_key_part in x["symbols"]
                        and x["lookback_hold"] == twin_cfg
                        and x.get("promote_to_lane_b") == "yes"
                    ]
                    if twin_rows:
                        exported.append(str(export_survivor_daily(
                            r["family"], twin_rows[0]["symbols"], twin_cfg, v
                        ).relative_to(ROOT)))
                    break
        write_voorstel(r, shortlist, len(all_rows), len(survivors))

    summary = {
        "cycle": "cycle_0046",
        "when": "2026-10-04 ~00:46 Europe/Amsterdam",
        "branch": "grok/strateeg-2",
        "prior_tip": "885090b",
        "next_steps": "v113 @ 400d401",
        "method": "nonoverlap_hold; swap_drag = rt + swap_night*hold; promote=COST_OK only",
        "n_configs": len(all_rows),
        "families": sorted(df["family"].unique().tolist()),
        "new_family_count": int(df["family"].nunique()),
        "n_promote_configs": len(survivors),
        "n_promote_families": len(surv_best),
        "n_cost_hostile_bruto_ok": int(len(hostile)),
        "n_cost_tight_bruto_ok": int(len(tight)),
        "shortlist": shortlist,
        "survivors": surv_best,
        "exported_daily": exported,
        "strateeg_lane_b": "HOLD_v113",
    }
    (OUT / "prescreen_summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")

    lines = [
        "# Strateeg-2 Lane-A pre-screen — cycle_0046 (C-028 + POST-N78/N93; non-overlap holds)",
        "",
        "**When:** 2026-10-04 ~00:46 Europe/Amsterdam (CEST).",
        "**Branch:** `grok/strateeg-2`. **Trials:** 0. Reserve 2025+: untouched.",
        "**Prior tip:** `885090b` (LQD_IG_CREDIT_STRESS + EWY_KOREA_STRESS → N166 FAIL_CLONE / N167 FAIL; families now DEAD).",
        "**NEXT_STEPS:** v113 @ `400d401` (HOLD Strateeg; C-047 NEW_FAMILY ask stale; OPEN empty; TRIAL 471; FREEZE OFF).",
        "**Method:** non-overlapping multi-day trades; drag = RT + swap_night×hold; promote = COST_OK only.",
        "**Note:** Strateeg Lane-B = HOLD — survivors packed for later, not immediate PREREG ask.",
        "",
        "## Families (all NEW_FAMILY)",
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
        f"**Configs:** {len(all_rows)}. **Promote configs:** {len(survivors)}. "
        f"**Promote families:** {len(surv_best)}. **COST_HOSTILE bruto-ok:** {len(hostile)}. "
        f"**COST_TIGHT bruto-ok:** {len(tight)}.",
        "",
        "## Survivors (cost-stressed)" if surv_best else "## Survivors",
    ]
    if surv_best:
        for r in surv_best:
            lines.append(
                f"- **{r['family']}** `{r['symbols']}` {r['lookback_hold']}: "
                f"day_t={r['day_t']}, mean={r['mean_bp']} bp, n={r['n_days']}, yrs={r['train_years']}, "
                f"FTMO={r.get('ftmo_symbol')}, drag={r.get('drag_bp')}, net={r.get('net_after_drag')}, {r.get('cost_flag')}"
            )
    else:
        lines.append("None — no config cleared day_t>=2 + POST-N78 COST_OK.")
    if len(hostile):
        lines += ["", "## Bruto OK but COST_HOSTILE"]
        for _, r in hostile.sort_values("day_t", ascending=False).head(10).iterrows():
            lines.append(f"- {r['family']} `{r['symbols']}` {r['lookback_hold']}: day_t={r['day_t']} mean={r['mean_bp']} drag={r.get('drag_bp')}")
    if len(tight):
        lines += ["", "## Bruto OK but COST_TIGHT (not promoted this cycle)"]
        for _, r in tight.sort_values("day_t", ascending=False).head(10).iterrows():
            lines.append(f"- {r['family']} `{r['symbols']}` {r['lookback_hold']}: day_t={r['day_t']} mean={r['mean_bp']} drag={r.get('drag_bp')} net={r.get('net_after_drag')}")
    (OUT / "prescreen.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT / "survivor_export.json").write_text(
        json.dumps({"survivors": surv_best, "hostile_count": int(len(hostile)), "tight_count": int(len(tight)), "exported": exported}, indent=2, default=str),
        encoding="utf-8",
    )
    print(json.dumps({k: summary[k] for k in summary if k not in ("shortlist", "survivors")}, indent=2))
    cols = ["family", "symbols", "lookback_hold", "train_years", "mean_bp", "day_t", "n_days", "ftmo_symbol", "drag_bp", "cost_flag", "promote_to_lane_b"]
    print("---SHORTLIST---")
    print(pd.DataFrame(shortlist)[cols].to_string(index=False))
    if surv_best:
        print("---SURVIVORS---")
        print(pd.DataFrame(surv_best)[cols].to_string(index=False))
    if len(tight):
        print("---COST_TIGHT (top)---")
        print(tight.sort_values("day_t", ascending=False).head(5)[cols].to_string(index=False))
    if len(hostile):
        print("---COST_HOSTILE (top)---")
        print(hostile.sort_values("day_t", ascending=False).head(5)[cols].to_string(index=False))


if __name__ == "__main__":
    main()
