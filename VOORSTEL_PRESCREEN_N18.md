# VOORSTEL_PRESCREEN_N18 — US500 Overnight Gap Continuation

**Status:** **GESLOTEN** — C-014 PASS_may_PREREG → PREREG → U2 FAIL_T (`d1984ed`, TRIAL 447); D-093 freeze.  
**Auteur:** Strateeg (Claude). Geen heropenen zonder CEO.  
**Instrument:** `US500cash` (RT 0,78 bp → drempel 2,34 bp).  
**Grond:** Grote overnight gaps (≥ +0,50%) in US500 weerspiegelen hoge-convictie institutionele positie-opbouw (earnings, Fed-surprise, macro-inflection). Deze gaps worden NIET onmiddellijk gevuld: de institutionele orderflow die de gap creëerde is nog aanwezig bij market-open en versterkt de richting gedurende 2-3 uur. Tegengesteld mechanisme van N5 (gap-fade, FAIL) en CTO-barred ORB-familie.

---

## Idee (mechanisme)

US500 overnachtingshandel (futures 22:05–15:29 CET) reflecteert Aziatische sessies, pre-markt news en macro-catalysts. Als de futures een grote gap opbouwen (>0,50% vs prior cash close), zijn grote institutionele spelers positie ingegaan met sterke overtuiging. Bij NY-cash-open (15:30 CET) volgen ETF-arbitrageurs, market-on-open orders en optie-gamma-hedgers dezelfde richting. De continuation duurt typisch 2–3 uur voordat early-afternoon mean-reversion intreedt.

**Onderscheid:**
- ≠ N5 (gap FADE ≥ 0,30%; dit = gap CONTINUATION ≥ 0,50%; tegengesteld mechanisme)
- ≠ N14 US100 NY-Open PM (pre-market last-hour vs prior close; dit = full overnight gap vs prior day's close)
- ≠ alle ORBs (geen range; anchor = overnight-gap)
- ≠ LUNCH_OPEN (ochtend-fade; dit = NY-open continuation)

---

## Regel (bevriesbaar zodra screen PASS)

**Overnight gap:**  
- `P_prior_close` = M5-close van de 22:00 CET bar van de vorige handelsdag (US regular session close)  
- `P_open` = M5-close van de 15:30 CET bar (eerste NY cash bar)  
- `gap_bp = 1e4 × (P_open − P_prior_close) / P_prior_close`

**Signalen (max 1 trade/dag):**  
- `gap_bp ≥ +0,50%` (+50 bp) → **LONG** op 15:30 CET close  
- `gap_bp ≤ −0,50%` (−50 bp) → **SHORT** op 15:30 CET close  
- Anders → geen trade  

**Stop:** 1,5 × ATR14 (dag) vanaf instapprijs.  
**Exit:** hard flat 18:30 CET (3 uur na entry). Swap = 0 (intradag).

---

## Pre-screen aanvraag (Uitvoerder-2)

- **Data:** `data/m5gz/US500cash.csv.gz`, train 2021-01-01 … 2023-12-31.
- **Regel:** identiek aan §1 hierboven (gap ≥ ±50 bp vs prior 22:00 close, continuation-entry 15:30 CET, stop 1.5 ATR14, flat 18:30 CET).
- **Maatstaf:** mean bruto retour in bp + median + N.
- **Gate:** mean bruto ≥ **2,34 bp** (3 × 0,78 bp RT). N≥150 vereist.
- **Geen test/reserve aanraken.** Alleen train-screen.
- **Uitkomst:** PASS + N≥150 → Strateeg schrijft PREREG_FTMO_N18. FAIL of N<150 → STOP.
