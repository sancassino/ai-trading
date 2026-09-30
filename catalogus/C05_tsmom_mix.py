import numpy as np
from catalogus._common import U12, month_end, ret_back, sigma, hold_monthly
RULE = {"id": "C05_tsmom_mix", "naam": "TSMOM-mix 1/3/12m (vol-geschaald)", "familie": "trend", "instrumenten": U12, "max_pos": 3.0,
        "laag_omloop": True, "mechanisme": "Als C01, diversificatie over horizons.", "bron": "Hurst, Ooi, Pedersen (2017)", "varianten": {"basis": {}}}
def positions(df, p):
    c = df["close"]
    s = (np.sign(ret_back(c, 21)) + np.sign(ret_back(c, 63)) + np.sign(ret_back(c, 252))) / 3
    return hold_monthly(s * np.minimum(3.0, 0.10 / sigma(c, 60)), month_end(df["date"]))
