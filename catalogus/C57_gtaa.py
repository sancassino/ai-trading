import numpy as np
from catalogus._common import month_end, weights_to_positions
CL = ["SPY", "EFA", "IEF", "GLD", "DBC"]
RULE = {"id": "C57_gtaa", "naam": "Faber-GTAA: 10-mnd-SMA long/kas op 5 klassen (VS, ex-VS, obligatie, goud, grondstoffen), 1/5 per klasse", "familie": "trend/allocatie", "aggregatie": "som",
        "instrumenten": CL, "vehicle": "etf", "laag_omloop": True, "start_jaar": 2003, "benchmark": {"naam": "60/40 SPY/IEF", "gewichten": {"SPY": 0.6, "IEF": 0.4}},
        "mechanisme": "Trend per klasse met eigen (lage-correlatie) rendementsbron; kas als terugvaloptie.", "bron": "Faber (2007) 'A Quantitative Approach to Tactical Asset Allocation'",
        "varianten": {"basis": {}}}
def positions_all(data, p):
    cal = data["SPY"]["date"]; me = month_end(np.array(cal)); idx = {n: {d: i for i, d in enumerate(data[n]["date"])} for n in data}
    mds = [d for k, d in enumerate(cal) if me[k]]; w = {}
    for k, d in enumerate(mds):
        if k < 10:
            continue
        wt = {}
        for n in CL:
            vals = [data[n]["close"][idx[n][x]] if x in idx[n] else np.nan for x in mds[k - 9:k + 1]]
            if all(np.isfinite(vals)) and vals[-1] > np.mean(vals):
                wt[n] = 0.2
        w[d] = wt
    return weights_to_positions(data, w)
