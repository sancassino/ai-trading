"""I5: robuustheid FTMO-RSI(2) per jaar/regime, volgens PREREG_I5.md."""
import math, statistics
from collections import defaultdict
import e1_rsi2_ftmo as e1
import stats_tools as st
sl = [e1.ftmo_sleeve(s)[0] for s in e1.SWAP_LONG]
p = e1.pooled(sl)
r = dict(p)
days = [d for d, _ in p]
print(f"volledig 2021–26: SR {st.sharpe(list(r.values()))[0]:.2f}")
yr = defaultdict(list)
for d, x in p: yr[d.year].append(x)
ysr = {y: st.sharpe(v)[0] for y, v in yr.items()}
yret = {y: math.prod(1 + x for x in v) - 1 for y, v in yr.items()}
print("per jaar (SR / rendement): " + " ".join(f"{y}:{ysr[y]:+.2f}/{yret[y]*100:+.1f}%" for y in sorted(yr)))
best = max(yret, key=yret.get)
ex = [x for d, x in p if d.year != best]
print(f"excl. beste jaar ({best}): SR {st.sharpe(ex)[0]:.2f} → {'OK (≥ 0,4)' if st.sharpe(ex)[0] >= 0.4 else 'AFHANKELIJK VAN ÉÉN JAAR'}")
print(f"2026 tot nu: SR {ysr.get(2026, float('nan')):.2f}, rendement {yret.get(2026, 0)*100:+.1f}%")
roll = []
for i, d in enumerate(days):
    if d.day > 7 or (roll and roll[-1][0].month == d.month): continue
    w = [x for dd, x in p if 0 < (d - dd).days <= 365]
    if len(w) > 200: roll.append((d, st.sharpe(w)[0]))
print("rollende 12-mnd SR (per kwartaal): " + " ".join(f"{d:%y-%m}:{s:+.1f}" for d, s in roll if d.month in (1, 4, 7, 10)))
us = e1.ftmo_close("US500cash"); c = [x[1] for x in us]; ud = [x[0] for x in us]
rv = {}
for i in range(21, len(c)):
    rv[ud[i]] = statistics.stdev([c[j] / c[j - 1] - 1 for j in range(i - 19, i + 1)])
vals = sorted(rv[d] for d in days if d in rv)
t1, t2 = vals[len(vals) // 3], vals[2 * len(vals) // 3]
reg = defaultdict(list)
for d, x in p:
    if d in rv: reg["laag" if rv[d] <= t1 else ("midden" if rv[d] <= t2 else "hoog")].append(x)
print("per volregime (US500 20d-vol tercielen): " + " ".join(f"{k}: SR {st.sharpe(v)[0]:+.2f} (N {len(v)})" for k, v in reg.items()))
