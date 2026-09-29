"""C1: pairs/stat-arb, exact volgens PREREG_C1.md. Gebruik: python3 c1_pairs.py"""
import bisect
import csv
import math
import os
import statistics
from datetime import date, datetime

import stats_tools as st

ETF = [("SPY", "DIA", "US500/US30"), ("SPY", "QQQ", "US500/US100"), ("GLD", "SLV", "XAUUSD/XAGUSD"),
       ("EWG", "EWU", "GER40/UK100")]
FTMO = [("US500cash", "US30cash"), ("US500cash", "US100cash"), ("GER40cash", "EU50cash"), ("GER40cash", "FRA40cash"),
        ("UK100cash", "EU50cash"), ("XAUUSD", "XAGUSD"), ("UKOILcash", "USOILcash"), ("GER40cash", "UK100cash")]
COST = {"SLV": 0.0005, "XAGUSD": 0.0005, "UKOILcash": 0.0005, "USOILcash": 0.0005, "EU50cash": 0.0005, "FRA40cash": 0.0005}
LOOK, ENTRY, EXIT, STOP, MAXD = 60, 2.0, 0.5, 4.0, 20


def load(path, fmt="%Y.%m.%d"):
    out = {}
    for r in csv.DictReader(open(path, encoding="utf-8-sig"), delimiter=";"):
        out[datetime.strptime(r["date"][:10], fmt).date()] = float(r["close"])
    return out


def rf_series():
    ks, vs = [], []
    for r in csv.DictReader(open("data/fred/DTB3.csv")):
        if r["DTB3"] not in (".", ""):
            ks.append(datetime.strptime(r["observation_date"], "%Y-%m-%d").date()); vs.append(float(r["DTB3"]) / 100)
    return lambda d: vs[max(0, bisect.bisect_right(ks, d) - 1)]


RF = rf_series()


def ols(x, y):
    mx, my = statistics.mean(x), statistics.mean(y)
    sxx = sum((a - mx) ** 2 for a in x)
    b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sxx if sxx > 0 else 0.0
    return my - b * mx, b


def run(pa, pb, ca, cb, start):
    dates = sorted(set(pa) & set(pb))
    la = [math.log(pa[d]) for d in dates]
    lb = [math.log(pb[d]) for d in dates]
    daily = []  # (datum, rendement)
    trades = 0
    pos = 0          # +1 long spread (long a/short b), -1 short spread
    wa = wb = 0.0
    held = 0
    pending = None   # beslissing op t, uitvoering op t+1
    for t in range(LOOK + 1, len(dates)):
        d = dates[t]
        r = 0.0
        # 1) P&L van positie over dag t (gehouden sinds slot t-1)
        if pos:
            ra, rb = pa[d] / pa[dates[t - 1]] - 1, pb[d] / pb[dates[t - 1]] - 1
            nights = (d - dates[t - 1]).days
            f = RF(dates[t - 1])
            fin = 0.0
            for w in (wa, wb):
                fin += 0.0 if os.environ.get("NOCOST") else (-w * f - abs(w) * 0.02) * nights / 365  # long betaalt rf+2%, short ontvangt rf-2%
            r += wa * ra + wb * rb + fin
            held += 1
        # 2) uitvoeren van de beslissing van gisteren op slot t
        if pending is not None:
            kind, new_pos, beta = pending
            if kind == "exit" and pos:
                r -= abs(wa) * ca + abs(wb) * cb
                pos = 0; wa = wb = 0.0
            elif kind == "entry" and not pos:
                pos = new_pos
                wa = pos / (1 + abs(beta)); wb = -pos * beta / (1 + abs(beta))
                r -= abs(wa) * ca + abs(wb) * cb
                held = 0; trades += 1
            pending = None
        # 3) beslissing op slot t (venster t-60..t-1)
        a, b = ols(lb[t - LOOK:t], la[t - LOOK:t])
        res = [la[i] - a - b * lb[i] for i in range(t - LOOK, t)]
        m, s = statistics.mean(res), statistics.stdev(res)
        if s > 0:
            z = (la[t] - a - b * lb[t] - m) / s
            if pos and (abs(z) < EXIT or abs(z) > STOP or held >= MAXD):
                pending = ("exit", 0, b)
            elif not pos and abs(z) > ENTRY and abs(z) <= STOP:
                pending = ("entry", -1 if z > 0 else 1, b)
        if d >= start:
            daily.append((d, r))
    return daily, trades


def summarize(label, daily, trades, n_trials=334):
    rets = [r for _, r in daily]
    eq, peak, mdd = 1.0, 1.0, 0.0
    yr = {}
    for d, r in daily:
        prev = eq; eq *= 1 + r; peak = max(peak, eq); mdd = max(mdd, 1 - eq / peak)
        yr.setdefault(d.year, [prev, eq])[1] = eq
    yrs = len(rets) / 252
    cagr = eq ** (1 / yrs) - 1 if yrs > 0 else 0
    t = st.t_stat(rets)
    dsr = st.deflated_sharpe(rets, n_trials)[0]
    print(f"  {label:<24}{yrs:>5.1f}jr N {trades:>4} CAGR {cagr*100:+6.2f}% SR {st.sharpe(rets)[0]:+.2f} t {t:+.2f} "
          f"DD {mdd*100:5.1f}% jaren+ {sum(v[1] > v[0] for v in yr.values())}/{len(yr)} DSR {dsr:.2f} totaal {(eq-1)*100:+.1f}%")
    return {"t": t, "trades": trades, "dsr": dsr, "total": eq - 1, "yrs": yrs}


def main():
    os.makedirs("results/c1", exist_ok=True)
    print("ETF-paren (Yahoo, 2004–2026):")
    etf_res = {}
    for a, b, ftmo in ETF:
        pa, pb = load(f"data/yahoo/{a}.csv"), load(f"data/yahoo/{b}.csv")
        daily, n = run(pa, pb, COST.get(a, 0.0002), COST.get(b, 0.0002), date(2004, 1, 1))
        etf_res[ftmo] = summarize(f"{a}/{b}", daily, n)
    print("FTMO-paren (D1, test 2021–2026):")
    for a, b in FTMO:
        pa, pb = load(f"{a}_rates.csv"), load(f"{b}_rates.csv")
        daily, n = run(pa, pb, COST.get(a, 0.0002), COST.get(b, 0.0002), date(2021, 1, 1))
        key = f"{a.replace('cash', '')}/{b.replace('cash', '')}"
        fr = summarize(key, daily, n)
        e = etf_res.get(key)
        ok = e is not None and e["t"] >= 3 and e["yrs"] >= 15 and e["trades"] >= 300 and e["dsr"] >= 0.5 and fr["total"] > 0
        print(f"      → {'GESLAAGD' if ok else 'afgewezen'}" + ("" if e else " (geen ETF-tegenhanger: 15-jaar-eis niet toetsbaar)"))


if __name__ == "__main__":
    main()
