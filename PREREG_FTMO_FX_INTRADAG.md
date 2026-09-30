# PREREG FTMO-FX-INTRADAG — London-Open Breakout (2026-09-30)

**Status: Pre-Registration for FTMO FX intraday trading. Ready for engine/ftmo.py + M5 data.**

## 1. Regel (Exact)

**FX-Intraday Breakout, London-Open (A5 voorstel):** 
- **Instrumenten:** EURUSD, GBPUSD, USDJPY
- **Sessie:** London-open venster (08:00–09:00 CET / 07:00–08:00 GMT)
- **Entry:** Long-breakout als koers > range 08:00–08:30 CET; Short als < range-low
- **Exit:** EOD (17:00 CET NYC-sluit) op dezelfde dag (intraday-vlak)
- **Posities:** Gelijk gewicht per pair (1/3 notional per 100-pip-risk)
- **Stop-loss:** −50 pip per positie (hard, geen uitzonderingen)

## 2. Mechanisme (Waarom het werkt)

**Europese sessie-microstructuur:** Londense openingsuren (08:00 CET) zijn vaak explosief: weergave van Aziatische overnight-bewegingen + eerste institutionele activiteit. Breakout-logica (Donchian-style): marktdeelnemers jagen groepen limiet-orders op weerstandsniveaus; eerste uurtje range-break kan intraday-momentum aanwakkeren.

**Waarom FTMO-geschikt:**
- **Swap-kosten = nul:** intraday-exit voorkomt nachts financing-kosten (~2,3 bp/nacht × 2 voor major-pairs)
- **Spread laag:** major FX-paren EURUSD/GBPUSD ≈ 0,6–0,8 bp; USDJPY ≈ 0,7 bp
- **Trend duurt uren, niet dagen:** lagere fill-risico's dan stijgende trend-regels
- **Vastgesteld einde:** EOD-exit voorkomt overnight-news-risico

## 3. Entry/Exit-Regels (Vooraf vastgesteld)

| Element | Specificatie |
|---------|-----------|
| **Periode** | 08:00–08:30 CET range vastgesteld |
| **Entry-signaal (Long)** | Slot > range_high_0800_0830; market-order op eerste tick > high |
| **Entry-signaal (Short)** | Slot < range_low_0800_0830; market-order op eerste tick < low |
| **Entry-timing** | Meteen na range-break (≤ 5 minuten; M5-bar bevestiging) |
| **Stop-Loss** | 50 pip vaste distance (niet trailing) |
| **Take-Profit** | Geen vaste TP; handmatige EOD-sluit of algoritme @ 17:00 CET |
| **Exit-tijd** | Strict 17:00 CET (vóór NYSE-sluiting, voorkomt overnight-gat) |
| **Geen herentry** | Na exit op dezelfde dag, geen extra posities |
| **Risk-sizing** | 1% per positie (totaal 3% notional voor 3 pairs) |

## 4. Dataset

| Item | Waarde |
|------|--------|
| **Lange basisreeks** | `data/daily/` — EURUSD, GBPUSD, USDJPY van FRED (1971–heden, noon-vastgesteld) |
| **Intradag-testdata** | `data/ftmo_m5/` — FTMO-M5-ticks EURUSD (2021–09-30 aanwezig); GBPUSD/USDJPY nog niet beschikbaar |
| **Ruwe ontdekking** | 2020–2024 EURUSD M5 (FTMO-data bestaande) |
| **Reserve-OOS** | 2025-01-01 tot heden (enkel na shortlist-selectie, éénmalig) |
| **Aanvulling nodig** | GBPUSD + USDJPY M5 van FTMO (R2-007 actie Uitvoerder-1) |

## 5. Kostenmodel (FTMO-CFD FX)

| Kostencomponent | Schatting | Toelichting |
|-----------------|-----------|-----------|
| **Bid-ask spread** | 0,6 bp (EURUSD), 0,7 bp (GBPUSD), 0,7 bp (USDJPY) | Major pairs, normale volume's |
| **Commissie FTMO** | ≈ 0,1–0,2 bp | Typisch FX-CFD |
| **Nacht-swap (niet van toepassing)** | 0 | Intraday-exit → geen overnight-financing |
| **Uur-commissie/spread** | ≈ 1–2 bp totaal per trade | 1 in + 1 uit |
| **Totaal per trade** | ≈ 2–4 bp | Afhankelijk van pair |
| **Poorteis** | Gemiddeld bruto ≥ 3 × 3 bp = 9 bp/trade | 50-pip-range ≈ 500 bp; poort gemakkelijk |

## 6. Beslisregel (FTMO-EV-variant)

Volg STRATEGIE_CATALOGUS v2 §3 + §9c (FTMO-EV metrics), specifiek:

**Metrics:**
1. **FTMO-EV via engine/ftmo.py:**
   - Win-ratio (%) en gemiddelde win/verlies (pip's)
   - P(fase 1: +10% vóór −10% op 21-daags venster) — realistische FTMO-simulator
   - P(fase 2 | fase1_pass)
   - Verwachte uitbetaling per maand (gefund.) → netto EV na €540 fee
   
2. **Statistiek:**
   - Winst per ingang cluster-t (Newey–West, τ=5)
   - SR_netto ≥ 0,4 (intraday-regels hebben laag SE)
   - ≥ 70% van maanden SR > 0 (minder variabiliteit dan meerdag-regels)
   - Beide helften (2020–22 en 2023–26) > 0

3. **Bevestigingscriteria:**
   - FTMO-EV ≥ €80/poging netto (boven fee)
   - Max intraday-dip ≤ −1,5% (intraday-klanten slapen niet over risico's)
   - Win-ratio ≥ 55% (niet afhankelijk van grote winnars)
   - Positieve scheefheid (veel kleine winsten beter dan enkele grote; intraday = hoger geluid)
   - Geen overlap met ORB/B4a (correlatie ≤ 0,3 in entries)

4. **Faalcriteria vooraf:** 
   - Break-even op M5-data is niet genoeg; minimaal intraday-ruis moet voorkomen

## 7. Verwachte Uitkomst & Falen

**Waarschijnlijk:** Londense breakouts hebben gemengde historische getuienis. Eenvoudige range-breaks falen in ranging-markten (2016–2017, veel van 2024). Verwacht: SR ≈ 0,2–0,4 bruto, swap-voordeel ≈ 2–3%/jr t.o.v. meerdag-variant.

**Succes:** FTMO-EV > €100/poging netto + ≥ 55% win-ratio + geen overlap met ORB (A1).

**Falen:** FTMO-EV < €30/poging, of win-ratio < 50%, of aantoonbare overlap met ORB-entries (veel dezelfde dagenmarktbewegingen).

## 8. Voorwaardelijke Varianten (Niet tellen als aparte trial)

1. **Time-variant:**
   - NY-open breakout (13:00–14:00 CET) i.p.v. London
   - Vergelijking alleen in uitvoer, geen aparte trial tenzij hypothese radicaal verandert

2. **Risk-sizing:**
   - Dynamisch sizing naar vol (risico-constante) — zou in engine zitten, geen voorafgaande wijziging

3. **Pair-selectie:**
   - Alleen EURUSD (data beschikbaar) eerste; GBPUSD/USDJPY daarna

## 9. Uitvoer (na engine/ftmo.py + M5-data)

- Win-ratio, gemiddeld win/verlies (pip's)
- Netto SR per maand (2020–26 totaal + beide helften)
- Scheefheid en max intraday-dip
- FTMO-fase-slagingskansen per periode
- FTMO-EV, fee, break-even
- Correlatie met ORB (S3, A1) — voorkom dubbel-tellen
- M5 vs D1 vergelijking (ruis, microstructuur)

---

**Bereid op:** 2026-09-30 21:35 CET  
**Auteur:** Strateeg  
**Volgende stap:** 
1. R2-007 (Uitvoerder-1): GBPUSD + USDJPY M5 van FTMO verzamelen
2. Engine/ftmo.py klaar → EURUSD-test run
3. Tweede run met drieluik zodra alle pairs beschikbaar
