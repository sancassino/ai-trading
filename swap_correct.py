"""Corrigeer de swap-kosten van een MT5-backtest voor het "vaste punten"-artefact.

FTMO rekent swap in punten per lot per dag (swap_mode=1). De Strategy Tester past
de HUIDIGE puntwaarde toe op de hele historie. Bij een instrument dat sindsdien
fors gestegen is (NVDA: $13 in 2021, $225 nu, split-gecorrigeerd) koop je
vroeger veel meer stuks voor hetzelfde bedrag, dus wordt de swap per euro
exposure absurd hoog (NVDA 2021: ~145%/jaar i.p.v. ~8%).

Correctie: swap_gecorrigeerd = swap x (koers op sluitdatum / koers nu), d.w.z.
dezelfde %-financiering als vandaag over de hele periode. Dat is nog steeds
conservatief voor 2021-2022 (rente toen ~0%). Koersen uit <SYMBOOL>_rates.csv.

Schrijft <run>_swapcorr.csv (deals) en <run>_swapcorr_daily.csv (dag-equity,
correctie cumulatief geboekt op sluitdatum) zodat analyze_daily/mc/walk_forward
er direct op draaien.
Gebruik: python3 swap_correct.py results/eur/EUR_t2_l3_r0_g0_e30.csv [...]
"""
import bisect
import csv
import sys
from collections import defaultdict

_cache = {}


def rates(sym):
    if sym not in _cache:
        fn = sym.replace(".cash", "cash") + "_rates.csv"
        try:
            rows = [(r["date"], float(r["close"])) for r in csv.DictReader(open(fn, encoding="utf-8-sig"), delimiter=";")]
        except FileNotFoundError:
            rows = []
        _cache[sym] = rows
    return _cache[sym]


def factor(sym, date):
    rs = rates(sym)
    if not rs:
        return None
    dates = [d for d, _ in rs]
    i = min(bisect.bisect_right(dates, date) - 1, len(rs) - 1)
    return rs[max(i, 0)][1] / rs[-1][1]


def correct(path):
    deals = list(csv.DictReader(open(path, encoding="utf-8-sig"), delimiter=";"))
    fields = list(deals[0].keys())
    adj_by_day = defaultdict(float)
    missing = set()
    tot_old = tot_new = 0.0
    for r in deals:
        if not r.get("close_time"):
            continue
        sw = float(r["swap"])
        f = factor(r["symbol"], r["close_time"][:10])
        if f is None:
            missing.add(r["symbol"])
            f = 1.0
        f = min(f, 1.0)  # nooit duurder maken dan de tester al rekende
        new_sw = sw * f
        adj = new_sw - sw
        tot_old += sw
        tot_new += new_sw
        r["swap"] = f"{new_sw:.2f}"
        r["profit"] = f"{float(r['profit']) + adj:.2f}"
        adj_by_day[r["close_time"][:10]] += adj
    out = path.replace(".csv", "_swapcorr.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter=";")
        w.writeheader()
        w.writerows(r for r in deals if r.get("close_time"))
    daily = list(csv.DictReader(open(path.replace(".csv", "_daily.csv"), encoding="utf-8-sig"), delimiter=";"))
    cum = 0.0
    for r in daily:
        # correctie geldt vanaf de sluitdag (balance en equity schuiven gelijk op)
        for k in ("start_balance", "start_equity", "min_equity"):
            r[k] = f"{float(r[k]) + cum:.2f}"
        cum += adj_by_day.get(r["date"], 0.0)
        r["end_equity"] = f"{float(r['end_equity']) + cum:.2f}"
    with open(out.replace(".csv", "_daily.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(daily[0].keys()), delimiter=";")
        w.writeheader()
        w.writerows(daily)
    return tot_old, tot_new, missing


if __name__ == "__main__":
    for p in sys.argv[1:]:
        o, n, miss = correct(p)
        print(f"{p.split('/')[-1]:<34} swap tester {o:>10,.0f}  gecorrigeerd {n:>10,.0f}  verschil {n-o:>+10,.0f}"
              + (f"  (geen koersdata: {','.join(sorted(miss))})" if miss else ""))
