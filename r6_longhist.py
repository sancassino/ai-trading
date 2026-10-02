"""R6 (PREREG_CAT6 §2): risicopariteit-allocatie vs 60/40 op maandreeksen 1973→2024 (SPX, BOND10_SYN, goud Pink Sheet, grondstoffenindex Pink Sheet). Geen trial."""
import math
import numpy as np
from datetime import date
from engine.run_rule import load_daily, rf_on
END = date(2024, 12, 31)
def monthly(name, field="adjclose", folder="daily"):
    d = {}
    import os
    path = next(p for p in (f"data/daily/{name}.csv", f"data/derived/{name}.csv") if os.path.exists(p))
    for l in open(path):
        if l[:1].isdigit():
            a = l.rstrip().split(";"); v = a[5] if a[5] else a[4]
            d[date.fromisoformat(a[0])] = float(v)
    ks = sorted(d); by = {}
    for k in ks: by[(k.year, k.month)] = d[k]           # laatste waarde van de maand
    return by
def pink(name):
    d = {}
    for l in open(f"data/monthly/{name}.csv"):
        if l[:1].isdigit():
            a = l.rstrip().split(";"); x = date.fromisoformat(a[0]); d[(x.year, x.month)] = float(a[4])
    return d
spx = monthly("SPX", "close"); spxtr = monthly("SPX_TR"); bond = monthly("BOND10_SYN"); gold = pink("WB_GOLD"); com = pink("WBIDX_TOTAL_INDEX")
months = sorted(k for k in spx if k in bond and k in gold and k in com and (2024, 12) >= k >= (1972, 12))
def ret(series_, ms, tr=None):
    r = []; 
    for a, b in zip(ms[:-1], ms[1:]):
        if tr is not None and a in tr and b in tr: r.append(tr[b] / tr[a] - 1)
        else: r.append(series_[b] / series_[a] - 1)
    return np.array(r)
ms = months; R = np.vstack([ret(spx, ms, spxtr), ret(bond, ms), ret(gold, ms), ret(com, ms)]); dates = ms[1:]
# rf maandelijks (DTB3 op het maandeinde)
last_day = {}
for l in open("data/daily/SPX.csv"):
    if l[:1].isdigit():
        d = date.fromisoformat(l.split(";")[0]); last_day[(d.year, d.month)] = d
rf = np.array([rf_on([last_day.get(m, date(m[0], m[1], 28))])[0] / 100 / 12 for m in dates])
RT = 6.5e-4; TER = 0.0007 / 12
def rp(idx, win=36, tgt=0.08):
    n = R.shape[1]; W = np.zeros((len(idx), n)); cur = np.zeros(len(idx))
    for t in range(win, n):
        Rw = R[idx][:, t - win:t]; s = Rw.std(axis=1, ddof=1) * math.sqrt(12); w = (1 / s) / (1 / s).sum(); sp = math.sqrt(w @ (np.cov(Rw) * 12) @ w); cur = w * min(1.0, tgt / sp); W[:, t] = cur
    return W
def run(W, idx):
    n = R.shape[1]; Wp = W; turn = np.abs(np.diff(np.c_[np.zeros(len(idx)), W], axis=1)).sum(axis=0)
    x = (Wp * (R[idx] - rf)).sum(axis=0) - turn * RT - np.abs(Wp).sum(axis=0) * TER
    return x
def fixed(w):
    idx = list(range(len(w))); W = np.repeat(np.array(w)[:, None], R.shape[1], axis=1); return W
def stats(x, mask):
    e = x[mask]; t = e + rf[mask]; eq = np.cumprod(1 + t); dd = float(np.max(1 - eq / np.maximum.accumulate(eq)))
    w12 = min(np.prod(1 + t[i:i + 12]) - 1 for i in range(len(t) - 11)) if len(t) >= 12 else float("nan")
    return e.mean() / e.std() * math.sqrt(12), eq[-1] ** (12 / len(t)) - 1, dd, w12
strat = {}
W3 = rp([0, 1, 2]); strat["risicopariteit 3 activa (SPX, obl., goud)"] = (run(W3, [0, 1, 2]))
W4 = rp([0, 1, 2, 3]); strat["risicopariteit 4 activa (+ grondstoffen)"] = run(W4, [0, 1, 2, 3])
strat["60/40 (SPX/obligatie)"] = run(np.vstack([fixed([0.6, 0.4])[:, :], ]), [0, 1])
strat["gelijk gewogen 4 activa (25% elk)"] = run(fixed([0.25] * 4), [0, 1, 2, 3])
strat["alleen SPX (B&H)"] = run(fixed([1.0]), [0])
valid = np.array([i >= 36 for i in range(len(dates))])
periods = [("1976–79 (jaren 70)", 1976, 1979), ("1980s", 1980, 1989), ("1990s", 1990, 1999), ("2000s", 2000, 2009), ("2010s", 2010, 2019), ("2020–24", 2020, 2024), ("2022", 2022, 2022), ("alles (1976→)", 1976, 2024)]
out = ["# R6 — lange-historie-toets structuur (PREREG_CAT6 §2; maandfrequentie, 1973→; ontdekking ≤ 2024; geen trial)", "",
       f"Reeksen: SPX (TR vanaf 1988, daarvoor **prijsindex zonder dividend**: onderschat aandelen in de jaren 70/80), BOND10_SYN (uit ^TNX), goud Pink Sheet (maandgemiddelde, USD), grondstoffenindex Pink Sheet (maandgemiddelde → gladde reeks, lage gemeten vol). Eerste weging na 36 maanden (dus vanaf ≈ 1976). {len(dates)} maanden.", ""]
for lab, a, b in periods:
    mask = valid & np.array([a <= m[0] <= b for m in dates])
    if mask.sum() < 10: continue
    out += [f"**{lab}** ({mask.sum()} mnd)", "", "| strategie | SR (excess) | CAGR totaal | maxDD | slechtste 12 mnd |", "|---|---|---|---|---|"]
    for k, x in strat.items():
        s = stats(x, mask); out.append(f"| {k} | {s[0]:+.2f} | {s[1]*100:+.1f}% | {s[2]*100:.0f}% | {s[3]*100:+.0f}% |")
    out.append("")
open("results/R2/run6_longhist.md", "w").write("\n".join(out) + "\n"); print("\n".join(out))
