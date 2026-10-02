"""R8 (PREREG_CAT8): C02 Faber in USD-termen op EM-markten + STI/KOSPI/TWII. Informatief, geen trial."""
import math
import numpy as np
from datetime import date
from engine.run_rule import load_daily, rf_on, t_nw
import r5_crossmarket as R5
END = date(2024, 12, 31)
MK = {"BVSP": ("FXBIS_BRL", date(1995, 1, 1), "EM"), "MXX": ("FXBIS_MXN", date(1997, 1, 1), "EM"), "JKSE": ("FXBIS_IDR", date(1990, 1, 1), "EM"), "SENSEX": ("FXBIS_INR", date(1997, 1, 1), "EM"),
      "STI": ("FXBIS_SGD", date(1988, 1, 1), "AZ"), "KOSPI": ("FXBIS_KRW", date(1997, 1, 1), "AZ"), "TWII": ("FXBIS_TWD", date(1997, 1, 1), "AZ")}
out = ["# R8 — C02 Faber in USD-termen: EM-markten + STI/KOSPI/TWII (PREREG_CAT8; informatief; ontdekking ≤ 2024; USD-rf gelabeld)", "",
       "| markt | groep | periode | SR Faber | SR B&H | ΔSR | maxDD Faber | maxDD B&H | ΔmaxDD | NW-t (verschil) | 1990s ΔSR | 2000s | 2010s | 2020–24 |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
res = {}
for m, (fxn, start, grp) in MK.items():
    df = load_daily(m, "close"); keep = np.array([start <= d <= END for d in df["date"]]); d = np.array(df["date"])[keep]; c = np.asarray(df["close"])[keep]
    fx = load_daily(fxn, "close"); ks = np.array(fx["date"], dtype="datetime64[D]"); j = np.searchsorted(ks, np.array(d, dtype="datetime64[D]"), side="right") - 1
    loc = np.where(j >= 0, np.asarray(fx["close"])[np.clip(j, 0, None)], np.nan); ok = np.isfinite(loc) & (loc > 0); d, c, loc = d[ok], c[ok], loc[ok]
    usd = c / loc; r = np.r_[0.0, usd[1:] / usd[:-1] - 1]; nights = np.r_[0, [(b - a).days for a, b in zip(d[:-1], d[1:])]]; rfd = rf_on(list(d)) / 100 / 365 * nights
    me = R5.month_end_idx(d); xf, pos = R5.faber(r, rfd, me); xb = R5.bh(r, rfd); s0 = me[9] + 1
    res[m] = (d[s0:], xf[s0:], xb[s0:], rfd[s0:], grp)
    dec = []
    for a, b in ((1990, 1999), (2000, 2009), (2010, 2019), (2020, 2024)):
        s = np.array([a <= x.year <= b for x in d[s0:]]); dec.append(f"{R5.sr(xf[s0:][s]) - R5.sr(xb[s0:][s]):+.2f}" if s.sum() > 500 else "–")
    out.append(f"| {m} | {grp} | {d[s0]}→{END} | {R5.sr(xf[s0:]):+.2f} | {R5.sr(xb[s0:]):+.2f} | {R5.sr(xf[s0:])-R5.sr(xb[s0:]):+.2f} | {R5.maxdd(xf[s0:], rfd[s0:])*100:.0f}% | {R5.maxdd(xb[s0:], rfd[s0:])*100:.0f}% | {(R5.maxdd(xf[s0:], rfd[s0:])-R5.maxdd(xb[s0:], rfd[s0:]))*100:+.0f} pp | {t_nw(xf[s0:]-xb[s0:]):+.2f} | " + " | ".join(dec) + " |")
rng = np.random.default_rng(8)
def pooled(ms, label):
    ds = [R5.sr(res[m][1]) - R5.sr(res[m][2]) for m in ms]; dd = [R5.maxdd(res[m][1], res[m][3]) - R5.maxdd(res[m][2], res[m][3]) for m in ms]
    years = sorted({x.year for m in ms for x in res[m][0]}); by = {m: {y: np.array([x.year == y for x in res[m][0]]) for y in years} for m in ms}; bs = []
    for _ in range(2000):
        ys = rng.choice(years, len(years)); v = []
        for m in ms:
            a = np.concatenate([res[m][1][by[m][y]] for y in ys]); b = np.concatenate([res[m][2][by[m][y]] for y in ys])
            if len(a) > 500: v.append(R5.sr(a) - R5.sr(b))
        bs.append(np.mean(v))
    ci = np.percentile(bs, [5, 95]); return f"- **{label}** ({len(ms)} markten): gepoold ΔSR {np.mean(ds):+.3f} (90%-BI {ci[0]:+.2f}…{ci[1]:+.2f}); ΔmaxDD < 0 in {sum(x < 0 for x in dd)}/{len(ms)} (gem. {np.mean(dd)*100:+.0f} pp); SR Faber > 0 in {sum(R5.sr(res[m][1]) > 0 for m in ms)}/{len(ms)}"
out += ["", pooled([m for m in MK if MK[m][2] == "EM"], "EM-4 (BVSP, MXX, JKSE, SENSEX)"), pooled([m for m in MK if MK[m][2] == "AZ"], "STI/KOSPI/TWII (USD)"), pooled(list(MK), "alle 7")]
out += ["", "Lezing: zie RUNLOG_R2. Valuta-ruis (BRL/MXN/IDR-crises) zit in zowel Faber als B&H; Faber beschermt tegen lokale crashes maar niet tegen valuta-schokken tijdens een belegde maand."]
open("results/R2/run8_em.md", "w").write("\n".join(out) + "\n"); print("\n".join(out))
