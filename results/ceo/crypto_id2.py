import pandas as pd,numpy as np
cost={}
for l in open('/tmp/stk_costs.csv'):
    p=l.strip().split(';')
    try:cost[p[0]]=float(p[1])
    except:pass
coins=['BTCUSD','ETHUSD','LTCUSD','SOLUSD','DOGEUSD','ADAUSD','BNBUSD','DOTUSD','LNKUSD','BCHUSD']
allr=[]
for s in coins:
    try:d=pd.read_csv(f'/tmp/m5/{s}.csv.gz',sep=';',skiprows=1)
    except Exception as e:print(s,'geen data');continue
    d['time']=pd.to_datetime(d['time'],format='%Y.%m.%d %H:%M');d=d.set_index('time').sort_index();d=d[~d.index.duplicated()]
    u=(d.index-pd.Timedelta(hours=7)).tz_localize('America/New_York',ambiguous='NaT',nonexistent='NaT').tz_convert('UTC')
    d=d[~u.isna()];d.index=u[~u.isna()].tz_localize(None);c=d.close;rows=[]
    for day in pd.Series(c.index.date).unique():
        t=lambda h,m:pd.Timestamp(day)+pd.Timedelta(hours=h,minutes=m)
        try:a=c[:t(14,30)].iloc[-1];b=c[:t(15,0)].iloc[-1];e=c[:t(17,0)].iloc[-1]
        except:continue
        if c[:t(14,30)].index[-1]<t(14,20) or c[:t(17,0)].index[-1]<t(16,50):continue
        rows.append((pd.Timestamp(day),(b/a-1)*1e4,(e/b-1)*1e4))
    R=pd.DataFrame(rows,columns=['d','r1','r2']).set_index('d')
    thr=R.r1.abs().rolling(60).median().shift(1);R=R[R.r1.abs()>thr]
    R['y']=np.sign(R.r1)*R.r2-cost.get(s,10.0);R['sym']=s;allr.append(R.reset_index())
A=pd.concat(allr)
def dagt(x):
    b=x.groupby('d').y.mean();return b.mean()/(b.std(ddof=1)/np.sqrt(len(b)))
for nm,a,b in (('train','2021','2023'),('test','2024','2024')):
    x=A[(A.d>=a)&(A.d<f'{int(b)+1}')]
    per=x.groupby('sym').y.mean().round(1).to_dict()
    print(f'{nm}: gepoold N={len(x)} netto {x.y.mean():+.2f}bp dag-t={dagt(x):+.2f} | positief {sum(v>0 for v in per.values())}/{len(per)}')
    print('  ',per)
