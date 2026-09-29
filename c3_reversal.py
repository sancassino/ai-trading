"""C3: kortetermijn-omkeer markt-neutraal, exact volgens PREREG_C3.md. Gebruik: python3 c3_reversal.py [--rfcost]"""
import argparse
import bisect
import csv
import math
from datetime import date, datetime

import stats_tools as st

YAHOO = {"ADSGn": "ADS.DE", "AIRF": "AF.PA", "ALVG": "ALV.DE", "BAYGn": "BAYN.DE", "DBKGn": "DBK.DE",
         "IBE": "IBE.MC", "LVMH": "MC.PA", "VOWG_p": "VOW3.DE", "BRK.B": "BRK-B"}
COST = 0.0005


def load(path):
    out = {}
    for r in csv.DictReader(open(path, encoding="utf-8-sig"), delimiter=";"):
        out[datetime.strptime(r["date"][:10], "%Y.%m.%d").date()] = float(r["close"])
    return out


def rf_fn():
    ks, vs = [], []
    for r in csv.DictReader(open("data/fred/DTB3.csv")):
        if r["DTB3"] not in (".", ""):
            ks.append(datetime.strptime(r["observation_date"], "%Y-%m-%d").date()); vs.append(float(r["DTB3"]) / 100)
    return lambda d: vs[max(0, bisect.bisect_right(ks, d) - 1)]


def run(series, start, end, rfcost):
    rf = rf_fn()
    cal = sorted({d for s in series.values() for d in s if start <= d <= end})
    # voorwaarts gevulde prijzen op de kalender; None vóór eerste notering
    px = {}
    for n, s in series.items():
        ks = sorted(s)
        col, j, last = [], 0, None
        for d in cal:
            while j < len(ks) and ks[j] <= d:
                last = s[ks[j]]; j += 1
            col.append(last)
        px[n] = col
    w = {}
    daily = []
    pending = None
    for t in range(1, len(cal)):
        d, dp = cal[t], cal[t - 1]
        r = 0.0
        nights = (d - dp).days
        for n, wt in w.items():
            a, b = px[n][t - 1], px[n][t]
            if a and b:
                r += wt * (b / a - 1)
            if rfcost:
                f = rf(dp)
                r += (-wt * f - abs(wt) * 0.02) * nights / 365
            else:
                r -= (abs(wt) * (0.084 if wt > 0 else 0.067)) * nights / 365
        if pending is not None:  # uitvoeren op slot t
            new = pending
            for n in set(w) | set(new):
                r -= abs(new.get(n, 0.0) - w.get(n, 0.0)) * COST
            w = new
            pending = None
        if t >= 5 and t % 5 == 0:  # vaste 5-dagen-cyclus, signaal op slot t
            rets = []
            for n in series:
                a, b = px[n][t - 5], px[n][t]
                if a and b:
                    rets.append((b / a - 1, n))
            rets.sort()
            q = max(1, len(rets) // 5)
            if len(rets) >= 10:
                pending = {n: 0.5 / q for _, n in rets[:q]}
                pending.update({n: -0.5 / q for _, n in rets[-q:]})
        daily.append((d, r))
    return daily


def report(label, daily, halves):
    rets = [r for _, r in daily]
    eq, peak, mdd = 1.0, 1.0, 0.0
    yr = {}
    for d, r in daily:
        prev = eq; eq *= 1 + r; peak = max(peak, eq); mdd = max(mdd, 1 - eq / peak)
        yr.setdefault(d.year, [prev, eq])[1] = eq
    yrs = len(rets) / 252
    h = [math.prod(1 + r for d, r in daily if a <= d <= b) - 1 for a, b in halves]
    sr, t = st.sharpe(rets)[0], st.t_stat(rets)
    dsr = st.deflated_sharpe(rets, 340)[0]
    ok = sr >= 0.7 and t >= 3 and all(x > 0 for x in h) and dsr >= 0.5
    print(f"{label:<34}{yrs:5.1f}jr CAGR {(eq**(1/yrs)-1)*100:+6.2f}% SR {sr:+.2f} t {t:+.2f} DD {mdd*100:5.1f}% "
          f"helften {h[0]*100:+.1f}% / {h[1]*100:+.1f}% DSR {dsr:.2f} → {'GESLAAGD' if ok else 'afgewezen'}")
    print("    per jaar: " + " ".join(f"{str(y)[2:]}:{(v[1]/v[0]-1)*100:+.1f}" for y, v in sorted(yr.items())))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rfcost", action="store_true", help="diagnostiek: financiering DTB3 ± 2% i.p.v. FTMO-swaps")
    a = ap.parse_args()
    pool = open("universe_stocks49.txt").read().split(",")
    tag = " [diag: DTB3±2%]" if a.rfcost else ""
    ftmo = {n: load(f"{n}_rates.csv") for n in pool}
    report("FTMO 49 aandelen 2021–26" + tag, run(ftmo, date(2021, 1, 1), date(2026, 9, 21), a.rfcost),
           [(date(2021, 1, 1), date(2023, 12, 31)), (date(2024, 1, 1), date(2026, 9, 21))])
    yh = {n: load(f"data/yahoo/{YAHOO.get(n, n)}.csv") for n in pool}
    report("Yahoo 49 aandelen 2000–26 (bovengrens)" + tag, run(yh, date(2000, 1, 1), date(2026, 9, 21), a.rfcost),
           [(date(2000, 1, 1), date(2012, 12, 31)), (date(2013, 1, 1), date(2026, 9, 21))])


if __name__ == "__main__":
    main()
