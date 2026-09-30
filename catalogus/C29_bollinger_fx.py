import numpy as np
RULE = {"id": "C29_bollinger_fx", "naam": "Z-score(20d) ±2 omkeer op FX-kruisen, 5 dagen vast", "familie": "mean-reversion", "instrumenten": ["EURGBP", "EURJPY", "EURCHF"],
        "vehicle": "future", "start_jaar": 2004, "events": True, "mechanisme": "FX-kruisen keren in range-regimes terug naar hun 20d-gemiddelde; liquiditeitsverschaffing.",
        "bron": "klassieke Bollinger-omkeer; catalogus C29", "varianten": {"basis": {}}}
def positions(df, p):
    c = df["close"]; n = len(c); pos = np.zeros(n); hold = 0; cur = 0.0
    for i in range(20, n):
        if hold > 0:
            pos[i] = cur; hold -= 1; continue
        w = c[i - 19:i + 1]; sd = w.std(ddof=1); z = (c[i] - w.mean()) / sd if sd > 0 else 0.0
        if abs(z) > 2:
            cur = -np.sign(z); hold = 4; pos[i] = cur
        else:
            cur = 0.0
    return pos
