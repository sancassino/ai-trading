import pandas as pd,numpy as np
COST=11.0
syms=['SPX_TR','NDX','DAX','FTSE','N225','STOXX50','DJI']
out=[]
for s in syms:
    d=pd.read_csv(f'/tmp/daily/{s}.csv',sep=';',comment='#',parse_dates=['date']).set_index('date').sort_index()
    c=d.adjclose.dropna();c=c[c.index>='1990-01-01'];c=c[c.index<'2025-01-01']
    ym=c.index.to_period('M');pos=pd.Series(range(len(c)),index=c.index)
    first=pos.groupby(ym).transform('min');last=pos.groupby(ym).transform('max')
    # per maand: entry = slot 2e-laatste dag (last-1), exit = slot 3e handelsdag volgende maand (first_next+2)
    mm=sorted(set(ym));rows=[]
    for i,m in enumerate(mm[:-1]):
        l=int(last[ym==m].iloc[0]);f2=int(first[ym==mm[i+1]].iloc[0])
        e=l-1;x=f2+2
        if x>=len(c):continue
        rows.append((c.index[x],(c.iloc[x]/c.iloc[e]-1)*1e4))
    R=pd.DataFrame(rows,columns=['d','g']).set_index('d').g
    R=R[R.index>='1990-01-01']
    for nm,a,b in (('train','1990','2015'),('test','2016','2024')):
        r=R[a:b];n=r-COST
        out.append((s,nm,len(r),r.mean(),n.mean(),n.mean()/(n.std()/np.sqrt(len(n))),(n>0).mean()))
O=pd.DataFrame(out,columns=['sym','per','N','bruto','netto','t','hit']).round(2);print(O.to_string(index=False))
print(O.groupby('per')[['bruto','netto','t']].mean().round(2))
