"""K1: RSI(2)-edge per houdnacht + varianten max 1 / max 2 nachten, volgens PREREG_K1.md."""
import bisect
import csv
import math
import statistics
from collections import defaultdict
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import e1_rsi2_ftmo as e1
from b2_sim import rsi2
from b4_sim import NY, SYMS, load as load_m5


def rf_fn():
    ks, vs = [], []
    for r in csv.DictReader(open("data/fred/DTB3.csv")):
        if r["DTB3"] not in (".", ""):
            ks.append(datetime.strptime(r["observation_date"], "%Y-%m-%d").date()); vs.append(float(r["DTB3"]) / 100)
    return lambda d: vs[max(0, bisect.bisect_right(ks, d) - 1)]


RF = rf_fn()


def yahoo_rows(name):
    out = []
    for r in csv.DictReader(open(f"data/ohlc/{name}.csv"), delimiter=";"):
        out.append((datetime.strptime(r["date"], "%Y.%m.%d").date(), float(r["open"]), float(r["close"])))
    return [x for x in out if x[0].year >= 1990]


def ftmo_rows(sym):
    """(sessiedatum, cash-open, D1-slot, open-spread-frac)"""
    tzname, (oh, om), _, _ = SYMS[sym]
    tz = ZoneInfo(tzname)
    opens = {}
    for b in load_m5(sym):
        loc = (b[0] - timedelta(hours=7)).replace(tzinfo=NY).astimezone(tz)
        if (loc.hour, loc.minute) == (oh, om):
            opens[loc.date()] = (b[1], b[5] / b[1])
    closes = e1.ftmo_close(sym)
    return [(d, opens[d][0], c, opens[d][1]) for d, c in closes if d in opens]


def analyse(rows, entry_cost, exit_cost_fn, fin_fn):
    d = [r[0] for r in rows]; o = [r[1] for r in rows]; c = [r[2] for r in rows]
    rs = rsi2(c)
    sma = [statistics.mean(c[i - 199:i + 1]) if i >= 199 else None for i in range(len(c))]
    seg = defaultdict(list)  # ('N',k)/('D',k) -> rendementen
    i = 1
    while i < len(c) - 1:
        if rs[i] is not None and sma[i] and rs[i] < 10 and c[i] > sma[i]:
            j = next((k for k in range(i + 1, len(c)) if rs[k] is not None and rs[k] > 70), len(c) - 1)
            for k in range(1, j - i + 1):
                kk = min(k, 4)
                seg[("N", kk)].append(o[i + k] / c[i + k - 1] - 1)
                seg[("D", kk)].append(c[i + k] / o[i + k] - 1)
            i = j + 1
        else:
            i += 1
    var = {"a": [], "b": []}
    for v in ("a", "b"):
        i = 1
        while i < len(c) - 2:
            if rs[i] is not None and sma[i] and rs[i] < 10 and c[i] > sma[i]:
                if v == "a":
                    k, px, ex_day = i + 1, o[i + 1], d[i + 1]
                elif rs[i + 1] is not None and rs[i + 1] > 70:
                    k, px, ex_day = i + 1, c[i + 1], d[i + 1]
                else:
                    k, px, ex_day = i + 2, o[i + 2], d[i + 2]
                net = px / c[i] - 1 - entry_cost(i) - exit_cost_fn(k) - fin_fn(d[i], (ex_day - d[i]).days)
                var[v].append((d[i], net))
                i = k  # na uitstap opnieuw kijken vanaf die dag
                continue
            i += 1
    return seg, var


def tstat(x):
    return statistics.mean(x) / statistics.stdev(x) * math.sqrt(len(x)) if len(x) > 2 else float("nan")


def show_seg(label, seg):
    print(f"  {label} — gemiddeld rendement per segment (bp, t, N):")
    for k in (1, 2, 3, 4):
        n, dd = seg.get(("N", k), []), seg.get(("D", k), [])
        if n:
            print(f"     nacht {k if k < 4 else '4+'}: {statistics.mean(n)*1e4:+6.1f} bp (t {tstat(n):+.2f}, N {len(n)}) | "
                  f"dag {k if k < 4 else '4+'}: {statistics.mean(dd)*1e4:+6.1f} bp (t {tstat(dd):+.2f})")


def main():
    y_seg, y_var = defaultdict(list), {"a": [], "b": []}
    for name in ("SPY", "QQQ", "GLD", "DAX", "N225"):
        rows = yahoo_rows(name)
        seg, var = analyse(rows, lambda i: 0.0002, lambda k: 0.0002, lambda d, n: (RF(d) + 0.02) * n / 365)
        for k, v in seg.items():
            y_seg[k] += v
        for v in var:
            y_var[v] += var[v]
    f_seg, f_var = defaultdict(list), {"a": [], "b": []}
    for sym in e1.SWAP_LONG:
        rows = ftmo_rows(sym)
        eod = e1.eod_spread_frac(sym)
        osp = statistics.median([r[3] for r in rows])
        seg, var = analyse([(r[0], r[1], r[2]) for r in rows], lambda i: eod, lambda k: osp,
                           lambda d, n, sw=e1.SWAP_LONG[sym]: sw * n / 365)
        for k, v in seg.items():
            f_seg[k] += v
        for v in var:
            f_var[v] += [(d, n, sym) for d, n in var[v]]
    show_seg("Yahoo 1990–2026 (SPY, QQQ, GLD, DAX, N225)", y_seg)
    show_seg("FTMO 2021–2026 (6 symbolen)", f_seg)
    for v, label in (("a", "(a) max 1 nacht"), ("b", "(b) max 2 nachten")):
        yx = [n for _, n in y_var[v]]
        fx = [n for _, n, _ in f_var[v]]
        # FTMO-dagverlies bij schaal voor €150/mnd: som van verliezen van posities met dezelfde instapdatum
        yrs = 5.7
        per_unit = sum(fx) * 80000 / (yrs * 12)
        f = 150 / per_unit if per_unit > 0 else float("inf")
        by = defaultdict(float)
        for d, n, _ in f_var[v]:
            by[d] += min(0.0, n)
        worst = -min(by.values()) * f if per_unit > 0 else float("nan")
        ok = tstat(yx) >= 2.5 and tstat(fx) >= 2.5 and worst < 0.04
        print(f"{label}: Yahoo N {len(yx)}, {statistics.mean(yx)*1e4:+.1f} bp, t {tstat(yx):+.2f} | FTMO N {len(fx)}, "
              f"{statistics.mean(fx)*1e4:+.1f} bp, t {tstat(fx):+.2f} | schaal voor €150/mnd {f:.2f}× per positie → "
              f"slechtste nacht {worst*100:.2f}% → {'GESLAAGD' if ok else 'afgewezen'}")


if __name__ == "__main__":
    main()
