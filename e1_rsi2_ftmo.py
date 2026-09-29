"""E1: RSI(2) (regel B2b ongewijzigd) op FTMO-dagslotkoersen met FTMO-kosten; vergelijking met de Yahoo-versie.
Zie VOORSTEL_E.md. Gebruik: python3 e1_rsi2_ftmo.py"""
import csv
import math
import statistics
from collections import defaultdict
from datetime import date, datetime

import stats_tools as st
from b2_sim import UNIV, load as load_ohlc, rsi2, sleeve

SWAP_LONG = {"US500cash": 0.0495, "US100cash": 0.0712, "US30cash": 0.0833, "GER40cash": 0.0652,
             "UK100cash": 0.0828, "XAUUSD": 0.0793}
YAHOO_MAP = {"US500cash": "SPX", "US100cash": "NDX", "GER40cash": "DAX", "UK100cash": "FTSE", "XAUUSD": "GLD"}
LO, HI = date(2021, 1, 1), date(2026, 9, 21)


def ftmo_close(sym):
    rows = [(datetime.strptime(r["date"], "%Y.%m.%d").date(), float(r["close"]))
            for r in csv.DictReader(open(f"{sym}_rates.csv"), delimiter=";")]
    return sorted(rows)


def eod_spread_frac(sym):
    """mediaan (spread/prijs) van de laatste M5-bar van elke serverdag"""
    last = {}
    pt = None
    for line in open(f"data/m5/{sym}.csv"):
        if line.startswith("#"):
            pt = float(line.split("point=")[1].split(";")[0]); continue
        if not line[0].isdigit():
            continue
        p = line.rstrip().split(";")
        last[p[0][:10]] = int(p[5]) * pt / float(p[4])
    v = sorted(last.values())
    return v[len(v) // 2]


def ftmo_sleeve(sym):
    rows = ftmo_close(sym)
    d = [x[0] for x in rows]; c = [x[1] for x in rows]
    rs = rsi2(c)
    sma = [statistics.mean(c[i - 199:i + 1]) if i >= 199 else None for i in range(len(c))]
    spread = eod_spread_frac(sym)
    ret, inpos, trades = {}, False, 0
    for i in range(1, len(c)):
        r = 0.0
        if inpos:
            r += c[i] / c[i - 1] - 1 - SWAP_LONG[sym] * (d[i] - d[i - 1]).days / 365
        if inpos and rs[i] is not None and rs[i] > 70:
            inpos = False; r -= spread
        elif not inpos and rs[i] is not None and sma[i] and rs[i] < 10 and c[i] > sma[i]:
            inpos = True; r -= spread
            if LO <= d[i] <= HI:
                trades += 1
        if LO <= d[i] <= HI:
            ret[d[i]] = r
    return ret, trades, spread


def pooled(sleeves):
    days = sorted({x for s in sleeves for x in s})
    return [(x, statistics.mean(s.get(x, 0.0) for s in sleeves)) for x in days]


def monthly(daily):
    m = defaultdict(lambda: 1.0)
    for d, r in daily:
        m[(d.year, d.month)] *= 1 + r
    return {k: v - 1 for k, v in m.items()}


def main():
    ft = {}
    print("FTMO-sleeves (2021–2026):")
    for sym in SWAP_LONG:
        r, n, sp = ftmo_sleeve(sym)
        ft[sym] = r
        x = list(r.values())
        print(f"  {sym:<10} trades {n:>3} | spread {sp*100:.4f}% | CAGR {(math.prod(1+v for v in x)**(252/len(x))-1)*100:+.2f}% | t {st.t_stat(x):+.2f}")
    fp = pooled(list(ft.values()))
    yh = {}
    for sym, y in YAHOO_MAP.items():
        fn, start = UNIV["abd"][y]
        s = sleeve("b", load_ohlc(fn), start)[0]
        yh[sym] = {k: v for k, v in s.items() if LO <= k <= HI}
    yp = pooled(list(yh.values()))
    fp5 = pooled([ft[s] for s in YAHOO_MAP])
    for label, dly in (("FTMO gepoold (6)", fp), ("FTMO gepoold (5, zelfde als Yahoo)", fp5), ("Yahoo gepoold (5)", yp)):
        x = [r for _, r in dly]
        h1 = math.prod(1 + r for d, r in dly if d <= date(2023, 12, 31)) - 1
        h2 = math.prod(1 + r for d, r in dly if d > date(2023, 12, 31)) - 1
        print(f"{label:<36} SR {st.sharpe(x)[0]:+.2f} t {st.t_stat(x):+.2f} | 2021–23 {h1*100:+.1f}% | 2024–26 {h2*100:+.1f}% | totaal {(math.prod(1+r for r in x)-1)*100:+.1f}%")
    mf, my = monthly(fp5), monthly(yp)
    ks = sorted(set(mf) & set(my))
    corr = statistics.correlation([mf[k] for k in ks], [my[k] for k in ks])
    h1 = math.prod(1 + r for d, r in fp if d <= date(2023, 12, 31)) - 1
    h2 = math.prod(1 + r for d, r in fp if d > date(2023, 12, 31)) - 1
    ok = h1 > 0 and h2 > 0 and corr >= 0.7
    print(f"maandcorrelatie FTMO(5) ↔ Yahoo(5): {corr:.2f} | beslisregel E1 (FTMO(6) beide helften > 0, corr ≥ 0,7): {'GESLAAGD' if ok else 'AFGEWEZEN'}")


if __name__ == "__main__":
    main()
