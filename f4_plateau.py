"""F4: plateau- en decay-check voor RSI(2) en ORB, exact volgens PREREG_F4.md."""
import math
import statistics
from collections import defaultdict
from datetime import date, datetime, timedelta

import stats_tools as st
from b2_sim import END, MARKUP, SPREAD, START, UNIV, load, rate, rsi2
from b4_sim import SYMS, cost_frac, sessions


def rsi_sleeve(rows, start, entry, sma_n):
    d = [x[0] for x in rows]; c = [x[4] for x in rows]
    rs = rsi2(c)
    sma, s = [None] * len(c), 0.0
    for i in range(len(c)):
        s += c[i]
        if i >= sma_n:
            s -= c[i - sma_n]
        if i >= sma_n - 1:
            sma[i] = s / sma_n
    ret, inpos = {}, False
    for i in range(1, len(c)):
        if d[i] > END:
            break
        r = 0.0
        if inpos:
            r += c[i] / c[i - 1] - 1 - (rate(d[i - 1]) + MARKUP) / 365 * (d[i] - d[i - 1]).days
        if inpos and rs[i] is not None and rs[i] > 70:
            inpos = False; r -= SPREAD
        elif not inpos and d[i] >= start and rs[i] is not None and sma[i] and rs[i] < entry and c[i] > sma[i]:
            inpos = True; r -= SPREAD
        if d[i] >= start:
            ret[d[i]] = r
    return ret


def pooled(sleeves):
    days = sorted({x for r, _ in sleeves for x in r if x >= START})
    return [(x, statistics.mean(r.get(x, 0.0) for r, s in sleeves if x >= s)) for x in days]


def part_a(data):
    print("(a) Decay RSI(2) per index — rollende 5-jaars-Sharpe (eind jaar) en 1990–2009 vs 2010–2026")
    for name, (fn, start) in UNIV["abd"].items():
        r = rsi_sleeve(data[fn], start, 10, 200)
        items = sorted(r.items())
        roll = []
        for y in range(max(start.year, 1990) + 5, 2027):
            x = [v for d, v in items if y - 5 < d.year <= y]
            roll.append(f"{str(y)[2:]}:{st.sharpe(x)[0]:+.1f}")
        early = [v for d, v in items if d.year < 2010]; late = [v for d, v in items if d.year >= 2010]
        print(f"  {name:<5} SR <2010 {st.sharpe(early)[0]:+.2f} | ≥2010 {st.sharpe(late)[0]:+.2f} | rollend: {' '.join(roll)}")


def part_b(data):
    print("\n(b) Plateaukaart RSI(2) gepoold (t-stat / CAGR), kandidaat = drempel 10 / SMA200")
    grid = {}
    for entry in (5, 10, 15):
        row = []
        for n in (150, 200, 250):
            p = pooled([(rsi_sleeve(data[fn], start, entry, n), start) for fn, start in UNIV["abd"].values()])
            x = [v for _, v in p]
            cagr = math.prod(1 + v for v in x) ** (252 / len(x)) - 1
            grid[(entry, n)] = st.t_stat(x)
            row.append(f"{st.t_stat(x):+5.2f} / {cagr*100:+.2f}%")
        print(f"  drempel {entry:>2}: " + " | ".join(f"SMA{n}: {v}" for n, v in zip((150, 200, 250), row)))
    return verdict("RSI(2)", grid, (10, 200))


def orb_trades(sess, comm, n_bars, exit_noon):
    trades = []
    for d, s in sess:
        if len(s) < n_bars + 2:
            continue
        hi = max(b[2] for b in s[:n_bars]); lo = min(b[3] for b in s[:n_bars])
        if hi <= lo:
            continue
        last = len(s) - 1
        if exit_noon:
            idx = [i for i, b in enumerate(s) if b[0].hour < 12]
            if not idx or idx[-1] < n_bars:
                continue
            last = idx[-1]
        for k in range(n_bars, last + 1):
            b = s[k]
            up, dn = b[2] > hi, b[3] < lo
            if not (up or dn):
                continue
            if up and dn:
                side, entry, exit_p, xb = 1, max(hi, b[1]), lo, b
            else:
                side = 1 if up else -1
                entry = max(hi, b[1]) if up else min(lo, b[1])
                stop = lo if up else hi
                if (up and b[3] <= stop) or (dn and b[2] >= stop):
                    exit_p, xb = stop, b
                else:
                    exit_p = None
                    for b2 in s[k + 1:last + 1]:
                        if side > 0 and b2[3] <= stop:
                            exit_p, xb = min(stop, b2[1]), b2; break
                        if side < 0 and b2[2] >= stop:
                            exit_p, xb = max(stop, b2[1]), b2; break
                    if exit_p is None:
                        xb = s[last]; exit_p = xb[4]
            trades.append(side * (exit_p - entry) / entry - cost_frac(side, b, xb, entry, comm))
            break
    return trades


def part_c():
    print("\n(c) Plateaukaart ORB (bp/trade / t), kandidaat = 30 min / sessie-einde")
    sess = {s: sessions(s) for s in SYMS}
    grid = {}
    per_sym = defaultdict(dict)
    for n_min in (15, 30, 60):
        cells = []
        for noon in (True, False):
            allt = []
            for s in SYMS:
                t = orb_trades(sess[s], SYMS[s][3], n_min // 5, noon)
                per_sym[s][(n_min, noon)] = statistics.mean(t) * 1e4 if t else float("nan")
                allt += t
            bp = statistics.mean(allt) * 1e4
            t = statistics.mean(allt) / statistics.stdev(allt) * math.sqrt(len(allt))
            grid[(n_min, noon)] = bp
            cells.append(f"{'12:00' if noon else 'einde'}: {bp:+.2f} bp / t {t:+.2f} (N {len(allt)})")
        print(f"  OR {n_min:>2} min: " + " | ".join(cells))
    print("  per symbool (bp/trade; volgorde 15/12:00, 15/einde, 30/12:00, 30/einde, 60/12:00, 60/einde):")
    for s, cells in per_sym.items():
        print(f"    {s:<10} " + " ".join(f"{cells[(m, n)]:+5.1f}" for m in (15, 30, 60) for n in (True, False)))
    return verdict("ORB", grid, (30, False))


def verdict(name, grid, cand):
    c = grid[cand]
    nb = [v for k, v in grid.items() if k != cand]
    same = sum(1 for v in nb if v * c > 0)
    strong = sum(1 for v in nb if v * c > 0 and abs(v) >= 0.5 * abs(c))
    ok = same >= 2 / 3 * len(nb) and strong >= 2 / 3 * len(nb)
    print(f"  → {name}: {same}/{len(nb)} buren zelfde teken, {strong}/{len(nb)} ook ≥ 50% van het niveau → {'PLATEAU' if ok else 'PIEK'}")
    return ok


def main():
    data = {fn: load(fn) for fn, _ in UNIV["abd"].values()}
    part_a(data)
    part_b(data)
    part_c()


if __name__ == "__main__":
    main()
