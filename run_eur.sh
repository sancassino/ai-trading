#!/bin/bash
# Kernconfigs opnieuw op het echte account: €80.000, EUR. Output: results/eur/
VM=sandro_cassino@34.69.153.107; KEY=~/mt5_vm_key
C='C:/Users/sandro_cassino/AppData/Roaming/MetaQuotes/Terminal/Common/Files'
OUT=results/eur; mkdir -p $OUT
CONFIGS="${CONFIGS:-2,3,0,0,30 2,1,10,3,60 2,1,10,0,30 2,2,10,0,30 2,3,10,0,30 3,1,10,0,30 3,2,10,0,30 3,3,10,0,30 4,1,10,0,30 4,2,10,0,30 4,3,10,0,30}"
for cfg in $CONFIGS; do IFS=, read T L R G E <<< "$cfg"
  N="EUR_t${T}_l${L}_r${R}_g${G}_e${E}.csv"; [ -f "$OUT/$N" ] && continue
  ssh -o BatchMode=yes -i $KEY $VM "powershell -File C:\Users\sandro_cassino\vm_run_momentum.ps1 -FromDate 2021.01.01 -ToDate 2026.09.24 -TopN $T -LookbackMonths $L -ExposureFrac 0.$E -RegimeSMAMonths $R -DailyGuardPct $G -Deposit 80000 -Currency EUR -MaxWait 900 -OutCsv $N"
  scp -q -i $KEY "$VM:$C/$N" "$VM:$C/${N%.csv}_daily.csv" "$VM:$C/${N%.csv}_ranks.csv" $OUT/
done; echo SWEEP_DONE
