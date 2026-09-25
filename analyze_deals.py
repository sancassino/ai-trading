import sys, csv
from collections import defaultdict
from datetime import datetime

def load(path):
    deals = []
    with open(path, encoding="utf-8-sig") as f:
        r = csv.DictReader(f, delimiter=";")
        for row in r:
            if not row.get("close_time"):
                continue
            dt = datetime.strptime(row["close_time"], "%Y.%m.%d %H:%M")
            profit = float(row["profit"])
            deals.append((dt, profit))
    return sorted(deals)

def analyze(path, start_balance=100000.0):
    deals = load(path)
    if not deals:
        print(f"{path}: no deals")
        return
    yearly = defaultdict(float)
    monthly = defaultdict(float)
    for dt, p in deals:
        yearly[dt.year] += p
        monthly[(dt.year, dt.month)] += p
    total = sum(p for _, p in deals)
    wins = sum(1 for _, p in deals if p > 0)
    n = len(deals)
    print(f"\n=== {path} ===")
    print(f"trades={n} winrate={wins/n*100:.1f}% total_profit=${total:,.2f} ({total/start_balance*100:.1f}% of ${start_balance:,.0f})")
    print(f"span: {deals[0][0].date()} .. {deals[-1][0].date()}")
    years_pos = sum(1 for y in sorted(yearly) if yearly[y] > 0)
    years_tot = len(yearly)
    print(f"years positive: {years_pos}/{years_tot}")
    for y in sorted(yearly):
        print(f"  {y}: ${yearly[y]:>10,.2f}")
    months_pos = sum(1 for k in monthly if monthly[k] > 0)
    print(f"months positive: {months_pos}/{len(monthly)} ({months_pos/len(monthly)*100:.1f}%)")
    avg_month = total / len(monthly) if monthly else 0
    print(f"avg $/month (active months only): ${avg_month:,.2f}")

if __name__ == "__main__":
    for p in sys.argv[1:]:
        analyze(p)
