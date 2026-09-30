"""S9 stap 1 (diagnose, geen trial, mag geen regel wijzigen): ORB-B4a- en S1(a)-trades per 20d-RV-terciel (t−1, eigen 252d-historie)."""
import math
from collections import defaultdict
from datetime import datetime
import numpy as np
import b4_sim, s1_noise


def regime(sym):
    sess = b4_sim.sessions(sym)
    cl = np.array([s[-1][4] for _, s in sess]); r = np.r_[np.nan, np.log(cl[1:] / cl[:-1])]
    rv = np.array([np.std(r[max(1, i - 20):i], ddof=1) if i > 21 else np.nan for i in range(len(r))])  # t.e.m. t−1
    out = {}
    for i, (d, _) in enumerate(sess):
        hist = rv[max(0, i - 252):i]; hist = hist[np.isfinite(hist)]
        if len(hist) < 120 or not np.isfinite(rv[i]):
            continue
        q1, q2 = np.percentile(hist, [100 / 3, 200 / 3])
        out[d] = 0 if rv[i] <= q1 else (1 if rv[i] <= q2 else 2)
    return out


def report(name, trades):
    by = defaultdict(list); byday = defaultdict(lambda: defaultdict(list)); yr = defaultdict(lambda: defaultdict(list))
    for d, s, n, reg in trades:
        by[reg].append(n); byday[reg][d].append(n); yr[d.year][reg].append(n)
    print(f"\n{name}:")
    for reg, lab in ((0, "laag"), (1, "midden"), (2, "hoog")):
        x = np.array(by[reg]); dm = np.array([np.mean(v) for v in byday[reg].values()])
        print(f"  {lab:<6} N {len(x):>5} | {x.mean()*1e4:+.2f} bp/trade | dag-geclusterde t {dm.mean()/dm.std(ddof=1)*math.sqrt(len(dm)):+.2f}")
    print("  per jaar (laag/midden/hoog bp, N hoog): " + " ".join(
        f"{y}:{'/'.join(f'{np.mean(v[k])*1e4:+.1f}' if v[k] else 'n.v.t.' for k in (0, 1, 2))}({len(v[2])})" for y, v in sorted(yr.items())))


regs = {s: regime(s) for s in b4_sim.SYMS}
orb = []
for line in open("results/b4/B4_a_ORB_trades.csv"):
    if line[0].isdigit():
        d, s, n, _ = line.strip().split(";"); d = datetime.strptime(d, "%Y-%m-%d").date()
        if d in regs[s]:
            orb.append((d, s, float(n), regs[s][d]))
report("ORB-B4a (FTMO 2021–26, 5 symbolen)", orb)
s1 = []
for s in s1_noise.SYMS:
    trades, _ = s1_noise.run(s1_noise.prepare(s), 30, True, 14)
    s1 += [(d, s, g - c, regs[s][d]) for d, g, c in trades if d in regs[s]]
report("S1 variant (a) (FTMO 2021–26, 4 indices)", s1)
