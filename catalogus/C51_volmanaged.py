import numpy as np
from catalogus._common import month_end, sigma, hold_monthly
RULE = {"id": "C51_volmanaged", "naam": "Vol-managed index: gewicht = min(1; 10%/σ21), maandelijks", "familie": "volatiliteit/sizing",
        "instrumenten": ["SPX", "NDX", "DAX"], "field": "close", "vehicle": "etf", "laag_omloop": True,
        "mechanisme": "Risico/rendement is niet evenredig: bij hoge vol daalt het rendement per risico-eenheid, dus vol-schalen verbetert SR en DD.",
        "bron": "Moreira & Muir (2017); Harvey e.a. (2018)", "varianten": {"basis": {}}}
def positions(df, p):
    c = df["close"]; s = sigma(c, 21)
    tgt = np.minimum(1.0, 0.10 / s)
    return hold_monthly(tgt, month_end(df["date"]))
