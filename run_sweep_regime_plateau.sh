#!/bin/bash
# Plateau-sweep: TopN {2,3,4} x lookback {1,2,3} x regime-filter {0,10}, 30% exposure.
# Resultaten (deals + daily equity) komen in results/plateau/.
# Optioneel: REGIMES="10" DG=4 TG=8 EXPO=0.30 TAG=_g4_8 ./run_sweep_regime_plateau.sh
set -u
VM=sandro_cassino@34.69.153.107
KEY=~/mt5_vm_key
C='C:/Users/sandro_cassino/AppData/Roaming/MetaQuotes/Terminal/Common/Files'
OUT=results/plateau; mkdir -p $OUT
for R in ${REGIMES:-0 10}; do for T in 2 3 4; do for L in 1 2 3; do
  N="PL_t${T}_l${L}_r${R}${TAG:-}.csv"
  [ -f "$OUT/$N" ] && continue
  ssh -o BatchMode=yes -i $KEY $VM "powershell -File C:\Users\sandro_cassino\vm_run_momentum.ps1 -FromDate 2021.01.01 -ToDate 2026.09.24 -TopN $T -LookbackMonths $L -ExposureFrac ${EXPO:-0.30} -RegimeSMAMonths $R -DailyGuardPct ${DG:-0} -TotalGuardPct ${TG:-0} -OutCsv $N"
  scp -q -i $KEY "$VM:$C/$N" "$VM:$C/${N%.csv}_daily.csv" $OUT/
done; done; done
echo SWEEP_DONE
