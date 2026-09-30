"""Forward-papier portefeuilles (D-050) exact volgens PREREG_PORT.md (SHA in RUNLOG). Geen orders, alleen papier.
- Sleeve-reeksen: engine/forward.series (huidige vehikelset), volledige historie t/m de laatste complete dag in data/daily.
- Portefeuilles P-ETF-a, P-ETF-b, P1, P-breed; maandelijkse herweging (eerste handelsdag), σ = 60 d vertraagd, herwegingskosten per vehikel.
- USD-totaalrendement, EUR ongehedged (hoofd) en EUR gehedged (gevoeligheid).
- forward/portfolio_daily.csv: append-only vanaf FORWARD_START; eerder gelogde dagen worden herberekend en afwijkingen > 1 bp gelogd (tracking-band).
- --backtest: statistiek alleen over de ontdekkingsset (≤ 2024-12-31); de reserve (2025-01 → 2026-09) wordt NIET gerapporteerd (D-038).
"""
import math
import os
import sys
from datetime import date, datetime, timezone

import numpy as np

from engine.forward import series
from engine.run_rule import load_daily, rate_on, rf_on

FORWARD_START = date(2026, 10, 1)
DISC_END = date(2024, 12, 31)
OUT = "forward/portfolio_daily.csv"
TRACK = "forward/portfolio_tracking.log"
SLEEVES = {"S_C52L": ("C52_allweather", "lang", "etf"), "S_C52B": ("C52_allweather", "basis", "etf"), "S_C02": ("C02_faber", "basis", "etf"),
           "S_C17": ("C17_fomc_cycle", "basis", "future"), "S_C54Q": ("C54_carver", "qa", "future"), "S_C54B": ("C54_carver", "basis", "future"),
           # PREREG_PORT2 (D-061)
           "S_C55": ("C55_daa", "basis", "etf"), "S_C16": ("C16_halloween", "basis", "etf"), "S_C44": ("C44_krediet", "basis", "etf"),
           "S_C33": ("C33_trend_lowvol", "basis", "future")}
PORTS2 = {"P-breed-2": ["S_C02", "S_C52B", "S_C52L", "S_C54B", "S_C54Q", "S_C55", "S_C16", "S_C44", "S_C33"]}
PETF2 = ["S_C52L", "S_C02", "S_C55"]
OUT2 = "forward/portfolio2_daily.csv"
HALF_RT = {"etf": 6.5e-4, "future": 0.5e-4}
SURCHARGE = 0.015
PORTS = {"P1": ["S_C54Q", "S_C52L", "S_C02", "S_C17"], "P-breed": ["S_C02", "S_C52B", "S_C52L", "S_C54B", "S_C54Q"]}
PETF = ["S_C52L", "S_C02"]


def calendar_and_x(names, S):
    days = sorted(set.intersection(*[set(S[n]) for n in names]))
    X = np.array([[S[n][d][0] for d in days] for n in names])
    return days, X


def rebalance_flags(days):
    return np.array([i == 0 or days[i].month != days[i - 1].month for i in range(len(days))])


def sig(x, i, w=60):
    return x[i - w:i].std() * math.sqrt(252) if i >= w else np.nan


def run_petf(S, PETF=PETF):
    days, X = calendar_and_x(PETF, S)
    n = len(days); nights = np.r_[0, [(b - a).days for a, b in zip(days[:-1], days[1:])]]
    rf = rf_on(days) / 100 / 365 * nights
    reb = rebalance_flags(days)
    w = np.full((len(PETF), n), np.nan); cost_a = np.zeros(n)
    cur = None
    for i in range(n):
        if reb[i]:
            s = np.array([sig(X[j], i) for j in range(len(PETF))])
            if np.all(np.isfinite(s)) and np.all(s > 0):
                new = (1 / s) / (1 / s).sum()
                if cur is not None:
                    cost_a[i] = np.abs(new - cur).sum() * HALF_RT["etf"]
                cur = new
        if cur is not None:
            w[:, i] = cur
    xa = np.nansum(w * X, axis=0) - cost_a
    valid = ~np.isnan(w[0])
    tot_a = rf + xa
    # P-ETF-b: k = min(2, 0,10/σ_P) op maandbasis, geleend deel tegen rf + 1,5%
    k = np.full(n, np.nan); kc = None; cost_b = cost_a.copy()
    for i in range(n):
        if reb[i] and valid[i]:
            hist = xa[:i][valid[:i]]
            sp = hist[-60:].std() * math.sqrt(252) if len(hist) >= 60 else np.nan
            if np.isfinite(sp) and sp > 0:
                nk = min(2.0, 0.10 / sp)
                if kc is not None:
                    cost_b[i] += abs(nk - kc) * HALF_RT["etf"]
                kc = nk
        if kc is not None:
            k[i] = kc
    xb = np.where(np.isfinite(k), k * (xa + cost_a) - cost_b - np.maximum(np.nan_to_num(k) - 1, 0) * SURCHARGE / 365 * nights, np.nan)
    tot_b = rf + xb
    return days, {"P-ETF-a": (np.where(valid, tot_a, np.nan), np.where(valid, xa, np.nan), np.where(valid, 1.0, np.nan)),
                  "P-ETF-b": (tot_b, xb, k)}


def run_scaled(names, S):
    days, X = calendar_and_x(names, S)
    n = len(days); m = len(names); nights = np.r_[0, [(b - a).days for a, b in zip(days[:-1], days[1:])]]
    rf = rf_on(days) / 100 / 365 * nights
    reb = rebalance_flags(days)
    veh = [SLEEVES[s][2] for s in names]
    # sleeve-schalen k_s (maandelijks, vertraagd); gemiddelde reeks voor σ_P
    ks = np.full((m, n), np.nan); cur = None
    for i in range(n):
        if reb[i]:
            s = np.array([sig(X[j], i) for j in range(m)])
            if np.all(np.isfinite(s)) and np.all(s > 0):
                cur = np.minimum(3.0, 0.10 / s)
        if cur is not None:
            ks[:, i] = cur
    avg = np.nanmean(ks * X, axis=0)
    validk = np.isfinite(ks[0])
    kp = np.full(n, np.nan); cp = None; e_prev = None; cost = np.zeros(n)
    for i in range(n):
        if reb[i] and validk[i]:
            hist = avg[:i][validk[:i]]
            if len(hist) >= 60 and hist[-60:].std() > 0:
                cp = min(3.0, 0.10 / (hist[-60:].std() * math.sqrt(252)))
        if cp is not None:
            kp[i] = cp
    E = np.minimum(3.0, ks * kp)                                    # totale hefboom per sleeve ≤ 3
    x = np.full(n, np.nan); tot = np.full(n, np.nan); lev = np.full(n, np.nan)
    for i in range(n):
        if not np.isfinite(kp[i]):
            continue
        e = E[:, i]
        if reb[i] and e_prev is not None:
            cost[i] = sum(abs(e[j] - e_prev[j]) / m * HALF_RT[veh[j]] for j in range(m))
        e_prev = e
        sur = sum(max(e[j] - 1, 0) / m for j in range(m) if veh[j] == "etf") * SURCHARGE / 365 * nights[i]
        x[i] = (e * X[:, i]).mean() - cost[i] - sur
        tot[i] = rf[i] + x[i]; lev[i] = e.mean()
    return days, (tot, x, lev)


def eur_series(days, tot):
    eu = load_daily("EURUSD", "close"); fx = dict(zip(eu["date"], eu["close"]))
    last = None; r_un = np.full(len(days), np.nan)
    import bisect
    ks = list(eu["date"])
    def fx_on(d):
        j = bisect.bisect_right(ks, d) - 1
        return eu["close"][j] if j >= 0 else np.nan
    f = np.array([fx_on(d) for d in days])
    r_un[1:] = (1 + tot[1:]) * f[:-1] / f[1:] - 1
    nights = np.r_[0, [(b - a).days for a, b in zip(days[:-1], days[1:])]]
    hedge = (rate_on("EUR", days) - rate_on("USD", days)) / 100 / 365 * nights
    return r_un, tot + hedge


def all_portfolios(which=1):
    need = set(PETF) | {n for v in PORTS.values() for n in v} if which == 1 else set(PETF2) | {n for v in PORTS2.values() for n in v}
    S = {k: series(*SLEEVES[k]) for k in need}
    out = {}
    if which == 1:
        d, petf = run_petf(S)
        for k, v in petf.items():
            out[k] = (d,) + v
        ports = PORTS
    else:
        d, petf = run_petf(S, PETF2)
        out["P-ETF+"] = (d,) + petf["P-ETF-a"]
        ports = PORTS2
    for p, names in ports.items():
        d, v = run_scaled(names, S)
        out[p] = (d,) + v
    return out


def stats(days, tot, x, lo=None, hi=DISC_END):
    sel = np.array([(lo is None or d >= lo) and d <= hi for d in days]) & np.isfinite(tot)
    t, e = tot[sel], x[sel]
    eq = np.cumprod(1 + t); dd = float(np.max(1 - eq / np.maximum.accumulate(eq))); cagr = eq[-1] ** (252 / len(t)) - 1
    return dict(start=[d for d, s in zip(days, sel) if s][0], SR=e.mean() / e.std() * math.sqrt(252), vol=e.std() * math.sqrt(252), CAGR=cagr, maxDD=dd)


def backtest(which=1):
    P = all_portfolios(which)
    lines = ["# Portefeuilles volgens PREREG_PORT — ontdekkingsset (≤ 2024-12-31); reserve niet gerapporteerd", ""]
    for p, (days, tot, x, lev) in P.items():
        st = stats(days, tot, x)
        eur_un, eur_h = eur_series(days, tot)
        m = np.array([d <= DISC_END for d in days]) & np.isfinite(tot)
        eq_eur = np.cumprod(1 + np.nan_to_num(eur_un[m])); cagr_eur = eq_eur[-1] ** (252 / m.sum()) - 1
        lines.append(f"- **{p}** ({st['start']} → 2024-12-31): SR {st['SR']:.2f}, vol {st['vol']*100:.1f}%, CAGR USD {st['CAGR']*100:.1f}% "
                     f"(EUR ongehedged {cagr_eur*100:.1f}%), maxDD {st['maxDD']*100:.1f}%, gem. hefboom {np.nanmean(lev[m]):.2f} "
                     f"→ €{st['CAGR']*80000/12:,.0f}/mnd bruto op €80k (USD-CAGR; vóór live-haircut 30–50% en box 3)")
    open(f"results/port/PORT{'' if which == 1 else '2'}_backtest.md", "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


def forward(which=1):
    OUT_ = OUT if which == 1 else OUT2
    P = all_portfolios(which)
    names = list(P)
    logged = {}
    if os.path.exists(OUT_):
        for l in open(OUT_):
            if l[:1].isdigit():
                f = l.strip().split(";"); logged[f[0]] = f
    else:
        with open(OUT_, "w") as fh:
            fh.write("date;" + ";".join(f"{p}_usd;{p}_eur;{p}_eur_hedged;{p}_hefboom" for p in names) + ";berekend_utc\n")
    rows = {}
    for p in names:
        days, tot, x, lev = P[p]
        eu, eh = eur_series(days, tot)
        for i, d in enumerate(days):
            if d >= FORWARD_START and np.isfinite(tot[i]):
                rows.setdefault(d.isoformat(), {})[p] = (tot[i], eu[i], eh[i], lev[i])
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    new = []
    for d in sorted(rows):
        if len(rows[d]) != len(names):
            continue
        vals = ";".join(f"{rows[d][p][0]:.8f};{rows[d][p][1]:.8f};{rows[d][p][2]:.8f};{rows[d][p][3]:.4f}" for p in names)
        if d in logged:
            old = logged[d][1:1 + 4 * len(names)]
            for j, p in enumerate(names):
                if abs(float(old[4 * j]) - rows[d][p][0]) > 1e-4:
                    with open(TRACK, "a") as fh:
                        fh.write(f"{ts} {d} {p}: gelogd {float(old[4*j]):+.6f}, herberekend {rows[d][p][0]:+.6f} (> 1 bp; data-herziening?)\n")
        else:
            new.append(f"{d};{vals};{ts}")
    if new:
        with open(OUT_, "a") as fh:
            fh.write("\n".join(new) + "\n")
    print(f"forward_portfolio[{which}]: {len(new)} nieuwe dag(en) gelogd (vanaf {FORWARD_START}); totaal {len(logged) + len(new)}")


if __name__ == "__main__":
    os.makedirs("results/port", exist_ok=True); os.makedirs("forward", exist_ok=True)
    for w in (1, 2):
        backtest(w) if "--backtest" in sys.argv else forward(w)
