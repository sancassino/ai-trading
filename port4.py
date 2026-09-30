"""PREREG_PORT4 (SHA in RUNLOG): P-ETF-lite = ALLOCATIE_V1_2 §2 op instrumentniveau. Geen trial, geen selectie.
Gebruik: python port4.py → results/port/PORT4_backtest.md (ontdekking ≤ 2024);  python port4.py --forward → forward/portfolio4_daily.csv"""
import bisect
import math
import os
import sys
from datetime import date, datetime, timezone

import numpy as np

import catalogus.C52_allweather as C52
import forward_portfolio as FP
from engine.run_rule import load_daily, rf_on

CAP = 80000.0
DISC = date(2024, 12, 31)
FORWARD_START = date(2026, 10, 1)
OUT = "forward/portfolio4_daily.csv"
INST = ["SP", "BOND", "GOLD"]
TER = {"SP": 0.07, "BOND": 0.10, "GOLD": 0.12}


def ffill_on(dates_src, vals, cal):
    ks = list(dates_src); out = np.full(len(cal), np.nan)
    for i, d in enumerate(cal):
        j = bisect.bisect_right(ks, d) - 1
        if j >= 0:
            out[i] = vals[j]
    return out


def build():
    sp_tr = load_daily("SPX_TR", "adjclose"); cal = list(sp_tr["date"])
    spx = load_daily("SPX", "close")
    px = {"SP": sp_tr["close"], "BOND": ffill_on(*(lambda d: (d["date"], d["close"]))(load_daily("BOND10_SYN", "close")), cal),
          "GOLD": ffill_on(*(lambda d: (d["date"], d["close"]))(load_daily("GOLD_F", "close")), cal)}
    n = len(cal)
    R = {k: np.r_[np.nan, px[k][1:] / px[k][:-1] - 1] for k in INST}
    # --- sleeve A: C52 lang-gewichten (maandeinde), uitgevoerd per kwartaal ---
    R52 = C52.RULE; p52 = R52["varianten"]["lang"]
    d52 = {m: load_daily(m, R52.get("field", "adjclose")) for m in R52["instrumenten"]}
    pos52 = C52.positions_all(d52, p52)
    map52 = {"SP": "SPY", "BOND": "BOND10_SYN", "GOLD": "GOLD_F"}
    w52 = {k: ffill_on(d52[map52[k]]["date"], np.nan_to_num(pos52[map52[k]]), cal) for k in INST}
    first_td = [i == 0 or cal[i].month != cal[i - 1].month for i in range(n)]
    quarter = [first_td[i] and cal[i].month in (1, 4, 7, 10) for i in range(n)]
    A = {k: np.zeros(n) for k in INST}; cur = {k: 0.0 for k in INST}
    for i in range(n):
        if quarter[i] and i > 0:
            cur = {k: float(np.nan_to_num(w52[k][i - 1])) for k in INST}     # gewichten van het laatste maandeinde vóór de kwartaaldag
        for k in INST:
            A[k][i] = cur[k]
    # --- sleeve B: Faber alleen SPX, flip uitgevoerd op de eerste handelsdag van de volgende maand ---
    spx_c = ffill_on(spx["date"], spx["close"], cal)
    me_idx = [i for i in range(n) if i + 1 == n or cal[i + 1].month != cal[i].month]
    sig = {}
    for j in range(9, len(me_idx)):
        i = me_idx[j]; sig[i] = 1.0 if spx_c[i] > np.mean([spx_c[k] for k in me_idx[j - 9:j + 1]]) else 0.0
    B = np.zeros(n); b = 0.0; pending = None; flip = np.zeros(n, bool)
    for i in range(n):
        if first_td[i] and pending is not None:
            if pending != b:
                flip[i] = True
            b = pending; pending = None
        B[i] = b
        if i in sig:
            pending = sig[i]
    # --- sleeve-rendementen (positie van gisteren) en 1/σ60-combinatie, maandelijks ---
    ra = np.array([sum(A[k][i - 1] * np.nan_to_num(R[k][i]) for k in INST) if i else 0.0 for i in range(n)])
    rb = np.array([B[i - 1] * np.nan_to_num(R["SP"][i]) if i else 0.0 for i in range(n)])
    W = np.full((2, n), np.nan); cw = None
    for i in range(n):
        if first_td[i] and i >= 61:
            s = np.array([ra[i - 60:i].std(), rb[i - 60:i].std()]) * math.sqrt(252)
            if np.all(s > 0):
                cw = (1 / s) / (1 / s).sum()
        if cw is not None:
            W[:, i] = cw
    T = []
    for i in range(n):
        if not np.isfinite(W[0, i]):
            T.append(None); continue
        t = {k: W[0, i] * A[k][i] for k in INST}; t["SP"] += W[1, i] * B[i]
        T.append(t)
    return cal, R, T, quarter, flip


def simulate(cal, R, T, quarter, flip, model, thr=0.02):
    n = len(cal); nights = np.r_[0, [(b - a).days for a, b in zip(cal[:-1], cal[1:])]]
    rf = rf_on(cal) / 100 / 365 * nights
    h = {k: 0.0 for k in INST}; cash = 1.0; V = 1.0; prev = None; started = False
    tot = np.full(n, np.nan); ntr = np.zeros(n); turn = np.zeros(n); costs = np.zeros(n)
    for i in range(n):
        if started:
            r = sum(h[k] * np.nan_to_num(R[k][i]) for k in INST) + cash * rf[i] - sum(h[k] * TER[k] for k in INST) / 100 / 365 * nights[i]
            for k in INST:
                h[k] = h[k] * (1 + np.nan_to_num(R[k][i])) / (1 + r)
            cash = cash * (1 + rf[i]) / (1 + r); V *= 1 + r; tot[i] = r
        t = T[i]
        if t is None:
            continue
        started = True
        changed = prev is None or any(abs(t[k] - prev[k]) > 1e-12 for k in INST)
        prev = t
        if not changed and not quarter[i] and not flip[i]:
            continue
        c = 0.0
        for k in INST:
            dl = t[k] - h[k]
            force = quarter[i] or (flip[i] and k == "SP")
            if abs(dl) > 1e-9 and (force or abs(dl) >= thr):
                c += (3.50 / (CAP * V) + abs(dl) * 1.5e-4) if model == "B" else abs(dl) * 6.5e-4
                h[k] = t[k]; cash -= dl; ntr[i] += 1; turn[i] += abs(dl)
        cash -= c; costs[i] = c
        if np.isfinite(tot[i]):
            tot[i] -= c
    return tot, ntr, turn, costs, rf


def report():
    cal, R, T, q, f = build(); D = np.array(cal)
    lines = ["# PORT4 — P-ETF-lite (PREREG_PORT4; ontdekking ≤ 2024; geen trial)", "",
             "| kosten | periode | SR (excess) | CAGR | maxDD | alfa/jr | transacties/jr | omloop/jr | kosten €/jr | alfa €/mnd |", "|---|---|---|---|---|---|---|---|---|---|"]
    for m in ("B", "A"):
        tot, ntr, turn, costs, rf = simulate(cal, R, T, q, f, m)
        for lo, per in ((date(2001, 1, 1), "2001–24"), (date(2011, 1, 1), "2011–24"), (date(2021, 1, 1), "2021–24")):
            sel = (D >= lo) & (D <= DISC) & np.isfinite(tot)
            t, e = tot[sel], tot[sel] - rf[sel]; yrs = sel.sum() / 252
            eq = np.cumprod(1 + t); dd = float(np.max(1 - eq / np.maximum.accumulate(eq))); ex = np.prod(1 + e) ** (1 / yrs) - 1
            lines.append(f"| {m} | {per} | {e.mean()/e.std()*math.sqrt(252):.2f} | {(eq[-1]**(1/yrs)-1)*100:.1f}% | {dd*100:.1f}% | {ex*100:.1f}% | "
                         f"{ntr[sel].sum()/yrs:.0f} | {turn[sel].sum()/yrs:.2f} | {costs[sel].sum()/yrs*CAP:,.0f} | €{CAP*ex/12:,.0f} |")
    lines += ["", "Referentie (PORT3, model B, 2001–24): P-ETF-a-inst SR 0,86 / 153 transacties/jr / €268/jr; P-ETF-a-D1 SR 0,91 / 57/jr / €116/jr.",
              "Beslisregel lite vs L0 (ALLOCATIE_V1_2 §4) en rijen L0–L6: Uitvoerder-2."]
    open("results/port/PORT4_backtest.md", "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


def forward():
    cal, R, T, q, f = build()
    tot, ntr, *_ = simulate(cal, R, T, q, f, "B")
    eu, eh = FP.eur_series(cal, tot)
    logged = set()
    if os.path.exists(OUT):
        logged = {l.split(";")[0] for l in open(OUT) if l[:1].isdigit()}
    else:
        with open(OUT, "w") as fh:
            fh.write("date;P-ETF-lite_usd;P-ETF-lite_eur;P-ETF-lite_eur_hedged;P-ETF-lite_transacties;berekend_utc\n")
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    new = [f"{d.isoformat()};{tot[i]:.8f};{eu[i]:.8f};{eh[i]:.8f};{int(ntr[i])};{ts}" for i, d in enumerate(cal)
           if d >= FORWARD_START and np.isfinite(tot[i]) and d.isoformat() not in logged]
    if new:
        with open(OUT, "a") as fh:
            fh.write("\n".join(new) + "\n")
    print(f"port4 forward: {len(new)} nieuwe dag(en)")


if __name__ == "__main__":
    os.makedirs("results/port", exist_ok=True); os.makedirs("forward", exist_ok=True)
    forward() if "--forward" in sys.argv else report()
