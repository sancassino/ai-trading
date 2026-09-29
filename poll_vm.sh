#!/bin/bash
# Poll een achtergrond-sweep tot SWEEP_DONE of ~9 min; meldt als de tester-CPU stilstaat.
LOG=$1; LIMIT=${2:-540}; prev=-1; still=0
while [ $SECONDS -lt $LIMIT ]; do
  grep -q SWEEP_DONE $LOG && { echo KLAAR; break; }
  sleep 40
  read cpu free < <(ssh -o BatchMode=yes -o ConnectTimeout=15 -i ~/mt5_vm_key sandro_cassino@34.69.153.107 "[int](Get-Process metatester64,terminal64 -EA SilentlyContinue | Measure CPU -Sum).Sum; [int]((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1024)" 2>&1 | tr '\n' ' ')
  [ "$cpu" = "$prev" ] && still=$((still+40)) || still=0; prev=$cpu
  echo "$(date +%H:%M:%S) cpu=$cpu freeMB=$free"
  [ $still -ge 240 ] && { echo "STALL: CPU 4 min stil"; break; }
done | tail -2; grep -h "DONE\|TIMEOUT" $LOG
