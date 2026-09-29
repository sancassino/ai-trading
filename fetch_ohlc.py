"""OHLC-dagdata: Yahoo (chart-API, ongecorrigeerde OHLC) of Stooq -> data/ohlc/<naam>.csv (date;open;high;low;close)."""
import csv, io, json, os, sys, time, urllib.request
os.makedirs("data/ohlc", exist_ok=True)
ADJ = os.environ.get("ADJ") == "1"  # ETF's: dividend-gecorrigeerde OHLC
def yahoo(t):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=567993600&period2=1790000000&interval=1d&events=div,split"
    res = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30))["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    adj = res["indicators"].get("adjclose", [{}])[0].get("adjclose") if ADJ else None
    out = []
    for i, (ts, o, h, l, c) in enumerate(zip(res["timestamp"], q["open"], q["high"], q["low"], q["close"])):
        if None in (o, h, l, c):
            continue
        f = adj[i] / c if adj and adj[i] else 1.0  # dividend-correctie (ETF's): O/H/L/C op adjusted-schaal
        out.append((time.strftime("%Y.%m.%d", time.gmtime(ts)), o * f, h * f, l * f, c * f))
    return out
def stooq(s):
    txt = urllib.request.urlopen(urllib.request.Request(f"https://stooq.com/q/d/l/?s={s}&i=d", headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read().decode()
    return [(r["Date"].replace("-", "."), float(r["Open"]), float(r["High"]), float(r["Low"]), float(r["Close"])) for r in csv.DictReader(io.StringIO(txt))]
for spec in sys.argv[1:]:
    src, t, name = spec.split(":")
    try:
        rows = yahoo(t) if src == "y" else stooq(t)
        with open(f"data/ohlc/{name}.csv", "w") as f:
            f.write("date;open;high;low;close\n"); f.writelines(f"{d};{o};{h};{l};{c}\n" for d, o, h, l, c in rows)
        print(f"{name}: {len(rows)} dagen {rows[0][0]} .. {rows[-1][0]}")
    except Exception as e:
        print(f"{name}: FOUT {e}")
    time.sleep(0.5)
