#!/usr/bin/env python3
"""C-020 — D-096 / PREREG_FTMO_P1_ORB_BTC stap 2: ONE-SHOT reserve run.

Binding:
  - Scales frozen from train 2021-01-01 .. 2023-12-31 only (eqvol + recommend_scale)
  - Reserve window: 2025-01-01 → data end (one look; no re-estimate)
  - Max daily loss cap 4% of initial via frozen recommend_scale
  - PASS iff all PREREG §3 criteria hold (Auditor independent PASS still required)
  - Appends TRIALS / bumps TRIAL_COUNT regardless of outcome
"""
from __future__ import annotations

import csv
import gzip
import json
import os
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np

from engine.ftmo import ftmo_ev, load_daily_equity_csv, recommend_scale, trades_bp_to_daily

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/cto/p1_reserve"
SCALES_PATH = ROOT / "results/cto/p1_scales.json"
TRIALS_PATH = ROOT / "catalogus/TRIALS.csv"
TRIAL_COUNT_PATH = ROOT / "TRIAL_COUNT.md"

NY = ZoneInfo("America/New_York")
CET = ZoneInfo("Europe/Amsterdam")
BTC = "BTCUSD"
US100 = "US100cash"
COMM_BP_SIDE = 0.20
RANGE_MIN, RANGE_MAX, GAP_MIN = 0.0020, 0.0150, 0.0015
TRAIN_START, TRAIN_END = date(2021, 1, 1), date(2023, 12, 31)
RESERVE_START = date(2025, 1, 1)
SEED = 7
N_PATHS = 8_000
WHEN = "2026-10-01 ~08:57 Europe/Amsterdam (CEST / UTC+2)"


def server_to_cet(server: datetime) -> datetime:
    return (server - timedelta(hours=7)).replace(tzinfo=NY).astimezone(CET)


def load_gz(sym: str, *, lo: date | None = None, hi: date | None = None):
    point = None
    bars = []
    path = ROOT / f"data/m5gz/{sym}.csv.gz"
    for line in gzip.open(path, "rt"):
        if line.startswith("#"):
            point = float(line.split("point=")[1].split(";")[0])
            continue
        if not line or not line[0].isdigit():
            continue
        t, o, h, l, c, sp = line.rstrip().split(";")
        server = datetime.strptime(t, "%Y.%m.%d %H:%M")
        local = server_to_cet(server)
        d = local.date()
        if lo and d < lo:
            continue
        if hi and d > hi:
            continue
        bars.append(
            {
                "local": local,
                "o": float(o),
                "h": float(h),
                "l": float(l),
                "c": float(c),
                "spread": int(sp) * point,
            }
        )
    return bars


def us100_cash_gap(by_day_us, d: date):
    priors = sorted(x for x in by_day_us if x < d)
    if not priors:
        return None
    prev_bars = sorted(by_day_us[priors[-1]], key=lambda b: b["local"])
    cash_close = [b for b in prev_bars if b["local"].hour < 22]
    if not cash_close:
        return None
    prev_close = cash_close[-1]["c"]
    day_bars = sorted(by_day_us[d], key=lambda b: b["local"])
    open_bars = [
        b
        for b in day_bars
        if (b["local"].hour == 15 and b["local"].minute >= 30) or b["local"].hour > 15
    ]
    if not open_bars or prev_close <= 0:
        return None
    return open_bars[0]["o"] / prev_close - 1.0


def run_btc(lo: date, hi: date | None = None):
    """Frozen S2-BTC US-open rule (identical logic to U2 s2_btc_cost_gate_train)."""
    load_lo = lo - timedelta(days=14)
    btc = load_gz(BTC, lo=load_lo, hi=hi)
    us = load_gz(US100, lo=load_lo, hi=hi)
    by_btc, by_us = defaultdict(list), defaultdict(list)
    for b in btc:
        by_btc[b["local"].date()].append(b)
    for b in us:
        by_us[b["local"].date()].append(b)

    rows = []
    for d in sorted(by_btc):
        if d < lo:
            continue
        if hi and d > hi:
            continue
        if d not in by_us:
            continue
        gap = us100_cash_gap(by_us, d)
        if gap is None or abs(gap) < GAP_MIN:
            continue
        day_bars = sorted(by_btc[d], key=lambda x: x["local"])
        pre = [
            b
            for b in day_bars
            if (b["local"].hour == 14 and b["local"].minute >= 30)
            or (b["local"].hour == 15 and b["local"].minute < 30)
        ]
        entry_win = [
            b for b in day_bars if b["local"].hour == 15 and b["local"].minute >= 30
        ]
        post_flat = [
            b
            for b in day_bars
            if (b["local"].hour > 15 or (b["local"].hour == 15 and b["local"].minute >= 30))
            and (b["local"].hour < 21 or (b["local"].hour == 21 and b["local"].minute == 0))
        ]
        if len(pre) < 10 or not entry_win:
            continue
        rh = max(b["h"] for b in pre)
        rl = min(b["l"] for b in pre)
        mid = 0.5 * (rh + rl)
        if mid <= 0 or rh <= rl:
            continue
        width = (rh - rl) / mid
        if width < RANGE_MIN or width > RANGE_MAX:
            continue
        trade = None
        hit_up = hit_dn = False
        for b in entry_win:
            up = b["c"] >= rh
            dn = b["c"] <= rl
            hit_up |= up
            hit_dn |= dn
            if hit_up and hit_dn:
                trade = None
                break
            if not (up or dn):
                continue
            side = 1 if up else -1
            if side * gap <= 0:
                break
            entry, stop = b["c"], mid
            seq = [x for x in post_flat if x["local"] >= b["local"]]
            if not seq:
                break
            exit_p = exit_bar = None
            for i, eb in enumerate(seq):
                if i == 0:
                    continue
                if (side > 0 and eb["l"] <= stop) or (side < 0 and eb["h"] >= stop):
                    exit_p, exit_bar = stop, eb
                    break
            if exit_p is None:
                flat = [
                    x for x in seq if x["local"].hour == 21 and x["local"].minute == 0
                ]
                exit_bar = flat[0] if flat else seq[-1]
                exit_p = exit_bar["c"]
            gross = side * (exit_p - entry) / entry
            spread_frac = (b["spread"] / entry) if entry > 0 else 0.0
            comm_frac = 2 * COMM_BP_SIDE * 1e-4
            cost = spread_frac + comm_frac
            cost_stress = 1.5 * spread_frac + comm_frac
            trade = {
                "date": str(d),
                "symbol": BTC,
                "side": side,
                "gap_pct": gap * 100,
                "width_pct": width * 100,
                "entry": entry,
                "exit": exit_p,
                "stop": stop,
                "gross_bp": gross * 1e4,
                "cost_bp": cost * 1e4,
                "cost_stress_bp": cost_stress * 1e4,
                "net_bp": (gross - cost) * 1e4,
                "net_stress_bp": (gross - cost_stress) * 1e4,
                "entry_t": str(b["local"]),
                "exit_t": str(exit_bar["local"]),
            }
            break
        if trade:
            rows.append(trade)
    return rows


def load_orb_series():
    r, dd = load_daily_equity_csv(str(ROOT / "results/f/F2_ORB_daily.csv"))
    dates = []
    with open(ROOT / "results/f/F2_ORB_daily.csv", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f, delimiter=";"):
            dates.append(row["date"].replace(".", "-"))
    return np.asarray(dates), r, dd


def align_to(calendar_days, src_days, src_r):
    out = np.zeros(calendar_days.size, float)
    idx = {str(d): i for i, d in enumerate(calendar_days)}
    for d0, v in zip(src_days, src_r):
        k = str(d0)
        if k in idx:
            out[idx[k]] += float(v)
    return out


def vol_factor(x, target_daily_std):
    s = float(np.std(x))
    if s <= 0:
        return 0.0
    return float(target_daily_std) / s


def day_clustered_t(daily, lags=5):
    """One-sided Newey–West t on daily series (zeros included)."""
    x = np.asarray(daily, float).ravel()
    n = x.size
    if n < 5:
        return None
    mu = float(x.mean())
    xc = x - mu
    gamma0 = float(np.dot(xc, xc) / n)
    nw = gamma0
    for L in range(1, lags + 1):
        w = 1.0 - L / (lags + 1.0)
        cov = float(np.dot(xc[L:], xc[:-L]) / n)
        nw += 2.0 * w * cov
    se = np.sqrt(max(nw, 0.0) / n)
    if se <= 0:
        return None
    return mu / se


def pack_ev(series, *, scale=1.0, n_paths=N_PATHS):
    series = np.asarray(series, float).ravel()
    r = series * float(scale)
    loss = np.maximum(0.0, -r)
    ev = ftmo_ev(series, n_paths=n_paths, scale=float(scale), seed=SEED)
    return {
        "scale": float(scale),
        "p95_daily_loss": float(np.quantile(loss, 0.95)) if loss.size else 0.0,
        "max_daily_loss": float(loss.max()) if loss.size else 0.0,
        "p_pass_1": float(ev["p_pass_1"]),
        "p_pass_2": float(ev["p_pass_2"]),
        "p_pass_product": float(ev["p_pass_1"] * ev["p_pass_2"]),
        "p_survive": float(ev["p_survive"]),
        "net_ev_monthly": float(ev["net_ev_monthly"]),
        "exp_payout_monthly": float(ev["exp_payout_monthly"]),
        "attempts_mean": float(ev["attempts_mean"]),
    }


def series_stats(x):
    x = np.asarray(x, float)
    std = float(x.std())
    return {
        "n_days": int(x.size),
        "n_active": int((x != 0).sum()),
        "mean": float(x.mean()),
        "std": std,
        "ann_sr": float(x.mean() / std * np.sqrt(252.0)) if std > 0 else None,
        "skew": float(((x - x.mean()) ** 3).mean() / (std ** 3)) if std > 0 else None,
    }


def append_trials(verdict: str, summary: dict):
    """Append-only catalogus/TRIALS.csv + TRIAL_COUNT.md bump 447→448."""
    t_str = summary.get("day_clust_t")
    t_fmt = f"{t_str:.2f}" if isinstance(t_str, (int, float)) else ""
    sr = summary["port_stats"]["ann_sr"]
    sr_fmt = f"{sr:.3f}" if sr is not None else ""
    beslissing = (
        f"{verdict}: P1 ORB+BTC reserve one-shot (D-096); "
        f"mean={summary['port_stats']['mean']:.6g} t_NW5={t_fmt} "
        f"SR={sr_fmt} p1p2={summary['ftmo_ev']['p_pass_product']:.3f} "
        f"EV€/m={summary['ftmo_ev']['net_ev_monthly']:.1f} "
        f"legs A_mean={summary['leg_A_stats']['mean']:.6g} "
        f"B_mean={summary['leg_B_stats']['mean']:.6g} "
        f"BTC_N={summary['btc_reserve_n_trades']}; "
        f"Auditor pending AUDIT_4; TRIAL_COUNT 448; "
        f"reserve 2025+ consumed for P1 only"
    )
    row = (
        f"2026-10-01;FTMO_P1_ORB_BTC;P1_eqvol_frozen;"
        f"FTMO M5 ORB(F2)+BTCUSOPEN reserve2025-01→2026-09 (PREREG_FTMO_P1_ORB_BTC / D-096);"
        f"reserve;{sr_fmt};{t_fmt} NW;;{beslissing}\n"
    )
    with open(TRIALS_PATH, "a", encoding="utf-8") as f:
        f.write(row)

    # bump TRIAL_COUNT.md
    text = TRIAL_COUNT_PATH.read_text(encoding="utf-8")
    if "FTMO_P1_ORB_BTC" not in text:
        text = text.rstrip() + (
            "\n| 2026-10-01 | P1/PREREG_FTMO_P1_ORB_BTC: ORB+BTC eqvol reserve one-shot "
            f"({verdict}, D-096; 1 variant) | 1 | 448 |\n"
        )
        TRIAL_COUNT_PATH.write_text(text, encoding="utf-8")


def main():
    os.chdir(ROOT)
    OUT.mkdir(parents=True, exist_ok=True)

    # --- 1) Freeze scales from train 2021–2023 ---
    train_csv = ROOT / "results/cto/s2_btc_prep/cost_gate_s2_btc_train.csv"
    btc_train_rows = [
        r
        for r in csv.DictReader(open(train_csv))
        if TRAIN_START.isoformat() <= r["date"] <= TRAIN_END.isoformat()
    ]
    btc_tr_r, btc_tr_days = trades_bp_to_daily(
        [r["date"] for r in btc_train_rows],
        [float(r["net_bp"]) for r in btc_train_rows],
    )

    orb_dates, orb_r_all, orb_dd_all = load_orb_series()
    m_tr = (orb_dates >= "2021-01-01") & (orb_dates <= "2023-12-31")
    orb_days = np.asarray(orb_dates[m_tr], dtype="datetime64[D]")
    orb_r = orb_r_all[m_tr]
    target = float(orb_r.std())
    btc_on_tr = align_to(orb_days, btc_tr_days, btc_tr_r)
    fA_vol = vol_factor(orb_r, target)
    fB_vol = vol_factor(btc_on_tr, target)
    blend_tr = 0.5 * (fA_vol * orb_r + fB_vol * btc_on_tr)
    rec = recommend_scale(blend_tr, None, n_paths=3000, seed=SEED)
    port_scale = float(rec["scale"])
    sA = 0.5 * fA_vol * port_scale
    sB = 0.5 * fB_vol * port_scale

    scales = {
        "when_frozen": WHEN,
        "train_window": "2021-01-01..2023-12-31",
        "method": "eqvol_to_ORB_train_std then recommend_scale; sA/sB absorb 1/2 weights",
        "target_daily_std_orb_train": target,
        "fA_vol": fA_vol,
        "fB_vol": fB_vol,
        "port_recommend_scale": port_scale,
        "recommend_binding": rec["binding"],
        "recommend_p95_daily_loss": float(rec["p95_daily_loss"]),
        "recommend_max_daily_loss": float(rec["max_daily_loss"]),
        "sA": sA,
        "sB": sB,
        "max_daily_loss_cap": 0.04,
        "btc_train_n_trades": len(btc_train_rows),
        "orb_train_n_days": int(orb_r.size),
        "prereg": "PREREG_FTMO_P1_ORB_BTC",
        "besluit": "D-096",
        "note": "Frozen once from train; never re-estimated on reserve.",
    }
    SCALES_PATH.write_text(json.dumps(scales, indent=2) + "\n")

    # --- 2) Reserve BTC (first look) ---
    print("running BTC reserve …", flush=True)
    btc_res_rows = run_btc(RESERVE_START, hi=None)
    with open(OUT / "btc_reserve_trades.csv", "w", newline="") as f:
        if btc_res_rows:
            w = csv.DictWriter(f, fieldnames=list(btc_res_rows[0].keys()))
            w.writeheader()
            w.writerows(btc_res_rows)

    if btc_res_rows:
        btc_res_r, btc_res_days = trades_bp_to_daily(
            [r["date"] for r in btc_res_rows],
            [float(r["net_bp"]) for r in btc_res_rows],
        )
        btc_res_stress_r, _ = trades_bp_to_daily(
            [r["date"] for r in btc_res_rows],
            [float(r["net_stress_bp"]) for r in btc_res_rows],
        )
    else:
        btc_res_r = np.zeros(0)
        btc_res_days = np.asarray([], dtype="datetime64[D]")
        btc_res_stress_r = np.zeros(0)

    m_res = orb_dates >= "2025-01-01"
    orb_res_days = np.asarray(orb_dates[m_res], dtype="datetime64[D]")
    orb_res_r = orb_r_all[m_res]
    btc_on = align_to(orb_res_days, btc_res_days, btc_res_r)
    btc_on_stress = align_to(orb_res_days, btc_res_days, btc_res_stress_r)

    port = sA * orb_res_r + sB * btc_on
    # Stress: BTC +50% spread (realized); ORB ×0.95 conservative cost haircut
    # (F2_ORB daily has no separable cost column; documented proxy).
    port_stress = sA * (orb_res_r * 0.95) + sB * btc_on_stress

    t_port = day_clustered_t(port)
    st_port = series_stats(port)
    st_A = series_stats(orb_res_r)
    st_B = series_stats(btc_on)
    st_stress = series_stats(port_stress)

    print("running ftmo_ev …", flush=True)
    ev = pack_ev(port, scale=1.0)
    ev_stress = pack_ev(port_stress, scale=1.0)

    # Write daily series
    with open(OUT / "p1_reserve_daily.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "date",
                "orb_unit",
                "btc_unit",
                "port",
                "port_stress",
                "sA",
                "sB",
            ]
        )
        for i, d in enumerate(orb_res_days):
            w.writerow(
                [
                    str(d),
                    float(orb_res_r[i]),
                    float(btc_on[i]),
                    float(port[i]),
                    float(port_stress[i]),
                    sA,
                    sB,
                ]
            )

    crit = {
        "net_mean_gt_0": bool(st_port["mean"] > 0),
        "day_clust_t_ge_2": bool(t_port is not None and t_port >= 2.0),
        "ann_sr_ge_0_8": bool(
            st_port["ann_sr"] is not None and st_port["ann_sr"] >= 0.8
        ),
        "p_pass_product_ge_0_35": bool(ev["p_pass_product"] >= 0.35),
        "net_ev_gt_0": bool(ev["net_ev_monthly"] > 0),
        "stress_p_pass_product_ge_0_35": bool(ev_stress["p_pass_product"] >= 0.35),
        "stress_net_ev_gt_0": bool(ev_stress["net_ev_monthly"] > 0),
        "leg_A_mean_ge_0": bool(st_A["mean"] >= 0),
        "leg_B_mean_ge_0": bool(st_B["mean"] >= 0),
        "auditor_independent_pass": None,
    }
    cto_keys = [k for k in crit if k != "auditor_independent_pass"]
    cto_pass = all(crit[k] for k in cto_keys)
    if cto_pass:
        verdict = "PASS_MECHANICAL_PENDING_AUDITOR"
    else:
        verdict = "FAIL"

    years = {}
    for y in sorted({str(d)[:4] for d in orb_res_days}):
        mask = np.array([str(d).startswith(y) for d in orb_res_days])
        years[y] = {
            "n_days": int(mask.sum()),
            "port_mean": float(port[mask].mean()) if mask.any() else None,
            "orb_mean": float(orb_res_r[mask].mean()) if mask.any() else None,
            "btc_mean": float(btc_on[mask].mean()) if mask.any() else None,
            "btc_n_trades": int(
                sum(1 for r in btc_res_rows if r["date"].startswith(y))
            ),
        }

    summary = {
        "when": WHEN,
        "deliverable": "C-020 P1 ORB+BTC reserve one-shot (D-096)",
        "prereg": "PREREG_FTMO_P1_ORB_BTC",
        "besluit": "D-096",
        "reserve_window": (
            "2025-01-01.." + (str(orb_res_days[-1]) if orb_res_days.size else "NA")
        ),
        "reserve_2025_touched": True,
        "scales_path": str(SCALES_PATH.relative_to(ROOT)),
        "scales": scales,
        "btc_reserve_n_trades": len(btc_res_rows),
        "btc_reserve_mean_gross_bp": (
            float(np.mean([r["gross_bp"] for r in btc_res_rows])) if btc_res_rows else None
        ),
        "btc_reserve_mean_net_bp": (
            float(np.mean([r["net_bp"] for r in btc_res_rows])) if btc_res_rows else None
        ),
        "orb_reserve_n_days": int(orb_res_r.size),
        "port_stats": st_port,
        "leg_A_stats": st_A,
        "leg_B_stats": st_B,
        "stress_stats": st_stress,
        "day_clust_t": t_port,
        "ftmo_ev": ev,
        "ftmo_ev_stress": ev_stress,
        "criteria": crit,
        "failed_criteria": [k for k in cto_keys if not crit[k]],
        "cto_mechanical_pass": cto_pass,
        "verdict": verdict,
        "year_split": years,
        "trial_count_after": 448,
        "note": (
            "One-shot reserve; scales frozen on train 2021-23; "
            "Auditor must file AUDIT_4 independently. Agents do not buy FTMO."
        ),
        "stress_method": (
            "BTC leg uses +50% spread (net_stress_bp); "
            "ORB leg x0.95 proxy (no separable cost in F2_ORB_daily)."
        ),
    }

    (OUT / 'p1_reserve_summary.json').write_text(
        json.dumps(summary, indent=2) + chr(10)
    )

    md_lines = []
    md_lines.append("# C-020 — P1 ORB+BTC reserve one-shot (D-096)")
    md_lines.append("")
    md_lines.append("**When:** " + WHEN)
    md_lines.append("**Verdict (CTO mechanical):** **" + verdict + "**")
    md_lines.append("**Auditor:** pending `AUDIT_4.md` (required for full PASS).")
    md_lines.append("")
    md_lines.append("## Scales (frozen train 2021-2023)")
    md_lines.append(
        "- sA=%.6g  sB=%.6g  port_recommend_scale=%.4f" % (sA, sB, port_scale)
    )
    md_lines.append(
        "- target_daily_std(ORB train)=%.6g  fB_vol=%.4f" % (target, fB_vol)
    )
    md_lines.append(
        "- max daily loss (train recommend)=%.4f (cap 0.04)" % rec["max_daily_loss"]
    )
    md_lines.append("")
    md_lines.append("## Reserve window")
    md_lines.append(
        "- %s  (ORB days=%d, BTC trades=%d)"
        % (summary["reserve_window"], st_port["n_days"], len(btc_res_rows))
    )
    md_lines.append("")
    md_lines.append("## Combined series (after frozen sA/sB)")
    md_lines.append(
        "- mean=%.6g  ann_SR=%s" % (st_port["mean"], st_port["ann_sr"])
    )
    md_lines.append("- day-clustered t (NW-L5)=%s" % t_port)
    md_lines.append(
        "- ftmo_ev: p1*p2=%.4f  net_EV_eur/m=%.1f  p_surv=%.3f"
        % (ev["p_pass_product"], ev["net_ev_monthly"], ev["p_survive"])
    )
    md_lines.append(
        "- stress: p1*p2=%.4f  net_EV_eur/m=%.1f"
        % (ev_stress["p_pass_product"], ev_stress["net_ev_monthly"])
    )
    md_lines.append("")
    md_lines.append("## Legs (unit, before sA/sB)")
    md_lines.append(
        "- ORB mean=%.6g  SR=%s" % (st_A["mean"], st_A["ann_sr"])
    )
    md_lines.append(
        "- BTC mean=%.6g  SR=%s  (active days=%d)"
        % (st_B["mean"], st_B["ann_sr"], st_B["n_active"])
    )
    md_lines.append("")
    md_lines.append("## Criteria")
    for k, v in crit.items():
        md_lines.append("- `%s`: %s" % (k, v))
    if summary["failed_criteria"]:
        md_lines.append("")
        md_lines.append("**Failed:** " + ", ".join(summary["failed_criteria"]))
    md_lines.append("")
    md_lines.append("## Year split (informative)")
    md_lines.append("| Year | port mean | ORB mean | BTC mean | BTC N |")
    md_lines.append("|---|---:|---:|---:|---:|")
    for y, info in years.items():
        md_lines.append(
            "| %s | %s | %s | %s | %s |"
            % (
                y,
                info["port_mean"],
                info["orb_mean"],
                info["btc_mean"],
                info["btc_n_trades"],
            )
        )
    md_lines.append("")
    md_lines.append("## Integrity")
    md_lines.append("- PREREG before this result: `PREREG_FTMO_P1_ORB_BTC.md`")
    md_lines.append("- BESLUITEN D-096 reserve vrijgave for P1 only")
    md_lines.append("- TRIAL_COUNT 447 -> 448 (append-only)")
    md_lines.append("- No FTMO signup / no fee spend by agents")
    md_lines.append("")
    (OUT / "p1_reserve_summary.md").write_text(chr(10).join(md_lines) + chr(10))

    board = {
        "cycle": "C-020",
        "when": WHEN,
        "verdict": verdict,
        "cto_mechanical_pass": cto_pass,
        "failed": summary["failed_criteria"],
        "trial_count": 448,
        "next": "Auditor AUDIT_4; CEO advice to Sandro only if full PASS",
    }
    (OUT / "c020_board.json").write_text(json.dumps(board, indent=2) + chr(10))

    append_trials(verdict, summary)
    print(
        json.dumps(
            {
                "verdict": verdict,
                "failed": summary["failed_criteria"],
                "t": t_port,
                "sr": st_port["ann_sr"],
                "p1p2": ev["p_pass_product"],
                "ev": ev["net_ev_monthly"],
                "btc_n": len(btc_res_rows),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

