"""SHOCK stap 1: bouw shock-events uit M5 (D-103). Alleen data < 2025-01-01 wordt geladen (reserve dicht)."""
import pandas as pd, numpy as np, sys
SYMS=open('/tmp/m5/symbols.txt').read().split()
K=5.0          # shock = |r| >= K x mediaan |r| zelfde tijdslot, vorige 20 dagen
HOLDS=(6,12,24)   # 30/60/120 min (in M5-bars)
COMM_BP=0.5
rows=[]
for s in SYMS:
    hdr=open(f'/tmp/m5/{s}.csv.gz','rb')
    d=pd.read_csv(f'/tmp/m5/{s}.csv.gz',sep=';',skiprows=1)
    import gzip
    point=float(gzip.open(f'/tmp/m5/{s}.csv.gz','rt').readline().split('point=')[1].split(';')[0])
    d['time']=pd.to_datetime(d['time'],format='%Y.%m.%d %H:%M'); d=d.set_index('time').sort_index()
    d=d[d.index<'2025-01-01']
    d=d[~d.index.duplicated()]
    r=(d['close']/d['open']-1)*1e4
    spr=(d['spread']*point/d['close']*1e4).clip(lower=0)
    slot=d.index.hour*60+d.index.minute
    df=pd.DataFrame({'r':r,'spr':spr,'slot':slot,'date':d.index.normalize()}).dropna()
    ar=df['r'].abs()
    # mediaan |r| en spread per tijdslot over vorige 20 dagen (shift 1 -> geen lookahead)
    df['ar']=ar
    g=df.groupby('slot')
    df['scale']=g['ar'].transform(lambda x:x.shift(1).rolling(20,min_periods=10).median())
    df['spr_med']=g['spr'].transform(lambda x:x.shift(1).rolling(20,min_periods=10).median())
    df['z']=df['ar']/df['scale'].replace(0,np.nan)
    # context-features
    c=d['close'].reindex(df.index)
    df['trend1h']=(c/c.shift(12)-1)*1e4
    df['trend1d']=(c/c.shift(288)-1)*1e4
    df['vol1h']=df['r'].rolling(12).std()
    df['dow']=df.index.dayofweek
    idx=np.arange(len(df)); cl=c.values
    cand=np.where((df['z'].values>=K)&(df['ar'].values>=3.0))[0]
    last_exit=-1
    for i in cand:
        e=i+1
        if e<=last_exit or e+max(HOLDS)>=len(df): continue
        if (df.index[e+max(HOLDS)]-df.index[e]).total_seconds()>max(HOLDS)*300*1.5: continue  # gaten (weekend/sessie) overslaan
        side=np.sign(df['r'].iloc[i])
        entry=cl[e]; cost=df['spr'].iloc[e]+COMM_BP
        rec=dict(sym=s,time=df.index[e],side=side,z=df['z'].iloc[i],shock_bp=df['r'].iloc[i],spr_ratio=df['spr'].iloc[i]/max(df['spr_med'].iloc[i],1e-9),
                 trend1h=df['trend1h'].iloc[i],trend1d=df['trend1d'].iloc[i],vol1h=df['vol1h'].iloc[i],slot=int(df['slot'].iloc[i]),dow=int(df['dow'].iloc[i]),cost_bp=cost)
        for h in HOLDS: rec[f'ret{h*5}']=side*(cl[e+h]/entry-1)*1e4
        rows.append(rec); last_exit=e+max(HOLDS)
    print(s,len(df),'events tot nu',len(rows),flush=True)
ev=pd.DataFrame(rows); ev.to_csv('results/ceo/shock_events.csv.gz',index=False)
print(ev.shape)
