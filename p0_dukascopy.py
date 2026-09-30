"""P0: lange M1-data 2011–2020 van de publieke Dukascopy-datafeed, traag en netjes (NEXT_STEPS v16, D-014/D-018).

Regels: eerlijke User-Agent (geen browser-imitatie), 1 verzoek per 4 s, 429/503 → Retry-After of exponentieel wachten (max 15 min),
na 6 mislukte pogingen op rij stoppen en loggen; hervatbaar (bestaande bestanden worden overgeslagen); zaterdagen overgeslagen.
Uitvoer: data/dukascopy_raw/<SYM>/<jaar>/<mm>/<dd>.bi5 en per symbool/jaar een zip in HistData-formaat (EST = UTC−5) in data/long_m1/,
zodat s3_histdata.py / run_s3.sh ongewijzigd werken.
Gebruik: python p0_dukascopy.py [SYM ...]   (standaard SPX → NSX → GRX → XAU)"""
import io
import lzma
import os
import struct
import sys
import time
import urllib.error
import urllib.request
import zipfile
from datetime import date, datetime, timedelta, timezone

UA = "ai-trading-research/1.0 (slow, resumable; respects 429/Retry-After)"
BASE = "https://datafeed.dukascopy.com/datafeed"
MAP = {"SPXUSD": "USA500IDXUSD", "NSXUSD": "USATECHIDXUSD", "GRXEUR": "DEUIDXEUR", "XAUUSD": "XAUUSD"}
FTMO = {"SPXUSD": "US500cash", "NSXUSD": "US100cash", "GRXEUR": "GER40cash", "XAUUSD": "XAUUSD"}
RAW = "data/dukascopy_raw"
OUT = "data/long_m1"
PAUSE = 8.0
LOG = "results/p0/p0_log.txt"


def log(msg):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    line = f"{datetime.now(timezone.utc):%Y-%m-%d %H:%M:%S}Z {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


class Stop(Exception):
    pass


_fails = 0


def fetch(inst, d):
    """geeft bytes (kan leeg zijn), None bij 404; wacht netjes bij 429/503."""
    global _fails
    url = f"{BASE}/{inst}/{d.year}/{d.month - 1:02d}/{d.day:02d}/BID_candles_min_1.bi5"
    wait = 60
    while True:
        time.sleep(PAUSE)
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
                _fails = 0
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                _fails = 0
                return None
            if e.code in (429, 503):
                _fails += 1
                if _fails >= 6:
                    raise Stop(f"{e.code} zes keer op rij bij {url}")
                ra = e.headers.get("Retry-After")
                w = int(ra) if ra and ra.isdigit() else wait
                log(f"  {e.code} bij {inst} {d}; wacht {w} s (poging {_fails})")
                time.sleep(w); wait = min(wait * 2, 900)
                continue
            raise
        except (urllib.error.URLError, TimeoutError) as e:
            _fails += 1
            if _fails >= 6:
                raise Stop(f"netwerkfout zes keer op rij: {e}")
            time.sleep(wait); wait = min(wait * 2, 900)


def decode(raw, d, div):
    if not raw:
        return []
    data = lzma.decompress(raw)
    day0 = datetime(d.year, d.month, d.day)
    out = []
    for i in range(len(data) // 24):
        t, o, c, l, h, v = struct.unpack(">IIIIIf", data[i * 24:(i + 1) * 24])
        if v <= 0:
            continue  # geen handel/quotes in die minuut
        out.append((day0 + timedelta(seconds=t), o / div, h / div, l / div, c / div))
    return out


def divisor(hd, inst):
    """kies de deler die de prijs van 2022-03-01 14:00 UTC het best laat passen op het FTMO-slot van dat uur."""
    raw = fetch(inst, date(2022, 3, 1))
    data = lzma.decompress(raw)
    t, o, c, l, h, v = struct.unpack(">IIIIIf", data[14 * 60 * 24:(14 * 60 + 1) * 24])
    ftmo = None
    for line in open(f"data/m5/{FTMO[hd]}.csv"):
        if line.startswith("2022.03.01 16:00"):  # 14:00 UTC = 09:00 NY (EST) = 16:00 server
            ftmo = float(line.split(";")[4]); break
    best = min((1, 10, 100, 1000, 10000, 100000), key=lambda k: abs(c / k - ftmo) / ftmo)
    log(f"{hd}: deler {best} (Dukascopy {c / best:.2f} vs FTMO {ftmo:.2f}, verschil {abs(c / best - ftmo) / ftmo * 100:.2f}%)")
    if abs(c / best - ftmo) / ftmo > 0.02:
        raise Stop(f"{hd}: prijsniveau past niet op FTMO (>2%)")
    return best


def run(hd):
    inst = MAP[hd]
    div = divisor(hd, inst)
    for year in range(2011, 2021):
        zpath = os.path.join(OUT, f"HISTDATA_COM_ASCII_{hd}_M1{year}.zip")
        if os.path.exists(zpath):
            continue
        d, rows, n404, seen, nonempty = date(year, 1, 1), [], 0, 0, 0
        while d.year == year:
            if seen >= 10 and nonempty == 0:
                log(f"{hd} {year}: eerste 10 werkdagen leeg/404 → jaar niet beschikbaar op de feed, overgeslagen")
                break
            if d.weekday() != 5:
                p = os.path.join(RAW, hd, str(year), f"{d.month:02d}", f"{d.day:02d}.bi5")
                if os.path.exists(p):
                    raw = open(p, "rb").read()
                else:
                    raw = fetch(inst, d)
                    if raw is None:
                        n404 += 1; raw = b""
                    os.makedirs(os.path.dirname(p), exist_ok=True)
                    open(p, "wb").write(raw)
                if d.weekday() < 5:
                    seen += 1; nonempty += bool(raw)
                for t, o, h, l, c in decode(raw, d, div):
                    est = t - timedelta(hours=5)
                    rows.append(f"{est:%Y%m%d %H%M%S};{o};{h};{l};{c};0")
            d += timedelta(days=1)
        if not rows:
            continue
        os.makedirs(OUT, exist_ok=True)
        with zipfile.ZipFile(zpath + ".tmp", "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(f"DAT_ASCII_{hd}_M1_{year}.csv", "\n".join(sorted(rows)))
        os.replace(zpath + ".tmp", zpath)
        log(f"{hd} {year}: {len(rows)} M1-regels, {n404} dagen zonder bestand (404) → {zpath}")


if __name__ == "__main__":
    syms = sys.argv[1:] or ["SPXUSD", "NSXUSD", "GRXEUR", "XAUUSD"]
    log(f"start P0 voor {', '.join(syms)} (pauze {PAUSE} s, UA '{UA}')")
    try:
        for hd in syms:
            run(hd)
        log("P0 KLAAR")
    except Stop as e:
        log(f"P0 GESTOPT (netjes): {e}")
