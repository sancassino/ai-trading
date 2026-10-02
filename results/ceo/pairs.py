import pandas as pd,numpy as np
def load(s):
    d=pd.read_csv(f'/tmp/daily/{s}.csv',sep=';',comment='#',parse_dates=['date']).set_index('date').sort_index();return d.adjclose.dropna()
pairs=[('NDX','SPX_TR'),('DAX','STOXX50'),('DJI','SPX_TR'),('FTSE','DAX')]
COST=5.0  # bp per dag (spread beide benen ~2.6 + swap ~2.4)
for a,b in pairs:
    x=pd.concat([load(a),load(b)],axis=1,keys=['a','b']).dropna();x=x[(x.index>='1995-01-01')&(x.index<'2025-01-01')]
    s=(x.a.pct_change()-x.b.pct_change())*1e4;z=s.rolling(5).sum().shift(1)/(s.rolling(60).std().shift(1)*np.sqrt(5))
    for h in (1,5):
        fwd=s.rolling(h).sum().shift(-h+1) if h>1 else s  # rendement dag t..t+h-1
        sig=-np.sign(z).where(z.abs()>1.5)
        g=(sig*fwd).dropna()
        for nm,lo,hi in (('train','1995','2015'),('test','2016','2024')):
            r=g[lo:hi]
            if h>1:r=r.iloc[::h]
            n=r-COST*h
            print(f'{a}-{b} h={h} {nm}: N={len(r)} bruto {r.mean():+.2f} netto {n.mean():+.2f} t={n.mean()/(n.std()/np.sqrt(len(n))):+.2f}')
