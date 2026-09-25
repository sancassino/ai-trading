import csv, random
from collections import defaultdict

def load_monthly_returns(path, start_balance=100000.0):
    """Rebuild the real equity curve from actual MT5 trades and return the
    list of REAL monthly % returns (not $ amounts) so they can be
    bootstrap-resampled and compounded onto any starting balance."""
    monthly_pnl = defaultdict(float)
    with open(path, encoding="utf-8-sig") as f:
        r = csv.DictReader(f, delimiter=";")
        eq = start_balance
        rows = []
        for row in r:
            if not row.get("close_time"):
                continue
            rows.append((row["close_time"], float(row["profit"])))
    rows.sort()
    eq = start_balance
    for close_time, profit in rows:
        month_key = close_time[:7]
        monthly_pnl[month_key] += profit
    # convert to sequential % returns against a running compounded balance
    eq = start_balance
    pct_returns = []
    for k in sorted(monthly_pnl):
        ret = monthly_pnl[k] / eq
        pct_returns.append(ret)
        eq += monthly_pnl[k]
    return pct_returns

def simulate(pct_returns, n_sims=20000, phase1_target=0.10, phase2_target=0.05,
             max_dd=0.10, max_months=18, seed=42, block_size=6):
    """Block-bootstrap: draw contiguous BLOCKS of real consecutive months
    (not i.i.d. single months) so regime persistence -- like the ~15-month
    2022 drawdown -- can show up as a clustered run in the simulated path,
    the same way real bad regimes actually unfold, instead of averaging out
    across independent monthly draws."""
    rng = random.Random(seed)
    n = len(pct_returns)
    max_start = n - block_size
    phase1_pass = 0
    funded = 0
    live_income_ok = 0

    def month_stream():
        """Yields an endless stream of real returns as contiguous blocks."""
        while True:
            start = rng.randrange(0, max(1, max_start + 1))
            for i in range(block_size):
                yield pct_returns[(start + i) % n]

    for _ in range(n_sims):
        stream = month_stream()
        balance = 100000.0
        floor = balance * (1 - max_dd)
        phase = 1
        phase_start_balance = balance
        breached = False

        for m in range(max_months):
            r = next(stream)
            balance *= (1 + r)

            if balance < floor:
                breached = True
                break

            if phase == 1 and balance >= phase_start_balance * (1 + phase1_target):
                phase = 2
                # FTMO's max DD is static from the ORIGINAL 100k, not reset
                phase_start_balance = balance
            elif phase == 2 and balance >= phase_start_balance * (1 + phase2_target):
                phase = 3  # funded / live
                phase_start_balance = balance
                break

        if breached:
            continue
        if phase >= 2:
            phase1_pass += 1
        if phase == 3:
            funded += 1
            # simulate 12 more months live, same static floor from ORIGINAL 100k
            live_floor = 100000.0 * (1 - max_dd)
            live_balance = balance
            live_breached = False
            monthly_dollar = []
            for m in range(12):
                r = next(stream)
                pnl = live_balance * r
                live_balance += pnl
                monthly_dollar.append(pnl)
                if live_balance < live_floor:
                    live_breached = True
                    break
            if not live_breached and len(monthly_dollar) == 12:
                avg_month = sum(monthly_dollar) / 12
                if avg_month >= 1000:
                    live_income_ok += 1

    return {
        "phase1_pass": phase1_pass / n_sims,
        "funded": funded / n_sims,
        "live_income_ok_given_attempt": live_income_ok / n_sims,
    }

if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "MR_t2_l3.csv"
    rets = load_monthly_returns(path)
    print(f"{path}: {len(rets)} real monthly returns loaded")
    print(f"  mean monthly return: {sum(rets)/len(rets)*100:.2f}%  min: {min(rets)*100:.2f}%  max: {max(rets)*100:.2f}%")
    result = simulate(rets)
    print(f"\nMonte Carlo (block-bootstrap of REAL monthly returns, FTMO rules: phase1=10%, phase2=5%, maxDD=10% static):")
    print(f"  Phase 1 pass:               {result['phase1_pass']*100:.1f}%")
    print(f"  Funded (phase1+2):          {result['funded']*100:.1f}%")
    print(f"  Live >=$1000/mo avg, 12mo:  {result['live_income_ok_given_attempt']*100:.1f}% (of all sims, not just funded ones)")
