"""C6: vol-timing van index-exposure vs b&h op gelijke vol, exact volgens PREREG_C6.md."""
import bisect
import csv
import math
import statistics
from datetime import date, datetime

import stats_tools as st

IDX = {"SPX": date(1990, 1, 1), "NDX": date(1990, 1, 1), "DAX": date(1994, 1, 1)}
TGT, CAP, SPREAD, MARKUP = 0.08, 1.5, 0.0002, 0.02


def rf_fn():
    ks, vs = [], []
    for r in csv.DictReader(open("data/fred/DTB3.csv")):
        if r["DTB3"] not in (".", ""):
            ks.append(datetime.strptime(r["observation_date"], "%Y-%m-%d").date()); vs.append(float(r["DTB3"]) / 100)
    return lambda d: vs[max(0, bisect.bisect_right(ks, d) - 1)]


RF = rf_fn()


def load(n):
    rows = [(datetime.strptime(r["date"], "%Y.%m.%d").date(), float(r["close"]))
            for r in csv.DictReader(open(f"data/ohlc/{n}.csv"), delimiter=";")]
    return [x[0] for x in rows], [x[1] for x in rows]


def simulate(d, c, start, weight_fn):
    w = 0.0
    out = []
    last_m = None
    for i in range(1, len(d)):
        if d[i] < start:
            continue
        r = w * (c[i] / c[i - 1] - 1) - abs(w) * (RF(d[i - 1]) + MARKUP) * (d[i] - d[i - 1]).days / 365
        if (d[i].year, d[i].month) != last_m:
            last_m = (d[i].year, d[i].month)
            nw = weight_fn(i)
            r -= abs(nw - w) * SPREAD
            w = nw
        out.append((d[i], r))
    return out


def stats(daily):
    rets = [r for _, r in daily]
    eq, peak, mdd = 1.0, 1.0, 0.0
    for r in rets:
        eq *= 1 + r; peak = max(peak, eq); mdd = max(mdd, 1 - eq / peak)
    yrs = len(rets) / 252
    return {"cagr": eq ** (1 / yrs) - 1, "vol": statistics.stdev(rets) * math.sqrt(252), "sr": st.sharpe(rets)[0],
            "dd": mdd, "rets": rets}


def main():
    combo_vt, combo_bh = [], []
    for n, start in IDX.items():
        d, c = load(n)
        i0 = next(i for i, x in enumerate(d) if x >= start)
        full_vol = statistics.stdev([c[i] / c[i - 1] - 1 for i in range(i0 + 1, len(d))]) * math.sqrt(252)
        k_bh = TGT / full_vol

        def vt(i):
            rs = [c[j] / c[j - 1] - 1 for j in range(i - 21, i)]  # t/m vorige slot
            s = statistics.stdev(rs) * math.sqrt(252)
            return min(CAP, TGT / s) if s > 0 else 0.0

        a = simulate(d, c, start, vt)
        b = simulate(d, c, start, lambda i: k_bh)
        sa, sb = stats(a), stats(b)
        ok = sa["sr"] - sb["sr"] >= 0.15 and sa["dd"] < 0.15
        print(f"{n}: vol-getimed CAGR {sa['cagr']*100:+.2f}% vol {sa['vol']*100:.1f}% SR {sa['sr']:.2f} DD {sa['dd']*100:.1f}% | "
              f"b&h@8% (w={k_bh:.2f}) CAGR {sb['cagr']*100:+.2f}% vol {sb['vol']*100:.1f}% SR {sb['sr']:.2f} DD {sb['dd']*100:.1f}% | "
              f"ΔSR {sa['sr']-sb['sr']:+.2f} → {'GESLAAGD' if ok else 'afgewezen'}")
        for lo, hi in ((date(1990, 1, 1), date(2007, 12, 31)), (date(2008, 1, 1), date(2026, 9, 21))):
            xa = [r for x, r in a if lo <= x <= hi]; xb = [r for x, r in b if lo <= x <= hi]
            print(f"    {lo.year}–{hi.year}: SR getimed {st.sharpe(xa)[0]:.2f} vs b&h {st.sharpe(xb)[0]:.2f}")
        combo_vt.append(dict(a)); combo_bh.append(dict(b))
    days = sorted(set.intersection(*[set(x) for x in combo_vt]))
    cv = [statistics.mean(x[t] for x in combo_vt) for t in days]
    cb = [statistics.mean(x[t] for x in combo_bh) for t in days]
    print(f"Combinatie 3 indices (informatief, {days[0]}..): SR getimed {st.sharpe(cv)[0]:.2f} vs b&h {st.sharpe(cb)[0]:.2f}; "
          f"DSR344 getimed {st.deflated_sharpe(cv, 344)[0]:.2f}")


if __name__ == "__main__":
    main()
