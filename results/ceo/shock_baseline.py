import pandas as pd, numpy as np
ev=pd.read_csv('results/ceo/shock_events.csv.gz',parse_dates=['time'])
ev['date']=ev.time.dt.normalize()
cls={'US30cash':'idx','US100cash':'idx','US500cash':'idx','GER40cash':'idx','UK100cash':'idx','JP225cash':'idx','EU50cash':'idx','FRA40cash':'idx','XAUUSD':'met','XAGUSD':'met','XCUUSD':'met','USOILcash':'en','UKOILcash':'en','NATGAScash':'en','BTCUSD':'cry','ETHUSD':'cry'}
ev['cls']=ev.sym.map(cls).fillna('fx')
def stat(x,col,sign,stress):
    n=sign*x[col]-stress*x.cost_bp
    # dag-geclusterd t: som per dag
    byd=n.groupby(x.date).sum()
    t=byd.mean()/(byd.std(ddof=1)/np.sqrt(len(byd))) if len(byd)>2 else np.nan
    return len(x),n.mean(),t
tr=ev[ev.time<'2024-01-01']; va=ev[(ev.time>='2024-01-01')&(ev.time<'2025-01-01')]
print('events train',len(tr),'val',len(va))
rows=[]
for h in (30,60,120):
    for sign,nm in((1,'mee'),(-1,'tegen')):
        for stress in (1,2):
            n1,m1,t1=stat(tr,f'ret{h}',sign,stress); n2,m2,t2=stat(va,f'ret{h}',sign,stress)
            rows.append((h,nm,stress,n1,round(m1,2),round(t1,2),n2,round(m2,2),round(t2,2)))
print(pd.DataFrame(rows,columns=['hold','richt','kostx','N_tr','net_tr','t_tr','N_va','net_va','t_va']).to_string(index=False))
print('\nper klasse, hold 60, kostx2 (train | val):')
for c,g in tr.groupby('cls'):
    for sign,nm in((1,'mee'),(-1,'tegen')):
        a=stat(g,'ret60',sign,2); b=stat(va[va.cls==c],'ret60',sign,2)
        print(f'{c:4s} {nm:5s} N={a[0]:6d} net={a[1]:+6.2f} t={a[2]:+5.2f} | N={b[0]:5d} net={b[1]:+6.2f} t={b[2]:+5.2f}')
print('\nper z-bucket (alle klassen), hold 60, kostx2, train:')
tr=tr.assign(zb=pd.qcut(tr.z,5,duplicates='drop'))
for zb,g in tr.groupby('zb',observed=True):
    a=stat(g,'ret60',1,2); b=stat(g,'ret60',-1,2); print(zb,f'mee {a[1]:+.2f} (t {a[2]:+.2f})  tegen {b[1]:+.2f} (t {b[2]:+.2f})  N={a[0]}')
