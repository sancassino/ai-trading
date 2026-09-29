"""D4: risicopariteit op FTMO-verhandelbare klassen (SPY, EFA, GLD, USO), exact volgens PREREG_D4.md."""
import bisect
import csv
import math
import statistics
from datetime import date, datetime

import stats_tools as st
from momentum_sim import load_series

START, END = date(2001, 1, 1), date(2026, 9, 21)
TGT, CAP, SPREAD, MARKUP = 0.08, 3.0, 0.0002, 0.02


def rf_fn():
    ks, vs = [], []
    for r in csv.DictReader(open("data/fred/DTB3.csv")):
        if r["DTB3"] not in (".", ""):
            ks.append(datetime.strptime(r["observation_date"], "%Y-%m-%d").date()); vs.append(float(r["DTB3"]) / 100)
    return lambda d: vs[max(0, bisect.bisect_right(ks, d) - 1)]


def main():
    rf = rf_fn()
    names = ["SPY", "EFA", "GLD", "USO"]
    ser = {n: dict(load_series(n, "yahoo")) for n in names}
    cal = [d for d in sorted(ser["SPY"]) if d <= END]
    px = {}
    for n in names:
        col, last = [], None
        for d in cal:
            last = ser[n].get(d, last)
            col.append(last)
        px[n] = col

    def rets(n, i, k):
        return [px[n][j] / px[n][j - 1] - 1 for j in range(i - k, i) if px[n][j - 1] and px[n][j]]

    def run(weight_fn):
        w = {n: 0.0 for n in names}
        out, last_m = [], None
        for i in range(61, len(cal)):
            d = cal[i]
            if d < START:
                continue
            dt = (d - cal[i - 1]).days / 365
            r = 0.0
            for n, x in w.items():
                if x and px[n][i - 1]:
                    r += x * (px[n][i] / px[n][i - 1] - 1) - abs(x) * (rf(cal[i - 1]) + MARKUP) * dt
            if (d.year, d.month) != last_m:
                last_m = (d.year, d.month)
                nw = weight_fn(i)
                r -= sum(abs(nw[n] - w[n]) for n in names) * SPREAD
                w = nw
            out.append((d, r))
        return out

    def rp(i):
        act = [n for n in names if px[n][i - 61] is not None]
        inv = {}
        for n in act:
            rs = rets(n, i, 60)
            if len(rs) > 20:
                inv[n] = 1 / (statistics.stdev(rs) * math.sqrt(252))
        tot = sum(inv.values())
        raw = {n: inv.get(n, 0.0) / tot if tot else 0.0 for n in names}
        port = [sum(raw[n] * (px[n][j] / px[n][j - 1] - 1) for n in names if raw[n] and px[n][j - 1]) for j in range(i - 60, i)]
        sp = statistics.stdev(port) * math.sqrt(252)
        k = min(TGT / sp, CAP) if sp > 0 else 0.0
        return {n: raw[n] * k for n in names}

    a = run(rp)
    spy_full = statistics.stdev([px["SPY"][j] / px["SPY"][j - 1] - 1 for j in range(1, len(cal)) if cal[j] >= START]) * math.sqrt(252)
    b = run(lambda i: {"SPY": TGT / spy_full, "EFA": 0.0, "GLD": 0.0, "USO": 0.0})
    for label, dly in (("Risicopariteit SPY/EFA/GLD/USO @8%", a), ("Referentie SPY b&h @8% vol", b)):
        rr = [x for _, x in dly]
        eq, peak, mdd, yr = 1.0, 1.0, 0.0, {}
        for d, x in dly:
            prev = eq; eq *= 1 + x; peak = max(peak, eq); mdd = max(mdd, 1 - eq / peak)
            yr.setdefault(d.year, [prev, eq])[1] = eq
        h = [math.prod(1 + x for d, x in dly if lo <= d <= hi) - 1 for lo, hi in ((date(2001, 1, 1), date(2013, 12, 31)), (date(2014, 1, 1), END))]
        sr, dsr = st.sharpe(rr)[0], st.deflated_sharpe(rr, 348)[0]
        yrs = len(rr) / 252
        ok = sr >= 0.7 and mdd < 0.15 and all(x > 0 for x in h) and dsr >= 0.5
        print(f"{label}: CAGR {(eq**(1/yrs)-1)*100:+.2f}% vol {statistics.stdev(rr)*math.sqrt(252)*100:.1f}% SR {sr:.2f} t {st.t_stat(rr):.2f} "
              f"DD {mdd*100:.1f}% helften {h[0]*100:+.1f}% / {h[1]*100:+.1f}% jaren+ {sum(v[1] > v[0] for v in yr.values())}/{len(yr)} "
              f"DSR348 {dsr:.2f}" + (f" → {'GESLAAGD' if ok else 'afgewezen'}" if label.startswith("Risico") else ""))
        print("    per jaar: " + " ".join(f"{str(y)[2:]}:{(v[1]/v[0]-1)*100:+.1f}" for y, v in sorted(yr.items())))


if __name__ == "__main__":
    main()
