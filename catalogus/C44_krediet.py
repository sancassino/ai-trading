import numpy as np
from catalogus._common import month_end, hold_monthly, series_on
RULE = {"id": "C44_krediet", "naam": "Krediet-signaal: HYG/IEF-ratio 3m-trend > 0 → SPY lang, anders kas", "familie": "cross-asset", "instrumenten": ["SPY"], "vehicle": "etf",
        "laag_omloop": True, "start_jaar": 2008, "mechanisme": "Kredietspreads leiden aandelen (informatie in obligatiemarkt); risk-off vroeg zichtbaar.", "bron": "catalogus C44; Gilchrist–Zakrajšek (2012)",
        "varianten": {"basis": {}}}
def positions(df, p):
    h = series_on("HYG", df["date"], "adjclose"); i_ = series_on("IEF", df["date"], "adjclose"); r = h / i_; n = len(r); m = np.full(n, np.nan); m[63:] = r[63:] / r[:-63] - 1
    return hold_monthly(np.where(np.isfinite(m), (m > 0).astype(float), np.nan), month_end(df["date"]))
