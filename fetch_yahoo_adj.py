"""Download adjusted-close dagdata van Yahoo (chart-API) naar data/yahoo/<TICKER>.csv (date;close)."""
import json, sys, time, urllib.request, os

def fetch(t):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=883612800&period2=1790000000&interval=1d&events=div,split"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        res = json.load(r)["chart"]["result"][0]
    ts = res["timestamp"]
    adj = res["indicators"].get("adjclose", [{}])[0].get("adjclose") or res["indicators"]["quote"][0]["close"]
    return [(time.strftime("%Y.%m.%d", time.gmtime(a)), c) for a, c in zip(ts, adj) if c]

os.makedirs("data/yahoo", exist_ok=True)
for t in sys.argv[1:]:
    try:
        rows = fetch(t)
        with open(f"data/yahoo/{t.replace('=','_').replace('^','')}.csv", "w") as f:
            f.write("date;close\n"); f.writelines(f"{d};{c:.6f}\n" for d, c in rows)
        print(f"{t}: {len(rows)} dagen {rows[0][0]} .. {rows[-1][0]}")
    except Exception as e:
        print(f"{t}: FOUT {e}")
    time.sleep(0.5)
