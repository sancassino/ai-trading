import numpy as np
from catalogus._common import FX6, sigma
RULE = {"id": "C04_ema", "naam": "EMA 50/200-kruising (FX-majors + goud), vol-geschaald", "familie": "trend", "instrumenten": FX6 + ["GOLD_F"], "max_pos": 3.0,
        "vehicle": "future", "start_jaar": 1990, "mechanisme": "Trendvolging op weken-horizon; onder-reactie op informatie.", "bron": "klassieke MA-crossover; Neely e.a. (FX-technische regels)",
        "varianten": {"basis": {}}}
def ema(x, n):
    a = 2 / (n + 1); o = np.empty(len(x)); o[0] = x[0]
    for i in range(1, len(x)):
        o[i] = o[i - 1] + a * (x[i] - o[i - 1])
    return o
def positions(df, p):
    c = df["close"]; s = np.sign(ema(c, 50) - ema(c, 200)); s[:200] = 0
    return s * np.minimum(3.0, 0.10 / np.nan_to_num(sigma(c, 60), nan=1.0))
