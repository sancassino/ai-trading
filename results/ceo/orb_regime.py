"""ORB regime-tabel (beschrijvend + 5 vooraf genoemde features x 2 helften). Keuze op 2021-24; 2025-26 alleen als bevestiging (reeds deels gezien: besmet)."""
import pandas as pd,numpy as np,warnings;warnings.filterwarnings('ignore')
T=pd.read_csv('/tmp/orb_trades.csv',sep=';',parse_dates=['date']);T['y']=T.net_frac*1e4
fs=[]
for s in T.symbol.unique():
    d=pd.read_csv(f'/tmp/m5/{s}.csv.gz',sep=';',skiprows=1);d['time']=pd.to_datetime(d['time'],format='%Y.%m.%d %H:%M');d=d.set_index('time').sort_index();d=d[~d.index.duplicated()]
    D=d.resample('D').agg({'open':'first','high':'max','low':'min','close':'last'}).dropna()
    D['ret']=D.close.pct_change()*1e4;D['rng']=(D.high-D.low)/D.close*1e4
    f=pd.DataFrame(index=D.index)
    atr=D.rng.rolling(20).mean().shift(1)
    f['vol_lvl']=atr/atr.rolling(250,min_periods=100).median().shift(1)          # volatiliteit t.o.v. 1 jaar
    f['rng_ratio']=D.rng.shift(1)/atr                                            # gisteren relatief
    f['trend']=D.ret.rolling(20).sum().shift(1).abs()/(atr*np.sqrt(20))         # |20d-trend| gestandaardiseerd
    f['gap']=((D.open/D.close.shift(1)-1)*1e4).abs()/atr
    f['sym']=s;f['date']=f.index;fs.append(f.reset_index(drop=True))
X=T.merge(pd.concat(fs),left_on=['symbol','date'],right_on=['sym','date'],how='left').dropna(subset=['vol_lvl','rng_ratio','trend','gap'])
X['yr']=X.date.dt.year
def dagt(g):
    b=g.groupby('date').y.sum();return b.mean()/(b.std(ddof=1)/np.sqrt(len(b))) if len(b)>5 else np.nan
# per symbool mediaan op data <=2024 -> vaste splitsing (geen lookahead voor 2025+)
for f in ['vol_lvl','rng_ratio','trend','gap']:
    med=X[X.date<'2025-01-01'].groupby('symbol')[f].median();X['hi']=X[f]>X.symbol.map(med)
    print(f'\n== {f}: hoog (>mediaan per symbool) vs laag')
    for nm,g in (('laag',X[~X.hi]),('hoog',X[X.hi])):
        pj=g.groupby('yr').y.mean().round(1).to_dict();a=g[g.date<'2025-01-01'];b=g[g.date>='2025-01-01']
        print(f' {nm}: 21-24 {a.y.mean():+.2f}bp t={dagt(a):+.2f} | 25-26 {b.y.mean():+.2f} t={dagt(b):+.2f} | per jaar {pj}')
