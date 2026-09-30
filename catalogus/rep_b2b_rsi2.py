"""Replicatie B2b (validatie van de engine, geen nieuwe hypothese): RSI(2) < 10 boven SMA200 → long, uit bij RSI(2) > 70."""
import numpy as np

RULE = {"id": "rep_b2b_rsi2", "naam": "RSI(2)-dip boven SMA200 (replicatie B2b)", "familie": "kortetermijn-omkeer",
        "mechanisme": "Liquiditeitsvoorziening na korte uitverkoop in een opwaartse trend; kopers worden betaald voor overnight-risico.",
        "bron": "Connors & Alvarez (2008); eerder getest als B2b (t 3,65)", "instrumenten": ["SPX", "NDX", "DAX", "FTSE", "N225", "GOLD_F"],
        "field": "adjclose", "start_jaar": 1990, "dataset": "D2 (replicatie, telt niet als nieuwe trial)",
        "varianten": {"basis": {"entry": 10, "exit": 70, "sma": 200}}}


def rsi2(c):
    out = np.full(len(c), np.nan); up = dn = None
    for i in range(1, len(c)):
        ch = c[i] - c[i - 1]; u, d = max(ch, 0), max(-ch, 0)
        if up is None:
            up, dn = u, d
        else:
            up, dn = (up + u) / 2, (dn + d) / 2
        out[i] = 100 if dn == 0 else 100 - 100 / (1 + up / dn)
    return out


def positions(df, p):
    c = df["close"]; r = rsi2(c)
    sma = np.convolve(c, np.ones(p["sma"]) / p["sma"], mode="full")[:len(c)]
    pos = np.zeros(len(c)); inpos = False
    for i in range(p["sma"], len(c)):
        if inpos and r[i] > p["exit"]:
            inpos = False
        elif not inpos and r[i] < p["entry"] and c[i] > sma[i]:
            inpos = True
        pos[i] = 1.0 if inpos else 0.0
    return pos
