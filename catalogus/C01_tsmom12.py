import numpy as np
from catalogus._common import U12, month_end, ret_back, sigma, hold_monthly
RULE = {"id": "C01_tsmom12", "naam": "TSMOM 12m multi-asset (vol-geschaald)", "familie": "trend", "instrumenten": U12, "max_pos": 3.0,
        "laag_omloop": True, "mechanisme": "Onder-reactie en hedgers die een risicopremie betalen; trends in futures-rendementen.",
        "bron": "Moskowitz, Ooi, Pedersen (2012)", "varianten": {"basis": {}}}
def positions(df, p):
    c = df["close"]; tgt = np.sign(ret_back(c, 252)) * np.minimum(3.0, 0.10 / sigma(c, 60))
    return hold_monthly(tgt, month_end(df["date"]))
