"""D-044(d): officiële openbare bronnen voor rentes/CPI (FRED is vanaf onze IP's geblokkeerd; niet omzeild).
US Treasury (daily par yield curve, 1990→), MoF Japan (JGB, 1974→), Bank of England (10j gilt, IUDMNZC), Bundesbank (10j Bund, Svensson, 1997→),
BLS (CPI-U CUUR0000SA0, API v1 zonder sleutel). Eerlijke UA, 3 s tussen verzoeken. Uitvoer: data/daily/YLD_*.csv, data/daily/CPI_US.csv
(kolommen als D2: date;open;high;low;close;adjclose;volume, alleen close/adjclose gevuld)."""
import csv
import io
import json
import time
import urllib.request
from datetime import date, datetime

UA = "ai-trading-research/1.0 (daily research data; slow)"


def get(url, data=None, headers=None):
    h = {"User-Agent": UA}
    h.update(headers or {})
    time.sleep(3)
    with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=h), timeout=90) as r:
        return r.read().decode("utf-8-sig", errors="replace")


def write(name, rows, src):
    rows = sorted({d: v for d, v in rows}.items())
    with open(f"data/daily/{name}.csv", "w") as f:
        f.write(f"# bron: {src}, opgehaald {date.today()} (officieel, openbaar)\ndate;open;high;low;close;adjclose;volume\n")
        for d, v in rows:
            f.write(f"{d.isoformat()};;;;{v:.6g};{v:.6g};\n")
    print(f"{name}: {len(rows)} ({rows[0][0]} .. {rows[-1][0]})", flush=True)


def treasury():
    cols = {"3 Mo": "YLD_US3M", "2 Yr": "YLD_US2Y", "10 Yr": "YLD_US10Y", "30 Yr": "YLD_US30Y"}
    out = {v: [] for v in cols.values()}
    for y in range(1990, date.today().year + 1):
        txt = get(f"https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/{y}/all"
                  f"?type=daily_treasury_yield_curve&field_tdr_date_value={y}&page&_format=csv")
        for r in csv.DictReader(io.StringIO(txt)):
            d = datetime.strptime(r["Date"], "%m/%d/%Y").date()
            for c, n in cols.items():
                if r.get(c) not in (None, "", "N/A"):
                    out[n].append((d, float(r[c])))
    for n, rows in out.items():
        write(n, rows, "US Treasury daily par yield curve (home.treasury.gov)")


def jgb():
    txt = get("https://www.mof.go.jp/english/policy/jgbs/reference/interest_rate/historical/jgbcme_all.csv")
    rows = []
    rd = csv.reader(io.StringIO(txt)); next(rd); hdr = next(rd); k = hdr.index("10Y")
    for r in rd:
        if len(r) > k and r[k] not in ("", "-"):
            rows.append((datetime.strptime(r[0], "%Y/%m/%d").date(), float(r[k])))
    write("YLD_JP10Y", rows, "Ministry of Finance Japan, JGB constant maturity (jgbcme_all.csv)")


def gilt():
    txt = get("https://www.bankofengland.co.uk/boeapps/database/_iadb-fromshowcolumns.asp?csv.x=yes&SeriesCodes=IUDMNZC"
              "&Datefrom=01/Jan/1970&Dateto=now&CSVF=TN&UsingCodes=Y&VPD=Y&VFD=N")
    rows = [(datetime.strptime(r["DATE"], "%d %b %Y").date(), float(r["IUDMNZC"])) for r in csv.DictReader(io.StringIO(txt)) if r.get("IUDMNZC")]
    write("YLD_UK10Y", rows, "Bank of England database, IUDMNZC (10j nominale nulcoupon)")


def bund():
    txt = get("https://api.statistiken.bundesbank.de/rest/data/BBSIS/D.I.ZST.ZI.EUR.S1311.B.A604.R10XX.R.A.A._Z._Z.A?format=csv&lang=en")
    rows = []
    for r in csv.reader(io.StringIO(txt)):
        if r and r[0][:4].isdigit() and len(r) > 1 and r[1] not in ("", "."):
            try:
                rows.append((date.fromisoformat(r[0]), float(r[1])))
            except ValueError:
                pass
    write("YLD_DE10Y", rows, "Deutsche Bundesbank, BBSIS 10j (Svensson)")


def cpi():
    rows = []
    for y0 in range(1913, date.today().year + 1, 10):
        body = json.dumps({"seriesid": ["CUUR0000SA0"], "startyear": str(y0), "endyear": str(min(y0 + 9, date.today().year))}).encode()
        res = json.loads(get("https://api.bls.gov/publicAPI/v1/timeseries/data/", data=body, headers={"Content-type": "application/json"}))
        for s in res.get("Results", {}).get("series", []):
            for x in s["data"]:
                if x["period"].startswith("M") and x["period"] != "M13" and x["value"].replace(".", "", 1).isdigit():
                    rows.append((date(int(x["year"]), int(x["period"][1:]), 1), float(x["value"])))
    write("CPI_US", rows, "BLS CPI-U CUUR0000SA0 (maandelijks, datum = 1e van de maand; publicatie ≈ 2 weken later)")


if __name__ == "__main__":
    for f in (jgb, gilt, bund, cpi, treasury):
        try:
            f()
        except Exception as e:
            print(f"{f.__name__}: FOUT {e}", flush=True)


# ---------- D2b (S11 §4 rang 3): lokale korte rentes voor cross-market-replicatie ----------
def boe_short():
    for code, name in (("IUDBEDR", "YLD_UK_BANKRATE"), ("IUDSOIA", "YLD_UK_SONIA")):
        txt = get(f"https://www.bankofengland.co.uk/boeapps/database/_iadb-fromshowcolumns.asp?csv.x=yes&SeriesCodes={code}"
                  f"&Datefrom=01/Jan/1970&Dateto=now&CSVF=TN&UsingCodes=Y&VPD=Y&VFD=N")
        rows = [(datetime.strptime(r["DATE"], "%d %b %Y").date(), float(r[code])) for r in csv.DictReader(io.StringIO(txt)) if r.get(code)]
        write(name, rows, f"Bank of England database, {code}")


def snb():
    txt = get("https://data.snb.ch/api/cube/zimoma/data/csv/en")
    want = {"3M0": "YLD_CHF_LIBOR3M", "SARON": "YLD_CHF_SARON", "TONA": "YLD_JPY_TONA", "EG3M": "YLD_CHF_EG3M"}
    pts = {k: [] for k in want}
    for r in csv.reader(io.StringIO(txt), delimiter=";"):
        if len(r) == 3 and r[1] in want and r[2]:
            y, m = map(int, r[0].split("-")); pts[r[1]].append((date(y, m, 1), float(r[2])))
    for k, n in want.items():
        write(n, pts[k], f"Swiss National Bank data portal, cube zimoma, {k} (maandwaarde; datum = 1e van de maand)")


def boc():
    txt = get("https://www.bankofcanada.ca/valet/observations/V80691303/csv")
    rows = []
    started = False
    for r in csv.reader(io.StringIO(txt)):
        if r and r[0] == "date":
            started = True; continue
        if started and len(r) > 1 and r[1]:
            rows.append((date.fromisoformat(r[0]), float(r[1])))
    write("YLD_CAD_TBILL3M", rows, "Bank of Canada Valet, V80691303 (3-month treasury bill)")


def hkma():
    rows, off = [], 0
    while True:
        res = json.loads(get(f"https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/er-ir/hk-interbank-ir-daily?pagesize=1000&offset={off}"))
        recs = res["result"]["records"]
        rows += [(date.fromisoformat(x["end_of_day"]), float(x["ir_3m"])) for x in recs if x.get("ir_3m") not in (None, "")]
        if len(recs) < 1000:
            break
        off += 1000
    write("YLD_HKD_HIBOR3M", rows, "Hong Kong Monetary Authority API, HIBOR 3m (daily)")


def d2b():
    for f in (boe_short, snb, boc, hkma):
        try:
            f()
        except Exception as e:
            print(f"{f.__name__}: FOUT {e}", flush=True)


def bis_fx():
    """R2-006: BIS WS_XRU dagkoersen (lokale valuta per USD; publiek, bronvermelding BIS). Lange EM-FX voor lokale-valuta-indices."""
    areas = {"BR": "BRL", "MX": "MXN", "ID": "IDR", "IN": "INR", "KR": "KRW", "TW": "TWD", "SG": "SGD", "ZA": "ZAR", "HK": "HKD",
             "CN": "CNY", "TH": "THB", "CL": "CLP", "TR": "TRY", "AU": "AUD", "CA": "CAD", "CH": "CHF", "SE": "SEK", "NO": "NOK",
             "JP": "JPY", "GB": "GBP", "XM": "EUR"}
    for a, c in areas.items():
        try:
            txt = get(f"https://stats.bis.org/api/v1/data/WS_XRU/D.{a}.{c}.A?format=csv")
            rows = []
            for r in csv.DictReader(io.StringIO(txt)):
                v = r.get("OBS_VALUE")
                if v and v != "NaN":
                    rows.append((date.fromisoformat(r["TIME_PERIOD"]), float(v)))
            write(f"FXBIS_{c}", rows, f"BIS WS_XRU D.{a}.{c}.A ({c} per USD, dagelijks; bronvermelding BIS)")
        except Exception as e:
            print(f"BIS {c}: FOUT {e}", flush=True)
