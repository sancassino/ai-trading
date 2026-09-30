#!/usr/bin/env python3
"""N5 US500/US100 Opening Gap Fill — PRE-trial kostenpoort TRAIN 2021–2023.

PREREG_FTMO_N5_GAP_FILL.md (Strateeg cb786f1 / CTO land).
Gap-fade at US cash open M5 close; flat 11:00 ET / 17:00 CET; stop 1.5×ATR14.
Poort: pooled mean bruto ≥ 1.95 bp; +50% RT stress reported.
Reserve 2025→ skipped at load. No TRIAL_COUNT on FAIL. Not a formal trial.
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
SYMS = ["US500cash", "US100cash"]
RT_BP = {"US500cash": 0.70, "US100cash": 0.60}
GATE_FIXED = 1.95  # 3 × 0.65 pooled (PREREG)
TRAIN_START = date(2021, 1, 1)
TRAIN_END = date(2023, 12, 31)
OUT_DIR = Path("results/cto/n5_gap_fill_prep")
GAP_MIN = 0.0030
ATR_N = 14
STOP_ATR = 1.5


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
    cash = [b for b in day_bars if 15 <= b["local"].hour < 22]
    if len(cash) < 6:
        return None
    return max(b["h"] for b in cash), min(b["l"] for b in cash), cash[-1]["c"]


def atr14(days, day_map, i):
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


def simulate_day(day_bars, prior_close, atr_price, rt_bp: float):
    open_bars = [
        b
        for b in day_bars
        if (b["local"].hour > 15 or (b["local"].hour == 15 and b["local"].minute >= 30))
        and b["local"].hour < 18
    ]
    if not open_bars:
        return None
    t0 = open_bars[0]["local"]
    if not (t0.hour == 15 and t0.minute <= 35):
        return None
    session_open = open_bars[0]["o"]
    if prior_close is None or prior_close <= 0 or session_open <= 0 or atr_price is None or atr_price <= 0:
        return None
    gap = session_open / prior_close - 1.0
    if abs(gap) < GAP_MIN:
        return None
    side = -1 if gap >= GAP_MIN else 1
    entry = open_bars[0]["c"]  # close of first M5
    entry_t = open_bars[0]["local"]
    stop = entry - side * STOP_ATR * atr_price
    # flat at 17:00 CET (= 11:00 ET)
    rest = [
        b
        for b in day_bars
        if b["local"] > entry_t
        and (
            b["local"].hour < 17
            or (b["local"].hour == 17 and b["local"].minute == 0)
        )
    ]
    if not rest:
        return None
    exit_p = rest[-1]["c"]
    exit_reason = "time"
    for b in rest:
        if side > 0 and b["l"] <= stop:
            exit_p = stop
            exit_reason = "stop"
            break
        if side < 0 and b["h"] >= stop:
            exit_p = stop
            exit_reason = "stop"
            break
    bruto_bp = 1e4 * side * (exit_p - entry) / entry
    return {
        "side": side,
        "gap_pct": gap * 100.0,
        "bruto_bp": bruto_bp,
        "rt_bp": rt_bp,
        "netto_bp": bruto_bp - rt_bp,
        "exit": exit_reason,
    }


def run_sym(sym: str):
    bars = load_gz(sym)
    day_map_bars = by_day(bars)
    days = sorted(day_map_bars)
    hlc_map = {}
    for d in days:
        hlc = daily_hlc(day_map_bars[d])
        if hlc is not None:
            hlc_map[d] = hlc
    trades = []
    for i, d in enumerate(days):
        if d < TRAIN_START or d > TRAIN_END:
            continue
        if d not in hlc_map:
            continue
        atr = atr14(days, hlc_map, i)
        # prior session close = previous cash day close
        prev_close = None
        for j in range(i - 1, -1, -1):
            if days[j] in hlc_map:
                prev_close = hlc_map[days[j]][2]
                break
        tr = simulate_day(day_map_bars[d], prev_close, atr, RT_BP[sym])
        if tr is None:
            continue
        tr["date"] = d.isoformat()
        tr["sym"] = sym
        trades.append(tr)
    return trades


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    all_tr = []
    by_sym = {}
    for sym in SYMS:
        tr = run_sym(sym)
        by_sym[sym] = tr
        all_tr.extend(tr)
        print(f"{sym}: N={len(tr)} mean_bruto={np.mean([t['bruto_bp'] for t in tr]) if tr else float('nan'):+.2f} bp")

    with open(OUT_DIR / "trades_train.csv", "w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["date", "sym", "side", "gap_pct", "bruto_bp", "rt_bp", "netto_bp", "exit"],
        )
        w.writeheader()
        for t in all_tr:
            w.writerow(t)

    if not all_tr:
        summary = {"n": 0, "verdict": "STOP_NO_TRADES", "gate_bp": GATE_FIXED}
    else:
        bruto = np.array([t["bruto_bp"] for t in all_tr], float)
        rt = np.array([t["rt_bp"] for t in all_tr], float)
        mean_b = float(bruto.mean())
        tw_rt = float(rt.mean())
        gate_3x = 3.0 * tw_rt
        gate_stress = 3.0 * 1.5 * tw_rt
        # Binding PREREG = fixed 1.95; also require stress for CTO consistency with other gates
        if mean_b < GATE_FIXED:
            verdict = "FAIL_STOP"
        elif mean_b < gate_stress:
            verdict = "FAIL_STOP_STRESS"
        else:
            verdict = "PASS_GATE"
        summary = {
            "prereg": "PREREG_FTMO_N5_GAP_FILL.md",
            "window": "2021-01-01..2023-12-31",
            "reserve_2025": "untouched",
            "n": int(len(all_tr)),
            "mean_bruto_bp": mean_b,
            "mean_netto_bp": float((bruto - rt).mean()),
            "tw_rt_bp": tw_rt,
            "gate_fixed_bp": GATE_FIXED,
            "gate_3x_rt": gate_3x,
            "gate_3x_rt_stress50": gate_stress,
            "pass_fixed": bool(mean_b >= GATE_FIXED),
            "pass_stress50": bool(mean_b >= gate_stress),
            "stop_rate": float(np.mean([t["exit"] == "stop" for t in all_tr])),
            "verdict": verdict,
            "by_sym": {
                s: {
                    "n": len(by_sym[s]),
                    "mean_bruto_bp": float(np.mean([t["bruto_bp"] for t in by_sym[s]])) if by_sym[s] else None,
                }
                for s in SYMS
            },
        }
    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print("OUT", OUT_DIR)


if __name__ == "__main__":
    main()
