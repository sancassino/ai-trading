#!/usr/bin/env python3
"""S2-GER40 PRE-trial kostenpoort — PREREG_S2_GER40_OPEN, TRAIN 2021–2023 ONLY.

data/m5gz/GER40cash.csv.gz. No 2025→. Rule: pre-range 08:00–09:00 CET;
close-break 09:00–09:30; stop = stricter of mid or 1×ATR(14,D1); flat 15:15;
SMA(20,D1) trend filter. Poort: mean bruto ≥ 2× RT AND costs < 50% bruto; +50% stress.
"""
from __future__ import annotations

import csv, gzip, json
from collections import defaultdict
from datetime import datetime, timedelta, date
from pathlib import Path
from zoneinfo import ZoneInfo
import numpy as np

NY = ZoneInfo("America/New_York")
CET = ZoneInfo("Europe/Amsterdam")
SYM = "GER40cash"
COMM_EUR = 3.0  # typical index; refine via COSTS if needed — use bar spread + COSTS RT
# COSTS_FTMO GER40cash roundtrip ~0.72 bp; commission in that figure
RT_FIXED_BP = 0.72
TRAIN_START = date(2021, 1, 1)
TRAIN_END = date(2023, 12, 31)
OUT_DIR = Path("results/cto/s2_ger40_prep")


def server_to_cet(server: datetime) -> datetime:
    return (server - timedelta(hours=7)).replace(tzinfo=NY).astimezone(CET)


def load_gz(sym: str):
    point = None
    bars = []
    for line in gzip.open(f"data/m5gz/{sym}.csv.gz", "rt"):
        if line.startswith("#"):
            point = float(line.split("point=")[1].split(";")[0])
            # contract from header if present
            continue
        if not line or not line[0].isdigit():
            continue
        t, o, h, l, c, sp = line.rstrip().split(";")
        server = datetime.strptime(t, "%Y.%m.%d %H:%M")
        local = server_to_cet(server)
        if local.year >= 2025 or local.year < 2021:
            continue
        bars.append({"local": local, "o": float(o), "h": float(h), "l": float(l), "c": float(c), "spread": int(sp) * point})
    return bars


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    bars = load_gz(SYM)
    print(f"loaded {len(bars)} bars")
    by_day = defaultdict(list)
    for b in bars:
        by_day[b["local"].date()].append(b)
    days = sorted(by_day)

    # D1 closes + ATR(14,D1) + SMA(20)
    d1 = []
    for d in days:
        db = sorted(by_day[d], key=lambda x: x["local"])
        d1.append({"date": d, "o": db[0]["o"], "h": max(x["h"] for x in db), "l": min(x["l"] for x in db), "c": db[-1]["c"]})
    d1_by = {x["date"]: x for x in d1}
    closes = [x["c"] for x in d1]
    # daily TR / ATR
    dtr = []
    for i, x in enumerate(d1):
        if i == 0:
            dtr.append(x["h"] - x["l"])
        else:
            pc = d1[i - 1]["c"]
            dtr.append(max(x["h"] - x["l"], abs(x["h"] - pc), abs(x["l"] - pc)))

    rows = []
    for i, d in enumerate(days):
        if d < TRAIN_START or d > TRAIN_END:
            continue
        if i < 20:
            continue
        sma20 = float(np.mean(closes[i - 20 : i]))  # prior 20 closes (exclude today)
        prev_c = closes[i - 1]
        atr_d1 = float(np.mean(dtr[i - 14 : i])) if i >= 14 else None
        if atr_d1 is None or atr_d1 <= 0:
            continue
        allow_long = prev_c > sma20
        allow_short = prev_c < sma20
        if not (allow_long or allow_short):
            continue

        day_bars = sorted(by_day[d], key=lambda x: x["local"])
        pre = [b for b in day_bars if b["local"].hour == 8]
        post = [b for b in day_bars if (b["local"].hour == 9 and b["local"].minute < 30)]
        rest = [b for b in day_bars if (b["local"].hour == 9 and b["local"].minute >= 30) or (10 <= b["local"].hour < 15) or (b["local"].hour == 15 and b["local"].minute < 15)]
        if len(pre) < 10 or not post:
            continue
        if not (pre[0]["local"].hour == 8 and pre[0]["local"].minute == 0):
            continue
        rh = max(b["h"] for b in pre)
        rl = min(b["l"] for b in pre)
        mid = 0.5 * (rh + rl)
        if rh <= rl:
            continue

        trade = None
        for b in post:
            up = b["c"] > rh
            dn = b["c"] < rl
            if up and dn:
                break
            if up and dn:
                break
            if not (up or dn):
                continue
            if up and dn:
                break
            # exclusive
            if up and dn:
                pass
            if up and not dn:
                if not allow_long:
                    break
                side = 1
                entry = b["c"]
            elif dn and not up:
                if not allow_short:
                    break
                side = -1
                entry = b["c"]
            else:
                break
            stop_mid = mid
            stop_atr = entry - atr_d1 if side > 0 else entry + atr_d1
            # stricter = closer to entry
            if side > 0:
                stop = max(stop_mid, stop_atr)
            else:
                stop = min(stop_mid, stop_atr)
            seq = [b] + [x for x in post if x["local"] > b["local"]] + rest
            exit_p = None
            exit_bar = None
            for eb in seq:
                if side > 0 and eb["l"] <= stop:
                    exit_p, exit_bar = stop, eb
                    break
                if side < 0 and eb["h"] >= stop:
                    exit_p, exit_bar = stop, eb
                    break
            if exit_p is None:
                exit_bar = seq[-1] if seq else b
                exit_p = exit_bar["c"]
            gross = side * (exit_p - entry) / entry
            spread_frac = b["spread"] / entry if entry else 0
            # commission baked into COSTS RT; use bar spread as variable + fixed remainder to hit ~0.72 when spread small
            # Prefer: cost = max(bar_spread_bp, RT_FIXED) style — use bar spread only + assume RT covers commission
            # A5 used spread + 2*comm. For index, COSTS says roundtrip 0.72 includes commission.
            cost_bp = max(spread_frac * 1e4, RT_FIXED_BP)
            cost_stress_bp = max(1.5 * spread_frac * 1e4, 1.5 * RT_FIXED_BP)
            trade = {
                "date": str(d),
                "symbol": SYM,
                "side": side,
                "gross_bp": gross * 1e4,
                "cost_bp": cost_bp,
                "cost_stress_bp": cost_stress_bp,
                "net_bp": gross * 1e4 - cost_bp,
                "entry_t": str(b["local"]),
                "exit_t": str(exit_bar["local"]),
            }
            break
        if trade:
            rows.append(trade)

    if not rows:
        raise SystemExit("no trades")
    g = np.array([r["gross_bp"] for r in rows])
    c = np.array([r["cost_bp"] for r in rows])
    cs = np.array([r["cost_stress_bp"] for r in rows])
    mean_g, mean_c, mean_cs = float(np.mean(g)), float(np.mean(c)), float(np.mean(cs))
    med_g = float(np.median(g))
    gate_2x = mean_g >= 2 * mean_c
    gate_share = (mean_c < 0.5 * mean_g) if mean_g > 0 else False
    gate_s2x = mean_g >= 2 * mean_cs
    gate_sshare = (mean_cs < 0.5 * mean_g) if mean_g > 0 else False
    verdict = "PASS" if (gate_2x and gate_share and gate_s2x and gate_sshare) else "FAIL"
    summary = {
        "n_trades": len(rows),
        "symbol": SYM,
        "train": "2021-01-01..2023-12-31",
        "prereg": "PREREG_S2_GER40_OPEN",
        "mean_gross_bp": mean_g,
        "median_gross_bp": med_g,
        "mean_cost_bp": mean_c,
        "mean_cost_stress_bp": mean_cs,
        "gate_2x_realized": gate_2x,
        "gate_cost_share_lt_50pct": gate_share,
        "gate_stress_2x": gate_s2x,
        "gate_stress_share_lt_50pct": gate_sshare,
        "verdict": verdict,
        "reserve_2025_touched": False,
    }
    with open(OUT_DIR / "cost_gate_s2_ger40_train.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    (OUT_DIR / "cost_gate_s2_ger40_train.json").write_text(json.dumps(summary, indent=2) + "\n")
    (OUT_DIR / "cost_gate_s2_ger40_train.md").write_text(
        f"# S2-GER40 kostenpoort TRAIN\n\nN={len(rows)} mean_bruto={mean_g:+.2f}bp mean_cost={mean_c:.2f}bp **{verdict}**\n\nReserve 2025→ onaangeraakt.\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
