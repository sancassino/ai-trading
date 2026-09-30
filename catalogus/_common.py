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


def common_calendar(data, names):
    """gezamenlijke handelsdagen (inner join) van de genoemde reeksen + closes-matrix (R2, allocatieregels)."""
    sets = [set(data[n]["date"]) for n in names]
    cal = sorted(set.intersection(*sets)) if sets else []
    return cal


def to_series(df, cal_idx):
    """rij-index in df voor elke datum van cal_idx (dict datum → i)."""
    return {d: i for i, d in enumerate(df["date"])}


def weights_to_positions(data, weights_by_date):
    """weights_by_date: {datum: {naam: w}} (beslissing op slot van die dag) → per instrument een positie-array op de eigen kalender;
    doorgezet tot de volgende beslisdatum."""
    ends = sorted(weights_by_date); out = {}
    for n, df in data.items():
        pos = np.zeros(len(df["date"])); cur = 0.0; j = 0
        for i, d in enumerate(df["date"]):
            while j < len(ends) and ends[j] <= d:
                cur = weights_by_date[ends[j]].get(n, 0.0); j += 1
            pos[i] = cur
        out[n] = pos
    return out


def cash_12m(dates, i):
    """gemiddelde risicovrije rente over de 252 dagen tot en met dates[i], als 12m-rendement (fractie)."""
    from engine.run_rule import rf_on
    return float(np.mean(rf_on(dates[max(0, i - 251):i + 1])) / 100)


def series_on(name, dates, field="close"):
    """waarde van reeks `name` (data/daily) op elke datum, laatste bekende waarde (geen lookahead); NaN vóór de start."""
    from engine.run_rule import load_daily
    d = load_daily(name, field); ks = np.array(d["date"], dtype="datetime64[D]")
    j = np.searchsorted(ks, np.array(dates, dtype="datetime64[D]"), side="right") - 1
    return np.where(j >= 0, np.asarray(d["close"])[np.clip(j, 0, None)], np.nan)
