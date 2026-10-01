"""D-097 / spoor 6: koppeltabel FTMO-symbool → langste dagelijkse proxyreeks in de repo (voor ≥ 10 jaar mechanisme-toetsen; FTMO-M5 voor kosten).
Uitvoer: data/PROXY_MAP_FTMO.csv. Geen analyse, geen resultaat — alleen beschikbaarheid."""
import csv
import os
from datetime import date

CCY = {"USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "NZD", "SEK", "NOK", "MXN", "ZAR", "SGD", "HKD", "CNH", "CZK", "HUF", "PLN", "ILS", "TRY", "CNY"}
BIS = {"BRL", "MXN", "IDR", "INR", "KRW", "TWD", "SGD", "ZAR", "HKD", "CNY", "THB", "CLP", "TRY", "AUD", "CAD", "CHF", "SEK", "NOK", "JPY", "GBP", "EUR"}
IDX = {"US500.cash": ["SPX_TR", "SPX"], "US100.cash": ["NDX", "NASDAQ_COMP"], "US30.cash": ["DJI"], "GER40.cash": ["DAX"], "UK100.cash": ["FTSE"],
       "JP225.cash": ["N225"], "HK50.cash": ["HSI"], "AUS200.cash": ["AXJO"], "FRA40.cash": ["CAC40"], "SPN35.cash": ["IBEX"], "N25.cash": ["AEX"],
       "EU50.cash": ["STOXX50"], "US2000.cash": ["RUT"], "DXY.cash": ["DXY"]}
CMD = {"XAUUSD": ["GOLD_F", "monthly:WB_GOLD"], "XAGUSD": ["SILVER_F", "monthly:WB_SILVER"], "XPTUSD": ["PLAT_F", "monthly:WB_PLATINUM"],
       "XPDUSD": ["PALL_F"], "XCUUSD": ["COPPER_F", "monthly:WB_COPPER"], "USOIL.cash": ["WTI_F", "monthly:WB_CRUDE_OIL_WTI"],
       "UKOIL.cash": ["BRENT_F", "monthly:WB_CRUDE_OIL_BRENT"], "NATGAS.cash": ["NATGAS_F", "monthly:WB_NATURAL_GAS_US"],
       "HEATOIL.c": ["HEATOIL_F"], "CORN.c": ["CORN_F", "monthly:WB_MAIZE"], "WHEAT.c": ["WHEAT_F", "monthly:WB_WHEAT_US_HRW"],
       "SOYBEAN.c": ["SOY_F", "monthly:WB_SOYBEANS"], "COFFEE.c": ["COFFEE_F", "monthly:WB_COFFEE_ARABICA"], "SUGAR.c": ["SUGAR_F", "monthly:WB_SUGAR_WORLD"],
       "COTTON.c": ["COTTON_F", "monthly:WB_COTTON_A_INDEX"], "COCOA.c": ["COCOA_F", "monthly:WB_COCOA"],
       "XAUEUR": ["GOLD_F+FXBIS_EUR"], "XAUAUD": ["GOLD_F+FXBIS_AUD"], "XAGEUR": ["SILVER_F+FXBIS_EUR"], "XAGAUD": ["SILVER_F+FXBIS_AUD"]}
CRYPTO = {"BTC": "BTC_USD", "ETH": "ETH_USD", "LTC": "LTC_USD", "XRP": "XRP_USD", "BCH": "BCH_USD", "ADA": "ADA_USD", "DOGE": "DOGE_USD", "XLM": "XLM_USD",
          "XMR": "XMR_USD", "DASH": "DASH_USD", "ETC": "ETC_USD", "SOL": "SOL_USD", "DOT": "DOT_USD", "LNK": "LINK_USD", "BNB": "BNB_USD", "AVA": "AVAX_USD", "UNI": "UNI_USD"}
STOCK = {"BRK.B": "BRK-B", "ADSGn": "ADS.DE", "AIRF": "AF.PA", "ALVG": "ALV.DE", "BAYGn": "BAYN.DE", "DBKGn": "DBK.DE", "IBE": "IBE.MC", "LVMH": "MC.PA",
         "VOWG_p": "VOW3.DE", "SIEGn": "SIE_DE", "BMW": "BMW_DE", "MBG": "MBG_DE"}


def span(name):
    for d in ("data/daily", "data/yahoo", "data/monthly", "data/derived"):
        p = f"{d}/{name}.csv"
        if os.path.exists(p):
            ds = [l.split(";")[0].split(",")[0] for l in open(p) if l[:1].isdigit()]
            if ds:
                return p, ds[0][:10].replace(".", "-"), ds[-1][:10].replace(".", "-")
    return None, None, None


def first_year(parts):
    starts = []
    for x in parts:
        x = x.replace("monthly:", "")
        p, a, b = span(x)
        if not p:
            return None, []
        starts.append(a)
    return max(starts), parts


rows = []
for r in csv.DictReader(open("SymbolList_FTMO.csv"), delimiter=";"):
    s, path = r["symbol"], r["path"]
    m5 = os.path.exists(f"data/m5gz/{s.replace('.cash', 'cash')}.csv.gz")
    cand, cat, note = [], "", ""
    if s in IDX:
        cat, cand = "index", [[x] for x in IDX[s]]
    elif s in CMD:
        cat = "commodity/metal"; cand = [x.split("+") for x in CMD[s]]
    elif "Crypto" in path:
        base = s[:-3]; cat = "crypto"
        cand = [[CRYPTO[base]]] if base in CRYPTO else []
        note = "crypto: < 10 jaar historie bestaat niet (BTC/LTC 2014→, overige 2017/2020→)"
    elif len(s) == 6 and s[:3] in CCY and s[3:] in CCY:
        cat = "fx"; b, q = s[:3], s[3:].replace("CNH", "CNY")
        legs = [f"FXBIS_{c}" for c in (b, q) if c != "USD"]
        if all(c in BIS or c == "USD" for c in (b, q.replace("CNY", "CNY"))):
            cand = [legs]; note = f"cross uit BIS (lokaal per USD): {s} = {'1' if q == 'USD' else 'FXBIS_' + q} / {'1' if b == 'USD' else 'FXBIS_' + b}"
        y = {"EURUSD": "FX_EURUSD", "GBPUSD": "FX_GBPUSD", "USDJPY": "FX_USDJPY", "AUDUSD": "FX_AUDUSD", "USDCAD": "FX_USDCAD", "USDCHF": "FX_USDCHF", "NZDUSD": "FX_NZDUSD"}.get(s)
        if y:
            cand.insert(0, [y])
    else:
        cat = "stock"; t = STOCK.get(s, s)
        cand = [[t]]
    best = (None, None)
    for c in cand:                      # volgorde = voorkeur (dagdata eerst): eerste met ≥ 10 jaar wint, anders de langste
        fy, parts = first_year(c)
        if fy and (date(2024, 12, 31) - date.fromisoformat(fy)).days >= 3652:
            best = (fy, parts); break
        if fy and (best[0] is None or fy < best[0]):
            best = (fy, parts)
    fy, parts = best
    yrs = (date(2024, 12, 31) - date.fromisoformat(fy)).days / 365.25 if fy else 0
    rows.append((s, cat, "+".join(parts) if parts else "", fy or "", f"{yrs:.1f}", "ja" if yrs >= 10 else "nee", "ja" if m5 else "nee",
                 note or ("monthly = World Bank maandgemiddelde (geen dagdata)" if parts and any(p.startswith("monthly:") for p in parts) else "")))
with open("data/PROXY_MAP_FTMO.csv", "w") as f:
    f.write("# FTMO-symbool → langste proxyreeks in de repo (D-097/spoor 6; alleen beschikbaarheid). 'jaren_tm_2024' = jaren historie t/m 2024-12-31.\n")
    f.write("ftmo_symbol;categorie;proxy;proxy_start;jaren_tm_2024;10j_plus;m5gz;opmerking\n")
    for r in rows:
        f.write(";".join(r) + "\n")
from collections import Counter
c = Counter((r[1], r[5]) for r in rows)
print(len(rows), "symbolen;", ", ".join(f"{k[0]} {k[1]}={v}" for k, v in sorted(c.items())))
print("zonder proxy:", [r[0] for r in rows if not r[2]])
