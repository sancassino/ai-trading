"""D2: goud vs reële rente (DFII10), exact volgens PREREG_D2.md. Gebruik: python3 d2_gold_realrate.py [--rf]"""
import bisect, csv, math, sys
from datetime import date, datetime
import stats_tools as st

def fred(i):
    out = []
    for r in csv.DictReader(open(f"data/fred/{i}.csv")):
        if r[i] not in (".", ""):
            out.append((datetime.strptime(r["observation_date"], "%Y-%m-%d").date(), float(r[i])))
    return out

rr = fred("DFII10"); rk = [d for d, _ in rr]
rf = fred("DTB3"); fk = [d for d, _ in rf]
gld = [(datetime.strptime(r["date"], "%Y.%m.%d").date(), float(r["close"])) for r in csv.DictReader(open("data/yahoo/GLD.csv"), delimiter=";")]
use_rf = "--rf" in sys.argv
w, last_m, daily = 0.0, None, []
for i in range(1, len(gld)):
    d, p = gld[i]; dp, pp = gld[i - 1]
    r = w * (p / pp - 1)
    nights = (d - dp).days
    if w:
        if use_rf:
            f = rf[max(0, bisect.bisect_right(fk, dp) - 1)][1] / 100
            r += (-w * f - abs(w) * 0.02) * nights / 365
        else:
            r -= (0.0793 if w > 0 else 0.0037) * abs(w) * nights / 365
    if (d.year, d.month) != last_m:
        last_m = (d.year, d.month)
        j = bisect.bisect_left(rk, d) - 2  # t-2
        nw = 0.0
        if j - 20 >= 0:
            delta = rr[j][1] - rr[j - 20][1]
            nw = 1.0 if delta < 0 else (-1.0 if delta > 0 else 0.0)
        r -= abs(nw - w) * 0.0002
        w = nw
    daily.append((d, r))
rets = [x for _, x in daily]
eq, peak, mdd, yr = 1.0, 1.0, 0.0, {}
for d, x in daily:
    prev = eq; eq *= 1 + x; peak = max(peak, eq); mdd = max(mdd, 1 - eq / peak)
    yr.setdefault(d.year, [prev, eq])[1] = eq
h = [math.prod(1 + x for d, x in daily if a <= d <= b) - 1 for a, b in ((date(2005, 1, 1), date(2015, 12, 31)), (date(2016, 1, 1), date(2026, 9, 21)))]
sr, t, dsr = st.sharpe(rets)[0], st.t_stat(rets), st.deflated_sharpe(rets, 347)[0]
ok = sr >= 0.7 and t >= 3 and all(x > 0 for x in h) and dsr >= 0.5
yrs = len(rets) / 252
print(f"D2 goud vs reële rente [{'diag DTB3±2%' if use_rf else 'FTMO-swap'}] CAGR {(eq**(1/yrs)-1)*100:+.2f}% SR {sr:.2f} t {t:.2f} DD {mdd*100:.1f}% "
      f"helften {h[0]*100:+.1f}% / {h[1]*100:+.1f}% jaren+ {sum(v[1]>v[0] for v in yr.values())}/{len(yr)} DSR347 {dsr:.2f} → {'GESLAAGD' if ok else 'afgewezen'}")
print("    per jaar: " + " ".join(f"{str(y)[2:]}:{(v[1]/v[0]-1)*100:+.1f}" for y, v in sorted(yr.items())))
