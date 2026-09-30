"""v31 QA-2/3 (geen trial): (a) kosten/omloop van P-ETF-a per jaar in €/€80k — omloop per instrument, aantal transacties, kosten volgens
model A (engine: 13 bp rondreis = 6,5 bp per eenheid) en model B (NL-retail vast €3,50/transactie + 1,5 bp halve spread; web-claim €3–3,75),
TER per bouwsteen (aandelen-ETF 0,07%, obligatie-ETF 0,10%, goud-ETC 0,12%; web-claims); (b) EUR-backtest van de hele P-ETF-a (ongehedged
en gehedged) met €/mnd totaal en boven EUR-cash. Ontdekking ≤ 2024; reserve niet aangeraakt."""
import math
from collections import defaultdict
from datetime import date

import numpy as np

import catalogus.C02_faber as C02
import catalogus.C52_allweather as C52
import forward_portfolio as FP
from engine.forward import series
from engine.run_rule import load_daily

CAP = 80000.0
DISC = date(2024, 12, 31)
TER = {"SPY": 0.07, "BOND10_SYN": 0.10, "GOLD_F": 0.12, "SPX": 0.07, "NDX": 0.07, "DJI": 0.07, "DAX": 0.07, "N225": 0.07}
FIX, HALF_SPREAD = 3.50, 1.5e-4

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
def posmap(df, pos):   # positie ná slot t (doelpositie van dag t)
    return {d: float(v) for d, v in zip(df["date"], np.nan_to_num(pos))}
m52 = {n: posmap(d52[n], pos52[n]) for n in p52["assets"]}
m02 = {n: posmap(d02[n], p02[n]) for n in d02}

# doel-exposure per instrument (fractie kapitaal) per dag; transactie = wijziging t.o.v. vorige dag
inst = list(m52) + list(m02)
prev = {n: 0.0 for n in inst}
last = {n: 0.0 for n in inst}   # laatst bekende sleeve-positie (feestdagen/kalenderverschil: positie loopt door, geen neppe transactie)
yr_turn, yr_trades, yr_fix, yr_pct, yr_ter, yr_days = (defaultdict(float) for _ in range(6))
for i, d in enumerate(days):
    if not np.isfinite(W[0, i]) or d > DISC:
        continue
    for n in m52:
        last[n] = m52[n].get(d, last[n])
    for n in m02:
        last[n] = m02[n].get(d, last[n])
    tgt = {n: W[0, i] * last[n] for n in m52}
    tgt.update({n: W[1, i] * last[n] / len(m02) for n in m02})
    y = d.year
    for n in inst:
        dlt = abs(tgt[n] - prev[n])
        if dlt > 1e-6:
            yr_turn[y] += dlt; yr_trades[y] += 1
            yr_fix[y] += FIX + dlt * CAP * HALF_SPREAD
            yr_pct[y] += dlt * CAP * 6.5e-4
        yr_ter[y] += abs(tgt[n]) * CAP * TER[n] / 100 / 252
        prev[n] = tgt[n]
    yr_days[y] += 1
yrs = sorted(y for y in yr_days if yr_days[y] > 200)
lines = ["# v31 QA-2/3 — kosten/omloop P-ETF-a per jaar (€ op €80k) en EUR-backtest (ontdekking ≤ 2024)", "",
         "Transactie = wijziging van de doelpositie van een instrument (maandherweging zonder drempel volgens PREREG_PORT + signaalwissels C02/C52).",
         "Model A = engine (6,5 bp per eenheid omloop = 0,05% commissie + 1,5 bp halve spread); model B = NL-retail vast €3,50/transactie (web-claim €3–3,75) + 1,5 bp.",
         "TER (web-claims): aandelen-ETF 0,07%, obligatie-ETF 0,10%, goud-ETC 0,12%.", "",
         "| jaar | omloop (× kapitaal) | transacties | kosten A € | kosten B € | TER € | totaal A+TER € | totaal B+TER € |", "|---|---|---|---|---|---|---|---|"]
for y in yrs:
    lines.append(f"| {y} | {yr_turn[y]:.2f} | {int(yr_trades[y])} | {yr_pct[y]:,.0f} | {yr_fix[y]:,.0f} | {yr_ter[y]:,.0f} | {yr_pct[y]+yr_ter[y]:,.0f} | {yr_fix[y]+yr_ter[y]:,.0f} |")
avg = lambda dct: np.mean([dct[y] for y in yrs])
lines += ["", f"**Gemiddeld per jaar ({yrs[0]}–{yrs[-1]}):** omloop {avg(yr_turn):.2f}× kapitaal, {avg(yr_trades):.0f} transacties; kosten A €{avg(yr_pct):,.0f} "
          f"(≈ {avg(yr_pct)/CAP*100:.2f}%), B €{avg(yr_fix):,.0f} (≈ {avg(yr_fix)/CAP*100:.2f}%), TER €{avg(yr_ter):,.0f} (≈ {avg(yr_ter)/CAP*100:.2f}%) "
          f"→ totaal A+TER ≈ €{(avg(yr_pct)+avg(yr_ter))/12:,.0f}/mnd, B+TER ≈ €{(avg(yr_fix)+avg(yr_ter))/12:,.0f}/mnd.",
          "In de backtest/forward zitten al: model A + TER 0,07% overal (engine). Extra t.o.v. de engine bij model B: "
          f"≈ €{(avg(yr_fix)-avg(yr_pct))/12:,.0f}/mnd; bij TER-verschillen ≈ €{(avg(yr_ter)-sum(avg({y: 0 for y in yrs}) for _ in [0]))/12 - 80000*0.0007/12*0:,.0f}/mnd (zie TER-kolom).",
          f"Een drempelregel (bv. geen transactie < 1% gewichtsverschil) zou het aantal transacties sterk verlagen — dat is een **andere regel** (niet in PREREG_PORT) en alleen als gevoeligheid te toetsen."]

# EUR-backtest hele P-ETF-a
Pd, P = FP.run_petf(S)
tot, x, _ = P["P-ETF-a"]
eu, eh = FP.eur_series(Pd, tot)
es = {l.split(";")[0]: float(l.split(";")[4]) for l in open("data/daily/YLD_ESTR.csv") if l[:1].isdigit()}
eb = sorted((l.split(";")[0], float(l.split(";")[4])) for l in open("data/daily/YLD_EURIBOR3M.csv") if l[:1].isdigit())
import bisect
kb = [a for a, _ in eb]; ks = sorted(es)
def eurc(d):
    s = d.isoformat()
    if ks and s >= ks[0]:
        return es[ks[bisect.bisect_right(ks, s) - 1]]
    return eb[max(0, bisect.bisect_right(kb, s) - 1)][1]
D = np.array(Pd)
lines += ["", "## EUR-backtest van de hele P-ETF-a (ontdekking)", "", "| periode | variant | CAGR EUR | vol | maxDD | boven EUR-cash/jr | €/mnd totaal | €/mnd boven cash |", "|---|---|---|---|---|---|---|---|"]
for lo, lbl in ((date(2004, 1, 1), "2004–24"), (date(2011, 1, 1), "2011–24"), (date(2021, 1, 1), "2021–24")):
    sel = (D >= lo) & (D <= DISC) & np.isfinite(eu) & np.isfinite(eh)
    dd = D[sel]; nights = np.r_[0, [(b - a).days for a, b in zip(dd[:-1], dd[1:])]]
    ec = np.array([eurc(d) for d in dd]) / 100 / 365 * nights
    for vn, r in (("ongehedged", eu[sel]), ("gehedged", eh[sel])):
        n = len(r); eq = np.cumprod(1 + r); cagr = eq[-1] ** (252 / n) - 1
        mdd = float(np.max(1 - eq / np.maximum.accumulate(eq))); ex = np.prod(1 + r - ec) ** (252 / n) - 1
        lines.append(f"| {lbl} | {vn} | {cagr*100:.1f}% | {r.std()*math.sqrt(252)*100:.1f}% | {mdd*100:.1f}% | {ex*100:.1f}% | €{CAP*cagr/12:,.0f} | €{CAP*ex/12:,.0f} |")
lines += ["", "Backtest-getallen = gerealiseerde premies (regime-afhankelijk, D-070/D-073); vóór live-haircut en box 3. Verwachting: zie VERWACHTING.md / QA_exposures_MC.md."]
open("results/port/QA_kosten_EUR.md", "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
