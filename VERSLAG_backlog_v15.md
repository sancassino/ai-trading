# VERSLAG backlog v14/v15.1 (Uitvoerder, 2026-09-30)

| Taak | Uitkomst | Trials |
|---|---|---|
| S0 kosten | COSTS_FTMO.csv (+ per uur), swap 17 instrumenten, tick_volume-export. Rondreis: US30 0,45 · US100 0,66 · GER40 0,72 · US500 0,78 · XAU 0,83 · FX-majors 0,63–1,22 · olie 2,7–3,3 · XAG 5,1 bp | 0 |
| S1 noise-area | regel geverifieerd uit volledige paper (St. Gallen-repository); 4 varianten door kostenpoort, alle **afgewezen**: train t 1,3–3,4, test t 0,4–1,1, OOS 2025–26 ≈ 0; corr ORB 0,5 | +4 → 414 |
| S2 stocks-in-play ORB | regel geverifieerd (alleen OR-richting); mediaan-bruto −20…−53 bp → **poort faalt**, stop (D-010) | 0 |
| S3 voorbereiding | PREREG_S3 (drempels vast), s3_histdata.py, s3_run.py, run_s3.sh; parser-test 565/565 + 512/512 identiek incl. DST-weken | (1 bij run) |
| Q7 ORB + RSI(2) | mix verhoogt SR (0,91 → 1,03) maar verlaagt FTMO-uitkomst (€484 → €171–333/mnd): RSI(2)-dips raken de daggrens | 0 |
| U1 kostenpoort | 8 extra indices 1,4–6,5 bp → geen enkele ≤ 1,0 bp; U1-test vervalt | 0 |
| Q6 forward | cron actief (eerste dag vanavond 22:15 UTC), getest onder cron-Python | 0 |

**Stand:** ORB (US500/US100/US30/GER40) blijft de enige kandidaat met het juiste FTMO-profiel; bevestiging kan alleen nog via lange data (S3, A-01 bij Sandro).
Stopcriterium D-004 (vr 3 okt 12:00) nadert: S1 en S2 zijn niet positief.
**Open vragen:** U-002 (U2 sizing / U3 London-ORB) in VRAGEN_UITVOERDER.md. **Wacht op:** data/long_m1 → `./run_s3.sh` (preempt alles).
