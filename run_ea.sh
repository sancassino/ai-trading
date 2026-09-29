#!/bin/bash
# Draai een EA in de Strategy Tester op de VM en haal de output op. Gebruik: ./run_ea.sh EXPERT OUTNAAM [inputs-bestand] [outdir]
VM=sandro_cassino@34.69.153.107; KEY=~/mt5_vm_key
C='C:/Users/sandro_cassino/AppData/Roaming/MetaQuotes/Terminal/Common/Files'
EXP=$1; N=$2; INP=${3:-}; OUT=${4:-results/f}; mkdir -p $OUT
ARG=""
if [ -n "$INP" ]; then scp -q -i $KEY "$INP" "$VM:C:/Users/sandro_cassino/ea_inputs.txt"; ARG="-InputsFile C:\Users\sandro_cassino\ea_inputs.txt"; fi
timeout 2000 ssh -o BatchMode=yes -i $KEY $VM "powershell -File C:\Users\sandro_cassino\vm_run_ea.ps1 -Expert $EXP -Period H1 $ARG -OutCsv $N"
scp -q -i $KEY "$VM:$C/$N" "$VM:$C/${N%.csv}_daily.csv" $OUT/ 2>/dev/null
echo SWEEP_DONE
