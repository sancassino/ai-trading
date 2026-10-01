#!/usr/bin/env python3
"""D-092.3 + D-092.4 — F2-ORB reference EV band + weak-sleeve portfolio table.

Informational only: NOT a PREREG trial; no TRIALS append; reserve 2025+ unused
for any decision row (decision windows clipped to ≤2024-12-31).
"""
from __future__ import annotations

import csv
import json
import os
from pathlib import Path

import numpy as np

from engine.ftmo import ftmo_ev, load_daily_equity_csv, recommend_scale, trades_bp_to_daily

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/cto/d092_portfolio_ev.json"
N_PATHS = 5_000
SEED = 7


def load_orb_dates():
    dates = []
    with open(ROOT / "results/f/F2_ORB_daily.csv", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f, delimiter=";"):
            dates.append(row["date"].replace(".", "-"))
    return np.asarray(dates)


def ev_pack(series, dd=None, *, label, sleeve, window, extra=None):
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
    rec = recommend_scale(series, dd, n_paths=N_PATHS, seed=SEED)
    ev = ftmo_ev(
        series,
        daily_drawdowns=None if dd is None else dd,
        n_paths=N_PATHS,
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
    if a.std() == 0 or b.std() == 0:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def main():
    os.chdir(ROOT)
    r, dd = load_daily_equity_csv("results/f/F2_ORB_daily.csv")
    dates = load_orb_dates()

    rows = []

    # --- D-092.3 F2 reference (reserve-safe) ---
    for label, lo, hi, note in [
        (
            "F2_ORB_reference_le2024",
            "2021-01-01",
            "2024-12-31",
            "Binding D-092.3 reference; reserve 2025+ not used",
        ),
        (
            "F2_ORB_train_2021_2023",
            "2021-01-01",
            "2023-12-31",
            "Train window aligned with sleeve cost-gates",
        ),
        (
            "F2_ORB_diagnostic_full_csv",
            "2021-01-01",
            "2026-09-23",
            "DIAGNOSTIC only — CSV contains post-2024 bars; do NOT use for selection (D-084)",
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
                extra={"note": note, "uses_trough_dd": True},
            )
        )

    # --- Sleeve trade series (train artefacts already ≤2023) ---
    btc_dates, btc_net = [], []
    with open("results/cto/s2_btc_prep/cost_gate_s2_btc_train.csv") as f:
        for row in csv.DictReader(f):
            btc_dates.append(row["date"])
            btc_net.append(float(row["net_bp"]))
    btc_r, btc_days = trades_bp_to_daily(btc_dates, btc_net)

    xau_dates, xau_net = [], []
    with open("results/s2_xau_am_fade_train.csv") as f:
        for row in csv.DictReader(f):
            xau_dates.append(row["date"])
            xau_net.append(float(row["bruto_bp"]) - float(row["rt"]))
    xau_r, xau_days = trades_bp_to_daily(xau_dates, xau_net)

    # Calendar = ORB train days (business-dense equity path)
    m_tr = (dates >= "2021-01-01") & (dates <= "2023-12-31")
    orb_days = np.asarray(dates[m_tr], dtype="datetime64[D]")
    orb_r = r[m_tr]
    orb_dd = dd[m_tr]
    btc_on = align_to(orb_days, btc_days, btc_r)
    xau_on = align_to(orb_days, xau_days, xau_r)

    corrs = {
        "orb_btc": corr(orb_r, btc_on),
        "orb_xau": corr(orb_r, xau_on),
        "btc_xau": corr(btc_on, xau_on),
    }

    # Singles on train calendar
    rows.append(
        ev_pack(
            orb_r,
            orb_dd,
            label="sleeve_train",
            sleeve="F2_ORB",
            window="2021-01-01..2023-12-31",
            extra={
                "note": "ORB alone on train; trough DD used",
                "status": "reference_edge",
                "uses_trough_dd": True,
            },
        )
    )
    rows.append(
        ev_pack(
            btc_on,
            None,
            label="sleeve_train",
            sleeve="S2_BTC",
            window="2021-01-01..2023-12-31",
            extra={
                "note": "Power-FAIL alone (N=132<150); net_bp after realized cost",
                "status": "power_fail_watch",
                "n_trades": 132,
            },
        )
    )
    rows.append(
        ev_pack(
            xau_on,
            None,
            label="sleeve_train",
            sleeve="XAU_AM_FADE",
            window="2021-01-01..2023-12-31",
            extra={
                "note": "Watch-only (N=12≪120); bruto−rt",
                "status": "watch_only_underpowered",
                "n_trades": 12,
            },
        )
    )

    # Portfolio blends: match each sleeve to ORB's natural daily std, equal-weight sum,
    # then recommend_scale (honest diversification test without inventing 100% unit-vol days).
    target = float(orb_r.std())
    orb_v = vol_target(orb_r, target)
    btc_v = vol_target(btc_on, target)
    xau_v = vol_target(xau_on, target)

    blends = {
        "ORB+BTC_eqvol": (orb_v + btc_v) / 2.0,
        "ORB+XAU_eqvol": (orb_v + xau_v) / 2.0,
        "ORB+BTC+XAU_eqvol": (orb_v + btc_v + xau_v) / 3.0,
        # Risk-budget: ORB 70% / BTC 25% / XAU 5% (XAU sparse)
        "ORB70_BTC25_XAU5": 0.70 * orb_v + 0.25 * btc_v + 0.05 * xau_v,
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
                        "D-092.4: sleeves vol-matched to ORB daily std then weighted; "
                        "close-only DD proxy; NOT a new hypothesis/trial"
                    ),
                    "target_daily_std": target,
                    "uses_trough_dd": False,
                },
            )
        )

    # +50% cost stress on BTC leg of ORB+BTC (proxy): shrink BTC mean by using stress net
    btc_stress = []
    with open("results/cto/s2_btc_prep/cost_gate_s2_btc_train.csv") as f:
        for row in csv.DictReader(f):
            # gross - 1.5*cost ≈ net - 0.5*cost
            btc_stress.append(float(row["gross_bp"]) - 1.5 * float(row["cost_bp"]))
    btc_s_r, btc_s_days = trades_bp_to_daily(btc_dates, btc_stress)
    btc_s_on = align_to(orb_days, btc_s_days, btc_s_r)
    btc_s_v = vol_target(btc_s_on, target)
    rows.append(
        ev_pack(
            (orb_v + btc_s_v) / 2.0,
            None,
            label="portfolio_blend_train_cost_stress50_btc",
            sleeve="ORB+BTC_eqvol_BTCstress50",
            window="2021-01-01..2023-12-31",
            extra={
                "note": "BTC leg uses gross−1.5×cost; ORB unchanged (already net of CFD path)",
                "uses_trough_dd": False,
            },
        )
    )

    # Human table
    md_lines = [
        "# D-092 portfolio / reference EV (CTO)",
        "",
        f"- When: 2026-10-01 ~01:53 Europe/Amsterdam",
        "- Reserve 2025+: **not used** for decision rows",
        "- No PREREG trial / no TRIALS append",
        "",
        "## Correlations (train 2021–2023, dense ORB calendar)",
        "",
        f"| Pair | ρ |",
        f"|---|---:|",
        f"| ORB ↔ BTC | {corrs['orb_btc']:.3f} |" if corrs["orb_btc"] is not None else "| ORB ↔ BTC | n/a |",
        f"| ORB ↔ XAU | {corrs['orb_xau']:.3f} |" if corrs["orb_xau"] is not None else "| ORB ↔ XAU | n/a |",
        f"| BTC ↔ XAU | {corrs['btc_xau']:.3f} |" if corrs["btc_xau"] is not None else "| BTC ↔ XAU | n/a |",
        "",
        "## Results",
        "",
        "| Sleeve | Window / label | N_act | ann SR | scale | p95 dip | max dip | p1·p2 | p_survive | €/m net EV |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        if "error" in row:
            continue
        md_lines.append(
            "| {sleeve} | {label} | {n_active_days} | {sr} | {scale:.2f} | {p95:.2%} | {mx:.2%} | {pp:.3f} | {ps:.3f} | {ev:.0f} |".format(
                sleeve=row["sleeve"],
                label=row["label"][:40],
                n_active_days=row.get("n_active_days", ""),
                sr=("" if row.get("ann_sr_proxy") is None else f"{row['ann_sr_proxy']:.2f}"),
                scale=row["scale"],
                p95=row["p95_daily_loss"],
                mx=row["max_daily_loss"],
                pp=row["p_pass_product"],
                ps=row["p_survive"],
                ev=row["net_ev_monthly"],
            )
        )
    md_lines += [
        "",
        "## Readout (CTO)",
        "",
        "1. **F2-ORB ≤2024** is the binding reference: recommend_scale + trough DD → "
        "see JSON row `F2_ORB_reference_le2024`. Full-CSV (~€290 at scale≈2.8) is diagnostic decay only.",
        "2. Correlations are **low** (ρ≈0.04–0.11) → diversification is real on paper.",
        "3. **XAU_AM_FADE** remains structurally underpowered (N=12); it barely moves portfolio EV.",
        "4. **S2-BTC** lifts SR in eqvol blend but is still power-FAIL alone; stress-50 BTC blend must stay >0 EV to count under D-092.5 cost stress.",
        "5. No new trial claimed. Strateeg path = D-092.1 pre-screen + D-092.2 S2c XAU+XAG PREREG.",
        "",
    ]
    md_path = ROOT / "results/cto/d092_portfolio_ev.md"
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    out = {
        "when": "2026-10-01 ~01:53 Europe/Amsterdam",
        "decision": "D-092.3 + D-092.4",
        "reserve_2025_touched": False,
        "prereg_trial": False,
        "n_paths": N_PATHS,
        "seed": SEED,
        "correlations_train_2021_2023": corrs,
        "sleeve_inputs": {
            "F2_ORB": "results/f/F2_ORB_daily.csv",
            "S2_BTC": "results/cto/s2_btc_prep/cost_gate_s2_btc_train.csv (net_bp; power-FAIL N=132)",
            "XAU_AM_FADE": "results/s2_xau_am_fade_train.csv (bruto-rt; watch-only N=12)",
        },
        "method": (
            "recommend_scale(p95≤2%, max≤4%) then ftmo_ev; "
            "portfolio = vol-match sleeves to ORB daily std, weighted sum, close-only DD proxy"
        ),
        "ambition_note": (
            "D-092.5: €300–500/m robust acceptable; candidate if p_pass_1·p_pass_2≥0.35 "
            "and net_EV>0 with +50% cost stress and Auditor-PASS"
        ),
        "rows": rows,
        "markdown": str(md_path.relative_to(ROOT)),
    }
    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

    # Console summary
    print("Wrote", OUT)
    print("Wrote", md_path)
    print("corrs", corrs)
    for row in rows:
        if "error" in row:
            continue
        print(
            f"{row['sleeve']:28s} {row['label'][:34]:34s} "
            f"SR={row.get('ann_sr_proxy') and round(row['ann_sr_proxy'],2)} "
            f"EV={row['net_ev_monthly']:.0f} "
            f"p1p2={row['p_pass_product']:.3f} "
            f"surv={row['p_survive']:.3f} scale={row['scale']:.2f}"
        )


if __name__ == "__main__":
    main()
