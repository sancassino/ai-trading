"""Ronde 2 (NEXT_STEPS): familie 1 (tijdreeks-trend multi-asset) en familie 2 (G10 FX carry+trend).
Implementeert exact PREREG_ronde2.md. Gebruik: python3 ronde2_sim.py 1|2|ref [--out prefix]
"""
import argparse
import bisect
import csv
import math
import statistics
from datetime import date, datetime

START, END = date(2000, 1, 1), date(2026, 9, 21)
import os
VOL_TGT, LEV_CAP, SPREAD = 0.10, 4.0, 0.0005
MARKUP_ETF, MARKUP_FX = 0.02, 0.015
if os.environ.get("NO_MARKUP"):  # diagnostiek: zonder spread/markup (financiering tegen korte rente blijft)
    SPREAD, MARKUP_ETF, MARKUP_FX = 0.0, 0.0, 0.0


def read_csv(path, datecol, valcol, fmt):
    out = []
    for r in csv.DictReader(open(path, encoding="utf-8-sig"), delimiter="," if path.endswith("csv") and "fred" in path else ";"):
        v = r[valcol].strip()
        if v in ("", "."):
            continue
        out.append((datetime.strptime(r[datecol][:10], fmt).date(), float(v)))
    return sorted(out)


def yahoo(t):
    return read_csv(f"data/yahoo/{t.replace('=', '_').replace('^', '')}.csv", "date", "close", "%Y.%m.%d")


def fred(i):
    return read_csv(f"data/fred/{i}.csv", "observation_date", i, "%Y-%m-%d")


def splice(main, proxy):
    d0, p0 = main[0]
    anchor = [p for d, p in proxy if d <= d0]
    if not anchor:
        return main
    k = p0 / anchor[-1]
    return [(d, p * k) for d, p in proxy if d < d0 and p > 0] + main


class Step:
    """voorwaarts gevulde reeks"""
    def __init__(self, rows):
        self.d = [x[0] for x in rows]
        self.v = [x[1] for x in rows]

    def at(self, day):
        i = bisect.bisect_right(self.d, day) - 1
        return self.v[i] if i >= 0 else None


def monthly_lagged(series_id):
    """maandreeks (observation = eerste van de maand) 1 maand vertraagd beschikbaar"""
    rows = fred(series_id)
    shifted = []
    for d, v in rows:
        m = d.month + 1
        shifted.append((date(d.year + (m > 12), (m - 1) % 12 + 1, 1), v / 100))
    return Step(shifted)


CCY_FX = {  # prijs = USD per 1 eenheid valuta
    "EUR": ("DEXUSEU", False), "GBP": ("DEXUSUK", False), "AUD": ("DEXUSAL", False), "NZD": ("DEXUSNZ", False),
    "JPY": ("DEXJPUS", True), "CHF": ("DEXSZUS", True), "CAD": ("DEXCAUS", True), "NOK": ("DEXNOUS", True),
    "SEK": ("DEXSDUS", True)}
CCY_RATE = {"USD": "US", "EUR": "EZ", "JPY": "JP", "GBP": "GB", "CHF": "CH", "AUD": "AU", "NZD": "NZ",
            "CAD": "CA", "NOK": "NO", "SEK": "SE"}


def build(family):
    inst = {}  # naam -> dict(price=Step, kind='etf'|'fx', ccy)
    if family in ("1", "ref"):
        etfs = {"SPY": None, "EFA": None, "EEM": None, "TLT": None, "IEF": None,
                "GLD": "GC=F", "USO": "CL=F", "DBC": "^SPGSCI"} if family == "1" else {"SPY": None}
        for t, px in etfs.items():
            rows = yahoo(t)
            if px:
                rows = splice(rows, yahoo(px))
            inst[t] = {"rows": rows, "kind": "etf"}
    ccys = ["EUR", "JPY", "GBP", "AUD"] if family == "1" else (list(CCY_FX) if family == "2" else [])
    for c in ccys:
        sid, inv = CCY_FX[c]
        rows = [(d, 1 / v if inv else v) for d, v in fred(sid)]
        inst[c] = {"rows": rows, "kind": "fx", "ccy": c}
    return inst


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("family", choices=["1", "2", "ref"])
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    inst = build(a.family)
    cal = [d for d, _ in yahoo("SPY") if d <= END]
    rusd = Step([(d, v / 100) for d, v in fred("DTB3")])
    rates = {c: monthly_lagged(f"IR3TIB01{k}M156N") for c, k in CCY_RATE.items()}
    for v in inst.values():
        v["px"] = Step(v["rows"])
        v["first"] = v["rows"][0][0]

    # dagrendementen per instrument op de kalender (voorwaarts gevuld)
    names = list(inst)
    px = {n: [inst[n]["px"].at(d) for d in cal] for n in names}

    def ret_hist(n, i, k):
        """laatste k dagrendementen t/m index i-1 (vorige slot)"""
        p = px[n]
        return [p[j] / p[j - 1] - 1 for j in range(max(1, i - k), i) if p[j] and p[j - 1]]

    equity = 100000.0
    units = {n: 0.0 for n in names}
    notional_prev = {n: 0.0 for n in names}
    daily = []
    last_month = None
    prev_i = None
    started = False
    gross_hist = []
    for i, d in enumerate(cal):
        if d < START:
            continue
        # P&L van gisteren naar vandaag
        if prev_i is not None:
            dt = (d - cal[prev_i]).days / 365
            pnl = 0.0
            ru = rusd.at(cal[prev_i]) or 0.0
            for n in names:
                u = units[n]
                if not u:
                    continue
                p0, p1 = px[n][prev_i], px[n][i]
                notional = u * p0
                pnl += u * (p1 - p0)
                if inst[n]["kind"] == "etf":
                    if a.family != "ref":  # referentie = gewone b&h, financiering via cash-rest hieronder
                        pnl += -notional * ru * dt - abs(notional) * MARKUP_ETF * dt
                else:
                    rc = rates[inst[n]["ccy"]].at(cal[prev_i])
                    rus = rates["USD"].at(cal[prev_i])
                    diff = (rc - rus) if rc is not None and rus is not None else 0.0
                    pnl += notional * diff * dt - abs(notional) * MARKUP_FX * dt
            equity_prev = equity
            equity += pnl
            daily.append((d, equity_prev, equity))
        # maandelijkse rebalans
        if (d.year, d.month) != last_month:
            last_month = (d.year, d.month)
            active = [n for n in names if px[n][i - 1] and i > 252 + 61 and px[n][i - 253]
                      and inst[n]["first"] <= cal[i - 253]]
            w = {n: 0.0 for n in names}
            vol = {}
            for n in active:
                rs = ret_hist(n, i, 60)
                vol[n] = statistics.stdev(rs) * math.sqrt(252) if len(rs) > 20 else None
            active = [n for n in active if vol.get(n)]

            def trend_weights(ns):
                out = {}
                for n in ns:
                    s = 1.0 if px[n][i - 1] / px[n][i - 253] - 1 > 0 else -1.0
                    out[n] = s * (VOL_TGT / vol[n]) / len(ns)
                return out

            def scale(wd):
                if not wd:
                    return wd
                port = []
                for j in range(max(1, i - 60), i):
                    port.append(sum(wv * (px[n][j] / px[n][j - 1] - 1) for n, wv in wd.items()))
                sp = statistics.stdev(port) * math.sqrt(252) if len(port) > 20 else 0
                k = VOL_TGT / sp if sp > 0 else 0
                g = sum(abs(v) for v in wd.values()) * k
                if g > LEV_CAP:
                    k *= LEV_CAP / g
                return {n: v * k for n, v in wd.items()}

            if a.family == "1":
                w.update(scale(trend_weights(active)))
            elif a.family == "2":
                # carry: rangschik 10 valuta's (JPY pas als rente beschikbaar is)
                avail = [c for c in CCY_RATE if rates[c].at(d) is not None and (c == "USD" or c in active)]
                ranked = sorted(avail, key=lambda c: rates[c].at(d), reverse=True)
                carry = {}
                if len(ranked) >= 6:
                    for c in ranked[:3]:
                        if c != "USD":
                            carry[c] = carry.get(c, 0) + 1 / 6
                    for c in ranked[-3:]:
                        if c != "USD":
                            carry[c] = carry.get(c, 0) - 1 / 6
                carry = {c: v * VOL_TGT / vol[c] for c, v in carry.items()}
                trend = trend_weights(active)
                cs, ts = scale(carry), scale(trend)
                comb = {n: 0.5 * cs.get(n, 0) + 0.5 * ts.get(n, 0) for n in set(cs) | set(ts)}
                w.update(scale(comb))
            else:  # ref: SPY 100% (schaal later)
                w["SPY"] = 1.0 if "SPY" in active else 0.0
            # uitvoeren op slot van vandaag
            cost = 0.0
            for n in names:
                new_notional = w[n] * equity
                cost += abs(new_notional - units[n] * px[n][i]) * SPREAD if px[n][i] else 0
                units[n] = new_notional / px[n][i] if px[n][i] and w[n] else 0.0
            equity -= cost
            gross_hist.append((d, sum(abs(v) for v in w.values())))
            if daily:
                daily[-1] = (daily[-1][0], daily[-1][1], equity)
        prev_i = i

    # referentie: SPY op 10% vol, cash-rest tegen DTB3 (geen hefboomkosten nodig: schaal < 1)
    if a.family == "ref":
        rets = [e1 / e0 - 1 for _, e0, e1 in daily]
        k = VOL_TGT / (statistics.stdev(rets) * math.sqrt(252))
        eq = 100000.0
        nd = []
        for (d, e0, e1), r in zip(daily, rets):
            prev = eq
            eq *= 1 + k * r + (1 - k) * (rusd.at(d) or 0) / 252
            nd.append((d, prev, eq))
        daily = nd
        print(f"referentie-schaal SPY: {k:.2f}")
    report(daily, rusd, a.family, gross_hist)
    if a.out:
        with open(a.out, "w") as f:
            f.write("date;start_balance;start_equity;min_equity;end_equity\n")
            for d, e0, e1 in daily:
                f.write(f"{d.strftime('%Y.%m.%d')};{e0:.2f};{e0:.2f};{min(e0, e1):.2f};{e1:.2f}\n")


def report(daily, rusd, fam, gross_hist):
    rets = [e1 / e0 - 1 for _, e0, e1 in daily]
    # bugfix: bij familie 1/2 is de P&L al excess (longs betalen de korte rente, cash rendeert niet),
    # dus rf NIET nogmaals aftrekken; alleen bij de referentie (cash-rest verdient rf).
    ex = [r - ((rusd.at(d) or 0) / 252 if fam == "ref" else 0) for (d, _, _), r in zip(daily, rets)]
    yrs = len(daily) / 252
    cagr = (daily[-1][2] / daily[0][1]) ** (1 / yrs) - 1
    vol = statistics.stdev(rets) * math.sqrt(252)
    sharpe = statistics.mean(ex) / statistics.stdev(ex) * math.sqrt(252)
    # DD op dag- en maandbasis
    peak, ddd = daily[0][1], 0.0
    me = {}
    for d, e0, e1 in daily:
        peak = max(peak, e1); ddd = max(ddd, 1 - e1 / peak)
        me[(d.year, d.month)] = e1
    peak, mdd = daily[0][1], 0.0
    for v in me.values():
        peak = max(peak, v); mdd = max(mdd, 1 - v / peak)
    worst_day = min(rets)
    yr = {}
    for (d, e0, e1) in daily:
        y = yr.setdefault(d.year, [e0, e1]); y[1] = e1
    yret = {y: v[1] / v[0] - 1 for y, v in yr.items()}
    npos = sum(r > 0 for r in yret.values())

    def ep(a, b):
        xs = [(e0, e1) for d, e0, e1 in daily if a <= d <= b]
        return xs[-1][1] / xs[0][0] - 1 if xs else float("nan")

    print(f"FAMILIE {fam}: {daily[0][0]}..{daily[-1][0]} ({yrs:.1f} jr) | CAGR netto {cagr*100:+.2f}% | vol {vol*100:.1f}% | "
          f"Sharpe {sharpe:.2f} | maand-DD {mdd*100:.1f}% | dag-DD {ddd*100:.1f}% | slechtste dag {worst_day*100:.2f}% | "
          f"jaren+ {npos}/{len(yret)} ({npos/len(yret)*100:.0f}%) | €/mnd op €80k ≈ {cagr*80000/12:,.0f}")
    print("  episodes: 2000–02 {:+.1f}% | 2008 {:+.1f}% | 2020 {:+.1f}% | 2022 {:+.1f}%".format(
        ep(date(2000, 1, 1), date(2002, 12, 31)) * 100, ep(date(2008, 1, 1), date(2008, 12, 31)) * 100,
        ep(date(2020, 1, 1), date(2020, 12, 31)) * 100, ep(date(2022, 1, 1), date(2022, 12, 31)) * 100))
    print("  per jaar: " + " ".join(f"{str(y)[2:]}:{r*100:+.1f}" for y, r in yret.items()))
    if gross_hist:
        g = [x for _, x in gross_hist]
        print(f"  bruto hefboom: gem {statistics.mean(g):.2f}, max {max(g):.2f}")


if __name__ == "__main__":
    main()
