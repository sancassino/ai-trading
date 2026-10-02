"""NFP-surprise-proxy (FRED PAYEMS, surprise = Δ − gem. Δ vorige 3 mnd; release = eerste vrijdag volgende maand). Alleen <2025. Vraag: voorspelt teken(surprise)+eerste-uur-reactie de vervolgbeweging?"""
import pandas as pd,numpy as np
P=pd.read_csv('/tmp/payems.csv',parse_dates=['observation_date']).set_index('observation_date').PAYEMS
dl=P.diff();sur=dl-dl.rolling(3).mean().shift(1)
rel={}
for m,v in sur.dropna().items():
    n=(m+pd.offsets.MonthBegin(1));fr=n+pd.offsets.Week(weekday=4) if n.weekday()!=4 else n
    rel[fr]=v
rel={k:v for k,v in rel.items() if '2019-01-01'<=str(k)<'2025-01-01'}
def load(s):
    d=pd.read_csv(f'/tmp/m5/{s}.csv.gz',sep=';',skiprows=1);d['time']=pd.to_datetime(d['time'],format='%Y.%m.%d %H:%M');return d.set_index('time').sort_index()['close']
for s in ('US500cash','XAUUSD','EURUSD','US100cash'):
    c=load(s);rows=[]
    # tijdzone-check: uur met grootste gem. |ret| op NFP-dagen
    h=pd.Series(0.0,index=range(24));
    for day,v in rel.items():
        x=c.loc[str(day.date()):str(day.date())]
        if len(x)<100:continue
        r=x.pct_change().abs();h=h.add(r.groupby(x.index.hour).mean(),fill_value=0)
    pk=int(h.idxmax())
    for day,v in rel.items():
        x=c.loc[str(day.date()):str(day.date())]
        if len(x)<100:continue
        t0=x[x.index.hour==pk].index.min() if False else pd.Timestamp(f'{day.date()} {pk:02d}:25')
        t1=t0+pd.Timedelta(minutes=65);t2=t0+pd.Timedelta(minutes=185)
        try:a=x[:t0].iloc[-1];b=x[:t1].iloc[-1];e=x[:t2].iloc[-1]
        except:continue
        rows.append((day,v,(b/a-1)*1e4,(e/b-1)*1e4))
    R=pd.DataFrame(rows,columns=['d','sur','react','cont'])
    cs=np.sign(R.sur);rs=np.sign(R.react)
    print(s,'piekuur',pk,'N',len(R),'corr(sur,react)=%.2f'%R.sur.corr(R.react),'corr(sur,cont)=%.2f'%R.sur.corr(R.cont),'corr(react,cont)=%.2f'%R.react.corr(R.cont))
    for nm,sg in (('sign(sur)',cs),('sign(react)',rs)):
        pnl=sg*R.cont;print(f'   cont*{nm}: gem {pnl.mean():+.1f}bp t={pnl.mean()/(pnl.std()/np.sqrt(len(pnl))):+.2f}')
