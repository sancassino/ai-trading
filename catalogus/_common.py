"""Gedeelde hulpfuncties voor catalogusregels (geen lookahead: alles t/m slot t)."""
import numpy as np

U12 = ["FX_EURUSD", "FX_GBPUSD", "FX_USDJPY", "FX_AUDUSD", "FX_USDCAD", "FX_USDCHF", "GOLD_F", "SILVER_F", "SPX", "NDX", "DAX", "N225"]
FX6 = U12[:6]
IDX5 = ["SPX", "NDX", "DJI", "DAX", "N225"]


def month_end(dates):
    """True op de laatste handelsdag van elke maand (in de eigen reeks)."""
    m = np.array([d.year * 12 + d.month for d in dates])
    return np.r_[m[1:] != m[:-1], True]


def ret_back(c, k):
    out = np.full(len(c), np.nan); out[k:] = c[k:] / c[:-k] - 1; return out


def sigma(c, n=60):
    r = np.r_[np.nan, np.log(c[1:] / c[:-1])]; out = np.full(len(c), np.nan)
    for i in range(n, len(c)):
        out[i] = np.std(r[i - n + 1:i + 1], ddof=1) * np.sqrt(252)
    return out


def hold_monthly(target, me):
    """zet een maandeinde-doelpositie door tot het volgende maandeinde."""
    pos = np.zeros(len(target)); cur = 0.0
    for i in range(len(target)):
        if me[i] and np.isfinite(target[i]):
            cur = target[i]
        pos[i] = cur
    return pos
