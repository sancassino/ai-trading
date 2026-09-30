"""Exporteer tick_volume van M5-bars naar C:\\Users\\sandro_cassino\\m5_vol\\<SYM>.csv (time;tick_volume), aparte bestanden zodat
bestaande loaders (6 kolommen) niet breken. Draait op de VM."""
import os, sys
from datetime import datetime, timezone
import MetaTrader5 as mt5
if not mt5.initialize(path=r"C:\Program Files\MetaTrader 5\terminal64.exe", timeout=60000):
    sys.exit(f"initialize FAILED: {mt5.last_error()}")
out = r"C:\Users\sandro_cassino\m5_vol"; os.makedirs(out, exist_ok=True)
for s in sys.argv[1].split(","):
    mt5.symbol_select(s, True)
    n = 0
    with open(os.path.join(out, s.replace(".cash", "cash") + ".csv"), "w") as f:
        f.write("time;tick_volume\n")
        for y in range(2021, 2027):
            r = mt5.copy_rates_range(s, mt5.TIMEFRAME_M5, datetime(y, 1, 1), datetime(y + 1, 1, 1))
            for x in (r if r is not None else []):
                f.write(f"{datetime.fromtimestamp(int(x['time']), timezone.utc):%Y.%m.%d %H:%M};{int(x['tick_volume'])}\n"); n += 1
    print(s, n, flush=True)
mt5.shutdown()
