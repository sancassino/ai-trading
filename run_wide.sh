#!/bin/bash
# Breed universum (universe_wide.txt, 65 symbolen). Args via env: TOPS LBS R DG EXPO UFILE PFX RA=true IV=true
VM=sandro_cassino@34.69.153.107; KEY=~/mt5_vm_key
C='C:/Users/sandro_cassino/AppData/Roaming/MetaQuotes/Terminal/Common/Files'
OUT=results/wide; mkdir -p $OUT; U=file:${UFILE:-universe_wide.txt}
for T in ${TOPS:-3}; do for L in ${LBS:-1}; do
  N="${PFX:-W}_t${T}_l${L}_r${R:-10}_g${DG:-0}_e${EXPO:-30}${RA:+_ra}${IV:+_iv}.csv"; [ -f "$OUT/$N" ] && continue
  ssh -o BatchMode=yes -i $KEY $VM "powershell -File C:\Users\sandro_cassino\vm_run_momentum.ps1 -FromDate 2021.01.01 -ToDate 2026.09.24 -TopN $T -LookbackMonths $L -ExposureFrac 0.${EXPO:-30} -RegimeSMAMonths ${R:-10} -DailyGuardPct ${DG:-0} -UniverseList '$U' -RankByRiskAdj ${RA:-false} -UseInverseVolWeight ${IV:-false} -MaxWait 1800 -OutCsv $N"
  scp -q -i $KEY "$VM:$C/$N" "$VM:$C/${N%.csv}_daily.csv" "$VM:$C/${N%.csv}_ranks.csv" $OUT/
done; done; echo SWEEP_DONE
