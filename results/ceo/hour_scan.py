import pandas as pd,numpy as np,glob,os
cost={}
for l in open('/tmp/stk_costs.csv'):
    p=l.strip().split(';')
    try:cost[p[0]]=float(p[1])
    except:pass
files=sorted(glob.glob('/tmp/m5/*.csv.gz')+glob.glob('/tmp/stk/*.csv.gz'))
rows=[]
for f in files:
    s=os.path.basename(f).split('.')[0]
    if s=='symbols':continue
    d=pd.read_csv(f,sep=';',skiprows=1);d['time']=pd.to_datetime(d['time'],format='%Y.%m.%d %H:%M');d=d.set_index('time').sort_index();d=d[~d.index.duplicated()]
    d=d[d.index<'2025-01-01']
    g=d.groupby([d.index.date,d.index.hour]).agg(o=('open','first'),c=('close','last'),n=('open','size'))
    g=g[g.n>=10];g['r']=(g.c/g.o-1)*1e4
    g=g.reset_index();g.columns=['day','hour','o','c','n','r'];g['day']=pd.to_datetime(g.day)
    for h,x in g.groupby('hour'):
        tr=x[x.day<'2024-01-01'];te=x[x.day>='2024-01-01']
        if len(tr)<300 or len(te)<80:continue
        t=tr.r.mean()/(tr.r.std()/np.sqrt(len(tr)))
        tt=te.r.mean()/(te.r.std()/np.sqrt(len(te)))
        rows.append((s,h,len(tr),tr.r.mean(),t,te.r.mean(),tt))
R=pd.DataFrame(rows,columns=['sym','hour','Ntr','m_tr','t_tr','m_te','t_te'])
R['cost']=R.sym.map(lambda s:cost.get(s,3.0))
print('hypotheses',len(R))
sel=R[(R.t_tr.abs()>=4)&(R.m_tr.abs()>=2*R.cost)]
print('geselecteerd (train |t|>=4 & |m|>=2x kosten):',len(sel))
sel=sel.copy();sel['sign']=np.sign(sel.m_tr);sel['net_te']=sel.sign*sel.m_te-sel.cost;sel['t_te_s']=sel.sign*sel.t_te
print(sel.round(2).sort_values('t_tr',key=abs,ascending=False).head(25).to_string(index=False))
print('forward-share: positieve netto test', (sel.net_te>0).mean() if len(sel) else None)
print('top-train-|t| (ongeacht kosten), test-teken gelijk:',(np.sign(R.m_tr)==np.sign(R.m_te))[R.t_tr.abs()>=3].mean(),' N=',(R.t_tr.abs()>=3).sum())
R.to_csv('/tmp/hour_scan.csv',index=False)
