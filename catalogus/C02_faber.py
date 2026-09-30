import numpy as np
from catalogus._common import IDX5, month_end, hold_monthly
RULE = {"id": "C02_faber", "naam": "Faber SMA-10-maanden long/cash op indices", "familie": "trend", "instrumenten": IDX5, "laag_omloop": True,
        "mechanisme": "Trend + drawdown-beperking: vermijd lange bear-markten.", "bron": "Faber (2007)", "field": "close", "varianten": {"basis": {}}}
def positions(df, p):
    c = df["close"]; me = month_end(df["date"]); idx = np.where(me)[0]; tgt = np.full(len(c), np.nan)
    for k in range(9, len(idx)):
        i = idx[k]; tgt[i] = 1.0 if c[i] > np.mean(c[idx[k - 9:k + 1]]) else 0.0
    return hold_monthly(tgt, me)
