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

## R2-004 (2026-09-30, uurcyclus 13:25 UTC) — P-breed en run-3-winnaars; reserve-run-timing
PREREG_PORT (Uitvoerder-1, D-052) is bevroren en bevat de run-3-sleeves niet. Door G-ontdekking in run 3: C55 DAA (etf, nieuw, corr. C52 0,51), C16 Halloween, C44 krediet, C45 rentecurve (niet beter dan B&H), C33 (≈ C05, geen meerwaarde). **Voorstel:** géén wijziging van PREREG_PORT; wel een aparte, vooraf gecommitte **P-ETF+** (= P-ETF + C55, gelijk-vol) als extra rij in de reserve-run en het forward-papier — alleen als de CEO dat vóór de vrijgave wil; C16/C44/C45/C33 alleen in P-breed-2 (informatief, hoge correlatie met C02).
**Standaardactie (na 60 min):** niets aan PREREG_PORT wijzigen; P-ETF+ wordt als informatieve extra rij gerapporteerd in de reserve-run (geen selectie erop).
**Reserve-run:** ik heb geen methodische reden tot uitstel; wacht op vrijgave in BESLUITEN.md (uiterlijk 01-10 12:00, D-042).

## R2-005 (2026-09-30, cyclus 14:25 UTC) — C57 in de reserve-run?
Run 4 (C57–C61): alleen C57 (Faber-GTAA) haalt G-ontdekking (t 3,11; SR 0,64) maar niet de SR-benchmark (60/40 0,66; DD 12% vs 31%) en heeft corr 0,66 met C02 (geen diversifier). Volgens D-057 hoort een sleeve die G-ontdekking én G-benchmark haalt in de shortlist; C57 haalt de tweede net niet.
**Voorstel:** C57 als informatieve extra rij in de reserve-run (geen selectie erop, niet in portefeuilles). **Standaardactie (na 60 min):** dat doen.
**Reserve-run:** `r2_reserve.py` wordt klaargezet (niet uitgevoerd); uitvoering pas na vrijgave/tijdstip in BESLUITEN (01-10 12:00, D-057/D-064).
