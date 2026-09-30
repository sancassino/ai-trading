"""R2 (D-043 + D-047 pt 5): regime-stress (jaren 70/80/90, 2022), rolling-SR, DD-duur, live-haircut. Geen trial (geen nieuwe signalen). Ontdekking ≤ 2024."""
import math, importlib
import numpy as np
from datetime import date
from engine.run_rule import load_daily, rf_on
from engine.forward import series
import forward_portfolio as FP
DISC = date(2024, 12, 31)
def dstats(days, ex, tot):
    ex, tot = np.asarray(ex), np.asarray(tot); eq = np.cumprod(1 + tot); dd = float(np.max(1 - eq / np.maximum.accumulate(eq)))
    return ex.mean() / ex.std() * math.sqrt(252) if ex.std() > 0 else float("nan"), eq[-1] ** (252 / len(tot)) - 1, dd
def by_decade(days, ex, tot, title, out):
    out.append(f"\n**{title}**\n\n| periode | SR (overschot) | CAGR totaal | maxDD |\n|---|---|---|---|")
    groups = [("1970s", 1970, 1979), ("1980s", 1980, 1989), ("1990s", 1990, 1999), ("2000s", 2000, 2009), ("2010s", 2010, 2019), ("2020–24", 2020, 2024), ("2022", 2022, 2022), ("alles", 0, 9999)]
    for lab, a, b in groups:
        idx = [i for i, d in enumerate(days) if a <= d.year <= b and d <= DISC]
        if len(idx) < 200: continue
        s, c, dd = dstats([days[i] for i in idx], [ex[i] for i in idx], [tot[i] for i in idx]); out.append(f"| {lab} | {s:+.2f} | {c*100:+.1f}% | {dd*100:.1f}% |")
def dd_duration(tot):
    eq = np.cumprod(1 + tot); peak = np.maximum.accumulate(eq); under = eq < peak - 1e-12; best = cur = 0
    for u in under:
        cur = cur + 1 if u else 0; best = max(best, cur)
    return best
def rolling(ex, w=756):
    r = [ex[i - w:i].mean() / ex[i - w:i].std() * math.sqrt(252) for i in range(w, len(ex) + 1, 21)]
    return min(r), float(np.median(r)), r[-1]
def bench(days, wts):
    R = {}
    for n in wts:
        df = load_daily(n, "adjclose"); c = df["close"]; R[n] = dict(zip(df["date"][1:], c[1:] / c[:-1] - 1))
    nights = np.r_[0, [(b - a).days for a, b in zip(days[:-1], days[1:])]]; rf = rf_on(days) / 100 / 365 * nights
    tot = np.array([sum(w * R[n].get(d, 0.0) for n, w in wts.items()) for d in days]); return tot - rf, tot
out = ["# R2 — regime-stress, rolling-SR, DD-duur, live-haircut (D-043/D-047; ontdekking ≤ 2024-12-31; geen trial)", ""]
# 1. Regime-stress 1970–2000 met de langste proxies
out.append("## 1. Regime-stress: lange proxies (rente stijgend 1970–1981)\nAanname/beperking: SPX-prijsindex vóór 1988 zonder dividend (SPX_TR pas vanaf 1988) → aandelen in de jaren 70/80 onderschat (≈ 3–5%/jr); obligatie = synthetisch uit ^TNX (D=8, C=80); goud pas vanaf 2000 → geen 3e activum.")
mod = importlib.import_module("catalogus.C52_allweather"); R = mod.RULE
R["instrumenten"] = list(R["instrumenten"]) + ["SPX"]
R["varianten"]["s70"] = {"assets": ["SPX", "BOND10_SYN"], "start_jaar": 1970}
s = series("C52_allweather", "s70", "etf", start=date(1970, 1, 1), end=DISC)
days = sorted(s); ex = [s[d][0] for d in days]; tot = [s[d][1] for d in days]
by_decade(days, ex, tot, "C52 all-weather, 2-activa (SPX + obligatie, ∝ 1/σ60, vol-target 8%, geen hefboom; etf) vs 60/40", out)
bx, bt = bench(days, {"SPX": 0.6, "BOND10_SYN": 0.4})
out.append("\n60/40 SPX/BOND10_SYN (zelfde dagen):")
by_decade(days, bx, bt, "60/40", out)
for name, var, veh in (("C02 Faber (5 indices, etf)", "basis", "etf"),):
    ss = series("C02_faber", var, veh, end=DISC); dd_ = sorted(ss); by_decade(dd_, [ss[d][0] for d in dd_], [ss[d][1] for d in dd_], name + " — vanaf 1927", out)
ss = series("C54_carver", "basis", "future", end=DISC); dd_ = sorted(ss)
by_decade(dd_, [ss[d][0] for d in dd_], [ss[d][1] for d in dd_], "C54 Carver 'basis' (future; 1971→, FX-pegs/WTI-artefact-gevoelig!) — leest de jaren 70/80 met voorzichtigheid", out)
# 2. Portefeuilles: rolling SR, DD-duur, 2022, haircut
out.append("\n## 2. Portefeuilles (PREREG_PORT-methode, forward_portfolio.py; ontdekking)\n\n| portefeuille | SR | CAGR USD | maxDD | langste DD-duur (jaren) | rolling-3j-SR min / mediaan / laatste | 2022 | CAGR na haircut 30% / 50% | € per maand (na 30% / 50%, vóór box 3) |\n|---|---|---|---|---|---|---|---|---|")
P = FP.all_portfolios(); deferred = []
for p, (days, tot, x, lev) in P.items():
    m = np.array([d <= DISC for d in days]) & np.isfinite(tot); t = tot[m]; e = x[m]; dd_days = [d for d, k in zip(days, m) if k]
    eq = np.cumprod(1 + t); dd = float(np.max(1 - eq / np.maximum.accumulate(eq))); cagr = eq[-1] ** (252 / len(t)) - 1
    r22 = float(np.prod([1 + v for d, v in zip(dd_days, t) if d.year == 2022]) - 1); rs = rolling(e)
    out.append(f"| {p} | {e.mean()/e.std()*math.sqrt(252):.2f} | {cagr*100:.1f}% | {dd*100:.1f}% | {dd_duration(t)/252:.1f} | {rs[0]:+.2f} / {rs[1]:+.2f} / {rs[2]:+.2f} | {r22*100:+.1f}% | {cagr*70:.1f}% / {cagr*50:.1f}% | €{cagr*0.7*80000/12:,.0f} / €{cagr*0.5*80000/12:,.0f} |")
    if p in ("P-ETF-a", "P1"):
        deferred.append((dd_days, list(e), list(t), f"{p} per decennium"))
for a_ in deferred:
    by_decade(*a_, out)
open("results/R2/stress_haircut.md", "w").write("\n".join(out) + "\n"); print("\n".join(out))
