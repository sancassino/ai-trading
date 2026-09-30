"""Q3: crypto intraday (BTC/ETH), geen positie over servermiddernacht, exact volgens PREREG_Q3.md."""
import math
import statistics
from collections import defaultdict

import stats_tools as st
from b4_sim import TRAIN_END, load

COMM = 0.0001


def h1(sym):
    groups = defaultdict(list)
    for b in load(sym):
        groups[b[0].replace(minute=0)].append(b)
    out = []
    for hr in sorted(groups):
        bs = groups[hr]
        # (uur, open, slot, spread slotbar, laatste M5-tijd)
        out.append((hr, bs[0][1], bs[-1][4], bs[-1][5], bs[-1][0]))
    return out


def run(sym, rule):
    bars = h1(sym)
    c = [b[2] for b in bars]
    rets = [0.0] + [c[i] / c[i - 1] - 1 for i in range(1, len(c))]
    trades, pos = [], None  # pos = (side, entry_idx, entry_price, entry_spread)
    for i in range(480, len(bars)):
        hr, o, cl, spr, last = bars[i]
        if pos:
            side, ei, ep, esp = pos
            midnight = hr.hour == 23 or (i + 1 < len(bars) and bars[i + 1][0].date() != hr.date())
            if rule == "mom":
                sma = sum(c[i - 47:i + 1]) / 48
                done = i - ei >= 6 or c[i] / c[i - 24] - 1 <= 0 or cl <= sma
            else:
                done = i - ei >= 4
            if done or midnight:
                gross = side * (cl - ep) / ep
                cost = (esp if side > 0 else spr) / ep + 2 * COMM
                trades.append((hr.date(), gross - cost, gross, cost))
                pos = None
                continue
        if pos is None and hr.hour < 22:
            if rule == "mom":
                sma = sum(c[i - 47:i + 1]) / 48
                if c[i] / c[i - 24] - 1 > 0 and cl > sma:
                    pos = (1, i, cl, spr)
            else:
                sd = statistics.pstdev(rets[i - 480:i])
                if sd > 0 and rets[i] < -3 * sd:
                    pos = (1, i, cl, spr)
                elif sd > 0 and rets[i] > 3 * sd:
                    pos = (-1, i, cl, spr)
    return trades


def main():
    for s in ("BTCUSD", "ETHUSD"):
        v = [b[3] / b[2] for b in h1(s)]
        v.sort()
        print(f"{s}: mediaan spread {v[len(v)//2]*1e4:.1f} bp, P90 {v[int(len(v)*0.9)]*1e4:.1f} bp")
    for rule, label in (("mom", "(a) H1-momentum long"), ("rev", "(b) omkeer na 3σ-uur")):
        x = sorted(run("BTCUSD", rule) + run("ETHUSD", rule))
        nets = [t[1] for t in x]
        tr = [t[1] for t in x if str(t[0]) <= TRAIN_END]; te = [t[1] for t in x if str(t[0]) > TRAIN_END]
        tt = lambda v: statistics.mean(v) / statistics.stdev(v) * math.sqrt(len(v)) if len(v) > 2 else float("nan")
        yr = defaultdict(list)
        for t in x:
            yr[t[0].year].append(t[1])
        pos = sum(statistics.mean(v) > 0 for v in yr.values())
        gross = statistics.mean(t[2] for t in x); cost = statistics.mean(t[3] for t in x)
        dsr = st.deflated_sharpe(nets, 398)[0]
        ok = tt(tr) >= 3 and tt(te) >= 3 and len(nets) >= 500 and pos >= 4 and dsr > 0.5 and gross >= 3 * cost
        print(f"{label}: N {len(nets)} | netto {statistics.mean(nets)*1e4:+.1f} bp | bruto {gross*1e4:+.1f} vs kosten {cost*1e4:.1f} bp | "
              f"t train {tt(tr):+.2f} | t test {tt(te):+.2f} | jaren+ {pos}/{len(yr)} | DSR {dsr:.2f} → {'GESLAAGD' if ok else 'afgewezen'}")
        print("    per jaar (bp, N): " + " ".join(f"{y}:{statistics.mean(v)*1e4:+.1f}({len(v)})" for y, v in sorted(yr.items())))


if __name__ == "__main__":
    main()
