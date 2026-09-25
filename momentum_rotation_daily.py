import csv, sys
from datetime import datetime
from collections import defaultdict

SYMS = {
    "US500": "US500cash_rates.csv",
    "US100": "US100cash_rates.csv",
    "US30":  "US30cash_rates.csv",
    "EU50":  "EU50cash_rates.csv",
    "UK100": "UK100cash_rates.csv",
    "GER40": "GER40cash_rates.csv",
    "XAU":   "XAUUSD_rates.csv",
    "OIL":   "USOILcash_rates.csv",
    "EURUSD": "EURUSD_rates.csv",
    "AAPL": "AAPL_rates.csv",
    "MSFT": "MSFT_rates.csv",
    "AMZN": "AMZN_rates.csv",
    "GOOG": "GOOG_rates.csv",
    "META": "META_rates.csv",
    "NVDA": "NVDA_rates.csv",
    "TSLA": "TSLA_rates.csv",
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
sym_dates_sorted = {k: sorted(v.keys()) for k, v in series.items()}
_all_dates_full = sorted(set().union(*[set(s.keys()) for s in series.values()]))
import os as _os
_start_cutoff = datetime.strptime(_os.environ.get("MOM_START", "2018-01-01"), "%Y-%m-%d").date()
all_dates = [d for d in _all_dates_full if d >= _start_cutoff]

def price_near(sym, target_date):
    ds = sym_dates_sorted[sym]
    best = None
    for d in ds:
        if d <= target_date:
            best = d
        else:
            break
    return series[sym].get(best) if best else None

def run(lookback_months, top_n, exposure_frac, start_balance=100000.0):
    last_of_month = {}
    for d in all_dates:
        last_of_month[(d.year, d.month)] = d
    rebalance_dates = sorted(last_of_month.values())

    holdings = {}  # sym -> (entry_price, weight)
    balance = start_balance
    equity_curve = []  # (date, equity)

    reb_idx = 0
    next_rebalance = rebalance_dates[lookback_months] if len(rebalance_dates) > lookback_months else None

    for d in all_dates:
        if d < rebalance_dates[lookback_months]:
            equity_curve.append((d, balance))
            continue

        # rebalance check
        if next_rebalance is not None and d >= next_rebalance:
            i = rebalance_dates.index(next_rebalance)
            today = next_rebalance
            lookback_date = rebalance_dates[i - lookback_months]
            if holdings:
                total_pnl = 0.0
                for sym, (entry_price, weight) in holdings.items():
                    p = price_near(sym, today)
                    if p is None or entry_price is None:
                        continue
                    ret = (p - entry_price) / entry_price
                    total_pnl += weight * exposure_frac * balance * ret
                balance += total_pnl
                holdings = {}
            scores = []
            for sym in SYMS:
                p_now = price_near(sym, today)
                p_then = price_near(sym, lookback_date)
                if p_now is None or p_then is None or p_then == 0:
                    continue
                ret = (p_now - p_then) / p_then
                scores.append((ret, sym, p_now))
            scores.sort(reverse=True)
            top = scores[:top_n]
            if top:
                weight = 1.0 / len(top)
                for ret, sym, p_now in top:
                    holdings[sym] = (p_now, weight)
            idx = rebalance_dates.index(next_rebalance)
            next_rebalance = rebalance_dates[idx + 1] if idx + 1 < len(rebalance_dates) else None

        # mark-to-market daily unrealized P&L on current holdings
        unrealized = 0.0
        for sym, (entry_price, weight) in holdings.items():
            p = price_near(sym, d)
            if p is None or entry_price is None:
                continue
            ret = (p - entry_price) / entry_price
            unrealized += weight * exposure_frac * balance * ret
        equity_curve.append((d, balance + unrealized))

    # stats
    eq_vals = [e for _, e in equity_curve]
    # trailing-peak DD (conservative reference)
    peak = eq_vals[0]
    max_dd = 0.0
    max_dd_date = None
    for d, e in equity_curve:
        peak = max(peak, e)
        dd = (peak - e) / peak
        if dd > max_dd:
            max_dd = dd
            max_dd_date = d
    # FTMO's actual rule: static floor = 10% below the ORIGINAL start balance,
    # not trailing peak. This is what actually determines a breach.
    min_eq = min(eq_vals)
    min_eq_date = equity_curve[[e for _, e in equity_curve].index(min_eq)][0]
    static_dd_from_start = (start_balance - min_eq) / start_balance
    daily_pnl = [(equity_curve[i][0], equity_curve[i][1] - equity_curve[i-1][1]) for i in range(1, len(equity_curve))]
    worst_day = min(daily_pnl, key=lambda x: x[1])
    monthly_pnl = defaultdict(float)
    for d, pnl in daily_pnl:
        monthly_pnl[(d.year, d.month)] += pnl
    years = defaultdict(float)
    for (y, m), pnl in monthly_pnl.items():
        years[y] += pnl
    total_ret = (eq_vals[-1] / start_balance - 1) * 100
    months_pos = sum(1 for k in monthly_pnl if monthly_pnl[k] > 0)
    avg_month = sum(monthly_pnl.values()) / len(monthly_pnl) if monthly_pnl else 0
    return {
        "final": eq_vals[-1], "total_ret": total_ret, "max_dd": max_dd, "max_dd_date": max_dd_date,
        "static_dd_from_start": static_dd_from_start, "min_eq_date": min_eq_date,
        "worst_day": worst_day, "years": years, "months_pos": months_pos, "n_months": len(monthly_pnl),
        "avg_month": avg_month,
    }

if __name__ == "__main__":
    lookback = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    top_n = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    exposure = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    r = run(lookback, top_n, exposure)
    print(f"lookback={lookback}mo top_n={top_n} exposure={exposure*100:.0f}%")
    print(f"final=${r['final']:,.2f} total_ret={r['total_ret']:.1f}% trailing_peak_dd={r['max_dd']*100:.1f}% (around {r['max_dd_date']})")
    print(f"FTMO static DD (below $100k start): {r['static_dd_from_start']*100:.1f}% (lowest point {r['min_eq_date']})")
    print(f"worst day: {r['worst_day'][0]} ${r['worst_day'][1]:,.2f} ({r['worst_day'][1]/100000*100:.2f}% of $100k)")
    print(f"years positive: {sum(1 for y in r['years'] if r['years'][y]>0)}/{len(r['years'])}")
    for y in sorted(r['years']):
        print(f"  {y}: ${r['years'][y]:>10,.2f}")
    print(f"months positive: {r['months_pos']}/{r['n_months']} ({r['months_pos']/r['n_months']*100:.1f}%)")
    print(f"avg $/month: ${r['avg_month']:,.2f}")
