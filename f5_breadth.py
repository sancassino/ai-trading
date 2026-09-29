"""F5: breedte met identieke regels (RSI(2), ORB, IBS) op extra FTMO-instrumenten, volgens PREREG_F5.md.
Afwijking (gemeld): huidige FTMO-longswap EU50 (+10%/jr) en FRA40 (+31%/jr) is een dividendseizoen-anomalie → voor
beide de GER40-longswap (−6,52%/jr) gebruikt."""
import csv
import math
import statistics
from collections import defaultdict
from datetime import date, datetime

import b4_sim
import e1_rsi2_ftmo as e1
import stats_tools as st
from b2_sim import rsi2

NEW = ["JP225cash", "AUS200cash", "HK50cash", "EU50cash", "FRA40cash", "SPN35cash", "N25cash", "XAGUSD"]
SWAP_NEW = {"JP225cash": 0.0491, "AUS200cash": 0.0802, "HK50cash": 0.0724, "EU50cash": 0.0652, "FRA40cash": 0.0652,
            "SPN35cash": 0.0661, "N25cash": 0.0348, "XAGUSD": 0.1142}
SESS_NEW = {"JP225cash": ("Asia/Tokyo", (9, 0), (15, 0), 0.0), "AUS200cash": ("Australia/Sydney", (10, 0), (16, 0), 0.0),
            "HK50cash": ("Asia/Hong_Kong", (9, 30), (16, 0), 0.0), "EU50cash": ("Europe/Berlin", (9, 0), (17, 30), 0.0),
            "FRA40cash": ("Europe/Berlin", (9, 0), (17, 30), 0.0), "SPN35cash": ("Europe/Berlin", (9, 0), (17, 30), 0.0),
            "N25cash": ("Europe/Berlin", (9, 0), (17, 30), 0.0), "XAGUSD": ("America/New_York", (9, 30), (16, 0), 0.000006)}
MID = date(2023, 12, 31)


def halves(d):
    a = math.prod(1 + v for k, v in d.items() if k <= MID) - 1
    b = math.prod(1 + v for k, v in d.items() if k > MID) - 1
    return a, b


def corr(a, b):
    ks = sorted(set(a) | set(b))
    return statistics.correlation([a.get(k, 0.0) for k in ks], [b.get(k, 0.0) for k in ks])


def decide(name, rets, ref):
    x = list(rets.values())
    t = st.t_stat(x)
    h1, h2 = halves(rets)
    c = corr(rets, ref)
    ok = t >= 2 and c < 0.5 and h1 > 0 and h2 > 0
    print(f"  {name:<22} t {t:+.2f} | corr {c:+.2f} | 2021–23 {h1*100:+.1f}% | 2024–26 {h2*100:+.1f}% → {'OPNEMEN' if ok else 'niet'}")
    return ok


def ibs_sleeve(sym):
    rows = []
    for line in open("data/ftmo_d1ohlc_US500_US100.txt"):
        p = line.strip().split(";")
        if len(p) == 6 and p[0] == sym.replace("cash", ".cash"):
            rows.append((datetime.strptime(p[1], "%Y.%m.%d").date(), *map(float, p[2:])))
    d = [r[0] for r in rows]; h = [r[2] for r in rows]; l = [r[3] for r in rows]; c = [r[4] for r in rows]
    spread = e1.eod_spread_frac(sym)
    swap = e1.SWAP_LONG[sym]
    ret, inpos, held = {}, False, 0
    for i in range(1, len(c)):
        r = 0.0
        if inpos:
            r += c[i] / c[i - 1] - 1 - swap * (d[i] - d[i - 1]).days / 365
            held += 1
        if inpos and (c[i] > h[i - 1] or held >= 5):
            inpos = False; r -= spread
        elif not inpos and h[i] > l[i] and (c[i] - l[i]) / (h[i] - l[i]) < 0.2:
            inpos = True; held = 0; r -= spread
        if e1.LO <= d[i] <= e1.HI:
            ret[d[i]] = r
    return ret


def orb_daily(sym):
    tr = b4_sim.run_orb(b4_sim.sessions(sym), b4_sim.SYMS[sym][3])
    out = defaultdict(float)
    for d, n, _ in tr:
        out[d] += n
    return dict(out), len(tr)


def main():
    e1.SWAP_LONG.update(SWAP_NEW)
    b4_sim.SYMS.update(SESS_NEW)
    old_rsi = [e1.ftmo_sleeve(s)[0] for s in ["US500cash", "US100cash", "US30cash", "GER40cash", "UK100cash", "XAUUSD"]]
    rsi_ref = dict(e1.pooled(old_rsi))
    orb_old = ["US500cash", "US100cash", "US30cash", "XAUUSD", "GER40cash", "UK100cash", "EURUSD"]
    orb_ref = defaultdict(float)
    for s in orb_old:
        for d, v in orb_daily(s)[0].items():
            orb_ref[d] += v / 7
    print("RSI(2)-sleeves (FTMO-D1), vs RSI(2) gepoold-6:")
    rsi_in = [s for s in NEW if decide(f"RSI {s}", e1.ftmo_sleeve(s)[0], rsi_ref)]
    print("ORB-sleeves (FTMO-M5), vs ORB gepoold-7:")
    orb_in = []
    for s in NEW:
        daily, n = orb_daily(s)
        print(f"    ({s}: {n} trades)")
        if decide(f"ORB {s}", daily, orb_ref):
            orb_in.append(s)
    print("IBS-sleeves (FTMO-D1-OHLC), vs RSI(2) gepoold-6:")
    ibs_in = [s for s in ("US500cash", "US100cash") if decide(f"IBS {s}", ibs_sleeve(s), rsi_ref)]
    print(f"\nOpgenomen: RSI {rsi_in} | ORB {orb_in} | IBS {ibs_in}")


if __name__ == "__main__":
    main()
