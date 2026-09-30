"""L3(a): pre-FOMC op Yahoo-dagproxy SPY 1994–2026, volgens PREREG_L3.md."""
import csv, math, statistics
from datetime import date, datetime
F = [date.fromisoformat(l.strip()) for l in open("fomc_dates_1994_2020.txt") if l[0].isdigit()]
F += [date.fromisoformat(r["date"]) for r in csv.DictReader((l for l in open("events.csv") if not l.startswith("#")), delimiter=";") if r["event"] == "FOMC"]
F = sorted(set(F))
rows = [(datetime.strptime(r["date"], "%Y.%m.%d").date(), float(r["open"]), float(r["close"])) for r in csv.DictReader(open("data/ohlc/SPY.csv"), delimiter=";")]
idx = {d: i for i, (d, _, _) in enumerate(rows)}
cc, oc, base_cc, base_oc = {}, {}, [], []
fset = set(F)
for i in range(1, len(rows)):
    d, o, c = rows[i]
    r_cc, r_oc = c / rows[i - 1][2] - 1, c / o - 1
    if d in fset: cc[d], oc[d] = r_cc, r_oc
    elif d.year >= 1994: base_cc.append(r_cc); base_oc.append(r_oc)
def rep(label, sub, base):
    x = list(sub.values())
    t = statistics.mean(x) / statistics.stdev(x) * math.sqrt(len(x))
    print(f"  {label:<28} N {len(x):>3} | {statistics.mean(x)*1e4:+6.1f} bp | t {t:+.2f} | baseline {statistics.mean(base)*1e4:+.1f} bp | positief {sum(v>0 for v in x)}/{len(x)}")
    return statistics.mean(x), t
print("L3(a) pre-FOMC, SPY-dagproxy:")
for name, dd, base in (("slot(d−1)→slot(FOMC)", cc, base_cc), ("open→slot (FOMC-dag)", oc, base_oc)):
    print(f" {name}:")
    m_all, t_all = rep("1994–2026", dd, base)
    for lo, hi in ((1994, 2011), (2012, 2026), (2010, 2020), (2021, 2026)):
        rep(f"{lo}–{hi}", {k: v for k, v in dd.items() if lo <= k.year <= hi}, base)
m1020 = statistics.mean([v for k, v in cc.items() if 2010 <= k.year <= 2020]); m2126 = statistics.mean([v for k, v in cc.items() if k.year >= 2021])
x = list(cc.values()); t = statistics.mean(x) / statistics.stdev(x) * math.sqrt(len(x))
ok = t >= 2.5 and len(x) >= 120 and m1020 >= 0.5 * m2126
print(f"Beslisregel (slot→slot): t {t:+.2f} (≥ 2,5), N {len(x)} (≥ 120), 2010–20 {m1020*1e4:+.1f} bp vs 50% van 2021–26 ({0.5*m2126*1e4:+.1f} bp) → {'GESLAAGD' if ok else 'AFGEWEZEN'}")
