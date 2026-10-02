#!/usr/bin/env python3
"""A4 PRE-trial kostenpoort for PREREG_FTMO_C17 — TRAIN 2021–2023 ONLY.

NOT a formal trial. Does not touch catalogus/TRIALS.csv or 2025→ reserve.

Gate (PREREG §1 / §4): median bruto per trade (bp) >= 3 × round-trip cost incl. swap.
Cost per trade = roundtrip_intraday_bp + n_nights * swap_long_bp_per_nacht
  (also report +50% swap sensitivity per PREREG).

Positions: identical WINDOWS logic to catalogus/C17_fomc_cycle.py (bevroren regel).
Universe: US500cash, US100cash, GER40cash (D1).
"""
from __future__ import annotations

import bisect
import csv
import json
from datetime import date, timedelta
from pathlib import Path

import numpy as np

TRAIN_START = date(2021, 1, 1)
TRAIN_END = date(2023, 12, 31)
# hard cap — never peek reserve
HARD_CAP = date(2024, 12, 31)

SYMBOLS = ["US500cash", "US100cash", "GER40cash"]
WINDOWS = [(-1, 4), (9, 14), (19, 24), (29, 34)]  # C17 catalogus


def load_fomc() -> list[date]:
    ds = set()
    for path in ("data/fomc_dates.csv", "fomc_dates_1994_2020.txt", "events.csv"):
        p = Path(path)
        if not p.exists():
            continue
        for line in p.open():
            line = line.strip()
            if path.endswith("events.csv"):
                f = line.split(";")
                if len(f) >= 2 and f[1] == "FOMC" and f[0][:1].isdigit():
                    ds.add(date.fromisoformat(f[0][:10]))
            elif line[:1].isdigit():
                ds.add(date.fromisoformat(line.split(";")[0][:10]))
    return sorted(ds)


def load_daily(name: str) -> dict:
    path = Path(f"data/daily/{name}.csv")
    d, c = [], []
    for line in path.open():
        if not line[:1].isdigit():
            continue
        f = line.rstrip("\n").split(";")
        dd = date.fromisoformat(f[0])
        if dd > HARD_CAP:
            continue  # reserve 2025→ onaangeraakt
        d.append(dd)
        c.append(float(f[4]))  # close
    return {"date": np.array(d, dtype=object), "close": np.array(c, dtype=float), "name": name}


def load_costs() -> dict[str, dict]:
    out = {}
    with open("COSTS_FTMO.csv") as f:
        rows = csv.DictReader((l for l in f if not l.startswith("#")), delimiter=";")
        for r in rows:
            out[r["symbol"]] = {
                "rt": float(r["roundtrip_intraday_bp"]),
                "swap_long": float(r["swap_long_bp_per_nacht"]),
                "swap_short": float(r["swap_short_bp_per_nacht"]),
            }
    return out


def positions_c17(cal: list[date], fomc: list[date]) -> np.ndarray:
    """pos[t] = exposure after close t (same as catalogus/C17_fomc_cycle)."""
    fidx = sorted({bisect.bisect_left(cal, f) for f in fomc if f >= cal[0] and bisect.bisect_left(cal, f) < len(cal)})
    pos = np.zeros(len(cal))
    for i, d in enumerate(cal):
        k = i  # cal is this instrument's calendar
        k1 = k + 1
        j = bisect.bisect_right(fidx, k1 + 1) - 1
        on = False
        for jj in (j, j + 1):
            if 0 <= jj < len(fidx):
                rel = k1 - fidx[jj]
                if any(a <= rel <= b for a, b in WINDOWS):
                    on = True
        pos[i] = 1.0 if on else 0.0
    return pos


def extract_trades(dates: np.ndarray, closes: np.ndarray, pos: np.ndarray):
    """Contiguous long blocks → (entry_date, exit_date, bruto_frac, nights)."""
    trades = []
    n = len(pos)
    i = 0
    while i < n:
        if pos[i] < 0.5:
            i += 1
            continue
        start = i
        while i < n and pos[i] >= 0.5:
            i += 1
        end_pos = i - 1  # last day with pos=1
        # returns accrue on days start+1 .. end_pos+1 (if exists)
        exit_i = end_pos + 1
        if exit_i >= n:
            # incomplete trade at series end — drop
            break
        entry_px = float(closes[start])
        exit_px = float(closes[exit_i])
        if entry_px <= 0:
            continue
        bruto = exit_px / entry_px - 1.0
        nights = (dates[exit_i] - dates[start]).days
        trades.append(
            {
                "entry": dates[start],
                "exit": dates[exit_i],
                "bruto": bruto,
                "bruto_bp": bruto * 1e4,
                "nights": nights,
                "entry_i": start,
                "exit_i": exit_i,
            }
        )
    return trades


def main():
    fomc = load_fomc()
    costs = load_costs()
    assert all(s in costs for s in SYMBOLS), f"missing costs for {SYMBOLS}"

    all_trades = []
    per_sym = {}

    for sym in SYMBOLS:
        df = load_daily(sym)
        cal = list(df["date"])
        pos = positions_c17(cal, fomc)
        trades = extract_trades(df["date"], df["close"], pos)
        # TRAIN filter: entry in 2021–2023 (trade must complete; exit may be early 2024 only if entry in train — keep exit<=HARD_CAP already)
        train_trades = [t for t in trades if TRAIN_START <= t["entry"] <= TRAIN_END and t["exit"] <= HARD_CAP]
        # stricter: only trades fully inside train window (exit also <= TRAIN_END) for clean train cost-gate
        train_trades = [t for t in train_trades if t["exit"] <= TRAIN_END]

        c = costs[sym]
        rows = []
        for t in train_trades:
            cost_bp = c["rt"] + t["nights"] * c["swap_long"]
            cost_bp_sens = c["rt"] + t["nights"] * c["swap_long"] * 1.5
            netto_bp = t["bruto_bp"] - cost_bp
            rows.append({**t, "symbol": sym, "cost_bp": cost_bp, "cost_bp_sens50": cost_bp_sens, "netto_bp": netto_bp})
            all_trades.append(rows[-1])

        bruto = np.array([r["bruto_bp"] for r in rows]) if rows else np.array([])
        cost = np.array([r["cost_bp"] for r in rows]) if rows else np.array([])
        netto = np.array([r["netto_bp"] for r in rows]) if rows else np.array([])
        med_bruto = float(np.median(bruto)) if len(bruto) else float("nan")
        med_cost = float(np.median(cost)) if len(cost) else float("nan")
        med_netto = float(np.median(netto)) if len(netto) else float("nan")
        # gate readings
        thr_3x_med_cost = 3.0 * med_cost if np.isfinite(med_cost) else float("nan")
        # per-trade: compare each trade's cost; primary = median(bruto) >= 3 * median(cost_incl_swap)
        # also: fraction of trades with bruto >= 3*own_cost
        pass_med = bool(med_bruto >= thr_3x_med_cost) if rows else False
        # alternate reading: median(netto) >= 0 and median(bruto) >= 3*median(cost)
        per_sym[sym] = {
            "n_trades": len(rows),
            "median_bruto_bp": med_bruto,
            "median_cost_bp": med_cost,
            "median_netto_bp": med_netto,
            "threshold_3x_median_cost_bp": thr_3x_med_cost,
            "gate_median_bruto_ge_3x_cost": pass_med,
            "mean_nights": float(np.mean([r["nights"] for r in rows])) if rows else float("nan"),
            "rt_bp": c["rt"],
            "swap_long_bp": c["swap_long"],
            "median_cost_sens50_bp": float(np.median([r["cost_bp_sens50"] for r in rows])) if rows else float("nan"),
        }

    bruto_all = np.array([t["bruto_bp"] for t in all_trades])
    cost_all = np.array([t["cost_bp"] for t in all_trades])
    netto_all = np.array([t["netto_bp"] for t in all_trades])
    med_b = float(np.median(bruto_all)) if len(bruto_all) else float("nan")
    med_c = float(np.median(cost_all)) if len(cost_all) else float("nan")
    med_n = float(np.median(netto_all)) if len(netto_all) else float("nan")
    thr = 3.0 * med_c if np.isfinite(med_c) else float("nan")
    # PREREG approx absolute threshold ~15 bp
    abs_thr = 15.0
    gate = bool(med_b >= thr) if len(bruto_all) else False
    gate_abs = bool(med_b >= abs_thr) if len(bruto_all) else False
    gate_sens = bool(med_b >= 3.0 * float(np.median([t["cost_bp_sens50"] for t in all_trades]))) if all_trades else False

    summary = {
        "label": "A4_C17_cost_gate_TRAIN_PRE_trial",
        "train_window": "2021-01-01..2023-12-31",
        "hard_cap": str(HARD_CAP),
        "reserve_2025": "ONAANGERAAKT",
        "n_trades_total": len(all_trades),
        "per_symbol": per_sym,
        "pooled": {
            "median_bruto_bp": med_b,
            "median_cost_bp_incl_swap": med_c,
            "median_netto_bp": med_n,
            "threshold_3x_median_cost_bp": thr,
            "prereg_approx_abs_threshold_bp": abs_thr,
            "gate_median_bruto_ge_3x_cost": gate,
            "gate_median_bruto_ge_15bp": gate_abs,
            "gate_sens_swap_plus50pct": gate_sens,
            "mean_nights": float(np.mean([t["nights"] for t in all_trades])) if all_trades else float("nan"),
        },
        "verdict": "PASS" if gate else "FAIL",
        "note": "PRE-trial cost-gate only. Formal trial blocked until Strateeg amends PREREG test window to ≤2024 / heel 2024.",
    }

    out_dir = Path("results/R2/a4_prep")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "cost_gate_c17_train.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")

    # trades CSV
    with (out_dir / "cost_gate_c17_train_trades.csv").open("w") as f:
        f.write("symbol;entry;exit;nights;bruto_bp;cost_bp;cost_bp_sens50;netto_bp\n")
        for t in all_trades:
            f.write(
                f"{t['symbol']};{t['entry']};{t['exit']};{t['nights']};"
                f"{t['bruto_bp']:.4f};{t['cost_bp']:.4f};{t['cost_bp_sens50']:.4f};{t['netto_bp']:.4f}\n"
            )

    # human markdown
    lines = [
        "# A4 C17 kostenpoort — TRAIN 2021–2023 (PRE-trial)",
        "",
        "**Label:** cost-gate/train PRE-trial — **NOT** a formal PREREG trial result.",
        "**Window:** entry & exit ∈ 2021-01-01 … 2023-12-31. Reserve 2025-01→ onaangeraakt.",
        "**Engine positions:** C17 WINDOWS (catalogus). **Costs:** COSTS_FTMO.csv RT + nights×swap_long.",
        "",
        f"## Verdict: **{summary['verdict']}** (median bruto {med_b:.2f} bp vs 3× median cost {thr:.2f} bp)",
        "",
        "| Symbol | N | med bruto bp | med cost bp | med netto bp | 3×cost | gate |",
        "|--------|---|--------------|-------------|--------------|--------|------|",
    ]
    for sym, s in per_sym.items():
        lines.append(
            f"| {sym} | {s['n_trades']} | {s['median_bruto_bp']:.2f} | {s['median_cost_bp']:.2f} | "
            f"{s['median_netto_bp']:.2f} | {s['threshold_3x_median_cost_bp']:.2f} | "
            f"{'PASS' if s['gate_median_bruto_ge_3x_cost'] else 'FAIL'} |"
        )
    lines += [
        "",
        f"- Pooled median bruto: **{med_b:.2f} bp**",
        f"- Pooled median cost (RT+swap): **{med_c:.2f} bp** (3× = {thr:.2f} bp)",
        f"- Pooled median netto: **{med_n:.2f} bp**",
        f"- Absolute PREREG ≈15 bp check: {'PASS' if gate_abs else 'FAIL'} ({med_b:.2f} vs 15)",
        f"- Swap +50% sensitivity gate: {'PASS' if gate_sens else 'FAIL'}",
        f"- Mean nights held: {summary['pooled']['mean_nights']:.2f}",
        "",
        "Formal trial / TRIALS.csv append: **blocked** until Strateeg amends PREREG_FTMO_C17 test section to ≤2024 / heel 2024.",
        "",
    ]
    (out_dir / "cost_gate_c17_train.md").write_text("\n".join(lines))

    print(json.dumps(summary, indent=2, default=str))
    print("\n" + "\n".join(lines))


if __name__ == "__main__":
    main()
