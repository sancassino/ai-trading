"""I2: intraday mean-reversion op H1 (IBS en RSI(2)), exact volgens PREREG_I2.md."""
import math
import statistics
from collections import defaultdict
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import stats_tools as st
from b2_sim import rsi2
from b4_sim import NY, SYMS, TRAIN_END, load

SYM3 = ["US500cash", "US100cash", "GER40cash"]


def h1_bars(sym):
    """H1 per serveruur: (server-uur-start, o, h, l, c, spread, local_close_time)"""
    tzname, (oh, om), (ch, cm), _ = SYMS[sym]
    tz = ZoneInfo(tzname)
    groups = defaultdict(list)
    for b in load(sym):
        groups[b[0].replace(minute=0)].append(b)
    out = []
    for hr in sorted(groups):
        bs = groups[hr]
        last = bs[-1]
        close_srv = last[0] + timedelta(minutes=5)
        local_close = (close_srv - timedelta(hours=7)).replace(tzinfo=NY).astimezone(tz)
        out.append((hr, bs[0][1], max(b[2] for b in bs), min(b[3] for b in bs), last[4], last[5], local_close))
    return out, tz, (oh, om), (ch, cm)


def in_session(t, open_hm, close_hm):
    op = t.replace(hour=open_hm[0], minute=open_hm[1], second=0, microsecond=0)
    cl = t.replace(hour=close_hm[0], minute=close_hm[1], second=0, microsecond=0)
    return op < t <= cl, cl


def run(sym, rule):
    bars, tz, op_hm, cl_hm = h1_bars(sym)
    c = [b[4] for b in bars]
    rs = rsi2(c) if rule == "rsi" else None
    trades = []
    pos = None  # (entry_idx, entry_price, spread, session_close)
    s = 0.0
    sma = [None] * len(c)
    for i in range(len(c)):
        s += c[i]
        if i >= 200:
            s -= c[i - 200]
        if i >= 199:
            sma[i] = s / 200
    for i, (hr, o, h, l, cl, spr, lt) in enumerate(bars):
        inside, sess_close = in_session(lt, op_hm, cl_hm)
        if pos:
            ei, ep, esp, ses_end, day = pos
            # sessie-einde: sluit op het slot van de laatste bar die vóór/op sessie-einde eindigt
            end_now = lt >= ses_end or lt.date() != day
            if rule == "ibs":
                ex = i - ei >= 4
            else:
                ex = rs[i] is not None and rs[i] > 65
            if end_now or ex or not inside:
                px = cl if (inside and not lt > ses_end) else bars[i - 1][4]
                d = day
                trades.append((d, (px - ep) / ep - esp / ep))
                pos = None
        if pos is None and inside and lt < sess_close and sma[i]:
            sig = False
            if rule == "ibs" and h > l:
                sig = (cl - l) / (h - l) < 0.2 and cl > sma[i]
            elif rule == "rsi" and rs[i] is not None:
                sig = rs[i] < 10 and cl > sma[i]
            if sig:
                pos = (i, cl, spr, sess_close, lt.date())
    return trades


def evaluate(name, trades):
    trades.sort()
    nets = [n for _, n in trades]
    tr = [n for d, n in trades if str(d) <= TRAIN_END]
    te = [n for d, n in trades if str(d) > TRAIN_END]
    t = lambda x: statistics.mean(x) / statistics.stdev(x) * math.sqrt(len(x))
    yearly = defaultdict(list)
    for d, n in trades:
        yearly[d.year].append(n)
    pos = sum(sum(v) > 0 for v in yearly.values())
    # schaal: notional per trade (fractie equity) voor ≥ €150/mnd; dagverlies = som verliezende trades per dag
    by_day = defaultdict(list)
    for d, n in trades:
        by_day[d].append(n)
    yrs = (max(by_day) - min(by_day)).days / 365.25
    per_unit_month = sum(nets) * 80000 / (yrs * 12)
    f = 150 / per_unit_month if per_unit_month > 0 else float("inf")
    worst = max(-sum(x for x in v if x < 0) for v in by_day.values()) * f if per_unit_month > 0 else float("nan")
    ok = len(nets) >= 1500 and t(tr) >= 3 and t(te) >= 3 and pos >= 4 and worst < 0.04
    print(f"{name:<18} N {len(nets):>5} | {statistics.mean(nets)*1e4:+.2f} bp | t train {t(tr):+.2f} (N {len(tr)}) | t test {t(te):+.2f} "
          f"(N {len(te)}) | jaren+ {pos}/{len(yearly)} | schaal voor €150/mnd {f:.2f}× notional/trade → slechtste dag {worst*100:.2f}% | "
          f"{'GESLAAGD' if ok else 'afgewezen'}")
    print("    per jaar (bp, N): " + " ".join(f"{y}:{statistics.mean(v)*1e4:+.1f}({len(v)})" for y, v in sorted(yearly.items())))


def main():
    for rule, name in (("ibs", "(a) IBS-H1"), ("rsi", "(b) RSI(2)-H1")):
        allt = []
        for s in SYM3:
            t = run(s, rule)
            print(f"    {name} {s}: N {len(t)}, {statistics.mean([n for _, n in t])*1e4:+.2f} bp")
            allt += t
        evaluate(name, allt)


if __name__ == "__main__":
    main()
