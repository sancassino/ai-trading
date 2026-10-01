"""SHOCK model 1 (D-103): LightGBM regressie op bruto ret60 (mee-richting). 1 trial. Test = 2024. Reserve 2025+ niet geladen."""
import pandas as pd, numpy as np, lightgbm as lgb
ev=pd.read_csv('results/ceo/shock_events.csv.gz',parse_dates=['time']); ev['date']=ev.time.dt.normalize()
cls={'US30cash':'idx','US100cash':'idx','US500cash':'idx','GER40cash':'idx','UK100cash':'idx','JP225cash':'idx','EU50cash':'idx','FRA40cash':'idx','XAUUSD':'met','XAGUSD':'met','XCUUSD':'met','USOILcash':'en','UKOILcash':'en','NATGAScash':'en','BTCUSD':'cry','ETHUSD':'cry'}
ev['cls']=ev.sym.map(cls).fillna('fx')
ev['s_shock']=ev.shock_bp.abs(); ev['t1h']=ev.trend1h*ev.side; ev['t1d']=ev.trend1d*ev.side
ev['clsc']=ev.cls.astype('category'); ev['symc']=ev.sym.astype('category')
F=['z','s_shock','spr_ratio','t1h','t1d','vol1h','slot','dow','cost_bp','clsc','symc']
y='ret60'
tr=ev[ev.time<'2023-07-01']; va=ev[(ev.time>='2023-07-01')&(ev.time<'2024-01-01')]; te=ev[(ev.time>='2024-01-01')&(ev.time<'2025-01-01')]
lo,hi=tr[y].quantile([.01,.99])
m=lgb.LGBMRegressor(n_estimators=2000,learning_rate=0.02,num_leaves=15,min_child_samples=300,subsample=0.8,subsample_freq=1,colsample_bytree=0.8,reg_lambda=5,verbose=-1,random_state=1)
m.fit(tr[F],tr[y].clip(lo,hi),eval_set=[(va[F],va[y].clip(lo,hi))],callbacks=[lgb.early_stopping(100,verbose=False)])
print('beste iteratie',m.best_iteration_)
def dagt(n,dates):
    b=n.groupby(dates).sum(); return b.mean()/(b.std(ddof=1)/np.sqrt(len(b))) if len(b)>2 else np.nan
for nm,d in(('val 2023H2',va),('test 2024',te)):
    p=m.predict(d[F]); d=d.assign(p=p)
    print(f'\n{nm}: corr(pred,real)={np.corrcoef(p,d[y])[0,1]:+.3f}')
    for stress in (1,2):
        for q in (0.9,0.95,0.99):
            thr=np.quantile(np.abs(p),q)
            sel=d[np.abs(d.p)>=thr]; side=np.sign(sel.p)
            net=side*sel[y]-stress*sel.cost_bp
            print(f' kostx{stress} top{int((1-q)*100):2d}%: N={len(sel):5d} net={net.mean():+6.2f}bp bruto={(side*sel[y]).mean():+6.2f} dag-t={dagt(net,sel.date):+5.2f}')
imp=pd.Series(m.feature_importances_,F).sort_values(ascending=False); print('\nbelang:',dict(imp))
