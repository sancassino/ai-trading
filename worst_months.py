import csv, sys
from datetime import datetime

path = sys.argv[1]
start = 100000.0
eq = start
rows = []
with open(path, encoding="utf-8-sig") as f:
    r = csv.DictReader(f, delimiter=";")
    for row in r:
        if not row.get("close_time"):
            continue
        profit = float(row["profit"])
        pct = profit / eq * 100
        rows.append((row["close_time"], row["symbol"], profit, pct, eq))
        eq += profit

rows.sort(key=lambda x: x[2])
print(f"{path}: worst 5 trades by $ and by % of equity at the time")
print("-- by $ --")
for r in rows[:5]:
    print(f"  {r[0]} {r[1]:10s} ${r[2]:>10,.2f}  ({r[3]:+.1f}% of ${r[4]:,.0f})")
rows.sort(key=lambda x: x[3])
print("-- by % of equity --")
for r in rows[:5]:
    print(f"  {r[0]} {r[1]:10s} ${r[2]:>10,.2f}  ({r[3]:+.1f}% of ${r[4]:,.0f})")
