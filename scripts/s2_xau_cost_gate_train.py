#!/usr/bin/env python3
"""S2-XAU PRE-trial kostenpoort — PREREG_S2_XAU_OVERLAP, TRAIN 2021–2023 ONLY.

Loads data/m5gz/XAUUSD.csv.gz (U-006 A). Does NOT read 2025→ for the gate.
Rule (frozen PREREG): London–NY overlap 14:00–17:00 Europe/Amsterdam;
range 14:00–14:30; breakout after 14:30; stop = 0.35×ATR(14,M5); flat 17:00;
Asia-range filter < median of prior 20 sessions.
Poort: mean bruto ≥ 2× RT AND costs < 50% bruto; +50% spread stress same.
FAIL → STOP; no TRIALS append / no trial claim from this script alone.
"""
from __future__ import annotations

import csv
import gzip
import json
import math
from collections import defaultdict
from datetime import datetime, timedelta, date
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np

NY = ZoneInfo("America/New_York")
CET = ZoneInfo("Europe/Amsterdam")
SYM = "XAUUSD"
# COSTS_FTMO: €2.00/lot/side; contract 100 oz (from m5gz header)
COMM_EUR = 2.0
CONTRACT = 100.0
RT_FIXED_BP = 0.83  # COSTS_FTMO roundtrip_intraday
TRAIN_START = date(2021, 1, 1)
TRAIN_END = date(2023, 12, 31)
OUT_DIR = Path("results/cto/s2_xau_prep")
ATR_N = 14
STOP_ATR = 0.35
ASIA_LOOKBACK = 20


def server_to_cet(server: datetime) -> datetime:
    # FTMO server = NY+7 (same convention as A5 / m5gz README)
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
            continue  # hard skip reserve for all analysis here
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


def true_ranges(bars):
    tr = []
    prev_c = None
    for b in bars:
        if prev_c is None:
            tr.append(b["h"] - b["l"])
        else:
            tr.append(max(b["h"] - b["l"], abs(b["h"] - prev_c), abs(b["l"] - prev_c)))
        prev_c = b["c"]
    return tr


def atr_at(tr, idx):
    if idx < ATR_N:
        return None
    return float(np.mean(tr[idx - ATR_N : idx]))


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    bars = load_gz(SYM)
    print(f"loaded {len(bars)} bars (2021–2024 only; 2025+ skipped)")
    by_day = defaultdict(list)
    for b in bars:
        by_day[b["local"].date()].append(b)
    days = sorted(by_day)

    # Asia ranges per day (00:00–08:00 CET)
    asia = {}
    for d in days:
        ab = [b for b in by_day[d] if 0 <= b["local"].hour < 8]
        if len(ab) < 12:
            continue
        asia[d] = max(b["h"] for b in ab) - min(b["l"] for b in ab)

    # Chronological flat list for ATR
    flat = []
    idx_of = {}
    for d in days:
        for b in sorted(by_day[d], key=lambda x: x["local"]):
            idx_of[(d, b["local"])] = len(flat)
            flat.append(b)
    tr = true_ranges(flat)

    rows = []
    asia_days_sorted = sorted(asia)
    for d in days:
        if d < TRAIN_START or d > TRAIN_END:
            continue
        # Asia filter
        if d not in asia:
            continue
        prior = [asia[x] for x in asia_days_sorted if x < d][-ASIA_LOOKBACK:]
        if len(prior) < ASIA_LOOKBACK:
            continue
        med = float(np.median(prior))
        if asia[d] >= med:
            continue  # need compression

        day_bars = sorted(by_day[d], key=lambda x: x["local"])
        rng = [
            b
            for b in day_bars
            if (b["local"].hour == 14 and b["local"].minute < 30)
            or (
                False
            )  # 14:00–14:30
        ]
        # clearer: [14:00, 14:30)
        rng = [
            b
            for b in day_bars
            if b["local"].hour == 14 and b["local"].minute < 30
        ]
        post = [
            b
            for b in day_bars
            if (b["local"].hour == 14 and b["local"].minute >= 30)
            or (15 <= b["local"].hour < 17)
        ]
        if len(rng) < 6 or not post:
            continue
        # require starting at 14:00
        if not (rng[0]["local"].hour == 14 and rng[0]["local"].minute == 0):
            continue
        rh = max(b["h"] for b in rng)
        rl = min(b["l"] for b in rng)
        if rh <= rl:
            continue

        trade = None
        for b in post:
            up = b["h"] > rh
            dn = b["l"] < rl
            if up and dn:
                break  # two-way same bar → skip day
            if not (up or dn):
                continue
            side = 1 if up else -1
            entry = max(rh, b["o"]) if up else min(rl, b["o"])
            fi = idx_of[(d, b["local"])]
            atr = atr_at(tr, fi)
            if atr is None or atr <= 0:
                break
            stop_dist = STOP_ATR * atr
            stop = entry - stop_dist if side > 0 else entry + stop_dist
            # simulate from entry bar onward until 17:00
            exit_p = None
            exit_bar = None
            # entry bar stop check first
            seq = [b] + [
                x
                for x in post
                if x["local"] > b["local"]
            ]
            for eb in seq:
                if side > 0 and eb["l"] <= stop:
                    exit_p = stop
                    exit_bar = eb
                    break
                if side < 0 and eb["h"] >= stop:
                    exit_p = stop
                    exit_bar = eb
                    break
            if exit_p is None:
                # flat at last bar before 17:00
                exit_bar = seq[-1]
                exit_p = exit_bar["c"]
            gross = side * (exit_p - entry) / entry
            # cost: entry spread (long pays ask) + 2× commission; stress later
            mid = entry
            comm_frac = (2 * COMM_EUR) / (CONTRACT * mid)
            spread_frac = (b["spread"] / mid) if mid > 0 else 0.0
            cost = spread_frac + comm_frac
            trade = {
                "date": str(d),
                "symbol": SYM,
                "side": side,
                "entry": entry,
                "exit": exit_p,
                "stop": stop,
                "atr": atr,
                "asia_rng": asia[d],
                "asia_med20": med,
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
        raise SystemExit("no trades — abort")

    g = np.array([r["gross_bp"] for r in rows])
    c = np.array([r["cost_bp"] for r in rows])
    cs = np.array([r["cost_stress_bp"] for r in rows])
    mean_g = float(np.mean(g))
    med_g = float(np.median(g))
    mean_c = float(np.mean(c))
    mean_cs = float(np.mean(cs))
    # PREREG §4: mean bruto ≥ 2× RT AND costs < 50% bruto
    # Use realized mean cost; also report vs fixed 0.83 bp.
    gate_2x_realized = mean_g >= 2 * mean_c
    gate_2x_fixed = mean_g >= 2 * RT_FIXED_BP
    gate_cost_share = (mean_c < 0.5 * mean_g) if mean_g > 0 else False
    gate_stress_2x = mean_g >= 2 * mean_cs
    gate_stress_share = (mean_cs < 0.5 * mean_g) if mean_g > 0 else False
    # Binding: BOTH mean≥2× realized-RT AND cost-share; stress must also pass
    verdict_pass = gate_2x_realized and gate_cost_share and gate_stress_2x and gate_stress_share
    verdict = "PASS" if verdict_pass else "FAIL"

    summary = {
        "n_trades": len(rows),
        "symbol": SYM,
        "train": "2021-01-01..2023-12-31",
        "prereg": "PREREG_S2_XAU_OVERLAP",
        "mean_gross_bp": mean_g,
        "median_gross_bp": med_g,
        "mean_cost_bp": mean_c,
        "mean_cost_stress_bp": mean_cs,
        "fixed_rt_bp": RT_FIXED_BP,
        "gate_2x_realized": gate_2x_realized,
        "gate_2x_fixed_0_83": gate_2x_fixed,
        "gate_cost_share_lt_50pct": gate_cost_share,
        "gate_stress_2x": gate_stress_2x,
        "gate_stress_share_lt_50pct": gate_stress_share,
        "cost_share_pct": (100.0 * mean_c / mean_g) if mean_g else None,
        "verdict": verdict,
        "reserve_2025_touched": False,
        "note": "CTO wake cost-gate; formal trial/TRIALS only if PASS and U2/CTO appends under PREREG discipline",
    }

    csv_path = OUT_DIR / "cost_gate_s2_xau_train.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    json_path = OUT_DIR / "cost_gate_s2_xau_train.json"
    json_path.write_text(json.dumps(summary, indent=2) + "\n")
    md_path = OUT_DIR / "cost_gate_s2_xau_train.md"
    md_path.write_text(
        "\n".join(
            [
                "# S2-XAU kostenpoort TRAIN — PREREG_S2_XAU_OVERLAP",
                "",
                f"- Train: 2021-01-01 … 2023-12-31 (geen 2024/2025 in poort)",
                f"- Data: `data/m5gz/XAUUSD.csv.gz` (U-006 A)",
                f"- Regel: overlap 14:00–17:00 CET; range 14:00–14:30; stop 0.35×ATR(14); Asia-compressiefilter",
                f"- N trades: **{len(rows)}**",
                f"- Mean bruto: **{mean_g:+.2f} bp** | median bruto: {med_g:+.2f} bp",
                f"- Mean cost (bar-spread+2×€2/lot): **{mean_c:.2f} bp** → 2× = **{2*mean_c:.2f} bp**",
                f"- Mean cost +50% spread: **{mean_cs:.2f} bp** → 2× = **{2*mean_cs:.2f} bp**",
                f"- Fixed RT (COSTS_FTMO): {RT_FIXED_BP} bp → 2× = {2*RT_FIXED_BP:.2f} bp (info)",
                f"- Cost share: **{(100*mean_c/mean_g) if mean_g else float('nan'):.1f}%** (poort <50%)",
                f"- Gates: 2×realized={gate_2x_realized} cost_share={gate_cost_share} stress_2x={gate_stress_2x} stress_share={gate_stress_share}",
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
