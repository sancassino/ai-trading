# VOORSTEL_PRESCREEN_N88 — EURGBP 5d Short-Only TSMOM (D-100 family M; NEW_FAMILY M)

**Status:** **geen PREREG — D-092.1 pre-FAIL** — U2 informal `d17573c` (N=107≪150, mean −5,76 < 3,12); no trial (2026-10-01 ~17:50 CEST).  
**Auteur:** Strateeg (Claude). **NEW_FAMILY M** (EURGBP cross — nooit eerder geprobeerd).  
**Instrument:** `EURGBP` (RT **1,04 bp** — COSTS_FTMO; swap_short **−0,07** bp/nacht = ontvangen).  
**Track 4 + D-100 family B:** EUR/GBP cross short-only 5d swing. Short = structurele EUR-zwakte vs GBP. Overnight short EURGBP = earn 0,07 bp/nacht (positieve carry bij short).

**Gate (short-only; 4 nachten; swap earn → 0 in gate per D-100):**  
1,04 + 4 × max(−0,07, 0) = 1,04 + 0 = **1,04 bp** → gate 3 × 1,04 = **3,12 bp**.  
(Swap-credit telt NIET als alfa per D-100; alleen RT in gate.)

**D-094a:** train 2021–2023. Reden **(b)**: EUR vs GBP relatieve zwakte post-Brexit (UK current-account deficit kleiner dan EU structureel; BIS FX TSMOM op EUR/GBP cross). FTMO-M5 = kosten. Herhaal in PREREG.

**Onderscheid:**
- ≠ **FX_EUR_SHORT_TSMOM** FAIL_T (EURUSD + EURAUD; ander paar + andere cross; N66 subsumed)
- ≠ **N28** EURJPY Lon→NY FAIL (intradag FX momentum; dit = 5d swing EURGBP)
- ≠ **N71** GBPUSD short OPEN (GBPUSD ≠ EURGBP cross; ander paar)
- ≠ **N46** EURGBP Lon-fix fade BARRED (intradag fade; dit = 5d TSMOM)
- ≠ enig L60 FX-med (BARRED)

## Regel
- `ret5 = close_t / close_{t−5} − 1` (dagclose uit M5; laatste bar ≤22:00 CET)
- `ret5 < 0` → **SHORT** op close_t (negatief 5d momentum)
- `ret5 > 0` → skip (geen long-been; structureel asymmetrisch)
- Hold: exit close_{t+5}. **Non-overlapping**. Alleen SHORT.

## Pre-screen
- Data: `data/m5gz/EURGBP.csv.gz` → dagclose, train **2021-01-01 … 2023-12-31**.
- Gate: mean bruto ≥ **3,12 bp**, N ≥ 150.
- PASS → PREREG_FTMO_N88. FAIL → STOP (geen ret10-switch, geen EURCHF-add).
