# VOORSTEL_PRESCREEN_N12 — XAU NY-Open Continuation

**Status:** **geen PREREG** — D-092.1 FAIL (C-012 `cdabfe8`; mean +0,59 < 2,49 bp; N=303).  
**Auteur:** Strateeg (Claude). Branch `claude/trusting-faraday-34tsmg`.  
**Instrument:** `XAUUSDcash` (RT 0,83 bp → drempel 2,49 bp).  
**Grond:** XAU heeft bewezen intradag-bruto-edge (XAU_AM_FADE +18,70 bp). NY-open (15:30 CET / 09:30 ET) activeert COMEX-futures en US-macro traders — sterkste liquiditeitsimpuls voor XAU na London. De pre-NY handoff-move (14:30–15:30 CET) signaleert institutionele richting; continuation na NY-open heeft andere dynamiek dan alle eerder geteste XAU-vensters.

---

## Idee (mechanisme)

Bij NY-open (15:30 CET) activeren COMEX-futures en US-gebaseerde hedgefondsen, ETF-leveranciers (GLD, IAU) en macro-traders hun dagelijkse XAU-posities. De uur vóór NY-open (14:30–15:30 CET) weerspiegelt London-to-NY handoff: de richting van deze move geeft de institutionele consensus op het moment dat de meest liquide markt opengaat. Na 15:30 CET versterkt COMEX-liquiditeit de bestaande richting gedurende ~90 minuten (tot voor de London/NY overlap-fade die later intreedt).

**Onderscheid van dode sleeves:**
- ≠ N4 XAU_PRENY (N4 = range-breakout van 13:00–14:55 CET range, entry 15:00 CET; dit = continuation-signaal van 14:30–15:30 CET move, entry 15:30 CET — later window, andere richting-definitie)
- ≠ N7 Pre-London BO (London open 09:00 CET; dit = NY-open 15:30 CET)
- ≠ N8 Post-AM-Fix (10:30 CET; dit = 15:30 CET)
- ≠ N10 Mid-London Fade (12:00 CET, fade; dit = 15:30 CET, continuation)
- ≠ XAU_AM_FADE (09:00–09:55 CET; dit = 15:30 CET)

---

## Regel (bevriesbaar zodra screen PASS)

**Handoff-move:**  
- `P_1430` = M5-close van de 14:30 CET bar  
- `P_1530` = M5-close van de 15:30 CET bar (NY-open bar)  
- `handoff_bp = 1e4 × (P_1530 − P_1430) / P_1430`

**Signalen (max 1 trade/dag):**  
- `handoff_bp ≥ +0,20%` (+20 bp) → **LONG** op 15:30 CET close (continuation)  
- `handoff_bp ≤ −0,20%` (−20 bp) → **SHORT** op 15:30 CET close  
- Anders → geen trade  

**Stop:** 1,0 × ATR14 (dag) vanaf instapprijs.  
**Exit:** hard flat 17:00 CET (90 minuten na entry; vóór London-NY overlap-fade en EOD-positionering). Swap = 0 (intradag).

---

## Pre-screen aanvraag (Uitvoerder-2)

- **Data:** `data/m5gz/XAUUSDcash.csv.gz`, train 2021-01-01 … 2023-12-31.
- **Regel:** identiek aan §1 hierboven (threshold ±20 bp handoff-move, continuation-entry 15:30 CET, stop ATR14, flat 17:00 CET).
- **Maatstaf:** mean bruto retour in bp (1 bp = 0,01%).
- **Gate:** mean bruto ≥ **2,49 bp** (3 × 0,83 bp RT).
- **Rapporteer ook N (aantal trades).**
- **Geen test/reserve aanraken.** Alleen train-screen.
- **Uitkomst:** PASS + N≥150 → Strateeg schrijft PREREG_FTMO_N12. FAIL of N<150 → STOP.
