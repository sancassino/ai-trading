# PREREG FTMO-C17 — FOMC-cyclus op index-CFD (FTMO-EV) — 2026-09-30

**Status:** Pre-registratie FASE 3 (D-085/D-087). Structuur compleet. **Nog geen resultaat.** Uitvoerder-2/CTO draait pas na freeze van OPEN-punt §1a.  
**Tier:** A4 (STRATEGIE_CATALOGUS §9).  
**Trial:** +1 als de kostenpoort haalt; append-only in `catalogus/TRIALS.csv`; BH over hele catalogus. Reserve 2025-01→ **onaangeraakt** tot CEO shortlist vrijgeeft.

## 1. Regel (exact — bevroren zodra OPEN §1a gesloten is)

### 1a. OPEN — regeldefinitie (blokkeert run)
Er liggen **twee** incompatible definities in de repo. Kies er één vóór enige berekening:

| Variant | Bron | Definitie |
|---------|------|-----------|
| **V-CAT1 (voorkeur tot CEO anders besluit)** | `PREREG_CAT1.md` C17 | FOMC-dag = dag 0; **long** indices op handelsdagen −1…+4, +9…+14, +19…+24, +29…+34 (even weken 0/2/4/6 in FOMC-tijd, SPX-handelsdagen sinds dag 0); anders flat. Dit is de regel met gerapporteerde t ≈ 2,85 op ETF-vehikel. |
| **V-PRE** | eerdere FTMO-PREREG-draft | Long D−5…D−1 vóór FOMC; flat op D0 en daarna. |

**Besluit tot CEO/Manager anders schrijft:** run op **V-CAT1**. V-PRE alleen als aparte PREREG (+1 trial) als iemand die expliciet wil — niet stilzwijgend verwisselen. Catalogusregel A4-tekst "5 van 6 weken vóór FOMC" is **niet** V-CAT1; §9 wordt bijgewerkt naar V-CAT1-formulering.

### 1b. Bevroren parameters (V-CAT1)
- **Instrumenten:** US500cash, US100cash (FTMO-index-CFD). Gelijk gewicht 50/50 (geen post-hoc portfolio-optimalisatie).
- **Gewicht per sleeve:** notional-doel zodanig dat **gecombineerd** dagverlies-risico bij −2% move ≈ 1% account (hard cap: never > 2% account-risico per dag op floating). Exacte lots = `engine/ftmo.py` sizing-helper; geen handmatige override na resultaat.
- **Entry/exit:** op D1-slot van de dag waarop de regel long zegt; flat op dagen waarop de regel geen long zegt. Geen intraday-timing in de primaire trial (intraday-vlak = aparte exploratieve C3, geen trial zonder eigen PREREG).
- **FOMC-kalender:** `fomc_dates_1994_2020.txt` + `events.csv` (2021→); geen handmatige uitzonderingen.
- **Stop:** geen trade-stop in primaire regel (D1-positie); FTMO-dagverlies wordt via sizing + `engine/ftmo.py` bewaakt, niet via een post-hoc stopregel.

## 2. Mechanisme
Cieslak–Morse–Vissing-Jørgensen (2019): excess returns geconcentreerd in even weken van de FOMC-cyclus (Fed-informatie-/risicopremie-kanaal). **Web/literatuur = claim; bewijs alleen via eigen data + FTMO-kosten.**

## 3. Dataset / vensters
| Item | Waarde |
|------|--------|
| Ontdekking | ≤ 2024-12-31 (D2-dagdata SPX/NDX als proxy; FTMO D1 waar beschikbaar 2021–24) |
| FTMO-check | FTMO D1/M5→D1 2021–2024 (zelfde regel, cfd-kosten) |
| Reserve-OOS | 2025-01-01→ **gesloten** tot CEO FTMO-shortlist vrijgeeft (D-084) |
| Bron FOMC | `fomc_dates_1994_2020.txt`, `events.csv` |

## 4. Kostenmodel (vehikel `cfd`, gemeten S0 waar beschikbaar)
Bron: `COSTS_FTMO.csv` (S0, 2026-09-30):

| Symbool | Rondreis intraday (bp) | Swap long (bp/nacht) | Swap short (bp/nacht) |
|---------|------------------------|----------------------|------------------------|
| US500cash | 0,78 | 1,36 | 0,81 |
| US100cash | 0,66 | 1,95 | 0,21 |

- D1-hold ≈ 1 kalendernacht swap (vrijdag → 3× weekend-rollover volgens FTMO-conventie; modelleer expliciet).
- Gevoeligheid: +50% spread én +50% \|swap\| (aparte rijen in uitvoer, geen extra trial).
- **Kostenpoort (geen trial als fail):** gemiddelde bruto ≥ 3× (spread-rondreis-equivalent + swap over hold). Exacte poortberekening in engine; faalt → stop, geen TRIALS-rij met "pass".

## 5. Beslisregel (FTMO-EV, vooraf)
1. Kostenpoort (§4) → anders STOP.
2. Statistiek ontdekking: dag-geclusterde t (NW lag 5 en/of blok-bootstrap 21d) — rapporteer beide; **poort:** min(t) ≥ 2,0 **én** beide helften (≤2012 / 2013–2024) excess > 0 na kosten **én** ≥ 60% niet-overlappende 5-jaarsvensters > 0.
3. FTMO-EV via `engine/ftmo.py` (aanname fee €540/€80k, split 80% — label "onder aanname fee"):  
   `P(fase1)`, `P(fase2|fase1)`, `P(survive_12m|funded)`, `E[uitbetaling/mnd]`, `FTMO_EV_netto`.  
   **Kandidaat-drempel (informatief tot S10-FTMO bindend is):** FTMO_EV_netto ≥ €100/poging **én** schaal zodanig dat p95 dagverlies ≤ 2% account (schaal > 4% alleen als bovengrens, D-016/D-085).
4. BH q ≤ 0,10 over catalogus-TRIALS (incl. eerdere 400+ trials).
5. Correlatie met A1 (ORB) en A5 (FX-intradag) rapporteren; geen selectie op correlatie.

## 6. Verwachting (geen resultaat — alleen prior)
ETF-vehikel gaf t ≈ 2,85 (CAT1); cfd-swap long 1,4–2,0 bp/nacht sleept. Prior: FTMO-EV vaak **onder** fee na realistische sizing; nuttig als lage-omloop sleeve alleen als EV ≥ drempel én lage correlatie met ORB.

## 7. Uitvoer (verplicht)
Netto SR/scheefheid/maxDD; jaar-per-jaar; swap-aandeel % kosten; FTMO-fase-kansen; EV-tabel; +50%-kostenrij; correlatie A1/A5; expliciete regel-SHA van dit bestand in RUNLOG vóór run.

---
**Bijgewerkt:** 2026-09-30 21:41 CEST — D-090 re-kickoff (Grok Strateeg): gaps gevuld (regel-OPEN, gemeten kosten, trial/BH, sizing-freeze).  
**Auteur:** Strateeg (`claude/trusting-faraday-34tsmg`)  
**Volgende:** Manager/CEO bevestigt V-CAT1; Uitvoerder-2 valideert `engine/ftmo.py`; daarna één run.
