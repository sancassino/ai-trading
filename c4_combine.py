"""C4: sizing RSI(2) (SPX+NDX) en gelijk-risico-combinatie RSI(2) + ORB, exact volgens PREREG_C4.md."""
import csv
import math
import statistics
from collections import defaultdict
from datetime import date, datetime

import stats_tools as st
from b2_sim import UNIV, load, sleeve


def curve_stats(rets):
    eq, peak, mdd = 1.0, 1.0, 0.0
    for r in rets:
        eq *= 1 + r; peak = max(peak, eq); mdd = max(mdd, 1 - eq / peak)
    return eq, mdd, min(rets)


def max_scale(rets, dd_lim=0.08, day_lim=0.03):
    k, best = 0.05, 0.0
    while k <= 20:
        _, mdd, worst = curve_stats([r * k for r in rets])
        if mdd < dd_lim and -worst < day_lim:
            best = k
        else:
            break
        k = round(k + 0.05, 2)
    return best


def describe(label, dated, k):
    rets = [r * k for _, r in dated]
    eq, mdd, worst = curve_stats(rets)
    yrs = len(rets) / 252
    cagr = eq ** (1 / yrs) - 1
    print(f"{label}: schaal {k:.2f} | {yrs:.1f} jr | CAGR {cagr*100:+.2f}% | €/mnd op €80k ≈ {cagr*80000/12:,.0f} | "
          f"SR {st.sharpe(rets)[0]:.2f} | t {st.t_stat(rets):.2f} | DD {mdd*100:.1f}% | slechtste dag {worst*100:.2f}% | "
          f"DSR340 {st.deflated_sharpe(rets, 340)[0]:.2f}")
    yr = defaultdict(float)
    for (d, _), r in zip(dated, rets):
        yr[d.year] = (1 + yr[d.year]) * (1 + r) - 1
    print("    per jaar: " + " ".join(f"{str(y)[2:]}:{v*100:+.1f}" for y, v in sorted(yr.items())))


def main():
    # (a) RSI(2) SPX + NDX, 50/50
    s = {}
    for n in ("SPX", "NDX"):
        fn, start = UNIV["abd"][n]
        s[n] = sleeve("b", load(fn), start)[0]
    dates = sorted(set(s["SPX"]) | set(s["NDX"]))
    rsi = [(d, 0.5 * s["SPX"].get(d, 0.0) + 0.5 * s["NDX"].get(d, 0.0)) for d in dates]
    k = max_scale([r for _, r in rsi])
    describe("(a) RSI(2) SPX+NDX", rsi, k)
    h = lambda a, b: math.prod(1 + r * k for d, r in rsi if a <= d <= b) - 1
    print(f"    helften 1995–2010 {h(date(1995,1,1), date(2010,12,31))*100:+.1f}% / 2011–2026 {h(date(2011,1,1), date(2026,9,21))*100:+.1f}%")

    # (b) RSI(2) gepoold (B2b) + ORB gepoold (B4a), overlap
    rsi_pool = {}
    for r in csv.DictReader(open("results/b2/B2_b_daily.csv"), delimiter=";"):
        rsi_pool[datetime.strptime(r["date"], "%Y.%m.%d").date()] = float(r["end_equity"]) / float(r["start_equity"]) - 1
    orb = defaultdict(float)
    for r in csv.DictReader(open("results/b4/B4_a_ORB_trades.csv"), delimiter=";"):
        orb[datetime.strptime(r["date"], "%Y-%m-%d").date()] += float(r["net_frac"]) / 7
    lo, hi = max(min(orb), date(2021, 9, 14)), max(orb)
    days = sorted(d for d in set(rsi_pool) | set(orb) if lo <= d <= hi)
    a = [rsi_pool.get(d, 0.0) for d in days]
    b = [orb.get(d, 0.0) for d in days]
    print(f"\n(b) overlap {lo}..{hi}, {len(days)} dagen | correlatie RSI(2)↔ORB {statistics.correlation(a, b):+.2f}")
    va, vb = statistics.stdev(a), statistics.stdev(b)
    wa, wb = (1 / va) / (1 / va + 1 / vb), (1 / vb) / (1 / va + 1 / vb)
    comb = [(d, wa * x + wb * y) for d, x, y in zip(days, a, b)]
    print(f"    gewichten (1/vol): RSI(2) {wa:.2f}, ORB {wb:.2f}")
    describe("    RSI(2) alleen (overlap)", list(zip(days, a)), max_scale(a))
    describe("    ORB alleen (overlap)", list(zip(days, b)), max_scale(b))
    kc = max_scale([r for _, r in comb])
    describe("    COMBINATIE", comb, kc)
    need = st.required_sharpe(880)[0]
    print(f"    benodigde Sharpe voor €880/mnd: {need:.2f}")


if __name__ == "__main__":
    main()
