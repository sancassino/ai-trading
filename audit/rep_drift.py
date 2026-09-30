"""AUDIT_1 — instrumentniveau-simulatie met MEEDRIJVENDE posities (geen dagelijkse herweging naar constante gewichten), eigen code.
Doel: toets de vereenvoudiging in PREREG_PORT §3 ('gewichten drijven niet mee'); PORT3 van het team geeft SR 0,86-0,91."""
import sys; sys.path.insert(0, ".")
import numpy as np, pandas as pd
from audit.rep_petf import *
from audit.common import load

def build(rf, rt_bp=13.0, ter_by=None, thresh=0.0, lag=0):
    ter_by = ter_by or {}
    c02, cols = c02_sleeve(rf, lag=lag); c52, Wd = c52_sleeve(rf, bond="own", lag=lag)
    xa, tot, w, X = pipeline(rf, c02, c52)
    cal = xa.index
    # instrument-rendementen op de kalender van de pipeline (ffill-prijzen), doelposities
    names = ["SPY","BOND","GOLD","SPX","NDX","DJI","DAX","N225"]
    px = {"SPY": load("SPY","adjclose"), "BOND": own_bond(), "GOLD": load("GOLD_F","close"),
          "SPX": load("SPX_TR","adjclose"), "NDX": load("NDX","close"), "DJI": load("DJI","close"), "DAX": load("DAX","close"), "N225": load("N225","close")}
    ful = pd.DatetimeIndex(sorted(set(cal)))
    R = pd.DataFrame({k: v.reindex(v.index.union(ful)).ffill().reindex(ful).pct_change() for k, v in px.items()}).fillna(0.0)
    # sleevegewichten (w) gelden voor rendement van dag i; posities (na slot i-1) uit sleeves
    P52 = Wd.reindex(ful, method="ffill").fillna(0.0).rename(columns={"SPY":"SPY","BOND":"BOND","GOLD":"GOLD"})
    P02 = pd.DataFrame({k: cols[k]["pos"].reindex(ful, method="ffill").fillna(0.0) / 5 for k in ["SPX","NDX","DJI","DAX","N225"]})
    W = w.reindex(ful).ffill()  # kolommen 0=c52, 1=c02
    T = pd.DataFrame(0.0, index=ful, columns=names)
    for k in ["SPY","BOND","GOLD"]: T[k] = P52[k].shift().fillna(0.0) * W[0]     # positie vastgesteld op slot i-1, gewicht ook (σ t/m i-1)
    for k in ["SPX","NDX","DJI","DAX","N225"]: T[k] = P02[k].shift().fillna(0.0) * W[1]
    T = T.fillna(0.0)
    nt = nights_of(ful); rff = rf_fac(ful, rf, nt)
    h = pd.Series(0.0, index=names); nav = 1.0; out = []; turn_tot = []; ntr = 0
    for i, d in enumerate(ful):
        # 1) rendement dag i op de posities aan het begin van de dag
        terc = sum(abs(h[k]) * ter_by.get(k, 0.0007) for k in names) / 365 * nt[i]
        gr = float((h * R.iloc[i]).sum()); cash = (1 - h.abs().sum()) * rff[i]
        Rp = gr + cash - terc
        out.append((d, Rp, cash))
        if 1 + Rp <= 0: break
        h = h * (1 + R.iloc[i]) / (1 + Rp)
        # 2) herbalanceren naar het doel voor de volgende dag (doel i+1 = T.iloc[i+1])
        if i + 1 < len(ful):
            tgt = T.iloc[i + 1]; diff = tgt - h
            mask = diff.abs() >= thresh if thresh > 0 else diff.abs() > 1e-12
            trade = diff.where(mask, 0.0); c = trade.abs().sum() * rt_bp / 2 * 1e-4
            h = h + trade; ntr += int((trade.abs() > 1e-9).sum()); turn_tot.append(trade.abs().sum())
            h = h * (1 - c) if False else h
            out[-1] = (d, Rp - c, cash)   # kosten direct in de dagrekening
    o = pd.DataFrame(out, columns=["d", "tot", "cash"]).set_index("d")
    x = o.tot - pd.Series(rff, index=ful)[o.index]
    x = x[x.index >= xa.index[0]]; t = o.tot[x.index]
    yrs = len(x) / 252
    return x, t, ntr / yrs, np.sum(turn_tot) / yrs

if __name__ == "__main__":
    rf = rf_series("dtb3")
    for lab, kw in (("drift, drempel 0", {}), ("drift, drempel 1% van NAV", {"thresh": 0.01}), ("drift, drempel 2%", {"thresh": 0.02})):
        x, t, ntr, turn = build(rf, **kw); s = stats(x, t)
        print(f"{lab:28s} SR {s['SR']:.3f} CAGR {s['CAGR']*100:.2f}% maxDD {s['maxDD']*100:.2f}% ; trades/jr {ntr:.0f} omloop/jr {turn:.2f}")
