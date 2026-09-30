# PREREG FTMO-C17 — FOMC-Cyclus Day-Trading Rule (2026-09-30)

**Status: Pre-Registration for FTMO-EV evaluation. Ready for engine/ftmo.py implementation.**

## 1. Regel (Exact)

**FOMC-Cyclus D1-Trading:** Long US500/US100 CFD op dagen D-5 tot D-1 (vóór FOMC-vergaderingen). 
- Entry: Open dag D-5; Exit: Sluit dag D-1 (voormarkt of eerste uur NYC-open, 14:00–15:00 CET)
- Geen positie op FOMC-dag zelf (D0) of daarna
- Gewicht: gelijk (50% US500, 50% US100) of per vooraf vastgestelde balans na portfolio-simulatie
- Universum: US500 (SPX) en US100 (NDX) CFD's via FTMO

## 2. Mechanisme (Waarom het werkt)

**Fed-informatieeffect:** Centrale banken geven subliminale signalen in hun communicatie (renteverwachtingen, forward guidance). Beleggers herbeoordelen aandelen vóór officiële FOMC-vergaderingen op basis van anticipatie op informatie. Historisch (Cieslak–Morse–Vissing-Jorgensen 2019): overtollige avkastingen (Sharpe 0,3–0,6) in "even weken" (D-5 tot D-1) vóór FOMC-data.

**FTMO-aanpassingen:**
- D1 = slechts 1 nacht swap-blootstelling (tegen ~1,5 bp × aantal nachten)
- Intraday-sluitings zijn mogelijk (voorkomen swap op D0)
- Swap-kosten ≈ 5–8%/jr voor long index, maar gespreid over 5 nachten en kort venster (alleen tijdens de voorbereiding van FOMC)

## 3. Entry/Exit-regels (Vooraf vastgesteld)

| Element | Specificatie |
|---------|-----------|
| **FOMC-daten** | Bron: `fomc_dates_1994_2020.txt` (herverlengen tot 2026) + forward-kalender |
| **Entry** | Open van dag D-5 (09:30 ET / 14:30 CET) |
| **Exit** | Sluit dag D-1 vóór 15:00 CET (einde NYC-sessie) |
| **Stop-loss** | −2% intraday per positie (FTMO 5%-dagdips voorkomen) |
| **Positionering** | 0,25× geheelde notional per index (totaal 0,5× account) |
| **Clustering** | Alle FOMC-cycli gelijk behandeld; geen gevoeligheid voor voorafgaande marktomstandigheden |

## 4. Dataset

| Item | Waarde |
|------|--------|
| **Lange basisreeks** | `data/daily/` — SPX en NDX van Yahoo Finance (1970–heden, aangeboren adjust) |
| **FTMO-testserie** | `data/ftmo_daily_spx_ndx.csv` (M5 → D1 aggregatie, 2021–09-30) |
| **Ruwe ontdekking** | 2001–2024-12 (lange ETF/index-data via Yahoo) |
| **Reserve-OOS** | 2025-01-01 tot vandaag (enkel na shortlist-selectie, éénmalig) |
| **FOMC-kalender** | `fomc_dates_1994_2020.txt` + handmatig verlengd tot 2026-12 |

## 5. Kostenmodel (FTMO-CFD)

| Kostencomponent | Schatting | Toelichting |
|-----------------|-----------|-----------|
| **Bid-ask spread** | 0,8 bp intraday | Indices, normaal volume; US500/US100 liquide |
| **Commissie FTMO** | ≈ 0,2–0,3 bp | Typisch voor index-CFD's |
| **Nacht-swap long** | ≈ 1,5 bp/nacht | US500 ≈ 1,4%, US100 ≈ 1,6% per jaar ÷ 365 |
| **Swap-bijzonderheden** | 3× op vrijdag (rollover) | Drie nachten heffing voor weekend |
| **Totaal netto (5 nachten)** | ≈ 8 bp bruto kosten | Swap (1,5 × 5 = 7,5 bp) + spread/commissie (1 bp) |
| **Poorteis** | Bruto gemiddeld ≥ 3 × 8 bp = 24 bp/maand | Anders geen trial |

## 6. Beslisregel (FTMO-EV-variant)

Volg de STRATEGIE_CATALOGUS v2 §3 (PREREG-sjabloon), maar vervang SR-grift met:

**Metrics:**
1. **FTMO-EV (verwacht netto per poging)** per regel, via `engine/ftmo.py`:
   - P(fase 1: +10% vóór −10%) — Monte Carlo op realiseerde dagrendement
   - P(fase 2 | fase1_pass) — idem +5% vóór −5%
   - P(12m overleven | funded) — geen statisch verlies
   - E[uitbetaling | gefunded] — na winstsplit (aanname: 80%)
   - Fee-aanname: €540/poging (niet geverifieerd; Sandro vaststellen)

2. **Statistiek:**
   - Day-geclusterde t-waarde (Newey–West, τ=5)
   - SR_netto ≥ 0,3 over lange reeks
   - ≥ 60% van 5-jaars-vensters > 0
   - Beide helften (2001–12 en 2013–24) > 0

3. **Bevestigingscriteria:**
   - FTMO-EV ≥ €100/poging netto (boven fee en ruis)
   - Max intraday-dip ≤ −2% (FTMO 5%-dagdipgrens niet voorkomen)
   - Positieve scheefheid of laag-DD-profiel (negatieve scheefheid = hoger risico op dagruin)
   - Swap-aandeel in kosten ≤ 80% (anders is het carry, niet een edge)

4. **Korte verwalking:** Herproberen met andere FOMC-cyclus-regels (bv. D-6…D-2 i.p.v. D-5…D-1) **vóór** resultaat alleen als hypothese vooraf gewijzigd

## 7. Verwachte Uitkomst & Falen

**Waarschijnlijk:** Historisch t ≈ 2,85 op Yahoo ETF-data, maar FTMO-CFD-kosten zijn hoger dan eigen vermogen. Verwacht: FTMO-EV ~€50–150/poging (negatief na €540 fee).

**Succes:** FTMO-EV > €200/poging netto + statistisch bevredigend; geen overlap met andere FTMO-A-tier-regels.

**Falen:** FTMO-EV < €50/poging, of de t-waarde < 1,5 op cluster-niveau (ruis, geen effect).

## 8. Uitvoer (na engine/ftmo.py)

- Netto Sharpe per periode (2001–12, 2013–24, 2021–26 totaal)
- Scheefheid en max intraday-dip
- FTMO-fase-slagingskansen (tabel per periode)
- FTMO-EV, fee, break-even analyse
- Swap-aandeel als % van totale kosten
- Correlatie met andere A-tier-sleeves (ORB, FX-intradag)

---

**Bereid op:** 2026-09-30 21:30 CET  
**Auteur:** Strateeg  
**Volgende stap:** Engine/ftmo.py klaar → herbereken op CFD-kostenmodel
