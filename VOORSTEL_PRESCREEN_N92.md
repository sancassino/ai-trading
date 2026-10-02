# VOORSTEL_PRESCREEN_N92 — US100cash NY-Open 2h Momentum (D-100 family D; NEW_FAMILY Q)

**Status:** **STOP FAIL_T** — U2 `b5b59e0` (TRIAL **457→458**); cost-gate PASS +5,90≥1,98 / stress PASS; formal t_NW 1,56<2 train; test t_NW 0,51. Dead += `N92_US100_NY_2H_MOM`. No NY-2h mom clones.  
**Auteur:** Strateeg (Claude). **NEW_FAMILY Q** (US100cash NY-session open-window momentum — nooit eerder als deze setup).  
**Instrument:** `US100cash` (RT **0,66 bp** — COSTS_FTMO; intradag-flat = geen swap).  
**Track 2+4 + D-100 family D:** richtingmomentum in eerste 2u van NY handelsdag (15:30–17:30 CET) → continuer positie 17:30–22:00 CET. Flat voor nacht.

**Gate (intradag-flat; geen swap):**  
0,66 + 0 = **0,66 bp** → gate 3 × 0,66 = **1,98 bp**.

**D-094a:** train 2021–2023. Reden **(b)**: intradag momentum equity-index NY-open (Gao et al. 2018 intraday momentum NAS futures; Chan et al. 1996 equity momentum; NASDAQ/tech open-auction persistent directional drift; FTMO-M5 = kosten). Herhaal in PREREG.

**Onderscheid:**
- ≠ **N89** GER40cash EU-session 2h open FAIL (ander index EU-sessie 08:00–10:00 CET; dit = US100 NY-sessie 15:30–17:30 CET; ander mechanisme en tijdvenster)
- ≠ **N40** GER40 mid-morning FAIL (DAX ander index)
- ≠ **N87** US30cash opening-gap fade FAIL_T (gap-fade mean-reversion ≠ session momentum continuation; US30 ≠ US100)
- ≠ **ORB** BARRED (range breakout; dit = directie van eerste 2u NY-window)
- ≠ enig TSMOM swing / FX carry / metals / overnight

## Regel
- `ret2h = (P_{17:30} − P_{15:30}) / P_{15:30}` (M5-bar close ≈ 17:30 CET vs ≈ 15:30 CET)
- `ret2h > 0` → **LONG** op 17:30-bar close; flat 22:00 CET (M5-bar ≈ 22:00)
- `ret2h < 0` → **SHORT** op 17:30-bar close; flat 22:00 CET
- `ret2h = 0` → skip
- **Geen overnight hold.** Bilateraal. Max 1 positie per dag.

## Pre-screen
- Data: `data/m5gz/US100cash.csv.gz` → M5 bars, train **2021-01-01 … 2023-12-31**.
- Gate: mean bruto ≥ **1,98 bp**, N ≥ 150.
- PASS → PREREG_FTMO_N92. FAIL → STOP (geen tijdvenster-grid, geen US500-switch).
