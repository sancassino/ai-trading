"""VOORSTEL_H: H2 pre-feestdag en H3 RSI(2)-overnight bij VIX > 20, volgens PREREG_H2H3.md."""
import bisect, csv, math, statistics
from datetime import date, datetime, timedelta
import k1_nights as k1
from b2_sim import rsi2

def tstat(x): return statistics.mean(x) / statistics.stdev(x) * math.sqrt(len(x))

# ---- H2
spy = [(datetime.strptime(r["date"], "%Y.%m.%d").date(), float(r["close"])) for r in csv.DictReader(open("data/yahoo/SPY.csv"), delimiter=";")]
spy = [x for x in spy if x[0] >= date(1993, 1, 1)]
d = [x[0] for x in spy]; c = [x[1] for x in spy]
tr = []
for i in range(1, len(d) - 1):
    gap_days = [d[i] + timedelta(k) for k in range(1, (d[i + 1] - d[i]).days)]
    if any(g.weekday() < 5 for g in gap_days):          # weekdag zonder notering = feestdag
        nights = (d[i] - d[i - 1]).days
        tr.append((d[i], c[i] / c[i - 1] - 1 - 0.0004 - (k1.RF(d[i - 1]) + 0.02) * nights / 365))
x = [t[1] for t in tr]
h1 = [t[1] for t in tr if t[0].year <= 2009]; h2 = [t[1] for t in tr if t[0].year >= 2010]
ok = tstat(x) >= 3 and statistics.mean(h1) > 0 and statistics.mean(h2) > 0
print(f"H2 pre-feestdag SPY 1993–2026: N {len(x)} | {statistics.mean(x)*1e4:+.1f} bp | t {tstat(x):+.2f} | 1993–2009 {statistics.mean(h1)*1e4:+.1f} bp (t {tstat(h1):+.2f}) | "
      f"2010–2026 {statistics.mean(h2)*1e4:+.1f} bp (t {tstat(h2):+.2f}) → {'GESLAAGD' if ok else 'AFGEWEZEN'}")

# ---- H3
vix = {datetime.strptime(r["date"], "%Y.%m.%d").date(): float(r["close"]) for r in csv.DictReader(open("data/yahoo/VIX.csv"), delimiter=";")}
allx, fx = [], []
for name in ("SPY", "QQQ", "GLD", "DAX", "N225"):
    rows = k1.yahoo_rows(name)
    dd = [r[0] for r in rows]; o = [r[1] for r in rows]; cc = [r[2] for r in rows]
    rs = rsi2(cc)
    for i in range(200, len(cc) - 1):
        if rs[i] is not None and rs[i] < 10 and cc[i] > statistics.mean(cc[i - 199:i + 1]):
            net = o[i + 1] / cc[i] - 1 - 0.0004 - (k1.RF(dd[i]) + 0.02) * (dd[i + 1] - dd[i]).days / 365
            allx.append((dd[i], net, vix.get(dd[i])))
flt = [n for dd_, n, v in allx if v is not None and v > 20]
base = [n for dd_, n, v in allx if v is not None]
ok = tstat(flt) >= 3 and statistics.mean(flt) >= 1.5 * statistics.mean(base)
print(f"H3 RSI(2) max 1 nacht, Yahoo 1998–2026: alle (met VIX) N {len(base)}, {statistics.mean(base)*1e4:+.1f} bp, t {tstat(base):+.2f} | "
      f"VIX > 20: N {len(flt)}, {statistics.mean(flt)*1e4:+.1f} bp, t {tstat(flt):+.2f} | VIX ≤ 20: "
      f"{statistics.mean([n for _, n, v in allx if v is not None and v <= 20])*1e4:+.1f} bp → {'GESLAAGD' if ok else 'AFGEWEZEN'}")
