# NEXT_STEPS / BACKLOG v2 — supervisor, 2026-09-30 00:10 Amsterdam

De uitvoerder deed B1–B5 in 20 minuten; de backlog was dus leeg vóór mijn uurlijkse refill. **Oplossing: backlog nu ≈ 6–8 uur werk + automatische reserve (zie einde).** Wacht nooit: is C(n) klaar → pak C(n+1). Push na elke taak. PREREG vóór elk resultaat; TRIAL_COUNT bijwerken; beslisregels hieronder zijn vast.

## Beoordeling B1–B5 (goed werk; opmerkingen)
- Uitstekend: DSR + TRIAL_COUNT (326) laten zien dat geen enkel eerder resultaat significant is. Vereiste Sharpe voor €880/mnd = 1,41 — dat is de lat.
- Dichtstbij: **RSI(2)** (t 3,65, DSR305 0,76, faalt alleen op DD 15,9% bij 100% notional; H2 zwakker) en **ORB** (N 9.249, t train 2,9 / test 1,1). Bij beide is de edge klein (ORB 1,7 bp/trade) → kosten/slippage-gevoelig. Niet tunen; wel sizing en combineren (C4).
- Wantrouw B5-EV (RSI2 €2.358/poging, SPY €3.058): sterk drift-gedreven (nul-drift-controle €24–1.066), slot-tot-slot (optimistisch), en het is een optie-/loterijconstructie. **FTMO-voorwaarden verbieden gokgedrag/niet-authentieke strategieën — risico op afkeuring.** Niet als strategie presenteren zonder Sandro's akkoord (zie C7).
- Gap: alle eerdere tests waren **directioneel** (beta). Markt-neutrale, hoge-breedte-edges zijn nauwelijks getest (B3 was neutraal maar op een dode factor).

## BACKLOG (volgorde = prioriteit)

**C1 — Stat-arb / pairs tussen bijna-identieke instrumenten (markt-neutraal, hoge breedte).** Paren: US500/US30, US500/US100, GER40/EU50, GER40/FRA40, UK100/EU50, XAUUSD/XAGUSD, UKOIL/USOIL, (+ ETF-proxy's voor lange data: SPY/DIA/QQQ, GLD/SLV, EWG/EWU). Regel (vast, literatuur): log-spread t.o.v. rollende regressiehedge 60 d, z-score; entry |z|>2, exit |z|<0,5, stop |z|>4, max 20 d. Data: FTMO D1 2017–2026 en Yahoo 2004–2026 voor ETF-paren. Kosten: FTMO-spread beide benen + swap beide benen (long én short). Beslisregel: per paar netto t ≥ 3 over gepoold ≥15 jaar (ETF) én positief in test 2021–26 (FTMO), N ≥ 300 trades, DSR(N=trials) ≥ 0,5. Verwacht: kosten/dunne edge; XAU/XAG en Brent/WTI de beste kandidaten.

**C2 — Lead-lag en tijd-van-de-dag op de bestaande M5-data (data/m5, N groot).** (a) US-sessie-rendement (vorige dag 15:30–22:00 CET) → GER40/UK100 eerste 60 min; (b) GER40 eerste 30 min → US500 open-uur; (c) uur-van-de-dag-profiel per symbool: alleen **vooraf vastgelegde** venster (bv. XAU 13:30–14:30 CET, US100 15:30–16:00) – geen scan van alle uren zonder N-correctie (TRIAL_COUNT +24×7 als je toch scant). Train 2021–23 / test 2024–26. Beslisregel: t ≥ 3 in train én test, N ≥ 1.000, expectancy na echte kosten > 0 in ≥ 4/6 jaren.

**C3 — Kortetermijn-omkeer (reversal) markt-neutraal op FTMO-aandelen (49–65 namen) en Yahoo-large-caps.** Wekelijks: long onderste 20%, short bovenste 20% op 5-daags rendement (dollar-neutraal, sector-ongecorrigeerd), houd 5 d. Let op: Yahoo-universum met huidige samenstelling heeft survivorship-bias → geef dat expliciet als bovengrens; FTMO-set 2021–26 is de eerlijke test (maar hindsight in 'welke aandelen'; gebruik `universe_wide.txt`, vooraf vastgelegd). Beslisregel: netto (spread+swap long én short) Sharpe ≥ 0,7, t ≥ 3, positief in beide helften, DSR ≥ 0,5.

**C4 — Sizing en combineren van bestaande sleeves.** (a) RSI(2) op SPX+NDX: zet notional zó dat max dag-equity-DD < 8% en dagverlies < 3%; rapporteer €/mnd op €80k en Sharpe (geen nieuwe parameters, alleen schaal). (b) Gelijk-risico-combinatie van sleeves die **individueel** t ≥ 2,5 haalden in B1–B4/C1–C3 (vooraf lijst vastleggen; geen selectie op P&L): gecombineerde Sharpe, correlatiematrix, DSR, €/mnd, FTMO-dagverlies-check op dagreeks. Verwacht: gecombineerde Sharpe 0,5–0,8 → €150–400/mnd; laat zien wat het **plafond** is en wat er nog aan Sharpe 1,41 ontbreekt.

**C5 — Crypto-trend/momentum (echt ander risicopremium, 24/7, hoge vol).** BTC/ETH (Yahoo 2014–2026; FTMO-crypto vanaf beschikbaarheid, check `symbol_history_FTMO.csv`). Vaste regels: 12-1 tijdreeksmomentum én 50/200-dagen-trend, vol-target 20%, kosten FTMO-crypto-spread + swap. Let op: enkele regimes (2017, 2021 bull) → hindsight-risico; rapporteer per jaar en excl. de twee beste jaren. Beslisregel: Sharpe ≥ 0,7 excl. beste 2 jaren, DD < 25% bij 20% vol, ≥ 5 jaar positief.

**C6 — Volatiliteits-timing van index-exposure (Moreira–Muir).** SPX/NDX/DAX: gewicht = target-vol / realized-vol(21 d), gecapt op 1,5×, vs buy&hold op gelijke vol. 1990–2026. Beslisregel: Sharpe-verbetering ≥ 0,15 t.o.v. b&h én max-DD < 15% bij 8% vol. Doel: een basiscomponent voor C4.

**C7 — (alleen ontwerp, geen loterij) MT5-realisme voor B5-EV.** Zet in `PREREG_C7.md` uit wat je zou testen (intraday-dip-equity, echte swap, ≥4 dagen, dagverlies op equity); voer NIET uit; lever een verwachtingswaarde-spreadsheet met controle nul-drift én een lijst FTMO-voorwaarde-risico's. Sandro beslist.

## Reserve (automatisch, als C1–C7 klaar): D1 FX-tijdreeksen op uur-van-dag met vaste vensters, D2 goud vs reële rente (^TNX-inflatiecomponent) lead-lag, D3 index-futures-basis/roll-effecten (niet handelbaar op CFD? — eerst kosten checken), D4 ETF-rotatie op vol-getargete risicopariteit als basis-sleeve. Loop je toch leeg: schrijf `VOORSTEL_*.md` met 3 nieuwe hypothesen + pre-registratie en ga door met de best onderbouwde.

## Portefeuille-beslisregel
Als na C1–C6 geen enkele sleeve/combinatie DSR ≥ 0,5 haalt → schrijf `PLAFOND_RAPPORT.md` (max haalbaar €/mnd onder FTMO-regels, met onzekerheidsmarge en eerlijke kans op €880+/mnd) en pauzeer; Sandro beslist over doel/aanpak.
