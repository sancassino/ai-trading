import numpy as np, pandas as pd, importlib.util, sys
spec=importlib.util.spec_from_file_location('ftmo','/tmp/ftmo.py'); f=importlib.util.module_from_spec(spec); spec.loader.exec_module(f)
d=pd.read_csv('/tmp/SPX.csv',sep=';',comment='#',parse_dates=['date']).set_index('date')['close']
START=sys.argv[1]; d=d[d.index>=START]; r=d.pct_change().dropna()
SW=0.0495/252   # FTMO US500 long swap, % per night of notional
def run(name,L,filt,start='2011-01-01'):
    pos=np.ones(len(r)) if not filt else (d.shift(1).rolling(1).mean().reindex(r.index) > d.rolling(200).mean().shift(1).reindex(r.index)).astype(float).values
    pos=np.nan_to_num(pos)
    x=(r.values*pos - SW*pos)*L
    ann=x.mean()*252; vol=x.std()*np.sqrt(252)
    out=f.ftmo_ev(x,n_paths=6000,seed=7)
    print(f'{name:18s} L={L:4.2f} netto {ann*100:5.1f}%/jr vol {vol*100:4.1f}% p1*p2={out["p_pass_1"]*out["p_pass_2"]:.2f} overleef={out["p_survive"]:.2f} net_ev_mnd={out["net_ev_monthly"]:.0f}')
print('SPX vanaf',START,';')
print(' long US500 CFD, swap -4.95%/jr, dividend/spread genegeerd')
for L in (0.25,0.5,0.75,1.0):
    run('buy&hold',L,False)
for L in (0.5,1.0,1.5):
    run('trend (>200d MA)',L,True)
