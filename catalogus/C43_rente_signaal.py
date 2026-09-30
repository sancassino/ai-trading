import numpy as np
from catalogus._common import month_end, hold_monthly, series_on
RULE = {"id": "C43_rente_signaal", "naam": "Rente-signaal: 10j-rente 3m stijgend → index kort, dalend → lang", "familie": "cross-asset", "instrumenten": ["SPX", "NDX", "DAX"],
        "field": "close", "vehicle": "future", "laag_omloop": True, "start_jaar": 1985, "mechanisme": "Hogere discontovoet drukt aandelenwaarderingen; rente-momentum leidt aandelen.",
        "bron": "catalogus C43; Fama–Schwert (1977) rente en aandelenrendement", "varianten": {"basis": {}}}
def positions(df, p):
    y = series_on("TNX_10Y", df["date"]); n = len(y); d63 = np.full(n, np.nan); d63[63:] = y[63:] - y[:-63]
    return hold_monthly(-np.sign(d63), month_end(df["date"]))
