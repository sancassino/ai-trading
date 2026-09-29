"""Exporteer M5-bars (servertijd) met spread naar C:\\Users\\sandro_cassino\\m5\\<SYM>.csv (draait op de VM)."""
import os, sys
from datetime import datetime
import MetaTrader5 as mt5
if not mt5.initialize(path=r"C:\Program Files\MetaTrader 5\terminal64.exe", timeout=60000):
    sys.exit(f"initialize FAILED: {mt5.last_error()}")
out = r"C:\Users\sandro_cassino\m5"
os.makedirs(out, exist_ok=True)
for s in sys.argv[1].split(","):
    mt5.symbol_select(s, True)
    info = mt5.symbol_info(s)
    rows = []
    for y in range(2021, 2027):  # per jaar ophalen (grootte-limieten)
        r = mt5.copy_rates_range(s, mt5.TIMEFRAME_M5, datetime(y, 1, 1), datetime(y + 1, 1, 1))
        if r is not None:
            rows.extend(r)
    with open(os.path.join(out, s.replace(".cash", "cash") + ".csv"), "w") as f:
        f.write(f"# point={info.point};digits={info.digits};contract={info.trade_contract_size}\n")
        f.write("time;open;high;low;close;spread\n")
        for x in rows:
            f.write(f"{datetime.utcfromtimestamp(int(x['time'])).strftime('%Y.%m.%d %H:%M')};{x['open']};{x['high']};{x['low']};{x['close']};{x['spread']}\n")
    print(s, len(rows), flush=True)
mt5.shutdown()
