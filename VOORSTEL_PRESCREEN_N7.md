# VOORSTEL_PRESCREEN_N7 — XAU Pre-London Range Breakout

**Status:** Pre-screen aanvraag (D-092.1) — 2026-10-01 02:50 Europe/Amsterdam, branch `claude/trusting-faraday-34tsmg`.  
**Auteur:** Strateeg (Claude). **Geen PREREG vóór screen-PASS.**  
**Instrument:** `XAUUSDcash` (RT 0,83 bp → drempel 2,49 bp).  
**Grond:** XAU_AM_FADE heeft gate PASS (18,7 bp). XAU heeft bewezen intradag-bruto-edge. Dit is een ander tijdvenster + tegengesteld mechanisme (breakout ipv fade, Aziatisch-naar-London ipv London-open-fade).

---

## Idee (mechanisme)

De XAU-markt comprimeert 06:00–08:55 CET: Aziatische sessiespelers winden af, Europese LBMA-deelnemers zijn nog niet actief. Bij London open (09:00 CET) activeren Europese institutionele goudhandelaren (LBMA-leden, hedgefondsen, centrale banken) hun dagelijkse positieorders. Dit veroorzaakt een directionale impuls die de gecomprimeerde Aziatische range breekt.

**Onderscheid van dode sleeves:**
- ≠ XAU_AM_FADE (fade eerste ochtendbeweging 09:00–09:55 CET; dit = breakout na 09:00 CET)
- ≠ N4 XAU_PRENY (pre-NY range 13:00–14:55 CET, NY open; dit = pre-London range 06:00–08:55 CET)
- ≠ N7 is London-sessie (09:00 CET); N4 is NY-sessie (15:00 CET)

---

## Regel (bevriesbaar zodra screen PASS)

**Pre-London Range (PLR):** high/low van M5-bars 06:00–08:55 CET (36 bars).  
**Minimale breedte:** PLR_high − PLR_low ≥ 0,10% van PLR_midpoint (anders geen trade).  
**Entry:** eerste M5-slotkoers ná 09:00 CET > PLR_high → **long**; < PLR_low → **short**.  
**OCO:** zodra één kant geactiveerd, ander geannuleerd. Max 1 trade/dag.  
**Stop:** PLR tegenoverliggende kant (PLR_low voor long, PLR_high voor short).  
**Exit:** flat op 11:00 CET (2 uur na London open). Swap = 0 (intradag).

---

## Pre-screen aanvraag (Uitvoerder-2)

- **Data:** `data/m5gz/XAUUSDcash.csv.gz`, train 2021-01-01 … 2023-12-31.
- **Maatstaf:** mean bruto retour in bp (1 bp = 0,01%).
- **Gate:** mean bruto ≥ **2,49 bp** (3 × 0,83 bp RT).
- **Geen test/reserve aanraken.** Alleen train-screen.
- **Uitkomst:**
  - PASS → Strateeg schrijft PREREG_FTMO_N7.
  - FAIL → STOP, geen PREREG.
