"""DAGMODEL 1 (D-103 vervolg, trial 4): cross-sectioneel LightGBM op daggegevens, 44 FTMO-symbolen via >=10j proxy, weekhorizon.
Beslissing elke 5 handelsdagen, hold 5 handelsdagen. Walk-forward per jaar 2012-2024 (expanding). Reserve 2025+ niet geladen."""
import pandas as pd, numpy as np, lightgbm as lgb, warnings; warnings.filterwarnings('ignore')
mp=pd.read_csv('/tmp/daily/map.csv'); cs=pd.read_csv('/tmp/costs.csv',sep=';',comment='#',usecols=range(9),engine='python',on_bad_lines='skip').set_index('symbol'); sw=pd.read_csv('results/ceo/swap_side_map.csv',sep=';').set_index('symbol')
def sname(s): return s if s in sw.index else (s.replace('.cash','cash') if s.replace('.cash','cash') in sw.index else s)
px={}
for sym,prox,cat in zip(mp.sym,mp.proxy,mp.cat):
    d=pd.read_csv(f'/tmp/daily/{prox}.csv',sep=';',comment='#',parse_dates=['date']).set_index('date')
    c=d['close'].dropna(); c=c[~c.index.duplicated()]; c=c[(c.index>='1990-01-01')&(c.index<'2025-01-01')]
    if len(c)>2500: px[sym]=c
P=pd.DataFrame(px).sort_index()
P=P.ffill(limit=3)
ret1=np.log(P).diff()
feat={}
for h in (1,5,10,20,60,120,250): feat[f'r{h}']=np.log(P).diff(h)
vol20=ret1.rolling(20).std(); vol60=ret1.rolling(60).std()
feat['vol20']=vol20; feat['vr']=vol20/vol60
feat['ma200']=np.log(P/P.rolling(200).mean())/vol60
feat['dd']=np.log(P/P.rolling(250).max())/vol60
for h in (5,20,60): feat[f'z{h}']=feat[f'r{h}']/(vol60*np.sqrt(h))
fwd=np.log(P).shift(-5)-np.log(P)
rows=[]
dates=P.index[260::5]
cat=dict(zip(mp.sym,mp.cat))
for d in dates:
    for s in P.columns:
        if np.isnan(P.at[d,s]) or np.isnan(fwd.at[d,s]) or np.isnan(vol60.at[d,s]): continue
        r={k:v.at[d,s] for k,v in feat.items()}; r.update(date=d,sym=s,cat=cat[s],fwd=fwd.at[d,s]*1e4,v60=vol60.at[d,s]); rows.append(r)
D=pd.DataFrame(rows).dropna()
D['catc']=D.cat.astype('category'); D['symc']=D.sym.astype('category')
# cross-sectionele rang van momentum en vol
for k in ('r20','r60','r250','vol20'): D['cs_'+k]=D.groupby('date')[k].rank(pct=True)
D['y']=(D.fwd/1e4/(D.v60*np.sqrt(5))).clip(-4,4)
F=[c for c in D.columns if c not in('date','sym','cat','fwd','v60','y')]
# kosten per positie (bp): spread + commissie + swap op gekozen kant over 7 kalenderdagen (alleen kosten, geen credit)
def cost(s,side):
    n=sname(s)
    rt=float(cs.at[s,'rondreis_bp']) if s in cs.index else (float(cs.at[n,'rondreis_bp']) if n in cs.index else 3.0)
    if n not in sw.index: return rt
    pct=sw.at[n,'long_pct_yr'] if side>0 else sw.at[n,'short_pct_yr']
    return rt+max(0.0,-float(pct))*100*7/365
out=[]
for yr in range(2012,2025):
    tr=D[D.date<f'{yr}-01-01']; te=D[(D.date>=f'{yr}-01-01')&(D.date<f'{yr+1}-01-01')].copy()
    ps=[]
    for seed in range(3):
        m=lgb.LGBMRegressor(n_estimators=150,learning_rate=0.03,num_leaves=15,min_child_samples=200,subsample=0.8,subsample_freq=1,colsample_bytree=0.8,reg_lambda=5,verbose=-1,random_state=seed)
        m.fit(tr[F],tr.y); ps.append(m.predict(te[F]))
    te['p']=np.mean(ps,axis=0); out.append(te)
O=pd.concat(out)
O['pr']=O.groupby('date')['p'].rank(pct=True)
def wk(sel_long,sel_short,stress=1):
    L=O[sel_long].copy(); S=O[sel_short].copy()
    L['net']=L.fwd-stress*L.sym.map(lambda s:cost(s,1)); S['net']=-S.fwd-stress*S.sym.map(lambda s:cost(s,-1))
    A=pd.concat([L,S]); return A
def summary(A,name):
    byw=A.groupby('date')['net'].mean()      # gelijk gewicht per week
    sr=byw.mean()/byw.std()*np.sqrt(52); t=byw.mean()/(byw.std()/np.sqrt(len(byw)))
    print(f'{name:34s} N_pos={len(A):6d} netto/pos={A.net.mean():+6.2f}bp  weken={len(byw)} SR={sr:+.2f} t_week={t:+.2f}')
    return byw
print('Dagmodel 1: walk-forward 2012-2024, top/bottom 20% per week')
for st in (0,):
    A0=wk(O.pr>=0.8,O.pr<=0.2,st); summary(A0,'ML long/short BRUTO (kosten 0)')
    mom=O.groupby('date')['r250'].rank(pct=True); summary(wk(mom>=0.8,mom<=0.2,0),'baseline 12m-mom L/S BRUTO')
    ew=O.copy(); ew['net']=ew.fwd; summary(ew,'baseline long alles BRUTO')
    for c,g in A0.groupby('cat'): b=g.groupby('date').net.mean(); print('  ',c,f'{g.net.mean():+.2f}bp N={len(g)} t_week={b.mean()/(b.std()/np.sqrt(len(b))):+.2f}')
    cc=wk(O.pr>=0.8,O.pr<=0.2,1); cc['c']=cc.net-0; print('  gem. kosten/pos (bp):',round(A0.net.mean()-cc.net.mean(),2))
for st in (1,2):
    A=wk(O.pr>=0.8,O.pr<=0.2,st); summary(A,f'ML long/short kostx{st}')
A=wk(O.pr>=0.8,O.pr<0,1); summary(A,'ML alleen long top20% kostx1')
A=wk(O.pr>=0.8,O.pr<=0.2,1)
# baselines
mom=O.groupby('date')['r250'].rank(pct=True); Ab=wk(mom>=0.8,mom<=0.2,1); summary(Ab,'baseline 12m-momentum L/S kostx1')
ew=O.copy(); ew['net']=ew.fwd-ew.sym.map(lambda s:cost(s,1)); summary(ew,'baseline long alles kostx1')
print('\nper jaar ML L/S kostx1 (netto/pos, SR):')
A=A.assign(yr=A.date.dt.year)
for y,g in A.groupby('yr'):
    b=g.groupby('date').net.mean(); print(y, f'{g.net.mean():+6.2f}bp', f'SR {b.mean()/b.std()*np.sqrt(52):+.2f}')
print('\ncorr(p,y) gemiddeld:',O.groupby(O.date.dt.year).apply(lambda g:np.corrcoef(g.p,g.y)[0,1]).round(3).to_dict())
