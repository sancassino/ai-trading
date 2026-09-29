"""FTMO Monte Carlo op DAGBASIS, op de echte dagelijkse equity-log van een MT5-run.

Bootstrap-eenheid = een echte kalendermaand (rebalans tot rebalans) met al zijn
handelsdagen. Per dag wordt de dagstart-BALANCE, dagstart-equity en de laagste
equity van de dag meegenomen, relatief t.o.v. de equity aan het begin van die
maand. Zo tellen beide FTMO-verliesregels op dagniveau mee, inclusief zwevend
verlies dat over dagen heen wordt meegedragen:

  - dagverlies: equity < balance(00:00) - 5% van het startkapitaal  -> gebroken
  - max loss:   equity < 90% van het startkapitaal (statisch)      -> gebroken

Fase 1 +10%, fase 2 +5% (elk een vers 100k-account, doel op balance gemeten),
daarna 12 maanden live: geslaagd als niet gebroken en gemiddeld >= $1.000/mnd
bruto, resp. netto na 80% winstdeling.

Benaderingen (expliciet): bij een maandgrens wordt zwevend resultaat van een
doorlopend been "verzilverd" (balance = equity), en --scale k schaalt alle
afwijkingen lineair (~k x de exposure van de run). Exacte cijfers altijd in
MT5 bevestigen.

Gebruik: python3 mc_daily_ftmo.py results/plateau/PL_t2_l3_r10_daily.csv [--scale 1.3]
"""
import argparse
import csv
import random
from collections import OrderedDict

ACC = 100000.0


def load_months(path):
    """List of months; each month = list of (bal, eq_start, eq_min) per day,
    all relative to equity at the first tick of that month."""
    by_month = OrderedDict()
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f, delimiter=";"):
            if not r.get("date"):
                continue
            by_month.setdefault(r["date"][:7], []).append(
                (float(r["start_balance"]), float(r["start_equity"]), float(r["min_equity"]), float(r["end_equity"])))
    months = []
    keys = list(by_month)
    for idx, k in enumerate(keys):
        days = by_month[k]
        base = days[0][1]
        rel = [(b / base, e / base, m / base) for b, e, m, _ in days]
        nxt = by_month[keys[idx + 1]][0][1] if idx + 1 < len(keys) else days[-1][3]
        months.append((rel, nxt / base))
    return months


def run_account(stream, target, max_months, scale):
    """Returns ('pass'|'fail'|'timeout'|'done', months_used, final_equity)."""
    eq = ACC
    for mo in range(1, max_months + 1):
        days, end_rel = next(stream)
        for b, e, m in days:
            bal = eq * (1 + scale * (b - 1))
            low = eq * (1 + scale * (m - 1))
            if low < bal - 0.05 * ACC or low < 0.90 * ACC:
                return "fail", mo, low
        eq *= 1 + scale * (end_rel - 1)
        if eq < 0.90 * ACC:
            return "fail", mo, eq
        if target is not None and eq >= ACC * (1 + target):
            return "pass", mo, eq
    return ("timeout" if target is not None else "done"), max_months, eq


def simulate(months, scale, block, n_sims, seed, phase_months):
    rng = random.Random(seed)
    n = len(months)

    def stream():
        while True:
            s = rng.randrange(n)
            for i in range(block):
                yield months[(s + i) % n]

    c = {"p1": 0, "funded": 0, "live_gross": 0, "live_net": 0, "live_breach": 0}
    to_fund = []
    for _ in range(n_sims):
        st = stream()
        r1, m1, _ = run_account(st, 0.10, phase_months, scale)
        if r1 != "pass":
            continue
        c["p1"] += 1
        r2, m2, _ = run_account(st, 0.05, phase_months, scale)
        if r2 != "pass":
            continue
        c["funded"] += 1
        to_fund.append(m1 + m2)
        r3, _, eq = run_account(st, None, 12, scale)
        if r3 == "fail":
            c["live_breach"] += 1
            continue
        c["live_gross"] += (eq - ACC) >= 12000
        c["live_net"] += (eq - ACC) * 0.8 >= 12000
    out = {k: v / n_sims for k, v in c.items()}
    to_fund.sort()
    out["median_months_to_fund"] = to_fund[len(to_fund) // 2] if to_fund else float("nan")
    out["live_breach_given_funded"] = c["live_breach"] / c["funded"] if c["funded"] else float("nan")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("daily_csv")
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--sims", type=int, default=20000)
    ap.add_argument("--phase-months", type=int, default=12, help="max duur per fase (FTMO heeft geen limiet; dit is praktisch)")
    ap.add_argument("--blocks", default="1,3,6,12")
    a = ap.parse_args()
    months = load_months(a.daily_csv)
    print(f"{a.daily_csv}: {len(months)} maanden, scale={a.scale}")
    print(f"{'blok':>5}{'fase1':>8}{'funded':>8}{'mnd->fund':>10}{'live>=1k':>9}{'netto>=1k':>10}{'live-breuk|f':>13}")
    for b in (int(x) for x in a.blocks.split(",")):
        o = simulate(months, a.scale, b, a.sims, 42, a.phase_months)
        print(f"{b:>5}{o['p1']*100:>7.1f}%{o['funded']*100:>7.1f}%{o['median_months_to_fund']:>10.1f}"
              f"{o['live_gross']*100:>8.1f}%{o['live_net']*100:>9.1f}%{o['live_breach_given_funded']*100:>12.1f}%")
