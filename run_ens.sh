#!/bin/bash
# Ensemble-EA (TopN 2,3,4 x lb 1,2,3), SMA10, €80k EUR. CONFIGS="universe_bestand,expo,guard ..."
VM=sandro_cassino@34.69.153.107; KEY=~/mt5_vm_key
C='C:/Users/sandro_cassino/AppData/Roaming/MetaQuotes/Terminal/Common/Files'
OUT=results/ens; mkdir -p $OUT
for cfg in $CONFIGS; do IFS=, read U E G <<< "$cfg"
  N="ENS_${U%.txt}_e${E}_g${G}.csv"; N=${N/universe_/}; [ -f "$OUT/$N" ] && continue
  timeout 1900 ssh -o BatchMode=yes -i $KEY $VM "powershell -File C:\Users\sandro_cassino\vm_run_momentum.ps1 -FromDate 2021.01.01 -ToDate 2026.09.24 -ExposureFrac $(awk "BEGIN{print $E/100}") -RegimeSMAMonths 10 -DailyGuardPct $G -EnsembleTopNs '2,3,4' -EnsembleLookbacks '1,2,3' -UniverseList 'file:$U' -Deposit 80000 -Currency EUR -MaxWait 1800 -OutCsv $N"
  scp -q -i $KEY "$VM:$C/$N" "$VM:$C/${N%.csv}_daily.csv" "$VM:$C/${N%.csv}_ranks.csv" $OUT/
done; echo SWEEP_DONE
