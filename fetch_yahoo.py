import urllib.request, json, csv, time

TICKERS = {
    "SP500": "^GSPC",
    "NASDAQ": "^IXIC",
    "DOW": "^DJI",
    "GOLD": "GC=F",
}

def fetch(ticker, period1=946684800, period2=1893456000):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={period1}&period2={period2}&interval=1d"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.load(resp)
    result = data["chart"]["result"][0]
    ts = result["timestamp"]
    closes = result["indicators"]["quote"][0]["close"]
    return list(zip(ts, closes))

for name, ticker in TICKERS.items():
    try:
        rows = fetch(ticker)
        out = f"YAHOO_{name}.csv"
        with open(out, "w", newline="") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(["date", "close"])
            for ts, c in rows:
                if c is None:
                    continue
                d = time.strftime("%Y.%m.%d", time.gmtime(ts))
                w.writerow([d, f"{c:.5f}"])
        print(f"{name}: wrote {len(rows)} rows to {out}")
    except Exception as e:
        print(f"{name}: FAILED {e}")
    time.sleep(1)
