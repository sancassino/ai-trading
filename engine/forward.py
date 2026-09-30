"""Forward-dagreeks per catalogusregel (D-050): zelfde kern als engine.run_rule.run (positions → net_returns_vehicle → aggregatie → overschot/totaal),
maar zonder ontdekkings-/reservefilter en zonder TRIALS-rij. Validatie: over ≤ 2024 identiek aan results/R2/series/<id>__<variant>__<vehikel>.csv.
Gebruik: series(rule_id, variant, vehicle, start=date, end=None) -> {date: (excess, total)}"""
import importlib
from datetime import date

import numpy as np

from engine.run_rule import load_daily, net_returns_vehicle, rf_on, vehicles


def series(rule_id, variant, vehicle=None, start=date(1900, 1, 1), end=None):
    mod = importlib.import_module(f"catalogus.{rule_id}")
    R = mod.RULE
    veh = vehicle or R.get("vehicle", "cfd")
    params = R["varianten"][variant]
    data = {n: load_daily(n, R.get("field", "adjclose")) for n in R["instrumenten"]}
    mode = R.get("aggregatie", "gemiddelde"); cap = mode != "som"
    sj = params.get("start_jaar", R.get("start_jaar", 1900))
    mp = R.get("max_pos", 1.0)
    allpos = mod.positions_all(data, params) if hasattr(mod, "positions_all") else {n: mod.positions(df, params) for n, df in data.items()}
    port, absp = {}, {}
    for n, df in data.items():
        pos = np.clip(np.nan_to_num(np.asarray(allpos[n], float)), -mp, mp)
        net, *_ = net_returns_vehicle(df, pos, 1.0, veh, cap)
        ok = np.isfinite(net) & np.array([d.year >= sj and d >= start and (end is None or d <= end) for d in df["date"]])
        for d, v in zip(df["date"][ok], net[ok]):
            port.setdefault(d, []).append(v)
        pp = np.r_[0.0, (pos if vehicles()[veh]["short"] else np.maximum(pos, 0.0))[:-1]]
        for d, v in zip(df["date"][ok], np.abs(pp[ok])):
            absp[d] = absp.get(d, 0.0) + v
    days = sorted(port)
    agg = np.sum if mode == "som" else np.mean
    x = np.array([agg(port[d]) for d in days])
    nights = np.r_[0, [(b - a).days for a, b in zip(days[:-1], days[1:])]]
    rf_p = rf_on(days) / 100 / 365 * nights if veh != "cfd" else np.zeros(len(days))
    if mode == "som" and veh != "cfd":
        V = vehicles()[veh]
        cashfrac = np.array([np.clip(1 - absp.get(d, 0.0), 0, 1) for d in days]) if V["model"] == "etf" else np.ones(len(days))
        x = x + rf_p * cashfrac
    return {d: (float(a - r), float(a)) for d, a, r in zip(days, x, rf_p)}


def validate(rule_id, variant, vehicle):
    """vergelijk met de R2-export over de ontdekkingsperiode; geeft max. absolute afwijking."""
    ref = {}
    for line in open(f"results/R2/series/{rule_id}__{variant}__{vehicle}.csv"):
        if line[:1].isdigit():
            d, a, b = line.strip().split(";"); ref[date.fromisoformat(d)] = (float(a), float(b))
    s = series(rule_id, variant, vehicle, end=date(2024, 12, 31))
    common = [d for d in ref if d in s]
    diff = max(abs(s[d][1] - ref[d][1]) for d in common) if common else float("nan")
    return len(ref), len(common), diff


if __name__ == "__main__":
    import sys
    for spec in sys.argv[1:] or ["C02_faber:basis:etf", "C52_allweather:lang:etf", "C17_fomc_cycle:basis:etf"]:
        r, v, veh = spec.split(":")
        n, m, diff = validate(r, v, veh)
        print(f"{spec}: R2-reeks {n} dagen, gemeenschappelijk {m}, max |verschil totaal| {diff:.2e} → {'OK' if diff < 1e-7 and m == n else 'AFWIJKING'}")
