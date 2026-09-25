import csv, sys
from datetime import datetime

path = sys.argv[1]
start = 100000.0
eq = start
peak = start
peak_date = None
max_dd_peak = 0.0
max_dd_peak_range = (None, None)
max_dd_floor = 0.0  # below the fixed $100k start
max_dd_floor_date = None
worst_trade_pct = 0.0
worst_trade = None
with open(path, encoding="utf-8-sig") as f:
    r = csv.DictReader(f, delimiter=";")
    for row in r:
        if not row.get("close_time"):
            continue
        profit = float(row["profit"])
        pct_of_eq = profit / eq * 100
        if pct_of_eq < worst_trade_pct:
            worst_trade_pct = pct_of_eq
            worst_trade = (row["close_time"], row["symbol"], profit, eq)
        eq += profit
        if eq > peak:
            peak = eq
            peak_date = row["close_time"]
        dd_peak = (peak - eq) / peak
        if dd_peak > max_dd_peak:
            max_dd_peak = dd_peak
            max_dd_peak_range = (peak_date, row["close_time"])
        dd_floor = (start - eq) / start
        if dd_floor > max_dd_floor:
            max_dd_floor = dd_floor
            max_dd_floor_date = row["close_time"]

print(f"final equity: ${eq:,.2f}")
print(f"max drawdown from trailing peak: {max_dd_peak*100:.1f}% (peak {max_dd_peak_range[0]} -> trough {max_dd_peak_range[1]})")
print(f"max drawdown below fixed $100k start: {max_dd_floor*100:.1f}% (on {max_dd_floor_date})")
print(f"worst single trade: {worst_trade[0]} {worst_trade[1]} ${worst_trade[2]:,.2f} ({worst_trade[2]/worst_trade[3]*100:.1f}% of equity at the time)")
