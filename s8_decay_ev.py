"""S8 (geen trial): decay-bewuste FTMO-EV van ORB (MT5 F2) per venster; 'onder aanname fee €540/€80k'.
Schalen met max dagdip < 4% zijn toegestaan; hogere schalen alleen als bovengrens (optiewaarde, geen strategie).
Band: 30× blok-bootstrap (21 d) van de vensterreeks, op de gekozen schaal, 4.000 paden per herhaling → 10e–90e percentiel."""
import csv
import numpy as np
import q1b_products as qb

S = 80000.0
rows = list(csv.DictReader(open("results/f/F2_ORB_daily.csv"), delimiter=";"))
dates, r, d, prev = [], [], [], S
for x in rows:
    sb, mn, en = (float(x[k]) for k in ("start_balance", "min_equity", "end_equity"))
    dates.append(x["date"]); r.append(en / prev - 1); d.append(max(0.0, (sb - mn) / S)); prev = en
dates, r, d = np.array(dates), np.array(r), np.array(d)
W = {"(a) 2021–26": ("2021", "2027"), "(b) 2024–26": ("2024", "2027"), "(c) 2025-01…2026-09": ("2025", "2027"), "(d) 2021–23": ("2021", "2024")}
ALLOWED = [0.5, 1, 1.5, 2, 2.5]
UPPER = [3, 4, 5, 6, 8]
rng = np.random.default_rng(3)
for name, (a, b) in W.items():
    m = (dates >= a) & (dates < b)
    rw, dw = r[m], d[m]
    sr = rw.mean() / rw.std() * np.sqrt(252)
    ok = [t for t in ALLOWED if dw.max() * t < 0.04]
    for prod in ("2step", "scaling"):
        qb.SCALES = ok; qb.NPATH = 20000
        t, net, pl, fu = qb.best(rw, dw, prod)
        qb.SCALES = UPPER
        tu, netu, plu, fuu = qb.best(rw, dw, prod)
        band = ""
        if prod == "2step":
            qb.NPATH = 4000; vals = []
            n = len(rw)
            for k in range(30):
                st = rng.integers(0, n, n // 21 + 1)
                idx = ((st[:, None] + np.arange(21)[None, :]).ravel() % n)[:n]
                vals.append(qb.simulate(rw[idx], dw[idx], t, prod, seed=100 + k)[0])
            band = f" | band 10–90%: €{np.percentile(vals, 10):,.0f} … €{np.percentile(vals, 90):,.0f}"
            qb.NPATH = 20000
        print(f"{name:<22} {prod:<8} N {m.sum()} d, SR {sr:+.2f}, max dip {dw.max()*100:.2f}% | toegestaan (dip<4%) schaal {t}×: €{net:,.0f}/mnd, "
              f"P(netto<0) {pl*100:.0f}%, funded {fu*100:.0f}%{band} | bovengrens (optiewaarde) {tu}×: €{netu:,.0f}", flush=True)
