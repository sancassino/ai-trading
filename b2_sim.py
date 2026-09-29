"""B2: dagfrequente edges (IBS, RSI(2), intraday/overnight, turn-of-month), exact volgens PREREG_B2.md.
Gebruik: python3 b2_sim.py  -> samenvatting + results/b2/B2_<strat>_daily.csv (gepoold)"""
import csv
import math
import os
import statistics
from datetime import date, datetime

import stats_tools as st

SPREAD = 0.0002
MARKUP = 0.02
START, END = date(1990, 1, 1), date(2026, 9, 21)
H1 = (date(1995, 1, 1), date(2010, 12, 31))
H2 = (date(2011, 1, 1), date(2026, 9, 21))
UNIV = {  # strategie -> {naam: (bestand, startdatum)}
    "abd": {"SPX": ("SPX", START), "NDX": ("NDX", START), "DAX": ("DAX", date(1994, 1, 1)),
            "FTSE": ("FTSE", START), "N225": ("N225", START), "GLD": ("GLD", date(2004, 11, 18))},
    "c": {"SPY": ("SPY", date(1993, 2, 1)), "QQQ": ("QQQ", date(1999, 3, 10)), "DAX": ("DAX", date(1994, 1, 1)),
          "N225": ("N225", START), "GLD": ("GLD", date(2004, 11, 18))},
}


def load(name):
    rows = []
    for r in csv.DictReader(open(f"data/ohlc/{name}.csv"), delimiter=";"):
        rows.append((datetime.strptime(r["date"], "%Y.%m.%d").date(), float(r["open"]), float(r["high"]),
                     float(r["low"]), float(r["close"])))
    return rows


def dtb3():
    out = {}
    for r in csv.DictReader(open("data/fred/DTB3.csv")):
        if r["DTB3"] not in (".", ""):
            out[datetime.strptime(r["observation_date"], "%Y-%m-%d").date()] = float(r["DTB3"]) / 100
    ks = sorted(out)
    return ks, out


RK, RV = dtb3()


def rate(d):
    import bisect
    i = bisect.bisect_right(RK, d) - 1
    return RV[RK[i]] if i >= 0 else 0.0


def rsi2(closes):
    out = [None] * len(closes)
    ag = al = None
    for i in range(1, len(closes)):
        ch = closes[i] - closes[i - 1]
        g, l = max(ch, 0), max(-ch, 0)
        if i == 2 or ag is None:
            ag, al = g, l
        else:
            ag = (ag * 1 + g) / 2
            al = (al * 1 + l) / 2
        out[i] = 100.0 if al == 0 else 100 - 100 / (1 + ag / al)
    return out


def sleeve(strat, rows, start):
    """dagrendementen (datum -> r) van één instrument op 100% notional, en aantal trades"""
    d = [x[0] for x in rows]
    o = [x[1] for x in rows]
    h = [x[2] for x in rows]
    l = [x[3] for x in rows]
    c = [x[4] for x in rows]
    n = len(rows)
    ret = {}
    trades = 0
    rs = rsi2(c) if strat == "b" else None
    sma = [None] * n
    if strat == "b":
        s = 0.0
        for i in range(n):
            s += c[i]
            if i >= 200:
                s -= c[i - 200]
            if i >= 199:
                sma[i] = s / 200
    # turn-of-month: dagen met positie = laatste handelsdag + eerste 3 van de maand
    tom_hold = set()
    if strat == "d":
        for i in range(n - 1):
            if d[i + 1].month != d[i].month:  # i = laatste handelsdag van de maand
                for j in range(i, min(i + 4, n)):
                    tom_hold.add(j)
    inpos = False
    held = 0
    for i in range(1, n):
        if d[i] > END:
            break
        active = d[i] >= start
        nights = (d[i] - d[i - 1]).days
        fin = (rate(d[i - 1]) + MARKUP) / 365 * nights
        r = 0.0
        if strat in ("a", "b", "d"):
            if inpos:
                r += c[i] / c[i - 1] - 1 - fin
                held += 1
            # beslissing op slot i
            if strat == "a":
                if inpos and (c[i] > h[i - 1] or held >= 5):
                    inpos = False; r -= SPREAD
                elif not inpos and active and h[i] > l[i] and (c[i] - l[i]) / (h[i] - l[i]) < 0.2:
                    inpos = True; held = 0; r -= SPREAD; trades += 1
            elif strat == "b":
                if inpos and rs[i] is not None and rs[i] > 70:
                    inpos = False; r -= SPREAD
                elif not inpos and active and rs[i] is not None and sma[i] and rs[i] < 10 and c[i] > sma[i]:
                    inpos = True; held = 0; r -= SPREAD; trades += 1
            else:  # d: positie gehouden over dag j als j in tom_hold -> op slot i beslissen voor dag i+1
                want = (i + 1) in tom_hold
                if inpos and not want:
                    inpos = False; r -= SPREAD
                elif not inpos and want and active:
                    inpos = True; r -= SPREAD; trades += 1
        elif strat == "c1":
            if active:
                r = c[i] / o[i] - 1 - 2 * SPREAD; trades += 1
        elif strat == "c2":
            if active and d[i - 1] >= start:
                r = o[i] / c[i - 1] - 1 - 2 * SPREAD - fin; trades += 1
        if active:
            ret[d[i]] = r
    return ret, trades


def main():
    os.makedirs("results/b2", exist_ok=True)
    data = {}
    print(f"{'strat':<5}{'jr':>5}{'trades':>8}{'CAGR':>8}{'vol':>6}{'SR':>6}{'t':>6}{'H1':>8}{'H2':>8}{'maxDD':>7}"
          f"{'DSR305':>7}{'DSR35':>6}  oordeel")
    for strat in ("a", "b", "c1", "c2", "d"):
        u = UNIV["c" if strat.startswith("c") else "abd"]
        sleeves = {}
        tot_trades = 0
        per_inst = {}
        for name, (fn, start) in u.items():
            if fn not in data:
                data[fn] = load(fn)
            r, t = sleeve(strat, data[fn], start)
            sleeves[name] = (r, start)
            tot_trades += t
            per_inst[name] = (r, t)
        dates = sorted({x for r, _ in sleeves.values() for x in r if x >= START})
        pooled = []
        for x in dates:
            av = [r.get(x, 0.0) for r, s in sleeves.values() if x >= s]
            pooled.append((x, sum(av) / len(av) if av else 0.0))
        eq, peak, mdd = 1.0, 1.0, 0.0
        yearly = {}
        path = f"results/b2/B2_{strat}_daily.csv"
        with open(path, "w") as f:
            f.write("date;start_balance;start_equity;min_equity;end_equity\n")
            for x, r in pooled:
                prev = eq
                eq *= 1 + r
                peak = max(peak, eq); mdd = max(mdd, 1 - eq / peak)
                yearly.setdefault(x.year, [prev, eq])[1] = eq
                f.write(f"{x.strftime('%Y.%m.%d')};{prev*1e5:.2f};{prev*1e5:.2f};{min(prev, eq)*1e5:.2f};{eq*1e5:.2f}\n")
        rets = [r for _, r in pooled]
        yrs = len(rets) / 252

        def half(a, b):
            return math.prod(1 + r for x, r in pooled if a <= x <= b) - 1

        h1, h2 = half(*H1), half(*H2)
        sr = st.sharpe(rets)[0]
        t = st.t_stat(rets)
        dsr305, _ = st.deflated_sharpe(rets, 305)
        dsr35, _ = st.deflated_sharpe(rets, 35)
        ok = t >= 3 and h1 > 0 and h2 > 0 and tot_trades >= 300 and mdd < 0.15
        print(f"{strat:<5}{yrs:>5.1f}{tot_trades:>8}{(eq**(1/yrs)-1)*100:>7.2f}%{statistics.stdev(rets)*math.sqrt(252)*100:>5.1f}%"
              f"{sr:>6.2f}{t:>6.2f}{h1*100:>7.1f}%{h2*100:>7.1f}%{mdd*100:>6.1f}%{dsr305:>7.2f}{dsr35:>6.2f}  "
              f"{'GESLAAGD' if ok else 'afgewezen'}")
        print("      per jaar: " + " ".join(f"{str(y)[2:]}:{(v[1]/v[0]-1)*100:+.1f}" for y, v in sorted(yearly.items())))
        print("      per instrument (100% notional, t-stat / CAGR / trades): " + " ".join(
            f"{n}:{st.t_stat(list(r.values())):+.1f}/{(math.prod(1 + v for v in r.values())**(252/max(len(r),1))-1)*100:+.1f}%/{tr}"
            for n, (r, tr) in per_inst.items()))


if __name__ == "__main__":
    main()
