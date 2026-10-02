"""Recente FTMO-data voor de papieren forward-test (draait op de VM). Uitvoer naar stdout:
'M5;SYM;time;open;high;low;close;spread' (laatste N_M5 bars) en 'D1;SYM;date;close' (laatste 320 bars)."""
import sys
import time
from datetime import datetime, timezone
import MetaTrader5 as mt5


def fresh(sym, tf, n, lag):
    """copy_rates_from_pos geeft eerst de oude cache; MT5 synchroniseert asynchroon (gezien 2026-10-01: US500 bleef op 01:15 staan terwijl de
    tick 12:18 was). Opnieuw vragen tot de laatste bar binnen `lag` seconden van de laatste tick ligt (max 15 s). Alleen ophalen, geen regelwijziging."""
    r = None
    for _ in range(16):
        r = mt5.copy_rates_from_pos(sym, tf, 0, n)
        tk = mt5.symbol_info_tick(sym)
        if r is not None and len(r) and tk is not None and tk.time and int(r[-1]["time"]) >= tk.time - lag:
            break
        time.sleep(1)
    return r


if not mt5.initialize(path=r"C:\Program Files\MetaTrader 5\terminal64.exe", timeout=60000):
    sys.exit(f"initialize FAILED: {mt5.last_error()}")
m5_syms, d1_syms = sys.argv[1].split(","), sys.argv[2].split(",")
for s in m5_syms:
    mt5.symbol_select(s, True)
    r = fresh(s, mt5.TIMEFRAME_M5, 2000, 600)
    for x in (r if r is not None else []):
        t = datetime.fromtimestamp(int(x["time"]), timezone.utc).strftime("%Y.%m.%d %H:%M")
        print(f"M5;{s};{t};{x['open']};{x['high']};{x['low']};{x['close']};{x['spread']}")
for s in d1_syms:
    mt5.symbol_select(s, True)
    r = fresh(s, mt5.TIMEFRAME_D1, 320, 2 * 86400)
    for x in (r if r is not None else []):
        d = datetime.fromtimestamp(int(x["time"]), timezone.utc).strftime("%Y.%m.%d")
        print(f"D1;{s};{d};{x['close']}")
mt5.shutdown()
