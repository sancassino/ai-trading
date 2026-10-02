"""Ongefilterd ORB B4a: FTMO-EV over hele historie en per periode (beschrijvend, geen nieuwe test)."""
import sys,pandas as pd,numpy as np
sys.path.insert(0,'/tmp/eng');from engine import ftmo as fm
T=pd.read_csv('/tmp/orb_trades.csv',sep=';',parse_dates=['date'])
for nm,a,b in (('2021-24','2021-01-01','2024-12-31'),('2025-26','2025-01-01','2026-09-30'),('alles','2021-01-01','2026-09-30')):
    s=T[(T.date>=a)&(T.date<=b)].groupby('date').net_frac.sum();idx=pd.bdate_range(a,b);r=s.reindex(idx).fillna(0).values
    print(nm,f'N={len(r)}d gem {r.mean()*1e4:+.1f}bp SR {r.mean()/r.std()*np.sqrt(252):+.2f}')
    for sc in (0.2,0.3,0.4):
        o=fm.ftmo_ev(r,scale=sc,n_paths=4000,seed=7,horizon=504);print(f'   sc {sc}: p1p2={o["p_pass_1"]*o["p_pass_2"]:.2f} surv={o["p_survive"]:.2f} EV/mnd={o["net_ev_monthly"]:.0f}')
