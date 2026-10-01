"""Recente M5-bars (laatste N dagen) voor een paar symbolen naar stdout (draait op de VM). Voor het dagelijkse forward-papier (P1, D-095).
Uitvoer per symbool: regel '## <SYM> point=<p>' gevolgd door 'YYYY.MM.DD HH:MM;open;high;low;close;spread' (servertijd, zelfde formaat als mt5_export_m5).
Gebruik: python mt5_export_recent.py SYM1,SYM2 [dagen]"""
import sys
from datetime import datetime, timedelta, timezone
import MetaTrader5 as mt5
if not mt5.initialize(path=r"C:\Program Files\MetaTrader 5\terminal64.exe", timeout=60000):
    sys.exit(f"initialize FAILED: {mt5.last_error()}")
days = int(sys.argv[2]) if len(sys.argv) > 2 else 10
end = datetime.now() + timedelta(days=1); start = end - timedelta(days=days + 1)
for s in sys.argv[1].split(","):
    mt5.symbol_select(s, True)
    i = mt5.symbol_info(s)
    r = mt5.copy_rates_range(s, mt5.TIMEFRAME_M5, start, end)
    print(f"## {s.replace('.cash', 'cash')} point={i.point}")
    for x in (r if r is not None else []):
        t = datetime.fromtimestamp(int(x["time"]), timezone.utc)
        print(f"{t:%Y.%m.%d %H:%M};{x['open']};{x['high']};{x['low']};{x['close']};{int(x['spread'])}")
mt5.shutdown()
