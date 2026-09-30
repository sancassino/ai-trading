"""D-075 / VERWACHTING §7 (geen trial): (1) werkelijke gemiddelde exposures van P-ETF-a per activaklasse (aandelen/obligaties/goud/cash),
2001–24 en 2021–24; (2) gerealiseerde excess per klasse per decennium; (3) premie-verwachting met echte exposures + Monte-Carlo p(totaal ≥ €400) en
p(alfa ≥ €287). Premies (excess t.o.v. cash, %/jr) laag/midden/hoog uit VERWACHTING.md v1 (Strateeg; web-claims/aannames). Ontdekking ≤ 2024."""
import math
from datetime import date

import numpy as np

import catalogus.C02_faber as C02
import catalogus.C52_allweather as C52
import forward_portfolio as FP
from engine.forward import series
from engine.run_rule import load_daily, rf_on

DISC = date(2024, 12, 31)
PREMIE = {"aandelen": (0.0, 2.0, 4.3), "obligaties": (-0.5, 1.0, 1.8), "goud": (-1.5, -0.25, 1.0)}   # VERWACHTING.md v1
COST = 0.20   # %/jr: TER 0,07% + herweging/omloop (≈ 13 bp × omloop) — aanname
ESTR = float(open("data/daily/YLD_ESTR.csv").read().strip().splitlines()[-1].split(";")[4])
USD3M = 4.07

# ---- sleeve-gewichten P-ETF-a exact als FP.run_petf ----
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
dix = {d: i for i, d in enumerate(days)}

# ---- posities binnen de sleeves (positie ná slot t geldt voor dag t+1) ----
R52 = C52.RULE; p52 = R52["varianten"]["lang"]
d52 = {n: load_daily(n, R52.get("field", "adjclose")) for n in R52["instrumenten"]}
pos52 = C52.positions_all(d52, p52)
def lagged(df, pos):
    return {d: (pos[i - 1] if i > 0 else 0.0) for i, d in enumerate(df["date"])}
e52 = {n: lagged(d52[n], np.nan_to_num(pos52[n])) for n in p52["assets"]}
d02 = {n: load_daily(n, C02.RULE.get("field", "adjclose")) for n in C02.RULE["instrumenten"]}
e02 = {n: lagged(d02[n], np.asarray(C02.positions(d02[n], C02.RULE["varianten"]["basis"]), float)) for n in d02}

cls = {"SPY": "aandelen", "BOND10_SYN": "obligaties", "GOLD_F": "goud"}
expo = {k: np.full(len(days), np.nan) for k in ("aandelen", "obligaties", "goud", "cash")}
for i, d in enumerate(days):
    if not np.isfinite(W[0, i]):
        continue
    a = {"aandelen": 0.0, "obligaties": 0.0, "goud": 0.0}
    for n, c in cls.items():
        a[c] += W[0, i] * e52[n].get(d, 0.0)
    eq02 = [e02[n][d] for n in e02 if d in e02[n]]
    a["aandelen"] += W[1, i] * (np.mean(eq02) if eq02 else 0.0)
    for k, v in a.items():
        expo[k][i] = v
    expo["cash"][i] = 1 - sum(a.values())
D = np.array(days)
lines = ["# D-075 — werkelijke exposures P-ETF-a, gerealiseerde excess per klasse, Monte-Carlo (geen trial; ontdekking ≤ 2024)", ""]
lines += ["## 1. Gemiddelde exposure (fractie van het kapitaal)", "", "| periode | aandelen | obligaties | goud | cash |", "|---|---|---|---|---|"]
E = {}
for lo, lbl in ((date(2001, 1, 1), "2001–24"), (date(2011, 1, 1), "2011–24"), (date(2021, 1, 1), "2021–24")):
    sel = (D >= lo) & (D <= DISC) & np.isfinite(expo["cash"])
    E[lbl] = {k: float(np.mean(v[sel])) for k, v in expo.items()}
    lines.append(f"| {lbl} | {E[lbl]['aandelen']:.2f} | {E[lbl]['obligaties']:.2f} | {E[lbl]['goud']:.2f} | {E[lbl]['cash']:.2f} |")
lines.append("\nStrateeg-aanname (VERWACHTING §2): aandelen 0,45 · obligaties 0,31 · goud 0,12 · cash 0,12.")

# ---- gerealiseerde excess per klasse per decennium ----
def excess_ann(name, lo, hi, field="adjclose", is_future=False):
    df = load_daily(name, field); c = df["close"]; dd = df["date"]
    sel = np.array([lo <= x <= hi for x in dd])
    idx = np.where(sel)[0]
    if len(idx) < 250:
        return float("nan")
    r = c[idx[1:]] / c[idx[:-1]] - 1
    nights = np.array([(dd[j] - dd[j - 1]).days for j in idx[1:]])
    rf = rf_on(list(dd[idx[1:]])) / 100 / 365 * nights
    ex = r if is_future else r - rf
    yrs = len(ex) / 252
    return (np.prod(1 + ex) ** (1 / yrs) - 1) * 100
lines += ["", "## 2. Gerealiseerde excess t.o.v. USD-cash (%/jr, meetkundig) per decennium", "",
          "| klasse (reeks) | 1990–99 | 2000–09 | 2010–19 | 2020–24 | forward laag/midden/hoog |", "|---|---|---|---|---|---|"]
for lbl, name, fut, pk in (("aandelen (SPX_TR)", "SPX_TR", False, "aandelen"), ("obligaties (BOND10_SYN)", "BOND10_SYN", False, "obligaties"),
                           ("goud (GOLD_F, future = al excess)", "GOLD_F", True, "goud")):
    vals = [excess_ann(name, date(a, 1, 1), date(b, 12, 31), is_future=fut) for a, b in ((1990, 1999), (2000, 2009), (2010, 2019), (2020, 2024))]
    lines.append(f"| {lbl} | " + " | ".join("n.v.t." if not np.isfinite(v) else f"{v:+.1f}" for v in vals) + f" | {PREMIE[pk][0]:+.2f} / {PREMIE[pk][1]:+.2f} / {PREMIE[pk][2]:+.2f} |")

# ---- verwachting met echte exposures + Monte-Carlo ----
lines += ["", "## 3. Premie-verwachting met echte exposures (ongehefeld; kosten −0,20%/jr aangenomen)", "",
          "| exposures | scenario | excess/jr | alfa €/mnd | + EUR-cash (€STR {:.2f}%) | + USD-cash ({:.2f}%) |".format(ESTR, USD3M), "|---|---|---|---|---|---|"]
for lbl in ("2001–24", "2021–24"):
    for j, sc in enumerate(("laag", "midden", "hoog")):
        ex = sum(E[lbl][k] * PREMIE[k][j] for k in PREMIE) - COST
        a = 80000 * ex / 100 / 12
        lines.append(f"| {lbl} | {sc} | {ex:+.2f}% | €{a:,.0f} | €{a + 80000*ESTR/100/12:,.0f} | €{a + 80000*USD3M/100/12:,.0f} |")
rng = np.random.default_rng(75); N = 200000
lines += ["", "## 4. Monte-Carlo (exposures 2001–24 en 2021–24; premies ~ N(midden, SE); EUR-cash vast op €STR)", "",
          "| exposures | variant | p(totaal ≥ €400) | p(alfa ≥ €287) | mediaan totaal €/mnd | 5–95% totaal |", "|---|---|---|---|---|---|"]
for lbl in ("2001–24", "2021–24"):
    for vname, se, rho, horizon_noise in (("parameteronzekerheid, SE 2%", 2.0, 0.0, False), ("parameteronzekerheid, SE 3%", 3.0, 0.0, False),
                                          ("SE 2,5%, corr 0,3", 2.5, 0.3, False), ("SE 2,5% + gerealiseerd 10-jr-gemiddelde (vol 6,1%)", 2.5, 0.0, True)):
        C = np.full((3, 3), rho); np.fill_diagonal(C, 1.0); L = np.linalg.cholesky(C * se ** 2)
        mu = np.array([PREMIE[k][1] for k in ("aandelen", "obligaties", "goud")])
        prem = mu + rng.standard_normal((N, 3)) @ L.T
        ex = prem @ np.array([E[lbl][k] for k in ("aandelen", "obligaties", "goud")]) - COST
        if horizon_noise:
            ex = ex + rng.standard_normal(N) * 6.1 / math.sqrt(10)
        alfa = 80000 * ex / 100 / 12; tot = alfa + 80000 * ESTR / 100 / 12
        lines.append(f"| {lbl} | {vname} | {np.mean(tot >= 400)*100:.1f}% | {np.mean(alfa >= 287)*100:.1f}% | €{np.median(tot):,.0f} | €{np.percentile(tot,5):,.0f}–{np.percentile(tot,95):,.0f} |")
lines += ["", "Lezing: exposures en premies zijn de enige invoer; het resultaat is zo goed als de premie-aannames (web-claims, VERWACHTING.md). "
          "Geen haircut toegepast (premies zijn al forward-verwachtingen, geen backtest)."]
open("results/port/QA_exposures_MC.md", "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
