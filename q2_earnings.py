"""Q2: earnings-gap continuatie en fade op FTMO-aandelen-CFD's (M5), exact volgens PREREG_Q2.md."""
import math
import statistics
from collections import defaultdict
from datetime import date, datetime, timedelta

import stats_tools as st
from b4_sim import TRAIN_END, load

COMM = 0.00002


def ny_sessions(sym):
    """NY-datum -> lijst M5-bars van de CFD-sessie (tuple: (hh,mm), o, h, l, c, spread_prijs).
    BUGFIX (gemeld): FTMO-aandelen-CFD's openen niet altijd om 09:30 (AAPL vanaf 2024 om 09:35) en sommige symbolen hebben
    een uur-offset in de tijdstempels (JPM '08:35'). Daarom: sessie = alle bars van die (NY-)datum, eerste bar = open,
    laatste bar = slot; minimaal 60 bars."""
    out = defaultdict(list)
    for b in load(sym):
        t = b[0] - timedelta(hours=7)
        out[t.date()].append(((t.hour, t.minute),) + b[1:])
    return {d: sorted(v) for d, v in out.items() if len(v) >= 60}


def events():
    ev = []
    for line in open("earnings.csv"):
        if line.startswith("#") or line.startswith("symbol"):
            continue
        s, ts = line.strip().split(";")
        t = datetime.strptime(ts, "%Y-%m-%d %H:%M")
        if t.hour == 0 and t.minute == 0:
            continue
        if (t.hour, t.minute) >= (16, 0):
            ev.append((s, t.date(), "amc"))
        elif (t.hour, t.minute) < (9, 30):
            ev.append((s, t.date(), "bmo"))
    return ev


def trade(sess, days, d, mode):
    """rendement netto, bruto, kosten of None"""
    if d not in sess:
        return None
    k = days.index(d)
    if k == 0:
        return None
    prev = sess[days[k - 1]]
    bars = sess[d]
    gap = bars[0][1] / prev[-1][4] - 1
    if abs(gap) <= 0.02:
        return None
    or_hi = max(b[2] for b in bars[:3]); or_lo = min(b[3] for b in bars[:3])
    eb = bars[3]  # 09:45-bar
    g = 1 if gap > 0 else -1
    side = g if mode == "cont" else -g
    entry = eb[1]
    stop = (or_lo if side > 0 else or_hi)
    exit_p, xb = None, bars[-1]
    for b in bars[3:]:
        if side > 0 and b[3] <= stop:
            exit_p = min(stop, b[1]); xb = b; break
        if side < 0 and b[2] >= stop:
            exit_p = max(stop, b[1]); xb = b; break
    if exit_p is None:
        exit_p = bars[-1][4]
    if (side > 0 and entry <= stop) or (side < 0 and entry >= stop):
        exit_p, xb = entry, eb  # instap al voorbij stop → direct gestopt (conservatief: alleen kosten)
    gross = side * (exit_p - entry) / entry
    cost = (eb[5] if side > 0 else xb[5]) / entry + 2 * COMM
    return gross - cost, gross, cost, gap


def main():
    ev = events()
    by_sym = defaultdict(list)
    for s, d, k in ev:
        by_sym[s].append((d, k))
    res = {"cont": [], "fade": []}
    gaps_event, gaps_all = [], []
    for s, lst in by_sym.items():
        sess = ny_sessions(s)
        days = sorted(sess)
        for i in range(1, len(days)):
            gaps_all.append(abs(sess[days[i]][0][1] / sess[days[i - 1]][-1][4] - 1))
        for d0, kind in lst:
            if kind == "amc":
                nxt = [x for x in days if x > d0]
                d = nxt[0] if nxt else None
            else:
                d = d0 if d0 in sess else None
            if d is None or d not in sess or days.index(d) == 0:
                continue
            gaps_event.append(abs(sess[d][0][1] / sess[days[days.index(d) - 1]][-1][4] - 1))
            for m in res:
                t = trade(sess, days, d, m)
                if t:
                    res[m].append((d, s) + t)
    print(f"Kwaliteitscheck: events met koersdata {len(gaps_event)}, mediaan |gap| op eventdagen {statistics.median(gaps_event)*100:.2f}% "
          f"vs alle dagen {statistics.median(gaps_all)*100:.2f}%; aandeel eventdagen met |gap| > 2%: {sum(g > 0.02 for g in gaps_event)/len(gaps_event)*100:.0f}%")
    for m, label in (("cont", "(a) continuatie"), ("fade", "(b) fade")):
        x = sorted(res[m])
        nets = [t[2] for t in x]
        tr = [t[2] for t in x if str(t[0]) <= TRAIN_END]; te = [t[2] for t in x if str(t[0]) > TRAIN_END]
        tt = lambda v: statistics.mean(v) / statistics.stdev(v) * math.sqrt(len(v)) if len(v) > 2 else float("nan")
        yr = defaultdict(list)
        for t in x:
            yr[t[0].year].append(t[2])
        pos = sum(statistics.mean(v) > 0 for v in yr.values())
        gross = statistics.mean(t[3] for t in x); cost = statistics.mean(t[4] for t in x)
        dsr = st.deflated_sharpe(nets, 396)[0]
        ok = tt(tr) >= 3 and tt(te) >= 3 and len(nets) >= 500 and pos >= 4 and dsr > 0.5 and gross >= 3 * cost
        print(f"{label}: N {len(nets)} | netto {statistics.mean(nets)*1e4:+.1f} bp | bruto {gross*1e4:+.1f} bp vs kosten {cost*1e4:.1f} bp | "
              f"t train {tt(tr):+.2f} (N {len(tr)}) | t test {tt(te):+.2f} (N {len(te)}) | jaren+ {pos}/{len(yr)} | DSR {dsr:.2f} → "
              f"{'GESLAAGD' if ok else 'afgewezen'}")
        print("    per jaar (bp, N): " + " ".join(f"{y}:{statistics.mean(v)*1e4:+.0f}({len(v)})" for y, v in sorted(yr.items())))


if __name__ == "__main__":
    main()
