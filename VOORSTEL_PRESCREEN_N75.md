# VOORSTEL_PRESCREEN_N75 — XAU/XAG ratio mean-reversion 3d (NEW_FAMILY A; D-100)

**Status:** **DIAG_FAIL** — CTO C-029 Lane-B diag (mean 10,86 ≪ gate 30,60; N=71). Geen PREREG. Drop pad (2026-10-01 ~13:15 CEST).
**Auteur:** Strateeg (Grok).  
**Instrumenten:** `XAUUSD` + `XAGUSD` (pair legs; COSTS_FTMO RT **0,83** + **5,07** = **5,90** bp).  
**NEW_FAMILY A:** metal **ratio / pairs** MR (EOD 3d) — ≠ solo XAU/XAG TSMOM, ≠ L60 FX-med, ≠ ENERGY, ≠ intradag ORB.

**Track 4 + D-100:** overnight **only** on cheapest net swap side for the pair.  
From COSTS: XAU swap_long **2,15** / short **0,10**; XAG long **3,15** / short **−0,18**.  
Net 2 nachten: long-XAU/short-XAG = 2×(2,15+0) = **4,30** bp; short-XAU/long-XAG = 2×(0,10+3,15) = **6,50** bp.  
→ **Allowed overnight side = long XAU / short XAG** (cheaper). Swap-earn never counts as alfa.

**Gate (D-100 zeros swap-credit):**  
5,90 + 4,30 = **10,20** bp → gate 3 × 10,20 = **30,60** bp.  
Alfa-maatstaf = signed mean bruto **prijs**rendement op equal-notional pair (geen swap-credit).

**D-094a:** train 2021–2023. Reden **(b)**: gold/silver ratio mean-reversion literatuur (LBMA/COMEX relative value; FTMO-M5 voor uitvoering/kosten). Herhaal in PREREG. Proxy `data/daily` XAU/XAG of m5gz dagclose.

**D-100 swap note:** `results/ceo/swap_side_map.csv` (CEO): XAU best_side≈short credit-hostile long; XAG best≈short. Pair-regel locked to **long gold / short silver** only when ratio signal agrees — no hostile short-gold/long-silver overnight.

**Onderscheid:**
- ≠ **N60/N65** XAG solo TSMOM FAIL; ≠ **N70** XAU 5d bi-dir DIAG_FAIL
- ≠ **N36/N7/N8** XAU intradag FAIL / watch
- ≠ **ENERGY / N49 / N59** oil TSMOM
- ≠ **N72–N74 / USDJPY_MED** L60 FX-med (C-028: no more L60 FX forks)
- ≠ plain ORB / intradag (this = 3d EOD pair)

## Regel
1. `R_t = close_XAU_t / close_XAG_t` (dagclose ≤22:00 CET uit M5).
2. `z_t = (ln R_t − mean_{20}(ln R)) / std_{20}(ln R)` (min 20 prior days).
3. Signal: `z_t < −1,0` → **LONG XAU + SHORT XAG** next close (ratio depressed → expect reversion up in ratio). Else flat.  
   (No trades on `z > +1` — that side is swap-hostile per D-100.)
4. Hold: exit close_{t+3} (3 handelsdagen, **2 nachten**). **Non-overlapping**.
5. PnL bruto bp = 0,5 × (XAU_long_bp + XAG_short_bp) equal €-notional; consistent in screen + PREREG.

## Pre-screen
- Data: `data/m5gz/XAUUSD.csv.gz` + `data/m5gz/XAGUSD.csv.gz` → dagclose; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **30,60** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N75 (Lane-B only after PASS). FAIL → STOP (geen z-grid, geen bilateral hostile side, geen XAU-solo fallback).
