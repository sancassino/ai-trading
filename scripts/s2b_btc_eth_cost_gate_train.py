#!/usr/bin/env python3
"""S2b BTC+ETH PRE-trial kostenpoort — PREREG_S2b_BTC_ETH, TRAIN 2021–2023 ONLY.

Same frozen rule as PREREG_S2_BTC_USOPEN per instrument (BTCUSD + ETHUSD).
COSTS bridge (CTO C-005): use COSTS_FTMO_alle.csv fixed RT —
  BTCUSD 1.25 bp, ETHUSD 7.98 bp — because COSTS_FTMO.csv lacks crypto rows.
Skips 2025→ at load. FAIL → STOP; no TRIALS append.
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
US100 = "US100cash"
# COSTS bridge: COSTS_FTMO_alle.csv rondreis_bp (CTO C-005)
RT = {"BTCUSD": 1.25, "ETHUSD": 7.98}
COMM_BP_SIDE = 0.20
TRAIN_START = date(2021, 1, 1)
TRAIN_END = date(2023, 12, 31)
OUT_DIR = Path("results/cto/s2b_btc_eth_prep")
RANGE_MIN = 0.0020
RANGE_MAX = 0.0150
GAP_MIN = 0.0015
SYMBOLS = ("BTCUSD", "ETHUSD")


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
                "spread": int(sp) * point,
            }
        )
    return bars


def us100_cash_gap(by_day_us, d: date):
    priors = sorted(x for x in by_day_us if x < d)
    if not priors:
        return None
    prev = priors[-1]
    prev_bars = sorted(by_day_us[prev], key=lambda b: b["local"])
    cash_close_candidates = [b for b in prev_bars if b["local"].hour < 22]
    if not cash_close_candidates:
        return None
    prev_close = cash_close_candidates[-1]["c"]
    day_bars = sorted(by_day_us[d], key=lambda b: b["local"])
    open_bars = [
        b
        for b in day_bars
        if (b["local"].hour == 15 and b["local"].minute >= 30) or b["local"].hour > 15
    ]
    if not open_bars or prev_close <= 0:
        return None
    return open_bars[0]["o"] / prev_close - 1.0


def trades_for_symbol(sym: str, by_sym, by_us):
    rows = []
    for d in sorted(by_sym):
        if d < TRAIN_START or d > TRAIN_END:
            continue
        if d not in by_us:
            continue
        gap = us100_cash_gap(by_us, d)
        if gap is None or abs(gap) < GAP_MIN:
            continue
        day_bars = sorted(by_sym[d], key=lambda x: x["local"])
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
            if side * gap <= 0:
                break
            entry = b["c"]
            stop = mid
            seq = [x for x in post_flat if x["local"] >= b["local"]]
            if not seq:
                break
            exit_p = None
            exit_bar = None
            for i, eb in enumerate(seq):
                if i == 0:
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
                flat_bars = [x for x in seq if x["local"].hour == 21 and x["local"].minute == 0]
                exit_bar = flat_bars[0] if flat_bars else seq[-1]
                exit_p = exit_bar["c"]
            gross = side * (exit_p - entry) / entry
            spread_frac = (b["spread"] / entry) if entry > 0 else 0.0
            comm_frac = 2 * COMM_BP_SIDE * 1e-4
            cost = spread_frac + comm_frac
            trade = {
                "date": str(d),
                "symbol": sym,
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
                "fixed_rt_bp": RT[sym],
                "entry_t": str(b["local"]),
                "exit_t": str(exit_bar["local"]),
            }
            break
        if trade:
            rows.append(trade)
    return rows


def leg_gates(rows, fixed_rt):
    if not rows:
        return {
            "n": 0,
            "mean_gross_bp": None,
            "mean_cost_bp": None,
            "mean_cost_stress_bp": None,
            "gate_2x_fixed": False,
            "gate_cost_share": False,
            "gate_stress_2x": False,
            "gate_stress_share": False,
            "pass": False,
            "reason": "no_trades",
        }
    g = np.array([r["gross_bp"] for r in rows])
    c = np.array([r["cost_bp"] for r in rows])
    cs = np.array([r["cost_stress_bp"] for r in rows])
    mean_g = float(np.mean(g))
    mean_c = float(np.mean(c))
    mean_cs = float(np.mean(cs))
    gate_2x_fixed = mean_g >= 2 * fixed_rt
    gate_cost_share = (mean_c < 0.5 * mean_g) if mean_g > 0 else False
    gate_stress_2x = mean_g >= 2 * mean_cs
    gate_stress_share = (mean_cs < 0.5 * mean_g) if mean_g > 0 else False
    ok = gate_2x_fixed and gate_cost_share and gate_stress_2x and gate_stress_share
    return {
        "n": len(rows),
        "mean_gross_bp": mean_g,
        "median_gross_bp": float(np.median(g)),
        "mean_cost_bp": mean_c,
        "mean_cost_stress_bp": mean_cs,
        "fixed_rt_bp": fixed_rt,
        "gate_2x_fixed": gate_2x_fixed,
        "gate_cost_share": gate_cost_share,
        "gate_stress_2x": gate_stress_2x,
        "gate_stress_share": gate_stress_share,
        "cost_share_pct": (100.0 * mean_c / mean_g) if mean_g else None,
        "pass": ok,
    }


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    us = load_gz(US100)
    by_us = defaultdict(list)
    for b in us:
        by_us[b["local"].date()].append(b)
    print(f"loaded US100 bars={len(us)} (2021–2024; 2025+ skipped)")

    all_rows = []
    per = {}
    for sym in SYMBOLS:
        bars = load_gz(sym)
        by_sym = defaultdict(list)
        for b in bars:
            by_sym[b["local"].date()].append(b)
        print(f"loaded {sym} bars={len(bars)}")
        rows = trades_for_symbol(sym, by_sym, by_us)
        all_rows.extend(rows)
        per[sym] = leg_gates(rows, RT[sym])
        print(f"  {sym}: N={per[sym]['n']} mean_g={per[sym]['mean_gross_bp']} pass={per[sym]['pass']}")

    # Pooled gates (PREREG §4.3)
    if all_rows:
        g = np.array([r["gross_bp"] for r in all_rows])
        c = np.array([r["cost_bp"] for r in all_rows])
        # trade-weighted fixed RT
        w_rt = np.array([r["fixed_rt_bp"] for r in all_rows])
        mean_g = float(np.mean(g))
        mean_c = float(np.mean(c))
        tw_rt = float(np.mean(w_rt))
        pooled_2x = mean_g >= 2 * tw_rt
        pooled_share = (mean_c < 0.5 * mean_g) if mean_g > 0 else False
    else:
        mean_g = mean_c = tw_rt = None
        pooled_2x = pooled_share = False

    power_ok = len(all_rows) >= 150
    eth_ok = per["ETHUSD"]["pass"]
    btc_ok = per["BTCUSD"]["pass"]
    # PREREG: ETH FAIL → S2b STOP; both legs + pooled + power
    verdict_pass = eth_ok and btc_ok and pooled_2x and pooled_share and power_ok
    reasons = []
    if not btc_ok:
        reasons.append("BTC_leg_FAIL")
    if not eth_ok:
        reasons.append("ETH_leg_FAIL")
    if not pooled_2x:
        reasons.append("pooled_2x_FAIL")
    if not pooled_share:
        reasons.append("pooled_cost_share_FAIL")
    if not power_ok:
        reasons.append("power_N_lt_150")
    verdict = "PASS" if verdict_pass else "FAIL"

    summary = {
        "prereg": "PREREG_S2b_BTC_ETH",
        "train": "2021-01-01..2023-12-31",
        "costs_bridge": "COSTS_FTMO_alle.csv (C-005); BTC=1.25 ETH=7.98 bp RT",
        "n_pooled": len(all_rows),
        "power_n_ge_150": power_ok,
        "legs": per,
        "pooled_mean_gross_bp": mean_g,
        "pooled_mean_cost_bp": mean_c,
        "pooled_trade_weighted_fixed_rt_bp": tw_rt,
        "pooled_gate_2x_tw_rt": pooled_2x,
        "pooled_gate_cost_share_lt_50pct": pooled_share,
        "verdict": verdict,
        "fail_reasons": reasons,
        "reserve_2025_touched": False,
        "note": "CTO wake S2b cost-gate; no TRIALS append on FAIL; ETH FAIL binds STOP per PREREG §4.4",
    }

    csv_path = OUT_DIR / "cost_gate_s2b_btc_eth_train.csv"
    if all_rows:
        with open(csv_path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
            w.writeheader()
            w.writerows(all_rows)
    json_path = OUT_DIR / "cost_gate_s2b_btc_eth_train.json"
    json_path.write_text(json.dumps(summary, indent=2) + "\n")

    def fmt_leg(sym, L):
        if L["n"] == 0:
            return f"- **{sym}**: N=0 → FAIL"
        return (
            f"- **{sym}**: N={L['n']}; mean bruto {L['mean_gross_bp']:+.2f} bp; "
            f"mean cost {L['mean_cost_bp']:.2f} bp; fixed RT {L['fixed_rt_bp']} bp (2×={2*L['fixed_rt_bp']:.2f}); "
            f"share {(L['cost_share_pct'] or float('nan')):.1f}%; "
            f"gates 2×fix={L['gate_2x_fixed']} share={L['gate_cost_share']} "
            f"stress2x={L['gate_stress_2x']} stress_share={L['gate_stress_share']} → "
            f"{'PASS' if L['pass'] else 'FAIL'}"
        )

    md = [
        "# S2b BTC+ETH kostenpoort TRAIN — PREREG_S2b_BTC_ETH",
        "",
        "- Train: 2021-01-01 … 2023-12-31 (geen 2025+)",
        "- Data: `data/m5gz/{BTCUSD,ETHUSD,US100cash}.csv.gz` (v41)",
        "- Regel: identiek parent S2-BTC_USOPEN per instrument; gepoold N",
        "- **COSTS bridge (C-005):** `COSTS_FTMO_alle.csv` BTC=1.25 / ETH=7.98 bp RT",
        f"- N pooled: **{len(all_rows)}** (power ≥150: {power_ok})",
        fmt_leg("BTCUSD", per["BTCUSD"]),
        fmt_leg("ETHUSD", per["ETHUSD"]),
        f"- Pooled mean bruto: **{(mean_g if mean_g is not None else float('nan')):+.2f} bp** | "
        f"mean cost {(mean_c if mean_c is not None else float('nan')):.2f} bp | "
        f"TW fixed RT {(tw_rt if tw_rt is not None else float('nan')):.2f} bp",
        f"- Pooled gates: 2×TW={pooled_2x} cost_share={pooled_share}",
        f"- Fail reasons: {', '.join(reasons) if reasons else '(none)'}",
        f"- **Verdict: {verdict}**",
        "",
        "Reserve 2025→: **onaangeraakt**. Geen TRIALS-append.",
        "",
    ]
    (OUT_DIR / "cost_gate_s2b_btc_eth_train.md").write_text("\n".join(md) + "\n")
    print(json.dumps(summary, indent=2))
    print(f"wrote {csv_path} {json_path}")


if __name__ == "__main__":
    main()
