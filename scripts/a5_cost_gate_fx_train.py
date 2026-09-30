#!/usr/bin/env python3
"""A5 PRE-trial kostenpoort for PREREG_FTMO_FX_INTRADAG — TRAIN 2021–2023 ONLY.

Loads FTMO-M5 from data/m5gz/*.csv.gz (U-006 A). Does not touch 2025→ for the gate.
PREREG: London-open OR 08:00–08:30 CET, exit 12:00 CET, majors EURUSD/GBPUSD/USDJPY/USDCHF.
Poort (frozen PREREG): median bruto ≥ 3× mean rondreis (trade-weighted); also report vs 2.1 bp.
FAIL → STOP; PREREG §5: no TRIAL_COUNT increment on cost-gate fail.
"""
from __future__ import annotations

import csv
import gzip
import json
import math
import os
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np

NY = ZoneInfo("America/New_York")
CET = ZoneInfo("Europe/Amsterdam")
SYMS = ["EURUSD", "GBPUSD", "USDJPY", "USDCHF"]
# €2.25 / lot / side; 1 lot = 100_000 units (same as u3_london_orb)
COMM_EUR = 2.25
LOT = 100_000.0
TRAIN_START = datetime(2021, 1, 1).date()
TRAIN_END = datetime(2023, 12, 31).date()
OUT_DIR = Path("results/R2/a5_prep")


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
        bars.append((server, float(o), float(h), float(l), float(c), int(sp) * point))
    return bars


def morning_sessions(sym: str):
    """CET sessions 08:00–12:00 with OR bars present; skip incomplete mornings."""
    by_day = defaultdict(list)
    for b in load_gz(sym):
        local = (b[0] - timedelta(hours=7)).replace(tzinfo=NY).astimezone(CET)
        # Restrict load window: train + test year only in memory later; still skip 2025+ early
        if local.year >= 2025:
            continue
        if local.year < 2021:
            continue
        by_day[local.date()].append((local,) + b[1:])
    out = []
    for d in sorted(by_day):
        if d < TRAIN_START or d > TRAIN_END:
            continue  # cost gate: TRAIN ONLY (no 2024/2025 peek)
        bars = sorted(by_day[d], key=lambda x: x[0])
        op = datetime(d.year, d.month, d.day, 8, 0, tzinfo=CET)
        mid = datetime(d.year, d.month, d.day, 8, 30, tzinfo=CET)
        cl = datetime(d.year, d.month, d.day, 12, 0, tzinfo=CET)
        window = [b for b in bars if op <= b[0] < cl]
        or_bars = [b for b in window if b[0] < mid]
        post = [b for b in window if b[0] >= mid]
        if len(or_bars) < 6 or not post:
            continue
        # require first OR bar at 08:00 and a bar that can serve as 11:55 exit
        if or_bars[0][0] != op:
            continue
        if post[-1][0] < cl - timedelta(minutes=5):
            continue
        out.append((d, or_bars, post))
    return out


def cost_frac(side: int, entry_bar, exit_bar, price: float, comm_frac: float) -> float:
    spread = entry_bar[5] if side > 0 else exit_bar[5]
    return spread / price + 2 * comm_frac


def run_a5(or_bars, post, comm_frac: float):
    """One trade max; OCO on first breakout after 08:30; stop = opposite OR; exit ≤ 12:00 CET."""
    hi = max(b[2] for b in or_bars)
    lo = min(b[3] for b in or_bars)
    if hi <= lo:
        return None
    for b in post:
        up, dn = b[2] > hi, b[3] < lo
        if not (up or dn):
            continue
        if up and dn:
            # both sides same bar → conservative loss (PREREG OCO / b4 convention)
            side = 1
            entry = max(hi, b[1])
            exit_p = lo
            ex_bar = b
            gross = side * (exit_p - entry) / entry
            rt = cost_frac(side, b, ex_bar, entry, comm_frac)
            return {
                "side": side,
                "entry": entry,
                "exit": exit_p,
                "gross": gross,
                "cost": rt,
                "net": gross - rt,
                "entry_t": str(b[0]),
                "exit_t": str(ex_bar[0]),
            }
        side = 1 if up else -1
        entry = max(hi, b[1]) if up else min(lo, b[1])
        stop = lo if up else hi
        # stop on entry bar?
        if (up and b[3] <= stop) or (dn and b[2] >= stop):
            exit_p = stop
            ex_bar = b
        else:
            exit_p = None
            ex_bar = None
            for b2 in post[post.index(b) + 1 :]:
                if side > 0 and b2[3] <= stop:
                    exit_p = min(stop, b2[1])
                    ex_bar = b2
                    break
                if side < 0 and b2[2] >= stop:
                    exit_p = max(stop, b2[1])
                    ex_bar = b2
                    break
            if exit_p is None:
                ex_bar = post[-1]
                exit_p = post[-1][4]  # 11:55 close ≈ flat at 12:00
        gross = side * (exit_p - entry) / entry
        rt = cost_frac(side, b, ex_bar, entry, comm_frac)
        return {
            "side": side,
            "entry": entry,
            "exit": exit_p,
            "gross": gross,
            "cost": rt,
            "net": gross - rt,
            "entry_t": str(b[0]),
            "exit_t": str(ex_bar[0]),
        }
    return None


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for sym in SYMS:
        sess = morning_sessions(sym)
        print(f"{sym}: {len(sess)} train mornings with OR+post")
        for d, or_bars, post in sess:
            # commission as fraction of notional using OR mid as proxy price
            mid = 0.5 * (or_bars[0][1] + or_bars[-1][4])
            # JPY pairs: pip value differs but €/lot / (lot*price) still works for price return
            comm_frac = COMM_EUR / (LOT * mid)
            tr = run_a5(or_bars, post, comm_frac)
            if tr is None:
                continue
            rows.append(
                {
                    "date": str(d),
                    "symbol": sym,
                    "side": tr["side"],
                    "gross_bp": tr["gross"] * 1e4,
                    "cost_bp": tr["cost"] * 1e4,
                    "net_bp": tr["net"] * 1e4,
                    "entry_t": tr["entry_t"],
                    "exit_t": tr["exit_t"],
                }
            )

    if not rows:
        raise SystemExit("no trades — abort")

    g = np.array([r["gross_bp"] for r in rows])
    c = np.array([r["cost_bp"] for r in rows])
    med_g = float(np.median(g))
    mean_g = float(np.mean(g))
    med_c = float(np.median(c))
    mean_c = float(np.mean(c))
    # PREREG: mediaan bruto ≥ 3× rondreis; also absolute 2.1 bp EURUSD-standard note
    gate_3x_mean = med_g >= 3 * mean_c
    gate_3x_med = med_g >= 3 * med_c
    gate_21 = med_g >= 2.1
    # Bindend: median bruto ≥ 3× mean trade cost (stricter of the 3× readings when mean>med)
    # Follow literal "mediaan bruto ≥ 3× rondreis" with trade-mean rondreis (like D-012 spirit on cost side).
    verdict_pass = gate_3x_mean
    verdict = "PASS" if verdict_pass else "FAIL"

    summary = {
        "n_trades": len(rows),
        "symbols": SYMS,
        "train": "2021-01-01..2023-12-31",
        "median_gross_bp": med_g,
        "mean_gross_bp": mean_g,
        "median_cost_bp": med_c,
        "mean_cost_bp": mean_c,
        "gate_3x_mean_cost": gate_3x_mean,
        "gate_3x_median_cost": gate_3x_med,
        "gate_abs_2_1bp": gate_21,
        "threshold_3x_mean_bp": 3 * mean_c,
        "threshold_3x_median_bp": 3 * med_c,
        "verdict": verdict,
        "reserve_2025_touched": False,
    }

    csv_path = OUT_DIR / "cost_gate_a5_train.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    json_path = OUT_DIR / "cost_gate_a5_train.json"
    json_path.write_text(json.dumps(summary, indent=2) + "\n")

    md = OUT_DIR / "cost_gate_a5_train.md"
    per = defaultdict(list)
    for r in rows:
        per[r["symbol"]].append(r)
    lines = [
        "# A5 kostenpoort TRAIN — PREREG_FTMO_FX_INTRADAG",
        "",
        f"- Train: 2021-01-01 … 2023-12-31 (geen 2024/2025 in poort)",
        f"- Data: `data/m5gz/` (U-006 A); CET Europe/Amsterdam; OR 08:00–08:30; flat ≤ 12:00",
        f"- N trades: **{len(rows)}**",
        f"- Median bruto: **{med_g:+.2f} bp** | mean bruto: {mean_g:+.2f} bp",
        f"- Mean cost (bar-spread+2×€2.25/lot): **{mean_c:.2f} bp** → 3× = **{3*mean_c:.2f} bp**",
        f"- Median cost: {med_c:.2f} bp → 3× = {3*med_c:.2f} bp",
        f"- Absolute PREREG note (≥ 2.1 bp): {'PASS' if gate_21 else 'FAIL'}",
        f"- **Verdict (median bruto ≥ 3× mean cost): {verdict}**",
        "",
        "## Per symbool (train)",
        "",
        "| Sym | N | med bruto bp | mean bruto bp | mean cost bp |",
        "|-----|--:|-------------:|--------------:|-------------:|",
    ]
    for s in SYMS:
        rs = per[s]
        if not rs:
            continue
        gg = [r["gross_bp"] for r in rs]
        cc = [r["cost_bp"] for r in rs]
        lines.append(
            f"| {s} | {len(rs)} | {float(np.median(gg)):+.2f} | {float(np.mean(gg)):+.2f} | {float(np.mean(cc)):.2f} |"
        )
    lines += [
        "",
        f"Reserve 2025→: **onaangeraakt**.",
        "",
    ]
    md.write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=2))
    print(f"wrote {csv_path} {json_path} {md}")


if __name__ == "__main__":
    main()
