# VOORSTEL_PRESCREEN_N74 — USDCHF long-only L60/H10 medium-term (D-100 family B)

**Status:** **BARRED/STOP** — C-028 closes the L60 FX-med family after USDJPY_MED **FAIL_T** (U2 `910d6ff`, TRIAL 454→455) and EURJPY_MED **FAIL_T** (U2 `65a9b23`, TRIAL 455→456); no more pair-forks. TRIAL_COUNT **456**.
**Auteur:** Strateeg (Claude).  
**Instrument:** `USDCHF` (RT **1,01 bp** — COSTS_FTMO; swap_long **−0,39** bp/nacht = earn).  
**Track 4 + D-100 family B:** FX medium-term TSMOM on cheap overnight long side (strongest FX long credit among majors in COSTS). Hold 10 handelsdagen.

**Gate (long-only; D-100 zeros swap-credit):**  
1,01 + 9 × max(−0,39, 0) = **1,01 bp** → gate 3 × 1,01 = **3,03 bp**.  
Alfa = bruto prijs (swap-earn nooit PASS-drager).

**D-094a:** proxy `data/daily/FX_USDCHF.csv` (≥10j). Reden **(b)**. Train **2000–2016** / test **2017–2024**; reserve 2025+ onaangeroerd.

**Onderscheid:**
- ≠ **S2 USDCHF_LONG_TSMOM** cycle_1140 FAIL (−3,32 vs gate 50; dit = **L60/H10**, gate 3,03)
- ≠ **N47** USDCHF Asia→Lon BARRED (intradag / C-021)
- ≠ **USDJPY_MED** / N72 / N73 (andere paren)
- ≠ **N69–N71** DIAG_FAIL / FX_EUR_SHORT / family A

## Regel
- `ret60 = close_t / close_{t−60} − 1`
- `ret60 > 0` → **LONG** next close; else flat
- Hold: exit close_{t+10}. **Non-overlapping**. Alleen LONG.

## Pre-screen
- Data: `data/daily/FX_USDCHF.csv`, train **2000-01-01 … 2016-12-31**.
- Gate: mean bruto prijs ≥ **3,03 bp**, N ≥ 150.
- PASS → PREREG_FTMO_N74. FAIL → STOP (geen L20-retune, geen EURCHF-add).
