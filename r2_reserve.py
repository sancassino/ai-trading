"""R2 — gezamenlijke reserve-run (D-038/D-042/D-057/D-064): 2025-01-01 → laatste complete dag. EENMALIG. NIET UITVOEREN vóór vrijgave in BESLUITEN.md (01-10 12:00).
Guard: draait alleen met RESERVE_RELEASED=1 én `--confirm-once`. Schrijft results/R2/reserve_run.md; append-only rij per sleeve/portefeuille in results/R2/reserve_log.csv.
Rapportage (D-057): teken, SR excess met 90%-betrouwbaarheidsinterval (analytisch + 21d-blok-bootstrap), verhouding tot ontdekking-SR, alfa boven cash in €/mnd (haircut 30/40/50% op excess,
EUR-cash apart), naast cash-only-nulbenchmark en 60/40. Pass/fail alleen op teken + 'niet significant afwijkend van ontdekking' — géén conclusies uit de puntschatting."""
import math, os, sys
import numpy as np
from datetime import date
from engine.forward import series
from engine.run_rule import load_daily, rf_on
import forward_portfolio as FP
START = date(2025, 1, 1); DISC = date(2024, 12, 31)
SLV = {"C52 lang": "S_C52L", "C52 basis": "S_C52B", "C02 Faber": "S_C02", "C17 FOMC (future)": "S_C17", "C54 qa (future)": "S_C54Q", "C55 DAA": "S_C55",
       "C44 krediet": "S_C44", "C16 Halloween": "S_C16", "C33 trend-laagvol (future)": "S_C33"}
INFO = {"C57 Faber-GTAA (informatief)": ("C57_gtaa", "basis", "etf")}
def sr_stats(x, rng, blk=21, B=2000):
    n = len(x); sr = x.mean() / x.std() * math.sqrt(252); yrs = n / 252
    se = math.sqrt((1 + sr ** 2 / 2) / yrs); lo, hi = sr - 1.645 * se, sr + 1.645 * se
    bs = []
    for _ in range(B):
        st = rng.integers(0, n, n // blk + 1); idx = ((st[:, None] + np.arange(blk)).ravel() % n)[:n]; y = x[idx]; bs.append(y.mean() / y.std() * math.sqrt(252) if y.std() > 0 else 0.0)
    return sr, (lo, hi), tuple(np.percentile(bs, [5, 95])), n
def main():
    if os.environ.get("RESERVE_RELEASED") != "1" or "--confirm-once" not in sys.argv:
        sys.exit("Reserve-run geblokkeerd: wacht op vrijgave door de CEO (BESLUITEN.md) en zet RESERVE_RELEASED=1 --confirm-once.")
    if os.path.exists("results/R2/reserve_run.md"):
        sys.exit("Reserve-run is al uitgevoerd (eenmalig, D-038); niet opnieuw.")
    rng = np.random.default_rng(5); rows = []
    end = None
    # sleeves (excess-reeksen) en discovery-SR
    full = {k: series(*FP.SLEEVES[v]) for k, v in SLV.items()}
    full.update({k: series(*v) for k, v in INFO.items()})
    for k, s in full.items():
        days = sorted(s); ex = np.array([s[d][0] for d in days]); dsel = np.array([d <= DISC for d in days]); rsel = np.array([d >= START for d in days])
        if rsel.sum() < 60: continue
        sd = ex[dsel].mean() / ex[dsel].std() * math.sqrt(252); sr, ci, bci, n = sr_stats(ex[rsel], rng)
        rows.append((k, days[rsel.argmax()], days[-1], n, sd, sr, ci, bci, ex[rsel].mean() * 252))
    P = dict(FP.all_portfolios(1)); P.update(FP.all_portfolios(2))   # PREREG_PORT (P-ETF-a/b, P1, P-breed) + PREREG_PORT2 (P-ETF+, P-breed-2)
    for p, (days, tot, x, lev) in P.items():
        ok = np.isfinite(x); dsel = np.array([d <= DISC for d in days]) & ok; rsel = np.array([d >= START for d in days]) & ok
        if rsel.sum() < 60: continue
        sd = x[dsel].mean() / x[dsel].std() * math.sqrt(252); sr, ci, bci, n = sr_stats(x[rsel], rng)
        rows.append((p, [d for d, r in zip(days, rsel) if r][0], days[-1], n, sd, sr, ci, bci, x[rsel].mean() * 252))
    out = ["# Gezamenlijke reserve-run (2025-01-01 →) — EENMALIG; rapportage volgens D-057/D-060", "",
           "| sleeve / portefeuille | periode | dagen | SR ontdekking | SR reserve | 90%-CI (analytisch) | 90%-CI (blok-bootstrap) | teken gelijk | SR-reserve ≥ 50% ontd. | ontdekking-SR binnen CI | alfa/jr reserve (excess) | alfa boven cash €/mnd na haircut 30/40/50% (op €80k) |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, a, b, n, sd, sr, ci, bci, al in rows:
        out.append(f"| {k} | {a}→{b} | {n} | {sd:.2f} | {sr:+.2f} | {ci[0]:+.2f}…{ci[1]:+.2f} | {bci[0]:+.2f}…{bci[1]:+.2f} | {'ja' if sr > 0 else 'nee'} | {'ja' if sr >= 0.5 * sd else 'nee'} | {'ja' if ci[0] <= sd <= ci[1] else 'nee'} | {al*100:+.1f}% | "
                   f"€{al*0.7*80000/12:.0f} / €{al*0.6*80000/12:.0f} / €{al*0.5*80000/12:.0f} |")
    # nulbenchmarks
    spx = load_daily("SPX_TR", "adjclose"); spy = load_daily("SPY", "adjclose"); ief = load_daily("IEF", "adjclose")
    def er(df):
        m = {d: c for d, c in zip(df["date"], df["close"])}; ds = sorted(d for d in m if d >= START); prev = max(d for d in m if d < START)
        r = []; p = m[prev]
        for d in ds: r.append(m[d] / p - 1); p = m[d]
        nights = np.array([(b - a).days for a, b in zip([prev] + ds[:-1], ds)]); return np.array(r) - rf_on(ds) / 100 / 365 * nights, ds
    b1, ds = er(spy); b2, _ = er(ief); b6040 = 0.6 * b1 + 0.4 * b2; nights = np.array([(b - a).days for a, b in zip([START] + ds[:-1], ds)]); rf = rf_on(ds) / 100 / 365 * nights
    out += ["", "**Nulbenchmarks (zelfde periode):** cash-only (T-bill 3m): rf ≈ %.2f%%/jr → €%.0f/mnd op €80k; €STR/EUR-cash apart (data/daily/YLD_ESTR). 60/40 SPY/IEF excess-SR %+.2f, SPY %+.2f." % (rf.sum() / (len(rf) / 252) * 100, rf.sum() / (len(rf) / 252) * 80000 / 12, b6040.mean() / b6040.std() * math.sqrt(252), b1.mean() / b1.std() * math.sqrt(252)),
            "", "Lezing (vooraf): 1,75 jr ⇒ SR-standaardfout ≈ 0,75; pass/fail alleen op teken + niet-significant-afwijkend; geen conclusies uit puntschattingen. Sleeves zijn ná ontdekkingsdata gekozen; de reserve is daarmee gebruikt en niet opnieuw beschikbaar."]
    open("results/R2/reserve_run.md", "w").write("\n".join(out) + "\n"); print("\n".join(out))
    with open("results/R2/reserve_log.csv", "a") as f:
        for k, a, b, n, sd, sr, ci, bci, al in rows: f.write(f"{date.today()};{k};{a};{b};{n};{sd:.3f};{sr:.3f};{ci[0]:.3f};{ci[1]:.3f}\n")
if __name__ == "__main__":
    main()
