# VOORSTEL_PRESCREEN_N20 — US30 PM Continuation (Post-Lunch AM-Trend Follow)

**Status:** **geen PREREG — U2 D-092.1 FAIL** (U2 `a1756a7` op `claude/uitvoerder2-r`; train 2021–2023: N=384, mean **−2,26** < gate **1,35** bp). Geen herstart zonder CEO. Vervangen door N24+ (D-094).  
**Auteur:** Strateeg (Grok).  
**Instrument:** `US30cash` (RT 0,45 bp COSTS_FTMO / screen → drempel **1,35 bp** = 3× RT).  
**Track:** index PM-continuation (heropen onder D-094; ≠ dead ORB-familie).  
**Grond:** Na de NY lunch lull (11:30–12:30 ET) hervatten institutionele traders hun AM-trend in de mid-sessie. De richting van de ochtendsessie (09:30–12:00 ET) is de voorspeller: een sterke AM-move die niet volledig reversed is voor 12:00 ET, zet door in de PM-sessie. Non-ORB, non-fade, onderscheidend van LUNCH_OPEN (fade) en N3 (close momentum). Gemiddeld ~120–160 signalen/jaar → N>150 over 3jr verwacht.

**D-094a (geschiedenis <5y):** train-screen 2021–2023 = 3y. Schriftelijke reden **(b)**: AM→PM continuation na lunch-lull is een tijdloos microstructure/inventory-mechanisme; langere proxy (DJI / YM futures D1+intraday elders) bevestigt sessie-handoff-patronen; FTMO-M5 toetst alleen kosten/uitvoering. Moet in toekomstige PREREG herhaald worden.

---

## Idee (mechanisme)

Na de NY noon-lull (12:00–12:30 ET) herstarten institutionele market-makers hun directionale flow. Als de AM-sessie een duidelijke richting had (09:30–12:00 ET), zijn long/short momentum-fondsen nog steeds positioneerd in die richting en addensen hun posities in de eerste 30 min na hervatting. De PM-sessie (12:30–15:00 ET) heeft een hogere hit-rate voor AM-trend-continuation dan reversal op sterke AM-trend-dagen.

**Onderscheid van dode sleeves:**
- ≠ LUNCH_OPEN (fade van 09:30–11:00 ET impulse terug naar open; dit = continuation van AM-trend in PM, TEGENGESTELD mechanisme)
- ≠ N3 US100 close-drive (14:30–15:55 ET entry; dit = 18:00 CET entry, eerder in PM)
- ≠ N14 US100 NY-Open PM (pre-market → NY-open signal; dit = AM-sessie-return als signal)
- ≠ MIDDAY_VWAP (dead; VWAP-gebaseerd; dit = session-open anchor)
- ≠ simple ORB-familie (A1/N11/N15–N17) — geen opening-range break

---

## Regel (bevriesbaar zodra screen PASS)

**AM-trend signal:**  
- `P_open` = M5-close van de 15:30 CET bar (NY session open)  
- `P_1800` = M5-close van de 18:00 CET bar (12:00 ET, na lunchpauze)  
- `am_bp = 1e4 × (P_1800 − P_open) / P_open`

**Signalen (max 1 trade/dag):**  
- `am_bp ≥ +0,30%` (+30 bp) → **LONG** op 18:00 CET close (AM-trend continue in PM)  
- `am_bp ≤ −0,30%` (−30 bp) → **SHORT** op 18:00 CET close  
- Anders → geen trade  

**Stop:** 1,0 × ATR14 (dag) vanaf instapprijs.  
**Exit:** hard flat 21:00 CET (15:00 ET / 3 uur na entry). Swap = 0 (intradag).

---

## Pre-screen aanvraag (Uitvoerder-2)

- **Data:** `data/m5gz/US30cash.csv.gz`, train 2021-01-01 … 2023-12-31.
- **Regel:** identiek hierboven (am_bp 15:30–18:00 CET ≥ ±30 bp, continuation-entry 18:00 CET, stop ATR14, flat 21:00 CET).
- **Maatstaf:** mean bruto retour in bp + median + N (signed mean).
- **Gate:** mean bruto ≥ **1,35 bp** (3 × 0,45 bp RT). N≥150 vereist.
- **Geen test/reserve aanraken.** Alleen train-screen.
- **Uitkomst:** PASS + N≥150 → Strateeg schrijft PREREG_FTMO_N20 (incl. D-094a (b)). FAIL of N<150 → STOP.
