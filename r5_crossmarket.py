"""R5 — cross-market-replicatie C02 (Faber) + regionale C52 volgens PREREG_CAT5.md / S11. Ontdekking ≤ 2024-12-31. Eén trial (1 rij in TRIALS.csv)."""
import math, sys, os
import numpy as np
from datetime import date
from engine.run_rule import load_daily, rf_on, t_nw
END = date(2024, 12, 31); RT_HALF = 6.5e-4; TER = 0.0007; SEED = 2026; NREP = int(os.environ.get("NREP", 1000))
PRIMARY = {"FTSE": "Europa", "CAC40": "Europa", "AEX": "Europa", "SMI": "Europa", "IBEX": "Europa", "BEL20": "Europa", "TSX": "N-Amerika", "HSI": "Azië-Pacific", "STI": "Azië-Pacific",
           "AXJO": "Azië-Pacific", "KOSPI": "Azië-Pacific", "TWII": "Azië-Pacific"}
INFO = ["STOXX50", "NIFTY", "OMXS30"]; INSAMPLE = ["DAX", "N225", "SPX", "NDX", "DJI"]
# rf-bron per markt: (lijst van (reeks, lag_dagen, vanaf_datum) in volgorde), label
def series_csv(name):
    d, v = [], []
    for l in open(f"data/daily/{name}.csv"):
        if l[:1].isdigit():
            a = l.rstrip().split(";"); d.append(date.fromisoformat(a[0])); v.append(float(a[4]))
    return np.array(d, dtype="datetime64[D]"), np.array(v)
def ffill(name, dates, lag=0):
    ks, vs = series_csv(name); j = np.searchsorted(ks, np.array(dates, dtype="datetime64[D]") - np.timedelta64(lag, "D"), side="right") - 1
    return np.where(j >= 0, vs[np.clip(j, 0, None)], np.nan), ks[0]
def local_rf(m, dates):
    """(rf %/jr per datum, label)"""
    usd = rf_on(dates); dts = np.array(dates, dtype="datetime64[D]")
    def mix(primary, start, lab):
        p, _ = primary; ok = np.isfinite(p) & (dts >= np.datetime64(start)); return np.where(ok, p, usd), lab
    if m in ("CAC40", "AEX", "IBEX", "BEL20", "DAX", "STOXX50"):
        return mix(ffill("YLD_EURIBOR3M", dates, 31), date(1994, 1, 1), "Euribor 3m (1994→), daarvoor USD-rf (benaderd)")
    if m == "FTSE":
        return mix(ffill("YLD_UK_BANKRATE", dates), date(1975, 1, 2), "BoE Bank Rate")
    if m == "SMI":
        a, _ = ffill("YLD_CHF_LIBOR3M", dates, 31); b, _ = ffill("YLD_CHF_SARON", dates, 31); p = np.where(dts <= np.datetime64("2021-12-31"), a, b)
        return mix((p, None), date(1989, 1, 1), "CHF-Libor 3m (1989–2021) / SARON, daarvoor USD-rf (benaderd)")
    if m == "TSX":
        return mix(ffill("YLD_CAD_TBILL3M", dates, 7), date(2000, 1, 4), "BoC 3m T-bill (2000→), daarvoor USD-rf (benaderd)")
    if m == "N225":
        return mix(ffill("YLD_JPY_TONA", dates, 31), date(1992, 1, 1), "JPY TONA (1992→), daarvoor USD-rf (benaderd)")
    return usd, "USD-rf (benaderd; geen lokale rente)"
FX = {"FTSE": ("FX_GBPUSD", False), "SMI": ("FX_USDCHF", True), "TSX": ("FX_USDCAD", True), "AXJO": ("FX_AUDUSD", False), "CAC40": ("FX_EURUSD", False), "AEX": ("FX_EURUSD", False),
      "IBEX": ("FX_EURUSD", False), "BEL20": ("FX_EURUSD", False), "HSI": (None, False), "DAX": ("FX_EURUSD", False), "N225": ("FX_USDJPY", True), "STOXX50": ("FX_EURUSD", False)}
def fx_on(m, dates):
    if m not in FX: return None
    nm, inv = FX[m]
    if nm is None: return np.ones(len(dates))
    d = load_daily(nm, "close"); ks = np.array(d["date"], dtype="datetime64[D]"); j = np.searchsorted(ks, np.array(dates, dtype="datetime64[D]"), side="right") - 1
    v = np.where(j >= 0, np.asarray(d["close"])[np.clip(j, 0, None)], np.nan); return 1 / v if inv else v
def load_market(m):
    df = load_daily(m, "close"); keep = np.array([d <= END for d in df["date"]]); d = np.array(df["date"])[keep]; c = np.asarray(df["close"])[keep]
    r = np.r_[0.0, c[1:] / c[:-1] - 1]; nights = np.r_[0, [(b - a).days for a, b in zip(d[:-1], d[1:])]]
    rf, lab = local_rf(m, list(d)); rfd = rf / 100 / 365 * nights
    return dict(name=m, dates=d, c=c, r=r, rfd=rfd, rflabel=lab)
def month_end_idx(dates):
    ym = np.array([x.year * 12 + x.month for x in dates]); return list(np.where(np.r_[ym[1:] != ym[:-1], True])[0])
def faber(r, rfd, rebal, ter=TER, nwin=10):
    n = len(r); P = np.cumprod(1 + r); pos = np.zeros(n)
    for j in range(nwin - 1, len(rebal)):
        i = rebal[j]; nxt = rebal[j + 1] if j + 1 < len(rebal) else n; pos[i:nxt] = 1.0 if P[i] > P[rebal[j - nwin + 1:j + 1]].mean() else 0.0
    pp = np.r_[0.0, pos[:-1]]; turn = np.abs(pos - np.r_[0.0, pos[:-1]])
    x = pp * (r - rfd) - turn * RT_HALF - pp * ter / 252
    return x, pos
def bh(r, rfd, ter=TER):
    return (r - rfd) - ter / 252
def sr(x): return x.mean() / x.std() * math.sqrt(252) if len(x) > 30 and x.std() > 0 else float("nan")
def maxdd(x, rfd):
    eq = np.cumprod(1 + x + rfd); return float(np.max(1 - eq / np.maximum.accumulate(eq)))
def stationary_idx(L, rng, mean_block=252):
    starts = rng.integers(0, L, L); nb = rng.random(L) < 1 / mean_block; nb[0] = True
    bid = np.cumsum(nb) - 1; first = np.where(nb)[0]; return (starts[nb][bid] + (np.arange(L) - first[bid])) % L
def main():
    rng = np.random.default_rng(SEED); out = ["# R5 — cross-market-replicatie C02 (Faber) en regionale C52 (PREREG_CAT5; ontdekking ≤ 2024; lokale valuta tenzij anders vermeld)", ""]
    M = {m: load_market(m) for m in list(PRIMARY) + INFO + INSAMPLE if os.path.exists(f"data/daily/{m}.csv")}
    # ---- Regel A: exact (maandeinde) per markt
    res = {}
    for m, D in M.items():
        me = month_end_idx(D["dates"]); xf, pos = faber(D["r"], D["rfd"], me); xb = bh(D["r"], D["rfd"])
        ok = np.ones(len(xf), bool)
        # begin pas na het 10e maandeinde (SMA beschikbaar): B&H op dezelfde dagen
        start = me[9] + 1; sl = slice(start, None)
        res[m] = dict(dates=D["dates"][sl], xf=xf[sl], xb=xb[sl], rfd=D["rfd"][sl], SRf=sr(xf[sl]), SRb=sr(xb[sl]), DDf=maxdd(xf[sl], D["rfd"][sl]), DDb=maxdd(xb[sl], D["rfd"][sl]), t=t_nw(xf[sl] - xb[sl]),
                      invested=float(pos[sl].mean()), label=D["rflabel"], years=len(xf[sl]) / 252, first=D["dates"][start])
    def row(m, tag=""):
        r_ = res[m]; return f"| {m}{tag} | {r_['first']}→{END} ({r_['years']:.0f} jr) | {r_['SRf']:+.2f} | {r_['SRb']:+.2f} | {r_['SRf']-r_['SRb']:+.2f} | {r_['DDf']*100:.0f}% | {r_['DDb']*100:.0f}% | {(r_['DDf']-r_['DDb'])*100:+.0f} pp | {r_['t']:+.2f} | {r_['invested']*100:.0f}% | {r_['label']} |"
    hdr = "| markt | periode | SR Faber | SR B&H | ΔSR | maxDD Faber | maxDD B&H | ΔmaxDD | NW-t (Faber−B&H) | % belegd | rf-bron |\n|---|---|---|---|---|---|---|---|---|---|---|"
    out += ["## Regel A — C02 Faber (maandeinde-uitvoering; SR op excess boven lokale/USD-rf; kosten 13 bp/TER 0,07%)", "", "**Primaire markten (tellen mee)**", "", hdr] + [row(m) for m in PRIMARY if m in res]
    out += ["", "**Informatief (< 20 jr) en in-sample (tellen niet mee)**", "", hdr] + [row(m, " (info)") for m in INFO if m in res] + [row(m, " (in-sample)") for m in INSAMPLE if m in res]
    prim = [m for m in PRIMARY if m in res]; dSR = np.array([res[m]["SRf"] - res[m]["SRb"] for m in prim]); dDD = np.array([res[m]["DDf"] - res[m]["DDb"] for m in prim])
    npos = int(sum(res[m]["SRf"] > 0 for m in prim)); ndd = int((dDD < 0).sum()); pooled = float(dSR.mean())
    # ---- jaar-blok-bootstrap CI gepoold
    years = sorted({d.year for m in prim for d in res[m]["dates"]}); byyear = {m: {y: np.array([d.year == y for d in res[m]["dates"]]) for y in years} for m in prim}
    bs = []
    for _ in range(2000):
        ys = rng.choice(years, len(years)); dl = []
        for m in prim:
            xf = np.concatenate([res[m]["xf"][byyear[m][y]] for y in ys]); xb = np.concatenate([res[m]["xb"][byyear[m][y]] for y in ys])
            if len(xf) > 500: dl.append(sr(xf) - sr(xb))
        if dl: bs.append(np.mean(dl))
    ci = np.percentile(bs, [5, 95])
    # ---- pre-1990
    pre = []
    for m in prim:
        s = np.array([d < date(1990, 1, 1) for d in res[m]["dates"]])
        if s.sum() > 750: pre.append((m, sr(res[m]["xf"][s]) - sr(res[m]["xb"][s]), maxdd(res[m]["xf"][s], res[m]["rfd"][s]) - maxdd(res[m]["xb"][s], res[m]["rfd"][s])))
    # ---- nulkalibratie (21-daagse benadering; alle 12 primaire markten, gedeelde getrokken dagen)
    U = sorted({d for m in prim for d in M[m]["dates"]}); pos_u = {d: i for i, d in enumerate(U)}; L = len(U)
    R = {m: np.full(L, np.nan) for m in prim}; F = {m: np.full(L, np.nan) for m in prim}
    for m in prim:
        ix = np.array([pos_u[d] for d in M[m]["dates"]]); R[m][ix] = M[m]["r"]; F[m][ix] = M[m]["rfd"]; R[m][ix[0]] = np.nan
    def dsr_path(r, f):
        x, _ = faber(r, f, list(range(0, len(r), 21))); b = bh(r, f); s0 = 210; return sr(x[s0:]) - sr(b[s0:]), maxdd(x[s0:], f[s0:]) - maxdd(b[s0:], f[s0:])
    obs = [dsr_path(M[m]["r"], M[m]["rfd"]) for m in prim]; obs_pool = float(np.nanmean([o[0] for o in obs])); obs_dd = float(np.nanmean([o[1] for o in obs]))
    nullp, nulldd = [], []
    for k in range(NREP):
        idx = stationary_idx(L, rng); ds, dd = [], []
        for m in prim:
            rr = R[m][idx]; ff = F[m][idx]; v = np.isfinite(rr)
            if v.sum() < 1500: continue
            a, b = dsr_path(rr[v], ff[v]); ds.append(a); dd.append(b)
        nullp.append(np.nanmean(ds)); nulldd.append(np.nanmean(dd))
    nullp = np.array(nullp); p = float((nullp >= obs_pool).mean()); pdd = float((np.array(nulldd) <= obs_dd).mean())
    out += ["", "## Gepoold (12 primaire markten) en beslisregel (PREREG_CAT5)", "",
            f"- gepoold ΔSR (exact, maandeinde): **{pooled:+.3f}**; 90%-BI (jaar-blok-bootstrap, 2.000×): {ci[0]:+.2f} … {ci[1]:+.2f}",
            f"- markten met netto SR(excess) Faber > 0: **{npos}/12** (eis ≥ 8); markten met ΔmaxDD < 0: **{ndd}/12** (eis ≥ 9); gem. ΔmaxDD {dDD.mean()*100:+.1f} pp; gemiddelde SR Faber {np.mean([res[m]['SRf'] for m in prim]):+.2f} vs B&H {np.mean([res[m]['SRb'] for m in prim]):+.2f}",
            f"- **nul-kalibratie** ({NREP} replica's, 21-daagse benadering): waargenomen gepoold ΔSR {obs_pool:+.3f} (benadering); nul-verdeling gemiddeld {nullp.mean():+.3f} (sd {nullp.std():.3f}, 5–95%: {np.percentile(nullp,5):+.3f} … {np.percentile(nullp,95):+.3f}); **p (eenzijdig) = {p:.3f}**",
            f"- nul-kalibratie voor ΔmaxDD: waargenomen gem. {obs_dd*100:+.1f} pp vs nul gem. {np.mean(nulldd)*100:+.1f} pp; aandeel nulpaden met ≥ zo grote DD-reductie: {pdd:.3f} (informatief: DD-reductie is grotendeels mechanica van het filter)"]
    replic = pooled > 0 and p <= 0.10 and npos >= 8 and ndd >= 9
    lowpow = ci[0] < 0 < 0.3 < ci[1]
    label = "GEREPLICEERD" if replic else ("niet gerepliceerd op SR, alleen DD-beschermend" if ndd >= 9 else "niet gerepliceerd; DD-bescherming ook niet in ≥ 9/12")
    if not replic and lowpow: label += " — en 'onvoldoende power' (90%-BI omvat 0 én +0,3)"
    out += [f"- **Label (vooraf vastgelegde beslisregel): {label}**", "", "**Pre-1990 ('andere tijd', apart):** " + ("; ".join(f"{m}: ΔSR {a:+.2f}, ΔmaxDD {b*100:+.0f} pp" for m, a, b in pre) + f"; gemiddeld ΔSR {np.mean([a for _, a, _ in pre]):+.2f} over {len(pre)} markten" if pre else "n.v.t.")]
    # per decennium ΔSR
    out += ["", "**ΔSR (Faber − B&H) per decennium per primaire markt**", "", "| markt | 1980s | 1990s | 2000s | 2010s | 2020–24 |", "|---|---|---|---|---|---|"]
    for m in prim:
        cells = []
        for a, b in ((1980, 1989), (1990, 1999), (2000, 2009), (2010, 2019), (2020, 2024)):
            s = np.array([a <= d.year <= b for d in res[m]["dates"]]); cells.append(f"{sr(res[m]['xf'][s])-sr(res[m]['xb'][s]):+.2f}" if s.sum() > 500 else "–")
        out.append(f"| {m} | " + " | ".join(cells) + " |")
    # gevoeligheid TER 0,20%
    tsens = []
    for m in prim:
        D = M[m]; me = month_end_idx(D["dates"]); xf, _ = faber(D["r"], D["rfd"], me, ter=0.0020); xb = bh(D["r"], D["rfd"], ter=0.0020); s0 = me[9] + 1; tsens.append(sr(xf[s0:]) - sr(xb[s0:]))
    out.append(f"\n**Gevoeligheid TER 0,20%:** gepoold ΔSR {np.mean(tsens):+.3f} (basis {pooled:+.3f}).")
    # ---- USD-rij
    out += ["", "## USD-rij (Regel A; equity in USD via FX uit D2, USD-rf; HSI: HKD-peg = lokaal)", "", "| markt | periode | SR Faber | SR B&H | ΔSR | maxDD Faber | maxDD B&H |", "|---|---|---|---|---|---|---|"]
    usd_d = []
    for m in prim:
        fx = fx_on(m, list(M[m]["dates"]))
        if fx is None: continue
        ok = np.isfinite(fx); D = M[m]; rr = np.r_[0.0, (1 + D["r"][1:]) * fx[1:] / fx[:-1] - 1]; rr = np.where(np.isfinite(rr), rr, 0.0)
        first = int(np.argmax(ok)); dts = D["dates"][first:]; r_ = rr[first:]; r_[0] = 0.0
        nights = np.r_[0, [(b - a).days for a, b in zip(dts[:-1], dts[1:])]]; f_ = rf_on(list(dts)) / 100 / 365 * nights
        me = month_end_idx(dts)
        if len(me) < 130: continue
        xf, _ = faber(r_, f_, me); xb = bh(r_, f_); s0 = me[9] + 1; usd_d.append(sr(xf[s0:]) - sr(xb[s0:]))
        out.append(f"| {m} | {dts[s0]}→{END} | {sr(xf[s0:]):+.2f} | {sr(xb[s0:]):+.2f} | {sr(xf[s0:])-sr(xb[s0:]):+.2f} | {maxdd(xf[s0:], f_[s0:])*100:.0f}% | {maxdd(xb[s0:], f_[s0:])*100:.0f}% |")
    out.append(f"\ngemiddelde ΔSR USD-rij: {np.mean(usd_d):+.3f} over {len(usd_d)} markten.")
    # ---- Regel B
    out += regel_b(rng, M, prim)
    txt = "\n".join(out); open("results/R2/run5_crossmarket.md", "w").write(txt + "\n"); print(txt)
    with open("catalogus/TRIALS.csv", "a") as f:
        f.write(f"{date.today()};S11_crossmarket_C02;basis;D2b [etf, 12 markten];ontdekking;{np.mean([res[m]['SRf'] for m in prim]):.3f};;{p:.6f};;{label[:60]}\n")
    import engine.run_rule as E; E.recompute_fdr()
def regel_b(rng, M, prim):
    out = ["", "## Regel B — regionale C52 (informatief; USD-rij; 2000-09→2024; lokale aandelen in USD + BOND10_SYN + GOLD_F; ∝ 1/σ60, vol-target 8%, geen hefboom; vs 60/40 lokale aandelen/obligatie)", ""]
    spx = load_daily("SPX", "close"); G = np.array([d for d in spx["date"] if date(2000, 9, 1) <= d <= END]); L = len(G)
    def on(name, field="adjclose"):
        df = load_daily(name, field); ks = np.array(df["date"], dtype="datetime64[D]"); j = np.searchsorted(ks, np.array(G, dtype="datetime64[D]"), side="right") - 1
        return np.where(j >= 0, np.asarray(df["close"])[np.clip(j, 0, None)], np.nan)
    B = on("BOND10_SYN"); Gd = on("GOLD_F", "close"); nights = np.r_[0, [(b - a).days for a, b in zip(G[:-1], G[1:])]]; rfd = rf_on(list(G)) / 100 / 365 * nights
    def rets(p): return np.r_[np.nan, p[1:] / p[:-1] - 1]
    mk = [m for m in prim if FX.get(m, (None,))[0] is not None or m == "HSI"]; E = {}
    for m in mk:
        c = on(m, "close"); fx = fx_on(m, list(G)); p = c * fx; p = np.where(np.isfinite(p), p, np.nan); E[m] = rets(p)
    rB, rG = rets(B), rets(Gd)
    def port(rE, rBb, rGg, rf, rebal):
        n = len(rE); R = np.vstack([rE, rBb, rGg]); W = np.zeros((3, n)); cur = np.zeros(3)
        for j, i in enumerate(rebal):
            if i < 61: continue
            win = R[:, i - 60:i + 1]
            if not np.all(np.isfinite(win)): continue
            s = win.std(axis=1, ddof=1) * math.sqrt(252); w = (1 / s) / (1 / s).sum(); sp = math.sqrt(w @ (np.cov(win) * 252) @ w); w = w * min(1.0, 0.08 / sp)
            nxt = rebal[j + 1] if j + 1 < len(rebal) else n; W[:, i:nxt] = w[:, None]
        Wp = np.c_[np.zeros(3), W[:, :-1]]; turn = np.abs(W - np.c_[np.zeros(3), W[:, :-1]]).sum(axis=0)
        x = (Wp * (np.nan_to_num(R) - rf)).sum(axis=0) - turn * RT_HALF - np.abs(Wp).sum(axis=0) * TER / 252
        wb = np.array([0.6, 0.4, 0.0])[:, None]; xb = (wb * (np.nan_to_num(R) - rf)).sum(axis=0) - 1.0 * TER / 252 * 1.0
        return x, xb
    def stat(x, xb, f, s0):
        return sr(x[s0:]) - sr(xb[s0:]), maxdd(x[s0:], f[s0:]) - maxdd(xb[s0:], f[s0:]), sr(x[s0:]), sr(xb[s0:])
    ym = np.array([d.year * 12 + d.month for d in G]); me = list(np.where(np.r_[ym[1:] != ym[:-1], True])[0])
    out += ["| markt | SR C52-reg | SR 60/40 | ΔSR | maxDD C52-reg | maxDD 60/40 | ΔmaxDD |", "|---|---|---|---|---|---|---|"]; obs = {}
    for m in mk:
        v = np.isfinite(E[m]); i0 = int(np.argmax(v))
        rE = np.where(v, E[m], np.nan); x, xb = port(rE, rB, rG, rfd, me); s0 = max(i0 + 300, 300)
        d_sr, d_dd, s1, s2 = stat(x, xb, rfd, s0); eqx = np.cumprod(1 + x[s0:] + rfd[s0:]); eqb = np.cumprod(1 + xb[s0:] + rfd[s0:])
        out.append(f"| {m} | {s1:+.2f} | {s2:+.2f} | {d_sr:+.2f} | {maxdd(x[s0:], rfd[s0:])*100:.0f}% | {maxdd(xb[s0:], rfd[s0:])*100:.0f}% | {d_dd*100:+.0f} pp |"); obs[m] = (d_sr, d_dd, s1)
    pooled = float(np.mean([o[0] for o in obs.values()])); npos = sum(o[2] > 0 for o in obs.values()); ndd = sum(o[1] < 0 for o in obs.values())
    # null (21-daagse benadering)
    reb = list(range(0, L, 21)); obs_a = []
    for m in mk:
        v = np.isfinite(E[m]); rE = np.where(v, E[m], np.nan); x, xb = port(rE, rB, rG, rfd, reb); obs_a.append(stat(x, xb, rfd, max(int(np.argmax(v)) + 300, 300))[0])
    obs_pool = float(np.mean(obs_a)); null = []
    for k in range(min(NREP, 500)):
        idx = stationary_idx(L, rng); ds = []
        for m in mk:
            v = np.isfinite(E[m][idx]);
            if v.sum() < 1500: continue
            rE = E[m][idx][v]; x, xb = port(rE, rB[idx][v], rG[idx][v], rfd[idx][v], list(range(0, len(rE), 21))); ds.append(stat(x, xb, rfd[idx][v], 300)[0])
        null.append(np.mean(ds))
    null = np.array(null); p = float((null >= obs_pool).mean())
    out += ["", f"- gepoold ΔSR (exact maandeinde) **{pooled:+.3f}**; SR C52-reg > 0 in {npos}/{len(mk)}; ΔmaxDD < 0 in {ndd}/{len(mk)}; nul-kalibratie ({len(null)} replica's, benadering): waargenomen {obs_pool:+.3f}, nul gem. {null.mean():+.3f} (sd {null.std():.3f}); **p = {p:.3f}**",
            "- Alleen informatief (PREREG_CAT5): obligatie-/goudpoot zijn geen onafhankelijke markttest van de timing; 60/40-benchmark bevat geen goud."]
    return out
if __name__ == "__main__":
    main()
