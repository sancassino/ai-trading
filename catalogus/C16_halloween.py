import numpy as np
RULE = {"id": "C16_halloween", "naam": "Halloween: lang indices nov–apr, anders kas", "familie": "seizoen", "instrumenten": ["SPX", "NDX", "DAX", "N225", "FTSE"],
        "field": "close", "vehicle": "etf", "laag_omloop": True, "mechanisme": "Seizoenspatroon in aandelenrendementen (zomer zwakker); gepubliceerd 2002 → verval mogelijk.",
        "bron": "Bouman & Jacobsen (2002)", "varianten": {"basis": {}}}
def positions(df, p):
    d = df["date"]; m = np.array([x.month for x in d]); nxt = np.r_[m[1:], m[-1]]      # maand van de volgende handelsdag (kalender bekend)
    return np.isin(nxt, [11, 12, 1, 2, 3, 4]).astype(float)
