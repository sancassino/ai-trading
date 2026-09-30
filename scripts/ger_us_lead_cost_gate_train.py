#!/usr/bin/env python3

NOTE: U2 C-007 binding uses AMS-wall m5gz (no NY-7h shift). This CTO parallel also FAIL; see results/cto/c007_kill_board.json.
"""S2 GER_US_LEAD — PRE-trial kostenpoort TRAIN 2021–2023.

PREREG_S2_GER_US_LEAD.md (Strateeg-2 d68caab / CTO land).
GER40 09:00–15:15 impulse → US100/US500 open continuation; flat 20:00 CET.
Poort: pooled mean bruto ≥ 3× TW-RT; +50% stress. Reserve 2025→ skipped.
"""
from __future__ import annotations

import csv, gzip, json
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
import numpy as np

NY = ZoneInfo("America/New_York")
CET = ZoneInfo("Europe/Amsterdam")
EXEC = ["US100cash", "US500cash"]
RT_BP = {"US100cash": 0.66, "US500cash": 0.78}
SIGNAL = "GER40cash"
TRAIN_START = date(2021, 1, 1)
TRAIN_END = date(2023, 12, 31)
OUT_DIR = Path("results/cto/ger_us_lead_prep")
FILT = 0.40
TGT = 1.0
STP = 0.75
ATR_N = 14


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
        bars.append({"local": local, "o": float(o), "h": float(h), "l": float(l), "c": float(c)})
    return bars


def by_day(bars):
    d = defaultdict(list)
    for b in bars:
        d[b["local"].date()].append(b)
    for k in d:
        d[k].sort(key=lambda x: x["local"])
    return d


def bar_at(day_bars, hour, minute):
    for b in day_bars:
        if b["local"].hour == hour and b["local"].minute == minute:
            return b
    return None


def daily_hlc_cash(day_bars, h0=9, h1=18):
    cash = [b for b in day_bars if h0 <= b["local"].hour < h1]
    if len(cash) < 6:
        return None
    return max(b["h"] for b in cash), min(b["l"] for b in cash), cash[-1]["c"]


def atr14(days, day_map, i):
    if i < ATR_N:
        return None
    trs = []
    for k in range(i - ATR_N, i):
        hlc = day_map.get(days[k])
        if hlc is None:
            return None
        h, l, c = hlc
        prev_c = day_map[days[k - 1]][2] if k > 0 and days[k - 1] in day_map else c
        trs.append(max(h - l, abs(h - prev_c), abs(l - prev_c)))
    return float(np.mean(trs))


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ger_days = by_day(load_gz(SIGNAL))
    us_days = {s: by_day(load_gz(s)) for s in EXEC}
    # GER D1 ATR map
    ger_dates = sorted(ger_days)
    ger_hlc = {}
    for d in ger_dates:
        hlc = daily_hlc_cash(ger_days[d], 9, 18)
        if hlc:
            ger_hlc[d] = hlc
    us_hlc = {}
    us_dates = {}
    for s in EXEC:
        dates = sorted(us_days[s])
        us_dates[s] = dates
        m = {}
        for d in dates:
            # US cash ~15:30–22:00 CET
            hlc = daily_hlc_cash(us_days[s][d], 15, 22)
            if hlc:
                m[d] = hlc
        us_hlc[s] = m

    trades = []
    for i, d in enumerate(ger_dates):
        if d < TRAIN_START or d > TRAIN_END:
            continue
        if d not in ger_hlc:
            continue
        atr_ger = atr14(ger_dates, ger_hlc, i)
        if atr_ger is None or atr_ger <= 0:
            continue
        g0900 = bar_at(ger_days[d], 9, 0)
        g1515 = bar_at(ger_days[d], 15, 15)
        if not g0900 or not g1515 or g0900["o"] <= 0:
            continue
        ger_bp = 1e4 * (g1515["c"] - g0900["o"]) / g0900["o"]
        atr_ger_bp = 1e4 * atr_ger / g0900["o"]
        if ger_bp >= FILT * atr_ger_bp:
            side = 1
        elif ger_bp <= -FILT * atr_ger_bp:
            side = -1
        else:
            continue

        for s in EXEC:
            if d not in us_days[s] or d not in us_hlc[s]:
                continue
            # US ATR from prior days index
            udates = us_dates[s]
            try:
                ui = udates.index(d)
            except ValueError:
                continue
            atr_us = atr14(udates, us_hlc[s], ui)
            if atr_us is None or atr_us <= 0:
                continue
            # US cash open ≈ 15:30 CET
            open_bars = [
                b for b in us_days[s][d]
                if (b["local"].hour > 15 or (b["local"].hour == 15 and b["local"].minute >= 30))
                and b["local"].hour < 17
            ]
            if not open_bars:
                continue
            t0 = open_bars[0]["local"]
            if not (t0.hour == 15 and t0.minute <= 35):
                continue
            entry = open_bars[0]["c"]
            entry_t = open_bars[0]["local"]
            atr_us_bp = 1e4 * atr_us / entry
            target = entry * (1 + side * TGT * atr_us_bp / 1e4)
            stop = entry * (1 - side * STP * atr_us_bp / 1e4)
            rest = [
                b for b in us_days[s][d]
                if b["local"] > entry_t
                and (
                    b["local"].hour < 20
                    or (b["local"].hour == 20 and b["local"].minute == 0)
                )
            ]
            if not rest:
                continue
            exit_p = rest[-1]["c"]
            exit_reason = "time"
            for b in rest:
                # same-bar: stop wins
                hit_stop = (side > 0 and b["l"] <= stop) or (side < 0 and b["h"] >= stop)
                hit_tgt = (side > 0 and b["h"] >= target) or (side < 0 and b["l"] <= target)
                if hit_stop:
                    exit_p = stop
                    exit_reason = "stop"
                    break
                if hit_tgt:
                    exit_p = target
                    exit_reason = "target"
                    break
            bruto_bp = 1e4 * side * (exit_p - entry) / entry
            trades.append({
                "date": d.isoformat(),
                "sym": s,
                "side": side,
                "ger_bp": ger_bp,
                "bruto_bp": bruto_bp,
                "rt_bp": RT_BP[s],
                "netto_bp": bruto_bp - RT_BP[s],
                "exit": exit_reason,
            })

    with open(OUT_DIR / "trades_train.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["date","sym","side","ger_bp","bruto_bp","rt_bp","netto_bp","exit"])
        w.writeheader()
        for t in trades:
            w.writerow(t)

    if not trades:
        summary = {"n": 0, "verdict": "STOP_NO_TRADES"}
    else:
        bruto = np.array([t["bruto_bp"] for t in trades], float)
        rt = np.array([t["rt_bp"] for t in trades], float)
        mean_b = float(bruto.mean())
        tw_rt = float(rt.mean())
        gate = 3.0 * tw_rt
        gate_s = 3.0 * 1.5 * tw_rt
        if mean_b < gate:
            verdict = "FAIL_STOP"
        elif mean_b < gate_s:
            verdict = "FAIL_STOP_STRESS"
        else:
            verdict = "PASS_GATE"
        by_sym = {}
        for s in EXEC:
            st = [t for t in trades if t["sym"] == s]
            by_sym[s] = {
                "n": len(st),
                "mean_bruto_bp": float(np.mean([t["bruto_bp"] for t in st])) if st else None,
            }
        summary = {
            "prereg": "PREREG_S2_GER_US_LEAD.md",
            "window": "2021-01-01..2023-12-31",
            "reserve_2025": "untouched",
            "n": int(len(trades)),
            "mean_bruto_bp": mean_b,
            "mean_netto_bp": float((bruto - rt).mean()),
            "tw_rt_bp": tw_rt,
            "gate_3x_rt": gate,
            "gate_3x_rt_stress50": gate_s,
            "pass_3x": bool(mean_b >= gate),
            "pass_stress50": bool(mean_b >= gate_s),
            "stop_rate": float(np.mean([t["exit"] == "stop" for t in trades])),
            "target_rate": float(np.mean([t["exit"] == "target" for t in trades])),
            "by_sym": by_sym,
            "verdict": verdict,
        }
    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
