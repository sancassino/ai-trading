# VOORSTEL_PRESCREEN_N76 — UKOIL Mon→Thu inventory-window long (NEW_FAMILY B; D-100)

**Status:** **OPEN** — awaiting D-092.1 (**C-028 Lane-B** + **D-094** track 2/4 + **D-097** commodities short-hold + **D-100** cheap long; filed 2026-10-01 ~12:40 CEST).  
**Auteur:** Strateeg (Grok).  
**Instrument:** `UKOILcash` (RT **2,71** bp — COSTS_FTMO; swap_long **−5,98** / short **+27,03**).  
**NEW_FAMILY B:** commodity **inventory-window / weekly calendar** — ≠ ENERGY L20 TSMOM, ≠ N54 winter-season month-bias, ≠ intradag ORB.

**Track 2+4 + D-100:** overnight **long-only** (cheapest side: long swap is earn → swap-cost in gate = 0; short is SWAP_HOSTILE +27 bp/nacht).  
Hold Mon close → Thu close = **3 nachten**. Alfa = bruto prijs (geen swap-credit).

**Gate (D-100 zeros swap-credit):**  
2,71 + 3 × max(−5,98, 0) = **2,71** bp → 3 × 2,71 = **8,13** bp.  
D-097 commodities prefer large bruto: binding screen gate = **max(50, 8,13) = 50,00** bp (same floor as N49/N54 energy screens).

**D-094a:** train 2021–2023. Reden **(b)**: weekly petroleum inventory cycle (API/EIA mid-week prints; refinery/runs calendar) — mechanism distinct from momentum; FTMO-M5 for costs. Optional long proxy `data/daily/BRENT_F.csv` ≥5y for mechanisme; execution = UKOILcash M5. Herhaal in PREREG.

**D-100 swap note:** `swap_side_map` UKOIL best_side=**long** (+8,55 bp/dag credit). We **do not** count that credit as alfa; gate uses max(swap_long,0)=0. Short side barred.

**Onderscheid:**
- ≠ **ENERGY_TSMOM / N49 / N50 / N59** L20/H10 TSMOM FAIL/BARRED
- ≠ **N54** winter Nov–Mar month-bias underpowered (this = **weekly Mon→Thu** inventory window, all months)
- ≠ **N22 / N43** UKOIL intradag FAIL/underpowered
- ≠ **N72–N74** L60 FX (C-028 freeze further FX-med forks)
- ≠ plain ORB

## Regel
1. Kalender: entry alleen op **Monday** D1 close (CET week; skip if no Monday bar).
2. **LONG** UKOILcash at Monday close.
3. Exit **Thursday** D1 close same week (3 nachten). If Thursday missing → exit next available ≤ Friday close; still count as one trade.
4. **Non-overlapping** (one position per week max). Long-only; no short.
5. Geen TSMOM/ATR filter in pre-screen (calendar-only — prevents ENERGY-clone retune).

## Pre-screen
- Data: `data/m5gz/UKOILcash.csv.gz` → dagclose; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **50,00** bp, **N ≥ 150** (≈3y × ~52 weeks → N≈150 target; if N<150 with mean≥50 → underpowered, no PREREG).
- PASS → PREREG_FTMO_N76. FAIL → STOP (geen L20-add, geen USOIL twin, geen winter-month merge with N54).
