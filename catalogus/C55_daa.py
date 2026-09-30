import numpy as np
from catalogus._common import month_end, ret_back, weights_to_positions
RISKY = ["SPY", "IWM", "EFA", "EEM", "VNQ", "DBC", "GLD", "TLT", "LQD", "HYG"]
RULE = {"id": "C55_daa", "naam": "Defensive asset allocation (Keller): canary EEM + AGG, top-6 van 10 risicoactiva, kas = SHY", "familie": "momentum/allocatie", "aggregatie": "som",
        "instrumenten": RISKY + ["AGG", "SHY"], "vehicle": "etf", "laag_omloop": True, "start_jaar": 2005, "benchmark": {"naam": "60/40 SPY/IEF", "gewichten": {"SPY": 0.6, "IEF": 0.4}},
        "mechanisme": "Breedte-momentum (canary) als crash-filter: beide canaries positief → volledig risico, één → half, geen → kas.", "bron": "Keller & Keuning (2018) DAA",
        "varianten": {"basis": {}}}
def mom(c, i):
    def rr(k):
        return c[i] / c[i - k] - 1 if i >= k else np.nan
    return (12 * rr(21) + 4 * rr(63) + 2 * rr(126) + rr(252)) / 19          # 13612W
def positions_all(data, p):
    idx = {n: {d: i for i, d in enumerate(data[n]["date"])} for n in data}; cal = data["SPY"]["date"]; me = month_end(np.array(cal)); w = {}
    for k, d in enumerate(cal):
        if not me[k] or d.year < 2004:
            continue
        m = {n: mom(data[n]["close"], idx[n][d]) if d in idx[n] else np.nan for n in data}
        can = [m["EEM"], m["AGG"]]
        if not all(np.isfinite(can)):
            continue
        nbad = sum(1 for x in can if x <= 0)
        cand = sorted([(m[n], n) for n in RISKY if np.isfinite(m[n])], reverse=True)[:6]
        risk_frac = {0: 1.0, 1: 0.5, 2: 0.0}[nbad]; wt = {}
        for _, n in cand:
            wt[n] = risk_frac / len(cand) if cand else 0.0
        wt["SHY"] = 1.0 - sum(wt.values())
        w[d] = wt
    return weights_to_positions(data, w)
