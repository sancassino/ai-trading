#!/bin/bash
# Dagelijks forward-papier P1 ORB+BTC (D-095 stap 3 / D-096.5): recente M5 van de VM → data/m5_fwd → forward_p1.py → commit/push.
cd /home/sandro_cassino/ai-trading || exit 1
SYMS="US500.cash,US100.cash,US30.cash,XAUUSD,GER40.cash,UK100.cash,EURUSD,BTCUSD"
# copy_rates_from_pos (bevroren exporter) geeft na een MT5-herstart de verouderde cache (gezien 2026-10-01); mt5_warmup.py (copy_rates_range) ververst eerst.
timeout 600 ssh -o BatchMode=yes -o ConnectTimeout=30 -i ~/mt5_vm_key sandro_cassino@34.69.153.107 "python C:\\Users\\sandro_cassino\\mt5_warmup.py $SYMS"
for i in 1 2 3; do
  OUT=$(timeout 600 ssh -o BatchMode=yes -o ConnectTimeout=30 -i ~/mt5_vm_key sandro_cassino@34.69.153.107 "python C:\\Users\\sandro_cassino\\mt5_export_recent.py $SYMS US500.cash" 2>/dev/null)
  echo "$OUT" | grep -q "^M5;BTCUSD" && break
  sleep 120
done
echo "$OUT" | .venv/bin/python update_m5_recent.py
.venv/bin/python forward_p1.py
git add forward/p1_daily.csv 2>/dev/null && git commit -q -m "forward P1: dagelijkse papierregel $(date -u +%F)" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || exit 0
for i in 1 2 3; do git push -q origin HEAD:main && break; git pull -q --rebase --autostash origin main; sleep 15; done
