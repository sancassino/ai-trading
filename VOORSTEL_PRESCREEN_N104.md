# VOORSTEL_PRESCREEN_N104 — GBPCHF Long-Only 5d GBP-CHF Carry+Momentum (NEW_FAMILY AA)

**Status:** **OPEN** — pipeline replace after U2 N100/N101 FAIL_T (filed 2026-10-02 ~22:05 CEST).  
**Auteur:** Strateeg (Grok). **NEW_FAMILY AA** (GBPCHF sterling-vs-CHF funding carry+momentum long-only — nooit als deze setup).  
**Instrument:** `GBPCHF` (RT **est. 1,51** bp — M5 spread_med≈0,91 bp 2024–26 + FX commissie≈0,30×2; **not in** `COSTS_FTMO.csv` — U2 remeasure before any PREREG; swap_long GBP vs CHF = earn → 0 in gate per D-100).  
**Track 4 + D-100 family B:** GBPCHF long-only 5d swing. Long = GBP vs CHF funding (BoE >> SNB) + positief 5d momentum.

**Gate (long-only; 4 nachten; swap earn → 0 in gate per D-100):**  
1,51 → gate 3 × 1,51 = **4,53** bp.  
(Swap-credit telt NIET als alfa; bruto = signed prijsrendement.)

**D-094a:** train 2021–2023. Reden **(b)**: FX carry + TSMOM on GBP/CHF (Menkhoff et al. 2012; funding-currency short CHF; FTMO-M5 = kosten). Herhaal in PREREG. ≥5y proxy + FTMO-M5 train.

**Onderscheid:**
- ≠ **N102** USDCHF LO 5d (USD≠GBP; Fed vs BoE funding)
- ≠ **N99** CADCHF LO oil-CHF DIAG_FAIL (CAD≠GBP; olie vs pure sterling funding)
- ≠ **N63** EURCHF LO FAIL / **N74** USDCHF L60 BARRED
- ≠ **N90** GBPJPY / **N91** AUDUSD / **N96** CADJPY / **N97** AUDCAD
- ≠ EMB / CRACK / SECTOR_DISP / VIX / ORB-meta / UKOIL-OVN / CORN / NY-2h / L60 / N75–N103 restarts

## Regel
- `ret5 = close_t / close_{t−5} − 1` (dagclose uit M5; laatste bar ≤22:00 CET)
- `ret5 > 0` → **LONG** op close_t
- `ret5 ≤ 0` → skip (geen short-been; short GBPCHF swap structureel duur vs long earn)
- Hold: exit close_{t+5}. **Non-overlapping**. Alleen LONG.

## Pre-screen
- Data: `data/m5gz/GBPCHF.csv.gz` → dagclose, train **2021-01-01 … 2023-12-31**.
- Gate: mean bruto ≥ **4,53** bp, N ≥ 150.
- PASS → PREREG_FTMO_N104. FAIL → STOP (geen ret10-switch, geen USDCHF/CADCHF twin, geen L60 rewrite, geen soft gate).
