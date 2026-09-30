import sys; sys.path.insert(0,".")
import numpy as np, pandas as pd
from audit.common import load
px = {"SPY": load("SPY","adjclose"), "GOLD": load("GOLD_F","close"), "BOND": load("BOND10_SYN","adjclose","data/derived")}
cal = pd.DatetimeIndex(sorted(set().union(*[set(v.index) for v in px.values()])))
cal = cal[(cal>="2000-09-01")&(cal<="2024-12-31")]
print("union dagen", len(cal))
for k,v in px.items():
    miss = cal.difference(v.index); print(k, "ontbrekende union-dagen:", len(miss), "voorbeelden", [str(x.date()) for x in miss[:8]])
# maandeinden in de unie-kalender
cl = pd.DatetimeIndex(sorted(set().union(*[set(v.index) for v in px.values()])))
me = pd.Series(cl, index=cl).groupby([cl.year, cl.month]).tail(1).index
ret = {k: set(v.index[1:]) for k,v in px.items()}
cnt = {0:0,1:0,2:0,3:0}; bad=[]
cli = list(cl)
for d in me:
    k = cli.index(d)
    if k < 61 or d.year < 2001 or d > pd.Timestamp("2024-12-31"): continue
    win = cli[k-60:k+1]
    avail = [n for n in px if all(x in ret[n] for x in win[1:])]
    cnt[len(avail)] += 1
    if len(avail) < 3: bad.append((str(d.date()), [n for n in px if n not in avail]))
print("aantal assets beschikbaar per maandeinde (engine-logica):", cnt)
print("maanden met drop:", bad[:40])
