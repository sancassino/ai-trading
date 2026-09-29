"""D1-OHLC per symbool (servertijd) naar stdout: 'SYM;date;open;high;low;close' (draait op de VM)."""
import sys
from datetime import datetime, timezone
import MetaTrader5 as mt5
mt5.initialize(path=r"C:\Program Files\MetaTrader 5\terminal64.exe", timeout=60000)
for s in sys.argv[1].split(","):
    mt5.symbol_select(s, True)
    r = mt5.copy_rates_range(s, mt5.TIMEFRAME_D1, datetime(2017, 1, 1), datetime(2026, 9, 30))
    for x in (r if r is not None else []):
        d = datetime.fromtimestamp(int(x["time"]), timezone.utc).strftime("%Y.%m.%d")
        print(f"{s};{d};{x['open']};{x['high']};{x['low']};{x['close']}")
mt5.shutdown()
