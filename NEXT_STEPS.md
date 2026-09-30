# NEXT_STEPS v21 — Manager, 2026-09-30 14:15 Amsterdam — verwerkt D-042…D-046, RUNLOG_R2 (catalogusrun 2), engine-vehikelstandaarden

Bindend: `CEO_MANDAAT.md`, `PROGRAMMA_FASE2.md`, D-025…D-046 (CEO-branch). Alleen Sandro beslist over stoppen/bevriezen. Doel v2: eigen kapitaal €80k, ambitie €800–900/mnd, €400–500/mnd ook succes.

## 0. Coördinatie (Manager-QA op wat er ligt)
- **Uitvoerder-2 werkt op branch `claude/uitvoerder2-r`, niet op main** (RUNLOG_R2, results/R2, TRIAL_COUNT 427). Beide Uitvoerders: `git fetch --all`, elkaar lezen; Uitvoerder-2 merged `origin/main` minstens elk uur in zijn branch; Uitvoerder-1 merged `claude/uitvoerder2-r` in main na elke afgeronde run (fast conflict-vrij: eigen bestanden). **TRIALS.csv/TRIAL_COUNT.md:** main zegt 421, U-2-branch 427 → bij merge = aantal geldige rijen; "ongeldig, telt niet"-rijen blijven buiten BH (D-045).
- **Manager-QA-bevindingen catalogusrun 2 (rapportage, geen blokkade):**
  1. **G-benchmark inconsistent toegepast:** C52 *basis* haalt SR 0,65 vs 60/40 0,66 (niet beter) maar staat 'door G-ontdekking'. Volgens D-038 (SR én maxDD beter) is dat een **fail op SR**; label 'door met voorbehoud: DD-voordeel, geen SR-voordeel' of CEO beslist. Rapporteer beslissing expliciet in TRIALS.csv.
  2. **C54 qa is post-hoc gekozen na zien van basis** (beide tellen als trial ✔). Behandel C54 basis niet als bewijs (artefacten: WTI<0, FX-pegs); alleen qa telt, en dan nog met winnaarsvloek-korting.
  3. **Winnaarsvloek P1:** sleeves gekozen na zien van ontdekkingsdata; SR 0,84 is een bovengrens. Rapporteer ook **P-ETF** (zonder futures/hefboom; Strateeg H5: micro-futures onuitvoerbaar bij €80k voor indices/goud) als eerlijke ondergrens en **P-ETF met 13 bp rondreis**.
  4. **Hefboom ≤ 3× tegen rf + 1,5% (D-042)** i.p.v. gratis rf; kosten per vehikel; herrekenen vóór iets over CAGR wordt gezegd.
  5. **Reserve-OOS-power:** 1,75 jr → SR-standaardfout ≈ 0,75; een 'pass' is nauwelijks informatief. Rapporteer puntschatting + CI (D-042), en zeg vooraf dat forward-paper (F) het echte bewijs levert.
  6. **Kapitaal-check doel:** met 2020s-SR ≈ 0,5 ≈ 5% CAGR bij 10% vol = ≈ €330/mnd bruto vóór belasting → onder de €400-drempel; nooit 'ontdekking-CAGR' als verwachting labelen.

## 0b. Direct (Uitvoerder-2, uiterlijk 01-10 12:00, D-042)
1. **Portefeuilleregel vooraf committen** (PREREG_PORT.md): sleeves elk 10% vol, gelijk gewogen, geen optimalisatie, hefboom ≤ 3× tegen rf + 1,5%, kosten per vehikel; commit (SHA in RUNLOG) vóór enige reserve-run.
2. **Run 3 (PREREG vóór resultaat):** C04, C13, C16, C29, C33, C43–C45, C24 + catalogus v1.1-nieuwkomers (trend/vol-managed/dual-momentum).
3. **Regime-stress (D-043):** alles op 1970–2000 (stijgende rente; TNX_10Y vanaf 1962), 2022 en de jaren 70 apart; rolling-SR + DD-duur; wat drijft 2022?
4. **H5 (D-043/Strateeg):** contracten per instrument bij 10% vol, afrondingsfout, marge, geen contract > 25% kapitaal; anders C54 alleen als 'grove legs via ETF/CFD' herformuleren.
5. Winnaarsvloek-log: per sleeve wanneer/waarom in shortlist.

## 0c. Direct (Uitvoerder-1)
1. **D2-uitbreiding (D-044, ≤ 3 u):** (a) TR/dividend (S&P, DAX, NDX) binnen bronvoorwaarden; (b) ≥ 20 instrumenten voor C54 (NZD/SEK/NOK-FX, Bund/JGB/Gilt-proxy's, agri/energie); (c) roll-schone zilver/koper/gas; (d) **FRED vanaf Debian ophalen en committen** (rentes, goud/CPI, FX); rate-limit, eerlijke UA, niets omzeilen.
2. **Engine (D-045):** future-model-fix (FX = spot + renteverschil; doorlopende futures zonder rf-aftrek) blijft; opnemen in engine/README + ENGINE_TEMPLATE (Manager werkt ENGINE_TEMPLATE bij: zie §V).
3. S3/P0 en F (forward) volgens bestaande punten hieronder.

## R — Catalogus (werkstroom R; volgorde D-032; ontdekking ≤ 2024-12-31, reserve-OOS 2025→ onaangeraakt)
1. **C02-QA (Uitvoerder-2; CFD-benchmark al ✔: SR 0,32 vs 0,18, maxDD 54% vs 88%). Nog te doen per vehikel etf/future (geen reserve-OOS):** (a) vergelijk met **buy-and-hold** (SR, maxDD, DD-duur, CAGR) op dezelfde 5 indices; (b) **total return** (adjclose) i.p.v. price-index en **rente op cash** (IRX) in de vlakke maanden; (c) signaal bij maand-slot, uitvoering volgende handelsdag (geen lookahead), **switch-kosten** per vehikel; (d) effectieve N: 5 indices zijn sterk gecorreleerd → dag-/maandgeclusterde bootstrap over de gepoolde reeks, en 1 index tegelijk (SPX 1927–2024, N225, DAX) als robuustheidscheck; (e) subperiodes (decennia) en 'verloren decennia'; (f) publicatie 2007: rapporteer 2008→2024 apart als quasi-out-of-sample.
2. **Engine `vehicle`-parameter (D-033):** `etf` (TER 0,07–0,12%, geen swap, long-only, deelbaar, adjclose), `future` (micro; roll/financiering in prijs; granulariteit), `cfd` (S0-kosten + financiering benchmark ± 1,5%). Standaardwaarden staan erin; Strateeg levert `engine/vehicles.csv` + retail-broker-kostencheck (D-041) → engine vervangt de standaarden, vermeld in RUNLOG.
3. **Catalogusrun 2 (Uitvoerder-2, één PREREG vóór resultaten; Strateeg levert klassen in catalogus v1.1):** vol-managed aandelenindex, risk-parity/all-weather, dual momentum (Antonacci), Carver-forecast-combinatie over ≥ 20 instrumenten, defensive asset allocation; daarna eerder prio-2/3-regels. Regels die al in de 414+7 trials zitten niet opnieuw testen.
4. Kandidaat-criteria (D-030 §5): netto SR ≥ 0,4 op ontdekking, positief in ≥ 2/3 decennia/regimes, kosten+swap, BH-significant (q = 0,10), lage correlatie met bestaande sleeves; **+ benchmark-vergelijking (D-032)**.

## D — Data
- P0 Dukascopy: voortgang in RUNLOG/`data/DATA_CATALOGUS.md`. D2: 61 reeksen in de repo ✔ (FRED onbereikbaar vanaf cloud-IP, niet omzeilen). Nog: NDX/andere total-return, bond-/credit-/sector-proxy's is gedaan; mis: DGS10/T10Y2Y-vervangers (alleen vrije bron met licentie), uitbreiden (obligatie-/rente-/credit-proxy's, sectoren, meer FX, grondstoffen, total-return-varianten waar vrij beschikbaar) met licentie-vermelding (D-030 §6). S3 blijft laagste prioriteit binnen R maar preempt zodra SPX 2012–2020 compleet is.
## V — Vehikel-analyse (Strateeg eigenaar; Manager QA)
- `VEHICLE_ANALYSE.md` v1 gelezen: goede structuur, bronnen gemarkeerd. **Manager-QA:** (1) 'ᵉ eigen kennis' cijfers (spreads, micro-contractkosten, valutakosten) moeten door brokerdocumentatie geverifieerd of expliciet als aanname in het kostenmodel; (2) box-3-berekening blijft 'niet geverifieerd, geen advies' (wetgeving/ingangsdatum onzeker) — niet in het bruto-doel verwerken; (3) UCITS-historie < 2012: proxy-reeks + TER, niet 'echte ETF-data'. **S10b** (Strateeg, ≤ 2 cycli): DD-budget, min. bewijs (≥ 20 jr, BH, reserve-OOS), vehikelkosten, forward-papier ≥ 3 mnd, Auditor.
## F — Forward/MT5
- Forward-paper (F3b) dagelijks; eerste dag 30-09 22:15 UTC → `forward/paper_daily.csv` moet er 1-10 zijn; meld gaten. Laagste prioriteit binnen het programma (Doel v2 heeft eigen-kapitaal-forward nodig, zie S10b).
