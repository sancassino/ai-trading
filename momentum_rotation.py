import csv
from datetime import datetime
from collections import defaultdict

SYMS = {
    "US500": "US500cash_rates.csv",
    "US100": "US100cash_rates.csv",
    "US30":  "US30cash_rates.csv",
    "EU50":  "EU50cash_rates.csv",
    "UK100": "UK100cash_rates.csv",
    "GER40": "GER40cash_rates.csv",
}

def load(path):
    out = {}
    with open(path, encoding="utf-8-sig") as f:
        r = csv.DictReader(f, delimiter=";")
        for row in r:
            d = datetime.strptime(row["date"], "%Y.%m.%d").date()
            out[d] = float(row["close"])
    return out

series = {k: load(v) for k, v in SYMS.items()}

# common trading calendar = union of dates, forward-filled per symbol
all_dates = sorted(set().union(*[set(s.keys()) for s in series.values()]))

def price_on(sym, d, ffill_cache={}):
    # last known price on or before d
    key = (sym, d)
    if key in ffill_cache:
        return ffill_cache[key]
    s = series[sym]
    if d in s:
        ffill_cache[key] = s[d]
        return s[d]
    return None

# build month-end rebalance dates
month_ends = []
cur_month = None
for d in all_dates:
    m = (d.year, d.month)
    if m != cur_month:
        if month_ends:
            pass
        cur_month = m
    month_ends.append(d)
last_of_month = {}
for d in all_dates:
    last_of_month[(d.year, d.month)] = d
rebalance_dates = sorted(last_of_month.values())

LOOKBACK_MONTHS = 6
TOP_N = 2
START_BALANCE = 100000.0

def get_price_series_sorted(sym):
    return sorted(series[sym].items())

# index each symbol's dates for fast lookback lookup
sym_dates_sorted = {k: sorted(v.keys()) for k, v in series.items()}

def price_near(sym, target_date):
    # last available price <= target_date
    ds = sym_dates_sorted[sym]
    lo, hi = 0, len(ds) - 1
    best = None
    for d in ds:
        if d <= target_date:
            best = d
        else:
            break
    if best is None:
        return None
    return series[sym][best]

balance = START_BALANCE
monthly_pnl = defaultdict(float)
holdings = {}  # sym -> (entry_price, weight)

for i in range(LOOKBACK_MONTHS, len(rebalance_dates)):
    today = rebalance_dates[i]
    lookback_date = rebalance_dates[i - LOOKBACK_MONTHS]

    # close existing holdings at today's price, realize P&L
    if holdings:
        total_pnl = 0.0
        for sym, (entry_price, weight) in holdings.items():
            p = price_near(sym, today)
            if p is None or entry_price is None:
                continue
            ret = (p - entry_price) / entry_price
            total_pnl += weight * balance * ret
        balance += total_pnl
        monthly_pnl[(today.year, today.month)] += total_pnl
        holdings = {}

    # rank all symbols by trailing return over lookback window
    scores = []
    for sym in SYMS:
        p_now = price_near(sym, today)
        p_then = price_near(sym, lookback_date)
        if p_now is None or p_then is None or p_then == 0:
            continue
        ret = (p_now - p_then) / p_then
        scores.append((ret, sym, p_now))
    scores.sort(reverse=True)
    top = scores[:TOP_N]
    if not top:
        continue
    weight = 1.0 / len(top)
    for ret, sym, p_now in top:
        holdings[sym] = (p_now, weight)

print(f"Momentum rotation: top {TOP_N} of {len(SYMS)}, {LOOKBACK_MONTHS}mo lookback, monthly rebalance")
print(f"Start balance: ${START_BALANCE:,.0f}  End balance: ${balance:,.2f}  Total return: {(balance/START_BALANCE-1)*100:.1f}%")
years = defaultdict(float)
for (y, m), pnl in monthly_pnl.items():
    years[y] += pnl
print(f"\nyears positive: {sum(1 for y in years if years[y]>0)}/{len(years)}")
for y in sorted(years):
    print(f"  {y}: ${years[y]:>10,.2f}")
months_pos = sum(1 for k in monthly_pnl if monthly_pnl[k] > 0)
print(f"\nmonths positive: {months_pos}/{len(monthly_pnl)} ({months_pos/len(monthly_pnl)*100:.1f}%)")
avg_month = sum(monthly_pnl.values()) / len(monthly_pnl)
print(f"avg $/month: ${avg_month:,.2f}")

# equity curve + drawdown (unscaled, 100% notional every month)
eq = START_BALANCE
peak = START_BALANCE
max_dd = 0.0
max_dd_date = None
sorted_months = sorted(monthly_pnl.keys())
worst_month = min(monthly_pnl.values())
worst_month_key = min(monthly_pnl, key=monthly_pnl.get)
for k in sorted_months:
    eq += monthly_pnl[k]
    peak = max(peak, eq)
    dd = (peak - eq) / peak
    if dd > max_dd:
        max_dd = dd
        max_dd_date = k
print(f"\nmax drawdown (unscaled, full notional): {max_dd*100:.1f}% (around {max_dd_date})")
print(f"worst single month: ${worst_month:,.2f} ({worst_month_key}) = {worst_month/START_BALANCE*100:.1f}% of start balance")
