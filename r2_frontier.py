"""R2 (D-062): rendement–DD-frontier voor P-ETF-a/b/+ : vol-doel 5–12% → CAGR, alfa boven cash, maxDD, p95-DD (5-jaars blok-bootstrap, 21d), DD-duur, financieringskosten, live-haircut-€/mnd.
Hefboom k = min(2, v/σ_P) (σ_P = 60d-vol van de ongehefelde P-ETF-a/+ , vertraagd, maandelijks); geleend deel (k−1)⁺ tegen rf + 1,5% (PREREG_PORT); k < 1 = rest in kas. Geen trial. Ontdekking ≤ 2024."""
import math
import numpy as np
from datetime import date
from engine.forward import series
from engine.run_rule import rf_on
import forward_portfolio as FP
DISC = date(2024, 12, 31); CAPITAL = 80000; ESTR = 0.0244
S = {k: series(*v, end=DISC) for k, v in FP.SLEEVES.items() if k in ("S_C52L", "S_C02", "S_C55")}
def base(names):
    d, o = FP.run_petf(S, names); tot, x, _ = o["P-ETF-a"]; ok = np.isfinite(x); return [dd for dd, k in zip(d, ok) if k], x[ok]
def level(days, xa, v, kmax=2.0):
    n = len(xa); nights = np.r_[0, [(b - a).days for a, b in zip(days[:-1], days[1:])]]; rf = rf_on(days) / 100 / 365 * nights
    k = np.zeros(n); cur = None; h = FP.HALF_RT["etf"]; x = np.zeros(n); prev = None
    for i in range(n):
        if i >= 60 and (i == 60 or days[i].month != days[i - 1].month):
            sp = xa[i - 60:i].std() * math.sqrt(252); cur = min(kmax, v / sp) if sp > 0 else 1.0
        kk = cur if cur is not None else 1.0
        x[i] = kk * xa[i] - (abs(kk - prev) * h if prev is not None else 0) - max(kk - 1, 0) * FP.SURCHARGE / 365 * nights[i]
        prev = kk; k[i] = kk
    return k, x, rf + x, rf
def p95dd(tot, rng, n=1260, B=1500, blk=21):
    N = len(tot); res = []
    for _ in range(B):
        st = rng.integers(0, N, n // blk + 1); idx = ((st[:, None] + np.arange(blk)).ravel() % N)[:n]; eq = np.cumprod(1 + tot[idx]); res.append(np.max(1 - eq / np.maximum.accumulate(eq)))
    return float(np.percentile(res, 95))
def dd_dur(t):
    eq = np.cumprod(1 + t); u = eq < np.maximum.accumulate(eq) - 1e-12; b = c = 0
    for z in u:
        c = c + 1 if z else 0; b = max(b, c)
    return b / 252
out = ["# R2 — rendement–drawdown-frontier (D-062; ontdekking ≤ 2024; geen trial)", "",
       "DD-budget (D-062): backtest-maxDD ≤ 20% **en** p95-DD (5-jaars blok-bootstrap) ≤ 25%. Alfa = geannualiseerd gemiddeld excess (na financieringsopslag); haircut op excess (D-055/D-060), EUR-cash (€STR 2,44% ≈ €163/mnd op €80k) apart. Hefboom ≤ 2× (PREREG_PORT §2).", ""]
rng = np.random.default_rng(11)
for lab, names in (("P-ETF-a/b (C52L + C02)", ["S_C52L", "S_C02"]), ("P-ETF+ (C52L + C02 + C55)", ["S_C52L", "S_C02", "S_C55"])):
    days, xa = base(names)
    out.append(f"## {lab} — {days[0]} → {days[-1]}\n\n| vol-doel | gem. hefboom | vol | alfa/jr | CAGR totaal (USD) | maxDD | p95-DD | langste DD (jr) | financieringsopslag €/jr | alfa boven cash €/mnd na haircut 30/40/50% | totaal €/mnd (+EUR-cash) 30/40/50% | binnen DD-budget |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
    for v in (0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.12):
        k, x, tot, rf = level(days, xa, v); e = x[60:]; t = tot[60:]; kk = k[60:]
        eq = np.cumprod(1 + t); dd = float(np.max(1 - eq / np.maximum.accumulate(eq))); cagr = eq[-1] ** (252 / len(t)) - 1
        alfa = e.mean() * 252; vol = e.std() * math.sqrt(252); pd_ = p95dd(t, rng); fin = np.mean(np.maximum(kk - 1, 0)) * FP.SURCHARGE * CAPITAL
        a3 = [alfa * (1 - h) * CAPITAL / 12 for h in (0.3, 0.4, 0.5)]; t3 = [alfa * (1 - h) * CAPITAL / 12 + ESTR * CAPITAL / 12 for h in (0.3, 0.4, 0.5)]
        out.append(f"| {v*100:.0f}% | {kk.mean():.2f} | {vol*100:.1f}% | {alfa*100:.1f}% | {cagr*100:.1f}% | {dd*100:.1f}% | {pd_*100:.1f}% | {dd_dur(t):.1f} | €{fin:,.0f} | €{a3[0]:.0f} / €{a3[1]:.0f} / €{a3[2]:.0f} | €{t3[0]:.0f} / €{t3[1]:.0f} / €{t3[2]:.0f} | {'JA' if dd <= 0.20 and pd_ <= 0.25 else 'nee'} |")
    out.append("")
out.append("Lezing: zie RUNLOG_R2 (D-062). Alle getallen zijn ontdekkings-uitkomsten van sleeves die ná zien van die data zijn gekozen (winnaarsvloek) en bevatten geen reserve-OOS.")
open("results/R2/frontier.md", "w").write("\n".join(out) + "\n"); print("\n".join(out))
