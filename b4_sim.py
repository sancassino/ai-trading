"""B4: intraday-strategieën op FTMO-M5-data, exact volgens PREREG_B4.md.
Gebruik: python3 b4_sim.py  -> samenvatting per strategie (gepoold), per symbool, per jaar; trades in results/b4/."""
import csv
import math
import os
import statistics
from collections import defaultdict
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import stats_tools as st

NY = ZoneInfo("America/New_York")
SYMS = {  # bestand: (sessie-tijdzone, open, sluit, commissie per kant als fractie van notional)
    "US500cash": ("America/New_York", (9, 30), (16, 0), 0.0),
    "US100cash": ("America/New_York", (9, 30), (16, 0), 0.0),
    "US30cash": ("America/New_York", (9, 30), (16, 0), 0.0),
    "XAUUSD": ("America/New_York", (9, 30), (16, 0), 0.000006),
    "GER40cash": ("Europe/Berlin", (9, 0), (17, 30), 0.0),
    "UK100cash": ("Europe/London", (8, 0), (16, 30), 0.0),
    "EURUSD": ("Europe/London", (8, 0), (16, 30), 0.0000225),
}
TRAIN_END = "2023-12-31"


def load(sym):
    point = None
    bars = []
    for line in open(f"data/m5/{sym}.csv"):
        if line.startswith("#"):
            point = float(line.split("point=")[1].split(";")[0])
            continue
        if not line[0].isdigit():
            continue
        t, o, h, l, c, sp = line.rstrip().split(";")
        server = datetime.strptime(t, "%Y.%m.%d %H:%M")
        bars.append((server, float(o), float(h), float(l), float(c), int(sp) * point))
    return bars


def sessions(sym):
    """lijst van sessies: (datum, [bars binnen sessie]) met lokale tijd; alleen volledige sessies."""
    tzname, (oh, om), (ch, cm), _ = SYMS[sym]
    tz = ZoneInfo(tzname)
    by_day = defaultdict(list)
    for b in load(sym):
        local = (b[0] - timedelta(hours=7)).replace(tzinfo=NY).astimezone(tz)
        by_day[local.date()].append((local,) + b[1:])
    out = []
    for d in sorted(by_day):
        op = datetime(d.year, d.month, d.day, oh, om, tzinfo=tz)
        cl = datetime(d.year, d.month, d.day, ch, cm, tzinfo=tz)
        s = [b for b in by_day[d] if op <= b[0] < cl]
        if s and s[0][0] == op and s[-1][0] == cl - timedelta(minutes=5):
            out.append((d, s))
    return out


def cost_frac(side, entry_bar, exit_bar, price, comm):
    spread = entry_bar[5] if side > 0 else exit_bar[5]
    return spread / price + 2 * comm


def run_orb(sess, comm):
    trades = []
    for d, s in sess:
        if len(s) < 8:
            continue
        hi = max(b[2] for b in s[:6]); lo = min(b[3] for b in s[:6])
        R = hi - lo
        if R <= 0:
            continue
        for k in range(6, len(s)):
            b = s[k]
            up, dn = b[2] > hi, b[3] < lo
            if not (up or dn):
                continue
            if up and dn:  # beide kanten in één bar: conservatief verlies
                side = 1; entry = max(hi, b[1]); exit_p = lo; ex_bar = b
            else:
                side = 1 if up else -1
                entry = max(hi, b[1]) if up else min(lo, b[1])
                stop = lo if up else hi
                if (up and b[3] <= stop) or (dn and b[2] >= stop):
                    exit_p = stop; ex_bar = b
                else:
                    exit_p = None
                    for b2 in s[k + 1:]:
                        if side > 0 and b2[3] <= stop:
                            exit_p = min(stop, b2[1]); ex_bar = b2; break
                        if side < 0 and b2[2] >= stop:
                            exit_p = max(stop, b2[1]); ex_bar = b2; break
                    if exit_p is None:
                        ex_bar = s[-1]; exit_p = s[-1][4]
            gross = side * (exit_p - entry) / entry
            net = gross - cost_frac(side, b, ex_bar, entry, comm)
            trades.append((d, net, net * entry / R))
            break
    return trades


def run_last30(sess, comm):
    trades = []
    prev_close = None
    for d, s in sess:
        if prev_close is not None and len(s) >= 18:
            r1 = s[5][4] / prev_close - 1
            r12 = s[-7][4] / s[-13][4] - 1  # slot van bar eindigend op sluiting−30 / sluiting−60
            sig = 1 if r1 + r12 > 0 else -1
            eb, xb = s[-6], s[-1]
            entry, exit_p = eb[1], xb[4]
            net = sig * (exit_p - entry) / entry - cost_frac(sig, eb, xb, entry, comm)
            trades.append((d, net, None))
        prev_close = s[-1][4]
    return trades


def run_gap(sess, comm):
    trades = []
    prev_close = None
    for d, s in sess:
        if prev_close is not None and len(s) >= 12:
            gap = s[0][1] / prev_close - 1
            if abs(gap) > 0.005:
                sig = -1 if gap > 0 else 1
                eb, xb = s[0], s[11]
                entry, exit_p = eb[1], xb[4]
                net = sig * (exit_p - entry) / entry - cost_frac(sig, eb, xb, entry, comm)
                trades.append((d, net, None))
        prev_close = s[-1][4]
    return trades


def tstat(x):
    return statistics.mean(x) / statistics.stdev(x) * math.sqrt(len(x)) if len(x) > 2 else float("nan")


def main():
    os.makedirs("results/b4", exist_ok=True)
    sess = {s: sessions(s) for s in SYMS}
    for s, v in sess.items():
        print(f"{s}: {len(v)} volledige sessies ({v[0][0]} .. {v[-1][0]})")
    for name, fn in (("a_ORB", run_orb), ("b_last30", run_last30), ("c_gaprev", run_gap)):
        allt = []
        per_sym = {}
        for s in SYMS:
            t = fn(sess[s], SYMS[s][3])
            per_sym[s] = t
            allt += [(d, n, r, s) for d, n, r in t]
        allt.sort()
        tr = [n for d, n, r, s in allt if str(d) <= TRAIN_END]
        te = [n for d, n, r, s in allt if str(d) > TRAIN_END]
        yearly = defaultdict(list)
        for d, n, r, s in allt:
            yearly[d.year].append(n)
        pos_years = sum(statistics.mean(v) > 0 for v in yearly.values())
        nets = [n for _, n, _, _ in allt]
        ok = tstat(tr) >= 3 and tstat(te) >= 3 and len(allt) >= 500 and pos_years >= 4
        dsr = st.deflated_sharpe(nets, 326)[0]
        rs = [r for _, _, r, _ in allt if r is not None]
        print(f"\n{name}: N {len(allt)} | exp {statistics.mean(nets)*1e4:+.2f} bp/trade"
              + (f" ({statistics.mean(rs):+.3f} R)" if rs else "")
              + f" | t train {tstat(tr):+.2f} (N {len(tr)}) | t test {tstat(te):+.2f} (N {len(te)}) | jaren+ {pos_years}/{len(yearly)}"
              f" | DSR326 {dsr:.2f} | {'GESLAAGD' if ok else 'afgewezen'}")
        print("   per jaar (bp/trade, N): " + " ".join(f"{y}:{statistics.mean(v)*1e4:+.1f}({len(v)})" for y, v in sorted(yearly.items())))
        print("   per symbool (bp/trade, t, N): " + " ".join(
            f"{s}:{statistics.mean([n for _, n, _ in t])*1e4:+.1f}/{tstat([n for _, n, _ in t]):+.1f}/{len(t)}" for s, t in per_sym.items() if len(t) > 2))
        with open(f"results/b4/B4_{name}_trades.csv", "w") as f:
            f.write("date;symbol;net_frac;net_R\n")
            for d, n, r, s in allt:
                f.write(f"{d};{s};{n:.6f};{'' if r is None else f'{r:.4f}'}\n")


if __name__ == "__main__":
    main()
