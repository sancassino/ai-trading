#!/usr/bin/env python3
"""C-021 — D-097 track-5: low-turnover / high-bruto FTMO target grids (CTO).

Diagnostic design table only — NOT a PREREG trial.
- Reserve 2025+: untouched
- No TRIALS.csv append
- Synthetic trade calendars on 2020-01-01 .. 2024-12-31 (≤5y FTMO-style window;
  D-094a proxy ≥10y is Strateeg's discovery job; this grid sizes the *target*)

Purpose: give Strateeg/S2 numeric bars for D-097.1 sleeves
(swing hold 3–20d, bruto 50–300 bp/trade, cost 1–10 bp + swap).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

from engine.ftmo import ftmo_ev, recommend_scale, trades_bp_to_daily

OUT = Path("results/cto/c021_d097_low_turnover")
SEED = 21
N_PATHS = 2500
HORIZON = 504
ACCOUNT = 80_000.0
FEE = 540.0

# Calendar for synthetic trades (no 2025+)
CAL_START = np.datetime64("2020-01-02")
CAL_END = np.datetime64("2024-12-31")


def _busdays(start, end):
    return np.busday_count(start, end + np.timedelta64(1, "D"))


def synth_trades(
    trades_per_year: float,
    mean_net_bp: float,
    hold_days: int,
    hit_rate: float,
    bp_vol: float,
    rng: np.random.Generator,
):
    """Sparse signed net-bp trades over CAL_START..CAL_END.

    Mean net_bp already includes RT+swap (Strateeg must clear cost gate separately).
    Hold_days used only to annotate / estimate overnight nights ≈ hold-1.
    """
    n_years = (CAL_END - CAL_START).astype(int) / 365.25
    n_trades = max(8, int(round(trades_per_year * n_years)))
    # Place trades on business days
    all_bd = np.busday_offset(CAL_START, np.arange(0, _busdays(CAL_START, CAL_END)))
    if all_bd.size < n_trades:
        n_trades = all_bd.size
    idx = np.sort(rng.choice(all_bd.size, size=n_trades, replace=False))
    dates = all_bd[idx]
    # Two-point distribution for skew control via hit_rate
    # E[bp] = hit*win + (1-hit)*(-loss) = mean_net_bp; set win/loss with fixed ratio
    # win = mean / (2*hit-1) style — use magnitude around mean
    if hit_rate <= 0.5:
        # force mild edge via small win>loss asymmetry on mean
        hit_rate = 0.55
    # Solve: h*W + (1-h)*(-L) = m, and W+L = 2*amp → use amp = |m| + bp_vol
    amp = abs(mean_net_bp) + max(bp_vol, 1.0)
    # h*W - (1-h)*L = m; W = L + delta. Simpler: wins = mean/hit_rate * k
    win = mean_net_bp / hit_rate + amp * (1 - hit_rate)
    loss = (win * hit_rate - mean_net_bp) / (1 - hit_rate)
    signs = rng.random(n_trades) < hit_rate
    bp = np.where(signs, win, -loss).astype(float)
    # add noise
    bp = bp + rng.normal(0.0, bp_vol, size=n_trades)
    # re-center to exact mean_net_bp (design table, not mining)
    bp = bp - bp.mean() + mean_net_bp
    return dates, bp, {
        "n_trades": int(n_trades),
        "n_years": float(n_years),
        "hold_days": int(hold_days),
        "nights_est": int(max(0, hold_days - 1)),
        "hit_rate_design": float(hit_rate),
        "win_bp_design": float(win),
        "loss_bp_design": float(loss),
    }


def day_clust_t(rets: np.ndarray, lag: int = 5) -> float:
    """Newey-West t on daily returns (same spirit as C-020 NW-L5)."""
    x = np.asarray(rets, float).ravel()
    n = x.size
    if n < lag + 5:
        return float("nan")
    mu = x.mean()
    xc = x - mu
    gamma0 = float(np.dot(xc, xc) / n)
    var = gamma0
    for L in range(1, lag + 1):
        w = 1.0 - L / (lag + 1.0)
        cov = float(np.dot(xc[L:], xc[:-L]) / n)
        var += 2.0 * w * cov
    se = math.sqrt(max(var, 1e-18) / n)
    return float(mu / se) if se > 0 else float("nan")


def ann_sr(rets: np.ndarray) -> float:
    x = np.asarray(rets, float)
    if x.std() <= 0:
        return 0.0
    return float(x.mean() / x.std() * math.sqrt(252))


def eval_cfg(cfg: dict, rng: np.random.Generator) -> dict:
    dates, bp, meta = synth_trades(
        cfg["trades_per_year"],
        cfg["mean_net_bp"],
        cfg["hold_days"],
        cfg["hit_rate"],
        cfg["bp_vol"],
        rng,
    )
    rets, _ = trades_bp_to_daily(dates, bp)
    # Active (non-zero) days for power note
    n_act = int((np.abs(rets) > 0).sum())
    t = day_clust_t(rets)
    sr = ann_sr(rets)
    skew = float(pd.Series(rets).skew()) if rets.size > 3 else 0.0
    rec = recommend_scale(
        rets,
        n_paths=N_PATHS,
        horizon=HORIZON,
        seed=int(rng.integers(1, 10_000)),
        max_daily_loss_cap=0.04,
        p95_daily_loss=0.02,
    )
    # Also flat scale=1 EV for reference
    ev1 = ftmo_ev(
        rets,
        fee=FEE,
        account=ACCOUNT,
        n_paths=N_PATHS,
        horizon=HORIZON,
        scale=1.0,
        seed=int(rng.integers(1, 10_000)),
    )
    row = {
        **cfg,
        **meta,
        "n_active_days": n_act,
        "mean_daily": float(rets.mean()),
        "day_clust_t_NW5": t,
        "ann_sr": sr,
        "skew_daily": skew,
        "t_ge_2": bool(t >= 2.0) if t == t else False,
        "sr_ge_0_8": bool(sr >= 0.8),
        "rec_scale": rec["scale"],
        "rec_binding": rec["binding"],
        "rec_p95": rec["p95_daily_loss"],
        "rec_max": rec["max_daily_loss"],
        "rec_p_pass_2": rec["p_pass_2"],
        "rec_p_survive": rec["p_survive"],
        "rec_net_ev_m": rec["net_ev_monthly"],
        "rec_p1p2": float(rec["p_pass_2"]),  # recommend_scale returns p_pass_2; approximate product via ev
        "scale1_net_ev_m": ev1["net_ev_monthly"],
        "scale1_p_pass_1": ev1["p_pass_1"],
        "scale1_p_pass_2": ev1["p_pass_2"],
        "scale1_p1p2": float(ev1["p_pass_1"] * ev1["p_pass_2"]),
        "scale1_p_survive": ev1["p_survive"],
    }
    # full p1·p2 at recommend_scale
    ev_rec = ftmo_ev(
        rets,
        fee=FEE,
        account=ACCOUNT,
        n_paths=N_PATHS,
        horizon=HORIZON,
        scale=rec["scale"],
        seed=7,
    )
    row["rec_p1p2"] = float(ev_rec["p_pass_1"] * ev_rec["p_pass_2"])
    row["rec_p_survive"] = float(ev_rec["p_survive"])
    row["rec_net_ev_m"] = float(ev_rec["net_ev_monthly"])
    row["clears_ev300"] = bool(row["rec_net_ev_m"] >= 300 and row["rec_p1p2"] >= 0.35)
    row["clears_ev500"] = bool(row["rec_net_ev_m"] >= 500 and row["rec_p1p2"] >= 0.35)
    row["clears_ev800"] = bool(row["rec_net_ev_m"] >= 800 and row["rec_p1p2"] >= 0.35)
    row["formal_stat_ok"] = bool(row["t_ge_2"] and row["sr_ge_0_8"])
    return row


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)

    # Grid: D-097.1 ranges
    trades_per_year = [12, 24, 36, 52, 78]  # ~monthly → ~1.5/week
    mean_net_bp = [20, 40, 60, 80, 100, 150, 200, 300]  # after costs
    hold_days = [3, 5, 10, 20]
    # Keep hit_rate / vol fixed for design clarity (Strateeg varies mechanism)
    hit_rate = 0.58
    bp_vol = 40.0

    rows = []
    # Full factorial would be huge; sample hold as outer with subset of others
    # Priority slice: for each (trades, mean_net) use hold=5 and hold=10 (core swing)
    for tpy in trades_per_year:
        for mbp in mean_net_bp:
            for hd in (5, 10):
                cfg = {
                    "trades_per_year": tpy,
                    "mean_net_bp": mbp,
                    "hold_days": hd,
                    "hit_rate": hit_rate,
                    "bp_vol": bp_vol,
                    "slice": "core_swing",
                }
                rows.append(eval_cfg(cfg, rng))

    # Extra: hold 3 and 20 at mid-frequency for horizon sensitivity
    for hd in (3, 20):
        for tpy in (24, 52):
            for mbp in (60, 100, 150):
                cfg = {
                    "trades_per_year": tpy,
                    "mean_net_bp": mbp,
                    "hold_days": hd,
                    "hit_rate": hit_rate,
                    "bp_vol": bp_vol,
                    "slice": "hold_sensitivity",
                }
                rows.append(eval_cfg(cfg, rng))

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "target_grid.csv", index=False)

    # Minimal bars: smallest mean_net_bp that clears each EV tier with t≥2 & SR≥0.8
    # at each trades_per_year (core_swing hold=5 preferred)
    summaries = []
    core = df[df["slice"] == "core_swing"]
    for tpy in trades_per_year:
        sub = core[(core["trades_per_year"] == tpy) & (core["hold_days"] == 5)].sort_values(
            "mean_net_bp"
        )
        for tier, col in [("ev300", "clears_ev300"), ("ev500", "clears_ev500"), ("ev800", "clears_ev800")]:
            ok = sub[sub[col] & sub["formal_stat_ok"]]
            if len(ok):
                r = ok.iloc[0]
                summaries.append(
                    {
                        "trades_per_year": tpy,
                        "hold_days": 5,
                        "tier": tier,
                        "min_mean_net_bp": float(r["mean_net_bp"]),
                        "ann_sr": float(r["ann_sr"]),
                        "day_clust_t_NW5": float(r["day_clust_t_NW5"]),
                        "rec_net_ev_m": float(r["rec_net_ev_m"]),
                        "rec_p1p2": float(r["rec_p1p2"]),
                        "rec_p_survive": float(r["rec_p_survive"]),
                        "rec_scale": float(r["rec_scale"]),
                        "n_trades": int(r["n_trades"]),
                    }
                )
            else:
                # best EV among formal_stat_ok, or among all
                pool = sub[sub["formal_stat_ok"]] if sub["formal_stat_ok"].any() else sub
                r = pool.sort_values("rec_net_ev_m", ascending=False).iloc[0]
                summaries.append(
                    {
                        "trades_per_year": tpy,
                        "hold_days": 5,
                        "tier": tier,
                        "min_mean_net_bp": None,
                        "note": "not_cleared_in_grid",
                        "best_mean_net_bp": float(r["mean_net_bp"]),
                        "ann_sr": float(r["ann_sr"]),
                        "day_clust_t_NW5": float(r["day_clust_t_NW5"]),
                        "rec_net_ev_m": float(r["rec_net_ev_m"]),
                        "rec_p1p2": float(r["rec_p1p2"]),
                        "formal_stat_ok": bool(r["formal_stat_ok"]),
                    }
                )

    # Strateeg target brief (binding design intent for D-097.1)
    # Pick practical operating points from grid
    practical = []
    for label, tpy, mbp, hd in [
        ("A_monthly_swing", 12, 150, 10),
        ("B_biweekly_swing", 24, 100, 5),
        ("C_weekly_swing", 52, 80, 5),
        ("D_high_bruto_sparse", 12, 300, 20),
    ]:
        hit = df[
            (df["trades_per_year"] == tpy)
            & (df["mean_net_bp"] == mbp)
            & (df["hold_days"] == hd)
        ]
        if len(hit):
            r = hit.iloc[0].to_dict()
            practical.append({"label": label, **{k: (float(v) if isinstance(v, (float, np.floating)) else v) for k, v in r.items()}})

    board = {
        "cycle": "C-021",
        "when": "2026-10-01 ~09:28 Europe/Amsterdam (CEST / UTC+2)",
        "decision": "D-097",
        "reserve_2025": "untouched",
        "trials_appended": 0,
        "track3_ceiling_combining": "PAUSED — D-097.3: combine only after individual day-clust t≥2.0; supersedes C-018 H-ENS-03 as candidate path",
        "dead_this_cycle": [
            "P1_ORB_BTC (C-020/AUDIT_4 FAIL)",
            "S2_BTC_US_open (D-097.4)",
            "N35 FAIL_T",
            "N36 FAIL_T",
            "N40 FAIL_STRESS",
            "N41 FAIL_T",
            "GBPJPY_EU_MOM FAIL_STRESS",
        ],
        "trial_count_observed_u2": 453,
        "n_paths": N_PATHS,
        "calendar": "2020-01-02..2024-12-31 (no 2025+)",
        "fee": FEE,
        "account": ACCOUNT,
        "grid_rows": int(len(df)),
        "tier_mins_hold5": summaries,
        "practical_targets": practical,
        "strateeg_bars": {
            "pre_screen": "mean bruto ≥ 3×(RT+expected_swap_over_hold) on train; prefer ≥50 bp bruto/trade",
            "formal": "day-clust t≥2.0 both halves; ann SR≥0.8; N_trades ≥ ~60 over ≥5y (or D-094a a/b/c + proxy ≥10y)",
            "ftmo_ambition": "recommend_scale p1·p2≥0.35 and net_EV>0; €300–500 ok if robust (D-092.5); €800 stretch",
            "combine": "NO portfolio until solo formal PASS (D-097.3)",
            "families": "TSMOM commodities/FX/indices; XS-momentum 166; carry/RV L/S-neutral; regime filter ATR% or 200d pre-registered",
        },
    }

    with open(OUT / "c021_board.json", "w") as f:
        json.dump(board, f, indent=2, default=str)
    with open(OUT / "tier_mins.json", "w") as f:
        json.dump(summaries, f, indent=2, default=str)

    # Markdown report
    lines = [
        "# C-021 — D-097 low-turnover FTMO target grid (CTO track 5)",
        "",
        f"- When: 2026-10-01 ~09:28 Europe/Amsterdam (CEST / UTC+2)",
        "- Branch: `grok/cto-1`",
        "- Reserve 2025+: **not used**",
        "- Trials appended: **0** (diagnostic design table)",
        "- Engine: `engine/ftmo.py` recommend_scale + ftmo_ev",
        f"- Synthetic calendar: 2020-01-02 … 2024-12-31; n_paths={N_PATHS}",
        "",
        "## Binding policy shifts (D-097)",
        "",
        "1. **Intraday micro-edges deprioritized** — 0–15 bp bruto dies on costs (P1/N35–N41 pattern).",
        "2. **Target sleeve class:** hold 3–20d, bruto 50–300 bp/trade, cost 1–10 bp + swap explicit.",
        "3. **Track 3 combining PAUSED** until individual day-clust t ≥ 2.0 (no more C-018-style ceiling books as candidates).",
        "4. Dead: P1, S2-BTC US-open, N35, N36, N40, N41, GBPJPY_EU_MOM. No clones.",
        "",
        "## Tier minima (hold=5d core slice; mean **net** bp/trade after costs)",
        "",
        "| trades/yr | tier | min net bp/trade | ann SR | t_NW5 | €/m EV | p1·p2 | note |",
        "|---:|---|---:|---:|---:|---:|---:|---|",
    ]
    for s in summaries:
        if s.get("min_mean_net_bp") is not None:
            lines.append(
                f"| {s['trades_per_year']} | {s['tier']} | **{s['min_mean_net_bp']:.0f}** | "
                f"{s['ann_sr']:.2f} | {s['day_clust_t_NW5']:.2f} | {s['rec_net_ev_m']:.0f} | "
                f"{s['rec_p1p2']:.2f} | cleared |"
            )
        else:
            lines.append(
                f"| {s['trades_per_year']} | {s['tier']} | — | {s['ann_sr']:.2f} | "
                f"{s['day_clust_t_NW5']:.2f} | {s['rec_net_ev_m']:.0f} | {s['rec_p1p2']:.2f} | "
                f"not in grid (best net={s.get('best_mean_net_bp')}) |"
            )

    lines += [
        "",
        "## Practical operating points (for Strateeg PREREG design)",
        "",
        "| label | trades/yr | hold | net bp | t_NW5 | SR | scale | €/m | p1·p2 | formal? |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|:---:|",
    ]
    for p in practical:
        lines.append(
            f"| {p['label']} | {p['trades_per_year']} | {p['hold_days']} | {p['mean_net_bp']} | "
            f"{p['day_clust_t_NW5']:.2f} | {p['ann_sr']:.2f} | {p['rec_scale']:.2f} | "
            f"{p['rec_net_ev_m']:.0f} | {p['rec_p1p2']:.2f} | {'Y' if p['formal_stat_ok'] else 'N'} |"
        )

    lines += [
        "",
        "## Strateeg / S2 bars (actionable)",
        "",
        "- **Pre-screen (free):** mean bruto ≥ 3× (RT + swap×nights); prefer ≥ **50 bp bruto/trade**.",
        "- **Discovery:** ≥10y proxy for mechanism (D-094a b) when FTMO-M5 <5y; freeze rule before FTMO cost gate.",
        "- **Formal:** day-clust t≥2.0 both halves + ann SR≥0.8; no threshold mining on 2021–22-only edges.",
        "- **FTMO:** `recommend_scale` with max daily loss ≤4%; need p1·p2≥0.35 and net_EV>0; €300–500 ok if robust.",
        "- **Combine (CTO track 3):** only after **solo** formal PASS — do not stack FAIL_T sleeves.",
        "- **Families:** commodity/FX/index TSMOM; XS-momentum across 166; carry/RV dollar-neutral; regime filter (ATR%ile or 200d) pre-registered as one rule.",
        "",
        "## CTO next",
        "",
        "- Idle on track-3 blends until a D-097 sleeve clears formal t.",
        "- When U2 lands a gate+stress+t PASS: run track-5 `recommend_scale` + optional solo `ftmo_ev` (still no 2025+ without BESLUITEN).",
        "- Manager: absorb D-097 into NEXT_STEPS (v67 still ends at D-096).",
        "",
        f"Artefacts: `{OUT}/target_grid.csv`, `tier_mins.json`, `c021_board.json`.",
        "",
    ]
    (OUT / "c021_report.md").write_text("\n".join(lines))
    print(f"Wrote {len(df)} rows → {OUT}")
    print(df.groupby(["trades_per_year", "hold_days"])["clears_ev500"].mean())


if __name__ == "__main__":
    main()
