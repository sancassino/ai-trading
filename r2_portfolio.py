"""R2 stap 4: sleeve-correlaties, vol-targeting (10%), samengestelde equity, vs benchmark. Ontdekking ≤ 2024. Geen trial (geen nieuwe signalen).
Sleeve-reeksen uit results/R2/series (engine-dump). Overschotrendement x; totaal = rf + k·x (hefboom financiert tegen rf; k ≤ KMAX)."""
import math, sys
import numpy as np
from datetime import date
from engine.run_rule import rf_on, load_daily
KMAX, TGT, W = 3.0, 0.10, 60
def load(name):
    d = {}
    for l in open(f"results/R2/series/{name}.csv"):
        if l[:1].isdigit():
            a = l.strip().split(";"); d[date.fromisoformat(a[0])] = (float(a[1]), float(a[2]))
    return d
def stats(x_ex, x_tot):
    n = len(x_ex); sr = x_ex.mean() / x_ex.std() * math.sqrt(252); eq = np.cumprod(1 + x_tot)
    dd = float(np.max(1 - eq / np.maximum.accumulate(eq))); cagr = eq[-1] ** (252 / n) - 1
    return dict(SR=sr, vol=x_ex.std() * math.sqrt(252), CAGR=cagr, maxDD=dd, Calmar=cagr / dd if dd > 0 else float("nan"), skew=float(((x_ex - x_ex.mean()) ** 3).mean() / x_ex.std() ** 3))
def voltarget(x, tgt=TGT, w=W, kmax=KMAX):
    """k_t = tgt / (vol_{t-w..t-1} · √252), geen lookahead (vertraagd), cap kmax."""
    out = np.zeros(len(x)); k = np.ones(len(x))
    for i in range(len(x)):
        if i >= w:
            v = x[i - w:i].std() * math.sqrt(252); k[i] = min(kmax, tgt / v) if v > 0 else 1.0
        out[i] = k[i] * x[i]
    return out, k
def combo(names, label, start, out):
    S = {n: load(n) for n in names}
    days = sorted(set.intersection(*[set(s) for s in S.values()]))
    days = [d for d in days if d >= start and d <= date(2024, 12, 31)]
    X = np.array([[S[n][d][0] for d in days] for n in names])
    rf = np.r_[0, [(b - a).days for a, b in zip(days[:-1], days[1:])]] * rf_on(days) / 100 / 365
    out.append(f"\n### {label}\nperiode {days[0]} → {days[-1]} ({len(days)} dagen); sleeves: {', '.join(names)}")
    C = np.corrcoef(X); out.append("correlatiematrix (overschotrendement, dagelijks):\n```\n" + "\n".join(f"{n[:34]:34s} " + " ".join(f"{c:+.2f}" for c in C[i]) for i, n in enumerate(names)) + "\n```")
    # gelijk-risico: elke sleeve op 10% vol (vertraagde 60d-vol), gemiddelde, daarna portefeuille op 10%
    sc = np.array([voltarget(X[i])[0] for i in range(len(names))]); avg = sc.mean(axis=0)
    p, k = voltarget(avg)
    st = stats(p, rf + p); out.append(f"portefeuille (sleeves elk 10% vol → gemiddelde → 10% vol, cap {KMAX}×): SR {st['SR']:.2f}, vol {st['vol']*100:.1f}%, CAGR {st['CAGR']*100:.1f}%, maxDD {st['maxDD']*100:.1f}%, Calmar {st['Calmar']:.2f}, skew {st['skew']:+.2f}; gem. hefboom {k.mean():.2f}")
    per_y = {}
    for d, v in zip(days, p): per_y.setdefault(d.year, []).append(v)
    out.append("per jaar (%, overschot bij 10% vol): " + " ".join(f"{y}:{sum(v)*100:+.1f}" for y, v in per_y.items()))
    dec = {}
    for d, v in zip(days, p): dec.setdefault(d.year // 10 * 10, []).append(v)
    out.append("SR per decennium: " + ", ".join(f"{a}s {np.mean(v)/np.std(v)*math.sqrt(252):+.2f}" for a, v in sorted(dec.items())))
    # benchmarks over dezelfde dagen, elk op 10% vol (vergelijkbaar) én ongeschaald
    for lab, wts in (("60/40 SPY/IEF" if days[0].year >= 2003 else "60/40 SPX/BOND10_SYN", {"SPY": .6, "IEF": .4} if days[0].year >= 2003 else {"SPX": .6, "BOND10_SYN": .4}), ("SPX buy-and-hold", {"SPX": 1.0})):
        R = {}
        for n, w in wts.items():
            df = load_daily(n, "adjclose"); r = np.r_[0.0, df["close"][1:] / df["close"][:-1] - 1]
            R[n] = dict(zip(df["date"], r))
        b = np.array([sum(w * R[n].get(d, 0.0) for n, w in wts.items()) for d in days]); bex = b - rf
        sb = stats(bex, b); bp, _ = voltarget(bex); sbp = stats(bp, rf + bp)
        out.append(f"benchmark {lab} (ongeschaald, prijs/adj): SR {sb['SR']:.2f}, vol {sb['vol']*100:.1f}%, CAGR {sb['CAGR']*100:.1f}%, maxDD {sb['maxDD']*100:.1f}%, Calmar {sb['Calmar']:.2f} | op 10% vol: SR {sbp['SR']:.2f}, CAGR {sbp['CAGR']*100:.1f}%, maxDD {sbp['maxDD']*100:.1f}%, Calmar {sbp['Calmar']:.2f}")
    return p, days, rf
if __name__ == "__main__":
    out = ["# R2 — portefeuillebouw (ontdekking ≤ 2024-12-31; reserve niet aangeraakt)", "Methode: zie r2_portfolio.py. Sleeve-reeksen = overschotrendement (x − rf) uit de engine per vehikel (etf/future). Hefboom (k>1) veronderstelt future/CFD-financiering tegen rf (in x al verwerkt via rf-aftrek; geen extra opslag → optimistisch bij k>1). Geen trial."]
    A = ["C54_carver__qa__future", "C52_allweather__lang__etf", "C02_faber__basis__etf", "C17_fomc_cycle__basis__etf"]
    combo(A, "P1: C54(qa) + C52(lang) + C02 + C17 (start 2001)", date(2001, 1, 1), out)
    combo(["C54_carver__qa__future", "C52_allweather__lang__etf"], "P2: C54(qa) + C52(lang) (start 2001)", date(2001, 1, 1), out)
    combo(["C54_carver__qa__future", "C02_faber__basis__etf", "C17_fomc_cycle__basis__etf"], "P3: C54(qa) + C02 + C17 (start 1994)", date(1994, 1, 1), out)
    combo(["C54_carver__qa__future", "C52_allweather__basis__etf", "C53_gem__basis__etf", "C02_faber__basis__etf", "C17_fomc_cycle__basis__etf", "rep_b2b_rsi2__basis__etf"], "P4: alle sleeves incl. GEM/RSI(2) (start 2003)", date(2003, 1, 1), out)
    open("results/R2/portefeuille.md", "w").write("\n".join(out) + "\n"); print("\n".join(out))
