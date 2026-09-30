"""U2 (informatief, geen trial): ORB-B4a vaste notional (1/7) vs vast risico per trade (ρ / OR-breedte, hefboom ≤ 4×) onder Q1b-FTMO-mechaniek.
Dagdip conservatief = som van de verliezende trades die dag. Toegestane schaal: max dagdip < 4%. 'Onder aanname fee €540/€80k'."""
from collections import defaultdict
import numpy as np
import q1b_products as qb

rows = []
for line in open("results/b4/B4_a_ORB_trades.csv"):
    if line[0].isdigit():
        d, s, n, r = line.strip().split(";")
        if r:
            rows.append((d, float(n), float(r)))
days = sorted({d for d, *_ in rows})
def series(w_fn):
    ret, dip = defaultdict(float), defaultdict(float)
    for d, n, r in rows:
        w = w_fn(n, r)
        ret[d] += w * n; dip[d] += w * max(0.0, -n)
    return np.array([ret[d] for d in days]), np.array([dip[d] for d in days])
fixed = series(lambda n, r: 1 / 7)
risk = series(lambda n, r: min(4.0, 0.0025 / (n / r)) if r != 0 and n / r > 0 else 0.0)  # ρ = 0,25% equity per trade
for name, (r, d) in (("vaste notional 1/7", fixed), ("vast risico 0,25%/trade", risk)):
    sr = r.mean() / r.std() * np.sqrt(252); sk = float((((r - r.mean()) / r.std()) ** 3).mean())
    ok = [t for t in (0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10) if d.max() * t < 0.04]
    qb.SCALES = ok
    t, net, pl, fu = qb.best(r, d, "2step")
    print(f"{name:<24} SR {sr:+.2f} skew {sk:+.2f} jaarvol {r.std()*np.sqrt(252)*100:.1f}% max dip {d.max()*100:.2f}% P99 dip {np.percentile(d,99)*100:.2f}% | "
          f"toegestaan tot {max(ok)}× → beste {t}×: €{net:,.0f}/mnd, P(netto<0) {pl*100:.0f}%, funded {fu*100:.0f}%", flush=True)
