"""AUDIT_1 §3: alfa of bètapremie? Regressie (dagelijks, HAC-NW L=21) van excess-rendement op (a) gelijkgewogen B&H van dezelfde 5 indices, (b) 60/40 SPY/obligatie."""
import sys; sys.path.insert(0, ".")
import numpy as np, pandas as pd, statsmodels.api as sm
import audit.rep_petf as R
from audit.common import load
rf = R.rf_series("dtb3"); c02, cols = R.c02_sleeve(rf); c52, _ = R.c52_sleeve(rf, bond="own", quirk=True)
xa, tot, w, X = R.pipeline(rf, c02, c52)
ex = lambda s: s - pd.Series(R.rf_fac(s.index, rf, R.nights_of(s.index)), index=s.index)
r = {}
for nm in ["SPX", "NDX", "DJI", "DAX", "N225"]:
    px = load(nm, "close"); rr = px.pct_change()
    if nm == "SPX":
        tr = load("SPX_TR", "adjclose").pct_change().reindex(px.index); rr = tr.where(tr.notna(), rr)
    nt = R.nights_of(px.index); r[nm] = rr - R.rf_fac(px.index, rf, nt) - 0.0007 / 365 * nt
bh5 = pd.concat(r, axis=1, sort=True).mean(axis=1, skipna=True)
spy = load("SPY", "adjclose").pct_change(); bond = R.own_bond().pct_change()
idx = spy.index.union(bond.index); nt = R.nights_of(idx); rfd = pd.Series(R.rf_fac(idx, rf, nt), index=idx)
b6040 = (0.6 * spy.reindex(idx).fillna(0) + 0.4 * bond.reindex(idx).fillna(0)) - rfd
def reg(y, x, lab, lo="2001-04-02", hi="2024-12-31"):
    j = pd.concat([y, x], axis=1, keys=["y", "x"], sort=True).dropna(); j = j[(j.index >= lo) & (j.index <= hi)]
    m = sm.OLS(j.y, sm.add_constant(j.x)).fit(cov_type="HAC", cov_kwds={"maxlags": 21})
    print(f"{lab:48s} alfa {m.params['const']*252*100:5.2f}%/jr  t(alfa,NW21) {m.tvalues['const']:5.2f}  beta {m.params['x']:.2f}  R2 {m.rsquared:.2f}  n={len(j)}")
reg(ex(c02), bh5, "C02 (etf) vs gelijkgew. B&H 5 indices")
reg(ex(c52), b6040, "C52 lang vs 60/40 SPY/obl")
reg(xa, b6040, "P-ETF-a vs 60/40 SPY/obl")
reg(xa, bh5, "P-ETF-a vs B&H 5 indices")
j = pd.concat([xa, b6040], axis=1, keys=["p", "b"], sort=True).dropna(); j = j[(j.index >= "2001-04-02") & (j.index <= "2024-12-31")]
sr = lambda x: x.mean() / x.std() * np.sqrt(252); print("SR P-ETF-a", round(sr(j.p), 3), "| SR 60/40 (zelfde dagen)", round(sr(j.b), 3))
