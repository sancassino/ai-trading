# VOORSTEL_PRESCREEN_N79 — Rate-curve steepener → UKOIL LO 5d (NEW_FAMILY D; D-097/D-100)

**Status:** **OPEN** — awaiting D-092.1 (**D-094** + **C-028** replace cycle after N78 FAIL_COST_GATE; filed 2026-10-01 ~12:55 CEST).  
**Auteur:** Strateeg (Grok).  
**Instrument:** `UKOILcash` (RT **2,71** bp; swap_long **−5,98** / short **+27,03**).  
**Signal data:** `data/daily/YLD_US10Y.csv` + `YLD_US2Y.csv` (US Treasury par yields).  
**NEW_FAMILY D:** **macro rate-curve → commodity** — ≠ C45 curve→equity, ≠ ENERGY L20 TSMOM, ≠ N76 Mon→Thu inventory calendar, ≠ VIX_TERM_VOV.

**Track 4 + D-100:** overnight **long-only** (cheapest side; long swap earn → swap-cost in gate = 0; short SWAP_HOSTILE barred). Hold 5 handelsdagen = **4 nachten**. Alfa = bruto prijs (geen swap-credit).

**Gate (D-100 zeros swap-credit + D-097 commodity floor):**  
2,71 + 4 × max(−5,98, 0) = **2,71** bp → 3 × 2,71 = **8,13** bp.  
Binding screen gate = **max(50, 8,13) = 50,00** bp.

**D-094a:** train 2021–2023. Reden **(b)**: yield-curve / growth-impulse → oil demand literature (Estrella–Mishkin style curve as cycle signal; target = energy CFD not equity index — distinct from archived C45→SPX). FTMO-M5 = kosten/uitvoering; curve series = public Treasury. Herhaal in PREREG.

**D-100 swap note:** UKOIL best_side≈long. Credit **not** alfa; gate uses max(swap_long,0)=0.

**Onderscheid:**
- ≠ **C45 / rente-curve→equity** (andere target: UKOIL not US100/SPX)
- ≠ **ENERGY_TSMOM / N49 / N50 / N59** price TSMOM FAIL/BARRED (dit = **curve signal**, geen ret20)
- ≠ **N76** Mon→Thu inventory calendar (dit = **macro curve**, any weekday entry)
- ≠ **N78 VIX_TERM_VOV** dead (geen VIX; geen US100 overnight long)
- ≠ **N75** metal ratio; ≠ **N77** FX XS; ≠ L60 FX-med; ≠ ORB / IDX_SHORT

## Regel
1. `curve_t = YLD_US10Y_t − YLD_US2Y_t` (aligned to UKOIL D1 close calendar; forward-fill ≤3d if yield holiday).
2. `Δcurve_5 = curve_t − curve_{t−5}`.
3. Signal: `Δcurve_5 > 0` **and** `curve_t > 0` (steepening in positive territory) → **LONG** UKOILcash next D1 close. Else flat.
4. Hold: exit close_{t+5} (**4 nachten**). **Non-overlapping**.
5. Long-only; no short; no TSMOM/ATR overlay in pre-screen.

## Pre-screen
- Data: `data/m5gz/UKOILcash.csv.gz` → dagclose + `data/daily/YLD_US10Y.csv` + `YLD_US2Y.csv`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **50,00** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N79. FAIL → STOP (geen curve-window grid, geen USOIL twin, geen equity-target fallback, geen softer gate).
