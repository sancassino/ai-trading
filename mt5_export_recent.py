"""Recente FTMO-data voor de papieren forward-test (draait op de VM). Uitvoer naar stdout:
'M5;SYM;time;open;high;low;close;spread' (laatste N_M5 bars) en 'D1;SYM;date;close' (laatste 320 bars)."""
import sys
from datetime import datetime, timezone
import MetaTrader5 as mt5
if not mt5.initialize(path=r"C:\Program Files\MetaTrader 5\terminal64.exe", timeout=60000):
    sys.exit(f"initialize FAILED: {mt5.last_error()}")
m5_syms, d1_syms = sys.argv[1].split(","), sys.argv[2].split(",")
for s in m5_syms:
    mt5.symbol_select(s, True)
    r = mt5.copy_rates_from_pos(s, mt5.TIMEFRAME_M5, 0, 2000)
    for x in (r if r is not None else []):
        t = datetime.fromtimestamp(int(x["time"]), timezone.utc).strftime("%Y.%m.%d %H:%M")
        print(f"M5;{s};{t};{x['open']};{x['high']};{x['low']};{x['close']};{x['spread']}")
for s in d1_syms:
    mt5.symbol_select(s, True)
    r = mt5.copy_rates_from_pos(s, mt5.TIMEFRAME_D1, 0, 320)
    for x in (r if r is not None else []):
        d = datetime.fromtimestamp(int(x["time"]), timezone.utc).strftime("%Y.%m.%d")
        print(f"D1;{s};{d};{x['close']}")
mt5.shutdown()
