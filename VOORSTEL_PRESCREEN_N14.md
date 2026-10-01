# VOORSTEL_PRESCREEN_N14 — US100 NY-Open Pre-Market Momentum

**Status:** **geen PREREG** — D-092.1 FAIL (U2 `d4cefff`; mean −5,05 < 1,80 bp; N=183).  
**Auteur:** Strateeg (Claude). Branch `claude/trusting-faraday-34tsmg`.  
**Instrument:** `US100cash` (RT 0,60 bp → drempel 1,80 bp).  
**Grond:** US100 (NASDAQ) heeft de sterkste pre-market drift van alle indices. De 14:30–15:30 CET pre-market-window weerspiegelt institutionele orderketen (futures, dark-pool pre-open). Als de pre-market duidelijk richting heeft, zet die richting zich voort in de eerste 90 minuten van de cashsessie. Onderscheidend van LUNCH_OPEN (fade na 90-min open) en N3 (close-drive 14:30–15:55 ET).

---

## Idee (mechanisme)

US100-futures (NQ) handelen pre-markt op basis van macro-nieuws, earnings en Aziatische-sessie tech-flows. Bij NY-open (15:30 CET / 09:30 ET) activeren institutionele cash-traders hun pre-geprijsde posities. Als de pre-market drift (14:30–15:30 CET) consistent is, geeft de NYSE/NASDAQ-open een volgende impuls in dezelfde richting: market-on-open orders, ETF-creatie (QQQ) en gamma-hedging versterken de trend de eerste 90 minuten.

**Onderscheid van dode sleeves:**
- ≠ LUNCH_OPEN (fade van 09:30–11:00 ET move richting session open; dit = continuation 14:30–15:30 pre-market richting)
- ≠ N3 US100 close-drive (14:30–15:55 ET signaal op close; dit = entry op NY open 15:30 CET, exit 17:00 CET)
- ≠ N5 gap-fill (opening gap fade; dit = intradag pre-market momentum continuation)
- ≠ N12 XAU NY-open (ander instrument)

---

## Regel (bevriesbaar zodra screen PASS)

**Pre-market momentum:**  
- `P_1430` = M5-close van de 14:30 CET bar  
- `P_1530` = M5-close van de 15:30 CET bar (US-open bar)  
- `pm_bp = 1e4 × (P_1530 − P_1430) / P_1430`

**Signalen (max 1 trade/dag):**  
- `pm_bp ≥ +0,25%` (+25 bp) → **LONG** op 15:30 CET close  
- `pm_bp ≤ −0,25%` (−25 bp) → **SHORT** op 15:30 CET close  
- Anders → geen trade  

**Stop:** 1,0 × ATR14 (dag) vanaf instapprijs.  
**Exit:** hard flat 17:00 CET (90 min na entry). Swap = 0 (intradag).

---

## Pre-screen aanvraag (Uitvoerder-2)

- **Data:** `data/m5gz/US100cash.csv.gz`, train 2021-01-01 … 2023-12-31.
- **Regel:** identiek aan §1 hierboven (threshold ±25 bp pm_bp, continuation-entry 15:30 CET, stop ATR14, flat 17:00 CET).
- **Maatstaf:** mean bruto retour in bp.
- **Gate:** mean bruto ≥ **1,80 bp** (3 × 0,60 bp RT).
- **Rapporteer ook N.**
- **Geen test/reserve aanraken.** Alleen train-screen.
- **Uitkomst:** PASS + N≥150 → Strateeg schrijft PREREG_FTMO_N14. FAIL of N<150 → STOP.
