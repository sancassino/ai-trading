"""Exporteer D1-slotkoersen (date;close) per symbool naar stdout-blokken (draait op de VM).
Gebruik: python mt5_export_rates.py SYM1,SYM2,...  -> regels 'SYM;date;close'"""
import sys
from datetime import datetime, timezone
import MetaTrader5 as mt5

if not mt5.initialize(path=r"C:\Program Files\MetaTrader 5\terminal64.exe", timeout=60000):
    sys.exit(f"initialize FAILED: {mt5.last_error()}")
for s in sys.argv[1].split(","):
    mt5.symbol_select(s, True)
    r = mt5.copy_rates_range(s, mt5.TIMEFRAME_D1, datetime(2019, 1, 1), datetime(2026, 9, 30))
    for row in (r if r is not None else []):
        d = datetime.fromtimestamp(int(row["time"]), timezone.utc).strftime("%Y.%m.%d")
        print(f"{s};{d};{row['close']:.5f}")
mt5.shutdown()
