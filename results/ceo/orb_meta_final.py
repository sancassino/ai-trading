"""Bevriest drempel + eindmodel voor ORB-meta (PREREG_ORB_META_V1). Alleen data <2025. Schrijft orb_meta_threshold.json en orb_meta_model_seed*.txt."""
import re,json,pandas as pd,numpy as np,lightgbm as lgb,warnings;warnings.filterwarnings('ignore')
src=open('results/ceo/orb_meta_stability.py').read().split("def dagt")[0]
exec(src)  # bouwt X, FE (features), T <2025
P=[];
for yr in (2022,2023,2024):
    tr=X[X.date<f'{yr}-01-01'];te=X[(X.date>=f'{yr}-01-01')&(X.date<f'{yr+1}-01-01')]
    lo,hi=tr.y.quantile([.02,.98]);ps=[]
    for s in range(5):
        m=lgb.LGBMRegressor(n_estimators=80,learning_rate=0.02,num_leaves=7,min_child_samples=150,subsample=0.8,subsample_freq=1,colsample_bytree=0.8,reg_lambda=10,verbose=-1,random_state=s)
        m.fit(tr[FE],tr.y.clip(lo,hi));ps.append(m.predict(te[FE]))
    P.append(np.mean(ps,axis=0))
thr=float(np.median(np.concatenate(P)))
tr=X[X.date<'2025-01-01'];lo,hi=tr.y.quantile([.02,.98])
for s in range(5):
    m=lgb.LGBMRegressor(n_estimators=80,learning_rate=0.02,num_leaves=7,min_child_samples=150,subsample=0.8,subsample_freq=1,colsample_bytree=0.8,reg_lambda=10,verbose=-1,random_state=s)
    m.fit(tr[FE],tr.y.clip(lo,hi));m.booster_.save_model(f'results/ceo/orb_meta_model_seed{s}.txt')
json.dump({'threshold':thr,'train_end':'2024-12-31','n_train':len(tr),'features':FE,'clip':[float(lo),float(hi)]},open('results/ceo/orb_meta_threshold.json','w'),indent=1)
print('thr',thr,'ntrain',len(tr))
