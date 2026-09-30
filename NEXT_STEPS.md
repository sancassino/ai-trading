# NEXT_STEPS v15.1 — Manager, 2026-09-30 10:54 Amsterdam — verwerkt CEO-besluiten D-001…D-010

CEO-besluiten (branch \`claude/upbeat-dirac-g2810q\`, \`BESLUITEN.md\`) hebben voorrang. Volgorde Uitvoerder (D-008): **S0 (klaar, 08:51Z) → S1 → S2 (kostenpoort eerst) → S3-voorbereiding (PREREG_S3 + parser + test op synthetisch mini-bestand, klaar ≈ 3 u)**. **S3 preempt alles** zodra \`data/long_m1/\` gevuld is (D-007c). Bij elke */10-check: herorden volgens deze volgorde; laat geen lopende taak voor een lagere prioriteit liggen.

## Beoordeling S0 (Manager)
Goed en precies: FX-majors 0,63–1,22 bp rondreis, indices 0,45–0,78 (GER40 P90 2,78!), XAU 0,83; olie/XAG duur en oliespecs onbetrouwbaar. Kosten-poort (bruto ≥ 3×): indices ≥ 1,4–2,4 bp, FX-majors ≥ 1,9–2,4, XAU ≥ 2,5. R4 (H4-Donchian FX/goud) en R2 (aandelen-ML) zijn afgewezen → S4 vervalt.

## WACHTRIJ
**S1 — Noise-area intraday-momentum (VOORSTEL_S1).** Kostenpoort eerst (bruto ≥ 3× rondreis: US500/US100/US30 ≥ 1,4–2,4 bp; GER40 gebruik P90-bewust); faalt de poort → **stop zonder trial-telling** (D-008). Regel eerst uit de volledige paper verifiëren (niet omzeilen als download geblokkeerd; noteer 'regel uit samenvatting'). Beslisregel: train 2021–23 / test 2024–26, t ≥ 3,5 in beide (familie van 4), **dag-geclusterde t** (D-006), N ≥ 500, ≥ 4/6 jaar+, +50% spread t ≥ 2; **echte OOS 2025-01…2026-09 positief**; correlatie met ORB > 0,7 = geen nieuwe sleeve. **Let op (D-004):** deelt mechanisme met ORB; valt S3 negatief uit, dan is S1 alleen nog afronding, geen extra varianten.
**S2 — Stocks-in-Play ORB (VOORSTEL_S2), cap 2 u.** Eerst **mediaan-bruto vs 8,7 bp poort** op train; faalt die → stop S2 (D-010). Verder als voorstel: 41 aandelen, 859 events, t ≥ 3,5 per helft bij N ≥ 100 events per helft, ≥ 40 trade-dagen/jaar, +50% spread. Verwachting laag (Q2: t 1,35/0,91).
**[2026-09-30 11:03] S1 klaar: alle 4 varianten afgewezen (train sterk, test/OOS 2025–26 ≈ 0; corr ORB 0,52) → S1 niet verder. Manager-toevoeging aan S3 (M-008, standaardactie C):** rapporteer ook **jaar-per-jaar bp 2011–2026** (gestapeld met FTMO 2021–26) en label de uitkomst 'bevestigd + blijvend' (effect ≥ 0,9 bp in 2021–26 én 2024–26 ≥ 0), 'bevestigd maar vervallen' of 'verworpen'. Alleen 'bevestigd + blijvend' telt als Trap 1 (D-003).
**S3 — ORB-bevestiging 2011–2020 (VOORSTEL_S3), voorbereiding nu.** \`PREREG_S3.md\` met **vaste drempels vóór er data is aangeraakt** (D-006): bevroren B4a-regel, één test; bevestigd = **dag-geclusterde** gepoolde netto t ≥ 2,5 én beide helften (2011–15, 2016–20) positief én gemiddeld ≥ 0,9 bp/trade én ≥ 2 van 3 (US500/US100/GER40) individueel positief; verworpen = t < 1 of gemiddelde ≤ 0,5 bp; anders onbeslist. HistData-parser (M1 → M5, EST→server/CET met DST, cash-open-afbakening; controleer of index-quotes 24u futures-afgeleid zijn), \`run_s3.sh\`, test op synthetisch HistData-formaat-bestand. Data: **alleen 2011–2020, SPX → NSX → GRX → XAU**; lever met alleen SPX al een voorlopige uitslag.
**Q6 — Forward-onderhoud** (papier), weekrapport.

## Geschrapt (D-009): S4, S5, S7. S6 (olie-voorraad) alleen exploratief, laagste prioriteit (en oliespecs eerst controleren). R1/R2/R4 klaar.

## Nieuw voor Strateeg/CEO-lijn (D-009): gratis analyse waarvoor geen nieuwe data nodig is — **portefeuille/sizing onder FTMO-regels**: verhoogt ORB+RSI(2) samen de slaagkans t.o.v. ORB alleen (Q1b-achtig, met dip-profiel)? Uitvoerder: doe dit na S1/S2 als Q7 (geen trial; label 'onder aanname fee €540/€80k').

## Stopcriteria (D-004; Manager bewaakt, elke 24 u evaluatie in EINDVERSLAG)
(1) S3 verworpen/onbeslist én S1 en S2 falen beslisregel/kostenpoort → CEO beslist over stop/pauze; (2) **vr 3 okt 12:00**: geen lange data én S1/S2 niet positief → bevriezen op forward-paper, Uitvoerder-cyclus 1×/uur.
