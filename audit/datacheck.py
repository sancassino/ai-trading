import numpy as np, pandas as pd, sys
sys.path.insert(0, ".")
from audit.common import *
g = load("GOLD_F", "close"); gl = load("GLD", "adjclose")
r = g.pct_change().dropna(); print("GOLD_F n", len(r), "max |r|", r.abs().max(), "start", g.index[0])
print("GOLD_F grootste dagen:\n", r.abs().sort_values().tail(6))
j = pd.concat([g, gl], axis=1, keys=["g", "gld"]).dropna()
yrs = (j.index[-1] - j.index[0]).days / 365.25
print("periode", j.index[0].date(), j.index[-1].date())
for c in ("g", "gld"):
    print(c, "CAGR", (j[c].iloc[-1] / j[c].iloc[0]) ** (1 / yrs) - 1)
# t/m 2024
k = j[:"2024-12-31"]; yrs = (k.index[-1] - k.index[0]).days / 365.25
for c in ("g", "gld"):
    print("<=2024", c, "CAGR", (k[c].iloc[-1] / k[c].iloc[0]) ** (1 / yrs) - 1)
# daily correlation, tracking diff
rr = j.pct_change().dropna(); print("corr", rr.corr().iloc[0, 1], "diff ann mean", (rr.g - rr.gld).mean() * 252)
# jaarverschil
y = rr.groupby(rr.index.year).apply(lambda d: pd.Series({"g": (1 + d.g).prod() - 1, "gld": (1 + d.gld).prod() - 1}))
y["diff"] = y.g - y.gld; print(y.round(3))
# TNX
t = load("TNX_10Y", "close"); print("TNX stats", t.describe()); dt = t.diff().abs().sort_values().tail(8); print(dt)
print(t["2003-01-01":"2003-12-31"].describe())
