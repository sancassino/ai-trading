# VOORSTEL_PRESCREEN_N19 — XAU Overnight Gap Fill

**Status:** Pre-screen aanvraag (D-092.1) — 2026-10-01 04:35 Europe/Amsterdam, branch `claude/trusting-faraday-34tsmg`.  
**Auteur:** Strateeg (Claude). **Geen PREREG vóór screen-PASS.**  
**Instrument:** `XAUUSDcash` (RT 0,83 bp → drempel 2,49 bp).  
**Grond:** XAU sluit elke dag via LBMA/COMEX at-close en opent de volgende dag op basis van Aziatische overnight flows. Overnight gaps voor XAU worden bij London-preopen (08:00 CET) gewoonlijk geïnitieerd voor het fill: LBMA-leden herpositioneren t.o.v. het gefixte niveau en de prior-day-close. Dit is een gap-fill-mechanisme specifiek voor XAU (anders dan N5 = US-equity gap fill FAIL; en alle geteste XAU-vensters zijn London/NY-sessie, niet pre-London).

---

## Idee (mechanisme)

De LBMA-markt gaat open om 08:00 CET met LBMA-leden die hun overnight inventaris sluiten en herpositioneren t.o.v. de prior-day close. Overnight moves in XAU worden grotendeels gedreven door Aziatische retail (Shanghai Gold Exchange) en macro-news buiten handelsuren. LBMA-professionals handelen t.o.v. bekende fundamentele niveaus (AM/PM fix, prior close) en brengen de prijs terug naar "fair value" vóór de London AM session opent voor institutionele orders.

**Onderscheid:**
- ≠ N5 gap fill (US500/US100 equity; dit = XAU, ander mechanisme en sessieopening)
- ≠ XAU_AM_FADE (fade van eerste London-move 09:00–09:55 CET; dit = pre-London gap fill 08:00–10:00 CET vs prior close)
- ≠ N7 Pre-London BO (breakout 06:00–08:55 CET range; dit = gap fill vs prior-day close)
- ≠ N8/N10/N12 (post-AM-fix / mid-London / NY-open vensters)

---

## Regel (bevriesbaar zodra screen PASS)

**Overnight gap:**  
- `P_prior_close` = M5-close van de 22:00 CET bar (COMEX close, vorige handelsdag)  
- `P_preopen` = M5-close van de 08:00 CET bar (London pre-open bar)  
- `gap_bp = 1e4 × (P_preopen − P_prior_close) / P_prior_close`

**Signalen (max 1 trade/dag):**  
- `gap_bp ≥ +0,30%` (+30 bp) → **SHORT** op 08:00 CET close (fade gap omhoog terug naar prior close)  
- `gap_bp ≤ −0,30%` (−30 bp) → **LONG** op 08:00 CET close (fade gap omlaag)  
- Anders → geen trade  

**Target:** `P_prior_close` (gap fill).  
**Stop:** 1,0 × ATR14 (dag) vanaf instapprijs.  
**Exit:** hard flat 10:30 CET (2,5 uur na entry; vóór LBMA AM-fixing). Swap = 0 (intradag).

---

## Pre-screen aanvraag (Uitvoerder-2)

- **Data:** `data/m5gz/XAUUSDcash.csv.gz`, train 2021-01-01 … 2023-12-31.
- **Regel:** identiek aan §1 hierboven (overnight gap ≥ ±30 bp vs 22:00 CET prior close, fade-entry 08:00 CET, target = prior close, stop ATR14, flat 10:30 CET).
- **Maatstaf:** mean bruto retour in bp + median + N.
- **Gate:** mean bruto ≥ **2,49 bp** (3 × 0,83 bp RT). N≥150 vereist.
- **Geen test/reserve aanraken.** Alleen train-screen.
- **Uitkomst:** PASS + N≥150 → Strateeg schrijft PREREG_FTMO_N19. FAIL of N<150 → STOP.
