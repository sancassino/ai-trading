"""G3-H2 (Double 7s) en G3-H3 (RSI(2) alleen in hoog-vol-regime), volgens VOORSTEL_F.md."""
import math, statistics
from datetime import date
import stats_tools as st
import e1_rsi2_ftmo as e1
from b2_sim import END, MARKUP, SPREAD, START, UNIV, load, rate, rsi2

def sleeve(d, c, start, mode, spread, fin):
    """mode: 'd7' (Double 7s), 'rsi', 'rsihv' (RSI(2) + hoog-vol-filter). fin(d_prev, nights) -> financieringsfractie."""
    rs = rsi2(c)
    ret, inpos = {}, False
    rets = [0.0] + [c[i] / c[i - 1] - 1 for i in range(1, len(c))]
    for i in range(1, len(c)):
        if d[i] > END: break
        r = 0.0
        if inpos:
            r += c[i] / c[i - 1] - 1 - fin(d[i - 1], (d[i] - d[i - 1]).days)
        sma = statistics.mean(c[i - 199:i + 1]) if i >= 199 else None
        if mode == "d7":
            exit_ = inpos and i >= 6 and c[i] >= max(c[i - 6:i + 1])
            entry = (not inpos) and i >= 6 and sma and c[i] <= min(c[i - 6:i + 1]) and c[i] > sma
        else:
            exit_ = inpos and rs[i] is not None and rs[i] > 70
            entry = (not inpos) and rs[i] is not None and sma and rs[i] < 10 and c[i] > sma
            if entry and mode == "rsihv":
                if i < 272: entry = False
                else:
                    rv = lambda j: statistics.stdev(rets[j - 19:j + 1])
                    entry = rv(i) > statistics.median([rv(j) for j in range(i - 251, i + 1, 5)])
        if exit_:
            inpos = False; r -= spread
        elif entry and d[i] >= start:
            inpos = True; r -= spread
        if d[i] >= start:
            ret[d[i]] = r
    return ret

def pooled(sl):
    days = sorted({x for r, s in sl for x in r})
    return [(x, statistics.mean(r.get(x, 0.0) for r, s in sl if x >= s)) for x in days]

def yahoo(mode):
    sl = []
    for fn, start in UNIV["abd"].values():
        rows = load(fn)
        sl.append((sleeve([x[0] for x in rows], [x[4] for x in rows], start, mode, SPREAD,
                          lambda dp, n: (rate(dp) + MARKUP) / 365 * n), start))
    return [(x, r) for x, r in pooled(sl) if x >= START]

def ftmo(mode):
    sl = []
    for s in e1.SWAP_LONG:
        rows = e1.ftmo_close(s)
        r = sleeve([x[0] for x in rows], [x[1] for x in rows], date(2019, 1, 1), mode, e1.eod_spread_frac(s),
                   lambda dp, n, sw=e1.SWAP_LONG[s]: sw * n / 365)
        sl.append(({k: v for k, v in r.items() if e1.LO <= k <= e1.HI}, e1.LO))
    return pooled(sl)

def rep(label, p, n_trials=385):
    x = [r for _, r in p]
    h1 = math.prod(1 + r for d, r in p if date(1995, 1, 1) <= d <= date(2010, 12, 31)) - 1
    h2 = math.prod(1 + r for d, r in p if d >= date(2011, 1, 1)) - 1
    print(f"  {label:<30} SR {st.sharpe(x)[0]:+.2f} t {st.t_stat(x):+.2f} | 1995–2010 {h1*100:+.1f}% | 2011–26 {h2*100:+.1f}% | "
          f"totaal {(math.prod(1+r for r in x)-1)*100:+.1f}% | DSR{n_trials} {st.deflated_sharpe(x, n_trials)[0]:.2f}")
    return st.sharpe(x)[0], st.t_stat(x), h1, h2, st.deflated_sharpe(x, n_trials)[0], math.prod(1 + r for r in x) - 1

print("H2 Double 7s:")
y = rep("Yahoo 1990–2026 gepoold", yahoo("d7"))
f = rep("FTMO 2021–26 gepoold (6)", ftmo("d7"))
ok = y[1] >= 3 and y[2] > 0 and y[3] > 0 and y[4] >= 0.5 and f[5] > 0
print(f"  → H2 {'GESLAAGD' if ok else 'afgewezen'}")
print("H3 RSI(2) in hoog-vol-regime vs RSI(2):")
yb = rep("Yahoo RSI(2) basis", yahoo("rsi")); yh = rep("Yahoo RSI(2) hoog-vol", yahoo("rsihv"))
fb = rep("FTMO RSI(2) basis", ftmo("rsi")); fh = rep("FTMO RSI(2) hoog-vol", ftmo("rsihv"))
ok = yh[0] - yb[0] >= 0.15 and fh[0] >= fb[0]
print(f"  → H3 ΔSR Yahoo {yh[0]-yb[0]:+.2f}, FTMO {fh[0]-fb[0]:+.2f} → {'GESLAAGD' if ok else 'afgewezen'}")
