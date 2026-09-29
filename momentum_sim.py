"""Python-simulatie van MomentumRotation.mq5 (zelfde regels), voor lange validatie.

Regels (gelijk aan de EA):
- Rebalans op de eerste handelsdag van elke maand. Signaal = slot van de vorige
  handelsdag t.o.v. het slot op/voor (dag - 30*lookback kalenderdagen).
- Top-K op trailing rendement, gelijk gewogen: notional per leg = equity * exposure / K.
  Een leg die target blijft wordt NIET herschaald (EA houdt de positie).
- Regimefilter: gemiddelde van 10 slotkoersen (vorige dag, -30d, ..., -270d) van het
  regimesymbool; vorige slot <= dat gemiddelde -> alles flat die maand.
- Uitvoering: op het slot van de rebalansdag (1 dag vertraging, conservatief).
- CFD-boekhouding in accountvaluta: P&L = stuks * koersverschil * fx(nu).
- Kosten: financiering FIN_PCT/jaar over de notional per kalenderdag; spread
  SPREAD_PCT per kant over de verhandelde notional.

Universum: vaste lijst (--symbols) of point-in-time per handelsjaar (--pit bestand).
Bron: --src yahoo (data/yahoo/<T>.csv) of --src ftmo (<SYM>_rates.csv in de repo-root).
Output: samenvatting per jaar + <out>_daily.csv in het formaat van analyze_daily.py/
mc_daily_ftmo.py/walk_forward.py (min_equity = slotequity; geen intraday-data).
"""
import argparse
import bisect
import csv
import os
from datetime import date, datetime, timedelta

SPLICES = {"GLD": "GC=F", "SLV": "SI=F", "USO": "CL=F"}  # vóór ETF-start: futures-rendementen


def load_series(sym, src):
    if src == "yahoo":
        fn = f"data/yahoo/{sym.replace('=', '_')}.csv"
    else:
        fn = sym.replace(".cash", "cash") + "_rates.csv"
    out = []
    for r in csv.DictReader(open(fn, encoding="utf-8-sig"), delimiter=";"):
        out.append((datetime.strptime(r["date"][:10], "%Y.%m.%d").date(), float(r["close"])))
    out.sort()
    if src == "yahoo" and sym in SPLICES:
        base = load_series(SPLICES[sym], src)
        first_d, first_p = out[0]
        anchor = [p for d, p in base if d <= first_d]
        if anchor:
            k = first_p / anchor[-1]
            out = [(d, p * k) for d, p in base if d < first_d and p > 0] + out
    return out


class Series:
    def __init__(self, rows):
        self.d = [x[0] for x in rows]
        self.p = [x[1] for x in rows]

    def at_or_before(self, day):
        i = bisect.bisect_right(self.d, day) - 1
        return self.p[i] if i >= 0 else None

    def before(self, day):
        i = bisect.bisect_left(self.d, day) - 1
        return self.p[i] if i >= 0 else None

    def first(self):
        return self.d[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="yahoo")
    ap.add_argument("--symbols", default="")
    ap.add_argument("--pit", default="")
    ap.add_argument("--regime", default="SPY")
    ap.add_argument("--regime-months", type=int, default=10)
    ap.add_argument("--topn", type=int, default=2)
    ap.add_argument("--lookback", type=int, default=3)
    ap.add_argument("--exposure", type=float, default=0.30)
    ap.add_argument("--start", default="2000-01-01")
    ap.add_argument("--end", default="2026-09-21")
    ap.add_argument("--capital", type=float, default=100000)
    ap.add_argument("--fin", type=float, default=0.08)
    ap.add_argument("--spread", type=float, default=0.0005)
    ap.add_argument("--acct-ccy", default="USD", help="EUR: USD-instrumenten omgerekend via EURUSD")
    ap.add_argument("--ccy-map", default="EU50.cash:EUR,GER40.cash:EUR,UK100.cash:GBP")
    ap.add_argument("--out", default="")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--fill", default="close", choices=["close", "prevclose"], help="uitvoeringskoers rebalans: slot van de dag of vorige slot (~open)")
    ap.add_argument("--picks", default="", help="schrijf gekozen targets per rebalans naar dit bestand")
    a = ap.parse_args()

    pit = {}
    if a.pit:
        for r in csv.DictReader((l for l in open(a.pit) if not l.startswith("#")), delimiter=";"):
            pit[int(r["handelsjaar"])] = r["tickers"].split(",")
        syms = sorted({s for v in pit.values() for s in v})
    else:
        syms = a.symbols.split(",")
    series = {s: Series(load_series(s, a.src)) for s in set(syms) | {a.regime}}
    fx = {}
    ccy_of = dict(x.split(":") for x in a.ccy_map.split(",") if x)
    if a.acct_ccy == "EUR":
        fx["EURUSD"] = Series(load_series("EURUSD", "ftmo"))
        if os.path.exists("EURGBP_rates.csv"):
            fx["EURGBP"] = Series(load_series("EURGBP", "ftmo"))

    def to_acct(ccy, day):
        """waarde van 1 eenheid instrumentvaluta in accountvaluta"""
        if a.acct_ccy == "USD":
            return 1.0
        if ccy == "EUR":
            return 1.0
        if ccy == "GBP" and "EURGBP" in fx:
            return 1.0 / fx["EURGBP"].at_or_before(day)
        return 1.0 / fx["EURUSD"].at_or_before(day)  # USD (en GBP zonder koers: benadering)

    def universe(day):
        return pit.get(day.year, []) if pit else syms

    start = datetime.strptime(a.start, "%Y-%m-%d").date()
    end = datetime.strptime(a.end, "%Y-%m-%d").date()
    cal = [d for d in series[a.regime].d if start <= d <= end]

    realized = a.capital
    pos = {}  # sym -> [units, entry_price]
    daily = []
    trades = 0
    picklog = []
    last_month = None
    prev_day = None
    prev_eq = a.capital

    def fillp(s, day):
        return series[s].before(day) if a.fill == "prevclose" else series[s].at_or_before(day)

    def floating(day):
        tot = 0.0
        for s, (u, e) in pos.items():
            p = series[s].at_or_before(day)
            tot += u * (p - e) * to_acct(ccy_of.get(s, "USD"), day)
        return tot

    for day in cal:
        start_bal = realized
        start_eq = prev_eq
        # financiering over kalenderdagen sinds vorige handelsdag
        if prev_day is not None and pos:
            days = (day - prev_day).days
            for s, (u, e) in pos.items():
                p = series[s].at_or_before(prev_day)
                realized -= u * p * to_acct(ccy_of.get(s, "USD"), prev_day) * a.fin / 365 * days
        if (day.year, day.month) != last_month:
            last_month = (day.year, day.month)
            eq_now = realized + floating(day)
            targets = []
            rg = series[a.regime]
            closes = [rg.before(day - timedelta(days=30 * j)) if j else rg.before(day) for j in range(a.regime_months)]
            risk_on = a.regime_months <= 0 or None in closes or rg.before(day) > sum(closes) / len(closes)
            if risk_on:
                scored = []
                for s in universe(day):
                    sr = series[s]
                    now, then = sr.before(day), sr.at_or_before(day - timedelta(days=30 * a.lookback))
                    if now and then and sr.first() <= day - timedelta(days=30 * a.lookback):
                        scored.append(((now - then) / then, s))
                scored.sort(reverse=True)
                targets = [s for _, s in scored[:a.topn]]
            if a.picks:
                picklog.append(f"{day.strftime('%Y.%m')};{'on' if risk_on else 'off'};{','.join(targets)}")
            for s in list(pos):
                if s not in targets:
                    u, e = pos.pop(s)
                    p = fillp(s, day)
                    f = to_acct(ccy_of.get(s, "USD"), day)
                    realized += u * (p - e) * f - u * p * f * a.spread
                    trades += 1
            k = len(targets)
            for s in targets:
                if s in pos:
                    continue
                p = fillp(s, day)
                f = to_acct(ccy_of.get(s, "USD"), day)
                u = eq_now * a.exposure / k / (p * f)
                pos[s] = [u, p]
                realized -= u * p * f * a.spread
        eq = realized + floating(day)
        daily.append((day, start_bal, start_eq, min(start_eq, eq), eq))
        prev_eq = eq
        prev_day = day

    # samenvatting
    years = {}
    for d, sb, se, mn, en in daily:
        y = years.setdefault(d.year, [se, en])
        y[1] = en
    peak, mdd, sdd = a.capital, 0.0, 0.0
    for d, sb, se, mn, en in daily:
        peak = max(peak, en)
        mdd = max(mdd, (peak - mn) / peak)
        sdd = max(sdd, (a.capital - mn) / a.capital)
    yr_ret = {y: v[1] / v[0] - 1 for y, v in years.items()}
    months = len(daily) / 21
    cagr = (daily[-1][4] / a.capital) ** (12 / months) - 1
    if not a.quiet:
        print(" ".join(f"{y}:{r*100:+.1f}%" for y, r in yr_ret.items()))
    pos_years = sum(r > 0 for r in yr_ret.values())
    print(f"topn={a.topn} lb={a.lookback} expo={a.exposure:.2f} | CAGR {cagr*100:+.2f}%/jr | jaren+ {pos_years}/{len(yr_ret)} "
          f"({pos_years/len(yr_ret)*100:.0f}%) | trailDD {mdd*100:.1f}% | statDD {sdd*100:.1f}% | trades {trades} "
          f"| €/mnd op €80k ≈ {(daily[-1][4]/a.capital-1)*80000/months:,.0f}")
    if a.picks:
        open(a.picks, "w").write("\n".join(picklog) + "\n")
    if a.out:
        with open(a.out, "w") as f:
            f.write("date;start_balance;start_equity;min_equity;end_equity\n")
            for d, sb, se, mn, en in daily:
                f.write(f"{d.strftime('%Y.%m.%d')};{sb:.2f};{se:.2f};{mn:.2f};{en:.2f}\n")


if __name__ == "__main__":
    main()
