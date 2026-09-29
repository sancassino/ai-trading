#!/bin/bash
# lb=1, TopN {2,3,4}, regime SMA10, daily guard 4%, exposure-sweep.
VM=sandro_cassino@34.69.153.107; KEY=~/mt5_vm_key
C='C:/Users/sandro_cassino/AppData/Roaming/MetaQuotes/Terminal/Common/Files'
OUT=results/plateau
for E in ${EXPOS:-45 60}; do for T in 2 3 4; do
  N="PL_t${T}_l1_r10_g${DG:-4}_e${E}.csv"; [ -f "$OUT/$N" ] && continue
  ssh -o BatchMode=yes -i $KEY $VM "powershell -File C:\Users\sandro_cassino\vm_run_momentum.ps1 -FromDate 2021.01.01 -ToDate 2026.09.24 -TopN $T -LookbackMonths 1 -ExposureFrac 0.$E -RegimeSMAMonths 10 -DailyGuardPct ${DG:-4} -OutCsv $N"
  scp -q -i $KEY "$VM:$C/$N" "$VM:$C/${N%.csv}_daily.csv" $OUT/
done; done; echo SWEEP_DONE
