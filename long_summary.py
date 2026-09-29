"""Ensemble-samenvatting lange runs: gem. maandrendement over configs, per jaar, episodes, DD.
Gebruik: python3 long_summary.py 'results/long/LA_t?_l?_daily.csv' [label]"""
import glob, math, statistics, sys
from walk_forward import monthly_returns
files = sorted(glob.glob(sys.argv[1]))
runs = [monthly_returns(f) for f in files]
ms = sorted(set.intersection(*[set(r) for r in runs]))
ens = {m: statistics.mean(r[m] for r in runs) for m in ms}
eq, peak, dd = 1.0, 1.0, 0.0
yr = {}
for m in ms:
    eq *= 1 + ens[m]; peak = max(peak, eq); dd = max(dd, 1 - eq / peak)
    yr[m[:4]] = yr.get(m[:4], 1.0) * (1 + ens[m])
ep = lambda a, b: math.prod(1 + ens[m] for m in ms if a <= m <= b) - 1
n_pos = sum(v > 1 for v in yr.values())
cagr = eq ** (12 / len(ms)) - 1
print(f"{sys.argv[2] if len(sys.argv)>2 else ''} {len(files)} configs | CAGR {cagr*100:+.2f}%/jr (≈ €{cagr*80000/12:,.0f}/mnd op €80k) | jaren+ {n_pos}/{len(yr)} ({n_pos/len(yr)*100:.0f}%) | maand-DD {dd*100:.1f}%")
print("   episodes: 2000-02 {:+.1f}% | 2008 {:+.1f}% | 2020-Q1 {:+.1f}% | 2022 {:+.1f}% | 2021-26 {:+.1f}%".format(
    ep('2000.01','2002.12')*100, ep('2008.01','2008.12')*100, ep('2020.01','2020.03')*100, ep('2022.01','2022.12')*100, ep('2021.01','2026.09')*100))
print("   per jaar: " + " ".join(f"{y[2:]}:{(v-1)*100:+.1f}" for y, v in yr.items()))
