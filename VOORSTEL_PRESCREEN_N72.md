# VOORSTEL_PRESCREEN_N72 — EURJPY long-only L60/H10 medium-term (D-100 family B)

**Status:** **OPEN** — awaiting D-092.1 (**D-094** track 4 + **D-100 family B** + **D-097** medium-term; filed 2026-10-01 ~12:15 CEST; replace N69–N71 DIAG_FAIL).  
**Auteur:** Strateeg (Claude).  
**Instrument:** `EURJPY` (RT **1,10 bp** — COSTS_FTMO; swap_long **−0,11** bp/nacht = earn).  
**Track 4 + D-100 family B:** FX medium-term TSMOM on cheap overnight long side (parallel to CTO USDJPY_MED, **solo EURJPY**). Hold 10 handelsdagen (9 nachten).

**Gate (long-only; D-100 zeros swap-credit):**  
1,10 + 9 × max(−0,11, 0) = **1,10 bp** → gate 3 × 1,10 = **3,30 bp**.  
Alfa-maatstaf = bruto prijsrendement (geen swap-credit als alfa).

**D-094a:** proxy `data/daily/EURJPY.csv` (≥10j). Reden **(b)**: FX TSMOM literatuur; FTMO-M5/COSTS voor uitvoering. Train proxy **2000–2016** / test **2017–2024** (reserve 2025+ onaangeroerd). Herhaal in PREREG.

**Onderscheid:**
- ≠ **USDJPY_MED** (CTO C-026; ander paar; geen EURJPY-add in die v1)
- ≠ **N28** EURJPY Lon→NY intradag FAIL
- ≠ **N67** USDJPY L20 DIAG_FAIL / **FX_EUR_SHORT** FAIL_T
- ≠ **N69–N71** DIAG_FAIL / family A / ENERGY / ORB

## Regel
- `ret60 = close_t / close_{t−60} − 1` (dagclose)
- `ret60 > 0` → **LONG** next close; else flat
- Hold: exit close_{t+10}. **Non-overlapping**. Alleen LONG.

## Pre-screen
- Data: `data/daily/EURJPY.csv` (of FX proxy equivalent), train **2000-01-01 … 2016-12-31**.
- Gate: mean bruto prijs ≥ **3,30 bp**, N ≥ 150.
- PASS → PREREG_FTMO_N72. FAIL → STOP (geen L20-retune, geen USDJPY-add).
