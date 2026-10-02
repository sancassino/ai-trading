"""ORB tijdstop-test (mechanisme: opening-impuls dooft uit). Zelfde ORB als B4a (OR 30 min, stop = OR-andere kant), uitstap op sessieslot (baseline) of open+N uur. Kosten per symbool = gemiddelde (gross_mijn - net_B4a) op baseline-dagen. Alleen <2025 voor keuze."""
import pandas as pd,numpy as np,warnings;warnings.filterwarnings('ignore')
from zoneinfo import ZoneInfo
from datetime import timedelta
NY=ZoneInfo("America/New_York")
SYMS={"US500cash":("America/New_York",(9,30),(16,0)),"US100cash":("America/New_York",(9,30),(16,0)),"US30cash":("America/New_York",(9,30),(16,0)),"XAUUSD":("America/New_York",(9,30),(16,0)),"GER40cash":("Europe/Berlin",(9,0),(17,30)),"UK100cash":("Europe/London",(8,0),(16,30)),"EURUSD":("Europe/London",(8,0),(16,30))}
EXITS=[None,2,4]   # None = sessieslot (baseline)
O=pd.read_csv('/tmp/orb_trades.csv',sep=';',parse_dates=['date'])
rows=[]
for sym,(tzn,(oh,om),(ch,cm)) in SYMS.items():
    d=pd.read_csv(f'/tmp/m5/{sym}.csv.gz',sep=';',skiprows=1);d['time']=pd.to_datetime(d['time'],format='%Y.%m.%d %H:%M')
    d['loc']=d.time.apply(lambda t:t.replace(tzinfo=NY)-timedelta(hours=7)) if False else (d.time-pd.Timedelta(hours=7)).dt.tz_localize(NY,ambiguous='NaT',nonexistent='NaT').dt.tz_convert(tzn)
    d=d.dropna(subset=['loc']).drop_duplicates('loc').set_index('loc').sort_index()
    for day,g in d.groupby(d.index.date):
        op=pd.Timestamp(year=day.year,month=day.month,day=day.day,hour=oh,minute=om,tz=tzn);cl=pd.Timestamp(year=day.year,month=day.month,day=day.day,hour=ch,minute=cm,tz=tzn)
        s=g[(g.index>=op)&(g.index<cl)]
        if len(s)<8 or s.index[0]!=op or s.index[-1]!=cl-pd.Timedelta(minutes=5):continue
        a=s[['open','high','low','close']].values
        hi=a[:6,1].max();lo=a[:6,2].min()
        if hi<=lo:continue
        res={}
        for k in range(6,len(a)):
            up,dn=a[k,1]>hi,a[k,2]<lo
            if not(up or dn):continue
            if up and dn:
                side=1;entry=max(hi,a[k,0]);stopk=k;stoppx=lo
            else:
                side=1 if up else -1;entry=max(hi,a[k,0]) if up else min(lo,a[k,0]);stop=lo if up else hi
                stopk=None;stoppx=None
                for j in range(k+1,len(a)):
                    if side>0 and a[j,2]<=stop:stoppx=min(stop,a[j,0]);stopk=j;break
                    if side<0 and a[j,1]>=stop:stoppx=max(stop,a[j,0]);stopk=j;break
            for ex in EXITS:
                lim=len(a)-1 if ex is None else min(len(a)-1,6+ex*12)   # open+N uur (bar-index)
                if stopk is not None and stopk<=lim:px=stoppx
                else:px=a[lim,3]
                res[ex]=side*(px-entry)/entry
            break
        if res:rows.append((sym,pd.Timestamp(day),res))
G=pd.DataFrame([dict(symbol=s,date=d,**{f'g{str(e)}':v for e,v in r.items()}) for s,d,r in rows])
M=G.merge(O,on=['symbol','date'])
cost=(M.gNone-M.net_frac).groupby(M.symbol).mean();print('kosten/trade (frac)\n',(cost*1e4).round(2).to_dict(),'match',len(M),'/',len(O))
M['cost']=M.symbol.map(cost)
def dagt(y,d):
    b=y.groupby(d).sum();return b.mean()/(b.std(ddof=1)/np.sqrt(len(b)))
for ex in EXITS:
    y=(M[f'g{ex}']-M.cost)*1e4;M['y']=y;M['yr']=M.date.dt.year
    a=M[M.date<'2025-01-01']
    print(f'exit {ex}: 21-24 {a.y.mean():+.2f}bp t={dagt(a.y,a.date):+.2f} | 25-26 {M[M.date>="2025"].y.mean():+.2f} | per jaar',M.groupby('yr').y.mean().round(1).to_dict())
M.to_csv('/tmp/orb_timestop.csv',index=False)
