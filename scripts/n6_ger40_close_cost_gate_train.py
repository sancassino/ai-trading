#!/usr/bin/env python3

NOTE: U2 C-007 binding uses AMS-wall m5gz (no NY-7h shift). This CTO parallel also FAIL; see results/cto/c007_kill_board.json.
"""N6 GER40 Pre-Close Conditional Momentum — PRE-trial kostenpoort TRAIN 2021–2023.

PREREG_FTMO_N6_GER40_CLOSE.md (Strateeg cb786f1 / CTO land).
2h trend filter 13:30→15:30 CET (±0.20%); entry 17:30 close; flat 17:55; stop 0.75×ATR14.
Poort: mean bruto ≥ 4.20 bp (3×1.40 PREREG); +50% RT stress reported.
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
SYM = "GER40cash"
RT_BP = 1.40  # PREREG frozen (COSTS_FTMO S0 figure in PREREG; alle.csv shows 0.72)
GATE_FIXED = 4.20  # 3 × 1.40
TRAIN_START = date(2021, 1, 1)
TRAIN_END = date(2023, 12, 31)
OUT_DIR = Path("results/cto/n6_ger40_close_prep")
TREND_THR = 0.0020
ATR_N = 14
STOP_ATR = 0.75


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
    # GER cash session proxy: 09:00–18:00 CET
    cash = [b for b in day_bars if 9 <= b["local"].hour < 18]
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


def bar_at(day_bars, hour, minute):
    for b in day_bars:
        if b["local"].hour == hour and b["local"].minute == minute:
            return b
    return None


def simulate_day(day_bars, atr_price, rt_bp: float):
    b1330 = bar_at(day_bars, 13, 30)
    b1530 = bar_at(day_bars, 15, 30)
    b1730 = bar_at(day_bars, 17, 30)
    b1755 = bar_at(day_bars, 17, 55)
    if not all((b1330, b1530, b1730, b1755)):
        return None
    if atr_price is None or atr_price <= 0:
        return None
    open_1330 = b1330["o"]
    close_1530 = b1530["c"]
    if open_1330 <= 0:
        return None
    move = close_1530 / open_1330 - 1.0
    if move > TREND_THR:
        side = 1
    elif move < -TREND_THR:
        side = -1
    else:
        return None
    entry = b1730["c"]
    entry_t = b1730["local"]
    stop = entry - side * STOP_ATR * atr_price
    # path from after entry through 17:55 inclusive
    rest = [b for b in day_bars if b["local"] > entry_t and (
        b["local"].hour < 17 or (b["local"].hour == 17 and b["local"].minute <= 55)
    )]
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
        "trend_pct": move * 100.0,
        "bruto_bp": bruto_bp,
        "rt_bp": rt_bp,
        "netto_bp": bruto_bp - rt_bp,
        "exit": exit_reason,
    }


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    bars = load_gz(SYM)
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
        tr = simulate_day(day_map_bars[d], atr, RT_BP)
        if tr is None:
            continue
        tr["date"] = d.isoformat()
        tr["sym"] = SYM
        trades.append(tr)

    with open(OUT_DIR / "trades_train.csv", "w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["date", "sym", "side", "trend_pct", "bruto_bp", "rt_bp", "netto_bp", "exit"],
        )
        w.writeheader()
        for t in trades:
            w.writerow(t)

    if not trades:
        summary = {"n": 0, "verdict": "STOP_NO_TRADES", "gate_bp": GATE_FIXED}
    else:
        bruto = np.array([t["bruto_bp"] for t in trades], float)
        rt = np.array([t["rt_bp"] for t in trades], float)
        mean_b = float(bruto.mean())
        tw_rt = float(rt.mean())
        gate_3x = 3.0 * tw_rt
        gate_stress = 3.0 * 1.5 * tw_rt
        if mean_b < GATE_FIXED:
            verdict = "FAIL_STOP"
        elif mean_b < gate_stress:
            verdict = "FAIL_STOP_STRESS"
        else:
            verdict = "PASS_GATE"
        summary = {
            "prereg": "PREREG_FTMO_N6_GER40_CLOSE.md",
            "window": "2021-01-01..2023-12-31",
            "reserve_2025": "untouched",
            "n": int(len(trades)),
            "mean_bruto_bp": mean_b,
            "mean_netto_bp": float((bruto - rt).mean()),
            "tw_rt_bp": tw_rt,
            "gate_fixed_bp": GATE_FIXED,
            "gate_3x_rt": gate_3x,
            "gate_3x_rt_stress50": gate_stress,
            "pass_fixed": bool(mean_b >= GATE_FIXED),
            "pass_stress50": bool(mean_b >= gate_stress),
            "stop_rate": float(np.mean([t["exit"] == "stop" for t in trades])),
            "long_n": int(sum(1 for t in trades if t["side"] > 0)),
            "short_n": int(sum(1 for t in trades if t["side"] < 0)),
            "note_m5_2021": "GER40 m5gz sparse in 2021 (dense from ~2022); train uses available anchors only",
            "verdict": verdict,
        }
    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print("OUT", OUT_DIR)


if __name__ == "__main__":
    main()
