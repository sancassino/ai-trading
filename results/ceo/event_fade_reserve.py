import pandas as pd,numpy as np
nfp=[l.strip() for l in open('/tmp/dates_payems_res.txt') if l.strip()]
cpi_all=[l.strip() for l in open('/tmp/dates_cpi_res.txt') if l.strip()]
cpi={};[cpi.__setitem__(d[:7],d) for d in sorted(cpi_all)];cpi=sorted(cpi.values())
fomc=[]
_x=None
EV={'NFP':(nfp,15,30),'CPI':(cpi,15,30),'FOMC':(fomc,21,0)}
cost={'US500cash':0.8+1,'US100cash':0.5+1,'XAUUSD':0.7+1,'EURUSD':1.1+1,'GBPUSD':0.7+1,'USDJPY':1.0+1}
rows=[]
for s,c in cost.items():
    d=pd.read_csv(f'/tmp/m5/{s}.csv.gz',sep=';',skiprows=1);d['time']=pd.to_datetime(d['time'],format='%Y.%m.%d %H:%M');d=d.set_index('time').sort_index();d=d[~d.index.duplicated()];cl=d.close
    for ev,(dates,h,m) in EV.items():
        for ds in dates:
            T=pd.Timestamp(f'{ds} {h:02d}:{m:02d}')
            try:
                a=cl[:T-pd.Timedelta(minutes=5)];b=cl[:T+pd.Timedelta(minutes=10)];e=cl[:T+pd.Timedelta(minutes=70)]
                if a.index[-1]<T-pd.Timedelta(minutes=15) or b.index[-1]<T or e.index[-1]<T+pd.Timedelta(minutes=60):continue
                r1=(b.iloc[-1]/a.iloc[-1]-1)*1e4;r2=(e.iloc[-1]/b.iloc[-1]-1)*1e4
            except Exception:continue
            if abs(r1)<c:continue
            rows.append((ev,s,pd.Timestamp(ds),r1,-np.sign(r1)*r2-c))
R=pd.DataFrame(rows,columns=['ev','sym','d','r1','y'])
def t(x):
    b=x.groupby('d').y.mean();return b.mean()/(b.std(ddof=1)/np.sqrt(len(b))) if len(b)>3 else np.nan
for ex in (0,2):
    x=R.copy();x['y']=x.y-ex
    per=x.groupby('sym').y.mean().round(1).to_dict()
    print(f'extra kosten {ex}bp: Nobs={len(x)} events={x.d.nunique()} netto {x.y.mean():+.2f}bp t={t(x):+.2f} pos {sum(v>0 for v in per.values())}/{len(per)}',per)
    for ev in ('NFP','CPI'):
        y=x[x.ev==ev];print('  ',ev,len(y),f'{y.y.mean():+.2f}bp t={t(y):+.2f}')
