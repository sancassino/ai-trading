import pandas as pd,numpy as np,glob,os
cost=dict(l.strip().split(';') for l in open('/tmp/stk_costs.csv') if ';' in l and l[0].isalpha());cost={k:float(v) for k,v in cost.items() if v.replace('.','').isdigit()}
D={}
for f in sorted(glob.glob('/tmp/stk/*.csv.gz')):
    s=os.path.basename(f).split('.')[0]
    d=pd.read_csv(f,sep=';',skiprows=1);d['time']=pd.to_datetime(d['time'],format='%Y.%m.%d %H:%M');d=d.set_index('time').sort_index();d=d[~d.index.duplicated()]
    d=d[(d.index.hour*60+d.index.minute>=16*60+30)&(d.index.hour*60+d.index.minute<23*60)]   # server NY+7: 16:30-23:00
    g=d.groupby(d.index.date)
    r=pd.DataFrame({'open':g.open.first(),'close':g.close.last(),'n':g.size(),'c30':g.close.apply(lambda x:x.iloc[-7] if len(x)>=7 else np.nan)})
    r=r[r.n>=60]   # volledige sessie (78 bars) ruim
    D[s]=r
O=pd.DataFrame({s:v.open for s,v in D.items()});C=pd.DataFrame({s:v.close for s,v in D.items()});C30=pd.DataFrame({s:v.c30 for s,v in D.items()})
O.index=pd.to_datetime(O.index);C.index=O.index;C30.index=O.index
oc=(C/O-1)*1e4;prev=(C.pct_change()*1e4).shift(1);gap=(O/C.shift(1)-1)*1e4;last30=(C/C30-1)*1e4
last30=last30.shift(1)
cst=pd.Series({s:cost.get(s,5.0)+0.4 for s in O.columns})
def ls(sig,sign,k=6):
    out=[]
    for d in sig.index:
        v=sig.loc[d].dropna()
        if len(v)<2*k+2 or d not in oc.index:continue
        hi=v.nlargest(k).index;lo=v.nsmallest(k).index
        L,S=(hi,lo) if sign>0 else (lo,hi)
        gr=(oc.loc[d,L].mean()-oc.loc[d,S].mean())/2     # per notional (50/50)
        c=(cst[L].mean()+cst[S].mean())/2
        out.append((d,gr-c))
    return pd.Series(dict(out))
def rep(nm,r):
    for p,a,b in (('train','2021','2023'),('test','2024','2024')):
        x=r[a:b];print(f'{nm} {p}: N={len(x)} netto {x.mean():+.2f}bp/dag t={x.mean()/(x.std()/np.sqrt(len(x))):+.2f}')
print('symbolen',len(O.columns),O.index.min(),O.index.max(),'dagen',len(O))
rep('S1 reversal(prev-ret)',ls(prev,-1))
rep('S2 gap-momentum',ls(gap,+1))
rep('S3 gap-reversal',ls(gap,-1))
rep('S4 reversal(last30)',ls(last30,-1))
