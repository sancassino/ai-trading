"""R4-rapportage (geen trial): C61-compounding-test, C60 per decennium (1963→), diversifier-screen (corr, ΔSR/ΔmaxDD op P-ETF-a). Ontdekking ≤ 2024."""
import math
import numpy as np
from datetime import date
from engine.forward import series
from engine.run_rule import load_daily
import forward_portfolio as FP
DISC = date(2024, 12, 31); out = ["# R4-rapportage (D-063; ontdekking ≤ 2024; geen trial)", ""]
# 1. C61 compounding-test
spx = load_daily("SPX", "close"); c = spx["close"]; d = spx["date"]
out.append("## 1. C61 — compounding-/pad-afhankelijkheidstest dagelijks-gereste inverse (SPX, prijsindex)\n\n| episode | index-rendement R | naïef −R | −Σ dagrendementen | dagelijks gereset Π(1−r_d)−1 | verschil gereset vs −R |\n|---|---|---|---|---|---|")
for lab, a, b in (("2000-03-24 → 2002-10-09", date(2000, 3, 24), date(2002, 10, 9)), ("2007-10-09 → 2009-03-09", date(2007, 10, 9), date(2009, 3, 9)), ("2020-02-19 → 2020-03-23 (crash, 1 mnd)", date(2020, 2, 19), date(2020, 3, 23)), ("2022-01-03 → 2022-10-12", date(2022, 1, 3), date(2022, 10, 12))):
    i0 = max(j for j, x in enumerate(d) if x <= a); i1 = max(j for j, x in enumerate(d) if x <= b)
    r = c[i0 + 1:i1 + 1] / c[i0:i1] - 1; R = c[i1] / c[i0] - 1; inv = float(np.prod(1 - r) - 1)
    out.append(f"| {lab} | {R*100:+.1f}% | {-R*100:+.1f}% | {-r.sum()*100:+.1f}% | {inv*100:+.1f}% | {(inv+R)*100:+.1f} pp |")
out.append("\nLezing: het engine-model (dagelijks −1× herwogen) = de dagelijks-gereste inverse. In aanhoudende dalingen pakt de dagelijkse reset gunstig uit t.o.v. −R (+3 tot +32 pp; in zijwaartse, volatiele markten werkt het verval juist tegen). C61 is dus met de juiste dagelijks-herwogen conventie gemodelleerd én dit pad-effect is gunstig voor C61 — ondanks dat faalt C61. Uitkomst C61: SR 0,21 (t 2,1), niet beter dan buy-and-hold en zwakker dan C02 → de inverse-poot voegt niets toe (maxDD 81%, dag −20,5% in 1987 door short na rally).")
# 2. C60 per decennium
s = series("C60_bondtiming", "basis", "etf", end=DISC); days = sorted(s)
b = load_daily("BOND10_SYN", "adjclose"); bc = b["close"]; bret = dict(zip(b["date"][1:], bc[1:] / bc[:-1] - 1))
from engine.run_rule import rf_on
out.append("\n## 2. C60 obligatie-duurtiming per decennium (etf, excess SR; B&H = synthetische 10j-TR − rf)\n\n| periode | C60 SR | C60 CAGR tot. | C60 maxDD | B&H SR | B&H CAGR | B&H maxDD |\n|---|---|---|---|---|---|---|")
nights = np.r_[0, [(y - x).days for x, y in zip(days[:-1], days[1:])]]; rf = rf_on(days) / 100 / 365 * nights
btot = np.array([bret.get(x, 0.0) for x in days]); bex = btot - rf
for lab, a, bb in (("1963–69", 1963, 1969), ("1970s", 1970, 1979), ("1980s", 1980, 1989), ("1990s", 1990, 1999), ("2000s", 2000, 2009), ("2010s", 2010, 2019), ("2020–24", 2020, 2024), ("2022", 2022, 2022), ("alles", 0, 9999)):
    idx = [i for i, x in enumerate(days) if a <= x.year <= bb]
    if len(idx) < 150: continue
    def st(ex, tot):
        eq = np.cumprod(1 + tot); dd = float(np.max(1 - eq / np.maximum.accumulate(eq))); return ex.mean() / ex.std() * math.sqrt(252), eq[-1] ** (252 / len(tot)) - 1, dd
    e = np.array([s[days[i]][0] for i in idx]); t = np.array([s[days[i]][1] for i in idx]); sa = st(e, t); sb = st(bex[idx], btot[idx])
    out.append(f"| {lab} | {sa[0]:+.2f} | {sa[1]*100:+.1f}% | {sa[2]*100:.1f}% | {sb[0]:+.2f} | {sb[1]*100:+.1f}% | {sb[2]*100:.1f}% |")
# 3. diversifier-screen
X = {"C52L": ("C52_allweather", "lang", "etf"), "C02": ("C02_faber", "basis", "etf"), "C55": ("C55_daa", "basis", "etf"), "C57": ("C57_gtaa", "basis", "etf"), "C58": ("C58_goudtrend", "basis", "etf"),
     "C59": ("C59_grondstoftrend", "basis", "etf"), "C60": ("C60_bondtiming", "basis", "etf"), "C61": ("C61_ls_inverse", "basis", "etf_inverse")}
S = {k: series(*v, end=DISC) for k, v in X.items()}
spxr = series("C02_faber", "basis", "etf", end=DISC)  # placeholder voor kalender
spxdf = load_daily("SPX", "close"); spx_r = dict(zip(spxdf["date"][1:], spxdf["close"][1:] / spxdf["close"][:-1] - 1))
out.append("\n## 3. Diversifier-screen (corr op gemeenschappelijke dagen; ΔSR/ΔmaxDD = P-ETF-a met en zonder de extra sleeve op dezelfde periode)\n\n| sleeve | periode | corr C02 | corr C52L | corr SPX-excess | P-ETF-a (C52L+C02) SR / maxDD | + sleeve: SR / maxDD | ΔSR | ΔmaxDD | screen (corr ≤ 0,3 & ΔSR>0) |\n|---|---|---|---|---|---|---|---|---|---|")
for k in ("C55", "C57", "C58", "C59", "C60", "C61"):
    days = sorted(set(S[k]) & set(S["C02"]) & set(S["C52L"]))
    if len(days) < 500: continue
    v = np.array([S[k][x][0] for x in days]); a = np.array([S["C02"][x][0] for x in days]); b_ = np.array([S["C52L"][x][0] for x in days])
    nights = np.r_[0, [(y - x).days for x, y in zip(days[:-1], days[1:])]]; rf = rf_on(days) / 100 / 365 * nights; sx = np.array([spx_r.get(x, 0.0) for x in days]) - rf
    Sx = {n: S[n] for n in S}
    d0, o0 = FP.run_petf(Sx, ["S_" + "C52L", "S_C02"]) if False else (None, None)
    def petf(names):
        Sd = {n: S[n] for n in names}; dd, o = FP.run_petf(Sd, names); tot, x, _ = o["P-ETF-a"]; return dd, tot, x
    dA, tA, xA = petf(["C52L", "C02"]); dB, tB, xB = petf(["C52L", "C02", k]); lo = days[0]
    sa = FP.stats(dA, tA, xA, lo=lo); sb = FP.stats(dB, tB, xB, lo=lo)
    c1 = np.corrcoef(v, a)[0, 1]; c2 = np.corrcoef(v, b_)[0, 1]; c3 = np.corrcoef(v, sx)[0, 1]
    ok = max(abs(c1), abs(c2), abs(c3)) <= 0.3 and sb["SR"] > sa["SR"]
    out.append(f"| {k} | {days[0]}→{days[-1]} | {c1:+.2f} | {c2:+.2f} | {c3:+.2f} | {sa['SR']:.2f} / {sa['maxDD']*100:.1f}% | {sb['SR']:.2f} / {sb['maxDD']*100:.1f}% | {sb['SR']-sa['SR']:+.2f} | {(sb['maxDD']-sa['maxDD'])*100:+.1f} pp | {'JA' if ok else 'nee'} |")
open("results/R2/run4_rapport.md", "w").write("\n".join(out) + "\n"); print("\n".join(out))
