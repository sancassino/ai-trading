# Bevindingen — Momentum-rotatie strategie (25 september 2026)

## Samenvatting

Na het testen van mean-reversion (uit het overdrachtsdocument) en vier varianten
van trend-following (SMA-cross, Donchian-breakout, wekelijkse regime-exit,
hysteresis-band) — die allemaal geen aantoonbare edge hadden na correcte
uitvoering — is een fundamenteel andere aanpak gevonden die wél consistent
positief is: **cross-sectionele momentum-rotatie**.

## Wat de strategie doet

Elke maand: rangschik alle instrumenten in het universum op trailing-return
over de laatste N maanden, koop de top-K (gelijk gewogen), verkoop de rest.
Universum (16 instrumenten): US500, US100, US30, EU50, UK100, GER40 (cash
indices), XAUUSD, USOIL, EURUSD, en de megacap-techaandelen AAPL, MSFT, AMZN,
GOOG, META, NVDA, TSLA.

Bestand: `MomentumRotation.mq5`. Broker-side stop via `CTrade`, retry-bestendig
tegen het "Market closed"-probleem (zie hieronder).

## Drie bugs gevonden en gefixt (allemaal bevestigd met echte MT5 Strategy Tester runs)

1. **Entry-blokkade** (`TrendFollow_CrossAsset.mq5`): na een stop-out mocht
   opnieuw instappen alleen na een verse SMA-kruising. Op goud bleef de EA
   hierdoor 9 jaar (2012-2021) aan de zijlijn tijdens een duidelijke hausse.
2. **Order-retry** (beide EA's): orders werden maar 1x per dag geprobeerd,
   exact om 00:00. Als de markt op dat moment "closed" registreerde in de
   Strategy Tester (sessie-grens-eigenaardigheid), werd nooit meer geretryd.
   Bij `TrendFollow_CrossAsset` bleef hierdoor een positie 9 jaar open en
   verloor uiteindelijk -$20.237 (20% van het account) i.p.v. de bedoelde 1%
   risico. Bij `MomentumRotation` bleef het HELE account 8 jaar lang $100.000
   doordat zelfs de eerste rebalans nooit lukte.
   Fix: retry op elke tick, niet 1x per bar/dag. Vereist tester-`Model=1`
   ("1-minuut OHLC", duizenden ticks/dag) i.p.v. `Model=2` (1 tick/dag).
3. **Handmatige stop-loss i.p.v. broker-side SL**: de trailing stop werd
   gecontroleerd met `if(bid<=slLevel) closepositie` — als die sluitorder
   faalde op het exacte "Market closed"-moment én de prijs herstelde
   daarna, werd de positie nooit gesloten. Fix: echte broker-side SL via
   `trade.PositionModify`, zodat de tradeserver zelf de uitvoering bewaakt.

## Data-kwaliteitsbeperking (geen bug, een echt kenmerk van FTMO's data)

Cash-index CFD's (US500.cash etc.) hebben dagelijkse koersen terug tot
2017-2019, maar **betrouwbare intraday tick-data (nodig voor realistische
order-uitvoering) pas vanaf ~2021**. Vóór 2021 faalt vrijwel elke order
structureel op "Market closed" — dit is een kenmerk van de brokerdata, niet
op te lossen met code. De eerlijke, bruikbare backtest-periode is dus
**2021-02 t/m 2026-09 (5,6 jaar)** — precies aan de ondergrens van de eis
van minimaal 5 jaar, niet de voorkeur van 8-10 jaar.

## Belangrijke methodologische stap: overfitting gevangen

Een eerste veelbelovend resultaat (TopN=1, 1-maand lookback, 60% exposure:
+77% over 5,6 jaar, **6/6 jaar positief**, $1.541/maand bij volledige
inzet) bleek **niet robuust**: lookback=2,3,4,6 maanden gaven allemaal
zwakke tot negatieve resultaten (3-4/6 jaar positief, $70 tot -$190/maand).
Dit was ruis in een kleine steekproef (~40-50 trades), geen echte edge —
verworpen conform de eigen regel uit het overdrachtsdocument (wantrouw
resultaten die niet standhouden bij een naburige parameter).

## Robuuste bevinding

TopN ∈ {2,3,4} × lookback ∈ {1,2,3} maanden: **alle 9 combinaties netto
positief** over de volledige 5,6-jaar steekproef, met hetzelfde patroon
(2022 het enige zwakke jaar — een reële brede bear-market, geen
strategie-fout), 4-5 van de 6 jaar positief in elke combinatie.

| Config | $/maand @ ~27-30% exposure | Jaren+ |
|---|---|---|
| TopN=2, lb=1mo | $480 | 5/6 |
| TopN=2, lb=2mo | $321 | 4/6 |
| TopN=2, lb=3mo | $695 | 4/6 |
| TopN=3, lb=1mo | $410 | 5/6 |
| TopN=3, lb=2mo | $261 | 4/6 |
| TopN=3, lb=3mo | $520 | 5/6 |
| TopN=4, lb=1mo | $318 | 5/6 |
| TopN=4, lb=2mo | $205 | 4/6 |
| TopN=4, lb=3mo | $232 | 4/6 |

Beste config (TopN=2, lookback=3mo) opgeschaald naar de FTMO-limiet:

- **33% exposure**: $765/maand, statische drawdown 9,8% (net binnen de
  10%-regel, weinig marge), worst single trade -4,3% van het eigen
  vermogen, 4/6 jaar positief.
- 45% exposure geeft $1.056/maand maar drawdown 13,5% — **breekt door
  FTMO's regel**, dus niet bruikbaar zonder verdere risicoreductie.

## Eerlijke conclusie op dit moment

Het beste, met échte MT5-data gevalideerde en robuustheids-geteste resultaat
haalt ~$765/maand bij een drawdown die net binnen de FTMO-limiet past — dat
is onder de eis van minimaal $1.000/maand, en de steekproef is met 5,6 jaar
aan de ondergrens i.p.v. de voorkeur van 8-10 jaar. Dit is wel het sterkste,
mins-overfit resultaat van de hele sessie tot nu toe. Onderzoek gaat door.

## Update: inverse-volatiliteit positiegrootte

Vervolgtest: i.p.v. gelijke weging per been, weeg elk been omgekeerd naar
zijn eigen ATR% (volatielere namen als TSLA/NVDA krijgen een kleinere
notional-slice). Resultaat bij TopN=2/lookback=3mo: verbetering naar 5/6
jaar positief (was 4/6) en drawdown omlaag van 9,8% naar 8,4% bij gelijke
exposure — meer risico-marge.

Maar: bij het testen van de buurt-parameters (lookback 2 en 4, TopN=3) op
dezelfde 36%-exposure varieert de drawdown enorm (7,7% tot 16,7%) — de
"veilige exposure" van één specifieke config generaliseert niet naar zijn
buren. Om écht robuust te zijn (veilig over de hele geteste buurt, niet
alleen de beste config) moet exposure omlaag naar zo'n 20-22%, wat het
verwachte rendement terugbrengt naar ongeveer **$400-500/maand** — nog
steeds onder het doel, maar met een eerlijker risico-marge.

## Grondige toetsing (n.a.v. momentum_grondige_toetsing.md, 25 sep 2026)

### 1. Drawdown-instabiliteit verklaard

Volledige drawdown-tabel (equal-weight, ~27-30% exposure, 16-instrumenten-universum):

| Config | Trailing-peak DD | Statische DD | Piek → dal |
|---|---|---|---|
| TopN=2, lb=1 | 20.0% | 11.2% | 2022.04 → 2023.01 |
| TopN=2, lb=2 | 14.2% | 14.2% | — → 2023.02 |
| TopN=2, lb=3 | 8.8% | 8.8% | — → 2022.11 |
| TopN=3, lb=1 | 15.8% | 9.7% | 2022.04 → 2023.01 |
| TopN=3, lb=2 | 14.5% | 13.9% | 2022.01 → 2023.04 |
| TopN=3, lb=3 | 10.5% | 9.0% | 2021.11 → 2023.07 |
| TopN=4, lb=1 | 15.4% | 12.2% | 2022.04 → 2023.03 |
| TopN=4, lb=2 | 16.6% | 15.8% | 2022.01 → 2023.04 |
| TopN=4, lb=3 | 10.8% | 10.5% | 2021.09 → 2023.07 |

**Antwoord**: in alle 9 combinaties loopt de max-drawdown-periode van eind 2021/begin
2022 tot medio 2023 — het is dus consequent dezelfde 2022-bear-market-episode,
geen geïsoleerde uitschietermaand of -instrument. De variatie in ernst (8,8%-20%)
komt doordat elke config toevallig een andere subset instrumenten vasthield
tijdens die 15 maanden, niet uit een systematisch verschil.

**Weging als oorzaak?** Getest met `MaxLegWeight`-cap (0,65) op de twee meest
onstabiele configs (TopN=2, lb=2 en lb=4): drawdown veranderde nauwelijks
(16,7%→16,8% en 7,7%→8,0%). **Geen wegingsartefact** — de instabiliteit zit in
de instrument-selectie tijdens één specifieke macro-episode, niet in de
gewichtsberekening.

### 2. Train/test blind-split

Training (2021-02 t/m 2024-08, puur op dit venster de beste config gekozen):
TopN=2, lookback=3-4mo wint met ~$790-836/maand (2/4 jaar positief in de
training-periode zelf, want die bevat de volle 2022-episode).

Geselecteerde config (TopN=2, lookback=3mo) **ongewijzigd** getest op de blinde
testperiode (2024-08 t/m 2026-09, ~2 jaar, nooit gezien tijdens selectie):
**+8,7%, 3/3 jaar positief, $433/maand, drawdown vanaf de vaste $100k-vloer:
0%.** Dit is een echte out-of-sample bevestiging — de config is niet zomaar
ruis die toevallig bij de volledige periode paste.

Kanttekening: de testperiode bevat toevallig geen nieuwe 2022-achtige
bear-market, dus dit bevestigt vooral dat de opwaartse edge generaliseert,
niet dat de neerwaartse veerkracht opnieuw is getoetst.

### 3. Concentratietoets

| Config | Top-1 maand | Top-2 | Top-3 | % van netto-winst (top-3) |
|---|---|---|---|---|
| TopN=2, lb=1 | 2021-12 | +2025-11 | +2025-09 | 59,5% |
| TopN=2, lb=3 | 2024-08 | +2023-10 | +2026-03 | 87,3% |
| TopN=3, lb=1 (16-instr) | 2023-06 | +2026-01 | +2021-12 | 65,7% |
| TopN=4, lb=3 | 2023-09 | +2024-09 | +2026-03 | 101,7% |
| TopN=2, lb=3, inv-vol | 2024-08 | +2026-03 | +2025-10 | 85,8% |

**Universeel patroon, bevestigd op elke geteste config**: 60-100%+ van de totale
nettowinst komt uit slechts 2-3 maanden van de ~55-68 geteste. Dit is hetzelfde
type concentratierisico als bij de XAUUSD-Aug21-trade destijds. Het relativeert
de "robuustheid" van het brede plateau fors: het teken (positief) en de
jaar-op-jaar vorm zijn robuust, maar de exacte omvang van de winst hangt sterk
af van een handvol uitzonderlijke maanden.

### 4. Bottom-K-symmetrietoets

| Config | Top-K resultaat | Bottom-K resultaat |
|---|---|---|
| TopN=2, lb=3 | +36,1%, $695/mnd, 4/6 jaar+ | +13,9%, $239/mnd, 4/6 jaar+ |
| TopN=3, lb=1 | +22,5%/27,5%, $358-410/mnd, 5/6 jaar+ | +1,3%, $19/mnd, 5/6 jaar+ |

Bottom-K (slechtste-momentum instrumenten kopen) presteert in beide gevallen
merkbaar zwakker dan top-K — gedeeltelijke steun voor een echt momentum-effect.
Maar bottom-K is niet duidelijk verlieslatend (blijft licht positief), wat
erop wijst dat een deel van top-K's edge gewoon de algemene, brede
marktstijging van dit instrumenten-universum over de testperiode is
("meesurfen"), niet 100% zuiver differentiërend momentum. Geen vals-positieve
uitslag zoals bij de mean-reversion-shorttest destijds (die verloor duidelijk
geld), maar ook geen schone bevestiging.

### 5. Regime-analyse 2022

Macro-context 2022: agressieve Fed-renteverhogingen (van ~0% naar ~4,5% in één
jaar, snelste cyclus in decennia) tegen de hoogste inflatie in 40 jaar, plus de
Rusland-Oekraïne-oorlog (energie-prijsschok vanaf feb 2022). Groei-/tech-aandelen
werden het hardst geraakt door de hogere discontovoet (NASDAQ -33% in 2022).

Terugkeerpatroon getest op 26 jaar Yahoo-data (S&P500/NASDAQ/Dow/Goud,
2000-2026 — richtinggevend, niet exact, zoals bij de eerdere 26-jaars
gold/GER30-validatie): hetzelfde momentum-systeem verliest ook duidelijk geld
tijdens de **dot-com-crash (2000-2002)** en de **kredietcrisis (2008)** — 2022
is dus geen uniek fenomeen maar een terugkerend patroon bij brede,
meerdere-maanden-durende bear-markets, die ruwweg eens per 8-12 jaar
voorkomen. Over de volle 26 jaar: **21/27 jaar (78%) positief, totaalrendement
851-1066% (~9-10%/jaar) afhankelijk van lookback** — consistent robuust over
lookback=1,3,6 maanden, en een veel geloofwaardiger langetermijnpatroon dan
alles wat bij goud/indices-trendvolgen werd gevonden.

Regimefilter (niet roteren als brede markt onder eigen lange-termijn-MA
staat) is nog NIET getest — risico op het herintroduceren van dezelfde
whipsaw-problemen als bij de eerdere trend-following-experimenten. Volgende
stap.

## Antwoorden op vervolgvragen (n.a.v. momentum_vervolgvragen2.md, 25 sep 2026)

### 1. Out-of-sample drawdown, juiste definitie

Peak-to-trough (vergelijkbaar met de andere tabellen): **4,7%** (piek
2026-03-02 → dal 2026-09-23). De eerder gemelde "0%" was de statische-vloer-
definitie (nooit onder het startkapitaal), niet de gebruikelijke drawdown —
terecht opgemerkt, dit gaf een te rooskleurig beeld. 4,7% is een eerlijk,
vergelijkbaar cijfer, en ruim binnen de FTMO-marge — al is de testperiode dan
ook rustiger dan de trainingsperiode.

### 2. Concentratie specifiek op de blinde testperiode

Nog geconcentreerder dan de volledige periode: **top-2 maanden (2026-03 GOOG,
2025-10 NVDA) = 121% van de netto OOS-winst.** Dit bevestigt het vermoeden:
de out-of-sample-test toont aan dat het **teken** klopt (positief, 3/3 jaar),
niet dat de **maandelijkse omvang** ($433/maand) betrouwbaar is — die hangt
sterk af van twee specifieke aandelen-trades.

### 3. Exposure-niveaus op elkaar afgestemd

Alle drie de cijfers ($695/mnd @ ~30%, $765/mnd @ 33%, $433/mnd OOS @ 30%)
zijn op vergelijkbare ~30-33% exposure berekend — geen exposure-inconsistentie.
Het verschil komt door een randeffect: de OOS-periode start 2024-08-01, maar
de beste maand uit de volledige periode ("2024.08", +$12.617) kwam van een
positie geopend rond 1 juli 2024 — vóór het OOS-venster begon. De blinde test
kon die specifieke trade dus per definitie niet meepakken, wat het lagere
cijfer grotendeels verklaart.

### 4. Monte Carlo op de echte tradereeks

Block-bootstrap (niet i.i.d. losse maanden — die zouden de 2022-regime-clustering
onderschatten) van de 52 echte maandelijkse rendementen uit `MR_t2_l3.csv`
(TopN=2, lookback=3mo, 30% exposure), FTMO-regels (fase1=10%, fase2=5%,
statische max DD=10%):

| Blokgrootte | Fase 1 slaagt | Funded | Live ≥$1k/mnd, 12mnd |
|---|---|---|---|
| 1 maand (i.i.d.) | 60,6% | 31,6% | 12,2% |
| 3 maanden | 64,5% | 34,9% | 13,5% |
| 6 maanden | 68,5% | 36,0% | 17,4% |
| 9 maanden | 71,3% | 37,9% | 19,1% |
| 12 maanden | 69,2% | 37,4% | 20,5% |
| 18 maanden | 74,4% | 49,0% | 20,2% |

Redelijk stabiele marge: **fase 1 ~61-74%, funded ~32-49%, live-inkomen
≥$1.000/mnd ~12-21%.** Dit is een duidelijke verbetering t.o.v. de oude
100%-goud-Monte-Carlo (fase1 48,5%, funded 30,3%, live-inkomen 0,99%) — vooral
de live-inkomen-kans is 12-20x hoger.

**Kanttekening, expliciet**: met slechts 52 echte maanden kan block-bootstrap
alleen dezelfde handvol goede/slechte maanden herschikken, geen echt nieuwe
scenario's genereren — de werkelijke onzekerheidsmarge is breder dan deze
30.000-simulatie-uitkomst suggereert. Dagelijkse 5%-verlieslimiet is NIET
gemodelleerd (alleen maandresolutie beschikbaar) — een slechte dag binnen een
verder oké maand zou in werkelijkheid alsnog kunnen breken.

### 5. Regimefilter, apart getoetst op train/test én 26-jaars Yahoo-episodes

Filter: niet roteren wanneer `US500.cash` onder zijn eigen N-maands
gemiddelde staat (eenmaal per maandelijkse rebalans gecheckt, dus geen
intraday-whipsaw zoals bij de oude trend-following-experimenten).

**Training (2021-2024.08)**: 10-maands SMA-filter verbetert het 2022-verlies
drastisch: van -$7.175 (ongefilterd) naar +$508 — vrijwel volledig gedempt.
$985/mnd i.p.v. $791/mnd, 3/4 i.p.v. 2/4 jaar positief.

**Blinde test (2024.08-2026.09), ongewijzigde config**: vrijwel identiek aan
zonder filter ($431 vs $433/mnd, 3/3 jaar, DD 5,3% vs 4,7%) — logisch, deze
periode bevat geen 2022-achtige crisis om te dempen. **Belangrijk positief
signaal**: het filter kost niets in rustige periodes, dus het is geen
overfit "trucje" dat alleen op de trainingsdata werkt.

**26-jaars Yahoo-proxy (richtinggevend, 2000-2026)**: gemengd resultaat.
2008 (kredietcrisis) volledig vermeden (nul trades dat jaar — het filter
hield de hele periode risk-off). 2002 grotendeels gedempt (-$11.397 →
-$1.028). Maar 2000 hielp niet (-$11.322, vrijwel ongewijzigd) en 2022 werd
maar deels gedempt (-$130.047 → -$87.750, ~33% minder). Totaalrendement over
de cyclus daalt van +1065% naar +838% (het filter mist ook goede maanden
terwijl het aan de kant staat).

**Eerlijke conclusie**: het regimefilter is **geen wondermiddel** maar een
reële, gedeeltelijke verbetering — het dempt sommige bear-regimes bijna
volledig (2008, grotendeels 2022 in de FTMO-periode), andere maar deels
(2022 in de lange Yahoo-reeks) of niet (2000), en kost enig totaalrendement
in ruil. Geen teken van whipsaw-overfitting (bevestigd op zowel training,
blinde test, als lange historie apart), dus wel bruikbaar als extra
risicobeperking — niet als garantie tegen elke bear-market.

## Volgende stappen (nog te doen)

- Grotere TopN/lookback-grid om een breder robuust plateau te vinden.
- FTMO-stijl Monte Carlo (fase1=10%, fase2=5%, max DD=10%, dagelijkse DD=5%)
  op de echte trade-reeks om slaagkans te schatten.
- Losse/aparte volatiliteits-gebaseerde positiegrootte i.p.v. vaste
  exposure-fractie, om de drawdown te verkleinen zonder het rendement
  evenredig te verlagen.
- Nagaan of de 2022-verliezen te dempen zijn met een simpel regime-filter
  (bijv. niet handelen als de brede markt onder zijn eigen langetermijn-MA
  staat) zonder de whipsaw-problemen van eerdere trend-experimenten te
  herintroduceren.
