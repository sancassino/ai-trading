"""C5: crypto-trend BTC+ETH, exact volgens PREREG_C5.md. Gebruik: python3 c5_crypto.py [--fin ftmo|none|rf]"""
import argparse
import bisect
import csv
import math
import statistics
from datetime import datetime

import stats_tools as st


def load(t):
    return {datetime.strptime(r["date"], "%Y.%m.%d").date(): float(r["close"])
            for r in csv.DictReader(open(f"data/yahoo/{t}.csv"), delimiter=";")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fin", default="ftmo", choices=["ftmo", "none", "rf"])
    a = ap.parse_args()
    ks, vs = [], []
    for r in csv.DictReader(open("data/fred/DTB3.csv")):
        if r["DTB3"] not in (".", ""):
            ks.append(datetime.strptime(r["observation_date"], "%Y-%m-%d").date()); vs.append(float(r["DTB3"]) / 100)
    rf = lambda d: vs[max(0, bisect.bisect_right(ks, d) - 1)]
    data = {"BTC": load("BTC-USD"), "ETH": load("ETH-USD")}
    cal = sorted(data["BTC"])
    px = {n: [data[n].get(d) for d in cal] for n in data}
    for n in px:  # voorwaarts vullen
        last = None
        for i, v in enumerate(px[n]):
            last = v if v else last
            px[n][i] = last if v or last else None
    w = {"BTC": 0.0, "ETH": 0.0}
    daily = []
    last_m = None
    for i in range(1, len(cal)):
        d, dp = cal[i], cal[i - 1]
        r = 0.0
        nights = (d - dp).days
        for n, wt in w.items():
            if wt and px[n][i - 1] and px[n][i]:
                r += wt * (px[n][i] / px[n][i - 1] - 1)
                if a.fin == "ftmo":
                    r -= abs(wt) * 0.30 * nights / 365
                elif a.fin == "rf":
                    r += (-wt * rf(dp) - abs(wt) * 0.02) * nights / 365
        if (d.year, d.month) != last_m:
            last_m = (d.year, d.month)
            new = {}
            for n in w:
                p = px[n]
                j = i - 1  # vorige slot
                if j < 452 or not p[j - 452]:
                    new[n] = 0.0
                    continue
                mom = p[j - 21] / p[j - 252] - 1
                s50 = statistics.mean(p[j - 49:j + 1]); s200 = statistics.mean(p[j - 199:j + 1])
                sig = 1 if mom > 0 and s50 > s200 else (-1 if mom < 0 and s50 < s200 else 0)
                rets = [p[k] / p[k - 1] - 1 for k in range(j - 59, j + 1)]
                vol = statistics.stdev(rets) * math.sqrt(365)
                new[n] = sig * min(1.0, 0.5 * 0.20 / vol) if vol > 0 else 0.0
            for n in w:
                r -= abs(new[n] - w[n]) * 0.0005
            w = new
        if any(v for v in w.values()) or daily:
            daily.append((d, r))
    rets = [x for _, x in daily]
    eq, peak, mdd = 1.0, 1.0, 0.0
    yr = {}
    for d, x in daily:
        prev = eq; eq *= 1 + x; peak = max(peak, eq); mdd = max(mdd, 1 - eq / peak)
        yr.setdefault(d.year, [prev, eq])[1] = eq
    yret = {y: v[1] / v[0] - 1 for y, v in yr.items()}
    best2 = sorted(yret, key=lambda y: -yret[y])[:2]
    ex = [x for d, x in daily if d.year not in best2]
    yrs = len(rets) / 365
    sr_ex = st.sharpe(ex, 365)[0]
    npos = sum(v > 0 for v in yret.values())
    ok = sr_ex >= 0.7 and mdd < 0.25 and npos >= 5
    print(f"C5 crypto-trend [financiering: {a.fin}] {daily[0][0]}..{daily[-1][0]} | CAGR {(eq**(1/yrs)-1)*100:+.2f}% | "
          f"vol {statistics.stdev(rets)*math.sqrt(365)*100:.1f}% | SR {st.sharpe(rets, 365)[0]:.2f} | t {st.t_stat(rets):.2f} | "
          f"DD {mdd*100:.1f}% | jaren+ {npos}/{len(yret)} | SR excl. beste 2 jaren ({best2}) {sr_ex:.2f} | "
          f"DSR341 {st.deflated_sharpe(rets, 341)[0]:.2f} | {'GESLAAGD' if ok else 'afgewezen'}")
    print("    per jaar: " + " ".join(f"{str(y)[2:]}:{v*100:+.1f}" for y, v in sorted(yret.items())))


if __name__ == "__main__":
    main()
