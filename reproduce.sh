#!/bin/bash
# N6 — herberekent de kernresultaten uit gecommitte data + code en vergelijkt met de waarden in RUNLOG.md.
# Gebruik: ./reproduce.sh   (duurt enkele minuten; geen VM/MT5 nodig — MT5-uitkomsten komen uit results/f/*.csv)
cd "$(dirname "$0")"
PASS=0; FAIL=0
check() {  # check "omschrijving" "gevonden" "verwacht"
  if [ "$2" = "$3" ]; then echo "PASS  $1: $2"; PASS=$((PASS+1)); else echo "FAIL  $1: gevonden '$2', verwacht '$3'"; FAIL=$((FAIL+1)); fi
}
echo "== Checksums ruwe data (sha256) =="
sha256sum -c data/CHECKSUMS.sha256 --quiet && echo "PASS  checksums ruwe data" && PASS=$((PASS+1)) || { echo "FAIL  checksums ruwe data"; FAIL=$((FAIL+1)); }

if [ -d data/m5 ] && sha256sum -c data/CHECKSUMS_m5_lokaal.sha256 --quiet 2>/dev/null; then echo "INFO  M5-export (niet in git) identiek aan de gebruikte snapshot"; else echo "INFO  data/m5 ontbreekt of wijkt af → opnieuw exporteren met mt5_export_m5.py; K1/F-resultaten kunnen dan licht verschillen"; fi

echo "== B2: RSI(2) Yahoo 1990–2026, gepoold (RUNLOG: t 3,65, N 1.381) =="
B2=$(python3 b2_sim.py 2>/dev/null | awk '$1=="b"{print $3" "$7}')
check "B2 RSI(2) trades en t" "$B2" "1381 3.65"

echo "== K1: max 1 / max 2 nachten, Yahoo t (RUNLOG: 3,05 / 3,59) =="
K1=$(python3 k1_nights.py 2>/dev/null | grep -oE 'Yahoo N [0-9]+, [+-][0-9.]+ bp, t [+-][0-9.]+' | awk '{print $NF}' | tr '\n' ' ' | sed 's/ $//')
check "K1 Yahoo t (a, b)" "$K1" "+3.05 +3.59"

echo "== N5: onafhankelijke audit — alle vergelijkingen 100% =="
N5=$(python3 audit_n5.py 2>/dev/null | grep -c '(100.0%) | rendement-afwijking 0 | alleen mijn 0 | alleen ref 0')
check "N5 aantal 100%-vergelijkingen" "$N5" "11"

echo "== F3b: MT5-combinatie (RUNLOG: SR 0,95, slechtste dag 3,80%) =="
F3=$(python3 - <<'EOF'
import csv, stats_tools as st
rows=[r for r in csv.DictReader(open('results/f/F3b_comb_daily.csv'),delimiter=';')]
eq=[float(r['end_equity']) for r in rows]; rets=[eq[i]/eq[i-1]-1 for i in range(1,len(eq))]
worst=max((float(r['start_balance'])-float(r['min_equity']))/80000 for r in rows)
print(f"{st.sharpe(rets)[0]:.2f} {worst*100:.2f}")
EOF
)
check "F3b SR en slechtste dag" "$F3" "0.95 3.80"

echo "== N3: plafondtabel (RUNLOG: RSI(2) orig SR 0,49 / €84; max1 SR 0,48 / €99) =="
N3=$(python3 - <<'EOF'
import csv, stats_tools as st
S=80000
for f,t in (("results/f/F1_RSI2_swapcorr_daily.csv",0.62),("results/f/N1_max1_swapcorr_daily.csv",2.8)):
    rows=[r for r in csv.DictReader(open(f),delimiter=';')]; prev=S; rets=[]
    for r in rows:
        en=S+t*(float(r['end_equity'])-S); rets.append(en/prev-1); prev=en
    cagr=(prev/S)**(252/len(rets))-1
    print(f"{st.sharpe(rets)[0]:.2f}/{cagr*S/12:.0f}", end=" ")
EOF
)
check "N3 SR/€ per maand" "$(echo $N3)" "0.49/84 0.48/99"

echo "== Resultaat: $PASS geslaagd, $FAIL mislukt =="
[ $FAIL -eq 0 ]
