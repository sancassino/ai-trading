"""Test van s3_histdata op een synthetisch HistData-bestand: FTMO-M5 (2021–2023) → M1 in EST zonder DST (HistData-formaat, zip)
→ parser → b4_sim.run_orb; vergelijk met run_orb op de originele FTMO-data (zelfde dagen, zelfde bruto uitkomst verwacht)."""
import os
import shutil
import tempfile
import zipfile
from datetime import timedelta, timezone
from zoneinfo import ZoneInfo

import b4_sim
import s3_histdata

NY = ZoneInfo("America/New_York")
EST = timezone(timedelta(hours=-5))
TEST = {"US500cash": "SPXUSD", "GER40cash": "GRXEUR"}


def to_est(server):
    return (server - timedelta(hours=7)).replace(tzinfo=NY).astimezone(EST).replace(tzinfo=None)


def make_zip(sym, hd, d):
    lines = []
    for t, o, h, l, c, _ in b4_sim.load(sym):
        if not (2021 <= t.year <= 2023):
            continue
        e = to_est(t)
        path = [o, h, l, c, c] if c >= o else [o, l, h, c, c]  # 5 M1-bars die samen exact (o, h, l, c) geven
        prev = o
        for k, p in enumerate(path):
            hi, lo = max(prev, p), min(prev, p)
            lines.append(f"{e + timedelta(minutes=k):%Y%m%d %H%M%S};{prev};{hi};{lo};{p};0")
            prev = p
    with zipfile.ZipFile(os.path.join(d, f"HISTDATA_COM_ASCII_{hd}_M1_2021-2023.zip"), "w") as zf:
        zf.writestr(f"DAT_ASCII_{hd}_M1_2021-2023.csv", "\n".join(lines))


def gross(trades_sess, comm):
    return {d: round(n, 10) for d, n, _ in b4_sim.run_orb(trades_sess, comm)}


def main():
    src, out = tempfile.mkdtemp(), tempfile.mkdtemp()
    try:
        for s, hd in TEST.items():
            make_zip(s, hd, src)
        s3_histdata.convert(src, out, years=(2021, 2023))
        ok_all = True
        for s in TEST:
            zero = lambda sess: [(d, [b[:5] + (0.0,) for b in bars]) for d, bars in sess]  # bruto: spread 0
            ref_sess = [(d, bars) for d, bars in b4_sim.sessions(s) if 2021 <= d.year <= 2023]
            ref = gross(zero(ref_sess), 0.0)
            orig = b4_sim.load
            import s3_run
            s3_run.SRC = out
            b4_sim.load = s3_run.load_long
            try:
                new = gross(zero(b4_sim.sessions(s)), 0.0)
            finally:
                b4_sim.load = orig
            same = sum(1 for d in ref if d in new and abs(ref[d] - new[d]) < 1e-9)
            print(f"{s}: FTMO-trades {len(ref)}, na parser {len(new)}, identiek {same} "
                  f"({'OK' if same == len(ref) == len(new) else 'AFWIJKING'})")
            ok_all &= same == len(ref) == len(new)
            # DST-controle: maartweek 2022 (VS al zomertijd, Europa nog niet)
            dst = [d for d in ref if d.year == 2022 and d.month == 3 and 14 <= d.day <= 25]
            print(f"   DST-mismatchweken maart 2022: {len(dst)} trades, allemaal gelijk: {all(d in new and abs(ref[d] - new[d]) < 1e-9 for d in dst)}")
        print("PARSER-TEST " + ("GESLAAGD" if ok_all else "MISLUKT"))
    finally:
        shutil.rmtree(src); shutil.rmtree(out)


if __name__ == "__main__":
    main()
