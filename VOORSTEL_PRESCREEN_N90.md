# VOORSTEL_PRESCREEN_N90 — GBPJPY Long-Only 5d Carry+Momentum (D-100 family B; NEW_FAMILY O)

**Status:** **OPEN** — pipeline aanvulling na N87 FAIL_T (TRIAL 457; filed 2026-10-01 ~15:50 CEST).  
**Auteur:** Strateeg (Claude). **NEW_FAMILY O** (GBPJPY carry+momentum long-only — nooit eerder geprobeerd).  
**Instrument:** `GBPJPY` (RT **0,72 bp** — COSTS_FTMO; swap_long positief = earn bij long).  
**Track 4 + D-100 family B:** GBPJPY long-only 5d swing. Long = structurele GBP carry vs JPY (GBP policy rate >> JPY near-zero) + momentumsignaal. Overnight long GBPJPY = positieve carry (swap_long > 0).

**Gate (long-only; 4 nachten; swap earn → 0 in gate per D-100):**  
0,72 + 4 × max(swap_long_cost, 0) = 0,72 + 0 = **0,72 bp** → gate 3 × 0,72 = **2,16 bp**.  
(Swap-credit telt NIET als alfa per D-100; alleen RT in gate.)

**D-094a:** train 2021–2023. Reden **(b)**: GBP vs JPY carry-momentum cross (Menkhoff et al. 2012 FX TSMOM; Burnside et al. 2011 carry; GBPJPY = hoog-vol carry-cross met persistentie bij positief momentum; FTMO-M5 = kosten). Herhaal in PREREG.

**Onderscheid:**
- ≠ **N88** EURGBP 5d short-only OPEN (EURGBP cross + short-only EUR-zwakte; dit = GBPJPY + long-only GBP-carry)
- ≠ **N28** EURJPY Lon→NY FAIL (intradag FX momentum EUR/JPY; dit = 5d swing GBP/JPY)
- ≠ **L60 FX-med** BARRED (USDJPY_MED/EURJPY_MED; dit = GBPJPY cross + long-only carry)
- ≠ **FX_EUR_SHORT_TSMOM** FAIL_T (EUR-short EURUSD/EURAUD; dit = GBP-long GBPJPY)
- ≠ **N71** GBPUSD short OPEN (GBPUSD ≠ GBPJPY; USD ≠ JPY; ander mechanisme)
- ≠ enig intradag / gap-fade / equity-index / metals

## Regel
- `ret5 = close_t / close_{t−5} − 1` (dagclose uit M5; laatste bar ≤22:00 CET)
- `ret5 > 0` → **LONG** op close_t (positief 5d momentum = carry-richting)
- `ret5 < 0` → skip (geen short-been; structureel asymmetrisch: short-side swap-kosten te hoog)
- Hold: exit close_{t+5}. **Non-overlapping**. Alleen LONG.

## Pre-screen
- Data: `data/m5gz/GBPJPY.csv.gz` → dagclose, train **2021-01-01 … 2023-12-31**.
- Gate: mean bruto ≥ **2,16 bp**, N ≥ 150.
- PASS → PREREG_FTMO_N90. FAIL → STOP (geen ret10-switch, geen GBPUSD-add).
