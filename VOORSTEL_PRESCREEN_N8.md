# VOORSTEL_PRESCREEN_N8 — XAU Post-AM-Fix Continuation

**Status:** Pre-screen aanvraag (D-092.1) — 2026-10-01 02:50 Europe/Amsterdam, branch `claude/trusting-faraday-34tsmg`.  
**Auteur:** Strateeg (Claude). **Geen PREREG vóór screen-PASS.**  
**Instrument:** `XAUUSDcash` (RT 0,83 bp → drempel 2,49 bp).  
**Grond:** De LBMA AM-fixing (±10:30 CET) is het dagelijkse anker voor goudprijzen. Na de fixing is de institutionele orderflow zichtbaar: leveranciers, ETF-rebalancers en hedgefondsen reageren op het gefixte niveau. Dit is een mechanistisch ander venster dan AM_FADE (pre-fixing) en N4 (pre-NY).

---

## Idee (mechanisme)

De LBMA AM-fixing (±10:30 CET) fixeert de goudprijs op basis van bied-/laataanbod van LBMA-leden. Na de fixing:
- ETF-leveranciers en afnemers kopen/verkopen fysiek goud op basis van de gefixte prijs
- Macro-hedgefondsen positioneren op de dagrichting (fixing-prijs = referentie)
- De markt has een institutionele directionaliteit voor de komende 1,5–2 uur

Als de London-ochtend een duidelijke richting heeft (09:00–10:30 CET), versterkt de post-fixing flow die richting.

**Onderscheid van dode sleeves:**
- ≠ XAU_AM_FADE (fade van ochtendbeweging vóór 10:00 CET; dit = continuation ná fixing 10:30 CET)
- ≠ N4 XAU_PRENY (NY-sessie 13:00–15:00 CET; dit = London-mid-sessie 10:30–12:30 CET)
- ≠ N7 (N7 = bij London open 09:00 CET; dit = na AM-fixing 10:30 CET, later venster)

---

## Regel (bevriesbaar zodra screen PASS)

**Trend-filter (London ochtend):** close 10:30 CET vs open 09:00 CET:
- **Long-signaal:** close 10:30 CET > open 09:00 CET × 1,002 (+0,20%) → long entry op 10:30 CET close-bar.
- **Short-signaal:** close 10:30 CET < open 09:00 CET × 0,998 (−0,20%) → short entry op 10:30 CET close-bar.
- Geen trade als |beweging| < 0,20%.

**Entry:** close van 10:30 CET bar. Max 1 trade/dag; geen herentry.  
**Stop:** 1,0 × ATR14 (dag) vanaf instapprijs.  
**Exit:** flat op 12:30 CET (2 uur na entry). Swap = 0 (intradag).

---

## Pre-screen aanvraag (Uitvoerder-2)

- **Data:** `data/m5gz/XAUUSDcash.csv.gz`, train 2021-01-01 … 2023-12-31.
- **Maatstaf:** mean bruto retour in bp (1 bp = 0,01%).
- **Gate:** mean bruto ≥ **2,49 bp** (3 × 0,83 bp RT).
- **Geen test/reserve aanraken.** Alleen train-screen.
- **Uitkomst:**
  - PASS → Strateeg schrijft PREREG_FTMO_N8.
  - FAIL → STOP, geen PREREG.
