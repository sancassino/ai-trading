import bisect
from datetime import date
import numpy as np
from catalogus._common import IDX5
RULE = {"id": "C17_fomc_cycle", "naam": "FOMC-cyclus: lang in even weken", "familie": "kalender/Fed", "instrumenten": IDX5, "start_jaar": 1994,
        "field": "close", "mechanisme": "Fed-informatiestroom en informele communicatie in de even weken van de FOMC-cyclus.",
        "bron": "Cieslak, Morse, Vissing-Jorgensen (2019)", "varianten": {"basis": {}}}
def fomc_dates():
    ds = set()
    for line in open("fomc_dates_1994_2020.txt"):
        line = line.strip()
        if line[:1].isdigit():
            ds.add(date.fromisoformat(line[:10]))
    for line in open("events.csv"):
        f = line.strip().split(";")
        if len(f) >= 2 and f[1] == "FOMC" and f[0][:1].isdigit():
            ds.add(date.fromisoformat(f[0]))
    return sorted(ds)
WINDOWS = [(-1, 4), (9, 14), (19, 24), (29, 34)]
def positions(df, p):
    from engine.run_rule import load_daily
    spx = load_daily("SPX", "close"); cal = list(spx["date"]); F = fomc_dates()
    tday = {d: i for i, d in enumerate(cal)}
    # FOMC-dag-index in SPX-kalender (eerste handelsdag ≥ besluitdag)
    fidx = sorted({bisect.bisect_left(cal, f) for f in F if f >= cal[0]})
    pos = np.zeros(len(df["date"]))
    for i, d in enumerate(df["date"]):
        k = bisect.bisect_right(cal, d) - 1                  # SPX-handelsdagindex t/m d
        # positie ná slot d geldt voor dag d+1 → gebruik de cyclustelling van de volgende SPX-handelsdag
        k1 = k + 1
        j = bisect.bisect_right(fidx, k1 + 1) - 1           # laatste FOMC-index ≤ k1+1 (dag −1 telt mee)
        on = False
        for jj in (j, j + 1):
            if 0 <= jj < len(fidx):
                rel = k1 - fidx[jj]
                if any(a <= rel <= b for a, b in WINDOWS):
                    on = True
        pos[i] = 1.0 if on else 0.0
    return pos
