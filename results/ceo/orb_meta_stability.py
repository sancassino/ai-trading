"""ORB meta-labeling (trial 7): LightGBM beslist per ORB-trade (B4a, 7 symbolen) of de trade genomen wordt. Features uit M5-daggegevens van vóór de handeldag.
Train 2021-2023, test 2024. 2025+ niet geladen. Doel = net_bp (na kosten)."""
import pandas as pd, numpy as np, lightgbm as lgb, warnings; warnings.filterwarnings('ignore')
T=pd.read_csv('/tmp/orb_trades.csv',sep=';',parse_dates=['date']); T=T[T.date<'2025-01-01'].copy(); T['y']=T.net_frac*1e4
feats=[]
for s in T.symbol.unique():
    d=pd.read_csv(f'/tmp/m5/{s}.csv.gz',sep=';',skiprows=1); d['time']=pd.to_datetime(d['time'],format='%Y.%m.%d %H:%M'); d=d.set_index('time').sort_index()
    d=d[(d.index<'2025-01-01')&(~d.index.duplicated())]
    D=d.resample('D').agg({'open':'first','high':'max','low':'min','close':'last'}).dropna()
    D['ret']=D.close.pct_change()*1e4; D['rng']=(D.high-D.low)/D.close*1e4
    f=pd.DataFrame(index=D.index)
    f['prev_ret']=D.ret.shift(1); f['prev_rng']=D.rng.shift(1)
    f['atr20']=D.rng.rolling(20).mean().shift(1); f['rng_ratio']=f.prev_rng/f.atr20
    f['r5']=D.ret.rolling(5).sum().shift(1); f['r20']=D.ret.rolling(20).sum().shift(1)
    f['gap']=((D.open/D.close.shift(1)-1)*1e4)       # open vandaag vs close gisteren (open is bekend bij handeldag)
    f['gap_atr']=f.gap/f.atr20
    f['dist_hi20']=(D.close.shift(1)/D.high.rolling(20).max().shift(1)-1)*1e4
    f['vol5_20']=D.ret.rolling(5).std().shift(1)/D.ret.rolling(20).std().shift(1)
    f['symbol']=s; f['date']=f.index; feats.append(f.reset_index(drop=True))
F=pd.concat(feats); X=T.merge(F,on=['symbol','date'],how='left')
X['dow']=X.date.dt.dayofweek; X['sym']=X.symbol.astype('category'); X['month']=X.date.dt.month
FE=['prev_ret','prev_rng','atr20','rng_ratio','r5','r20','gap','gap_atr','dist_hi20','vol5_20','dow','month','sym']
X=X.dropna(subset=FE[:-1]); tr=X[X.date<'2024-01-01']; te=X[(X.date>='2024-01-01')]

def dagt(n,d): b=n.groupby(d).sum(); return b.mean()/(b.std(ddof=1)/np.sqrt(len(b)))
print("Stabiliteit: expanding walk-forward per jaar, 5 seeds, vooraf: handel de top 50% voorspellingen per jaar")
allr=[]; allte=[]
for yr in (2022,2023,2024):
    tr=X[X.date<f'{yr}-01-01']; te=X[(X.date>=f'{yr}-01-01')&(X.date<f'{yr+1}-01-01')].copy()
    lo,hi=tr.y.quantile([.02,.98]); ps=[]
    for seed in range(5):
        m=lgb.LGBMRegressor(n_estimators=80,learning_rate=0.02,num_leaves=7,min_child_samples=150,subsample=0.8,subsample_freq=1,colsample_bytree=0.8,reg_lambda=10,verbose=-1,random_state=seed)
        m.fit(tr[FE],tr.y.clip(lo,hi)); ps.append(m.predict(te[FE]))
    te['p']=np.mean(ps,axis=0); thr=te.p.median(); a=te[te.p>=thr]; b=te[te.p<thr]
    print(f'{yr}: corr={np.corrcoef(te.p,te.y)[0,1]:+.3f}  alle {te.y.mean():+.2f} | top50% N={len(a)} {a.y.mean():+.2f} (dag-t {dagt(a.y,a.date):+.2f}) | rest {b.y.mean():+.2f}')
    allr.append(a); te['sel']=te.p>=thr; allte.append(te)
A=pd.concat(allr); print(f'GEPOOLD top50% 2022-24: N={len(A)} netto={A.y.mean():+.2f}bp dag-t={dagt(A.y,A.date):+.2f}')
for st in (2,):
    print('kostenstress x2 (extra kosten ~ gelijk aan implicit kosten ORB: onbekend) -> niet apart gemodelleerd')

T=pd.concat(allte)
d=T.groupby(['date','sel']).y.mean().unstack(); d=d.dropna(); diff=(d[True]-d[False])
print(f"TOEGEVOEGDE WAARDE (geselecteerd - niet geselecteerd, gem. per dag): {diff.mean():+.2f}bp  t={diff.mean()/(diff.std(ddof=1)/np.sqrt(len(diff))):+.2f}  (dagen={len(diff)})")
allm=T.groupby('date').y.mean(); print(f"Ongefilterd ORB (alle trades) 2022-24: {T.y.mean():+.2f}bp/trade dag-t={dagt(T.y,T.date):+.2f}")
sel=T[T.sel]; print(f"Gefilterd: {sel.y.mean():+.2f}bp/trade (N={len(sel)}), dag-t={dagt(sel.y,sel.date):+.2f}; trades gehalveerd")
for s_,g in sel.groupby('symbol'): print('  ',s_,f'N={len(g)} {g.y.mean():+.2f}')

# FTMO-EV: gefilterd vs ongefilterd, out-of-sample 2022-24 (dagreeks = som van net_frac van de getrokken trades, geschaald)
import sys; sys.path.insert(0,'/tmp/eng')
from engine import ftmo as fm
def daily(df):
    s=df.groupby('date').net_frac.sum(); idx=pd.bdate_range('2022-01-01','2024-12-31'); return s.reindex(idx).fillna(0.0).values
for nm,df in (('ongefilterd',T),('gefilterd top50%',T[T.sel])):
    r=daily(df); print(f'{nm}: gem {r.mean()*1e4:+.2f} bp/dag, vol {r.std()*np.sqrt(252)*100:.1f}%/jr, SR {r.mean()/r.std()*np.sqrt(252):+.2f}')
    for sc in (0.15,0.25,0.35,0.5):
        o=fm.ftmo_ev(r,scale=sc,n_paths=4000,seed=7,horizon=504)
        print(f'   schaal {sc}: p1*p2={o["p_pass_1"]*o["p_pass_2"]:.2f} overleef={o["p_survive"]:.2f} net EV €/mnd={o["net_ev_monthly"]:.0f}')
