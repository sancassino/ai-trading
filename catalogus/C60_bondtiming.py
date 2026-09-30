import numpy as np
from catalogus._common import month_end, hold_monthly
RULE = {"id": "C60_bondtiming", "naam": "Obligatie-duurtiming: synthetische 10j-Treasury long als maandeindslot > gem. 10 maandeinden, anders kas", "familie": "trend", "instrumenten": ["BOND10_SYN"],
        "vehicle": "etf", "laag_omloop": True, "start_jaar": 1963, "mechanisme": "Rente-trends (persistentie van inflatie/beleid); lage of negatieve correlatie met aandelen.", "bron": "Faber (2007); Hurst–Ooi–Pedersen; catalogus C60 (test 1970–2000)",
        "varianten": {"basis": {}}}
def positions(df, p):
    c = df["close"]; me = month_end(df["date"]); idx = np.where(me)[0]; tgt = np.full(len(c), np.nan)
    for k in range(9, len(idx)):
        i = idx[k]; tgt[i] = 1.0 if c[i] > np.mean(c[idx[k - 9:k + 1]]) else 0.0
    return hold_monthly(tgt, me)
