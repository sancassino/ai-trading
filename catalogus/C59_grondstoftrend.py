import numpy as np
from catalogus._common import month_end, hold_monthly
RULE = {"id": "C59_grondstoftrend", "naam": "Grondstoffen-trend: long DBC als maandeindslot > gem. 10 maandeinden, anders kas", "familie": "trend", "instrumenten": ["DBC"], "vehicle": "etf", "laag_omloop": True,
        "start_jaar": 2007, "mechanisme": "Grondstoffenindex trendt (contango zit in de index); lage correlatie met obligaties.", "bron": "Faber (2007); catalogus C59 (korte reeks 2006→)", "varianten": {"basis": {}}}
def positions(df, p):
    c = df["close"]; me = month_end(df["date"]); idx = np.where(me)[0]; tgt = np.full(len(c), np.nan)
    for k in range(9, len(idx)):
        i = idx[k]; tgt[i] = 1.0 if c[i] > np.mean(c[idx[k - 9:k + 1]]) else 0.0
    return hold_monthly(tgt, me)
