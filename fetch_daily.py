"""D2: lange dagdata (OHLC + adjclose + volume) → data/daily/<naam>.csv. Yahoo chart-API met eerlijke User-Agent, 3 s tussen verzoeken,
429/5xx → wachten (Retry-After of exponentieel), nooit browser-imitatie of andere omzeiling. Gebruik: python fetch_daily.py [naam ...]"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

UA = "ai-trading-research/1.0 (daily research data; slow; respects 429)"
OUT = "data/daily"
SERIES = {  # naam: Yahoo-ticker
    "SPX": "^GSPC", "NASDAQ_COMP": "^IXIC", "NDX": "^NDX", "DJI": "^DJI", "RUT": "^RUT", "DAX": "^GDAXI", "FTSE": "^FTSE",
    "N225": "^N225", "HSI": "^HSI", "STOXX50": "^STOXX50E", "CAC40": "^FCHI", "VIX": "^VIX", "TNX_10Y": "^TNX", "IRX_3M": "^IRX",
    "DXY": "DX-Y.NYB", "GOLD_F": "GC=F", "SILVER_F": "SI=F", "WTI_F": "CL=F", "COPPER_F": "HG=F", "NATGAS_F": "NG=F",
    "XLB": "XLB", "XLE": "XLE", "XLF": "XLF", "XLI": "XLI", "XLK": "XLK", "XLP": "XLP", "XLU": "XLU", "XLV": "XLV", "XLY": "XLY",
    "SPY": "SPY", "TLT": "TLT", "EURUSD": "EURUSD=X", "USDJPY": "JPY=X", "GBPUSD": "GBPUSD=X",
    # uitbreiding v19: total return, obligaties/krediet, internationaal, grondstoffen, meer FX
    "SPX_TR": "^SP500TR", "NDX_TR": "^XNDX", "IEF": "IEF", "SHY": "SHY", "LQD": "LQD", "HYG": "HYG", "TIP": "TIP", "AGG": "AGG",
    "EFA": "EFA", "EEM": "EEM", "IWM": "IWM", "GLD": "GLD", "SLV": "SLV", "DBC": "DBC", "VNQ": "VNQ",
    "AUDUSD": "AUDUSD=X", "USDCAD": "CAD=X", "USDCHF": "CHF=X", "NZDUSD": "NZDUSD=X", "FVX_5Y": "^FVX", "TYX_30Y": "^TYX",
    # D-044: meer instrumenten (C54), roll-inclusieve ETF-proxy's
    "USDSEK": "SEK=X", "USDNOK": "NOK=X", "EURGBP": "EURGBP=X", "EURJPY": "EURJPY=X", "EURCHF": "EURCHF=X",
    "CORN_F": "ZC=F", "WHEAT_F": "ZW=F", "SOY_F": "ZS=F", "COFFEE_F": "KC=F", "SUGAR_F": "SB=F", "COTTON_F": "CT=F", "CATTLE_F": "LE=F",
    "HEATOIL_F": "HO=F", "GASOLINE_F": "RB=F", "BRENT_F": "BZ=F", "PLAT_F": "PL=F", "PALL_F": "PA=F",
    "CPER": "CPER", "UNG": "UNG", "USO": "USO", "PPLT": "PPLT", "DBA": "DBA",
    "BUND_ETF": "EXX6.DE", "GILT_ETF": "IGLT.L", "BWX": "BWX", "EMB": "EMB", "SPX_EQW": "RSP",
    # D2b (S11/D-066): extra onafhankelijke aandelenmarkten + factor-ETF's (korte N, label)
    "AXJO": "^AXJO", "TSX": "^GSPTSE", "SMI": "^SSMI", "OMXS30": "^OMX", "KOSPI": "^KS11", "TWII": "^TWII", "BVSP": "^BVSP",
    "MXX": "^MXX", "IBEX": "^IBEX", "AEX": "^AEX", "BEL20": "^BFX", "STI": "^STI", "SENSEX": "^BSESN", "NIFTY": "^NSEI", "JKSE": "^JKSE",
    # R2-006: EM-FX (lokale valuta per USD) voor EM-indices
    "USDBRL": "BRL=X", "USDMXN": "MXN=X", "USDIDR": "IDR=X", "USDINR": "INR=X", "USDKRW": "KRW=X", "USDTWD": "TWD=X", "USDSGD": "SGD=X",
    "USDZAR": "ZAR=X", "USDHKD": "HKD=X", "USDAUD_INV": "AUD=X", "USDCNY": "CNY=X",
    # R2-007: Cboe-optiestrategie-indices (privé-repo; Cboe-indexdata: eigen onderzoek, niet herverspreiden)
    "CBOE_PUT": "^PUT", "CBOE_BXM": "^BXM", "CBOE_WPUT": "^WPUT", "CBOE_BXMD": "^BXMD", "CBOE_PPUT": "^PPUT", "VIX9D": "^VIX9D", "VIX3M": "^VIX3M",
    "MTUM": "MTUM", "QUAL": "QUAL", "USMV": "USMV", "VLUE": "VLUE", "EWA": "EWA", "EWC": "EWC", "EWL": "EWL", "EWS": "EWS", "EWY": "EWY", "EWZ": "EWZ",
}


def get(ticker):
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.request.quote(ticker)}"
           f"?period1=-2208988800&period2=1790000000&interval=1d&events=div,split&includeAdjustedClose=true")
    wait = 30
    for attempt in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
                return json.load(r)["chart"]["result"][0]
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503):
                ra = e.headers.get("Retry-After")
                time.sleep(int(ra) if ra and ra.isdigit() else wait); wait = min(wait * 2, 600); continue
            raise
        except (urllib.error.URLError, TimeoutError):
            time.sleep(wait); wait = min(wait * 2, 600)
    raise RuntimeError("te veel fouten")


def main():
    os.makedirs(OUT, exist_ok=True)
    names = sys.argv[1:] or list(SERIES)
    for n in names:
        try:
            res = get(SERIES[n])
            q = res["indicators"]["quote"][0]
            adj = (res["indicators"].get("adjclose") or [{}])[0].get("adjclose") or [None] * len(res["timestamp"])
            rows = []
            for ts, o, h, l, c, v, a in zip(res["timestamp"], q["open"], q["high"], q["low"], q["close"], q.get("volume") or [None] * len(q["close"]), adj):
                if c is None:
                    continue
                rows.append(f"{time.strftime('%Y-%m-%d', time.gmtime(ts))};{o if o is not None else ''};{h if h is not None else ''};"
                            f"{l if l is not None else ''};{c};{a if a is not None else c};{v if v is not None else ''}")
            with open(os.path.join(OUT, f"{n}.csv"), "w") as f:
                f.write(f"# bron: Yahoo chart-API {SERIES[n]}, opgehaald {time.strftime('%Y-%m-%d')} (eerlijke UA)\n")
                f.write("date;open;high;low;close;adjclose;volume\n" + "\n".join(rows) + "\n")
            print(f"{n}: {len(rows)} dagen {rows[0][:10]} .. {rows[-1][:10]}", flush=True)
        except Exception as e:
            print(f"{n}: FOUT {e}", flush=True)
        time.sleep(3)


if __name__ == "__main__":
    main()
