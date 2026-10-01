# VOORSTEL_PRESCREEN_N25 — XAUUSD NY Afternoon Fade (vs NY open)

**Status:** **geen PREREG — D-092.1 FAIL** (Strateeg screen 2026-10-01 08:22; N=334, mean **+1,14** < 2,49 bp). Artifacts `results/R2/n24_n27_prescreen/`.  
**Auteur:** Strateeg (Grok).  
**Instrument:** `XAUUSD` (RT **0,83 bp** COSTS_FTMO / screen → drempel **2,49 bp** = 3× RT).  
**Track 2:** commodity/metaal — XAU, **ander venster** dan dode XAU-set.  
**Grond:** Na NY-open (15:30 CET) bouwt goud vaak een ochtendextensie op; in de NY afternoon (18:00–20:30 CET / 12:00–14:30 ET) unwindt COMEX/ETF-flow een deel van die extensie terug richting NY-open wanneer er geen verse macro-impuls is (puur prijsregel, geen event-peek). Intradag flat → swap 0.

**D-094a:** train 2021–2023 = 3y. Schriftelijke reden **(b)**: afternoon inventory fade op goud is tijdloos microstructure (proxy GC futures langer); FTMO-M5 = kosten/uitvoering. Herhaal in PREREG.

---

## Idee (mechanisme)

Meet afwijking van NY-open om 18:00 CET. Extreme |dev| ≥ 35 bp → fade terug in 18:00–20:30 CET. Dit is **niet** London-AM (AM_FADE/N10), **niet** pre-NY breakout (N4/N7), **niet** NY-open continuation (N12), **niet** overnight gap (N19).

**Onderscheid van dode sleeves:**
- ≠ **S2-XAU_AM_FADE** / **N10** (London-ochtend / mid-London → AM-fix)
- ≠ **N4** Pre-NY range BO / **N7** Pre-London BO / **N8** Post-AM-Fix cont. / **N12** NY-Open Continuation
- ≠ **N19** Overnight Gap Fill (pre-London 08:00)
- ≠ **S2-XAU** London–NY overlap **breakout**
- ≠ ORB-familie

---

## Regel (bevriesbaar zodra screen PASS)

**NY-open afwijking:**  
- `P_ny` = M5-close 15:30 CET  
- `P_1800` = M5-close 18:00 CET  
- `dev_bp = 1e4 × (P_1800 − P_ny) / P_ny`

**Signalen (max 1 trade/dag):**  
- `dev_bp ≥ +35 bp` → **SHORT** op 18:00 CET close  
- `dev_bp ≤ −35 bp` → **LONG** op 18:00 CET close  
- Anders → geen trade  

**Stop:** 1,0 × ATR14 (dag) vanaf entry.  
**Exit:** hard flat **20:30 CET**. **Swap = 0**.

---

## Pre-screen aanvraag (Uitvoerder-2)

- **Data:** `data/m5gz/XAUUSD.csv.gz`, train **2021-01-01 … 2023-12-31** only.
- **Regel:** dev_bp 15:30–18:00 CET ≥ ±35 bp → fade 18:00 CET, stop ATR14, flat 20:30 CET.
- **Maatstaf:** signed mean bruto bp + median + N.
- **Gate:** mean bruto ≥ **2,49 bp** (3 × 0,83 bp RT). N≥150.
- **Geen test/reserve aanraken.**
- **Uitkomst:** PASS + N≥150 → PREREG_FTMO_N25 (D-094a (b)). FAIL of N<150 → STOP.
