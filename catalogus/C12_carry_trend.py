import numpy as np
from catalogus._common import FX6, month_end, ret_back, hold_monthly
from engine.run_rule import rate_on
RULE = {"id": "C12_carry_trend", "naam": "FX-carry G7 met 3m-trendfilter", "familie": "carry", "instrumenten": FX6, "laag_omloop": True,
        "mechanisme": "Carry = compensatie voor crashrisico; trendfilter vermijdt carry-crashes.", "bron": "Lustig–Roussanov–Verdelhan (2011); Menkhoff e.a. (2012)",
        "varianten": {"basis": {}}}
CCY = {"FX_EURUSD": ("EUR", 1), "FX_GBPUSD": ("GBP", 1), "FX_AUDUSD": ("AUD", 1), "FX_USDJPY": ("JPY", -1), "FX_USDCAD": ("CAD", -1), "FX_USDCHF": ("CHF", -1)}
def positions_all(data, p):
    import bisect
    info = {}
    for n, df in data.items():
        ccy, orient = CCY[n]
        carry = rate_on(ccy, df["date"]) - rate_on("USD", df["date"])
        mom = ret_back(df["close"], 63) * orient          # rendement van X tegen USD
        info[n] = (df, carry, mom, orient, month_end(df["date"]))
    cal = sorted({d for df in data.values() for d in df["date"]})
    ends = sorted({(d.year, d.month): d for d in cal}.values())
    tgt_by_end = {}
    for e in ends:
        sc = {}
        for n, (df, carry, mom, orient, me) in info.items():
            i = bisect.bisect_right(df["date"], e) - 1
            if i >= 63 and (e - df["date"][i]).days <= 5 and np.isfinite(carry[i]) and np.isfinite(mom[i]):
                sc[n] = (carry[i], mom[i], orient)
        t = {}
        if len(sc) >= 6:
            order = sorted(sc, key=lambda k: sc[k][0])
            for n in order[-3:]:
                t[n] = sc[n][2] * 1.0 if sc[n][1] > 0 else 0.0
            for n in order[:3]:
                t[n] = -sc[n][2] * 1.0 if sc[n][1] < 0 else 0.0
        tgt_by_end[e] = t
    ends_sorted = sorted(tgt_by_end); pos = {}
    for n, (df, *_ ) in info.items():
        out = np.zeros(len(df["date"])); cur = 0.0; j = 0
        for i, d in enumerate(df["date"]):
            while j < len(ends_sorted) and ends_sorted[j] <= d:
                cur = tgt_by_end[ends_sorted[j]].get(n, 0.0); j += 1
            out[i] = cur
        pos[n] = out
    return pos
