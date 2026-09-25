import csv, sys
from collections import defaultdict

path = sys.argv[1]
monthly = defaultdict(float)
with open(path, encoding="utf-8-sig") as f:
    r = csv.DictReader(f, delimiter=";")
    for row in r:
        if not row.get("close_time"):
            continue
        d = row["close_time"][:7]  # YYYY.MM
        monthly[d] += float(row["profit"])

total_profit = sum(v for v in monthly.values() if v > 0)  # gross positive months
net_total = sum(monthly.values())
sorted_months = sorted(monthly.items(), key=lambda x: -x[1])

print(f"{path}: net total = ${net_total:,.2f}, sum of positive months = ${total_profit:,.2f}")
running = 0
for i, (m, v) in enumerate(sorted_months[:5], 1):
    running += v
    pct_of_gross = running / total_profit * 100 if total_profit else 0
    pct_of_net = running / net_total * 100 if net_total else 0
    print(f"  top-{i}: {m} ${v:>10,.2f}  cumulative ${running:>10,.2f}  ({pct_of_gross:.1f}% of gross-positive, {pct_of_net:.1f}% of net)")
