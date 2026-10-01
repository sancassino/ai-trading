import numpy as np, importlib.util
spec=importlib.util.spec_from_file_location('ftmo','/tmp/ftmo.py'); f=importlib.util.module_from_spec(spec); spec.loader.exec_module(f)
rng=np.random.default_rng(1)
n=2500
print('Synthetische dagreeks, zero-edge (mu=0) en met kostenlek, verschillende jaarvol; fee 540, split 80%')
for cost_bp_day in (0.0, 1.0, 3.0):
    for vol in (0.08,0.15,0.25,0.40):
        sd=vol/np.sqrt(252); x=rng.normal(-cost_bp_day*1e-4,sd,n)
        o=f.ftmo_ev(x,n_paths=6000,seed=3)
        print(f'kosten {cost_bp_day:3.1f} bp/dag  vol {vol*100:4.0f}%/jr  p1={o["p_pass_1"]:.2f} p2={o["p_pass_2"]:.2f} overleef={o["p_survive"]:.2f}  net_ev/mnd=€{o["net_ev_monthly"]:.0f}')
