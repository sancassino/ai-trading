import pandas as pd, numpy as np, gzip
def load(s):
    df=pd.read_csv(f'/tmp/m5/{s}.csv.gz',sep=';',skiprows=1)
    df['time']=pd.to_datetime(df['time'],format='%Y.%m.%d %H:%M')
    df=df.set_index('time').sort_index()
    return df[(df.index>='2021-01-01')&(df.index<'2024-01-01')]
SH=1  # broker server time = CET+1h (EET)
def at(df,day,h,m,after=True):
    t=pd.Timestamp(day)+pd.Timedelta(hours=h+SH,minutes=m)
    sub=df.loc[t:t+pd.Timedelta(minutes=30)]
    return sub.iloc[0] if len(sub) else None
def last_before(df,day,h,m):
    t=pd.Timestamp(day)+pd.Timedelta(hours=h+SH,minutes=m)
    sub=df.loc[t-pd.Timedelta(minutes=30):t]
    return sub.iloc[-1] if len(sub) else None
def report(name,r,rt):
    r=np.array(r); n=len(r)
    if n==0: print(name,'geen trades'); return
    print(f'{name}: N={n} mean_bruto={r.mean():+.2f}bp median={np.median(r):+.2f} gate={3*rt:.2f} -> {"PASS" if r.mean()>=3*rt and n>=150 else "FAIL"}  (t_day={r.mean()/(r.std(ddof=1)/np.sqrt(n)):+.2f})')
# N89 GER40: ret2h 08:00->10:00 CET, trade 10:00->17:00
g=load('GER40cash'); days=sorted(set(g.index.normalize()))
r=[]
for d in days:
    a=at(g,d,8,0); b=at(g,d,10,0); c=last_before(g,d,17,0)
    if a is None or b is None or c is None or d.weekday()>4: continue
    ret=(b['close']-a['open'])/a['open']
    if ret==0: continue
    side=1 if ret>0 else -1
    r.append(side*(c['close']-b['close'])/b['close']*1e4)
report('N89 GER40 2h-open momentum',r,0.72)
# N88 EURGBP 5d short-only: daily close (last bar <=22:00 CET)
e=load('EURGBP'); 
dc=[]
for d in sorted(set(e.index.normalize())):
    x=last_before(e,d,22,0)
    if x is not None and d.weekday()<5: dc.append((d,x['close']))
s=pd.Series({d:c for d,c in dc})
r=[]; i=5
while i+5<len(s):
    ret5=s.iloc[i]/s.iloc[i-5]-1
    if ret5<0: r.append(-(s.iloc[i+5]/s.iloc[i]-1)*1e4); i+=5
    else: i+=1
report('N88 EURGBP 5d short-only TSMOM',r,1.04)
# N87 US30 gap fade: open = first bar at/after 07:05 CET? use first bar >=08:00 server-time day; prior close last bar<=22:00 CET previous day
u=load('US30cash'); days=sorted(set(u.index.normalize())); r=[]
prev=None
for d in days:
    if d.weekday()>4: continue
    o=at(u,d,7,0); c=last_before(u,d,21,55)
    if prev is not None and o is not None and c is not None:
        gap=(o['open']-prev)/prev*1e4
        if abs(gap)>30:
            side=-1 if gap>0 else 1
            r.append(side*(c['close']-o['open'])/o['open']*1e4)
    if c is not None: prev=last_before(u,d,22,0)['close']
report('N87 US30 gap fade (|gap|>30bp)',r,0.45)
