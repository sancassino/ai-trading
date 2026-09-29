"""Benadering van een plateau-ensemble: N configs tegelijk, elk 1/N van de
exposure. Zonder guard is P&L ~lineair in exposure, dus ensemble-balance/equity
= 100k + k * gemiddelde afwijking van de losse runs. k = exposure-schaal t.o.v.
de runs (30%). Rapporteert FTMO-maatstaven op dagniveau + train/test.
Gebruik: python3 ensemble_eval.py "results/plateau/PL_t?_l?_r10_daily.csv" 1 1.5 2
"""
import csv, glob, sys
START = 100000.0; SPLIT = "2024.08.01"
files = sorted(glob.glob(sys.argv[1]))
data = [{r["date"]: (float(r["start_balance"]), float(r["start_equity"]), float(r["min_equity"]), float(r["end_equity"]))
         for r in csv.DictReader(open(f, encoding="utf-8-sig"), delimiter=";") if r.get("date")} for f in files]
dates = sorted(set.intersection(*[set(d) for d in data]))
avg = [[sum(d[t][i] for d in data) / len(data) - START for i in range(4)] for t in dates]
print(f"{len(files)} runs, {len(dates)} dagen")
print(f"{'k':>5}{'$/mnd':>8}{'train':>8}{'test':>8}{'statDD':>8}{'trailDD':>8}{'dagDD':>7}{'dagen>4%':>9}  per jaar")
for k in map(float, sys.argv[2:]):
    pk = START; dd = sdd = dl = 0; n4 = 0; yr = {}
    for t, (b, s, m, e) in zip(dates, avg):
        B, M, E = START + k*b, START + k*m, START + k*e
        sdd = max(sdd, (START - M)/START); dd = max(dd, (pk - M)/pk); pk = max(pk, E)
        loss = (B - M)/START; dl = max(dl, loss); n4 += loss > 0.04
        yr.setdefault(t[:4], [E, E]); yr[t[:4]][1] = E
    i = next(j for j, t in enumerate(dates) if t >= SPLIT)
    tot = k*avg[-1][3]/(len(dates)/21); tr = k*(avg[i][1]-avg[0][1])/(i/21); te = k*(avg[-1][3]-avg[i][1])/((len(dates)-i)/21)
    ys = " ".join(f"{y[2:]}:{(v[1]-v[0])/1000:+.1f}k" for y, v in yr.items())
    print(f"{k:>5}{tot:>8,.0f}{tr:>8,.0f}{te:>8,.0f}{sdd*100:>7.1f}%{dd*100:>7.1f}%{dl*100:>6.1f}%{n4:>9}  {ys}")
