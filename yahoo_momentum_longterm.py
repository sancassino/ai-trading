import csv
from datetime import datetime
from collections import defaultdict

SYMS = {"SP500": "YAHOO_SP500.csv", "NASDAQ": "YAHOO_NASDAQ.csv", "DOW": "YAHOO_DOW.csv", "GOLD": "YAHOO_GOLD.csv"}

def load(path):
    out = {}
    with open(path, encoding="utf-8-sig") as f:
        r = csv.DictReader(f, delimiter=";")
        for row in r:
            d = datetime.strptime(row["date"], "%Y.%m.%d").date()
            out[d] = float(row["close"])
    return out

series = {k: load(v) for k, v in SYMS.items()}
sym_dates_sorted = {k: sorted(v.keys()) for k, v in series.items()}
all_dates = sorted(set().union(*[set(s.keys()) for s in series.values()]))

def price_near(sym, target_date):
    ds = sym_dates_sorted[sym]
    best = None
    for d in ds:
        if d <= target_date:
            best = d
        else:
            break
    return series[sym].get(best) if best else None

def run(lookback_months, top_n, start_date=None, end_date=None, regime_sma_months=0, regime_sym="SP500"):
    last_of_month = {}
    for d in all_dates:
        if start_date and d < start_date: continue
        if end_date and d > end_date: continue
        last_of_month[(d.year, d.month)] = d
    rebalance_dates = sorted(last_of_month.values())
    if len(rebalance_dates) <= lookback_months:
        return None

    holdings = {}
    monthly_pnl = defaultdict(float)
    balance = 100000.0

    for i in range(lookback_months, len(rebalance_dates)):
        today = rebalance_dates[i]
        lookback_date = rebalance_dates[i - lookback_months]
        if holdings:
            total_pnl = 0.0
            for sym, (entry_price, weight) in holdings.items():
                p = price_near(sym, today)
                if p is None or entry_price is None: continue
                ret = (p - entry_price) / entry_price
                total_pnl += weight * balance * ret
            balance += total_pnl
            monthly_pnl[(today.year, today.month)] += total_pnl
            holdings = {}
        risk_on = True
        if regime_sma_months > 0:
            sma_vals = []
            for j in range(regime_sma_months):
                d = rebalance_dates[i - j] if i - j >= 0 else None
                if d is None: continue
                p = price_near(regime_sym, d)
                if p is not None: sma_vals.append(p)
            if sma_vals:
                sma = sum(sma_vals) / len(sma_vals)
                now_regime = price_near(regime_sym, today)
                risk_on = now_regime is not None and now_regime > sma

        if risk_on:
            scores = []
            for sym in SYMS:
                p_now = price_near(sym, today)
                p_then = price_near(sym, lookback_date)
                if p_now is None or p_then is None or p_then == 0: continue
                scores.append(((p_now - p_then) / p_then, sym, p_now))
            scores.sort(reverse=True)
            top = scores[:top_n]
            if top:
                w = 1.0 / len(top)
                for ret, sym, p_now in top:
                    holdings[sym] = (p_now, w)

    years = defaultdict(float)
    for (y, m), pnl in monthly_pnl.items():
        years[y] += pnl
    return balance, years, monthly_pnl

if __name__ == "__main__":
    import sys
    lb = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    tn = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    rsma = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    result = run(lb, tn, regime_sma_months=rsma)
    if result is None:
        print("not enough data"); sys.exit()
    balance, years, monthly = result
    print(f"4-instrument (SP500/NASDAQ/DOW/GOLD) momentum rotation, lookback={lb}mo top={tn}, 2000-2026 (Yahoo data, directional only)")
    print(f"final balance: ${balance:,.2f}  total return: {(balance/100000-1)*100:.1f}%")
    print(f"years positive: {sum(1 for y in years if years[y]>0)}/{len(years)}")
    for y in sorted(years):
        marker = "  <-- dotcom" if y in (2000,2001,2002) else ("  <-- GFC" if y in (2008,) else ("  <-- 2022-hikes" if y==2022 else ""))
        print(f"  {y}: ${years[y]:>10,.2f}{marker}")
