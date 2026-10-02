# VOORSTEL_PRESCREEN_N94 — NZDJPY Long-Only 5d Carry+Momentum (D-100 family B; NEW_FAMILY S)

**Status:** **DIAG_FAIL** — CTO C-032 Lane-B diag 2026-10-02 ~21:05 CEST (0 trials; no PREREG).  
**Auteur:** Strateeg (Grok). **NEW_FAMILY S** (NZDJPY NZD/JPY commodity-yen carry+momentum long-only — nooit eerder geprobeerd).  
**Instrument:** `NZDJPY` (RT **2,00 bp** — `COSTS_FTMO_alle`; swap_long ≈ **+0,30 %/jr** = earn bij long).  
**Track 4 + D-100 family B:** NZDJPY long-only 5d swing. Long = structurele NZD carry vs JPY (RBNZ policy rate >> BoJ near-zero; NZD = commodity currency — Chen & Rogoff 2003) + positief 5d momentum. Overnight long NZDJPY = positieve carry.

**Gate (long-only; 4 nachten; swap earn → 0 in gate per D-100):**  
2,00 + 4 × max(swap_long_cost, 0) = 2,00 + 0 = **2,00 bp** → gate 3 × 2,00 = **6,00 bp**.  
(Swap-credit telt NIET als alfa per D-100; alleen RT in gate. Bruto = signed prijsrendement.)

**D-094a:** train 2021–2023. Reden **(b)**: FX carry + TSMOM op commodity-yen cross (Menkhoff et al. 2012 FX TSMOM; Burnside et al. 2011 carry; NZD/JPY = hoog-vol carry-cross met persistentie bij positief momentum; FTMO-M5 = kosten). Herhaal in PREREG.

**Onderscheid:**
- ≠ **N90** GBPJPY LO 5d carry+mom UNDERPOWERED (GBP≠NZD; BoE≠RBNZ; ander cross + ander carry-regime)
- ≠ **N91** AUDUSD LO 5d DIAG_FAIL (AUD/USD ≠ NZD/JPY; USD-leg ≠ JPY-leg)
- ≠ **N62** GBPJPY LO 20→10 FAIL (ander lookback; GBPJPY ≠ NZDJPY)
- ≠ **L60 FX-med** BARRED (USDJPY_MED/EURJPY_MED; dit = NZDJPY + long-only carry 5d)
- ≠ **FX_EUR_SHORT** FAIL_T / **N88** EURGBP SO / **N58** AUDJPY LO FAIL
- ≠ enig intradag / gap-fade / equity-index / metals / VIX_TERM / ORB / UKOIL-OVN / CORN / N92 NY-2h

## Regel
- `ret5 = close_t / close_{t−5} − 1` (dagclose uit M5; laatste bar ≤22:00 CET)
- `ret5 > 0` → **LONG** op close_t (positief 5d momentum = carry-richting)
- `ret5 ≤ 0` → skip (geen short-been; short-side swap-kosten structureel hoog op NZDJPY)
- Hold: exit close_{t+5}. **Non-overlapping**. Alleen LONG.

## Pre-screen
- Data: `data/m5gz/NZDJPY.csv.gz` → dagclose, train **2021-01-01 … 2023-12-31**.
- Gate: mean bruto ≥ **6,00 bp**, N ≥ 150.
- PASS → PREREG_FTMO_N94. FAIL → STOP (geen ret10-switch, geen AUDJPY-add, geen soft gate).
