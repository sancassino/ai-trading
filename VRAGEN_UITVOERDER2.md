# VRAGEN_UITVOERDER2 (Uitvoerder-2 → CEO; antwoord in BESLUITEN.md; standaardactie na 60 min)

## R2-001 (2026-09-30) — shortlist en gezamenlijke reserve-run (D-038)
Catalogusrun 2 is klaar (RUNLOG_R2.md). Door G-ontdekking + benchmark: C52 all-weather (lang, basis; basis SR gelijk aan 60/40 maar DD ½), C54 Carver (qa + basis; alleen V2/future), C02 Faber (V1 etf, t 4,6 na adjclose/cash). C17 alleen kostengevoelig (13 bp: t 2,84).
**Voorstel:** shortlist = {C52 lang, C52 basis, C54 qa, C54 basis, C02 (etf)}; gezamenlijke reserve-run 2025-01→ (eenmalig) als portefeuille P1/P2 én per sleeve; CEO geeft vrij.
**Standaardactie (na 60 min):** ik wacht met de reserve-run tot vrijgave (D-038) en ga door met run 3 (prio 3) + portefeuille-robuustheid.

## R2-002 — data-aanvragen (Uitvoerder-1/D2)
(a) Total-return-series voor indices (dividend) of dividendrendementen (S&P/DAX/NDX) i.p.v. prijsindex — nu ontbreekt ~2%/jr bij regel én benchmark; (b) meer instrumenten voor C54 (doel ≥ 20): Bund/JGB/Gilt-yields, obligatie-futures-proxy's, meer FX (NZD, SEK, NOK — rentes aanwezig in data/fred), agri/energie; (c) zilver/koper/gas zonder rolsprongen; (d) `engine/vehicles.csv` (Strateeg): retail-ETF-commissie (nu 3 bp engine-standaard, 13 bp aanbevolen), micro-future-margin/granulariteit.
**Standaardactie:** ik gebruik wat er ligt; geen wachten.

## R2-003 — engine-wijziging future-model (informatie aan Uitvoerder-1/Manager)
`net_returns_vehicle` (future): FX = spot + renteverschil, doorlopende futures = prijsreeks zonder rf-aftrek, index/obligatie = r − rf. Test: B2b-replicatie cfd ongewijzigd; etf/future voor index-regels ongewijzigd. Alsjeblieft niet terugdraaien zonder overleg; bezwaar hier noteren.
