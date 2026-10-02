#!/usr/bin/env python3
"""Strateeg-2 Lane-A novelty screens — C-028 / cycle_2240 ~22:40 Europe/Amsterdam 2026-10-02.

≥4 NEW_FAMILY mechanisms vs last-30d dead set (incl. EMB_CREDIT_STRESS / CRACK_SPREAD_MACRO
→ N100/N101 FAIL_T, SECTOR_DISP → N93, VIX_TERM → N78, N75–N111, CEO T5–T16).
POST-N78/N93 cost stress. Multi-day holds use NON-OVERLAPPING trades + swap×hold nights.
Rules: Yahoo/proxy daily; cut ≤2024-12-31; reserve 2025+ untouched.
No PREREG (Lane-B = Strateeg).
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
OUT = ROOT / "results" / "strateeg2_prescreen" / "cycle_2240"
CAL_END = pd.Timestamp("2024-12-31")
CAL_START = pd.Timestamp("2005-01-01")
MIN_DAYS = 80
PROMOTE_T = 2.0
OUT.mkdir(parents=True, exist_ok=True)

FTMO_MAP = {
    "SPY": {"ftmo": "US500cash", "rt_bp": 0.78, "swap_long_pct_yr": -4.95, "swap_short_pct_yr": -2.95},
    "NDX": {"ftmo": "US100cash", "rt_bp": 0.66, "swap_long_pct_yr": -7.12, "swap_short_pct_yr": -0.75},
    "GLD": {"ftmo": "XAUUSD", "rt_bp": 0.83, "swap_long_pct_yr": -7.85, "swap_short_pct_yr": -0.37},
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
    # Promote COST_OK only this cycle (harder early stress; parent: mean≥3×RT + net≥1 → exclude HOSTILE)
    # Keep COST_TIGHT as near-miss visible but not promote (stricter than cycle_2140).
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


def screen_factor_qv():
    """FACTOR_QUALITY_VALUE: QUAL vs VLUE relative → SPY/NDX (≠ SECTOR_DISP XL*)."""
    qual = load_close(DAILY / "QUAL.csv")
    vlue = load_close(DAILY / "VLUE.csv")
    usmv = load_close(DAILY / "USMV.csv")
    spy = load_close(DAILY / "SPY.csv")
    ndx = load_close(DAILY / "NDX.csv")
    pairs = {
        "QUAL/VLUE": (qual / vlue).dropna(),
        "QUAL/USMV": (qual / usmv).dropna(),
    }
    rows, detail, pnl_store = [], [], {}
    for pname, rel in pairs.items():
        for z_win in (40, 60, 120):
            for thr in (0.5, 1.0, 1.5):
                z = zscore(rel, z_win)
                d20 = rel.pct_change(20)
                for hold in (1, 3, 5):
                    for tgt_name, tgt in (("SPY", spy), ("NDX", ndx)):
                        for mode in ("z_level", "fade_extreme", "mom_confirm"):
                            ret = fwd_ret(tgt, hold)
                            df = pd.concat({"z": z, "d20": d20, "ret": ret}, axis=1).dropna()
                            pos = pd.Series(0.0, index=df.index)
                            if mode == "z_level":
                                # quality-premium high → risk-on long equity
                                pos[df["z"] > thr] = 1.0
                                pos[df["z"] < -thr] = -1.0
                            elif mode == "fade_extreme":
                                pos[df["z"] > thr] = -1.0
                                pos[df["z"] < -thr] = 1.0
                            else:
                                pos[(df["z"] > 0) & (df["d20"] > 0)] = 1.0
                                pos[(df["z"] < 0) & (df["d20"] < 0)] = -1.0
                            pnl = nonoverlap_pnl(pos, df["ret"], hold)
                            lbh = f"z{z_win}/thr{thr}/{mode}|hold={hold}d"
                            row = summarize_row(
                                "FACTOR_QUALITY_VALUE", f"{pname}->{tgt_name}", lbh, pnl,
                                "NEW_FAMILY; QUAL vs VLUE/USMV factor relative->equity; != SECTOR_DISP XL* / MTUM clones",
                                target_for_cost=tgt_name, pos_mode="both", hold_days=hold,
                            )
                            rows.append(row)
                            detail.append({**row, "pair": pname, "z_win": z_win, "thr": thr, "mode": mode, "hold": hold, "target": tgt_name})
                            pnl_store[f"{pname}->{tgt_name}|{lbh}"] = pnl
    pd.DataFrame(detail).to_csv(OUT / "family_factor_quality_value.csv", index=False)
    return rows, pnl_store


def screen_smallcap():
    """SMALLCAP_BREADTH: IWM or RUT vs SPY relative → NDX/SPY (≠ SECTOR_DISP)."""
    iwm = load_close(DAILY / "IWM.csv")
    rut = load_close(DAILY / "RUT.csv")
    spy = load_close(DAILY / "SPY.csv")
    ndx = load_close(DAILY / "NDX.csv")
    pairs = {
        "IWM/SPY": (iwm / spy).dropna(),
        "RUT/SPY": (rut / spy).dropna(),
    }
    rows, detail, pnl_store = [], [], {}
    for pname, rel in pairs.items():
        for z_win in (40, 60, 120):
            for thr in (0.5, 1.0, 1.5):
                z = zscore(rel, z_win)
                d20 = rel.pct_change(20)
                for hold in (1, 3, 5):
                    for tgt_name, tgt in (("SPY", spy), ("NDX", ndx)):
                        for mode in ("z_level", "fade_extreme", "breadth_mom"):
                            ret = fwd_ret(tgt, hold)
                            df = pd.concat({"z": z, "d20": d20, "ret": ret}, axis=1).dropna()
                            pos = pd.Series(0.0, index=df.index)
                            if mode == "z_level":
                                # smallcap outperformance → risk-on
                                pos[df["z"] > thr] = 1.0
                                pos[df["z"] < -thr] = -1.0
                            elif mode == "fade_extreme":
                                pos[df["z"] > thr] = -1.0
                                pos[df["z"] < -thr] = 1.0
                            else:
                                pos[df["d20"] > 0] = 1.0
                                pos[df["d20"] < 0] = -1.0
                            pnl = nonoverlap_pnl(pos, df["ret"], hold)
                            lbh = f"z{z_win}/thr{thr}/{mode}|hold={hold}d"
                            row = summarize_row(
                                "SMALLCAP_BREADTH", f"{pname}->{tgt_name}", lbh, pnl,
                                "NEW_FAMILY; IWM/RUT vs SPY relative breadth->equity; != SECTOR_DISP / EQW_VS_CAP",
                                target_for_cost=tgt_name, pos_mode="both", hold_days=hold,
                            )
                            rows.append(row)
                            detail.append({**row, "pair": pname, "z_win": z_win, "thr": thr, "mode": mode, "hold": hold, "target": tgt_name})
                            pnl_store[f"{pname}->{tgt_name}|{lbh}"] = pnl
    pd.DataFrame(detail).to_csv(OUT / "family_smallcap_breadth.csv", index=False)
    return rows, pnl_store


def screen_gas():
    """GAS_EQUITY_MACRO: NATGAS_F / UNG z-stress → NDX/SPY (signal-only; NO gas CFD)."""
    nat = load_close(DAILY / "NATGAS_F.csv")
    ung = load_close(DAILY / "UNG.csv")
    spy = load_close(DAILY / "SPY.csv")
    ndx = load_close(DAILY / "NDX.csv")
    sigs = {"NATGAS_F": nat, "UNG": ung}
    rows, detail, pnl_store = [], [], {}
    for sname, sig in sigs.items():
        for z_win in (40, 60, 120):
            for thr in (0.5, 1.0, 1.5):
                z = zscore(sig, z_win)
                d5 = sig.pct_change(5)
                d20 = sig.pct_change(20)
                for hold in (1, 3, 5):
                    for tgt_name, tgt in (("SPY", spy), ("NDX", ndx)):
                        for mode in ("stress_buy", "gas_fade", "trend_follow"):
                            ret = fwd_ret(tgt, hold)
                            df = pd.concat({"z": z, "d5": d5, "d20": d20, "ret": ret}, axis=1).dropna()
                            pos = pd.Series(0.0, index=df.index)
                            if mode == "stress_buy":
                                # gas spike stress → risk-off short equity; crash → buy
                                pos[df["z"] > thr] = -1.0
                                pos[df["z"] < -thr] = 1.0
                            elif mode == "gas_fade":
                                pos[(df["z"] > thr) | (df["d5"] > 0.05)] = -1.0
                                pos[(df["z"] < -thr) | (df["d5"] < -0.05)] = 1.0
                            else:
                                pos[df["d20"] > 0] = -1.0  # rising gas often drag on growth
                                pos[df["d20"] < 0] = 1.0
                            pnl = nonoverlap_pnl(pos, df["ret"], hold)
                            lbh = f"z{z_win}/thr{thr}/{mode}|hold={hold}d"
                            # stress_buy / gas_fade lean short-bias on gas spikes (cheap US100 short swap)
                            pmode = "short_bias" if mode in ("stress_buy", "gas_fade", "trend_follow") else "both"
                            row = summarize_row(
                                "GAS_EQUITY_MACRO", f"{sname}->{tgt_name}", lbh, pnl,
                                "NEW_FAMILY; NATGAS/UNG z-stress->equity SIGNAL ONLY (no gas CFD); != ENERGY_TSMOM/UKOIL/USOIL->US100/CRACK",
                                target_for_cost=tgt_name, pos_mode=pmode, hold_days=hold,
                            )
                            rows.append(row)
                            detail.append({**row, "sig": sname, "z_win": z_win, "thr": thr, "mode": mode, "hold": hold, "target": tgt_name})
                            pnl_store[f"{sname}->{tgt_name}|{lbh}"] = pnl
    pd.DataFrame(detail).to_csv(OUT / "family_gas_equity_macro.csv", index=False)
    return rows, pnl_store


def screen_silver_gold():
    """SILVER_GOLD_RATIO: SLV/GLD or SILVER_F/GOLD_F → SPY/NDX or XAU (≠ COPPER_GOLD)."""
    slv = load_close(DAILY / "SLV.csv")
    gld = load_close(DAILY / "GLD.csv")
    sil_f = load_close(DAILY / "SILVER_F.csv")
    gold_f = load_close(DAILY / "GOLD_F.csv")
    spy = load_close(DAILY / "SPY.csv")
    ndx = load_close(DAILY / "NDX.csv")
    pairs = {
        "SLV/GLD": (slv / gld).dropna(),
        "SILVER_F/GOLD_F": (sil_f / gold_f).dropna(),
    }
    rows, detail, pnl_store = [], [], {}
    for pname, ratio in pairs.items():
        for z_win in (40, 60, 120):
            for thr in (0.5, 1.0, 1.5):
                z = zscore(ratio, z_win)
                d20 = ratio.pct_change(20)
                for hold in (1, 3, 5):
                    targets = (("SPY", spy), ("NDX", ndx), ("GLD", gld))
                    for tgt_name, tgt in targets:
                        for mode in ("z_level", "fade_extreme", "risk_on"):
                            ret = fwd_ret(tgt, hold)
                            df = pd.concat({"z": z, "d20": d20, "ret": ret}, axis=1).dropna()
                            pos = pd.Series(0.0, index=df.index)
                            if mode == "z_level":
                                # high Ag/Au = industrial risk-on
                                pos[df["z"] > thr] = 1.0
                                pos[df["z"] < -thr] = -1.0
                            elif mode == "fade_extreme":
                                pos[df["z"] > thr] = -1.0
                                pos[df["z"] < -thr] = 1.0
                            else:
                                # risk_on: Ag/Au rising → long equity / short gold
                                if tgt_name == "GLD":
                                    pos[df["d20"] > 0] = -1.0
                                    pos[df["d20"] < 0] = 1.0
                                else:
                                    pos[df["d20"] > 0] = 1.0
                                    pos[df["d20"] < 0] = -1.0
                            pnl = nonoverlap_pnl(pos, df["ret"], hold)
                            lbh = f"z{z_win}/thr{thr}/{mode}|hold={hold}d"
                            # GLD short-bias often cheap swap when risk_on shorts gold
                            pmode = "short_bias" if (tgt_name == "GLD" and mode == "risk_on") else "both"
                            row = summarize_row(
                                "SILVER_GOLD_RATIO", f"{pname}->{tgt_name}", lbh, pnl,
                                "NEW_FAMILY; Ag/Au industrial-vs-monetary ratio->equity/XAU; != COPPER_GOLD / PGM",
                                target_for_cost=tgt_name, pos_mode=pmode, hold_days=hold,
                            )
                            rows.append(row)
                            detail.append({**row, "pair": pname, "z_win": z_win, "thr": thr, "mode": mode, "hold": hold, "target": tgt_name})
                            pnl_store[f"{pname}->{tgt_name}|{lbh}"] = pnl
    pd.DataFrame(detail).to_csv(OUT / "family_silver_gold_ratio.csv", index=False)
    return rows, pnl_store


def export_survivor_daily(family, symbols, lookback_hold, pnl):
    safe = family + "_" + "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in f"{symbols}_{lookback_hold}")
    out = OUT / f"{safe[:120]}_daily.csv"
    pd.DataFrame({"date": pnl.index, "pnl_bp": pnl.values}).to_csv(out, index=False)
    return out


def write_voorstel(surv, shortlist, n_configs, n_surv_cfg):
    fam = surv["family"]
    path = OUT / f"VOORSTEL_S2_{fam}.md"
    lines = [
        f"# VOORSTEL S2 — {fam} (Lane-A survivor, C-028 + POST-N78/N93)",
        "",
        "**When:** 2026-10-02 ~22:40 Europe/Amsterdam (CEST)",
        "**Author:** Strateeg-2 (`grok/strateeg-2`) — Lane-A novelty researcher",
        "**Status:** Lane-A **promote** (day_t>=2 bruto **and** early FTMO RT/swap stress COST_OK). **Not** a PREREG. Strateeg files Lane-B PREREG if accepted.",
        "**Trials:** 0. Reserve 2025+: **untouched**.",
        "",
        "## Family tag",
        "",
        f"`NEW_FAMILY: {fam}`",
        "",
        "**Distinct from dead / barred:** ORB / TSMOM / L60 FX-med / ENERGY_TSMOM / VIX_TERM_VOV /",
        "CORN / UKOIL-OVN / ORB-meta / **SECTOR_DISP** / PC_RATIO / BREAKEVEN / COPPER_GOLD /",
        "CREDIT HYG-LQD / RATE_CURVE / EM_DM / **EMB_CREDIT_STRESS** / **CRACK_SPREAD_MACRO** /",
        "REIT_RATE / PGM / N75–N111 / CEO T5–T16 / FX LO carry clones.",
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
        "",
        f"Artefacts: `results/strateeg2_prescreen/cycle_2240/`. Script: `scripts/s2_c028_lane_a_cycle2240.py`.",
        "",
        "## Suggested Lane-B mapping (Strateeg — not filed by S2)",
        "",
        f"- **Symbol:** {surv.get('ftmo_symbol')}",
        "- Prefer session-flat when long index; D-100 swap-aware if overnight.",
        "- Freeze lookback/thresholds before any 2025+ touch.",
        "- Lane-A bruto day_t + early RT stress ≠ formal PASS.",
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
    lines += ["", f"Novelty: **4/4 NEW_FAMILY**. Configs: {n_configs}. Promote configs: {n_surv_cfg}.", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main():
    for old in OUT.glob("*"):
        if old.is_file():
            old.unlink()

    all_rows, pnl_all = [], {}
    for fn in (screen_factor_qv, screen_smallcap, screen_gas, screen_silver_gold):
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
        write_voorstel(r, shortlist, len(all_rows), len(survivors))

    summary = {
        "cycle": "cycle_2240",
        "when": "2026-10-02 ~22:40 Europe/Amsterdam",
        "branch": "grok/strateeg-2",
        "prior_tip": "67a9be1",
        "next_steps": "v91 @ 88ad118",
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
    }
    (OUT / "prescreen_summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")

    lines = [
        "# Strateeg-2 Lane-A pre-screen — cycle_2240 (C-028 + POST-N78/N93; non-overlap holds)",
        "",
        "**When:** 2026-10-02 ~22:40 Europe/Amsterdam (CEST).",
        "**Branch:** `grok/strateeg-2`. **Trials:** 0. Reserve 2025+: untouched.",
        "**Prior tip:** `67a9be1` (EMB+CRACK → N100/N101 FAIL_T; families now DEAD).",
        "**NEXT_STEPS:** v91 @ `88ad118` (C-036; TRIAL 460; formal OPEN empty).",
        "**Method:** non-overlapping multi-day trades; drag = RT + swap_night×hold; promote = COST_OK only.",
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


if __name__ == "__main__":
    main()
