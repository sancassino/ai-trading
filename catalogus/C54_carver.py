import numpy as np
from engine.run_rule import rate_on
RULE = {"id": "C54_carver", "naam": "Carver-forecastcombinatie: EWMAC(8,32/16,64/32,128/64,256) + FX-carry, 16 instrumenten, vol-target per instrument 10%",
        "familie": "trend+carry (multi-asset)", "vehicle": "future", "max_pos": 3.0, "laag_omloop": False,
        "instrumenten": ["FX_EURUSD", "FX_GBPUSD", "FX_USDJPY", "FX_AUDUSD", "FX_USDCAD", "FX_USDCHF", "GOLD_F", "SILVER_F", "WTI_F", "COPPER_F",
                         "SPX", "NDX", "DAX", "N225", "FTSE", "BOND10_SYN"],
        "benchmark": {"naam": "60/40 SPX/BOND10_SYN", "gewichten": {"SPX": 0.6, "BOND10_SYN": 0.4}},
        "mechanisme": "Trend (onder-reactie, hedgers) en carry (risicopremie) over veel weinig-gecorreleerde markten; diversificatie is de hefboom.",
        "bron": "Carver (2015) 'Systematic Trading'; Hurst–Ooi–Pedersen (2017); Koijen e.a. (2018)", "varianten": {"basis": {}}}
SCAL = {(8, 32): 5.3, (16, 64): 3.75, (32, 128): 2.65, (64, 256): 1.87}
def ema(x, span):
    a = 2 / (span + 1); out = np.empty(len(x)); out[0] = x[0]
    for i in range(1, len(x)):
        out[i] = out[i - 1] + a * ((x[i] if np.isfinite(x[i]) else out[i - 1]) - out[i - 1])
    return out
def positions(df, p):
    c = df["close"]; n = len(c)
    r = np.r_[0.0, c[1:] / c[:-1] - 1]; var = np.empty(n); var[0] = 1e-4
    for i in range(1, n):
        var[i] = var[i - 1] + (2 / 36) * (r[i] ** 2 - var[i - 1])            # EWMA-variantie, span 35
    sd_d = np.sqrt(var)                                                     # dagvol (fractie)
    sd_a = sd_d * np.sqrt(252)
    fc = np.zeros(n)
    for (f, s), sc in SCAL.items():
        raw = ema(c, f) - ema(c, s)
        fc += np.clip(raw / (c * sd_d) * sc, -20, 20) / len(SCAL)
    if df["name"].startswith("FX_"):
        carry = (rate_on(df["name"][3:6], df["date"]) - rate_on(df["name"][6:9], df["date"])) / 100
        fcar = np.clip(30 * np.nan_to_num(carry) / sd_a, -20, 20)
        fc = 0.6 * fc + 0.4 * fcar
    tgt = np.clip(fc / 10, -2, 2) * 0.10 / np.maximum(sd_a, 0.02)
    tgt[:260] = 0.0                                                         # inloop
    pos = np.zeros(n); cur = 0.0
    for i in range(n):
        buf = 0.1 * 0.10 / max(sd_a[i], 0.02)
        if abs(tgt[i] - cur) > buf:
            cur = tgt[i] - np.sign(tgt[i] - cur) * buf                       # Carver-buffer: trade naar de rand van de band
        pos[i] = cur
    return pos
