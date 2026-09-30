import numpy as np
from catalogus._common import month_end, hold_monthly
RULE = {"id": "C61_ls_inverse", "naam": "SPX Faber long / −1× inverse (dagelijks gereset, TER 0,50%) onder de 10-mnd-SMA", "familie": "trend (long/short)", "instrumenten": ["SPX"], "field": "close",
        "vehicle": "etf_inverse", "laag_omloop": True, "start_jaar": 1928, "mechanisme": "Long in uptrend; in downtrend inverse-ETF → verdient in bearmarkten, lagere correlatie in drawdowns dan C02.",
        "bron": "Faber (2007) + UCITS-inverse (Xtrackers S&P 500 Inverse Daily Swap, TER 0,50% = web-claim)", "varianten": {"basis": {}}}
def positions(df, p):
    c = df["close"]; me = month_end(df["date"]); idx = np.where(me)[0]; tgt = np.full(len(c), np.nan)
    for k in range(9, len(idx)):
        i = idx[k]; tgt[i] = 1.0 if c[i] > np.mean(c[idx[k - 9:k + 1]]) else -1.0
    return hold_monthly(tgt, me)
