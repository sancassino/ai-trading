#!/usr/bin/env python3
"""S2-USOIL PRE-trial kostenpoort — PREREG_S2_USOIL_EIA, TRAIN 2021–2023 ONLY.

Calendar: Wednesdays at 10:30 America/New_York (standard EIA WPSR slot).
Holiday postponements NOT fully modeled — provisional calendar for cost-gate only;
if near-pass, freeze exact EIA list before any formal trial.
Data: data/m5gz/USOILcash.csv.gz. Skips 2025→.
Poort: mean bruto ≥ 3× 3.34 bp AND costs < 50% bruto (PREREG §4).
"""
from __future__ import annotations

import csv
import gzip
import json
from collections import defaultdict
from datetime import datetime, timedelta, date, time
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np

NY = ZoneInfo("America/New_York")
CET = ZoneInfo("Europe/Amsterdam")
SYM = "USOILcash"
RT_FIXED_BP = 3.34
COMM_BP_SIDE = 0.0
TRAIN_START = date(2021, 1, 1)
TRAIN_END = date(2023, 12, 31)
OUT_DIR = Path("results/cto/s2_usoil_prep")
WIDTH_MIN = 0.0015
WIDTH_MAX = 0.0080
STOP_MULT = 1.25
TP_MULT = 2.0
MAX_MINUTES = 90


def server_to_cet(server: datetime) -> datetime:
    return (server - timedelta(hours=7)).replace(tzinfo=NY).astimezone(CET)


def load_gz(sym: str):
    point = None
    bars = []
    for line in gzip.open(f"data/m5gz/{sym}.csv.gz", "rt"):
        if line.startswith("#"):
            point = float(line.split("point=")[1].split(";")[0])
            continue
        if not line or not line[0].isdigit():
            continue
        t, o, h, l, c, sp = line.rstrip().split(";")
        server = datetime.strptime(t, "%Y.%m.%d %H:%M")
        local = server_to_cet(server)
        if local.year >= 2025 or local.year < 2021:
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


def eia_wednesdays():
    """Provisional: every Wednesday 2021–2023 @ 10:30 America/New_York."""
    out = []
    d = TRAIN_START
    while d <= TRAIN_END:
        if d.weekday() == 2:  # Wed
            out.append(datetime(d.year, d.month, d.day, 10, 30, tzinfo=NY))
        d += timedelta(days=1)
    return out


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    bars = load_gz(SYM)
    print(f"loaded {len(bars)} USOIL bars")
    by_day = defaultdict(list)
    for b in bars:
        by_day[b["local"].date()].append(b)

    rows = []
    for release_ny in eia_wednesdays():
        release_cet = release_ny.astimezone(CET)
        d = release_cet.date()
        day_bars = sorted(by_day.get(d, []), key=lambda x: x["local"])
        if not day_bars:
            continue
        pre_start = release_cet - timedelta(minutes=20)
        pre = [b for b in day_bars if pre_start <= b["local"] < release_cet]
        post = [
            b
            for b in day_bars
            if release_cet <= b["local"] <= release_cet + timedelta(minutes=MAX_MINUTES)
        ]
        # also hard flat 18:30 CET
        flat_deadline = release_cet.replace(hour=18, minute=30, second=0, microsecond=0)
        if flat_deadline < release_cet:
            flat_deadline = release_cet + timedelta(minutes=MAX_MINUTES)
        post = [b for b in post if b["local"] <= flat_deadline]
        if len(pre) < 3 or len(post) < 2:
            continue
        rh = max(b["h"] for b in pre)
        rl = min(b["l"] for b in pre)
        mid_px = 0.5 * (rh + rl)
        if mid_px <= 0 or rh <= rl:
            continue
        width = (rh - rl) / mid_px
        if width < WIDTH_MIN or width > WIDTH_MAX:
            continue
        # entry within 2 minutes after release: first M5 bar at/after release
        entry_bar = post[0]
        # if first bar starts more than 5 min after (M5 grid), still use it as proxy for "within 2 min mid"
        if entry_bar["local"] > release_cet + timedelta(minutes=5):
            continue
        mid_entry = 0.5 * (entry_bar["h"] + entry_bar["l"])
        if mid_entry > rh:
            side = 1
            entry = mid_entry
        elif mid_entry < rl:
            side = -1
            entry = mid_entry
        else:
            continue
        stop_dist = STOP_MULT * (rh - rl)
        tp_dist = TP_MULT * (rh - rl)
        stop = entry - stop_dist if side > 0 else entry + stop_dist
        tp = entry + tp_dist if side > 0 else entry - tp_dist
        exit_p = None
        exit_bar = None
        for eb in post[1:]:
            if side > 0:
                if eb["l"] <= stop:
                    exit_p, exit_bar = stop, eb
                    break
                if eb["h"] >= tp:
                    exit_p, exit_bar = tp, eb
                    break
            else:
                if eb["h"] >= stop:
                    exit_p, exit_bar = stop, eb
                    break
                if eb["l"] <= tp:
                    exit_p, exit_bar = tp, eb
                    break
        if exit_p is None:
            exit_bar = post[-1]
            exit_p = exit_bar["c"]
        gross = side * (exit_p - entry) / entry
        spread_frac = (entry_bar["spread"] / entry) if entry > 0 else 0.0
        cost = spread_frac + 2 * COMM_BP_SIDE * 1e-4
        rows.append(
            {
                "date": str(d),
                "release_ny": str(release_ny),
                "side": side,
                "width_pct": width * 100,
                "entry": entry,
                "exit": exit_p,
                "gross_bp": gross * 1e4,
                "cost_bp": cost * 1e4,
                "cost_stress_bp": (1.5 * spread_frac) * 1e4,
                "net_bp": (gross - cost) * 1e4,
                "entry_t": str(entry_bar["local"]),
                "exit_t": str(exit_bar["local"]),
            }
        )

    if not rows:
        summary = {"n_trades": 0, "verdict": "FAIL", "reason": "no_trades", "reserve_2025_touched": False}
        (OUT_DIR / "cost_gate_s2_usoil_train.json").write_text(json.dumps(summary, indent=2) + "\n")
        print(json.dumps(summary, indent=2))
        return

    g = np.array([r["gross_bp"] for r in rows])
    c = np.array([r["cost_bp"] for r in rows])
    cs = np.array([r["cost_stress_bp"] for r in rows])
    mean_g = float(np.mean(g))
    med_g = float(np.median(g))
    mean_c = float(np.mean(c))
    mean_cs = float(np.mean(cs))
    gate_3x = mean_g >= 3 * RT_FIXED_BP
    gate_3x_real = mean_g >= 3 * mean_c
    gate_share = (mean_c < 0.5 * mean_g) if mean_g > 0 else False
    gate_stress = mean_g >= 3 * mean_cs and ((mean_cs < 0.5 * mean_g) if mean_g > 0 else False)
    verdict_pass = gate_3x and gate_share and gate_stress
    verdict = "PASS" if verdict_pass else "FAIL"
    summary = {
        "n_trades": len(rows),
        "symbol": SYM,
        "train": "2021-01-01..2023-12-31",
        "prereg": "PREREG_S2_USOIL_EIA",
        "calendar": "provisional_wednesday_1030_America_New_York",
        "mean_gross_bp": mean_g,
        "median_gross_bp": med_g,
        "mean_cost_bp": mean_c,
        "mean_cost_stress_bp": mean_cs,
        "fixed_rt_bp": RT_FIXED_BP,
        "gate_3x_fixed": gate_3x,
        "gate_3x_realized": gate_3x_real,
        "gate_cost_share_lt_50pct": gate_share,
        "gate_stress": gate_stress,
        "cost_share_pct": (100.0 * mean_c / mean_g) if mean_g else None,
        "verdict": verdict,
        "reserve_2025_touched": False,
        "note": "Provisional EIA Wed calendar; holiday shifts not modeled. No TRIALS append.",
    }
    with open(OUT_DIR / "cost_gate_s2_usoil_train.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    (OUT_DIR / "cost_gate_s2_usoil_train.json").write_text(json.dumps(summary, indent=2) + "\n")
    (OUT_DIR / "cost_gate_s2_usoil_train.md").write_text(
        "\n".join(
            [
                "# S2-USOIL kostenpoort TRAIN — PREREG_S2_USOIL_EIA",
                "",
                f"- Train: 2021-01-01 … 2023-12-31",
                f"- Calendar: **provisional** Wed 10:30 America/New_York (holiday postponements not modeled)",
                f"- Data: `data/m5gz/USOILcash.csv.gz`",
                f"- N events/trades: **{len(rows)}**",
                f"- Mean bruto: **{mean_g:+.2f} bp** | median: {med_g:+.2f} bp",
                f"- Mean cost: **{mean_c:.2f} bp** | fixed RT {RT_FIXED_BP} → 3× = {3*RT_FIXED_BP:.2f} bp",
                f"- Cost share: **{(100*mean_c/mean_g) if mean_g else float('nan'):.1f}%**",
                f"- Gates: 3×fixed={gate_3x} share={gate_share} stress={gate_stress}",
                f"- **Verdict: {verdict}**",
                "",
                "Reserve 2025→ onaangeraakt. No formal trial from this script.",
                "",
            ]
        )
        + "\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
