"""Dagelijkse incrementele update van data/daily (forward, D-050): per Yahoo-reeks alleen de laatste ~30 dagen ophalen en nieuwe datums toevoegen
(bestaande regels worden niet gewijzigd; een koerscorrectie van Yahoo op een bestaande datum wordt gelogd, niet overschreven).
US Treasury 3m/2j/10j/30j: lopend jaar opnieuw. Eerlijke UA, 3 s tussen verzoeken. Gebruik: python update_daily.py [naam ...]"""
import csv
import io
import json
import os
import sys
import time
import urllib.request
from datetime import date, datetime, timezone

UA = "ai-trading-research/1.0 (daily research data; slow; respects 429)"
LOG = "results/update_daily.log"


def log(msg):
    with open(LOG, "a") as f:
        f.write(f"{datetime.now(timezone.utc):%Y-%m-%d %H:%M}Z {msg}\n")
    print(msg, flush=True)


def yahoo_ticker(path):
    first = open(path).readline()
    return first.split("Yahoo chart-API ")[1].split(",")[0].strip() if "Yahoo chart-API" in first else None


def fetch_recent(ticker):
    p1 = int(time.time()) - 35 * 86400
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.request.quote(ticker)}"
           f"?period1={p1}&period2={int(time.time()) + 86400}&interval=1d&events=div,split&includeAdjustedClose=true")
    time.sleep(3)
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
        res = json.load(r)["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    adj = (res["indicators"].get("adjclose") or [{}])[0].get("adjclose") or [None] * len(res.get("timestamp", []))
    out = []
    for ts, o, h, l, c, v, a in zip(res.get("timestamp", []), q["open"], q["high"], q["low"], q["close"], q.get("volume") or [None] * len(q["close"]), adj):
        if c is None:
            continue
        f = lambda x: "" if x is None else f"{x:.6g}"
        out.append((time.strftime("%Y-%m-%d", time.gmtime(ts)), f(o), f(h), f(l), f(c), f(a if a is not None else c), "" if v is None else str(int(v))))
    return out


def update_yahoo(path):
    tk = yahoo_ticker(path)
    if not tk:
        return 0
    lines = open(path).read().splitlines()
    have = {l.split(";")[0]: l for l in lines if l[:1].isdigit()}
    last = max(have) if have else "0000"
    new = []
    today = date.today().isoformat()
    for row in fetch_recent(tk):
        d = row[0]
        if d >= today:            # lopende (onvolledige) dag niet opslaan
            continue
        if d in have:
            old_c = have[d].split(";")[4]
            if old_c and row[4] and abs(float(old_c) / float(row[4]) - 1) > 1e-4:
                log(f"  {os.path.basename(path)} {d}: Yahoo-slot gewijzigd {old_c} → {row[4]} (niet overschreven)")
        elif d > last:
            new.append(";".join(row))
    if new:
        with open(path, "a") as f:
            f.write("\n".join(new) + "\n")
    return len(new)


def update_treasury():
    y = date.today().year
    cols = {"3 Mo": "YLD_US3M", "2 Yr": "YLD_US2Y", "10 Yr": "YLD_US10Y", "30 Yr": "YLD_US30Y"}
    time.sleep(3)
    url = (f"https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/{y}/all"
           f"?type=daily_treasury_yield_curve&field_tdr_date_value={y}&page&_format=csv")
    txt = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=90).read().decode("utf-8-sig")
    n = 0
    for c, name in cols.items():
        p = f"data/daily/{name}.csv"
        have = {l.split(";")[0] for l in open(p) if l[:1].isdigit()}
        last = max(have)
        rows = sorted((datetime.strptime(r["Date"], "%m/%d/%Y").date().isoformat(), float(r[c])) for r in csv.DictReader(io.StringIO(txt)) if r.get(c) not in (None, "", "N/A"))
        new = [f"{d};;;;{v:.6g};{v:.6g};" for d, v in rows if d > last]
        if new:
            with open(p, "a") as f:
                f.write("\n".join(new) + "\n")
            n += len(new)
    return n


def main():
    names = sys.argv[1:]
    paths = [f"data/daily/{n}.csv" for n in names] if names else sorted(p for p in (f"data/daily/{x}" for x in os.listdir("data/daily")) if p.endswith(".csv"))
    tot = 0
    for p in paths:
        try:
            k = update_yahoo(p); tot += k
        except Exception as e:
            log(f"  {os.path.basename(p)}: FOUT {e}")
    try:
        tot += update_treasury()
    except Exception as e:
        log(f"  Treasury: FOUT {e}")
    log(f"update_daily: {tot} nieuwe regels in {len(paths)} bestanden")


if __name__ == "__main__":
    main()
