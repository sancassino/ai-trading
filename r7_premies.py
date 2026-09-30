"""R7 (PREREG_CAT7): C66 VRP-proxy (evidentie) + C67 landenrotatie (1 trial). Ontdekking ≤ 2024-12-31."""
import math
import numpy as np
from datetime import date
from engine.run_rule import load_daily, rf_on, t_nw, p_one_sided, recompute_fdr
import r5_crossmarket as R5
END = date(2024, 12, 31)
out = ["# R7 — premies: C66 VRP-proxy (evidentie, geen trial) en C67 landenrotatie (1 trial) — PREREG_CAT7; ontdekking ≤ 2024", ""]
# ---------------- C66
spx = load_daily("SPX", "close"); vix = load_daily("VIX", "close"); vm = dict(zip(vix["date"], vix["close"]))
d = [x for x in spx["date"] if x <= END]; c = np.asarray(spx["close"])[:len(d)]; r = np.r_[0.0, c[1:] / c[:-1] - 1]
ym = np.array([x.year * 12 + x.month for x in d]); me = list(np.where(np.r_[ym[1:] != ym[:-1], True])[0])
rows = []
for i in me:
    if d[i] not in vm or i + 21 >= len(d): continue
    v = vm[d[i]]; rv = math.sqrt(252 * np.mean(r[i + 1:i + 22] ** 2)) * 100; ret = c[min(i + 21, len(c) - 1)] / c[i] - 1
    rows.append((d[i], v, rv, v - rv, (v ** 2 - rv ** 2) / v ** 2, ret))
D = [x[0] for x in rows]; V = np.array([x[1] for x in rows]); RV = np.array([x[2] for x in rows]); VRP = np.array([x[3] for x in rows]); Q = np.array([x[4] for x in rows]); SR_ = np.array([x[5] for x in rows])
sk = lambda x: float(((x - x.mean()) ** 3).mean() / x.std() ** 3); ku = lambda x: float(((x - x.mean()) ** 4).mean() / x.std() ** 4)
out += [f"## C66 — VRP-proxy (VIX − gerealiseerde SPX-vol vooruit 21 d; {D[0]}→{D[-1]}, {len(D)} maanden)", "",
        f"- gemiddelde VIX {V.mean():.1f}, gemiddelde RV {RV.mean():.1f}, **gemiddelde VRP {VRP.mean():+.2f} vol-punten**; VRP > 0 in **{(VRP>0).mean()*100:.0f}%** van de maanden; mediaan {np.median(VRP):+.2f}",
        f"- **variantieswap-proxy** r = (VIX² − RV²)/VIX² per eenheid variantie-notional: gem. {Q.mean():+.3f}/mnd, **SR {Q.mean()/Q.std()*math.sqrt(12):.2f}**, scheefheid {sk(Q):+.1f}, kurtosis {ku(Q):.0f}, slechtste maand {Q.min():.1f} ({D[int(Q.argmin())]}), beste {Q.max():+.2f}; 5 slechtste maanden = **{abs(np.sort(Q)[:5].sum())/Q.sum()*100:.0f}% van de totale winst** ({', '.join(str(D[i]) for i in np.argsort(Q)[:5])})",
        f"- corr met SPX-21d-rendement {np.corrcoef(Q, SR_)[0,1]:+.2f}; met 5%-vaste notional: maxDD {(1-np.min(np.cumprod(1+0.05*Q)/np.maximum.accumulate(np.cumprod(1+0.05*Q))))*100:.0f}% (capitaal-verlies als RV ≫ VIX), met 1%: {(1-np.min(np.cumprod(1+0.01*Q)/np.maximum.accumulate(np.cumprod(1+0.01*Q))))*100:.0f}%", "",
        "| periode | n | gem. VRP | % VRP > 0 | SR proxy | slechtste maand |", "|---|---|---|---|---|---|"]
for lab, a, b in (("1990s", 1990, 1999), ("2000s", 2000, 2009), ("2010s", 2010, 2019), ("2020–24", 2020, 2024)):
    s = np.array([a <= x.year <= b for x in D])
    if s.sum() > 12: out.append(f"| {lab} | {s.sum()} | {VRP[s].mean():+.2f} | {(VRP[s]>0).mean()*100:.0f}% | {Q[s].mean()/Q[s].std()*math.sqrt(12):.2f} | {Q[s].min():.1f} |")
out += ["", "| VIX-regime | n | gem. VRP | % VRP > 0 | SR proxy | slechtste maand |", "|---|---|---|---|---|---|"]
for lab, lo, hi in (("VIX < 15", 0, 15), ("15–25", 15, 25), ("> 25", 25, 999)):
    s = (V >= lo) & (V < hi)
    if s.sum() > 12: out.append(f"| {lab} | {s.sum()} | {VRP[s].mean():+.2f} | {(VRP[s]>0).mean()*100:.0f}% | {Q[s].mean()/Q[s].std()*math.sqrt(12):.2f} | {Q[s].min():.1f} |")
out += ["", "Staarttest: " + "; ".join(f"{lab}: proxy {Q[[i for i,x in enumerate(D) if (x.year,x.month)==ym_]][0]:.1f}" for lab, ym_ in (("2008-09/10", (2008, 9)), ("2008-10", (2008, 10)), ("2011-07", (2011, 7)), ("2018-01", (2018, 1)), ("2020-02", (2020, 2)))) +
        ". Lezing: het VRP-patroon is robuust (positief in 84% van de maanden, in elk decennium en elk VIX-regime), maar het is een verzekeringspremie met zware linkerstaart: de slechtste maand (−5,7) wist ≈ 18 maanden gemiddelde winst uit; bij 5% vaste notional is de maxDD 42%. De proxy is optimistisch (geen spreads/marge/strike-selectie; VIX-methodiek vóór 2003 anders → SR 5,2 in de jaren 90 is niet serieus te nemen); geen optie-P&L-claim. PutWrite-substitutie wacht op ^PUT/^BXM (R2-007)."]
# ---------------- C67
names = ["SPX", "DAX", "N225", "FTSE", "CAC40", "AEX", "SMI", "IBEX", "BEL20", "TSX", "HSI", "AXJO"]
G = np.array([x for x in spx["date"] if date(1999, 6, 1) <= x <= END]); L = len(G)
def on(name):
    df = load_daily(name, "close"); ks = np.array(df["date"], dtype="datetime64[D]"); j = np.searchsorted(ks, np.array(G, dtype="datetime64[D]"), side="right") - 1
    return np.where(j >= 0, np.asarray(df["close"])[np.clip(j, 0, None)], np.nan)
P = np.vstack([on(n) * (np.ones(L) if n == "SPX" else R5.fx_on(n, list(G))) for n in names])
ok0 = np.where(np.all(np.isfinite(P), axis=0))[0][0]
Rr = np.full(P.shape, np.nan); Rr[:, 1:] = P[:, 1:] / P[:, :-1] - 1
nights = np.r_[0, [(b - a).days for a, b in zip(G[:-1], G[1:])]]; rfd = rf_on(list(G)) / 100 / 365 * nights
ymG = np.array([x.year * 12 + x.month for x in G]); meG = np.where(np.r_[ymG[1:] != ymG[:-1], True])[0]
W = np.zeros((len(names), L)); cur = np.zeros(len(names)); start = None
for j, i in enumerate(meG):
    if i < ok0 + 252 or not np.all(np.isfinite(P[:, i - 252])): continue
    mom = P[:, i - 21] / P[:, i - 252] - 1; w = np.zeros(len(names)); w[np.argsort(mom)[-3:]] = 1 / 3
    nxt = meG[j + 1] if j + 1 < len(meG) else L; W[:, i:nxt] = w[:, None]; start = start or i
def sim(ter):
    Wp = np.c_[np.zeros(len(names)), W[:, :-1]]; turn = np.abs(W - np.c_[np.zeros(len(names)), W[:, :-1]]).sum(axis=0)
    x = (Wp * (np.nan_to_num(Rr) - rfd)).sum(axis=0) - turn * 6.5e-4 - Wp.sum(axis=0) * ter / 252
    xb = (np.nan_to_num(Rr) - rfd).mean(axis=0) - ter / 252; return x, xb
def st(x, m):
    e = x[m]; t = e + rfd[m]; eq = np.cumprod(1 + t); return e.mean() / e.std() * math.sqrt(252), eq[-1] ** (252 / len(t)) - 1, float(np.max(1 - eq / np.maximum.accumulate(eq)))
x, xb = sim(0.0007); m = np.arange(L) > start
ss, sb = st(x, m), st(xb, m); tn = t_nw(x[m] - xb[m]); p = p_one_sided(tn)
x2, xb2 = sim(0.0025); ss2, sb2 = st(x2, m), st(xb2, m); tn2 = t_nw(x2[m] - xb2[m])
mn = np.array([i for i in meG if i > start]); hit = np.mean([np.prod(1 + (Rr[:, a + 1:b + 1].T * W[:, a][None, :].T.T).sum(axis=1) if False else 1) for a, b in zip(mn[:-1], mn[1:])]) if False else None
gate = tn >= 3 and ss[0] > sb[0] and ss[2] <= sb[2]
label = "door G-ontdekking" if gate else "afgewezen"
out += ["", f"## C67 — landenrotatie (top-3 van 12 markten op 12-1m, USD; {G[start]}→{END}; ontdekking)", "",
        f"| | SR (excess) | CAGR totaal | maxDD |\n|---|---|---|---|\n| **top-3 rotatie** | {ss[0]:+.2f} | {ss[1]*100:.1f}% | {ss[2]*100:.0f}% |\n| gelijk gewogen 12 markten (benchmark) | {sb[0]:+.2f} | {sb[1]*100:.1f}% | {sb[2]*100:.0f}% |",
        "", f"- ΔSR {ss[0]-sb[0]:+.2f}, ΔmaxDD {(ss[2]-sb[2])*100:+.0f} pp, **NW-t van het verschil {tn:+.2f}** (eenzijdig p {p:.3f}); TER 0,25%-gevoeligheid: SR {ss2[0]:+.2f} vs {sb2[0]:+.2f}, t {tn2:+.2f}",
        f"- beslissing (vooraf: t ≥ 3 én ΔSR > 0 én ΔmaxDD ≤ 0): **{label}**"]
for lab, a, b in (("2000s", 2000, 2009), ("2010s", 2010, 2019), ("2020–24", 2020, 2024)):
    mm = m & np.array([a <= y.year <= b for y in G]); 
    if mm.sum() > 250: s1, s2 = st(x, mm), st(xb, mm); out.append(f"  - {lab}: top-3 SR {s1[0]:+.2f} vs benchmark {s2[0]:+.2f} (Δ {s1[0]-s2[0]:+.2f})")
open("results/R2/run7_premies.md", "w").write("\n".join(out) + "\n"); print("\n".join(out))
with open("catalogus/TRIALS.csv", "a") as f:
    f.write(f"{date.today()};C67_landenrotatie;basis;D2b [etf, 12 markten USD];ontdekking;{ss[0]:.3f};{tn:.3f};{p:.6f};;{label}\n")
recompute_fdr()
