"""S3: bevroren B4a-ORB op HistData 2011–2020 (data/long_m5), beslisregel volgens PREREG_S3.md.
Gebruik: python s3_run.py [m5-map]   (voorlopige uitslag als niet alle symbolen er zijn)"""
import math
import os
import sys
from collections import defaultdict
from datetime import datetime

import numpy as np

import b4_sim

SRC = sys.argv[1] if len(sys.argv) > 1 else "data/long_m5"
ORDER = ["US500cash", "US100cash", "GER40cash", "XAUUSD"]
_orig_load = b4_sim.load


def load_long(sym):
    point, bars = None, []
    for line in open(os.path.join(SRC, f"{sym}.csv")):
        if line.startswith("#"):
            point = float(line.split("point=")[1].split(";")[0]); continue
        if not line[0].isdigit():
            continue
        t, o, h, l, c, sp = line.rstrip().split(";")
        bars.append((datetime.strptime(t, "%Y.%m.%d %H:%M"), float(o), float(h), float(l), float(c), int(sp) * point))
    return bars


def run(spread_mult=1.0):
    b4_sim.load = load_long
    out = []
    try:
        for s in ORDER:
            if not os.path.exists(os.path.join(SRC, f"{s}.csv")):
                continue
            sess = b4_sim.sessions(s)
            if spread_mult != 1.0:
                sess = [(d, [b[:5] + (b[5] * spread_mult,) for b in bars]) for d, bars in sess]
            out += [(d, s, n) for d, n, _ in b4_sim.run_orb(sess, b4_sim.SYMS[s][3])]
    finally:
        b4_sim.load = _orig_load
    return out


def clustered_t(trades):
    by = defaultdict(list)
    for d, _, n in trades:
        by[d].append(n)
    x = np.array([np.mean(v) for v in by.values()])
    return x.mean() / x.std(ddof=1) * math.sqrt(len(x)) if len(x) > 2 else float("nan"), len(x)


def ref_2021_26(syms):
    tr = []
    for line in open("results/b4/B4_a_ORB_trades.csv"):
        if line[0].isdigit():
            d, s, n, _ = line.strip().split(";")
            if s in syms:
                tr.append((datetime.strptime(d, "%Y-%m-%d").date(), s, float(n)))
    return tr


def main():
    tr = run()
    syms = sorted({s for _, s, _ in tr}, key=ORDER.index)
    full = set(syms) >= {"US500cash", "US100cash", "GER40cash"}
    print(f"S3 {'DEFINITIEF' if full else 'VOORLOPIG (niet alle symbolen)'} — symbolen: {', '.join(syms)} | N {len(tr)}")
    net = np.array([n for _, _, n in tr]); mean_bp = net.mean() * 1e4
    t, ndays = clustered_t(tr)
    h1 = [n for d, _, n in tr if d.year <= 2015]; h2 = [n for d, _, n in tr if d.year >= 2016]
    per = {s: np.array([n for _, x, n in tr if x == s]) for s in syms}
    pos3 = sum(per[s].mean() > 0 for s in ("US500cash", "US100cash", "GER40cash") if s in per)
    t50, _ = clustered_t(run(1.5))
    print(f"   gemiddeld {mean_bp:+.2f} bp/trade | dag-geclusterde t {t:+.2f} ({ndays} dagen) | 2011–15 {np.mean(h1)*1e4:+.2f} bp (N {len(h1)}) | "
          f"2016–20 {np.mean(h2)*1e4:+.2f} bp (N {len(h2)}) | +50% spread t {t50:+.2f}")
    print("   per symbool (bp, t, N): " + " ".join(f"{s}:{v.mean()*1e4:+.2f}/{v.mean()/v.std(ddof=1)*math.sqrt(len(v)):+.1f}/{len(v)}" for s, v in per.items()))
    ref = ref_2021_26(syms)
    yr = defaultdict(list)
    for d, _, n in tr + ref:
        yr[d.year].append(n)
    print("   jaar-per-jaar bp (2011–20 HistData, 2021–26 FTMO): " + " ".join(f"{y}:{np.mean(v)*1e4:+.1f}" for y, v in sorted(yr.items())))
    ref_mean = np.mean([n for _, _, n in ref]) * 1e4; ref_2426 = np.mean([n for d, _, n in ref if d.year >= 2024]) * 1e4
    confirmed = t >= 2.0 and np.mean(h1) > 0 and np.mean(h2) > 0 and mean_bp >= 0.9 and pos3 >= 2
    rejected = t < 1 or mean_bp <= 0.5
    if confirmed:
        label = "BEVESTIGD + BLIJVEND" if ref_mean >= 0.9 and ref_2426 >= 0 else "BEVESTIGD MAAR VERVALLEN"
    else:
        label = "VERWORPEN" if rejected else "ONBESLIST"
    print(f"   referentie FTMO 2021–26 op dezelfde symbolen: {ref_mean:+.2f} bp/trade, 2024–26 {ref_2426:+.2f} bp")
    print(f"   → {label}{'' if full else ' (voorlopig; geen beslissing)'}")


if __name__ == "__main__":
    main()
