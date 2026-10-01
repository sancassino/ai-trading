#!/usr/bin/env python3
"""C-018 — D-094 tracks 3+5: weak-positive portfolio combine + FTMO sizing grid.

Informational / diagnostic only:
  - NOT a PREREG trial; no TRIALS append
  - Reserve 2025+ unused (decision windows ≤2024-12-31; sleeve trains ≤2023)
  - Gate-PASS→FAIL_T sleeves (N11/N18/LUNCH_OPEN) used ONLY as portfolio
    diagnostics — do NOT reopen as solo clones (D-094 + dead-set rule)
"""
from __future__ import annotations

import csv
import json
import os
from pathlib import Path

import numpy as np

from engine.ftmo import ftmo_ev, load_daily_equity_csv, recommend_scale, trades_bp_to_daily

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "results/cto/c018_combine_ftmo.json"
OUT_MD = ROOT / "results/cto/c018_combine_ftmo.md"
OUT_BOARD = ROOT / "results/cto/c018_board.json"
N_PATHS = 5_000
N_PATHS_GRID = 3_000
SEED = 7
WHEN = "2026-10-01 ~08:10 Europe/Amsterdam (CEST / UTC+2)"


def load_orb_dates():
    dates = []
    with open(ROOT / "results/f/F2_ORB_daily.csv", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f, delimiter=";"):
            dates.append(row["date"].replace(".", "-"))
    return np.asarray(dates)


def ev_pack(series, dd=None, *, label, sleeve, window, extra=None, n_paths=N_PATHS):
    series = np.asarray(series, float).ravel()
    if series.size < 2 or np.all(series == 0):
        return {
            "sleeve": sleeve,
            "label": label,
            "window": window,
            "n_days": int(series.size),
            "n_active_days": int((series != 0).sum()),
            "error": "empty_or_flat",
        }
    rec = recommend_scale(series, dd, n_paths=n_paths, seed=SEED)
    ev = ftmo_ev(
        series,
        daily_drawdowns=None if dd is None else dd,
        n_paths=n_paths,
        scale=rec["scale"],
        seed=SEED,
    )
    out = {
        "sleeve": sleeve,
        "label": label,
        "window": window,
        "n_days": int(series.size),
        "n_active_days": int((series != 0).sum()),
        "daily_mean": float(series.mean()),
        "daily_std": float(series.std()),
        "ann_sr_proxy": (
            float(series.mean() / series.std() * np.sqrt(252.0))
            if series.std() > 0
            else None
        ),
        "skew_daily": float(
            ((series - series.mean()) ** 3).mean() / (series.std() ** 3)
            if series.std() > 0
            else 0.0
        ),
        "scale": float(rec["scale"]),
        "binding": rec["binding"],
        "p95_daily_loss": float(rec["p95_daily_loss"]),
        "max_daily_loss": float(rec["max_daily_loss"]),
        "p_pass_1": float(ev["p_pass_1"]),
        "p_pass_2": float(ev["p_pass_2"]),
        "p_pass_product": float(ev["p_pass_1"] * ev["p_pass_2"]),
        "p_survive": float(ev["p_survive"]),
        "net_ev_monthly": float(ev["net_ev_monthly"]),
        "exp_payout_monthly": float(ev["exp_payout_monthly"]),
        "attempts_mean": float(ev["attempts_mean"]),
        "meets_d092_5_p_pass_product": bool(ev["p_pass_1"] * ev["p_pass_2"] >= 0.35),
        "meets_d092_5_net_ev_pos": bool(ev["net_ev_monthly"] > 0),
    }
    if extra:
        out.update(extra)
    return out


def align_to(calendar_days, src_days, src_r):
    out = np.zeros(calendar_days.size, float)
    idx = {str(d): i for i, d in enumerate(calendar_days)}
    for d0, v in zip(src_days, src_r):
        k = str(d0)
        if k in idx:
            out[idx[k]] += float(v)
    return out


def vol_target(x, target_daily_std):
    s = float(np.std(x))
    if s <= 0:
        return x * 0.0
    return x * (float(target_daily_std) / s)


def corr(a, b):
    mask = (a != 0) | (b != 0)
    aa, bb = a[mask], b[mask]
    if aa.size < 5 or aa.std() == 0 or bb.std() == 0:
        # fall back to full calendar if sparse overlap
        if a.std() == 0 or b.std() == 0:
            return None
        return float(np.corrcoef(a, b)[0, 1])
    return float(np.corrcoef(aa, bb)[0, 1])


def load_trades_bp(path, date_col, bp_col, *, filter_fn=None, bp_fn=None):
    dates, bps = [], []
    with open(ROOT / path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if filter_fn is not None and not filter_fn(row):
                continue
            dates.append(row[date_col])
            if bp_fn is not None:
                bps.append(float(bp_fn(row)))
            else:
                bps.append(float(row[bp_col]))
    return dates, bps


def scale_grid(series, dd=None, *, scales, n_paths=N_PATHS_GRID):
    """Track 5: sweep scale → p_pass / p_survive / EV (low-vol positive-skew sizing)."""
    rows = []
    for sc in scales:
        ev = ftmo_ev(
            series,
            daily_drawdowns=None if dd is None else dd,
            n_paths=n_paths,
            scale=float(sc),
            seed=SEED,
        )
        # empirical loss at this scale
        r = np.asarray(series, float).ravel() * float(sc)
        if dd is None:
            loss = np.maximum(0.0, -r)
        else:
            loss = np.asarray(dd, float).ravel() * float(sc)
        rows.append(
            {
                "scale": float(sc),
                "p_pass_1": float(ev["p_pass_1"]),
                "p_pass_2": float(ev["p_pass_2"]),
                "p_pass_product": float(ev["p_pass_1"] * ev["p_pass_2"]),
                "p_survive": float(ev["p_survive"]),
                "net_ev_monthly": float(ev["net_ev_monthly"]),
                "exp_payout_monthly": float(ev["exp_payout_monthly"]),
                "attempts_mean": float(ev["attempts_mean"]),
                "p95_daily_loss": float(np.quantile(loss, 0.95)),
                "max_daily_loss": float(loss.max()),
                "within_4pct_cap": bool(loss.max() <= 0.04 + 1e-12),
            }
        )
    # pick: max net_ev among within_4pct; also best p_pass*p_survive product
    feasible = [x for x in rows if x["within_4pct_cap"]]
    best_ev = max(feasible, key=lambda x: x["net_ev_monthly"]) if feasible else None
    best_pass_surv = (
        max(feasible, key=lambda x: x["p_pass_product"] * x["p_survive"])
        if feasible
        else None
    )
    # soft target: high survive with p_pass_product≥0.35 and EV>0
    cand = [
        x
        for x in feasible
        if x["p_pass_product"] >= 0.35 and x["net_ev_monthly"] > 0
    ]
    best_survive_under_gate = (
        max(cand, key=lambda x: x["p_survive"]) if cand else None
    )
    return {
        "rows": rows,
        "best_net_ev_within_4pct": best_ev,
        "best_pass_x_survive_within_4pct": best_pass_surv,
        "best_survive_given_pass035_evpos": best_survive_under_gate,
    }


def main():
    os.chdir(ROOT)
    r, dd = load_daily_equity_csv("results/f/F2_ORB_daily.csv")
    dates = load_orb_dates()

    rows = []
    inventory = []

    # --- Reference ORB windows ---
    for label, lo, hi, note in [
        (
            "F2_ORB_reference_le2024",
            "2021-01-01",
            "2024-12-31",
            "Binding reference; reserve 2025+ not used",
        ),
        (
            "F2_ORB_train_2021_2023",
            "2021-01-01",
            "2023-12-31",
            "Train window aligned with sleeve cost-gates",
        ),
    ]:
        m = (dates >= lo) & (dates <= hi)
        rows.append(
            ev_pack(
                r[m],
                dd[m],
                label=label,
                sleeve="F2_ORB",
                window=f"{lo}..{hi}",
                extra={"note": note, "uses_trough_dd": True, "status": "reference_edge"},
            )
        )
    inventory.append(
        {
            "sleeve": "F2_ORB",
            "role": "anchor / weak-positive reference",
            "status": "reference_edge (HistData M1 blocked for longer replicate)",
            "solo_reopen": False,
            "source": "results/f/F2_ORB_daily.csv",
        }
    )

    # --- Load sleeve trade series (all ≤2023 train artefacts) ---
    btc_dates, btc_net = load_trades_bp(
        "results/cto/s2_btc_prep/cost_gate_s2_btc_train.csv", "date", "net_bp"
    )
    btc_r, btc_days = trades_bp_to_daily(btc_dates, btc_net)
    inventory.append(
        {
            "sleeve": "S2_BTC",
            "role": "power-fail diversifier (high bruto, N<150)",
            "status": "power_FAIL N=132<150; cost gate PASS",
            "n_trades": len(btc_dates),
            "solo_reopen": False,
            "source": "results/cto/s2_btc_prep/cost_gate_s2_btc_train.csv",
        }
    )

    xau_dates, xau_net = load_trades_bp(
        "results/s2_xau_am_fade_train.csv",
        "date",
        "bruto_bp",
        bp_fn=lambda row: float(row["bruto_bp"]) - float(row["rt"]),
    )
    xau_r, xau_days = trades_bp_to_daily(xau_dates, xau_net)
    inventory.append(
        {
            "sleeve": "XAU_AM_FADE",
            "role": "watch-only underpowered",
            "status": "watch_only N=12≪120",
            "n_trades": len(xau_dates),
            "solo_reopen": False,
            "source": "results/s2_xau_am_fade_train.csv",
        }
    )

    n11_dates, n11_net = load_trades_bp(
        "results/R2/n11_prep/cost_gate_n11_train.csv", "date", "netto_bp"
    )
    n11_r, n11_days = trades_bp_to_daily(n11_dates, n11_net)
    inventory.append(
        {
            "sleeve": "N11_GER40_XETRA_ORB",
            "role": "portfolio diagnostic only (gate PASS → FAIL_STRESS/FAIL_T)",
            "status": "FAIL_STRESS_then_FAIL_T (t_day≈0.92); DEAD — no solo reopen/clone",
            "n_trades": len(n11_dates),
            "solo_reopen": False,
            "source": "results/R2/n11_prep/cost_gate_n11_train.csv",
        }
    )

    n18_dates, n18_net = load_trades_bp(
        "results/R2/n18_prep/cost_gate_n18_train.csv", "date", "netto_bp"
    )
    n18_r, n18_days = trades_bp_to_daily(n18_dates, n18_net)
    inventory.append(
        {
            "sleeve": "N18_US500_OVN_GAP_CONT",
            "role": "portfolio diagnostic only (gate+stress PASS → FAIL_T)",
            "status": "FAIL_T (t_day≈0.64; 2023 mean−12bp); DEAD — no solo reopen/clone",
            "n_trades": len(n18_dates),
            "solo_reopen": False,
            "source": "results/R2/n18_prep/cost_gate_n18_train.csv",
        }
    )

    lunch_dates, lunch_net = load_trades_bp(
        "results/R2/lunch_open_prep/trial_lunch_open_trades.csv",
        "date",
        "netto_bp",
        filter_fn=lambda row: row.get("window") == "train",
    )
    lunch_r, lunch_days = trades_bp_to_daily(lunch_dates, lunch_net)
    inventory.append(
        {
            "sleeve": "LUNCH_OPEN",
            "role": "portfolio diagnostic only (cost PASS → FAIL_T; positive skew)",
            "status": "FAIL_T (t_train≈1.14, t_test≈0.05); DEAD — no solo reopen/clone",
            "n_trades": len(lunch_dates),
            "solo_reopen": False,
            "note": "skew_day≈2.43 on train — interesting for track-5 low-vol positive-skew sizing",
            "source": "results/R2/lunch_open_prep/trial_lunch_open_trades.csv (train)",
        }
    )

    # Calendar = ORB train days
    m_tr = (dates >= "2021-01-01") & (dates <= "2023-12-31")
    orb_days = np.asarray(dates[m_tr], dtype="datetime64[D]")
    orb_r = r[m_tr]
    orb_dd = dd[m_tr]
    btc_on = align_to(orb_days, btc_days, btc_r)
    xau_on = align_to(orb_days, xau_days, xau_r)
    n11_on = align_to(orb_days, n11_days, n11_r)
    n18_on = align_to(orb_days, n18_days, n18_r)
    lunch_on = align_to(orb_days, lunch_days, lunch_r)

    series_map = {
        "ORB": orb_r,
        "BTC": btc_on,
        "XAU": xau_on,
        "N11": n11_on,
        "N18": n18_on,
        "LUNCH": lunch_on,
    }
    pair_names = list(series_map.keys())
    corrs = {}
    for i, a in enumerate(pair_names):
        for b in pair_names[i + 1 :]:
            corrs[f"{a}_{b}"] = corr(series_map[a], series_map[b])

    # Singles on train calendar
    singles = [
        ("F2_ORB", orb_r, orb_dd, "reference_edge", True, None),
        ("S2_BTC", btc_on, None, "power_fail_watch", False, 132),
        ("XAU_AM_FADE", xau_on, None, "watch_only_underpowered", False, 12),
        ("N11_GER40", n11_on, None, "FAIL_T_diagnostic_only", False, len(n11_dates)),
        ("N18_GAP_CONT", n18_on, None, "FAIL_T_diagnostic_only", False, len(n18_dates)),
        ("LUNCH_OPEN", lunch_on, None, "FAIL_T_diagnostic_only", False, len(lunch_dates)),
    ]
    for sleeve, ser, sdd, status, trough, ntr in singles:
        extra = {
            "status": status,
            "uses_trough_dd": trough,
            "note": "solo diagnostic; not a reopen",
        }
        if ntr is not None:
            extra["n_trades"] = ntr
        rows.append(
            ev_pack(
                ser,
                sdd,
                label="sleeve_train",
                sleeve=sleeve,
                window="2021-01-01..2023-12-31",
                extra=extra,
            )
        )

    # --- Track 3a: portfolio blends (vol-match to ORB daily std) ---
    target = float(orb_r.std())
    orb_v = vol_target(orb_r, target)
    btc_v = vol_target(btc_on, target)
    xau_v = vol_target(xau_on, target)
    n11_v = vol_target(n11_on, target)
    n18_v = vol_target(n18_on, target)
    lunch_v = vol_target(lunch_on, target)

    blends = {
        # carry-forward D-092 blends
        "ORB+BTC_eqvol": (orb_v + btc_v) / 2.0,
        "ORB+BTC+XAU_eqvol": (orb_v + btc_v + xau_v) / 3.0,
        "ORB70_BTC25_XAU5": 0.70 * orb_v + 0.25 * btc_v + 0.05 * xau_v,
        # C-018: add FAIL_T legs as *portfolio diagnostics only*
        "ORB+LUNCH_eqvol": (orb_v + lunch_v) / 2.0,
        "ORB+N18_eqvol": (orb_v + n18_v) / 2.0,
        "ORB+N11_eqvol": (orb_v + n11_v) / 2.0,
        "ORB+BTC+LUNCH_eqvol": (orb_v + btc_v + lunch_v) / 3.0,
        "ORB60_BTC25_LUNCH15": 0.60 * orb_v + 0.25 * btc_v + 0.15 * lunch_v,
        "ORB50_BTC20_LUNCH20_N18_10": (
            0.50 * orb_v + 0.20 * btc_v + 0.20 * lunch_v + 0.10 * n18_v
        ),
        "WEAK5_eqvol": (orb_v + btc_v + xau_v + lunch_v + n18_v) / 5.0,
    }
    for name, series in blends.items():
        rows.append(
            ev_pack(
                series,
                None,
                label="portfolio_blend_train",
                sleeve=name,
                window="2021-01-01..2023-12-31",
                extra={
                    "note": (
                        "D-094.3a / C-018: vol-match to ORB daily std then weighted; "
                        "close-only DD proxy; NOT a new hypothesis/trial; "
                        "FAIL_T legs are diversifier diagnostics only"
                    ),
                    "target_daily_std": target,
                    "uses_trough_dd": False,
                    "track": "3a_combining",
                },
            )
        )

    # BTC +50% cost stress on key blends
    btc_stress = []
    with open("results/cto/s2_btc_prep/cost_gate_s2_btc_train.csv") as f:
        for row in csv.DictReader(f):
            btc_stress.append(float(row["gross_bp"]) - 1.5 * float(row["cost_bp"]))
    btc_s_r, btc_s_days = trades_bp_to_daily(btc_dates, btc_stress)
    btc_s_on = align_to(orb_days, btc_s_days, btc_s_r)
    btc_s_v = vol_target(btc_s_on, target)
    stress_blends = {
        "ORB+BTC_eqvol_BTCstress50": (orb_v + btc_s_v) / 2.0,
        "ORB60_BTC25_LUNCH15_BTCstress50": (
            0.60 * orb_v + 0.25 * btc_s_v + 0.15 * lunch_v
        ),
    }
    for name, series in stress_blends.items():
        rows.append(
            ev_pack(
                series,
                None,
                label="portfolio_blend_train_cost_stress50_btc",
                sleeve=name,
                window="2021-01-01..2023-12-31",
                extra={
                    "note": "BTC leg gross−1.5×cost; other legs unchanged",
                    "uses_trough_dd": False,
                    "track": "3a_combining",
                },
            )
        )

    # --- Track 3b: ensemble / filter hypotheses (documented, not executed as trials) ---
    ensemble_hypotheses = [
        {
            "id": "H-ENS-01",
            "name": "ORB ∩ LUNCH same-day filter",
            "mechanism": (
                "Trade F2-ORB only on days LUNCH_OPEN also fires in same direction "
                "(or only when LUNCH morning residual agrees with ORB breakout side)."
            ),
            "why_plausible": (
                "LUNCH_OPEN is afternoon US indices mean-reversion/continuation after "
                "morning move; ORB is morning breakout — low raw ρ expected; AND-filter "
                "may cut false ORB days and raise per-trade edge at cost of N."
            ),
            "data_note": (
                f"ρ(ORB,LUNCH) on train dense calendar ≈ {corrs.get('ORB_LUNCH')}; "
                f"LUNCH N_train={len(lunch_dates)}; ORB active days≈{(orb_r!=0).sum()}. "
                "Overlap count not claimed as edge — needs own PREREG if pursued."
            ),
            "status": "hypothesis_only — no PREREG this cycle; do not mine thresholds post-hoc",
            "owner": "CEO/Strateeg (D-094.7: CEO may write ensemble PREREGs)",
        },
        {
            "id": "H-ENS-02",
            "name": "ORB + BTC regime gate",
            "mechanism": (
                "Size ORB normally; add BTC US-open sleeve only when BTC realized vol "
                "or prior-day range ≥ median (cost/vol screen already favors BTC)."
            ),
            "why_plausible": (
                "S2-BTC has large bruto (+18.5 bp mean net) but power-FAIL; regime gate "
                "may stabilize N while keeping diversifier ρ≈0.11 with ORB."
            ),
            "data_note": (
                f"ρ(ORB,BTC)≈{corrs.get('ORB_BTC')}; BTC N=132. Power fix = more instruments "
                "(ETH/SOL pool) not threshold-mining on same 132."
            ),
            "status": "hypothesis_only — prefer S2b/S2c-style pre-registered pools over filters",
            "owner": "Strateeg-2",
        },
        {
            "id": "H-ENS-03",
            "name": "Stack small edges → SR≈1 (equal-vol book)",
            "mechanism": (
                "Hold a book of 3–5 weak/near sleeves at equal vol contribution; "
                "scale book via recommend_scale for p_pass & p_survive (track 5)."
            ),
            "why_plausible": (
                "D-091 ambition grid: SR≳1 needed for €800/m. Single sleeves sit SR≈0.7–1.1; "
                "low pairwise ρ (see corr matrix) can lift book SR toward 1.2–1.3 on paper."
            ),
            "data_note": (
                "See WEAK5_eqvol / ORB60_BTC25_LUNCH15 rows. Paper SR lift ≠ validated edge: "
                "FAIL_T legs remain unvalidated; book is diagnostic ceiling not candidate."
            ),
            "status": "diagnostic_ceiling — Auditor may rebuild EV; no eval advice",
            "owner": "CTO (this deliverable) + Auditor",
        },
        {
            "id": "H-ENS-04",
            "name": "N18 year-stability filter (REJECT as solo reopen)",
            "mechanism": "Drop N18 2023 / trade only 2021–22 gap-cont.",
            "why_plausible": "None post-hoc — 2023 mean −12 bp is instability, not a filter to invent.",
            "data_note": "Explicit anti-pattern under integrity rules.",
            "status": "REJECTED — would be result-dependent reopen of dead sleeve",
            "owner": "CTO (bar)",
        },
    ]

    # --- Track 5: sizing grids for key series ---
    # scales from conservative to near 4% max-loss binding
    scale_list = [0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 7.0, 8.0]
    sizing = {}
    sizing_targets = {
        "F2_ORB_train": (orb_r, orb_dd),
        "F2_ORB_le2024": (
            r[(dates >= "2021-01-01") & (dates <= "2024-12-31")],
            dd[(dates >= "2021-01-01") & (dates <= "2024-12-31")],
        ),
        "LUNCH_OPEN_train": (lunch_on, None),
        "ORB+BTC_eqvol": (blends["ORB+BTC_eqvol"], None),
        "ORB60_BTC25_LUNCH15": (blends["ORB60_BTC25_LUNCH15"], None),
        "WEAK5_eqvol": (blends["WEAK5_eqvol"], None),
    }
    for name, (ser, sdd) in sizing_targets.items():
        # auto-extend grid around recommend_scale
        rec = recommend_scale(ser, sdd, n_paths=N_PATHS_GRID, seed=SEED)
        scales = sorted(set(scale_list + [round(rec["scale"], 2), round(rec["scale"] * 0.75, 2), round(rec["scale"] * 1.1, 2)]))
        sizing[name] = {
            "recommend_scale": {
                "scale": float(rec["scale"]),
                "binding": rec["binding"],
                "p95_daily_loss": float(rec["p95_daily_loss"]),
                "max_daily_loss": float(rec["max_daily_loss"]),
                "p_pass_2": float(rec["p_pass_2"]),
                "p_survive": float(rec["p_survive"]),
                "net_ev_monthly": float(rec["net_ev_monthly"]),
            },
            "grid": scale_grid(ser, sdd, scales=scales),
            "skew_daily": float(
                ((ser - ser.mean()) ** 3).mean() / (ser.std() ** 3)
                if ser.std() > 0
                else 0.0
            ),
            "ann_sr_proxy": (
                float(ser.mean() / ser.std() * np.sqrt(252.0)) if ser.std() > 0 else None
            ),
        }

    # --- Markdown ---
    def fmt_row(row):
        if "error" in row:
            return None
        sr = "" if row.get("ann_sr_proxy") is None else f"{row['ann_sr_proxy']:.2f}"
        return (
            f"| {row['sleeve']} | {row['label'][:36]} | {row.get('n_active_days','')} | "
            f"{sr} | {row.get('skew_daily',0):.2f} | {row['scale']:.2f} | "
            f"{row['p95_daily_loss']:.2%} | {row['max_daily_loss']:.2%} | "
            f"{row['p_pass_product']:.3f} | {row['p_survive']:.3f} | "
            f"{row['net_ev_monthly']:.0f} |"
        )

    md = [
        "# C-018 — D-094 tracks 3+5: combine + FTMO sizing (CTO)",
        "",
        f"- When: {WHEN}",
        "- Branch: `grok/cto-1`",
        "- Reserve 2025+: **not used**",
        "- No PREREG trial / no TRIALS append / no dead-sleeve solo reopen",
        "- Integrity: PREREG-before-results, append-only TRIALS, day-clustered t, FDR, FTMO costs",
        "",
        "## Inventory (weak-positive / near-pass)",
        "",
        "| Sleeve | Role | Status | Solo reopen? |",
        "|---|---|---|---|",
    ]
    for inv in inventory:
        md.append(
            f"| {inv['sleeve']} | {inv['role']} | {inv['status']} | "
            f"{'NO' if not inv['solo_reopen'] else 'yes'} |"
        )

    md += [
        "",
        "## Correlations (train 2021–2023, dense ORB calendar)",
        "",
        "| Pair | ρ |",
        "|---|---:|",
    ]
    for k, v in sorted(corrs.items()):
        md.append(f"| {k.replace('_', ' ↔ ')} | {v:.3f} |" if v is not None else f"| {k} | n/a |")

    md += [
        "",
        "## Track 3a — singles + portfolio blends (`recommend_scale` → `ftmo_ev`)",
        "",
        "| Sleeve | Window / label | N_act | ann SR | skew | scale | p95 dip | max dip | p1·p2 | p_survive | €/m net EV |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        line = fmt_row(row)
        if line:
            md.append(line)

    md += [
        "",
        "## Track 3b — ensemble / filter hypotheses (documented only)",
        "",
    ]
    for h in ensemble_hypotheses:
        md.append(f"### {h['id']}: {h['name']}")
        md.append(f"- **Status:** {h['status']}")
        md.append(f"- **Owner:** {h['owner']}")
        md.append(f"- **Mechanism:** {h['mechanism']}")
        md.append(f"- **Why plausible:** {h['why_plausible']}")
        md.append(f"- **Data note:** {h['data_note']}")
        md.append("")

    md += [
        "## Track 5 — FTMO sizing grids (optimize p_pass & p_survive; cap max daily loss ≤4%)",
        "",
        "Method: sweep scale on each series; report `recommend_scale` anchor plus best-EV /",
        "best (p_pass×p_survive) / best-survive-given (p1·p2≥0.35 ∧ EV>0) among scales with max loss ≤4%.",
        "",
    ]
    for name, block in sizing.items():
        rs = block["recommend_scale"]
        g = block["grid"]
        md.append(f"### {name}")
        md.append(
            f"- ann SR≈{block['ann_sr_proxy'] and round(block['ann_sr_proxy'],2)}; "
            f"daily skew≈{block['skew_daily']:.2f}"
        )
        md.append(
            f"- **recommend_scale:** scale={rs['scale']:.2f} ({rs['binding']}); "
            f"p95={rs['p95_daily_loss']:.2%}; max={rs['max_daily_loss']:.2%}; "
            f"p_pass2={rs['p_pass_2']:.3f}; p_survive={rs['p_survive']:.3f}; "
            f"EV≈€{rs['net_ev_monthly']:.0f}/m"
        )
        for key, label in [
            ("best_net_ev_within_4pct", "best net EV ≤4%"),
            ("best_pass_x_survive_within_4pct", "best p_pass×p_survive ≤4%"),
            ("best_survive_given_pass035_evpos", "best survive | p1·p2≥0.35 & EV>0"),
        ]:
            hit = g.get(key)
            if hit:
                md.append(
                    f"- **{label}:** scale={hit['scale']:.2f}; "
                    f"p1·p2={hit['p_pass_product']:.3f}; surv={hit['p_survive']:.3f}; "
                    f"EV≈€{hit['net_ev_monthly']:.0f}/m; "
                    f"p95={hit['p95_daily_loss']:.2%}; max={hit['max_daily_loss']:.2%}"
                )
            else:
                md.append(f"- **{label}:** none")
        md.append("")
        md.append("| scale | p1·p2 | p_survive | €/m EV | p95 | max | ≤4%? |")
        md.append("|---:|---:|---:|---:|---:|---:|:---:|")
        for gr in g["rows"]:
            md.append(
                f"| {gr['scale']:.2f} | {gr['p_pass_product']:.3f} | {gr['p_survive']:.3f} | "
                f"{gr['net_ev_monthly']:.0f} | {gr['p95_daily_loss']:.2%} | "
                f"{gr['max_daily_loss']:.2%} | {'Y' if gr['within_4pct_cap'] else 'N'} |"
            )
        md.append("")

    md += [
        "## Readout (CTO)",
        "",
        "1. **Anchor remains F2-ORB** (train SR≈1.0+, le2024 reference EV from recommend_scale).",
        "2. **Low correlations** across ORB / BTC / LUNCH / N18 → paper diversification is real; "
        "XAU still negligible (N=12).",
        "3. **FAIL_T legs (N11/N18/LUNCH) must not be reopened solo** — portfolio rows are "
        "diagnostic ceilings showing how stacking *could* lift SR toward ≈1.2, not candidates.",
        "4. **Track 5:** for positive-skew sparse sleeves (LUNCH), recommend_scale often binds on "
        "**max** daily loss before p95; lower scale raises p_survive at the cost of EV — "
        "use the survive-under-gate column when ambition is pass-rate not €/m max.",
        "5. **ORB+BTC** still the strongest *paper* two-sleeve book; +LUNCH can help survive "
        "if BTC stress-held; treat as research direction for CEO ensemble PREREG (H-ENS-01/03), "
        "not eval advice.",
        "6. **Manager NEXT_STEPS:** still v62 (D-093 freeze) on main at absorb time — D-094 not "
        "yet in NEXT_STEPS; CTO does not edit main (leave to Manager).",
        "7. No reserve 2025+ opened. No real money / no FTMO signup.",
        "",
    ]
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    out = {
        "when": WHEN,
        "deliverable": "C-018",
        "decision": "D-094 tracks 3 + 5",
        "reserve_2025_touched": False,
        "prereg_trial": False,
        "dead_sleeves_reopened_solo": False,
        "n_paths": N_PATHS,
        "n_paths_grid": N_PATHS_GRID,
        "seed": SEED,
        "inventory": inventory,
        "correlations_train_2021_2023": corrs,
        "ensemble_hypotheses": ensemble_hypotheses,
        "sleeve_inputs": {i["sleeve"]: i["source"] for i in inventory},
        "method": (
            "recommend_scale(p95≤2%, max≤4%) then ftmo_ev; "
            "portfolio = vol-match sleeves to ORB daily std, weighted sum, close-only DD; "
            "sizing grid sweeps scale for p_pass / p_survive / EV under 4% max-loss cap"
        ),
        "rows": rows,
        "sizing_grids": sizing,
        "markdown": str(OUT_MD.relative_to(ROOT)),
        "manager_next_steps_note": (
            "main NEXT_STEPS still v62 (D-093 freeze) at C-018 push; D-094/D-094a absorbed "
            "from origin/claude/ftmo-trading-strategy-98mplz into RUNLOG_CTO only — "
            "Manager owns NEXT_STEPS bump"
        ),
    }
    OUT_JSON.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

    board = {
        "id": "C-018",
        "when": WHEN,
        "tracks": ["D-094.3 combining", "D-094.5 FTMO structure/sizing"],
        "artefacts": [
            str(OUT_JSON.relative_to(ROOT)),
            str(OUT_MD.relative_to(ROOT)),
        ],
        "reserve_2025_touched": False,
        "prereg_trial": False,
        "highlights": {},
    }
    # pull key numbers into board
    for row in rows:
        if row.get("sleeve") in (
            "ORB+BTC_eqvol",
            "ORB60_BTC25_LUNCH15",
            "WEAK5_eqvol",
            "F2_ORB",
            "LUNCH_OPEN",
        ) and row.get("label") in (
            "portfolio_blend_train",
            "sleeve_train",
            "F2_ORB_train_2021_2023",
            "F2_ORB_reference_le2024",
        ):
            key = f"{row['sleeve']}::{row['label']}"
            board["highlights"][key] = {
                "ann_sr": row.get("ann_sr_proxy"),
                "scale": row.get("scale"),
                "p_pass_product": row.get("p_pass_product"),
                "p_survive": row.get("p_survive"),
                "net_ev_monthly": row.get("net_ev_monthly"),
            }
    for name, block in sizing.items():
        be = block["grid"].get("best_net_ev_within_4pct")
        bs = block["grid"].get("best_survive_given_pass035_evpos")
        board["highlights"][f"sizing::{name}"] = {
            "recommend_scale": block["recommend_scale"]["scale"],
            "recommend_ev": block["recommend_scale"]["net_ev_monthly"],
            "best_ev_scale": None if not be else be["scale"],
            "best_ev": None if not be else be["net_ev_monthly"],
            "best_survive_scale": None if not bs else bs["scale"],
            "best_survive": None if not bs else bs["p_survive"],
        }
    OUT_BOARD.write_text(json.dumps(board, indent=2) + "\n", encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_MD)
    print("Wrote", OUT_BOARD)
    print("corrs", {k: (None if v is None else round(v, 3)) for k, v in corrs.items()})
    for row in rows:
        if "error" in row:
            continue
        if row["label"] in (
            "portfolio_blend_train",
            "sleeve_train",
            "F2_ORB_train_2021_2023",
            "F2_ORB_reference_le2024",
            "portfolio_blend_train_cost_stress50_btc",
        ):
            print(
                f"{row['sleeve']:32s} {row['label'][:30]:30s} "
                f"SR={row.get('ann_sr_proxy') and round(row['ann_sr_proxy'],2)} "
                f"EV={row['net_ev_monthly']:.0f} "
                f"p1p2={row['p_pass_product']:.3f} "
                f"surv={row['p_survive']:.3f} scale={row['scale']:.2f}"
            )


if __name__ == "__main__":
    main()
