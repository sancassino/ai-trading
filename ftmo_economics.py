"""FTMO-economie (B5): slaagkans en verwachte uitbetaling voor een dagreeks, bij gegeven positiegrootte.

Regels 2-Step (ftmo.com, 29-09-2026): fase 1 +10%, fase 2 +5%, max dagverlies 5% van het startkapitaal
(t.o.v. dagstart), max verlies 10% (statisch), min. 4 handelsdagen, geen tijdslimiet (hier praktisch
begrensd op --max-months per fase), fee terug bij eerste uitbetaling. Funded: winst boven het
startkapitaal wordt maandelijks uitbetaald tegen --split (80%) en het saldo gaat terug naar start.

Bootstrap: aaneengesloten blokken echte dagrendementen (--block dagen), vermenigvuldigd met --scale.
Benadering: dagverlies gemeten op slot-tot-slot (geen intraday-dip) en balance = equity bij dagstart.

Gebruik: python3 ftmo_economics.py dagreeks.csv [--scale 1,2,3] [--fee 540] [--account 80000]
"""
import argparse
import csv
import random
import statistics


def daily_returns(path):
    eq = [float(r["end_equity"]) for r in csv.DictReader(open(path, encoding="utf-8-sig"), delimiter=";") if r.get("date")]
    return [eq[i] / eq[i - 1] - 1 for i in range(1, len(eq))]


def phase(stream, target, max_days):
    eq, days = 1.0, 0
    while days < max_days:
        r = next(stream)
        days += 1
        loss = -r * eq
        eq *= 1 + r
        if loss >= 0.05 or eq <= 0.90:
            return False, days
        if target is not None and eq >= 1 + target and days >= 4:
            return True, days
    return False, days


def funded(stream, months, split):
    payouts = []
    eq = 1.0
    for _ in range(months):
        for _ in range(21):
            r = next(stream)
            loss = -r * eq
            eq *= 1 + r
            if loss >= 0.05 or eq <= 0.90:
                return payouts, True
        if eq > 1.0:
            payouts.append((eq - 1.0) * split)
            eq = 1.0
    return payouts, False


def simulate(rets, scale, fee, account, sims=20000, block=21, max_months=24, live_months=12, split=0.8, seed=7):
    rng = random.Random(seed)
    x = [r * scale for r in rets]
    n = len(x)

    def stream():
        while True:
            s = rng.randrange(n)
            for i in range(block):
                yield x[(s + i) % n]

    p1 = fu = breach = 0
    pay_tot = []
    pay_only = []  # uitbetalingen zonder fee-restitutie, alleen funded accounts
    months_to_fund = []
    for _ in range(sims):
        st = stream()
        ok1, d1 = phase(st, 0.10, max_months * 21)
        if not ok1:
            pay_tot.append(0.0)
            continue
        p1 += 1
        ok2, d2 = phase(st, 0.05, max_months * 21)
        if not ok2:
            pay_tot.append(0.0)
            continue
        fu += 1
        months_to_fund.append((d1 + d2) / 21)
        pays, br = funded(st, live_months, split)
        breach += br
        pay_only.append(sum(pays) * account)
        total = sum(pays) * account + (fee if pays else 0.0)  # fee-restitutie bij eerste uitbetaling
        pay_tot.append(total)
    ev = statistics.mean(pay_tot) - fee
    return {
        "p1": p1 / sims, "funded": fu / sims, "breach_live": breach / fu if fu else float("nan"),
        "months_to_fund": statistics.median(months_to_fund) if months_to_fund else float("nan"),
        "payout_per_month_given_funded": (statistics.mean(pay_only) / live_months if pay_only else 0.0),
        "ev_per_attempt": ev, "break_even_fee": statistics.mean(pay_tot),
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--scale", default="1")
    ap.add_argument("--fee", type=float, default=540.0, help="challenge-fee in EUR (standaard 540, niet geverifieerd)")
    ap.add_argument("--account", type=float, default=80000)
    ap.add_argument("--sims", type=int, default=20000)
    ap.add_argument("--split", type=float, default=0.8)
    ap.add_argument("--demean", action="store_true", help="controle: dagrendementen zonder drift (edge = 0)")
    a = ap.parse_args()
    for f in a.files:
        rets = daily_returns(f)
        if a.demean:
            m = statistics.mean(rets)
            rets = [r - m for r in rets]
            print("  [controle: gedemeand, edge = 0]")
        vol = statistics.stdev(rets) * 252 ** 0.5
        print(f"{f.split('/')[-1]}: {len(rets)} dagen, vol {vol*100:.1f}%/jr (scale 1)")
        print(f"  {'scale':>5}{'fase1':>8}{'funded':>8}{'mnd→fund':>9}{'breuk live':>11}{'€/mnd|funded':>13}{'EV/poging':>11}{'break-even fee':>15}")
        for k in (float(v) for v in a.scale.split(",")):
            o = simulate(rets, k, a.fee, a.account, a.sims, split=a.split)
            print(f"  {k:>5.1f}{o['p1']*100:>7.1f}%{o['funded']*100:>7.1f}%{o['months_to_fund']:>9.1f}{o['breach_live']*100:>10.1f}%"
                  f"{o['payout_per_month_given_funded']:>13,.0f}{o['ev_per_attempt']:>11,.0f}{o['break_even_fee']:>15,.0f}")
