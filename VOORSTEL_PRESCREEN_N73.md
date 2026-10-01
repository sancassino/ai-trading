# VOORSTEL_PRESCREEN_N73 — USDCAD long-only L60/H10 medium-term (D-100 family B)

**Status:** **OPEN** — awaiting D-092.1 (**D-094** track 4 + **D-100 family B** + **D-097** medium-term; filed 2026-10-01 ~12:15 CEST; replace N69–N71 DIAG_FAIL).  
**Auteur:** Strateeg (Claude).  
**Instrument:** `USDCAD` (RT **0,80 bp** — COSTS_FTMO; swap_long **−0,09** bp/nacht = earn).  
**Track 4 + D-100 family B:** FX medium-term TSMOM on cheap overnight long side. Hold 10 handelsdagen.

**Gate (long-only; D-100 zeros swap-credit):**  
0,80 + 9 × max(−0,09, 0) = **0,80 bp** → gate 3 × 0,80 = **2,40 bp**.  
Alfa = bruto prijs.

**D-094a:** proxy `data/daily/FX_USDCAD.csv` (≥10j). Reden **(b)**. Train **2000–2016** / test **2017–2024**; reserve 2025+ onaangeroerd.

**Onderscheid:**
- ≠ **S2 USDCAD_LONG_TSMOM** cycle_1140 FAIL (L20-achtig / gate 50; dit = **L60/H10** medium, gate 2,40)
- ≠ **USDJPY_MED** / **N72 EURJPY** (andere paren)
- ≠ **N33** USDCAD Lon→NY intradag FAIL
- ≠ **N69–N71** DIAG_FAIL / FX_EUR_SHORT / family A

## Regel
- `ret60 = close_t / close_{t−60} − 1`
- `ret60 > 0` → **LONG** next close; else flat
- Hold: exit close_{t+10}. **Non-overlapping**. Alleen LONG.

## Pre-screen
- Data: `data/daily/FX_USDCAD.csv`, train **2000-01-01 … 2016-12-31**.
- Gate: mean bruto prijs ≥ **2,40 bp**, N ≥ 150.
- PASS → PREREG_FTMO_N73. FAIL → STOP (geen L20-retune, geen oil-correlation filter).
