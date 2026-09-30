"""AUDIT_1: timing-luck — beslisdatum = maandeinde + s handelsdagen (s = -10..+15). Dezelfde regel, andere fase van het maandraster."""
import sys; sys.path.insert(0, ".")
import numpy as np, pandas as pd
from audit.rep_petf import *
rf = rf_series("dtb3")
ex = lambda s: s - pd.Series(rf_fac(s.index, rf, nights_of(s.index)), index=s.index)
rows = []
for sh in (-15, -10, -5, -3, -1, 0, 1, 3, 5, 10, 15):
    c02, _ = c02_sleeve(rf, shift=sh); c52, _ = c52_sleeve(rf, bond="own", shift=sh)
    xa, tot, w, X = pipeline(rf, c02, c52); a = stats(xa, tot)
    e2 = ex(c02); e2 = e2[(e2.index >= "2001-04-02") & (e2.index <= "2024-12-31")]; e5 = ex(c52); e5 = e5[(e5.index >= "2001-04-02") & (e5.index <= "2024-12-31")]
    sr = lambda x: x.mean() / x.std() * np.sqrt(252)
    rows.append((sh, sr(e2), sr(e5), a["SR"], a["CAGR"] * 100, a["maxDD"] * 100)); print(f"shift {sh:+3d}: C02 SR {sr(e2):.3f} | C52L SR {sr(e5):.3f} | P-ETF-a SR {a['SR']:.3f} CAGR {a['CAGR']*100:.2f}% maxDD {a['maxDD']*100:.2f}%")
r = np.array(rows); print("P-ETF-a SR min/med/max over shifts:", r[:,3].min().round(3), np.median(r[:,3]).round(3), r[:,3].max().round(3), "| C02:", r[:,1].min().round(3), r[:,1].max().round(3), "| C52L:", r[:,2].min().round(3), r[:,2].max().round(3))
