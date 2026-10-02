# VOORSTEL_PRESCREEN_N89 — GER40cash EU-Session 2h Open Momentum (D-100 family D; NEW_FAMILY N)

**Status:** **geen PREREG — D-092.1 pre-FAIL** — U2 informal `d17573c` (mean +1,06 ≪ gate 2,16); no trial (2026-10-01 ~17:50 CEST).  
**Auteur:** Strateeg (Claude). **NEW_FAMILY N** (EU-session open-window momentum — nooit eerder als deze setup).  
**Instrument:** `GER40cash` (RT **0,72 bp** — COSTS_FTMO; intradag-flat = geen swap).  
**Track 2+4 + D-100 family D:** richtingmomentum in eerste 2u (08:00–10:00 CET) van EU handelsdag → continuer positie 10:00–17:00 CET. Flat voor nacht.

**Gate (intradag-flat; geen swap):**  
0,72 + 0 = **0,72 bp** → gate 3 × 0,72 = **2,16 bp**.

**D-094a:** train 2021–2023. Reden **(b)**: intradag momentum equity-index literatuur (Bogousslavsky & Muravyev 2023 open-auction persistence; EU-session DAX opening directional drift; FTMO-M5 = kosten). Herhaal in PREREG.

**Onderscheid:**
- ≠ **N40** GER40 mid-morning FAIL (N40 was mid-morning window ~10:00–12:00 momentum; dit = 08:00–10:00 open-window → continuer 10:00–17:00; ander mechanisme en tijdvenster)
- ≠ **N35** US100 EU→US continuation FAIL_T (ander index + US-sessie; dit = pure GER40 EU-sessie)
- ≠ **ORB** BARRED (range breakout na opening range; dit = directie van eerste 2u open-window)
- ≠ enig TSMOM swing / FX / metals / overnight

## Regel
- `ret2h = (P_{10:00} − P_{08:00}) / P_{08:00}` (M5-bar close ≈ 10:00 CET vs ≈ 08:00 CET)
- `ret2h > 0` → **LONG** op 10:00-bar close; flat 17:00 CET (M5-bar ≈ 17:00)
- `ret2h < 0` → **SHORT** op 10:00-bar close; flat 17:00 CET
- `ret2h = 0` → skip
- **Geen overnight hold.** Bilateraal. Max 1 positie per dag.

## Pre-screen
- Data: `data/m5gz/GER40cash.csv.gz` → M5 bars, train **2021-01-01 … 2023-12-31**.
- Gate: mean bruto ≥ **2,16 bp**, N ≥ 150.
- PASS → PREREG_FTMO_N89. FAIL → STOP (geen tijdvenster-grid, geen US500-switch).
