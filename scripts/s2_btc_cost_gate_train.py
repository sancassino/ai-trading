#!/usr/bin/env python3
"""S2-BTC PRE-trial kostenpoort — PREREG_S2_BTC_USOPEN, TRAIN 2021–2023 ONLY.

Loads data/m5gz/{BTCUSD,US100cash}.csv.gz (U-006 v41). Skips 2025→ at load.
Rule (frozen PREREG): pre-range 14:30–15:30 Europe/Amsterdam; entry 15:30–16:00
on M5 close beyond range; skip two-way; range width ∈ [0.20%, 1.50%]; stop = mid;
flat 21:00 same day; max 1/day; US100 cash-gap filter |gap|≥0.15% same sign.
Poort: mean bruto ≥ 2× 1.25 bp AND costs < 50% bruto; +50% spread stress same.
FAIL → STOP; no TRIALS append / no formal trial claim from this script alone.
"""
from __future__ import annotations

import csv
import gzip
import json
from collections import defaultdict
from datetime import datetime, timedelta, date
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np

NY = ZoneInfo("America/New_York")
CET = ZoneInfo("Europe/Amsterdam")
BTC = "BTCUSD"
US100 = "US100cash"
RT_FIXED_BP = 1.25  # COSTS_FTMO_alle roundtrip_intraday
COMM_BP_SIDE = 0.20
TRAIN_START = date(2021, 1, 1)
TRAIN_END = date(2023, 12, 31)
OUT_DIR = Path("results/cto/s2_btc_prep")
RANGE_MIN = 0.0020
RANGE_MAX = 0.0150
GAP_MIN = 0.0015


def server_to_cet(server: datetime) -> datetime:
    return (server - timedelta(hours=7)).replace(tzinfo=NY).astimezone(CET)


def load_gz(sym: str):
    point = None
    bars = []
    path = f"data/m5gz/{sym}.csv.gz"
    for line in gzip.open(path, "rt"):
        if line.startswith("#"):
            point = float(line.split("point=")[1].split(";")[0])
            continue
        if not line or not line[0].isdigit():
            continue
        t, o, h, l, c, sp = line.rstrip().split(";")
        server = datetime.strptime(t, "%Y.%m.%d %H:%M")
        local = server_to_cet(server)
        if local.year >= 2025:
            continue
        if local.year < 2021:
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
    """gap = cash-open / prev cash-close − 1. Cash open ≈ first bar at/after 15:30 CET."""
    # previous calendar days with bars (US100 only trades cash days roughly)
    priors = sorted(x for x in by_day_us if x < d)
    if not priors:
        return None
    prev = priors[-1]
    prev_bars = sorted(by_day_us[prev], key=lambda b: b["local"])
    # prev cash close ≈ last bar with hour < 22 CET (cash session end ~22:00 CET / 16:00 ET)
    cash_close_candidates = [b for b in prev_bars if b["local"].hour < 22]
    if not cash_close_candidates:
        return None
    prev_close = cash_close_candidates[-1]["c"]
    day_bars = sorted(by_day_us[d], key=lambda b: b["local"])
    open_bars = [
        b
        for b in day_bars
        if (b["local"].hour == 15 and b["local"].minute >= 30)
        or b["local"].hour > 15
    ]
    if not open_bars:
        return None
    # first bar at/after 15:30
    cash_open = open_bars[0]["o"]
    if prev_close <= 0:
        return None
    return cash_open / prev_close - 1.0


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    btc = load_gz(BTC)
    us = load_gz(US100)
    print(f"loaded BTC bars={len(btc)} US100 bars={len(us)} (2021–2024; 2025+ skipped)")
    by_btc = defaultdict(list)
    by_us = defaultdict(list)
    for b in btc:
        by_btc[b["local"].date()].append(b)
    for b in us:
        by_us[b["local"].date()].append(b)

    rows = []
    for d in sorted(by_btc):
        if d < TRAIN_START or d > TRAIN_END:
            continue
        # require US cash day (US100 present near open)
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
            b
            for b in day_bars
            if b["local"].hour == 15 and b["local"].minute >= 30
        ]
        # also allow 15:30–16:00 exclusive of 16:00+
        entry_win = [
            b
            for b in day_bars
            if (b["local"].hour == 15 and b["local"].minute >= 30)
            or (b["local"].hour == 16 and b["local"].minute == 0)
        ]
        # PREREG: 15:30–16:00 — include bars with start in [15:30, 16:00)
        entry_win = [
            b
            for b in day_bars
            if b["local"].hour == 15 and b["local"].minute >= 30
        ]
        post_flat = [
            b
            for b in day_bars
            if (b["local"].hour > 15 or (b["local"].hour == 15 and b["local"].minute >= 30))
            and (
                b["local"].hour < 21
                or (b["local"].hour == 21 and b["local"].minute == 0)
            )
        ]
        if len(pre) < 10 or len(entry_win) < 1:
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
            if up:
                hit_up = True
            if dn:
                hit_dn = True
            if hit_up and hit_dn:
                trade = None
                break
            if not (up or dn):
                continue
            side = 1 if up else -1
            # gap filter: same sign
            if side * gap <= 0:
                break
            entry = b["c"]
            stop = mid
            # simulate from next bars after entry through 21:00
            seq = [x for x in post_flat if x["local"] >= b["local"]]
            if not seq:
                break
            exit_p = None
            exit_bar = None
            for i, eb in enumerate(seq):
                if i == 0:
                    # entry bar: already closed beyond range; check stop after entry via subsequent bars
                    continue
                if side > 0 and eb["l"] <= stop:
                    exit_p = stop
                    exit_bar = eb
                    break
                if side < 0 and eb["h"] >= stop:
                    exit_p = stop
                    exit_bar = eb
                    break
            if exit_p is None:
                # flat at 21:00 bar if present else last before
                flat_bars = [x for x in seq if x["local"].hour == 21 and x["local"].minute == 0]
                exit_bar = flat_bars[0] if flat_bars else seq[-1]
                exit_p = exit_bar["c"]
            gross = side * (exit_p - entry) / entry
            spread_frac = (b["spread"] / entry) if entry > 0 else 0.0
            comm_frac = 2 * COMM_BP_SIDE * 1e-4
            cost = spread_frac + comm_frac
            trade = {
                "date": str(d),
                "symbol": BTC,
                "side": side,
                "gap_pct": gap * 100,
                "width_pct": width * 100,
                "entry": entry,
                "exit": exit_p,
                "stop": stop,
                "rh": rh,
                "rl": rl,
                "gross_bp": gross * 1e4,
                "cost_bp": cost * 1e4,
                "cost_stress_bp": (1.5 * spread_frac + comm_frac) * 1e4,
                "net_bp": (gross - cost) * 1e4,
                "entry_t": str(b["local"]),
                "exit_t": str(exit_bar["local"]),
            }
            break
        if trade:
            rows.append(trade)

    if not rows:
        summary = {
            "n_trades": 0,
            "verdict": "FAIL",
            "reason": "no_trades_after_filters",
            "reserve_2025_touched": False,
        }
        (OUT_DIR / "cost_gate_s2_btc_train.json").write_text(json.dumps(summary, indent=2) + "\n")
        (OUT_DIR / "cost_gate_s2_btc_train.md").write_text(
            "# S2-BTC kostenpoort TRAIN — FAIL (N=0 after filters)\n"
        )
        print(json.dumps(summary, indent=2))
        return

    g = np.array([r["gross_bp"] for r in rows])
    c = np.array([r["cost_bp"] for r in rows])
    cs = np.array([r["cost_stress_bp"] for r in rows])
    mean_g = float(np.mean(g))
    med_g = float(np.median(g))
    mean_c = float(np.mean(c))
    mean_cs = float(np.mean(cs))
    gate_2x_fixed = mean_g >= 2 * RT_FIXED_BP
    gate_2x_realized = mean_g >= 2 * mean_c
    gate_cost_share = (mean_c < 0.5 * mean_g) if mean_g > 0 else False
    gate_stress_2x = mean_g >= 2 * mean_cs
    gate_stress_share = (mean_cs < 0.5 * mean_g) if mean_g > 0 else False
    # PREREG §4: bruto mean ≥ 2× 1.25 bp AND costs < 50% bruto; +50% spread stress same
    # Binding uses fixed 1.25 bp (PREREG) AND realized cost-share; stress on realized
    power_ok = len(rows) >= 150
    verdict_pass = (
        gate_2x_fixed
        and gate_cost_share
        and gate_stress_2x
        and gate_stress_share
        and power_ok
    )
    verdict = "PASS" if verdict_pass else "FAIL"

    summary = {
        "n_trades": len(rows),
        "symbol": BTC,
        "train": "2021-01-01..2023-12-31",
        "prereg": "PREREG_S2_BTC_USOPEN",
        "mean_gross_bp": mean_g,
        "median_gross_bp": med_g,
        "mean_cost_bp": mean_c,
        "mean_cost_stress_bp": mean_cs,
        "fixed_rt_bp": RT_FIXED_BP,
        "gate_2x_fixed_1_25": gate_2x_fixed,
        "gate_2x_realized": gate_2x_realized,
        "gate_cost_share_lt_50pct": gate_cost_share,
        "gate_stress_2x": gate_stress_2x,
        "gate_stress_share_lt_50pct": gate_stress_share,
        "power_n_ge_150": power_ok,
        "cost_share_pct": (100.0 * mean_c / mean_g) if mean_g else None,
        "verdict": verdict,
        "reserve_2025_touched": False,
        "note": "CTO wake cost-gate; formal trial/TRIALS only if PASS under PREREG discipline",
    }

    csv_path = OUT_DIR / "cost_gate_s2_btc_train.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    json_path = OUT_DIR / "cost_gate_s2_btc_train.json"
    json_path.write_text(json.dumps(summary, indent=2) + "\n")
    md_path = OUT_DIR / "cost_gate_s2_btc_train.md"
    md_path.write_text(
        "\n".join(
            [
                "# S2-BTC kostenpoort TRAIN — PREREG_S2_BTC_USOPEN",
                "",
                f"- Train: 2021-01-01 … 2023-12-31 (geen 2024/2025 in poort)",
                f"- Data: `data/m5gz/BTCUSD.csv.gz` + `US100cash.csv.gz` (U-006 v41)",
                f"- Regel: pre-range 14:30–15:30 CET; entry close-break 15:30–16:00; stop=mid; flat 21:00; US100 |gap|≥0.15% same sign; width∈[0.20%,1.50%]",
                f"- N trades: **{len(rows)}** (power ≥150: {power_ok})",
                f"- Mean bruto: **{mean_g:+.2f} bp** | median bruto: {med_g:+.2f} bp",
                f"- Mean cost (bar-spread+2×0.20 bp): **{mean_c:.2f} bp**",
                f"- Mean cost +50% spread: **{mean_cs:.2f} bp**",
                f"- Fixed RT (COSTS_FTMO_alle): {RT_FIXED_BP} bp → 2× = {2*RT_FIXED_BP:.2f} bp",
                f"- Cost share: **{(100*mean_c/mean_g) if mean_g else float('nan'):.1f}%** (poort <50%)",
                f"- Gates: 2×fixed={gate_2x_fixed} cost_share={gate_cost_share} stress_2x={gate_stress_2x} stress_share={gate_stress_share} power={power_ok}",
                f"- **Verdict: {verdict}**",
                "",
                "Reserve 2025→: **onaangeraakt**.",
                "",
            ]
        )
        + "\n"
    )
    print(json.dumps(summary, indent=2))
    print(f"wrote {csv_path} {json_path} {md_path}")


if __name__ == "__main__":
    main()
