import numpy as np
from catalogus._common import month_end, hold_monthly, series_on
RULE = {"id": "C45_rentecurve", "naam": "Rentecurve-regime: (10j − 3m) > 0 → SPX lang, anders kas", "familie": "cross-asset", "instrumenten": ["SPX"], "field": "close", "vehicle": "etf",
        "laag_omloop": True, "start_jaar": 1962, "mechanisme": "Omgekeerde curve voorspelt recessie; risicopremie-timing. (T10Y2Y niet beschikbaar → 10j − 3m uit TNX/IRX.)", "bron": "catalogus C45; Estrella–Mishkin (1998)",
        "varianten": {"basis": {}}}
def positions(df, p):
    s = series_on("TNX_10Y", df["date"]) - series_on("IRX_3M", df["date"])
    return hold_monthly(np.where(np.isfinite(s), (s > 0).astype(float), np.nan), month_end(df["date"]))
