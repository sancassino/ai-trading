"""VOORSTEL_H / H1: maandeinde-herbalancering SPY vs TLT, exact volgens PREREG_H1.md."""
import bisect, csv, math, statistics
from collections import defaultdict
from datetime import datetime, date

def ser(path, fmt="%Y.%m.%d"):
    return sorted((datetime.strptime(r["date"][:10], fmt).date(), float(r["close"])) for r in csv.DictReader(open(path), delimiter=";"))
ks, vs = [], []
for r in csv.DictReader(open("data/fred/DTB3.csv")):
    if r["DTB3"] not in (".", ""): ks.append(datetime.strptime(r["observation_date"], "%Y-%m-%d").date()); vs.append(float(r["DTB3"]) / 100)
rf = lambda d: vs[max(0, bisect.bisect_right(ks, d) - 1)]

def run(px, tlt, fin, spread, start):
    d = [x[0] for x in px]; c = [x[1] for x in px]
    tl = dict(tlt); tk = sorted(tl)
    tat = lambda day: tl[tk[max(0, bisect.bisect_right(tk, day) - 1)]]
    months = defaultdict(list)
    for i, day in enumerate(d):
        if day >= start: months[(day.year, day.month)].append(i)
    trades = []
    for (y, m), idx in sorted(months.items()):
        if len(idx) < 6: continue
        first = idx[0] - 1
        if first < 0: continue
        sig_i, end_i = idx[-5], idx[-1]
        x = (c[sig_i] / c[first] - 1) - (tat(d[sig_i]) / tat(d[first]) - 1)
        side = -1 if x > 0 else 1
        gross = side * (c[end_i] / c[sig_i] - 1)
        nights = (d[end_i] - d[sig_i]).days
        trades.append((d[sig_i], gross - 2 * spread - fin(side, d[sig_i]) * nights / 365))
    return trades

def rep(label, tr, halves=None):
    x = [t[1] for t in tr]; tt = statistics.mean(x) / statistics.stdev(x) * math.sqrt(len(x))
    s = f"{label}: N {len(x)} | {statistics.mean(x)*1e4:+.1f} bp/trade | t {tt:+.2f} | positief {sum(v>0 for v in x)}/{len(x)}"
    hs = []
    if halves:
        for lo, hi in halves:
            v = [t[1] for t in tr if lo <= t[0] <= hi]; hs.append(statistics.mean(v))
            s += f" | {lo.year}–{hi.year} {statistics.mean(v)*1e4:+.1f} bp (t {statistics.mean(v)/statistics.stdev(v)*math.sqrt(len(v)):+.2f}, N {len(v)})"
    print(s); return tt, hs

spy = ser("data/yahoo/SPY.csv"); tlt = ser("data/yahoo/TLT.csv")
yfin = lambda side, day: (rf(day) + 0.02) if side > 0 else -(rf(day) - 0.02)
t, hs = rep("SPY 2002–2026", run(spy, tlt, yfin, 0.0002, date(2002, 8, 1)), [(date(2002, 8, 1), date(2013, 12, 31)), (date(2014, 1, 1), date(2026, 12, 31))])
us5 = ser("US500cash_rates.csv")
ffin = lambda side, day: 0.0495 if side > 0 else 0.0295
tf, _ = rep("FTMO US500 2021–2026", run(us5, tlt, ffin, 0.0001, date(2021, 1, 1)))
ftmo_tot = sum(x[1] for x in run(us5, tlt, ffin, 0.0001, date(2021, 1, 1)))
ok = t >= 3 and all(h > 0 for h in hs) and ftmo_tot > 0
print(f"Beslisregel: t {t:+.2f} (≥ 3), helften {'+' if all(h>0 for h in hs) else '−'}, FTMO totaal {ftmo_tot*1e4:+.0f} bp → {'GESLAAGD' if ok else 'AFGEWEZEN'}")
