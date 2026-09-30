"""N7 (geen trial): cluster-audit van kernresultaten — per-trade-t vs dag-geclusterde t; dagreeksen: gewone t vs Newey-West (lag 5) en blok-bootstrap."""
import csv, math
from collections import defaultdict
import numpy as np

def t(x): x = np.asarray(x, float); return x.mean() / x.std(ddof=1) * math.sqrt(len(x))
def nw_t(x, L=5):
    x = np.asarray(x, float); n = len(x); e = x - x.mean(); g0 = e @ e / n
    s = g0 + 2 * sum((1 - k / (L + 1)) * (e[k:] @ e[:-k] / n) for k in range(1, L + 1))
    return x.mean() / math.sqrt(s / n)
def boot_t(x, B=2000, blk=21, seed=1):
    x = np.asarray(x, float); n = len(x); rng = np.random.default_rng(seed); m = []
    for _ in range(B):
        st = rng.integers(0, n, n // blk + 1); idx = ((st[:, None] + np.arange(blk)).ravel() % n)[:n]; m.append(x[idx].mean())
    return x.mean() / np.std(m, ddof=1)
def clustered(trades):  # trades: (dag, net)
    by = defaultdict(list)
    for d, n in trades: by[d].append(n)
    dm = [np.mean(v) for v in by.values()]
    return t([n for _, n in trades]), t(dm), len(trades), len(by)
def daily(path):
    r, prev = [], None
    for x in csv.DictReader(open(path), delimiter=";"):
        e = float(x["end_equity"]); p = float(x["start_balance"]) if prev is None else prev
        r.append(e / p - 1); prev = e
    return [v for v in r]

rows = []
# ORB B4a
orb = [(l.split(";")[0], float(l.split(";")[2])) for l in open("results/b4/B4_a_ORB_trades.csv") if l[0].isdigit()]
rows.append(("ORB-B4a FTMO 2021–26 (7 symbolen)", "per trade → dag", *clustered(orb)))
orb4 = [(l.split(";")[0], float(l.split(";")[2])) for l in open("results/b4/B4_a_ORB_trades.csv") if l[0].isdigit() and l.split(";")[1] in ("US500cash", "US100cash", "GER40cash", "XAUUSD")]
rows.append(("ORB-B4a S3-set (US500, US100, GER40, XAU)", "per trade → dag", *clustered(orb4)))
# S1(a)
import s1_noise
s1 = []
for s in s1_noise.SYMS:
    tr, _ = s1_noise.run(s1_noise.prepare(s), 30, True, 14); s1 += [(d, g - c) for d, g, c in tr]
rows.append(("S1(a) noise-area FTMO 2021–26", "per trade → dag", *clustered(s1)))
# K1 (nachten, max 1/2 nachten; Yahoo + FTMO)
import k1_nights as k, e1_rsi2_ftmo as e1, statistics
RF = k.RF if hasattr(k, "RF") else k.rf_fn()
for label, src in (("Yahoo", "y"), ("FTMO", "f")):
    var = {"a": [], "b": []}
    if src == "y":
        for name in ("SPY", "QQQ", "GLD", "DAX", "N225"):
            _, v = k.analyse(k.yahoo_rows(name), lambda i: 0.0002, lambda kk: 0.0002, lambda d, n: (RF(d) + 0.02) * n / 365)
            for q in v: var[q] += v[q]
    else:
        for sym in e1.SWAP_LONG:
            rws = k.ftmo_rows(sym); eod = e1.eod_spread_frac(sym); osp = statistics.median([r[3] for r in rws])
            _, v = k.analyse([(r[0], r[1], r[2]) for r in rws], lambda i: eod, lambda kk: osp, lambda d, n, sw=e1.SWAP_LONG[sym]: sw * n / 365)
            for q in v: var[q] += v[q]
    for q, lab in (("a", "max 1 nacht"), ("b", "max 2 nachten")):
        rows.append((f"K1 {lab} {label}", "per trade → dag", *clustered(var[q])))
# dagreeksen
for label, path in (("B2b RSI(2) Yahoo gepoold 1990–2026", "results/b2/B2_b_daily.csv"), ("F3b RSI(2)+ORB MT5 2021–26", "results/f/F3b_comb_daily.csv"),
                    ("F2 ORB MT5 2021–26", "results/f/F2_ORB_daily.csv")):
    r = [x for x in daily(path)]
    rows.append((label, "dagreeks: t → NW / bootstrap", t(r), nw_t(r), len(r), boot_t(r)))
with open("RESULTATEN_GECLUSTERD.md", "w") as f:
    f.write("# RESULTATEN_GECLUSTERD (N7, 2026-09-30) — oude t vs geclusterde/autocorrelatie-robuuste t\n\n")
    f.write("Trade-resultaten: per-trade-t vs **dag-geclusterd** (gemiddelde per dag, t over dagen). Dagreeksen: gewone t vs **Newey-West (lag 5)** en blok-bootstrap (21 d).\n\n")
    f.write("| resultaat | methode | oude t | nieuwe t | N (trades/dagen) | N-dagen / bootstrap-t |\n|---|---|---|---|---|---|\n")
    for name, how, a, b, n, m in rows:
        last = f"{m}" if isinstance(m, int) else f"bootstrap-t {m:.2f}"
        f.write(f"| {name} | {how} | {a:+.2f} | **{b:+.2f}** | {n} | {last} |\n")
        print(f"{name:<40} {how:<30} oud {a:+.2f} → nieuw {b:+.2f} | N {n} | {last}")
