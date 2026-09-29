"""B3: dollar-neutrale long/short momentum, exact volgens PREREG_B3.md.
Gebruik: python3 b3_sim.py  -> per config + ensemble per universum; dagreeksen in results/b3/."""
import csv
import math
import os
import statistics
from datetime import date, timedelta

import stats_tools as st
from momentum_sim import Series, load_series

START, END = date(2000, 1, 1), date(2026, 9, 21)
VOL_TGT, LEV_CAP, SPREAD, MARKUP = 0.10, 4.0, 0.0005, 0.02


def load_pit():
    pit = {}
    for r in csv.DictReader((l for l in open("universe_pit_top10.csv") if not l.startswith("#")), delimiter=";"):
        pit[int(r["handelsjaar"])] = r["tickers"].split(",")
    return pit


def dtb3():
    rows = []
    for r in csv.DictReader(open("data/fred/DTB3.csv")):
        if r["DTB3"] not in (".", ""):
            y, m, d = map(int, r["observation_date"].split("-"))
            rows.append((date(y, m, d), float(r["DTB3"]) / 100))
    return Series(rows)


def run(universe_fn, syms, topn, lb, cal, px, rf):
    idx = {d: i for i, d in enumerate(cal)}
    w = {}
    units = {}
    equity = 1.0
    out = []
    last_month = None
    started = False
    for i, d in enumerate(cal):
        if d < START:
            continue
        # P&L gisteren -> vandaag (vanaf de 2e dag in de periode, ook zonder posities)
        if started:
            p0d = cal[i - 1]
            dt = (d - p0d).days / 365
            r0 = rf.at_or_before(p0d) or 0.0
            pnl = 0.0
            for s, u in units.items():
                a, b = px[s][i - 1], px[s][i]
                if a is None or b is None:
                    continue
                notional = u * a
                pnl += u * (b - a) - notional * r0 * dt - abs(notional) * MARKUP * dt
            prev = equity
            equity += pnl
            out.append((d, prev, equity))
        if (d.year, d.month) != last_month:
            last_month = (d.year, d.month)
            cutoff = d - timedelta(days=30 * lb)
            scored = []
            for s in universe_fn(d):
                sr = series_of[s]
                now, then = sr.before(d), sr.at_or_before(cutoff)
                if now and then and sr.first() <= cutoff and px[s][i] and i > 61:
                    scored.append(((now - then) / then, s))
            scored.sort(reverse=True)
            k = min(topn, len(scored) // 2)
            new_w = {}
            if k > 0:
                for _, s in scored[:k]:
                    new_w[s] = 1.0 / k
                for _, s in scored[-k:]:
                    new_w[s] = -1.0 / k
                # ex-ante vol met huidige gewichten over laatste 60 dagen
                port = []
                for j in range(i - 60, i):
                    v = 0.0
                    for s, wt in new_w.items():
                        a, b = px[s][j - 1], px[s][j]
                        if a and b:
                            v += wt * (b / a - 1)
                    port.append(v)
                sp = statistics.stdev(port) * math.sqrt(252)
                sc = VOL_TGT / sp if sp > 0 else 0.0
                g = sum(abs(x) for x in new_w.values()) * sc
                if g > LEV_CAP:
                    sc *= LEV_CAP / g
                new_w = {s: x * sc for s, x in new_w.items()}
            cost = 0.0
            new_units = {}
            for s in set(units) | set(new_w):
                p = px[s][i]
                old_n = units.get(s, 0.0) * p if p else 0.0
                new_n = new_w.get(s, 0.0) * equity
                cost += abs(new_n - old_n) * SPREAD
                if new_w.get(s) and p:
                    new_units[s] = new_n / p
            units = new_units
            equity -= cost
            if out:
                out[-1] = (out[-1][0], out[-1][1], equity)
        started = True
    return out


series_of = {}


def main():
    os.makedirs("results/b3", exist_ok=True)
    pit = load_pit()
    ua = open("universe_A_etf.txt").read().strip().split(",")
    ub = sorted({s for v in pit.values() for s in v})
    rf = dtb3()
    spy = Series(load_series("SPY", "yahoo"))
    cal = [d for d in spy.d if d <= END]
    for s in set(ua) | set(ub):
        series_of[s] = Series(load_series(s, "yahoo"))
    px = {s: [series_of[s].at_or_before(d) if series_of[s].first() <= d else None for d in cal] for s in series_of}
    spy_ret = {cal[i]: spy.p[spy.d.index(cal[i])] / spy.p[spy.d.index(cal[i - 1])] - 1 for i in range(1, len(cal)) if cal[i] >= START}
    universes = {"A": (lambda d: ua, ua), "B": (lambda d: pit.get(d.year, []), ub)}
    print(f"{'run':<10}{'CAGR':>8}{'vol':>6}{'SR':>6}{'t':>6}{'H1':>8}{'H2':>8}{'maxDD':>7}{'jaren+':>8}{'corrSPY':>8}{'DSR323':>7}{'DSR53':>6}")
    for u, (fn, syms) in universes.items():
        runs = []
        for k in (2, 3, 4):
            for lb in (1, 2, 3):
                res = run(fn, syms, k, lb, cal, px, rf)
                runs.append(res)
                summarize(f"{u}_t{k}_l{lb}", res, spy_ret)
        # ensemble: gemiddeld dagrendement
        dates = [x[0] for x in runs[0]]
        eq = 1.0
        ens = []
        for j, d in enumerate(dates):
            r = statistics.mean(rr[j][2] / rr[j][1] - 1 for rr in runs)
            prev = eq
            eq *= 1 + r
            ens.append((d, prev, eq))
        summarize(f"{u}_ENS", ens, spy_ret, write=True)


def summarize(name, res, spy_ret, write=False):
    rets = [e1 / e0 - 1 for _, e0, e1 in res]
    yrs = len(rets) / 252
    cagr = (res[-1][2] / res[0][1]) ** (1 / yrs) - 1
    peak, mdd = res[0][1], 0.0
    yr = {}
    for d, e0, e1 in res:
        peak = max(peak, e1); mdd = max(mdd, 1 - e1 / peak)
        yr.setdefault(d.year, [e0, e1])[1] = e1
    h = lambda a, b: math.prod(1 + (e1 / e0 - 1) for d, e0, e1 in res if a <= d <= b) - 1
    h1, h2 = h(date(2000, 1, 1), date(2012, 12, 31)), h(date(2013, 1, 1), END)
    sp = [spy_ret.get(d, 0.0) for d, _, _ in res]
    corr = statistics.correlation(rets, sp)
    npos = sum(v[1] > v[0] for v in yr.values())
    print(f"{name:<10}{cagr*100:>7.2f}%{statistics.stdev(rets)*math.sqrt(252)*100:>5.1f}%{st.sharpe(rets)[0]:>6.2f}"
          f"{st.t_stat(rets):>6.2f}{h1*100:>7.1f}%{h2*100:>7.1f}%{mdd*100:>6.1f}%{npos:>5}/{len(yr):<2}{corr:>8.2f}"
          f"{st.deflated_sharpe(rets, 323)[0]:>7.2f}{st.deflated_sharpe(rets, 53)[0]:>6.2f}")
    if write:
        print("      per jaar: " + " ".join(f"{str(y)[2:]}:{(v[1]/v[0]-1)*100:+.1f}" for y, v in sorted(yr.items())))
        with open(f"results/b3/B3_{name}_daily.csv", "w") as f:
            f.write("date;start_balance;start_equity;min_equity;end_equity\n")
            for d, e0, e1 in res:
                f.write(f"{d.strftime('%Y.%m.%d')};{e0*1e5:.2f};{e0*1e5:.2f};{min(e0, e1)*1e5:.2f};{e1*1e5:.2f}\n")


if __name__ == "__main__":
    main()
