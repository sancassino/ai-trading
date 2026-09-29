"""Train/test-split op de dagelijkse equity van bestaande runs (EA is causaal,
dus de testperiode van een volle run = een run die in 2024-08 start, op
compounding na). Train: 2021-01..2024-07, test: 2024-08..eind.
Gebruik: python3 split_eval.py results/plateau/*_daily.csv"""
import csv, sys
SPLIT = "2024.08.01"
rows = []
for p in sys.argv[1:]:
    d = [(r["date"], float(r["start_equity"]), float(r["min_equity"]), float(r["end_equity"]))
         for r in csv.DictReader(open(p, encoding="utf-8-sig"), delimiter=";") if r.get("date")]
    tr = [x for x in d if x[0] < SPLIT]; te = [x for x in d if x[0] >= SPLIT]
    def stats(seg, base):
        pk = seg[0][1]; dd = 0
        for _, s, m, e in seg:
            dd = max(dd, (pk - m) / pk); pk = max(pk, e)
        pnl = seg[-1][3] - seg[0][1]
        return pnl / (len(seg) / 21), pnl / seg[0][1] * 100, dd * 100
    a, b = stats(tr, 1), stats(te, 1)
    rows.append((p.split("/")[-1].replace("_daily.csv", ""), a, b))
rows.sort(key=lambda r: -r[1][0])
print(f"{'config':<26}{'train /m':>10}{'tr DD':>7}{'test /m':>10}{'test %':>8}{'te DD':>7}")
for n, a, b in rows:
    print(f"{n:<26}{a[0]:>10,.0f}{a[2]:>6.1f}%{b[0]:>10,.0f}{b[1]:>7.1f}%{b[2]:>6.1f}%")
