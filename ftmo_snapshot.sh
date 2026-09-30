#!/bin/bash
# Dagelijkse FTMO-symbool-snapshot (D-086): swaps (tijdvariabel) + spreads + specs voor alle symbolen uit SymbolList_FTMO.csv. Cron ma–vr 21:30 UTC.
cd /home/sandro_cassino/ai-trading || exit 1
VM=sandro_cassino@34.69.153.107; KEY=~/mt5_vm_key
SYMS=$(awk -F';' 'NR>1{print $1}' SymbolList_FTMO.csv | paste -sd,)
mkdir -p data/ftmo_specs
OUT=data/ftmo_specs/$(date -u +%F).csv
scp -q -i $KEY mt5_symbol_snapshot.py $VM:C:/Users/sandro_cassino/mt5_symbol_snapshot.py
timeout 600 ssh -o BatchMode=yes -i $KEY $VM "python C:\Users\sandro_cassino\mt5_symbol_snapshot.py $SYMS" 2>/dev/null | tr -d '\r' | grep -v '^$' > "$OUT.tmp"
if [ $(wc -l < "$OUT.tmp") -gt 100 ]; then mv "$OUT.tmp" "$OUT"; else echo "$(date -u) snapshot mislukt ($(wc -l < "$OUT.tmp") regels)" >> results/ftmo_snapshot.log; rm -f "$OUT.tmp"; exit 1; fi
git pull -q --rebase --autostash origin main || true
git add "$OUT" && git commit -q -m "data/ftmo_specs: snapshot $(date -u +%F)" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || exit 0
for i in 1 2 3; do git push -q origin HEAD:main && break; git pull -q --rebase --autostash origin main; sleep 20; done
