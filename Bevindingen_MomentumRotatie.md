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

## Sessie 28 sep 2026 — regimefilter over plateau, dag-equity, FTMO-dagregel

### Infrastructuur
- Python `MetaTrader5` 5.0.6180 op de VM werkt gewoon via SSH (`mt5_account_info.py`):
  FTMO-Demo, login 1514742872, **€80.000 (EUR!)** — backtests rekenen met $100k USD.
- EA logt nu per dag balance/equity bij dagstart + min-equity (`*_daily.csv`), en heeft
  een optionele equity-guard (`DailyGuardPct`, `TotalGuardPct`). Baseline reproduceert
  de oude `MR_t2_l3.csv` op centen na.
- Tools: `analyze_daily.py` (DD op dag-equity, FTMO-dagverlies), `mc_daily_ftmo.py`
  (Monte Carlo met hele echte maanden, balance + equity per dag), `split_eval.py`
  (train/test op dag-equity), runners `run_sweep_regime_plateau.sh`, `run_expo_l1.sh`.
  Alle resultaten in `results/plateau/`. Periode 2021-01-01 t/m 2026-09-24.

### 1. Eerdere drawdowns waren te rooskleurig
Oude cijfers keken alleen naar gesloten deals. Op dag-equity (incl. zwevend verlies):
TopN=2/lb=3 @30%: statische DD **10,4%** (niet 9,8%), trailing 19,4% (niet 8,8%), en
FTMO-dagverlies tot **6,7%** (maart 2021). FTMO-regel: equity moet boven
*balance om 00:00 CE(S)T − 5% van startkapitaal* blijven — zwevend verlies van eerdere
dagen telt dus mee, en dat is precies het risico van een maand vasthouden.
$/maand over de volle 69 maanden = $512 (eerder $695, gedeeld door ~52 mnd).
Dag-MC (FTMO-regels op dagniveau): funded 21–29%, live ≥$1k/mnd **3–6%**.

### 2. Regimefilter (US500 > SMA10 maanden) over alle 9 configs, 30% exposure
Alle 9 blijven positief, rendement vrijwel gelijk, 2022 grotendeels gedempt,
statische DD omlaag in élke config (10,4–15,9% → 4,4–10,4%), trailing ~19% → 12–15%.
**Lost de dagverlies-overschrijdingen niet op** (5,3–10,0%): die zitten in risk-on maanden.

### 3. Equity-guard
- `TotalGuardPct=8` is een ontwerpfout: onder $92k flattent de EA bij elke rebalans
  opnieuw → permanent plat (5 configs eindigen op −$8k). Niet gebruiken.
- `DailyGuardPct=4` (flat tot volgende maand): dagverlies ≤4–5% overal. Bij lb=1
  (TopN 2/3/4) goed: stat. DD 2,3–4,3%, 5/6 jaar+. Bij lb=2/3 schadelijk
  (verlies realiseren en daarna opnieuw instappen in de verliezer).
- Exposure omhoog (lb=1): resultaten sterk padafhankelijk. Beste in-sample:
  TopN=2/lb=1/SMA10/guard 3%/60%: $1.340/mnd, 6/6 jaar, stat. DD 5,6%, dag 4,1%,
  top-3 maanden = 50% van netto; dag-MC funded 45–61%, live ≥$1k 21–22%.
  Maar guard 4% i.p.v. 3% geeft $925, en TopN=3 gaat juist omlaag ($821→$661).

### 4. Train/test (2021-01..2024-07 / 2024-08..2026-09) over 36 runs
- **Teken robuust: 36/36 positief in de testperiode.**
- **Parameterkeuze niet robuust: Spearman train↔test = −0,28.** De beste
  train-configs (60% + guard) halen in test gemiddeld ~$440/mnd; simpele 30%-configs
  zonder guard $550–820/mnd in test (maar breken de FTMO-dagregel).
- Conclusie: $1.340/mnd is een in-sample selectie, geen verwachting. Realistische
  verwachting bij FTMO-veilige instelling ligt rond $400–600/mnd.

### 5. Plateau-ensemble (alle 9 configs tegelijk, elk 1/9 exposure) — `ensemble_eval.py`
Met SMA10-filter @30%: ~$341/mnd, stat. DD 6,8%, dagverlies 5,0%, train $245 → test $503.
Verdubbelen van exposure: dagverlies 10%, stat. DD 13,6% → breekt FTMO.
**Robuuste edge van de 16-instrumenten-rotatie ≈ $350–500/mnd per $100k bij FTMO-veilig risico.**

### 6. Breed universum (65 FTMO-instrumenten, vooraf vastgelegde regel: alle niet-FX/
niet-crypto met D1-data ≤ 2020-12-31; `universe_wide.txt`, `symbol_history_FTMO.csv`)
- Valkuil gevonden: Strategy Tester kapt string-inputs af (~255 tekens) → eerste "brede"
  run gebruikte stilletjes 33 symbolen (gearchiveerd in `results/wide/invalid_truncated/`).
  Fix: `UniverseList="file:<naam>"` leest uit Common\Files.
- Valkuil 2: retry-op-elke-tick met 65 symbolen gaf een tester-log van 3,8 GB; een
  log-query daarop liet de VM (8 GB) out-of-memory gaan → VM gereset via gcloud.
  Fix: retry max 1x/minuut (run 2x sneller, log ~70 MB). EA schrijft nu ook `*_ranks.csv`.
- Ruwe momentum, TopN {3,5,8} × lb {1,3}: **5/6 netto negatief, 1–2/6 jaar positief,
  stat. DD tot 30%.** Top-3 wordt gedomineerd door MSTR/NVDA/PLTR/AMD/TSLA/GME; GME
  alleen −$14,7k.
- Vol-gecorrigeerd (rang op rendement/ATR%, inverse-vol weging; `RankByRiskAdj`):
  breed lb=1 +$250–400/mnd maar 3/6 jaar+ (alle winst 2024–26), lb=3 ~vlak;
  op het 16-universum juist slechter ($131 vs $436/mnd). Geen robuuste verbetering.

### Conclusie na deze sessie
1. De momentum-edge is **niet universum-robuust**: buiten de 16 met terugwerkende
   kracht gekozen instrumenten (incl. NVDA/META/TSLA, de grote winnaars van precies
   2021–2026) verdwijnt hij. Het 16-resultaat is waarschijnlijk deels
   hindsight-selectie van het universum.
2. Binnen het 16-universum is het teken robuust (36/36 test-runs positief), maar
   parameterkeuze niet (Spearman −0,28) en het FTMO-veilige niveau ligt rond
   $350–500/mnd — onder het doel van $1.000.
3. Veel varianten getest op dezelfde 5,7 jaar data → verder variëren op deze data is
   data-mining. Verder zoeken vereist een andere bron van edge of langere/onafhankelijke data.

## Gecorrigeerd naar het echte account: €80.000, EUR (29 sep 2026)

Alle kernconfigs opnieuw in de Strategy Tester gedraaid met Deposit=80000, Currency=EUR
(`run_eur.sh`, `results/eur/`) — niet simpelweg omgerekend, want een EUR-account met
USD-posities (US-aandelen, goud, olie) loopt ook EUR/USD-valutarisico. Analysetools
lezen nu `ACCOUNT_START` en `MONTHLY_TARGET` uit de omgeving. FTMO-limieten schalen mee:
max loss €8.000, dagverlies €4.000. Doel $1.000/mnd ≈ **€880/mnd** (EUR/USD 1,138 op
2026-09-23); ook getoetst tegen €1.000.

| Kernconclusie | Was ($100k USD) | Nu (€80k EUR) |
|---|---|---|
| Beste in-sample config (TopN=2, lb=1, SMA10, guard 3%, 60%) | $1.340/mnd, 6/6 jaar | **€1.069/mnd**, 6/6 jaar, stat. DD 5,6%, dag 4,1% |
| — idem train → test | $1.646 → $827 | **€1.321 → €648** |
| Plateau 9 configs SMA10 @30%, per config | $189–473/mnd | **€163–380/mnd** |
| Plateau-ensemble @30% | $341/mnd (train 245, test 503) | **€284/mnd** (train 204, test 417), stat. DD 6,4%, dag 5,2% |
| "Realistisch FTMO-veilig" | $350–500/mnd | **≈ €280–420/mnd** |
| Baseline TopN=2/lb=3 zonder filter | $512/mnd, stat. DD 10,4%, dag 6,7% | €434/mnd, stat. DD 10,1%, dag 6,9% |

Dag-Monte Carlo (FTMO-regels op dagniveau, hele echte maanden gebootstrapt, blok 1/6/12 mnd):

| Config | Fase 1 | Funded | Live ≥ €880/mnd (12 mnd) | idem netto na 80% split | Live ≥ €1.000 |
|---|---|---|---|---|---|
| Baseline t2/lb3 zonder filter | 34–53% | 19–28% | 3–6% | 2–4% | — |
| t3/lb1 SMA10 @30%, geen guard | 26–28% | 10–17% | 1–3% | 0–1% | — |
| Beste in-sample (t2/lb1/SMA10/guard3/60%) | 59–68% | 44–62% | 19–22% | 15–18% | 17–20% |

De beste-config-rij is in-sample geselecteerd (zie train/test hierboven: halvering in de
testperiode) en dus een bovengrens, geen verwachting. Kernconclusies blijven gelijk:
teken robuust, niveau ~€300–400/mnd bij FTMO-veilig risico, onder het doel van €880.

## 29 sep 2026 — swap-artefact, universums zonder hindsight, walk-forward (alles €80k EUR)

### Swap-artefact in de Strategy Tester
FTMO-swap = vaste punten per lot per dag (`swap_mode=1`); de tester past de huidige
puntwaarde op de hele historie toe, terwijl koersen split-gecorrigeerd zijn. NVDA stond
in FTMO-data op $13 (2021) vs $225 nu → tester rekent ~145%/jaar financiering i.p.v. ~8%.
Swap at 34–62% van de bruto winst op. `swap_correct.py` herrekent swap naar constante
%-van-notional tegen het huidige tarief (conservatief voor 2021–22, rente toen ~0%;
nooit goedkoper voor instrumenten die sindsdien daalden). Correctie: +€10–23k per run
op het 16-universum. **Alle cijfers hieronder zijn swap-gecorrigeerd.** Commissie en
spread (zitten al in de tester via historische M1-spreads) zijn verwaarloosbaar.

### Universums (9 configs TopN 2–4 × lb 1–3, SMA10, 30%)
| Universum | Ensemble €/mnd | Walk-forward ensemble (24/6/3) | Per config €/mnd |
|---|---|---|---|
| Origineel 16 (hindsight: NVDA/META/TSLA) | €470 (train 475 / test 463) | €592, 12/14 vensters+ | €327–630 |
| **Top-10 marktkap. 31-12-2020 + 9 idx/grondst./FX (geen hindsight)** | **€200** (train 129 / test 318) | €333, 10/14 vensters+ | €61–309 |
| Alleen indices/grondstoffen (17) | €130 | €159, 8/14 vensters+ | €−3–212 |

Top-10 per 31-12-2020 (vooraf bekend): AAPL, MSFT, AMZN, GOOG, META, TSLA, BABA, BRK.B,
V, JNJ (NVDA stond toen ~#13). Marktkapitalisaties uit eigen kennis, op rangniveau.

### Walk-forward
Gem. rangcorrelatie train↔test in alle universums −0,05 tot −0,18: config kiezen op
historie voorspelt niets. Ensemble presteert gelijk of beter dan "kies de beste".

### Conclusie
Zonder hindsight is de edge echt maar klein: **≈ €200–330/mnd bij 30% exposure op
€80k** (~40% van het 16-niveau). €880/mnd zou ~3–4× de exposure vergen → breekt
FTMO-limieten. Swap-correctie maakt het 16-universum beter, maar dat universum is niet
eerlijk te gebruiken als verwachting.

### Echt ensemble in de EA (29 sep 2026)
EA-optie `EnsembleTopNs`/`EnsembleLookbacks` (9 sub-portefeuilles TopN 2–4 × lb 1–3 in één
account, gewichten per symbool opgeteld, legs >25% naast doel worden herschaald).
Gewichten en herschaling handmatig gecontroleerd. SMA10, €80k EUR, swap-gecorrigeerd:

| Run | €/mnd | jaren+ | stat. DD | dagverlies | train → test €/mnd |
|---|---|---|---|---|---|
| T10 30%, geen guard | €186 (lineaire benadering €200 ✓) | 5/6 | 4,7% | 3,9% | 107 → 318 |
| T10 60%, geen guard | €375 | 5/6 | 9,2% | **8,1% (breekt)** | 187 → 688 |
| T10 60%, guard 3% | €38 | 2/6 | 14,0% | 4,0% | 24 → 61 |
| T10 90%, guard 3% | €42 | 3/6 | 17,2% | 5,4% | −132 → 332 |
| 16 30%, geen guard | €450 | 5/6 | 3,5% | 4,8% | 442 → 462 |
| 16 60%, guard 3% | €637 | 5/6 | 8,1% | 4,7% | 773 → 409 |

De dagguard vernietigt het hindsight-vrije ensemble (verlies realiseren, herstel missen).
**Binnen deze strategiefamilie is er zonder hindsight geen FTMO-conforme route naar €880/mnd;
het haalbare niveau is ~€190–320/mnd op €80k.**

## NEXT_STEPS-toetsen (29 sep 2026) — zie `VERSLAG_NEXT_STEPS_2026-09-29.md`
Lange validatie 2000–2026 (ETF's en point-in-time top-10): ensemble +0,04 resp. +0,25%/jr na 8%
financiering, 48% resp. 33% jaren positief → faalt. Python↔MT5 klopt op ensemble-niveau (corr 0,951),
niet per config. Willekeurige universums: gem. €83/mnd, spreiding −€77…€333. **Edge niet aangetoond.**
