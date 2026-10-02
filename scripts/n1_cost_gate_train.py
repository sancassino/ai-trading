#!/usr/bin/env python3
"""N1 PRE-trial kostenpoort — PREREG_FTMO_N1_OPEN_FADE, TRAIN 2021–2023 ONLY.

Universe: US100cash, US30cash, US500cash.
Rule (frozen): 30-min opening drive vs ATR14; fade at T+30 close toward open;
target = mid(entry, open); stop = 1.0×|drive| beyond entry; same-bar → stop wins;
flatten session close (~22:00 CET). Intraday-flat (swap≈0).
Poort: signed mean bruto bp/trade ≥ 3× trade-weighted mean RT (COSTS_FTMO).
+50% RT stress reported. Reserve 2025→ skipped at load. No TRIAL_COUNT on FAIL.
"""
from __future__ import annotations

import csv
import gzip
import json
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np

NY = ZoneInfo("America/New_York")
CET = ZoneInfo("Europe/Amsterdam")
SYMS = ["US100cash", "US30cash", "US500cash"]
RT_BP = {"US100cash": 0.66, "US30cash": 0.45, "US500cash": 0.78}
TRAIN_START = date(2021, 1, 1)
TRAIN_END = date(2023, 12, 31)
OUT_DIR = Path("results/R2/n1_prep")
DRIVE_MULT = 1.5
ATR_N = 14


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
        if local.year >= 2025 or local.year < 2021:
            continue
        bars.append(
            {
                "local": local,
                "o": float(o),
                "h": float(h),
                "l": float(l),
                "c": float(c),
                "spread": int(sp) * (point or 0.01),
            }
        )
    return bars


def by_day(bars):
    d = defaultdict(list)
    for b in bars:
        d[b["local"].date()].append(b)
    for k in d:
        d[k].sort(key=lambda x: x["local"])
    return d


def daily_hlc(day_bars):
    """Cash-session approx: bars with CET hour in [15, 21]."""
    cash = [b for b in day_bars if 15 <= b["local"].hour < 22]
    if len(cash) < 6:
        return None
    return max(b["h"] for b in cash), min(b["l"] for b in cash), cash[-1]["c"]


def atr14(days, day_map, i):
    """Wilder-ish simple mean TR over prior ATR_N cash days."""
    if i < ATR_N:
        return None
    trs = []
    for k in range(i - ATR_N, i):
        d = days[k]
        hlc = day_map.get(d)
        if hlc is None:
            return None
        h, l, c = hlc
        prev_c = day_map[days[k - 1]][2] if k > 0 and days[k - 1] in day_map else c
        trs.append(max(h - l, abs(h - prev_c), abs(l - prev_c)))
    return float(np.mean(trs))


def simulate_day(day_bars, atr_price, rt_bp: float):
    """Return trade dict or None."""
    # cash open = first bar at/after 15:30 CET
    open_bars = [
        b
        for b in day_bars
        if (b["local"].hour > 15 or (b["local"].hour == 15 and b["local"].minute >= 30))
        and b["local"].hour < 22
    ]
    if len(open_bars) < 6:
        return None
    # need M5 resolution for first 30m: 6 bars starting near 15:30
    t0 = open_bars[0]["local"]
    if not (t0.hour == 15 and t0.minute == 30):
        # allow 15:30±0 if first available is slightly late but still ≤15:35
        if not (t0.hour == 15 and t0.minute <= 35):
            return None
    drive_bars = open_bars[:6]
    if len(drive_bars) < 6:
        return None
    # require ~5-min steps
    deltas = [
        (drive_bars[i + 1]["local"] - drive_bars[i]["local"]).total_seconds()
        for i in range(5)
    ]
    if any(d != 300 for d in deltas):
        return None

    p_open = drive_bars[0]["o"]
    p_t30 = drive_bars[5]["c"]
    if p_open <= 0 or atr_price <= 0:
        return None
    drive_bp = 1e4 * (p_t30 - p_open) / p_open
    atr_bp = 1e4 * atr_price / p_open
    if atr_bp <= 0:
        return None

    if drive_bp >= DRIVE_MULT * atr_bp:
        side = -1  # fade up → short
    elif drive_bp <= -DRIVE_MULT * atr_bp:
        side = 1  # fade down → long
    else:
        return None

    entry = p_t30
    entry_t = drive_bars[5]["local"]
    drive_abs = abs(p_t30 - p_open)
    target = entry + side * 0.5 * drive_abs  # mid toward open
    stop = entry - side * 1.0 * drive_abs  # beyond entry in drive dir

    # post-entry bars until session close
    rest = [b for b in open_bars if b["local"] > entry_t]
    if not rest:
        return None

    exit_p = None
    exit_reason = None
    for b in rest:
        hit_tgt = (side > 0 and b["h"] >= target) or (side < 0 and b["l"] <= target)
        hit_stp = (side > 0 and b["l"] <= stop) or (side < 0 and b["h"] >= stop)
        if hit_tgt and hit_stp:
            exit_p, exit_reason = stop, "stop_samebar"
            break
        if hit_stp:
            exit_p, exit_reason = stop, "stop"
            break
        if hit_tgt:
            exit_p, exit_reason = target, "target"
            break
    if exit_p is None:
        exit_p = rest[-1]["c"]
        exit_reason = "eod"

    bruto_bp = side * 1e4 * (exit_p - entry) / entry
    return {
        "side": side,
        "drive_bp": drive_bp,
        "atr_bp": atr_bp,
        "bruto_bp": bruto_bp,
        "rt_bp": rt_bp,
        "exit": exit_reason,
        "entry": entry,
        "exit_p": exit_p,
    }


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for sym in SYMS:
        bars = load_gz(sym)
        dd = by_day(bars)
        days = sorted(dd)
        day_map = {}
        for d in days:
            hlc = daily_hlc(dd[d])
            if hlc:
                day_map[d] = hlc
        cash_days = [d for d in days if d in day_map]
        idx = {d: i for i, d in enumerate(cash_days)}
        for d in cash_days:
            if d < TRAIN_START or d > TRAIN_END:
                continue
            i = idx[d]
            atr = atr14(cash_days, day_map, i)
            if atr is None:
                continue
            tr = simulate_day(dd[d], atr, RT_BP[sym])
            if tr is None:
                continue
            rows.append({"date": d.isoformat(), "symbol": sym, **tr})

    n = len(rows)
    if n == 0:
        summary = {"n": 0, "pass": False, "reason": "no_trades"}
    else:
        bruto = np.array([r["bruto_bp"] for r in rows], dtype=float)
        rts = np.array([r["rt_bp"] for r in rows], dtype=float)
        mean_bruto = float(bruto.mean())
        mean_rt = float(rts.mean())
        thr = 3.0 * mean_rt
        mean_bruto_stress = mean_bruto  # bruto independent of RT; stress raises threshold
        thr_stress = 3.0 * mean_rt * 1.5
        passed = mean_bruto >= thr
        summary = {
            "n": n,
            "mean_bruto_bp": mean_bruto,
            "median_bruto_bp": float(np.median(bruto)),
            "mean_rt_bp": mean_rt,
            "threshold_3x_rt": thr,
            "pass": bool(passed),
            "stress_threshold_3x_1p5rt": thr_stress,
            "stress_pass": bool(mean_bruto >= thr_stress),
            "n_by_sym": {s: sum(1 for r in rows if r["symbol"] == s) for s in SYMS},
            "mean_bruto_by_sym": {
                s: float(np.mean([r["bruto_bp"] for r in rows if r["symbol"] == s]))
                if any(r["symbol"] == s for r in rows)
                else None
                for s in SYMS
            },
            "exit_counts": {
                k: sum(1 for r in rows if r["exit"] == k)
                for k in sorted({r["exit"] for r in rows})
            },
        }

    with open(OUT_DIR / "cost_gate_n1_train.json", "w") as f:
        json.dump(summary, f, indent=2)
    with open(OUT_DIR / "cost_gate_n1_train.csv", "w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "date",
                "symbol",
                "side",
                "drive_bp",
                "atr_bp",
                "bruto_bp",
                "rt_bp",
                "exit",
                "entry",
                "exit_p",
            ],
        )
        w.writeheader()
        for r in rows:
            w.writerow(r)

    md = [
        "# N1 cost-gate TRAIN (PREREG_FTMO_N1_OPEN_FADE)",
        "",
        f"- Train: {TRAIN_START} … {TRAIN_END}; 2025+ skipped at load",
        f"- Symbols: {', '.join(SYMS)}",
        f"- RT fixed bp: {RT_BP}",
        f"- N trades: **{summary.get('n')}**",
    ]
    if summary.get("n", 0):
        md += [
            f"- Mean bruto: **{summary['mean_bruto_bp']:.4f} bp**",
            f"- Median bruto: {summary['median_bruto_bp']:.4f} bp",
            f"- Mean RT (trade-weighted): {summary['mean_rt_bp']:.4f} bp",
            f"- Poort 3×RT: {summary['threshold_3x_rt']:.4f} bp → "
            f"**{'PASS' if summary['pass'] else 'FAIL'}**",
            f"- +50% RT stress thr: {summary['stress_threshold_3x_1p5rt']:.4f} → "
            f"{'PASS' if summary['stress_pass'] else 'FAIL'}",
            f"- N by sym: {summary['n_by_sym']}",
            f"- Mean bruto by sym: {summary['mean_bruto_by_sym']}",
            f"- Exits: {summary['exit_counts']}",
        ]
    md += [
        "",
        "**Decision:** "
        + (
            "PASS → proceed to trial stats / ftmo_ev (CTO+U2)."
            if summary.get("pass")
            else "FAIL → STOP. No TRIAL_COUNT increment (poort-fail). No 2024 test."
        ),
        "",
        "Reserve 2025-01→ ONAANGERAAKT.",
    ]
    (OUT_DIR / "cost_gate_n1_train.md").write_text("\n".join(md) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
