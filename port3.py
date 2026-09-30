"""PREREG_PORT3 (SHA in RUNLOG): instrumentniveau-simulator P-ETF-a met meedrijvende posities; P-ETF-a-inst (drempel 0) en P-ETF-a-D1 (drempel 1%).
Kosten model B (NL-retail €3,50/transactie + 1,5 bp) primair, model A (6,5 bp/eenheid) gevoeligheid; TER per instrument. Geen trial, geen selectie.
Gebruik: python port3.py            → rapport results/port/PORT3_backtest.md (ontdekking ≤ 2024)
         python port3.py --forward  → forward/portfolio3_daily.csv (append-only vanaf 2026-10-01)"""
import math
import os
import sys
from datetime import date, datetime, timezone

import numpy as np

import catalogus.C02_faber as C02
import catalogus.C52_allweather as C52
import forward_portfolio as FP
from engine.forward import series
from engine.run_rule import load_daily, rf_on

CAP = 80000.0
DISC = date(2024, 12, 31)
FORWARD_START = date(2026, 10, 1)
OUT = "forward/portfolio3_daily.csv"
TER = {"SPY": 0.07, "BOND10_SYN": 0.10, "GOLD_F": 0.12, "SPX": 0.07, "NDX": 0.07, "DJI": 0.07, "DAX": 0.07, "N225": 0.07}
RET_SRC = {"SPX": ("SPX_TR", "adjclose")}          # etf-vehikel: total return voor SPX (zoals engine TR_PROXY)


def instrument_returns(names):
    out = {}
    for n in names:
        src, field = RET_SRC.get(n, (n, "adjclose" if n in ("SPY",) else "close"))
        df = load_daily(src, field); c = df["close"]
        out[n] = {d: float(c[i] / c[i - 1] - 1) for i, d in enumerate(df["date"]) if i > 0 and c[i - 1] > 0}
    return out


def targets():
    S = {"S_C52L": series("C52_allweather", "lang", "etf"), "S_C02": series("C02_faber", "basis", "etf")}
    days, X = FP.calendar_and_x(FP.PETF, S)
    reb = FP.rebalance_flags(days); W = np.full((2, len(days)), np.nan); cur = None
    for i in range(len(days)):
        if reb[i]:
            s = np.array([FP.sig(X[j], i) for j in range(2)])
            if np.all(np.isfinite(s)) and np.all(s > 0):
                cur = (1 / s) / (1 / s).sum()
        if cur is not None:
            W[:, i] = cur
    R52 = C52.RULE; p52 = R52["varianten"]["lang"]
    d52 = {n: load_daily(n, R52.get("field", "adjclose")) for n in R52["instrumenten"]}
    pos52 = C52.positions_all(d52, p52)
    d02 = {n: load_daily(n, C02.RULE.get("field", "adjclose")) for n in C02.RULE["instrumenten"]}
    p02 = {n: np.asarray(C02.positions(d02[n], C02.RULE["varianten"]["basis"]), float) for n in d02}
    m52 = {n: dict(zip(d52[n]["date"], np.nan_to_num(pos52[n]))) for n in p52["assets"]}
    m02 = {n: dict(zip(d02[n]["date"], np.nan_to_num(p02[n]))) for n in d02}
    last = {n: 0.0 for n in list(m52) + list(m02)}
    T = []
    for i, d in enumerate(days):
        for n in m52:
            last[n] = m52[n].get(d, last[n])
        for n in m02:
            last[n] = m02[n].get(d, last[n])
        if not np.isfinite(W[0, i]):
            T.append(None); continue
        t = {n: W[0, i] * last[n] for n in m52}
        t.update({n: W[1, i] * last[n] / len(m02) for n in m02})
        T.append(t)
    return days, T, list(m52) + list(m02)


def simulate(days, T, names, R, threshold, model):
    """doel T[i] = exposure ná slot van dag i (geldt voor het rendement van dag i+1). Rendement dag i met holdings van gisteren."""
    n = len(days); nights = np.r_[0, [(b - a).days for a, b in zip(days[:-1], days[1:])]]
    rf = rf_on(days) / 100 / 365 * nights
    h = {k: 0.0 for k in names}; cash = 1.0; V = 1.0
    tot = np.full(n, np.nan); ntr = np.zeros(n); turn = np.zeros(n); costs = np.zeros(n)
    started = False; prev_t = None
    for i, d in enumerate(days):
        if started:
            gross = sum(h[k] * R[k].get(d, 0.0) for k in names) + cash * rf[i]
            ter = sum(abs(h[k]) * TER[k] for k in names) / 100 / 365 * nights[i]
            r = gross - ter
            # drift
            for k in names:
                h[k] = h[k] * (1 + R[k].get(d, 0.0)) / (1 + r)
            cash = cash * (1 + rf[i]) / (1 + r)
            V *= 1 + r
            tot[i] = r
        t = T[i]
        if t is None:
            continue
        started = True
        changed = prev_t is None or any(abs(t[k] - prev_t[k]) > 1e-12 for k in names)
        prev_t = t
        if not changed:
            continue
        c = 0.0
        for k in names:
            dl = t[k] - h[k]
            if abs(dl) > 1e-9 and abs(dl) >= threshold:
                c += (3.50 / (CAP * V) + abs(dl) * 1.5e-4) if model == "B" else abs(dl) * 6.5e-4
                h[k] = t[k]; cash -= dl; ntr[i] += 1; turn[i] += abs(dl)
        cash -= c; costs[i] = c
        if np.isfinite(tot[i]):
            tot[i] -= c
    return tot, ntr, turn, costs, rf


def run_all():
    days, T, names = targets()
    R = instrument_returns(names)
    res = {}
    for lbl, thr in (("P-ETF-a-inst", 0.0), ("P-ETF-a-D1", 0.01)):
        for m in ("B", "A"):
            res[(lbl, m)] = simulate(days, T, names, R, thr, m)
    return np.array(days), res


def report():
    D, res = run_all()
    lines = ["# PORT3 — drempelvariant P-ETF-a (PREREG_PORT3; ontdekking ≤ 2024; geen trial)", "",
             "| rij | kosten | periode | SR (excess) | CAGR | maxDD | alfa/jr | transacties/jr | omloop/jr | kosten €/jr | alfa €/mnd |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for (lbl, m), (tot, ntr, turn, costs, rf) in res.items():
        for lo, per in ((date(2001, 1, 1), "2001–24"), (date(2011, 1, 1), "2011–24"), (date(2021, 1, 1), "2021–24")):
            sel = (D >= lo) & (D <= DISC) & np.isfinite(tot)
            t, e = tot[sel], tot[sel] - rf[sel]; yrs = sel.sum() / 252
            eq = np.cumprod(1 + t); dd = float(np.max(1 - eq / np.maximum.accumulate(eq)))
            ex = np.prod(1 + e) ** (1 / yrs) - 1
            lines.append(f"| {lbl} | {m} | {per} | {e.mean()/e.std()*math.sqrt(252):.2f} | {(eq[-1]**(1/yrs)-1)*100:.1f}% | {dd*100:.1f}% | {ex*100:.1f}% | "
                         f"{ntr[sel].sum()/yrs:.0f} | {turn[sel].sum()/yrs:.2f} | {costs[sel].sum()/yrs*CAP:,.0f} | €{CAP*ex/12:,.0f} |")
    lines += ["", "Referentie P-ETF-a (PREREG_PORT, sleeve-niveau, kosten model A in de engine): SR 0,94 / CAGR 7,4% / maxDD 11,2% (2001–24).",
              "Verschil inst-drempel-0 vs PREREG_PORT: meedrijvende posities i.p.v. vaste gewichten binnen de maand, kosten per instrument."]
    open("results/port/PORT3_backtest.md", "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


def forward():
    D, res = run_all()
    rows = {}
    for lbl in ("P-ETF-a-inst", "P-ETF-a-D1"):
        tot, ntr, *_ = res[(lbl, "B")]
        eu, eh = FP.eur_series(list(D), tot)
        for i, d in enumerate(D):
            if d >= FORWARD_START and np.isfinite(tot[i]):
                rows.setdefault(d.isoformat(), []).append(f"{tot[i]:.8f};{eu[i]:.8f};{eh[i]:.8f};{int(ntr[i])}")
    logged = set()
    if os.path.exists(OUT):
        logged = {l.split(";")[0] for l in open(OUT) if l[:1].isdigit()}
    else:
        with open(OUT, "w") as f:
            f.write("date;" + ";".join(f"{p}_usd;{p}_eur;{p}_eur_hedged;{p}_transacties" for p in ("P-ETF-a-inst", "P-ETF-a-D1")) + ";berekend_utc\n")
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    new = [f"{d};{';'.join(v)};{ts}" for d, v in sorted(rows.items()) if d not in logged and len(v) == 2]
    if new:
        with open(OUT, "a") as f:
            f.write("\n".join(new) + "\n")
    print(f"port3 forward: {len(new)} nieuwe dag(en)")


if __name__ == "__main__":
    os.makedirs("results/port", exist_ok=True); os.makedirs("forward", exist_ok=True)
    forward() if "--forward" in sys.argv else report()
