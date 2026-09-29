"""Haal accountinfo op via het MetaTrader5-package (draait op de Windows-VM)."""
import sys
import MetaTrader5 as mt5

TERMINAL = r"C:\Program Files\MetaTrader 5\terminal64.exe"

if not mt5.initialize(path=TERMINAL, timeout=60000):
    print("initialize FAILED:", mt5.last_error())
    sys.exit(1)
a = mt5.account_info()
if a is None:
    print("account_info FAILED:", mt5.last_error())
    mt5.shutdown()
    sys.exit(1)
print(f"login={a.login} server={a.server} balance={a.balance} equity={a.equity} currency={a.currency}")
mt5.shutdown()
