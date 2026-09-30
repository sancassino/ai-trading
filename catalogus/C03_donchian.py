import numpy as np
from catalogus._common import FX6
RULE = {"id": "C03_donchian", "naam": "Donchian 55/20 D1 met 2×ATR-stop (slotbasis)", "familie": "trend", "instrumenten": FX6 + ["GOLD_F"],
        "mechanisme": "Breakout-trend (Turtle): doorbraak van een lange range kondigt een trend aan.", "bron": "Faith (2007), Turtle-regels",
        "varianten": {"basis": {}}}
def positions(df, p):
    c = df["close"]; n = len(c); pos = np.zeros(n); side = 0; ep = 0.0
    atr = np.full(n, np.nan); d = np.abs(np.diff(c, prepend=np.nan))
    for i in range(20, n):
        atr[i] = np.nanmean(d[i - 19:i + 1])
    for i in range(55, n):
        if side == 1 and (c[i] < c[i - 20:i].min() or c[i] < ep - 2 * atr[i]):
            side = 0
        elif side == -1 and (c[i] > c[i - 20:i].max() or c[i] > ep + 2 * atr[i]):
            side = 0
        if side == 0:
            if c[i] > c[i - 55:i].max():
                side, ep = 1, c[i]
            elif c[i] < c[i - 55:i].min():
                side, ep = -1, c[i]
        pos[i] = side
    return pos
