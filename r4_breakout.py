"""R4: Donchian 20/10 + ATR-trailing op H4, 7 kosten-lage FX/goud, volgens PREREG_R4.md."""
import csv
import math
from collections import defaultdict

import numpy as np

import q1b_products as qb
from b4_sim import load
from r1_fx_ml import comm_frac

SYMS = ["EURUSD", "GBPUSD", "USDJPY", "USDCAD", "USDCHF", "XAUUSD", "GBPJPY"]
SWAP = {r["symbol"]: (float(r["long_pct_yr"]) / 100, float(r["short_pct_yr"]) / 100)
        for r in csv.DictReader(open("data/swap_specs_fx.csv"), delimiter=";")}


def h4(sym):
    g = defaultdict(list)
    for b in load(sym):
        g[b[0].replace(hour=b[0].hour // 4 * 4, minute=0)].append(b)
    out = []
    for k in sorted(g):
        bs = g[k]
        out.append((k, bs[0][1], max(x[2] for x in bs), min(x[3] for x in bs), bs[-1][4], bs[-1][5]))
    return out


def sleeve(sym, atr_norm):
    bars = h4(sym)
    t = [b[0] for b in bars]; h = np.array([b[2] for b in bars]); l = np.array([b[3] for b in bars])
    c = np.array([b[4] for b in bars]); sp = np.array([b[5] for b in bars])
    tr = np.maximum(h[1:] - l[1:], np.maximum(abs(h[1:] - c[:-1]), abs(l[1:] - c[:-1])))
    atr = np.r_[np.nan, np.convolve(tr, np.ones(20) / 20, mode="full")[:len(tr)]]
    trades, pnl_bar = [], np.zeros(len(c))  # pnl_bar: P&L als fractie van equity per H4-bar (mark-to-market)
    pos = None
    for i in range(21, len(c)):
        if pos:
            side, ep, w, ext, esp, et = pos
            pnl_bar[i] += side * w * (c[i] / c[i - 1] - 1)
            nights = (t[i].date() - t[i - 1].date()).days
            if nights:
                sw = SWAP[sym][0] if side > 0 else SWAP[sym][1]
                pnl_bar[i] += w * sw * nights / 365
            ext = max(ext, c[i]) if side > 0 else min(ext, c[i])
            ch_exit = c[i] < l[i - 10:i].min() if side > 0 else c[i] > h[i - 10:i].max()
            trail = c[i] < ext - 3 * atr[i] if side > 0 else c[i] > ext + 3 * atr[i]
            if ch_exit or trail:
                cost = (esp if side > 0 else sp[i]) / ep + 2 * comm_frac(sym, ep)
                pnl_bar[i] -= w * cost
                gross = side * (c[i] / ep - 1)
                trades.append((t[i].year, gross - cost, gross))
                pos = None
                continue
            pos = (side, ep, w, ext, esp, et)
        if pos is None and np.isfinite(atr[i]) and atr[i] > 0:
            side = 1 if c[i] > h[i - 20:i].max() else (-1 if c[i] < l[i - 20:i].min() else 0)
            if side:
                w = (1 / 7) * atr_norm / (atr[i] / c[i])
                pos = (side, c[i], w, c[i], sp[i], t[i])
    return t, pnl_bar, trades


def main():
    # normalisatie van de grootte (alleen schaal): mediane ATR% over alle symbolen
    atrp = []
    for s in SYMS:
        b = h4(s); c = np.array([x[4] for x in b]); h = np.array([x[2] for x in b]); l = np.array([x[3] for x in b])
        atrp.append(np.nanmedian((h - l) / c))
    norm = float(np.median(atrp))
    daily = defaultdict(float); dayminpath = defaultdict(list); alltr = []
    for s in SYMS:
        t, pb, tr = sleeve(s, norm)
        alltr += [(y, n, g, s) for y, n, g in tr]
        for ti, p in zip(t, pb):
            daily[ti.date()] += p
            dayminpath[ti.date()].append((ti, p))
    days = sorted(daily)
    r = np.array([daily[d] for d in days])
    dip = []
    for d in days:  # grootste tussentijdse daling binnen de dag op H4-resolutie
        cum, mn = 0.0, 0.0
        for _, p in sorted(dayminpath[d]):
            cum += p; mn = min(mn, cum)
        dip.append(-mn)
    dip = np.array(dip)
    x = np.array([a[1] for a in alltr]); tt = lambda v: v.mean() / v.std(ddof=1) * math.sqrt(len(v))
    trn = np.array([a[1] for a in alltr if a[0] <= 2023]); tst = np.array([a[1] for a in alltr if a[0] >= 2024])
    sr = r.mean() / r.std() * math.sqrt(252); sk = float((((r - r.mean()) / r.std()) ** 3).mean())
    tskew = float((((x - x.mean()) / x.std()) ** 3).mean())
    print(f"R4 Donchian 20/10 + 3×ATR-trailing (H4), 7 symbolen: N {len(x)} | netto {x.mean()*1e4:+.1f} bp/trade (bruto {np.mean([a[2] for a in alltr])*1e4:+.1f}) | "
          f"t train {tt(trn):+.2f} (N {len(trn)}) | t test {tt(tst):+.2f} (N {len(tst)}) | trade-skew {tskew:+.2f}")
    print(f"   dagreeks: SR {sr:+.2f} | skew {sk:+.2f} | jaarvol {r.std()*math.sqrt(252)*100:.1f}% | max dagdip {dip.max()*100:.2f}% | "
          f"per jaar " + " ".join(f"{y}:{r[[d.year == y for d in days]].sum()*100:+.1f}%" for y in sorted({d.year for d in days})))
    per = defaultdict(list)
    for a in alltr:
        per[a[3]].append(a[1])
    print("   per symbool (bp, t): " + " ".join(f"{s}:{np.mean(v)*1e4:+.0f}/{tt(np.array(v)):+.1f}" for s, v in per.items()))
    ok = tt(trn) >= 3 and tt(tst) >= 3 and sk > 0 and sr >= 1.0
    print(f"   → {'GESLAAGD' if ok else 'AFGEWEZEN'} (t ≥ 3 train én test, dag-skew > 0, dag-SR ≥ 1,0)")
    for p in ("2step", "scaling"):
        qb.SCALES = [0.5, 1, 2, 3, 4, 6, 8]
        tsc, net, pl, fu = qb.best(r, dip, p)
        print(f"   Q1b-frontier {p}: beste schaal {tsc}× → netto €{net:,.0f}/mnd, P(netto<0) {pl*100:.0f}%, funded {fu*100:.0f}%")


if __name__ == "__main__":
    main()
