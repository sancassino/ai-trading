"""AUDIT_1 §3: onafhankelijke t-waarden voor C02-, C52L-sleeves en P-ETF-a (excess, ≤2024): gewoon, Newey-West L=5/21/63, maandelijks (niet-overlappend), stationaire blok-bootstrap, SR-SE en DSR."""
import sys; sys.path.insert(0, ".")
import numpy as np, pandas as pd
from scipy.stats import norm
from audit.rep_petf import *
rf = rf_series("dtb3")
c02, _ = c02_sleeve(rf); c52, _ = c52_sleeve(rf, bond="own", quirk=True)
ex = lambda s: s - pd.Series(rf_fac(s.index, rf, nights_of(s.index)), index=s.index)
xa, tot, w, X = pipeline(rf, c02, c52)
def nw(x, L):
    x = np.asarray(x, float); n = len(x); e = x - x.mean(); s = e @ e / n
    s += 2 * sum((1 - k / (L + 1)) * (e[k:] @ e[:-k] / n) for k in range(1, L + 1)); return x.mean() / np.sqrt(s / n)
def boot(x, blk, B=2000, seed=11):
    rng = np.random.default_rng(seed); x = np.asarray(x); n = len(x); m = []
    for _ in range(B):
        idx = []; 
        while len(idx) < n:
            st = rng.integers(0, n); L = rng.geometric(1 / blk); idx += [(st + j) % n for j in range(L)]
        m.append(x[idx[:n]].mean())
    return x.mean() / np.std(m, ddof=1)
def rep(label, x):
    x = x[(x.index >= "2001-04-02") & (x.index <= "2024-12-31")]
    mo = x.groupby([x.index.year, x.index.month]).sum()
    sr = x.mean() / x.std() * np.sqrt(252); yrs = len(x) / 252
    ac = [x.autocorr(k) for k in (1, 5, 21)]
    print(f"{label:16s} n={len(x)} SR={sr:.2f} | t plain {x.mean()/x.std()*np.sqrt(len(x)):.2f} | NW5 {nw(x,5):.2f} NW21 {nw(x,21):.2f} NW63 {nw(x,63):.2f} | maand-t {mo.mean()/mo.std()*np.sqrt(len(mo)):.2f} (n={len(mo)}) | boot21 {boot(x,21):.2f} boot63 {boot(x,63):.2f} | ac1/5/21 {ac[0]:.3f}/{ac[1]:.3f}/{ac[2]:.3f}")
    return sr, yrs
sr1, y1 = rep("C52 lang", ex(c52)); sr2, _ = rep("C02 (etf)", ex(c02)); sr3, _ = rep("P-ETF-a", xa)
# DSR (Bailey & López de Prado) met SR-SE uit jaren; N = 440 (TRIAL_COUNT), 26 (catalogus), 40 (eff.)
def dsr(sr, yrs, N, skew=0.0, kurt=3.0):
    se = np.sqrt((1 - skew * sr + (kurt - 1) / 4 * sr ** 2) / yrs)   # SR in jaareenheden, yrs = T jaren (benadering)
    g = 0.5772156649; sr0 = se * ((1 - g) * norm.ppf(1 - 1 / N) + g * norm.ppf(1 - 1 / (N * np.e)))
    return se, sr0, norm.cdf((sr - sr0) / se)
for lab, s, n in (("P-ETF-a", sr3, None), ("C52 lang", sr1, None)):
    for N in (8, 26, 40, 440):
        se, sr0, d = dsr(s, y1, N); print(f"DSR {lab:9s} N={N:4d}: SR {s:.2f}, SE {se:.2f}, SR0 {sr0:.2f} -> DSR {d:.3f}")
# korting: SR-SE en 90%-CI
se = np.sqrt((1 + sr3 ** 2 / 2) / y1); print(f"P-ETF-a: SR {sr3:.2f}  analytische SE {se:.2f}; 90%-CI {sr3-1.645*se:.2f}…{sr3+1.645*se:.2f}")
