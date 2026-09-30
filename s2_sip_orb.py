"""S2: Stocks-in-Play ORB (5-min, OR-richting, stop 10% ATR14, EOD) op earnings-dagen, 41 US-aandelen, volgens PREREG_S2.md."""
import math
from collections import defaultdict
from datetime import datetime, timedelta

import numpy as np

from b4_sim import load

SYMS = open("universe_us41.txt").read().strip().split(",")
COMM = 0.00002
VARIANTS = {"a": ("or", False, None), "b": ("atr", False, None), "c": ("atr", True, None), "d": ("atr", False, (12, 0))}


def sessions(sym):
    by = defaultdict(list)
    for b in load(sym):
        ny = b[0] - timedelta(hours=7)
        by[ny.date()].append((ny,) + b[1:])
    return [(d, by[d]) for d in sorted(by) if len(by[d]) >= 60]


def events():
    ev = defaultdict(list)
    for line in open("earnings.csv"):
        if line[0] in "#s":
            continue
        s, ts = line.strip().split(";")
        ev[s].append(datetime.strptime(ts, "%Y-%m-%d %H:%M"))
    return ev


def trades_for(sym, ev, variant, spread_mult=1.0):
    stop_kind, long_only, exit_at = VARIANTS[variant]
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
    for i in sorted(trade_days):
        if i < 15:
            continue
        # ATR14 (dag) uit de 14 vorige sessies
        tr = []
        for k in range(i - 14, i):
            s_prev, s_cur = sess[k - 1][1], sess[k][1]
            hi, lo, pc = max(b[2] for b in s_cur), min(b[3] for b in s_cur), s_prev[-1][4]
            tr.append(max(hi - lo, abs(hi - pc), abs(lo - pc)))
        atr = float(np.mean(tr))
        d, s = sess[i]
        orb = s[0]
        if orb[4] == orb[1]:
            continue
        side = 1 if orb[4] > orb[1] else -1
        if long_only and side < 0:
            continue
        level = orb[2] if side > 0 else orb[3]
        end = len(s) - 1
        if exit_at:
            end = max(k for k, b in enumerate(s) if (b[0].hour, b[0].minute) < exit_at)
        entry = None
        for k in range(1, end + 1):
            b = s[k]
            if entry is None:
                if (side > 0 and b[2] >= level) or (side < 0 and b[3] <= level):
                    entry = max(level, b[1]) if side > 0 else min(level, b[1]); ek = k
                    stop = (orb[3] if side > 0 else orb[2]) if stop_kind == "or" else entry - side * 0.10 * atr
                    # stop in dezelfde bar: conservatief geraakt als de bar er doorheen gaat
                    if (side > 0 and b[3] <= stop) or (side < 0 and b[2] >= stop):
                        exit_p, xk = stop, k; break
                continue
            if (side > 0 and b[3] <= stop) or (side < 0 and b[2] >= stop):
                exit_p = min(stop, b[1]) if side > 0 else max(stop, b[1]); xk = k; break
        else:
            if entry is None:
                continue
            exit_p, xk = s[end][4], end
        if entry is None:
            continue
        gross = side * (exit_p / entry - 1)
        cost = spread_mult * (s[ek][5] if side > 0 else s[xk][5]) / entry + 2 * COMM
        stopdist = abs(entry - stop) / entry
        out.append((d, sym, gross, cost, stopdist, s[ek][0]))
    return out


def tstat(x):
    x = np.asarray(x)
    return x.mean() / x.std(ddof=1) * math.sqrt(len(x)) if len(x) > 2 else float("nan")


def orb_daily():
    r, prev = {}, None
    for line in open("results/f/F2_ORB_daily.csv"):
        if line[0].isdigit():
            f = line.strip().split(";"); d = datetime.strptime(f[0], "%Y.%m.%d").date(); eq = float(f[4])
            if prev:
                r[d] = eq / prev - 1
            prev = eq
    return r


def main():
    ev = events(); orb = orb_daily()
    for v in VARIANTS:
        tr = [x for s in SYMS for x in trades_for(s, ev, v)]
        tr50 = [x for s in SYMS for x in trades_for(s, ev, v, 1.5)]
        train = [x for x in tr if x[0].year <= 2023]; test = [x for x in tr if x[0].year >= 2024]
        g = np.array([x[2] for x in train]) * 1e4
        gate = np.median(g) >= 8.7
        net = lambda xs: np.array([x[2] - x[3] for x in xs])
        yrs = defaultdict(list)
        for x in tr:
            yrs[x[0].year].append(x[2] - x[3])
        pos_y = sum(np.mean(y) > 0 for y in yrs.values())
        days_per_year = {y: len({x[0] for x in tr if x[0].year == y}) for y in yrs}
        # dagreeks: 1% risico per trade, ≤ 4×, max 5 gelijktijdig (eerste 5 instappen)
        by_day = defaultdict(list)
        for x in tr:
            by_day[x[0]].append(x)
        dd = {}
        for d, xs in by_day.items():
            xs = sorted(xs, key=lambda x: x[5])[:5]
            dd[d] = sum(min(4.0, 0.01 / max(x[4], 1e-9)) * (x[2] - x[3]) for x in xs)
        cal = sorted({d for d in orb})  # alle handelsdagen (0 zonder event)
        r = np.array([dd.get(d, 0.0) for d in cal])
        sr = r.mean() / r.std() * math.sqrt(252); sk = float((((r - r.mean()) / r.std()) ** 3).mean())
        corr = np.corrcoef(r, [orb[d] for d in cal])[0, 1]
        t_tr, t_te = tstat(net(train)), tstat(net(test)); t50 = tstat(net([x for x in tr50 if x[0].year >= 2024]))
        print(f"\nVariant ({v}): N {len(tr)} (train {len(train)}, test {len(test)}) | poort: mediaan-bruto train {np.median(g):+.1f} bp (gemiddeld {g.mean():+.1f}; kosten gem. {np.mean([x[3] for x in train])*1e4:.1f}) → {'DOOR' if gate else 'STOP (geen trial)'}")
        print(f"   netto bp/trade: train {net(train).mean()*1e4:+.1f} (t {t_tr:+.2f}) | test {net(test).mean()*1e4:+.1f} (t {t_te:+.2f}) | +50% spread test t {t50:+.2f} | trade-skew {float(((net(tr)-net(tr).mean())**3).mean()/net(tr).std()**3):+.2f} | winkans {np.mean(net(tr) > 0)*100:.0f}%")
        print("   per jaar: " + " ".join(f"{y}:{np.mean(z)*1e4:+.1f}({len(z)})" for y, z in sorted(yrs.items())) + f" → {pos_y}/6 positief | trade-dagen/jaar: " + " ".join(f"{y}:{n}" for y, n in sorted(days_per_year.items())))
        print(f"   dagreeks (1% risico, ≤ 4×, max 5): SR {sr:+.2f} | skew {sk:+.2f} | jaarvol {r.std()*math.sqrt(252)*100:.1f}% | slechtste dag {r.min()*100:.2f}% | corr ORB {corr:+.2f}")
        ok = gate and t_tr >= 3.5 and t_te >= 3.5 and len(train) >= 100 and len(test) >= 100 and pos_y >= 4 and t50 >= 2
        print(f"   → {'GESLAAGD' if ok else 'AFGEWEZEN'}" + ("" if gate else " (poort; overige cijfers informatief)"), flush=True)


if __name__ == "__main__":
    main()
