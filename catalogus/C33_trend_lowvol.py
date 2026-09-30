import numpy as np
from catalogus._common import U12, month_end, ret_back, sigma, hold_monthly
RULE = {"id": "C33_trend_lowvol", "naam": "TSMOM-mix alleen in laag-vol-regime (σ60 < eigen mediane σ60 tot t)", "familie": "trend/regime", "instrumenten": U12, "max_pos": 3.0,
        "vehicle": "future", "laag_omloop": True, "mechanisme": "Trends zijn betrouwbaarder in rustige regimes; hoge vol = reversals/crashes.", "bron": "catalogus C33; Moreira–Muir-idee toegepast als regime-filter",
        "varianten": {"basis": {}}}
def positions(df, p):
    c = df["close"]; sg = sigma(c, 60)
    s = (np.sign(ret_back(c, 21)) + np.sign(ret_back(c, 63)) + np.sign(ret_back(c, 252))) / 3
    med = np.full(len(c), np.nan)
    for i in range(300, len(c)):
        v = sg[:i + 1]; v = v[np.isfinite(v)]; med[i] = np.median(v) if len(v) > 250 else np.nan      # expanding, alleen verleden
    calm = (sg < med).astype(float)
    return hold_monthly(s * np.minimum(3.0, 0.10 / sg) * calm, month_end(df["date"]))
