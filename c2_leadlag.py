"""C2: lead-lag en vaste tijdvensters op FTMO-M5, exact volgens PREREG_C2.md. Gebruik: python3 c2_leadlag.py"""
import statistics
from collections import defaultdict
from datetime import timedelta
from zoneinfo import ZoneInfo

import stats_tools as st
from b4_sim import NY, SYMS, TRAIN_END, cost_frac, load, sessions, tstat

CET = ZoneInfo("Europe/Berlin")


def trade(side, eb, xb, comm):
    entry, exit_p = eb[1], xb[4]
    return side * (exit_p - entry) / entry - cost_frac(side, eb, xb, entry, comm)


def window_trades(sym, start_hm, end_hm):
    """elke dag long van open bar start_hm tot slot bar vóór end_hm (CET)"""
    comm = SYMS[sym][3]
    by_day = defaultdict(dict)
    for b in load(sym):
        t = (b[0] - timedelta(hours=7)).replace(tzinfo=NY).astimezone(CET)
        by_day[t.date()][(t.hour, t.minute)] = (t,) + b[1:]
    last = (end_hm[0], end_hm[1] - 5) if end_hm[1] >= 5 else (end_hm[0] - 1, end_hm[1] + 55)
    out = []
    for d, bars in sorted(by_day.items()):
        if start_hm in bars and last in bars:
            out.append((d, trade(1, bars[start_hm], bars[last], comm)))
    return out


def evaluate(name, trades):
    trades.sort()
    nets = [n for _, n in trades]
    tr = [n for d, n in trades if str(d) <= TRAIN_END]
    te = [n for d, n in trades if str(d) > TRAIN_END]
    yearly = defaultdict(list)
    for d, n in trades:
        yearly[d.year].append(n)
    pos = sum(statistics.mean(v) > 0 for v in yearly.values())
    ok = tstat(tr) >= 3 and tstat(te) >= 3 and len(nets) >= 1000 and pos >= 4
    print(f"{name:<22} N {len(nets):>5} | exp {statistics.mean(nets)*1e4:+6.2f} bp | t train {tstat(tr):+.2f} (N {len(tr)}) | "
          f"t test {tstat(te):+.2f} (N {len(te)}) | jaren+ {pos}/{len(yearly)} | DSR338 {st.deflated_sharpe(nets, 338)[0]:.2f} | "
          f"{'GESLAAGD' if ok else 'afgewezen'}")
    print("    per jaar (bp, N): " + " ".join(f"{y}:{statistics.mean(v)*1e4:+.1f}({len(v)})" for y, v in sorted(yearly.items())))


def main():
    sess = {s: dict(sessions(s)) for s in ("US500cash", "GER40cash", "UK100cash")}
    us_days = sorted(sess["US500cash"])
    us_ret = {d: s[-1][4] / s[0][1] - 1 for d, s in sess["US500cash"].items()}
    # (a) laatste volledige NY-sessie vóór de Europese datum -> GER40/UK100 eerste 60 min
    a = []
    for sym in ("GER40cash", "UK100cash"):
        for d, s in sess[sym].items():
            prev = [x for x in us_days if x < d]
            if not prev or len(s) < 12:
                continue
            side = 1 if us_ret[prev[-1]] > 0 else -1
            a.append((d, trade(side, s[0], s[11], SYMS[sym][3])))
    evaluate("(a) US→GER40/UK100", a)
    # (b) GER40 eerste 30 min -> US500 eerste 60 min, zelfde datum
    b = []
    for d, s in sess["US500cash"].items():
        g = sess["GER40cash"].get(d)
        if not g or len(g) < 6 or len(s) < 12:
            continue
        side = 1 if g[5][4] / g[0][1] - 1 > 0 else -1
        b.append((d, trade(side, s[0], s[11], SYMS["US500cash"][3])))
    evaluate("(b) GER40→US500", b)
    evaluate("(c1) XAU 13:30-14:30", window_trades("XAUUSD", (13, 30), (14, 30)))
    evaluate("(c2) US100 15:30-16:00", window_trades("US100cash", (15, 30), (16, 0)))


if __name__ == "__main__":
    main()
