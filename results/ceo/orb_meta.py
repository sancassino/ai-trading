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
print('N train',len(tr),'test',len(te),'| baseline (alle trades) netto train',round(tr.y.mean(),2),'test',round(te.y.mean(),2))
def dagt(n,d): b=n.groupby(d).sum(); return b.mean()/(b.std(ddof=1)/np.sqrt(len(b)))
lo,hi=tr.y.quantile([.02,.98]); ps=[]
for seed in range(5):
    m=lgb.LGBMRegressor(n_estimators=80,learning_rate=0.02,num_leaves=7,min_child_samples=150,subsample=0.8,subsample_freq=1,colsample_bytree=0.8,reg_lambda=10,verbose=-1,random_state=seed)
    m.fit(tr[FE],tr.y.clip(lo,hi)); ps.append(m.predict(te[FE]))
te=te.assign(p=np.mean(ps,axis=0)); print('corr(pred,y) test',round(np.corrcoef(te.p,te.y)[0,1],3))
print('Baseline test: N',len(te),'netto',round(te.y.mean(),2),'bp/trade dag-t',round(dagt(te.y,te.date),2))
for q in (0.5,0.7,0.8,0.9):
    thr=te.p.quantile(q); s=te[te.p>=thr]
    print(f' top {int((1-q)*100)}% model: N={len(s)} netto={s.y.mean():+.2f}bp dag-t={dagt(s.y,s.date):+.2f}  (rest: {te[te.p<thr].y.mean():+.2f})')
print('belang:',dict(pd.Series(m.feature_importances_,FE).sort_values(ascending=False).head(6)))
