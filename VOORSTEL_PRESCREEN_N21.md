# VOORSTEL_PRESCREEN_N21 — GER40 Afternoon Deviation Fade (post-NY-open)

**Status:** **FAIL** — U2 D-092.1 train-only pre-screen 2026-10-01 CEST. N=234, mean bruto=-2.4515 bp, gate=2.16 bp → `NO_PREREG_screen_fail`. See `results/R2/n20_n23_prescreen/`. **No PREREG.**

**U2 pre-screen result:** see RUNLOG_R2 / prescreen.md — mean bruto below gate; N≥150; STOP.
**Auteur:** Strateeg (Grok).  
**Instrument:** `GER40cash` (RT 0,72 bp COSTS_FTMO / screen → drempel **2,16 bp** = 3× RT).  
**Track:** non-US index afternoon inventory-fade (heropen onder D-094).  
**Grond:** GER40 overshoots bij US-open (15:30 CET) door index-arbitrage. Na 1 uur (16:30 CET) is de NY-open volatiliteit verwerkt en begint XETRA-close positioning voor 17:30 CET. Als GER40 sterk is afgeweken van de XETRA-open (09:00 CET), trekken close-gerelateerde order-flows (ETF NAV-rebalancing, DAX-futures convergentie) de prijs terug richting dag-gemiddelde. Onderscheidend van N9 (morning fade) en N11 (ORB, dead).

**D-094a (geschiedenis <5y):** train-screen 2021–2023 = 3y. Schriftelijke reden **(b)**: end-of-day inventory unwind / deviation-fade naar open is een tijdloos microstructure-effect op liquide index futures (proxy: DAX/FDAX langere historie); FTMO-M5 toetst kosten/uitvoering. Herhaal in toekomstige PREREG.

---

## Idee (mechanisme)

XETRA-open (09:00 CET) is het dagankerpunt voor GER40 institutionele pricing. Door de dag heen — London morning, pre-NY, NY-open — beweegt GER40 van dit anker weg. Vóór de XETRA-close-auction (17:30 CET) moeten ETF-managers, DAX-futures arbs en index-rebalancers terug naar fair value. Als de cumulatieve dagsafwijking ≥ 0,50% is om 16:30 CET, is de kans op een partial-reversion in het 16:30–17:30 CET venster hoog. Dit is het "afternoon inventory unwind" mechanisme.

**Onderscheid van dode sleeves:**
- ≠ N9 GER40 Ochtend-Fade (entry 10:30 CET, exit 12:00 CET; dit = entry 16:30 CET, exit 17:30 CET — ander venster)
- ≠ N11 GER40 XETRA ORB (dead; ORB breakout; dit = end-of-day deviation fade)
- ≠ N6 GER40 pre-close momentum (N6 had CONTINUATION signal; dit = FADE/reversion signal)
- ≠ N13 GER40 US-Open Sync (US500 signal, continuation; dit = interne GER40 deviation, fade)
- ≠ simple ORB-familie

---

## Regel (bevriesbaar zodra screen PASS)

**Dagafwijking van XETRA-open:**  
- `P_xetra_open` = M5-close van de 09:00 CET bar (XETRA-open)  
- `P_1630` = M5-close van de 16:30 CET bar  
- `dev_bp = 1e4 × (P_1630 − P_xetra_open) / P_xetra_open`

**Signalen (max 1 trade/dag):**  
- `dev_bp ≥ +0,50%` (+50 bp) → **SHORT** op 16:30 CET close (fade terug richting XETRA-open)  
- `dev_bp ≤ −0,50%` (−50 bp) → **LONG** op 16:30 CET close  
- Anders → geen trade  

**Stop:** 1,0 × ATR14 (dag) vanaf instapprijs.  
**Exit:** hard flat 17:30 CET (XETRA-close; 1 uur na entry). Swap = 0 (intradag).

---

## Pre-screen aanvraag (Uitvoerder-2)

- **Data:** `data/m5gz/GER40cash.csv.gz`, train 2021-01-01 … 2023-12-31.
- **Regel:** identiek hierboven (dev_bp 09:00–16:30 CET ≥ ±50 bp, fade-entry 16:30 CET, stop ATR14, flat 17:30 CET).
- **Maatstaf:** mean bruto retour in bp + median + N (signed mean).
- **Gate:** mean bruto ≥ **2,16 bp** (3 × 0,72 bp RT). N≥150 vereist.
- **Geen test/reserve aanraken.** Alleen train-screen.
- **Uitkomst:** PASS + N≥150 → Strateeg schrijft PREREG_FTMO_N21 (incl. D-094a (b)). FAIL of N<150 → STOP.
