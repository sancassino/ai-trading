"""Maak een ensemble-dagreeks (gemiddeld dagrendement van meerdere runs, gelijk gewogen,
dagelijks herbalanceerd) in het *_daily.csv-formaat. Gebruik: python3 make_ensemble_daily.py out.csv 'glob'"""
import csv, glob, sys
files = sorted(glob.glob(sys.argv[2]))
series = []
for f in files:
    rows = {r["date"]: float(r["end_equity"]) for r in csv.DictReader(open(f, encoding="utf-8-sig"), delimiter=";") if r.get("date")}
    series.append(rows)
dates = sorted(set.intersection(*[set(s) for s in series]))
eq = 100000.0
with open(sys.argv[1], "w") as out:
    out.write("date;start_balance;start_equity;min_equity;end_equity\n")
    out.write(f"{dates[0]};{eq:.2f};{eq:.2f};{eq:.2f};{eq:.2f}\n")
    for a, b in zip(dates, dates[1:]):
        r = sum(s[b] / s[a] - 1 for s in series) / len(series)
        prev, eq = eq, eq * (1 + r)
        out.write(f"{b};{prev:.2f};{prev:.2f};{min(prev, eq):.2f};{eq:.2f}\n")
print(f"{sys.argv[1]}: {len(files)} runs, {len(dates)} dagen")
