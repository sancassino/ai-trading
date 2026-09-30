"""A2 kostenpoort TRAIN — PREREG_FTMO_A2 (variant b only). Geen 2025 in poort."""
from __future__ import annotations

import csv
import gzip
import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
M5GZ = ROOT / "data" / "m5gz"
OUT = Path(__file__).resolve().parent
COMM = 0.00002  # 0.20 bp/kant
TRAIN_Y0, TRAIN_Y1 = 2021, 2023


def load_gz(sym: str):
    path = M5GZ / f"{sym}.csv.gz"
    point, bars = None, []
    with gzip.open(path, "rt") as f:
        for line in f:
            if line.startswith("#"):
                point = float(line.split("point=")[1].split(";")[0])
                continue
            if not line or not line[0].isdigit():
                continue
            t, o, h, l, c, sp = line.rstrip().split(";")
            bars.append(
                (
                    datetime.strptime(t, "%Y.%m.%d %H:%M"),
                    float(o),
                    float(h),
                    float(l),
                    float(c),
                    int(sp) * point,
                )
            )
    return bars


def sessions(sym: str):
    by = defaultdict(list)
    for b in load_gz(sym):
        ny = b[0] - timedelta(hours=7)
        by[ny.date()].append((ny,) + b[1:])
    return [(d, by[d]) for d in sorted(by) if len(by[d]) >= 60]


def load_events():
    ev = defaultdict(list)
    for line in open(ROOT / "earnings.csv"):
        if line[0] in "#s":
            continue
        s, ts = line.strip().split(";")
        ev[s].append(datetime.strptime(ts, "%Y-%m-%d %H:%M"))
    return ev


def load_costs():
    costs = {}
    with open(ROOT / "COSTS_FTMO_alle.csv") as f:
        lines = [ln for ln in f if ln.strip() and not ln.startswith("#")]
    for row in csv.DictReader(lines, delimiter=";"):
        costs[row["symbol"]] = float(row["rondreis_bp"])
    return costs


def trades_for(sym, ev, costs):
    """Variant b: OR-richting, stop = 10% ATR14, EOD. Returns train-window trades."""
    sess = sessions(sym)
    dates = [d for d, _ in sess]
    idx = {d: i for i, d in enumerate(dates)}
    trade_days = set()
    for t in ev.get(sym, []):
        if t.hour * 60 + t.minute <= 9 * 60 + 30:
            d = t.date()
            if d in idx:
                trade_days.add(idx[d])
        else:
            j = next((i for i, d in enumerate(dates) if d > t.date()), None)
            if j is not None:
                trade_days.add(j)
    out = []
    rt_table = costs.get(sym)
    for i in sorted(trade_days):
        if i < 15:
            continue
        d = dates[i]
        if d.year < TRAIN_Y0 or d.year > TRAIN_Y1:
            continue
        tr = []
        for k in range(i - 14, i):
            s_prev, s_cur = sess[k - 1][1], sess[k][1]
            hi = max(b[2] for b in s_cur)
            lo = min(b[3] for b in s_cur)
            pc = s_prev[-1][4]
            tr.append(max(hi - lo, abs(hi - pc), abs(lo - pc)))
        atr = float(np.mean(tr))
        _, s = sess[i]
        orb = s[0]
        if orb[4] == orb[1]:
            continue
        side = 1 if orb[4] > orb[1] else -1
        level = orb[2] if side > 0 else orb[3]
        end = len(s) - 1
        entry = None
        exit_p = xk = ek = stop = None
        for k in range(1, end + 1):
            b = s[k]
            if entry is None:
                if (side > 0 and b[2] >= level) or (side < 0 and b[3] <= level):
                    entry = max(level, b[1]) if side > 0 else min(level, b[1])
                    ek = k
                    stop = entry - side * 0.10 * atr
                    if (side > 0 and b[3] <= stop) or (side < 0 and b[2] >= stop):
                        exit_p, xk = stop, k
                        break
                continue
            if (side > 0 and b[3] <= stop) or (side < 0 and b[2] >= stop):
                exit_p = min(stop, b[1]) if side > 0 else max(stop, b[1])
                xk = k
                break
        else:
            if entry is None:
                continue
            exit_p, xk = s[end][4], end
        if entry is None:
            continue
        gross = side * (exit_p / entry - 1)
        bar_cost = (s[ek][5] if side > 0 else s[xk][5]) / entry + 2 * COMM
        out.append(
            {
                "date": d.isoformat(),
                "year": d.year,
                "sym": sym,
                "gross_bp": gross * 1e4,
                "bar_cost_bp": bar_cost * 1e4,
                "table_rt_bp": rt_table if rt_table is not None else float("nan"),
            }
        )
    return out


def main():
    syms = open(ROOT / "universe_us41.txt").read().strip().split(",")
    ev = load_events()
    costs = load_costs()

    # Coverage (no P&L)
    cov_rows = []
    missing_m5 = []
    for s in syms:
        if not (M5GZ / f"{s}.csv.gz").exists():
            missing_m5.append(s)
            continue
        by_y = Counter(t.year for t in ev.get(s, []))
        cov_rows.append(
            {
                "sym": s,
                "ev_2021": by_y.get(2021, 0),
                "ev_2022": by_y.get(2022, 0),
                "ev_2023": by_y.get(2023, 0),
                "ev_2024": by_y.get(2024, 0),
                "m5": "yes",
                "rondreis_bp": costs.get(s, float("nan")),
            }
        )

    print(f"universe={len(syms)} missing_m5={missing_m5}")
    trades = []
    for s in syms:
        if s in missing_m5:
            continue
        print(f"sim {s} ...", flush=True)
        trades.extend(trades_for(s, ev, costs))

    n = len(trades)
    if n == 0:
        raise SystemExit("no train trades")

    g = np.array([t["gross_bp"] for t in trades])
    rt = np.array([t["table_rt_bp"] for t in trades])
    bar_c = np.array([t["bar_cost_bp"] for t in trades])
    mean_g = float(g.mean())
    med_g = float(np.median(g))
    mean_rt = float(np.nanmean(rt))
    mean_bar = float(bar_c.mean())
    gate_thresh = 3.0 * mean_rt
    pass_gate = mean_g >= gate_thresh

    # D-012 tail check (informative): mean without top-5% winners
    thr = np.quantile(g, 0.95)
    g_notop = g[g <= thr]
    mean_notop = float(g_notop.mean()) if len(g_notop) else float("nan")

    # +50% spread sensitivity on table RT
    gate_stress = mean_g >= 3.0 * mean_rt * 1.5

    by_year = {}
    for y in (2021, 2022, 2023):
        gy = g[[t["year"] == y for t in trades]]
        by_year[y] = {
            "n": int(len(gy)),
            "mean_bruto_bp": float(gy.mean()) if len(gy) else None,
            "median_bruto_bp": float(np.median(gy)) if len(gy) else None,
        }

    result = {
        "prereg": "PREREG_FTMO_A2",
        "variant": "b (stop=10% ATR14, OR-direction, EOD)",
        "train": "2021-01-01..2023-12-31",
        "reserve_2025": "onaangeraakt",
        "n_trades": n,
        "missing_m5": missing_m5,
        "mean_bruto_bp": mean_g,
        "median_bruto_bp": med_g,
        "mean_table_rt_bp": mean_rt,
        "gate_3x_mean_rt_bp": gate_thresh,
        "mean_bar_cost_bp": mean_bar,
        "mean_bruto_without_top5pct_winners_bp": mean_notop,
        "pass_mean_gate": pass_gate,
        "pass_plus50pct_spread_sensitivity": gate_stress,
        "by_year": by_year,
        "verdict": "PASS" if pass_gate else "FAIL",
    }

    with open(OUT / "cost_gate_a2_train.json", "w") as f:
        json.dump(result, f, indent=2)
    with open(OUT / "cost_gate_a2_train.csv", "w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["date", "year", "sym", "gross_bp", "bar_cost_bp", "table_rt_bp"],
        )
        w.writeheader()
        w.writerows(trades)
    with open(OUT / "coverage_a2.csv", "w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "sym",
                "ev_2021",
                "ev_2022",
                "ev_2023",
                "ev_2024",
                "m5",
                "rondreis_bp",
            ],
        )
        w.writeheader()
        w.writerows(cov_rows)

    md = f"""# A2 kostenpoort TRAIN — PREREG_FTMO_A2

- Variant: **b** (OR-richting, stop 10% ATR14, EOD; enige bindende)
- Train: 2021-01-01 … 2023-12-31 (geen 2024/2025 in poort)
- Data: `data/m5gz/` US41 + `earnings.csv` + `COSTS_FTMO_alle.csv`
- N trades: **{n}**
- Mean bruto: **{mean_g:+.2f} bp** | median bruto: **{med_g:+.2f} bp**
- Trade-gewogen mean rondreis (tabel): **{mean_rt:.2f} bp** → 3× = **{gate_thresh:.2f} bp**
- Mean bar-spread+comm (informatief): {mean_bar:.2f} bp
- Mean bruto zonder top-5% winnaars (D-012 staart, informatief): {mean_notop:+.2f} bp
- +50% spread-poort (gevoeligheid): {'PASS' if gate_stress else 'FAIL'}
- **Verdict (mean bruto ≥ 3× mean RT): {result['verdict']}**

## Per jaar (train)

| Jaar | N | mean bruto bp | median bruto bp |
|-----:|--:|--------------:|----------------:|
| 2021 | {by_year[2021]['n']} | {by_year[2021]['mean_bruto_bp']:+.2f} | {by_year[2021]['median_bruto_bp']:+.2f} |
| 2022 | {by_year[2022]['n']} | {by_year[2022]['mean_bruto_bp']:+.2f} | {by_year[2022]['median_bruto_bp']:+.2f} |
| 2023 | {by_year[2023]['n']} | {by_year[2023]['mean_bruto_bp']:+.2f} | {by_year[2023]['median_bruto_bp']:+.2f} |

Reserve 2025→: **onaangeraakt**. Bij FAIL: STOP, TRIALS append `stop:kostenpoort`, geen TRIAL_COUNT++, geen ftmo_ev().
"""
    (OUT / "cost_gate_a2_train.md").write_text(md)
    print(md)
    print("JSON:", result)


if __name__ == "__main__":
    main()
