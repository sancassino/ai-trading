import pandas as pd, numpy as np
RT=0.45
df=pd.read_csv('/tmp/m5/US30cash.csv.gz',sep=';',skiprows=1)
df['time']=pd.to_datetime(df['time'],format='%Y.%m.%d %H:%M'); df=df.set_index('time').sort_index()
df=df[(df.index>='2021-01-01')&(df.index<'2025-01-01')]   # reserve 2025+ NOT loaded
def win(d,h,m,span=30):
    t=d+pd.Timedelta(hours=h,minutes=m); return df.loc[t:t+pd.Timedelta(minutes=span)]
def lastb(d,h,m):
    t=d+pd.Timedelta(hours=h,minutes=m); s=df.loc[t-pd.Timedelta(minutes=30):t]; return s.iloc[-1] if len(s) else None
rows=[]; prev=None
for d in sorted(set(df.index.normalize())):
    if d.weekday()>4: continue
    o=win(d,8,0); c=lastb(d,22,55); p=lastb(d,23,0)
    if prev is not None and len(o) and c is not None:
        op=o.iloc[0]['open']; gap=(op-prev)/prev*1e4
        if abs(gap)>30:
            side=-1 if gap>0 else 1
            rows.append((d,side*(c['close']-op)/op*1e4-RT))
    if p is not None: prev=p['close']
r=pd.Series(dict(rows))
def rep(n,x):
    t=x.mean()/(x.std(ddof=1)/np.sqrt(len(x)))
    print(f'{n}: N={len(x)} netto_mean={x.mean():+.2f}bp dag-t={t:+.2f} win%={(x>0).mean()*100:.0f}')
rep('train 2021-23',r[r.index<'2024-01-01']); rep('test 2024',r[r.index>='2024-01-01'])
for y in (2021,2022,2023,2024): 
    x=r[(r.index>=f'{y}-01-01')&(r.index<f'{y+1}-01-01')]; 
    if len(x)>1: rep(str(y),x)
