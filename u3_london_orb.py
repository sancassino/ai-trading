"""U3: London-open ORB (b4_sim.run_orb ongewijzigd) op EURUSD/GBPUSD, volgens PREREG_U3.md."""
import math
from collections import defaultdict
from datetime import datetime
import numpy as np
import b4_sim

COMM = {"EURUSD": 2.25 / (100000 * 1.0), "GBPUSD": 2.25 / (100000 * 1.17)}
for s in COMM:
    b4_sim.SYMS[s] = ("Europe/London", (8, 0), (17, 0), COMM[s])


def trades(mult=1.0, zero=False):
    out = []
    for s in COMM:
        sess = b4_sim.sessions(s)
        if zero or mult != 1.0:
            sess = [(d, [b[:5] + (0.0 if zero else b[5] * mult,) for b in bars]) for d, bars in sess]
        out += [(d, s, n) for d, n, _ in b4_sim.run_orb(sess, 0.0 if zero else COMM[s])]
    return out


def ct(tr):
    by = defaultdict(list)
    for d, _, n in tr:
        by[d].append(n)
    x = np.array([np.mean(v) for v in by.values()])
    return x.mean() / x.std(ddof=1) * math.sqrt(len(x)), by


net, gross, n50 = trades(), trades(zero=True), trades(1.5)
g = {(d, s): n for d, s, n in gross}
train = [x for x in net if x[0].year <= 2023]; test = [x for x in net if x[0].year >= 2024]
gm = np.mean([g[(d, s)] for d, s, _ in train]) * 1e4; cm = gm - np.mean([n for *_, n in train]) * 1e4
gate = gm >= 3 * cm
print(f"U3 London-open ORB: N {len(net)} | poort train: bruto {gm:+.2f} bp vs 3× kosten {3*cm:.2f} bp → {'DOOR' if gate else 'STOP (geen trial)'}")
t_tr, _ = ct(train); t_te, _ = ct(test); t50, _ = ct([x for x in n50 if x[0].year >= 2024]); t_all, by = ct(net)
x = np.array([n for *_, n in net])
print(f"   netto: train {np.mean([n for *_, n in train])*1e4:+.2f} bp (dag-t {t_tr:+.2f}, N {len(train)}) | test {np.mean([n for *_, n in test])*1e4:+.2f} bp (dag-t {t_te:+.2f}, N {len(test)}) | +50% spread test dag-t {t50:+.2f} | per-trade t {x.mean()/x.std(ddof=1)*math.sqrt(len(x)):+.2f}")
yr = defaultdict(list); per = defaultdict(list)
for d, s, n in net:
    yr[d.year].append(n); per[s].append(n)
print("   per jaar: " + " ".join(f"{y}:{np.mean(v)*1e4:+.2f}({len(v)})" for y, v in sorted(yr.items())))
print("   per symbool: " + " ".join(f"{s}:{np.mean(v)*1e4:+.2f} bp/t {np.mean(v)/np.std(v, ddof=1)*math.sqrt(len(v)):+.2f}" for s, v in per.items()))
dm = np.array([np.mean(v) for v in by.values()])
print(f"   dagreeks (gelijk gewogen): SR {dm.mean()/dm.std()*math.sqrt(252):+.2f} | skew {float(((dm-dm.mean())**3).mean()/dm.std()**3):+.2f}")
ok = gate and t_tr >= 3 and t_te >= 3 and len(net) >= 500 and t50 >= 2
print(f"   → {'GESLAAGD' if ok else 'AFGEWEZEN'}")
