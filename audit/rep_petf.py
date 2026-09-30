"""AUDIT_1 — onafhankelijke herimplementatie P-ETF-a (C52 lang + C02, maandelijks 1/sigma, ETF-vehikel 13 bp rondreis / TER 0,07% / excess t.o.v. cash).
Uit ruwe data/daily/*.csv, pandas, eigen code. Geen import van engine/ of catalogus/. Specificatie uit PREREG_PORT.md + ENGINE_TEMPLATE (niet uit de code).
Opties voor gevoeligheidsanalyse: lag (signaaluitvoering +lag handelsdagen), bond (syn|ief|own), rf-bron, kosten."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, ".")
from audit.common import load, rf_daily_pct

RT_BP, TER = 13.0, 0.0007
START_C52, END = 2001, pd.Timestamp("2024-12-31")

def rf_series(kind="dtb3"):
    if kind == "dtb3":
        s = rf_daily_pct()
        ext = load("YLD_US3M", "close")
        ext = ext[ext.index > s.index[-1]]
        s = pd.concat([s, ext])
    elif kind == "irx":
        s = load("IRX_3M", "close")
    elif kind == "us3m":
        s = load("YLD_US3M", "close")
    return s[~s.index.duplicated()].sort_index()

def rf_fac(idx, rf, nights):
    """rendementsfactor per periode: (rente laatste bekende waarde op d_{t-1} ... ) - eigen keuze: rente op dag t (zoals spec 'laatste bekende waarde op dag t')."""
    r = rf.reindex(rf.index.union(idx)).ffill().reindex(idx)
    return (r / 100 / 365 * nights).values

def nights_of(idx):
    d = pd.Series(idx).diff().dt.days.fillna(0).values
    return d

def own_bond(D=8.0, C=80.0):
    y = load("TNX_10Y", "close") / 100
    dy = y.diff(); cd = pd.Series(y.index, index=y.index).diff().dt.days
    r = y.shift() * cd / 365 - D * dy + 0.5 * C * dy ** 2
    return (1 + r.fillna(0)).cumprod()

def c02_sleeve(rf, lag=0, rt_bp=RT_BP, ter=TER, signal_price_tr=False):
    """5 indices; signaal: slot(maandeinde) > gemiddelde laatste 10 maandeinde-sloten (prijsindex); rendement: SPX -> SPX_TR, overige prijsindex; long/cash."""
    cols = {}
    for nm in ["SPX", "NDX", "DJI", "DAX", "N225"]:
        px = load(nm, "close")
        pr = px.copy()
        ret_px = load("SPX_TR", "adjclose") if nm == "SPX" else px
        r = ret_px.pct_change()
        r = r.reindex(px.index)
        # SPX_TR kalender kan afwijken: reindex op SPX-dagen via cumulatieve factor
        if nm == "SPX":
            tr = load("SPX_TR", "adjclose"); trf = tr.reindex(tr.index.union(px.index)).ffill().reindex(px.index)
            r = trf.pct_change()
            r[px.index < tr.index[0]] = px.pct_change()[px.index < tr.index[0]]
        me = px.groupby([px.index.year, px.index.month]).tail(1).index
        ms = px.loc[me]; sma = ms.rolling(10).mean()
        sig = (ms > sma).astype(float); sig[sma.isna()] = np.nan
        tgt = pd.Series(np.nan, index=px.index); tgt.loc[me] = sig.values
        pos = tgt.ffill().fillna(0.0)
        if lag: pos = pos.shift(lag).fillna(0.0)
        pprev = pos.shift().fillna(0.0)
        turn = pos.diff().abs().fillna(pos.abs())
        nt = nights_of(px.index)
        rff = rf_fac(px.index, rf, nt)
        net = pprev * r.fillna(0.0) - turn * rt_bp / 2 * 1e-4 - pprev.abs() * ter / 365 * nt + (1 - pprev.abs()) * rff
        net[r.isna()] = np.nan
        cols[nm] = pd.DataFrame({"net": net, "pos": pos})
    net = pd.concat({k: v["net"] for k, v in cols.items()}, axis=1, sort=True)
    x = net.mean(axis=1, skipna=True).dropna()
    x = x[net.notna().any(axis=1)]
    return x, cols  # totaalrendement (kasrente zit erin); mean over beschikbare indices die dag

def c52_sleeve(rf, lag=0, rt_bp=RT_BP, ter=TER, bond="syn", assets=("SPY", "BOND", "GOLD"), scale_cap=1.0, tgt=0.08, quirk=False):
    px = {"SPY": load("SPY", "adjclose"), "GOLD": load("GOLD_F", "close")}
    px["BOND"] = own_bond() if bond in ("syn", "own") else load("IEF", "adjclose")
    if bond == "file":
        px["BOND"] = load("BOND10_SYN", "adjclose", "data/derived")
    px = {k: px[k] for k in assets}
    ret = {k: v.pct_change().dropna() for k, v in px.items()}
    cal = pd.DatetimeIndex(sorted(set().union(*[set(v.index) for v in px.values()])))
    me = pd.Series(cal, index=cal).groupby([cal.year, cal.month]).tail(1)  # maandeinde in gezamenlijke kalender
    if quirk:      # gedrag dat in de bestaande engine zit: asset met een gat in het 60d-venster valt die maand weg
        R = pd.DataFrame(ret).reindex(cal)
    else:          # schoon: prijzen doorgetrokken op gezamenlijke kalender (feestdag = 0-rendement)
        R = pd.DataFrame({k: v.reindex(cal).ffill().pct_change() for k, v in px.items()})
        R = R[R.index >= max(v.index[0] for v in px.values())]
        R = R.reindex(cal)
    W = {}
    cl = list(cal)
    meidx = set(me.index)
    for k, d in enumerate(cl):
        if d not in meidx or k < 61: continue
        win = R.iloc[k - 59:k + 1]      # 60 rendementen t/m slot van d (geen toekomst)
        av = [c for c in win.columns if not win[c].isna().any()]
        if len(av) < (2 if quirk else 3): continue
        win = win[av]
        sd = win.std(ddof=1) * np.sqrt(252); iv = 1 / sd; w = iv / iv.sum()
        cov = win.cov() * 252; sp = float(np.sqrt(w.values @ cov.values @ w.values))
        W[d] = (w * min(scale_cap, tgt / sp)).reindex(list(px)).fillna(0.0)
    Wd = pd.DataFrame(W).T.reindex(cal).ffill().fillna(0.0)
    if lag: Wd = Wd.shift(lag).fillna(0.0)
    out = 0
    parts = {}
    # elke asset op eigen kalender
    tot = pd.Series(0.0, index=cal); cashfrac_abs = pd.Series(0.0, index=cal)
    for k, s in px.items():
        idx = s.index; w = Wd[k].reindex(idx).ffill().fillna(0.0) if True else None
        # positie wordt gezet op slot van beslisdatum; posities op eigen kalender
        pos = Wd[k].reindex(idx, method="ffill").fillna(0.0)
        pprev = pos.shift().fillna(0.0); turn = pos.diff().abs().fillna(pos.abs())
        r = s.pct_change().fillna(0.0); nt = nights_of(idx)
        net = pprev * r - turn * rt_bp / 2 * 1e-4 - pprev.abs() * ter / 365 * nt
        tot = tot.add(net, fill_value=0.0); cashfrac_abs = cashfrac_abs.add(pprev.abs(), fill_value=0.0)
    nt = nights_of(cal); rff = rf_fac(cal, rf, nt)
    tot = tot + (1 - cashfrac_abs).clip(0, 1) * rff
    tot = tot[tot.index.year >= START_C52]
    return tot, Wd

def pipeline(rf, c02, c52, extra_cost_bp=6.5):
    """PREREG_PORT P-ETF-a: sleeves excess; weights ∝ 1/σ60 (vertraagd), maandelijks op eerste handelsdag; kost 6,5 bp × Σ|Δw|."""
    days = c02.index.intersection(c52.index).sort_values()
    nt = nights_of(days); rff = rf_fac(days, rf, nt)
    X = pd.DataFrame({"c52": c52.reindex(days).values - rff, "c02": c02.reindex(days).values - rff}, index=days)
    first = pd.Series(days.to_period("M"), index=days)
    reb = (first != first.shift()).values
    w = np.full((len(days), 2), np.nan); cur = None; cost = np.zeros(len(days))
    for i in range(len(days)):
        if reb[i] and i >= 60:
            s = X.iloc[i - 60:i].std(ddof=1).values * np.sqrt(252)
            new = (1 / s) / (1 / s).sum()
            if cur is not None: cost[i] = np.abs(new - cur).sum() * extra_cost_bp * 1e-4
            cur = new
        if cur is not None: w[i] = cur
    valid = ~np.isnan(w[:, 0])
    xa = (w * X.values).sum(axis=1) - cost
    xa = pd.Series(xa, index=days)[valid]; tot = xa + rff[valid]
    return xa, tot, pd.DataFrame(w, index=days)[valid], X

def stats(xa, tot, lo=None, hi=END):
    m = pd.Series(True, index=xa.index)
    if lo is not None: m &= xa.index >= pd.Timestamp(lo)
    m &= xa.index <= hi
    x, t = xa[m], tot[m]
    sr = x.mean() / x.std(ddof=0) * np.sqrt(252); eq = (1 + t).cumprod()
    return dict(start=str(x.index[0].date()), n=len(x), SR=sr, vol=x.std(ddof=0) * np.sqrt(252), CAGR=eq.iloc[-1] ** (252 / len(x)) - 1,
                maxDD=float((1 - eq / eq.cummax()).max()), mean_bp=x.mean() * 1e4)

def run(label, kind="dtb3", **kw):
    rf = rf_series(kind)
    quirk = kw.pop("quirk", False); lag = kw.pop("lag", 0); bond = kw.pop("bond", "syn"); rt = kw.pop("rt", RT_BP); ter = kw.pop("ter", TER)
    c02, _ = c02_sleeve(rf, lag=lag, rt_bp=rt, ter=ter); c52, _ = c52_sleeve(rf, lag=lag, rt_bp=rt, ter=ter, bond=bond, quirk=quirk)
    xa, tot, w, X = pipeline(rf, c02, c52, extra_cost_bp=rt / 2)
    s = stats(xa, tot); print(f"{label:38s} start {s['start']} n {s['n']} SR {s['SR']:.3f} vol {s['vol']*100:.2f}% CAGR {s['CAGR']*100:.2f}% maxDD {s['maxDD']*100:.2f}%")
    return xa, tot, w, X, c02, c52, s

if __name__ == "__main__":
    run("A. schoon (ffill-kalender), eigen bond", bond="own")
    run("B. engine-quirk (asset-drop), eigen bond", bond="own", quirk=True)
    run("C. engine-quirk, bond uit data/derived", bond="file", quirk=True)
