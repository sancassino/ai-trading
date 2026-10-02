# VOORSTEL_PRESCREEN_N24 — US500cash Mid-Session Lunch Fade (post-AM MR)

**Status:** **geen PREREG — U2 D-092.1 FAIL** (train N=271 mean 0.35 bp < gate 2.34; cite tip after this commit).
**Auteur:** Strateeg (Grok).  
**Instrument:** `US500cash` (RT **0,78 bp** COSTS_FTMO / `results/screen_cost_vol.csv` → drempel **2,34 bp** = 3× RT; cost_in_costs_ftmo=True).  
**Track 2:** index — US500 unused angle (N18 gap-cont dood; N5 gap-fade dood; geen US500 lunch-fade eerder).  
**Grond:** Na de NY ochtendimpuls (15:30–18:00 CET) trekt lunch-liquiditeit (12:00 ET) vaak een partial mean-reversion in: inventory van AM-trend-volgers wordt afgebouwd vóór de PM-sessie. Dit is **fade** van de AM-move op US500 — tegengesteld aan N20 (US30 PM **continuation**), en ≠ LUNCH_OPEN (open-anchor fade van 09:30–11:00 ET impulse). Intradag flat → swap 0.

**D-094a:** train 2021–2023 = 3y. Schriftelijke reden **(b)**: midday inventory / lunch mean-reversion op equity-index futures is microstructure-standaard (proxy ES/SPX langere historie); FTMO-M5 toetst kosten/uitvoering. Herhaal in toekomstige PREREG.

---

## Idee (mechanisme)

US500 AM-move 15:30→18:00 CET meet de ochtendimpuls. Als |impuls| ≥ 40 bp, fading desks en lunch-rebalancing duwen prijs terug richting NY-open in 18:00–20:30 CET. Geen ORB, geen gap-regel, geen PM-continuation.

**Onderscheid van dode sleeves:**
- ≠ **N20** US30 PM Continuation (continuation; ander symbool; dit = **fade** op US500)
- ≠ **LUNCH_OPEN** (fade naar daily open van vroege AM-impulse; dit = fade van 15:30–18:00 CET move, entry 18:00)
- ≠ **MIDDAY_VWAP** / **IB_FADE** / **VWAP_PB** (geen VWAP/IB-anker)
- ≠ **N5** gap-fill / **N18** overnight gap continuation
- ≠ ORB-familie (A1/N11/N15–N17)

---

## Regel (bevriesbaar zodra screen PASS)

**AM-impuls tot lunch:**  
- `P_open` = M5-close 15:30 CET (NY cash open)  
- `P_1800` = M5-close 18:00 CET (12:00 ET)  
- `am_bp = 1e4 × (P_1800 − P_open) / P_open`

**Signalen (max 1 trade/dag):**  
- `am_bp ≥ +40 bp` → **SHORT** op 18:00 CET close (fade AM-long)  
- `am_bp ≤ −40 bp` → **LONG** op 18:00 CET close  
- Anders → geen trade  

**Stop:** 1,0 × ATR14 (dag) vanaf entry.  
**Exit:** hard flat **20:30 CET** (14:30 ET). **Swap = 0** (intradag).

---

## Pre-screen aanvraag (Uitvoerder-2)

- **Data:** `data/m5gz/US500cash.csv.gz`, train **2021-01-01 … 2023-12-31** only.
- **Regel:** am_bp 15:30–18:00 CET ≥ ±40 bp → fade entry 18:00 CET, stop ATR14, flat 20:30 CET.
- **Maatstaf:** signed mean bruto bp + median + N.
- **Gate:** mean bruto ≥ **2,34 bp** (3 × 0,78 bp RT). N≥150.
- **Geen test/reserve (2024/2025+) aanraken.**
- **Uitkomst:** PASS + N≥150 → PREREG_FTMO_N24 (D-094a (b)). FAIL of N<150 → STOP.
