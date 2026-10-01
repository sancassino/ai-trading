# VOORSTEL_PRESCREEN_N71 — GBPUSD 10d TSMOM Short-Only (D-100 family B carry)

**Status:** **DIAG_FAIL** — CTO C-026 (train +3,8 < gate ~11; N≈107). Geen PREREG; geen EURUSD-switch.  
**Auteur:** Strateeg (Claude).  
**Instrument:** `GBPUSD` (RT **0,70 bp** — COSTS_FTMO; swap_short **0,30** bp/nacht).  
**Track 4 + D-100 family B:** FX carry+ short-only — GBPUSD short is carry-neutraal (swap_short 0,30 = betaal, maar laag). TSMOM-signaal L20 filter negatief. Hold 10 handelsdagen (9 nachten). Overnight goedkoopste kant met negatief momentum = **short**.

**Gate (short-only; worst-case = short-pays; 9 nachten × 0,30 bp):**  
0,70 + 9 × 0,30 = **3,40 bp** → gate 3 × 3,40 = **10,20 bp**.  
(Swap-kost WEL in poort; geen swap-credit als alfa per D-100.)

**D-094a:** train 2021–2023. Reden **(b)**: GBP negatief momentum historisch (BIS; post-Brexit structureel current-account deficit; FTMO-M5 kosten). Herhaal in PREREG.

**Onderscheid:**
- ≠ **N29** GBPUSD midday fade FAIL (intradag 12:00→15:00; dit = 10d swing short)
- ≠ **GBPJPY_EU_MOM** FAIL_T (ander paar + EU morning intradag mom)
- ≠ **N67** USDJPY DIAG_FAIL (ander paar)
- ≠ **TSMOM_DIV** dead (multi-asset maandelijks)
- ≠ **B1** FX maand-TSMOM STOP (~20+ nachten)
- ≠ enig ORB / intradag / energie

## Regel
- `ret20 = close_t / close_{t−20} − 1` (dagclose uit M5; laatste bar ≤22:00 CET)
- `ret20 < 0` → **SHORT** op close_t (negatief TSMOM)
- `ret10 < 0` (close_{t} vs _{t−10}) → bevestig; anders skip
- Hold: exit close_{t+10} (10 handelsdagen). **Non-overlapping**.
- Alleen SHORT.

## Pre-screen
- Data: `data/m5gz/GBPUSD.csv.gz` → dagclose, train **2021-01-01 … 2023-12-31**.
- Gate: mean bruto ≥ **10,20 bp**, N ≥ 150.
- PASS → PREREG_FTMO_N71. FAIL → STOP (geen lookback-grid, geen EURUSD-switch).
