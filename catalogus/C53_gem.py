import numpy as np
from catalogus._common import month_end, ret_back, weights_to_positions, common_calendar, cash_12m
RULE = {"id": "C53_gem", "naam": "Dual momentum (Antonacci GEM): US / ex-US aandelen of obligaties", "familie": "momentum/allocatie",
        "instrumenten": ["SPY", "EFA", "IEF"], "aggregatie": "som", "vehicle": "etf", "laag_omloop": True, "start_jaar": 2003,
        "benchmark": {"naam": "60/40 SPY/IEF", "gewichten": {"SPY": 0.6, "IEF": 0.4}},
        "mechanisme": "Absolute momentum (aandelen vs geldmarkt) beperkt bear-markt-DD; relatieve momentum kiest de sterkste regio.",
        "bron": "Antonacci (2014) 'Dual Momentum Investing'", "varianten": {"basis": {}}}
def positions_all(data, p):
    cal = common_calendar(data, ["SPY", "EFA", "IEF"]); idx = {n: {d: i for i, d in enumerate(data[n]["date"])} for n in data}
    r12 = {n: ret_back(data[n]["close"], 252) for n in data}
    me = month_end(np.array(cal)); w = {}
    for k, d in enumerate(cal):
        if not me[k]:
            continue
        i = {n: idx[n][d] for n in data}
        us, ex = r12["SPY"][i["SPY"]], r12["EFA"][i["EFA"]]
        if not (np.isfinite(us) and np.isfinite(ex)):
            continue
        cash = cash_12m(data["SPY"]["date"], i["SPY"])
        w[d] = ({"SPY": 1.0} if us >= ex else {"EFA": 1.0}) if us > cash else {"IEF": 1.0}
    return weights_to_positions(data, w)
