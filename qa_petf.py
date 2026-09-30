"""QA v24-1/2: decompositie P-ETF-a (PREREG_PORT) op de ontdekkingsset (≤ 2024-12-31; reserve niet aangeraakt). Geen trial, geen regelwijziging.
Varianten (alleen analyse): basis; zonder obligatiepoot (C52 lang = SPY + GOLD_F); C02 op prijsindex (geen SPX_TR); periodes; per decennium;
bijdrage per activum binnen C52 lang; haircut op totaal vs op excess + cash (M-012 optie C); cash-only nulbenchmark; alfa boven cash in €/mnd."""
import copy
import math
from datetime import date

import numpy as np

import engine.run_rule as E
import forward_portfolio as FP
from engine.forward import series

DISC = date(2024, 12, 31)
out = ["# QA P-ETF-a — decompositie (ontdekking ≤ 2024; reserve niet aangeraakt)", ""]


def with_variant(rule_mod, base, name, **over):
    import importlib
    m = importlib.import_module(f"catalogus.{rule_mod}")
    p = copy.deepcopy(m.RULE["varianten"][base]); p.update(over); m.RULE["varianten"][name] = p
    return name


def petf(S, lo=None, hi=DISC):
    days, P = FP.run_petf(S)
    tot, x, _ = P["P-ETF-a"]
    sel = np.array([(lo is None or d >= lo) and d <= hi for d in days]) & np.isfinite(tot)
    return np.array(days)[sel], tot[sel], x[sel]


def st(days, tot, x):
    eq = np.cumprod(1 + tot); dd = float(np.max(1 - eq / np.maximum.accumulate(eq))); yrs = len(tot) / 252
    cagr = eq[-1] ** (1 / yrs) - 1; ex_ann = (np.prod(1 + x)) ** (1 / yrs) - 1; cash_ann = cagr - ex_ann
    return dict(SR=x.mean() / x.std() * math.sqrt(252), vol=x.std() * math.sqrt(252), CAGR=cagr, EX=ex_ann, CASH=cash_ann, DD=dd, n=len(tot),
                start=days[0], end=days[-1])


def line(lbl, s):
    return (f"| {lbl} | {s['start']}→{s['end']} | {s['SR']:.2f} | {s['vol']*100:.1f}% | {s['CAGR']*100:.1f}% | {s['EX']*100:.1f}% | "
            f"{s['CASH']*100:.1f}% | {s['DD']*100:.1f}% |")


base = {"S_C52L": series("C52_allweather", "lang", "etf"), "S_C02": series("C02_faber", "basis", "etf")}
out += ["| variant | periode | SR (excess) | vol | CAGR totaal | excess/jr | cash/jr (≈ verschil) | maxDD |", "|---|---|---|---|---|---|---|---|"]
d, t, x = petf(base); s0 = st(d, t, x); out.append(line("**basis (PREREG_PORT)**", s0))
for lo, hi, lbl in ((date(2001, 1, 1), date(2010, 12, 31), "2001–2010"), (date(2011, 1, 1), DISC, "2011–2024")):
    out.append(line(f"basis {lbl}", st(*petf(base, lo, hi))))
for a, b in ((2001, 2010), (2011, 2020), (2021, 2024)):
    out.append(line(f"basis decennium {a}s" if b - a == 9 else f"basis {a}–{b}", st(*petf(base, date(a, 1, 1), date(b, 12, 31)))))
v = with_variant("C52_allweather", "lang", "qa_zonder_bond", assets=["SPY", "GOLD_F"])
nb = {"S_C52L": series("C52_allweather", v, "etf"), "S_C02": base["S_C02"]}
out.append(line("zonder obligatiepoot (C52 = SPY + goud)", st(*petf(nb))))
saved = dict(E.TR_PROXY); E.TR_PROXY.clear()
pi = {"S_C52L": base["S_C52L"], "S_C02": series("C02_faber", "basis", "etf")}
E.TR_PROXY.update(saved)
out.append(line("C02 op prijsindex (geen SPX_TR)", st(*petf(pi))))
only = {"S_C52L": base["S_C52L"], "S_C02": base["S_C52L"]}
out.append(line("alleen C52 lang (beide 'sleeves' = C52L)", st(*petf(only))))
only2 = {"S_C52L": base["S_C02"], "S_C02": base["S_C02"]}
out.append(line("alleen C02", st(*petf(only2))))

# bijdrage per activum binnen C52 lang (sleeve-niveau, som-aggregatie, zonder kasrente)
import catalogus.C52_allweather as C52
R = C52.RULE; p = R["varianten"]["lang"]
data = {n: E.load_daily(n, R.get("field", "adjclose")) for n in R["instrumenten"]}
pos = C52.positions_all(data, p)
out += ["", "**Bijdrage per activum binnen C52 lang (etf, ≤ 2024, jaarlijks gemiddeld, vóór kasrente):**", ""]
for n in p["assets"]:
    net, *_ = E.net_returns_vehicle(data[n], np.clip(np.nan_to_num(pos[n]), -1, 1), 1.0, "etf", False)
    sel = np.array([date(2001, 1, 1) <= dd <= DISC for dd in data[n]["date"]]) & np.isfinite(net)
    r = net[sel]; w = np.nan_to_num(pos[n])[sel]
    out.append(f"- {n}: gem. gewicht {w.mean():.2f}, bijdrage {r.mean()*252*100:+.2f}%/jr, SR van de bijdrage {r.mean()/r.std()*math.sqrt(252):+.2f}")

# haircut (M-012 optie C) en nulbenchmark
cap = 80000
ex, cash = s0["EX"], s0["CASH"]
rf_now_usd = float(E.rf_on([date(2026, 9, 29)])[0]) / 100
out += ["", "**Haircut en nulbenchmark (M-012 optie C; P-ETF-a basis, ontdekking):**", "",
        f"- Ontdekking: CAGR totaal {s0['CAGR']*100:.1f}% = excess ≈ {ex*100:.1f}% + cash ≈ {cash*100:.1f}% (USD-cash 2001–24).",
        f"- **A — haircut op totaal (D-054, conservatief):** 30–50% → {s0['CAGR']*0.5*100:.1f}–{s0['CAGR']*0.7*100:.1f}%/jr ≈ "
        f"€{cap*s0['CAGR']*0.5/12:,.0f}–{cap*s0['CAGR']*0.7/12:,.0f}/mnd.",
        f"- **B — haircut op excess + cash apart:** excess 30–50% korting → {ex*0.5*100:.1f}–{ex*0.7*100:.1f}%/jr = "
        f"€{cap*ex*0.5/12:,.0f}–{cap*ex*0.7/12:,.0f}/mnd **alfa boven cash**; plus cash in eigen valuta: bij USD-3m nu {rf_now_usd*100:.2f}% ≈ "
        f"€{cap*rf_now_usd/12:,.0f}/mnd (EUR-geldmarkt is lager; ESTR niet in de repo — nog op te halen).",
        f"- **Nulbenchmark cash-only:** ≈ €{cap*rf_now_usd/12:,.0f}/mnd (USD-3m nu) — elk resultaat eerst hiermee vergelijken.",
        "- Lezing: het beoordelingsgetal is de **alfa boven cash**; de totale €/mnd hangt sterk van het renteniveau af."]
open("results/port/QA_PETF_decompositie.md", "w").write("\n".join(out) + "\n")
print("\n".join(out))
