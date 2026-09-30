import numpy as np
from catalogus._common import month_end, weights_to_positions, common_calendar
RULE = {"id": "C52_allweather", "naam": "All-weather / risicopariteit: aandelen, obligaties, goud, grondstoffen (∝ 1/σ60, vol-target 8%, geen hefboom)",
        "familie": "allocatie/risicopariteit", "instrumenten": ["SPY", "IEF", "GLD", "DBC", "BOND10_SYN", "GOLD_F"], "aggregatie": "som", "vehicle": "etf", "laag_omloop": True,
        "start_jaar": 2003, "benchmark": {"naam": "60/40 SPY/IEF", "gewichten": {"SPY": 0.6, "IEF": 0.4}},
        "mechanisme": "Diversificatie over groei-/inflatieregimes; gelijke risicobijdrage i.p.v. gelijke kapitaalbijdrage.",
        "bron": "Dalio (All Weather); Asness–Frazzini–Pedersen (2012) risk parity", "varianten": {"basis": {}, "lang": {"assets": ["SPY", "BOND10_SYN", "GOLD_F"], "start_jaar": 2001, "benchmark": {"naam": "60/40 SPY/BOND10_SYN", "gewichten": {"SPY": 0.6, "BOND10_SYN": 0.4}}}}}
def positions_all(data, p):
    names = p.get("assets", ["SPY", "IEF", "GLD", "DBC"])
    allnames = list(data)
    names = [n for n in names if n in data]
    ret = {}
    for n in names:
        c = data[n]["close"]; ret[n] = dict(zip(data[n]["date"][1:], c[1:] / c[:-1] - 1))
    cal = sorted(set().union(*[set(data[n]["date"]) for n in names])); me = month_end(np.array(cal)); w = {}
    for k, d in enumerate(cal):
        if not me[k] or k < 61:
            continue
        win = cal[k - 60:k + 1]
        avail = [n for n in names if all(x in ret[n] for x in win[1:])]
        if len(avail) < 2:
            continue
        R = np.array([[ret[n][x] for x in win[1:]] for n in avail]); sd = R.std(axis=1, ddof=1) * np.sqrt(252)
        iv = 1 / sd; wt = iv / iv.sum(); sp = float(np.sqrt(wt @ (np.cov(R) * 252) @ wt))
        sc = min(1.0, 0.08 / sp)
        w[d] = {n: float(a * sc) for n, a in zip(avail, wt)}
    pos = weights_to_positions({n: data[n] for n in names}, w)
    for n in allnames:
        pos.setdefault(n, np.zeros(len(data[n]["date"])))
    return pos
