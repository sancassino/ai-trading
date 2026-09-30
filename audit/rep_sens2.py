import sys; sys.path.insert(0, ".")
import numpy as np, pandas as pd
from audit.rep_petf import *
rf = rf_series("dtb3")
def go(label, bond="own", assets=("SPY","BOND","GOLD"), c02on=True, lag=0, quirk=False, **kw):
    c02, _ = c02_sleeve(rf, lag=lag); c52, Wd = c52_sleeve(rf, bond=bond, assets=assets, quirk=quirk, lag=lag, **kw)
    if not c02on:
        xa = c52 - pd.Series(rf_fac(c52.index, rf, nights_of(c52.index)), index=c52.index); tot = c52
        xa = xa[xa.index >= "2001-04-02"]; tot = tot[xa.index]
        return xa, tot, None
    xa, tot, w, X = pipeline(rf, c02, c52); return xa, tot, w
def line(label, xa, tot, lo=None, hi="2024-12-31"):
    s = stats(xa, tot, lo, pd.Timestamp(hi)); print(f"{label:46s} {s['start']} SR {s['SR']:.3f} vol {s['vol']*100:.2f}% CAGR {s['CAGR']*100:.2f}% maxDD {s['maxDD']*100:.2f}%")
xa, tot, w = go("basis")
print("== periodes (schoon basis) ==")
for lo, hi in (("2001-01-01","2024-12-31"),("2001-01-01","2010-12-31"),("2011-01-01","2024-12-31"),("2021-01-01","2024-12-31"),("2002-11-01","2024-12-31"),("2015-01-01","2024-12-31")):
    line(f"{lo[:4]}–{hi[:4]}", xa, tot, lo, hi)
print("== per jaar (excess % / totaal %) ==")
y = pd.DataFrame({"x": xa, "t": tot}); g = y.groupby(y.index.year)
print(pd.DataFrame({"excess%": g.x.sum()*100, "tot%": g.t.apply(lambda s: ((1+s).prod()-1)*100)}).round(1).T.to_string())
print("== legs ==")
for lab, kw in (("zonder obligatiepoot (SPY+GOLD)", dict(assets=("SPY","GOLD"))), ("zonder goud (SPY+BOND)", dict(assets=("SPY","BOND"))), ("alleen SPY-risicoparity (n.v.t.)", None)):
    if kw is None: continue
    a, t, _ = go(lab, **kw); line("P-ETF-a " + lab, a, t)
a, t, _ = go("alleen C52", c02on=False); line("alleen C52 lang (sleeve, excess)", a, t)
c02, _ = c02_sleeve(rf); e = c02 - pd.Series(rf_fac(c02.index, rf, nights_of(c02.index)), index=c02.index); line("alleen C02 (sleeve, excess)", e[e.index>='2001-04-02'], c02[e.index>='2001-04-02'])
print("== bond echte IEF vs synthetisch, zelfde periode (vanaf 2002-11) ==")
a, t, _ = go("ief", bond="ief"); line("IEF", a, t, "2002-11-01"); a, t, _ = go("syn", bond="own"); line("synthetisch D8/C80", a, t, "2002-11-01")
a, t, _ = go("tlt", bond="own6"); line("synthetisch D6/C50", a, t, "2002-11-01")
