"""v28 QA-2 (geen trial): P-ETF-a met C02 vervangen door aandelen-buy-and-hold (zelfde 5 indices, etf, zelfde 1/σ-weging → zelfde risico)
= eerlijke ondergrens nu C02 'alleen DD-filter' is (run 5). Plus frontier (vol-doel 5–12%, hefboom ≤ 2×, rf + 1,5% op geleend deel,
maandelijks, σ 60 d vertraagd) voor 2001–24, 2011–24, 2021–24; DD-budget (D-062: maxDD ≤ 20%); €/mnd alfa boven cash (haircut 30–50% op excess)
+ EUR-cash (€STR nu). Ontdekkingsset ≤ 2024; reserve niet aangeraakt."""
import math
from datetime import date

import numpy as np

import forward_portfolio as FP
from engine.forward import series
from engine.run_rule import load_daily, net_returns_vehicle, rf_on

DISC = date(2024, 12, 31)
IDX5 = ["SPX", "NDX", "DJI", "DAX", "N225"]


def bh_series():
    port = {}
    for n in IDX5:
        df = load_daily(n, "close")
        net, *_ = net_returns_vehicle(df, np.ones(len(df["date"])), 1.0, "etf", True)
        for d, v in zip(df["date"], net):
            if np.isfinite(v):
                port.setdefault(d, []).append(v)
    days = sorted(port); x = np.array([np.mean(port[d]) for d in days])
    nights = np.r_[0, [(b - a).days for a, b in zip(days[:-1], days[1:])]]
    rf = rf_on(days) / 100 / 365 * nights
    return {d: (float(a - r), float(a)) for d, a, r in zip(days, x, rf)}


def petf_levels(S, vol_targets):
    days, P = FP.run_petf(S)
    tot_a, xa, _ = P["P-ETF-a"]
    n = len(days); nights = np.r_[0, [(b - a).days for a, b in zip(days[:-1], days[1:])]]
    rf = rf_on(days) / 100 / 365 * nights
    reb = FP.rebalance_flags(days); valid = np.isfinite(xa)
    out = {}
    for vt in vol_targets:
        k = np.full(n, np.nan); kc = None; cost = np.zeros(n)
        for i in range(n):
            if reb[i] and valid[i]:
                hist = xa[:i][valid[:i]]
                if len(hist) >= 60:
                    sp = hist[-60:].std() * math.sqrt(252)
                    if sp > 0:
                        nk = min(2.0, vt / sp)
                        if kc is not None:
                            cost[i] = abs(nk - kc) * FP.HALF_RT["etf"]
                        kc = nk
            if kc is not None:
                k[i] = kc
        x = k * xa - cost - np.maximum(np.nan_to_num(k) - 1, 0) * FP.SURCHARGE / 365 * nights
        out[vt] = (np.array(days), rf + x, x, k)
    return out


def st(days, tot, x, k, lo, hi=DISC):
    sel = (days >= lo) & (days <= hi) & np.isfinite(tot)
    t, e = tot[sel], x[sel]; yrs = sel.sum() / 252
    eq = np.cumprod(1 + t); dd = float(np.max(1 - eq / np.maximum.accumulate(eq)))
    ex = np.prod(1 + e) ** (1 / yrs) - 1
    return dict(SR=e.mean() / e.std() * math.sqrt(252), CAGR=eq[-1] ** (1 / yrs) - 1, EX=ex, DD=dd, lev=np.nanmean(k[sel]))


estr = float(open("data/daily/YLD_ESTR.csv").read().strip().splitlines()[-1].split(";")[4]) / 100
cash_eur = 80000 * estr / 12
S_base = {"S_C52L": series("C52_allweather", "lang", "etf"), "S_C02": series("C02_faber", "basis", "etf")}
S_bh = {"S_C52L": S_base["S_C52L"], "S_C02": bh_series()}
VT = [0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.12]
lines = ["# v28 QA-2 — P-ETF-a met C02 vervangen door aandelen-B&H (zelfde indices, zelfde 1/σ-weging) + frontier",
         "Ontdekking ≤ 2024 (reserve niet aangeraakt). Alfa = excess t.o.v. USD-cash (≈ EUR-gehedged, zie QA_PETF); €/mnd = alfa × (50–70%) × €80k/12;"
         f" EUR-cash apart: €STR nu {estr*100:.2f}% ≈ €{cash_eur:,.0f}/mnd. Hefboom (> 1×) = 'onbevestigd (broker)' (v26 QA-2). DD-budget: maxDD ≤ 20%.", ""]
for label, S in (("P-ETF-a basis (C02 = Faber)", S_base), ("P-ETF-a met C02 → aandelen-B&H", S_bh)):
    F = petf_levels(S, VT)
    days0, P0 = FP.run_petf(S)
    ta, xa, _ = P0["P-ETF-a"]; dd0 = np.array(days0)
    lines += [f"## {label}", "", "| periode | variant | SR | CAGR | alfa/jr | maxDD | hefboom | alfa €/mnd (haircut 50–30%) | + EUR-cash = totaal €/mnd | DD-budget |",
              "|---|---|---|---|---|---|---|---|---|---|"]
    for lo, lbl in ((date(2001, 1, 1), "2001–24"), (date(2011, 1, 1), "2011–24"), (date(2021, 1, 1), "2021–24")):
        s = st(dd0, ta, xa, np.ones(len(ta)), lo)
        a_lo, a_hi = 80000 * s["EX"] * 0.5 / 12, 80000 * s["EX"] * 0.7 / 12
        lines.append(f"| {lbl} | ongehefeld | {s['SR']:.2f} | {s['CAGR']*100:.1f}% | {s['EX']*100:.1f}% | {s['DD']*100:.1f}% | 1,00 | €{a_lo:,.0f}–{a_hi:,.0f} | "
                     f"€{a_lo+cash_eur:,.0f}–{a_hi+cash_eur:,.0f} | {'ja' if s['DD'] <= 0.20 else 'NEE'} |")
        for vt in VT:
            d, t, x, k = F[vt]; s = st(d, t, x, k, lo)
            a_lo, a_hi = 80000 * s["EX"] * 0.5 / 12, 80000 * s["EX"] * 0.7 / 12
            lines.append(f"| {lbl} | vol {int(vt*100)}% | {s['SR']:.2f} | {s['CAGR']*100:.1f}% | {s['EX']*100:.1f}% | {s['DD']*100:.1f}% | {s['lev']:.2f} | "
                         f"€{a_lo:,.0f}–{a_hi:,.0f} | €{a_lo+cash_eur:,.0f}–{a_hi+cash_eur:,.0f} | {'ja' if s['DD'] <= 0.20 else 'NEE'} |")
    lines.append("")
open("results/port/QA_C02_BH_frontier.md", "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
