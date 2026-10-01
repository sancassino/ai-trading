# VOORSTEL_PRESCREEN_N77 — FX majors vol-timed XS rank-reversal 5d (NEW_FAMILY C; D-100)

**Status:** **OPEN** — awaiting D-092.1 (**C-028 Lane-B** + **D-094** track 4 + **D-097** XS swing 5d + **D-100** swap in gate; filed 2026-10-01 ~12:40 CEST).  
**Auteur:** Strateeg (Grok).  
**Instrumenten (pool 6, alle in COSTS_FTMO + m5gz):** `EURUSD`, `GBPUSD`, `USDJPY`, `AUDUSD`, `USDCAD`, `USDCHF`.  
**NEW_FAMILY C:** cross-sectional **volatility-timed rank-reversal** on small liquid FX basket — ≠ TSMOM_DIV 12-1 monthly, ≠ N26/N30 XS index/intradag, ≠ L60 FX-med pair-forks.

**Track 4 + D-100:** hold 5 handelsdagen (**4 nachten**); long bottom-1 + short top-1 equal notional. Swap **in gate** (worst-case overnight among pool); no swap-credits as alfa.

**Kosten / gate (worst-case pair in pool):**  
RT_pair max = AUDUSD **1,22** + USDCHF **1,01** = **2,23** bp.  
Swap/nacht worst = max(swap_long pool paying) + max(swap_short pool paying) = EURUSD long **1,13** + USDCHF short **2,17** = **3,30** bp/nacht.  
4 nachten × 3,30 = **13,20** → cost = 2,23 + 13,20 = **15,43** bp → gate 3 × 15,43 = **46,29** bp.

**D-094a:** train 2021–2023. Reden **(c)**: multi-asset XS pool ≥5 with shared short-horizon reversal + vol-timing mechanism; Jegadeesh-style XS + vol-regime literature; FTMO-M5 costs on active legs. Herhaal in PREREG.

**D-100 swap note:** `swap_side_map` majors mixed (USDJPY/USDCAD/USDCHF long often cheapest solo). This sleeve is **LS pair** every trade — gate uses **worst-case** overnight, not best-side cherry-pick. Intradag-flat not used (5d hold).

**Onderscheid:**
- ≠ **TSMOM_DIV** dead (12-1 multi-asset monthly TSMOM; this = 5d **reversal** + vol gate)
- ≠ **N26** XS 1d index+XAU intradag sync FAIL; ≠ **N30** XS 5d **momentum** FAIL (this = **reversal** + vol-timed)
- ≠ **N57** FX basket **TSMOM** FAIL; ≠ **B1** month TSMOM STOP
- ≠ **N72–N74 / USDJPY_MED** single-pair L60/H10 (C-028: no more L60 FX longs)
- ≠ IDX_SHORT / ENERGY / plain ORB

## Regel
1. Elke dag t met flat book: for each pool symbol, `ret5 = close_t / close_{t−5} − 1` (dagclose ≤22:00 CET).
2. **Vol-timing gate:** `disp_t = stdev({ret5_i})` across the 6 names. Trade only if `disp_t > median(disp_{t−60…t−1})` (need ≥60 prior days). Else skip.
3. `long_sym` = argmin(ret5); `short_sym` = argmax(ret5); if tie → skip.
4. Entry next close: +1 long_sym, −1 short_sym (equal €-notional).
5. Exit close_{t+5}. **Non-overlapping**. Combined bruto bp = 0,5 × (long_leg_bp + short_leg_bp).
6. Geen ATR stops in pre-screen.

## Pre-screen
- Data: `data/m5gz/{EURUSD,GBPUSD,USDJPY,AUDUSD,USDCAD,USDCHF}.csv.gz` → dagclose; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **46,29** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N77. FAIL → STOP (geen dispersion-quantile grid, geen index-basket switch, geen L60 solo fork).
