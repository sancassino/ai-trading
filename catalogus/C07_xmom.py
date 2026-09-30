import numpy as np
from catalogus._common import U12, month_end
RULE = {"id": "C07_xmom", "naam": "Cross-asset momentum 12-1, lang top-3 / kort bottom-3", "familie": "cross-sectioneel", "instrumenten": U12,
        "laag_omloop": True, "mechanisme": "Relatieve trend tussen markten.", "bron": "Asness, Moskowitz, Pedersen (2013)", "varianten": {"basis": {}}}
def positions_all(data, p):
    # maandeinden volgens SPX-kalender (oudste lange reeks in U12 met indices); per maandeinde de laatste koers per instrument t/m die datum
    import bisect
    cal = sorted({d for df in data.values() for d in df["date"]})
    months = {}
    for d in cal:
        months[(d.year, d.month)] = d
    ends = sorted(months.values())
    pos = {n: np.zeros(len(df["date"])) for n, df in data.items()}
    tgt_by_end = {}
    for e in ends:
        scores = {}
        for n, df in data.items():
            i = bisect.bisect_right(df["date"], e) - 1
            if i >= 252 and (e - df["date"][i]).days <= 5:
                scores[n] = df["close"][i - 21] / df["close"][i - 252] - 1
        if len(scores) >= 6:
            order = sorted(scores, key=scores.get)
            tgt_by_end[e] = {n: (1.0 if n in order[-3:] else (-1.0 if n in order[:3] else 0.0)) for n in scores}
        else:
            tgt_by_end[e] = {}
    ends_sorted = sorted(tgt_by_end)
    for n, df in data.items():
        cur = 0.0; j = 0
        for i, d in enumerate(df["date"]):
            while j < len(ends_sorted) and ends_sorted[j] <= d:
                cur = tgt_by_end[ends_sorted[j]].get(n, 0.0); j += 1
            pos[n][i] = cur
    return pos
