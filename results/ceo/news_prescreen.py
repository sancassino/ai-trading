import pandas as pd, numpy as np
from zoneinfo import ZoneInfo
ev=pd.read_csv('/tmp/events.csv',sep=';',comment='#'); ev=ev[~ev.status.str.contains('NIET',na=False)]
ET,SRV=ZoneInfo('America/New_York'),ZoneInfo('Europe/Athens')   # brokerserver = EET/EEST
TIME={'NFP':(8,30),'CPI':(8,30),'FOMC':(14,0)}
RT={'US100cash':0.8,'US500cash':0.8,'XAUUSD':2.0,'EURUSD':0.9}   # ruwe RT bp; nieuws-stress x3 in gate
def load(s):
    d=pd.read_csv(f'/tmp/m5/{s}.csv.gz',sep=';',skiprows=1); d['time']=pd.to_datetime(d['time'],format='%Y.%m.%d %H:%M')
    return d.set_index('time').sort_index()
def run(sym,hold_min,mode,end='2024-01-01'):
    d=load(sym); out=[]
    for _,r in ev.iterrows():
        if r.date>=end: continue
        h,m=TIME[r.event]; t=pd.Timestamp(r.date).replace(hour=h,minute=m).tz_localize(ET).astimezone(SRV).tz_localize(None)
        if t not in d.index: continue
        b=d.loc[t]; i=d.index.get_loc(t)
        if i+1+hold_min//5>=len(d): continue
        ret=(b['close']-b['open'])/b['open']*1e4
        if abs(ret)<1e-9: continue
        side=np.sign(ret) if mode=='cont' else -np.sign(ret)
        entry=b['close']; ex=d.iloc[i+hold_min//5]['close']
        out.append((r.event,r.date,side*(ex-entry)/entry*1e4))
    return pd.DataFrame(out,columns=['ev','date','pnl'])
rows=[]
for sym in RT:
    for hold in (30,60):
        for mode in ('cont','fade'):
            x=run(sym,hold,mode)
            if len(x)<10: continue
            gate=3*RT[sym]*3     # 3x RT met x3 nieuws-spreadstress
            t=x.pnl.mean()/(x.pnl.std(ddof=1)/np.sqrt(len(x)))
            rows.append((sym,hold,mode,len(x),x.pnl.mean(),gate,t))
df=pd.DataFrame(rows,columns=['sym','hold_min','mode','N','mean_bruto_bp','gate_bp','t'])
print(df.round(2).to_string(index=False))
