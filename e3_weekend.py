"""E3: C4-combinatie (FTMO-RSI(2) + ORB) onder weekendregel Standard vs Swing, exact volgens PREREG_E3.md."""
import csv
import statistics
from collections import defaultdict
from datetime import date, datetime

import c4_combine as c4
import e1_rsi2_ftmo as e1
from b2_sim import rsi2

TRAIN_END = date(2023, 12, 31)


def sleeve(sym, standard):
    rows = e1.ftmo_close(sym)
    d = [x[0] for x in rows]; c = [x[1] for x in rows]
    rs = rsi2(c)
    sma = [statistics.mean(c[i - 199:i + 1]) if i >= 199 else None for i in range(len(c))]
    spread = e1.eod_spread_frac(sym)
    swap = e1.SWAP_LONG[sym]
    ret = {}
    state = False      # oorspronkelijke regel: 'in positie'
    held = False       # werkelijk aangehouden positie
    for i in range(1, len(c)):
        r = 0.0
        if held:
            r += c[i] / c[i - 1] - 1 - swap * (d[i] - d[i - 1]).days / 365
        # oorspronkelijke toestandsmachine op slot i
        if state and rs[i] is not None and rs[i] > 70:
            state = False
        elif not state and rs[i] is not None and sma[i] and rs[i] < 10 and c[i] > sma[i]:
            state = True
        last_of_week = i + 1 < len(d) and d[i + 1].isocalendar()[1] != d[i].isocalendar()[1]
        want = state and not (standard and last_of_week)
        if want != held:
            r -= spread
            held = want
        if e1.LO <= d[i] <= e1.HI:
            ret[d[i]] = r
    return ret


def orb_daily():
    orb = defaultdict(float)
    for r in csv.DictReader(open("results/b4/B4_a_ORB_trades.csv"), delimiter=";"):
        orb[datetime.strptime(r["date"], "%Y-%m-%d").date()] += float(r["net_frac"]) / 7
    return orb


def main():
    orb = orb_daily()
    for variant in ("Swing", "Standard"):
        sl = [sleeve(s, variant == "Standard") for s in e1.SWAP_LONG]
        rsi = dict(e1.pooled(sl))
        days = sorted(d for d in set(rsi) | set(orb) if date(2021, 9, 14) <= d <= max(orb))
        tr = [d for d in days if d <= TRAIN_END]
        va = statistics.stdev([rsi.get(d, 0) for d in tr]); vb = statistics.stdev([orb.get(d, 0) for d in tr])
        wa = (1 / va) / (1 / va + 1 / vb)
        comb = [(d, wa * rsi.get(d, 0) + (1 - wa) * orb.get(d, 0)) for d in days]
        k = c4.max_scale([r for d, r in comb if d <= TRAIN_END])
        print(f"\n== {variant}: gewichten RSI {wa:.2f} / ORB {1-wa:.2f}, schaal {k:.2f} (vastgezet op 2021-09..2023)")
        c4.describe("   volledig 2021-09..2026", comb, k)
        c4.describe("   TRAIN 2021-09..2023", [x for x in comb if x[0] <= TRAIN_END], k)
        c4.describe("   TEST 2024..2026", [x for x in comb if x[0] > TRAIN_END], k)
        eq = 1e5
        with open(f"results/e3/E3_{variant}_daily.csv", "w") as f:
            f.write("date;start_balance;start_equity;min_equity;end_equity\n")
            for d, r in comb:
                prev = eq; eq *= 1 + k * r
                f.write(f"{d.strftime('%Y.%m.%d')};{prev:.2f};{prev:.2f};{min(prev, eq):.2f};{eq:.2f}\n")


if __name__ == "__main__":
    main()
