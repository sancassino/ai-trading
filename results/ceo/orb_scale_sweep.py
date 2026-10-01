import numpy as np
from engine import ftmo as f
r,dd=f.load_daily_equity_csv('/tmp/F2.csv')
r=np.array(r); dd=np.array(dd)
print('F2-ORB 2021-2026 (incl. 2025+ beschrijvend), intradag-trough, ftmo_ev per schaal')
for sc in (1.5,2.8,4.0,5.0,6.0,8.0,10.0):
    o=f.ftmo_ev(r,daily_drawdowns=dd,scale=sc,n_paths=6000,seed=7)
    print(f'schaal {sc:4.1f}  p1={o["p_pass_1"]:.2f} p2={o["p_pass_2"]:.2f} overleef={o["p_survive"]:.2f} p_netto_verlies={o["p_net_loss"]:.2f} pogingen={o["attempts_mean"]:.1f}  net EV €/mnd={o["net_ev_monthly"]:.0f}')
# alleen <=2024 (zonder reserve)
import csv
rows=[x for x in csv.DictReader(open('/tmp/F2.csv'),delimiter=';')]
n24=sum(1 for x in rows if x['date']<'2025')
print('--- alleen t/m 2024 (',n24,'dagen) ---')
for sc in (2.8,4.0,6.0):
    o=f.ftmo_ev(r[:n24],daily_drawdowns=dd[:n24],scale=sc,n_paths=6000,seed=7)
    print(f'schaal {sc:4.1f}  p1={o["p_pass_1"]:.2f} p2={o["p_pass_2"]:.2f} overleef={o["p_survive"]:.2f} net EV €/mnd={o["net_ev_monthly"]:.0f}')
