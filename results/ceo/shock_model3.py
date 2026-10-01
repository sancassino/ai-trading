"""SHOCK model 2 (D-103): model 1 + marktbrede context (refs 30 min) + cross-asset schokken. 1 trial (nr 2). Test 2024; reserve niet geladen."""
import pandas as pd, numpy as np, lightgbm as lgb
ev=pd.read_csv('results/ceo/shock_events.csv.gz',parse_dates=['time']); ev['date']=ev.time.dt.normalize()
REFS=['US500cash','EURUSD','USDJPY','XAUUSD','USOILcash','BTCUSD']
refret={}
for s in REFS:
    d=pd.read_csv(f'/tmp/m5/{s}.csv.gz',sep=';',skiprows=1); d['time']=pd.to_datetime(d['time'],format='%Y.%m.%d %H:%M')
    d=d.set_index('time').sort_index(); d=d[(d.index<'2025-01-01')&(~d.index.duplicated())]
    c=d['close']; refret[s]=((c/c.shift(6)-1)*1e4).rename(s)       # 30 min t/m deze bar
R=pd.concat(refret.values(),axis=1)
# event 'time' = open van instapbar e; schokbar i = time-5min; refs t/m close van bar i
key=ev.time-pd.Timedelta(minutes=5)
X=R.reindex(key.values).reset_index(drop=True); X.index=ev.index
for s in REFS: ev['ref_'+s]=X[s]*ev.side            # richting t.o.v. de schok
ev['n_refs_same']=(np.sign(X[REFS]).mul(ev.side,axis=0)>0).sum(axis=1)
ev['ref_absmean']=X[REFS].abs().mean(axis=1)
cls={'US30cash':'idx','US100cash':'idx','US500cash':'idx','GER40cash':'idx','UK100cash':'idx','JP225cash':'idx','EU50cash':'idx','FRA40cash':'idx','XAUUSD':'met','XAGUSD':'met','XCUUSD':'met','USOILcash':'en','UKOILcash':'en','NATGAScash':'en','BTCUSD':'cry','ETHUSD':'cry'}
ev['cls']=ev.sym.map(cls).fillna('fx')
ev['s_shock']=ev.shock_bp.abs(); ev['t1h']=ev.trend1h*ev.side; ev['t1d']=ev.trend1d*ev.side
ev['clsc']=ev.cls.astype('category'); ev['symc']=ev.sym.astype('category')
F=['z','s_shock','spr_ratio','t1h','t1d','vol1h','slot','dow','cost_bp','clsc','symc','n_refs_same','ref_absmean']+['ref_'+s for s in REFS]
y='ret60'
def dagt(n,dates):
    b=n.groupby(dates).sum(); return b.mean()/(b.std(ddof=1)/np.sqrt(len(b))) if len(b)>2 else np.nan
print("Vooraf: handel als |pred| >= 2 x cost_bp (kostenbewust); n_estimators=60 vast; expanding walk-forward per jaar; 5 seeds gemiddeld")
allsel=[]
for yr in (2022,2023,2024):
    tr=ev[ev.time<f'{yr}-01-01']; te=ev[(ev.time>=f'{yr}-01-01')&(ev.time<f'{yr+1}-01-01')]
    lo,hi=tr[y].quantile([.01,.99]); ps=[]
    for seed in range(5):
        m=lgb.LGBMRegressor(n_estimators=60,learning_rate=0.02,num_leaves=15,min_child_samples=300,subsample=0.8,subsample_freq=1,colsample_bytree=0.8,reg_lambda=5,verbose=-1,random_state=seed)
        m.fit(tr[F],tr[y].clip(lo,hi)); ps.append(m.predict(te[F]))
    p=np.mean(ps,axis=0); d=te.assign(p=p)
    corr=np.corrcoef(p,d[y])[0,1]
    sel=d[np.abs(d.p)>=2*d.cost_bp]; side=np.sign(sel.p)
    r=side*sel[y]
    out=[f'{yr}: corr={corr:+.3f} N_sel={len(sel)}']
    for st in (1,2):
        net=r-st*sel.cost_bp; out.append(f'kostx{st}: net={net.mean():+.2f} bruto={r.mean():+.2f} t={dagt(net,sel.date):+.2f}')
    print(' | '.join(out)); allsel.append(sel.assign(r=r))
A=pd.concat(allsel)
for st in (1,2):
    net=A.r-st*A.cost_bp; print(f'GEPOOLD 2022-24 kostx{st}: N={len(A)} net={net.mean():+.2f}bp dag-t={dagt(net,A.date):+.2f}')
print('per klasse (gepoold, kostx1):')
for c,g in A.groupby('cls'): net=g.r-g.cost_bp; print(f'  {c}: N={len(g)} net={net.mean():+.2f} t={dagt(net,g.date):+.2f}')
