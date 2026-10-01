"""EENMALIGE reserve-run ORB-meta (D-104). Vaste drempel+modellen uit orb_meta_final.py. Periode 2025-01 -> einde."""
import json,pandas as pd,numpy as np,lightgbm as lgb,warnings,sys;warnings.filterwarnings('ignore')
T=pd.read_csv('/tmp/orb_trades.csv',sep=';',parse_dates=['date']);T=T[T.date>='2025-01-01'].copy();T['y']=T.net_frac*1e4
print('trades',len(T),T.date.min(),T.date.max())
feats=[]
for s in T.symbol.unique():
    d=pd.read_csv(f'/tmp/m5/{s}.csv.gz',sep=';',skiprows=1);d['time']=pd.to_datetime(d['time'],format='%Y.%m.%d %H:%M');d=d.set_index('time').sort_index();d=d[~d.index.duplicated()]
    D=d.resample('D').agg({'open':'first','high':'max','low':'min','close':'last'}).dropna()
    D['ret']=D.close.pct_change()*1e4;D['rng']=(D.high-D.low)/D.close*1e4
    f=pd.DataFrame(index=D.index)
    f['prev_ret']=D.ret.shift(1);f['prev_rng']=D.rng.shift(1)
    f['atr20']=D.rng.rolling(20).mean().shift(1);f['rng_ratio']=f.prev_rng/f.atr20
    f['r5']=D.ret.rolling(5).sum().shift(1);f['r20']=D.ret.rolling(20).sum().shift(1)
    f['gap']=((D.open/D.close.shift(1)-1)*1e4);f['gap_atr']=f.gap/f.atr20
    f['dist_hi20']=(D.close.shift(1)/D.high.rolling(20).max().shift(1)-1)*1e4
    f['vol5_20']=D.ret.rolling(5).std().shift(1)/D.ret.rolling(20).std().shift(1)
    f['symbol']=s;f['date']=f.index;feats.append(f.reset_index(drop=True))
X=T.merge(pd.concat(feats),on=['symbol','date'],how='left')
X['dow']=X.date.dt.dayofweek;X['month']=X.date.dt.month
J=json.load(open('results/ceo/orb_meta_threshold.json'));FE=J['features'];thr=J['threshold']
tr=pd.read_csv('/tmp/orb_trades.csv',sep=';');cats=sorted(tr[tr.date<'2025-01-01'].symbol.unique())
X['sym']=pd.Categorical(X.symbol,categories=cats)
X=X.dropna(subset=FE[:-1]).copy()
ps=[lgb.Booster(model_file=f'results/ceo/orb_meta_model_seed{s}.txt').predict(X[FE]) for s in range(5)]
X['p']=np.mean(ps,axis=0);X['sel']=X.p>=thr
def dagt(n,d): b=n.groupby(d).sum();return b.mean()/(b.std(ddof=1)/np.sqrt(len(b)))
a=X[X.sel];b=X[~X.sel]
print(f'corr {np.corrcoef(X.p,X.y)[0,1]:+.3f} | alle N={len(X)} {X.y.mean():+.2f} dag-t {dagt(X.y,X.date):+.2f} | gefilterd N={len(a)} {a.y.mean():+.2f} dag-t {dagt(a.y,a.date):+.2f} | rest N={len(b)} {b.y.mean():+.2f}')
d=X.groupby(['date','sel']).y.mean().unstack().dropna();df=d[True]-d[False]
print(f'toegevoegde waarde {df.mean():+.2f}bp t={df.mean()/(df.std(ddof=1)/np.sqrt(len(df))):+.2f} (dagen {len(df)})')
sys.path.insert(0,'/tmp/eng');from engine import ftmo as fm
idx=pd.bdate_range(X.date.min(),X.date.max())
for nm,df_ in (('ongefilterd',X),('gefilterd',a)):
    r=df_.groupby('date').net_frac.sum().reindex(idx).fillna(0).values
    print(nm,f'gem {r.mean()*1e4:+.2f}bp/dag SR {r.mean()/r.std()*np.sqrt(252):+.2f}')
    for sc in (0.25,0.35,0.5):
        o=fm.ftmo_ev(r,scale=sc,n_paths=4000,seed=7,horizon=504);print(f'  sc {sc}: p1*p2={o["p_pass_1"]*o["p_pass_2"]:.2f} surv={o["p_survive"]:.2f} EV/mnd={o["net_ev_monthly"]:.0f}')
