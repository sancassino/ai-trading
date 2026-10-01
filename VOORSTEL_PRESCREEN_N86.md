# VOORSTEL_PRESCREEN_N86 — XAU own RV-VoV → 3d gold MR (NEW_FAMILY K; D-097/D-100)

**Status:** **OPEN** — awaiting D-092.1 (**D-094** + Lane-B replace after N80 FAIL_COST_GATE; filed 2026-10-01 ~13:25 CEST).  
**Auteur:** Strateeg (Grok).  
**Instrument:** `XAUUSD` (RT **0,83** bp; swap_long **2,15** / swap_short **0,10** bp/nacht — `COSTS_FTMO.csv`).  
**NEW_FAMILY K:** **gold own realized vol-of-vol → multi-day mean-reversion** — ≠ N78 VIX_TERM_VOV (VIX9D/VIX3M → US100; **BARRED clones**), ≠ N70 XAU 5d TSMOM DIAG_FAIL, ≠ N75 XAU/XAG ratio DIAG_FAIL, ≠ XAU_AM_FADE intradag.

**Track 2 (commodities/metals swing) + D-100:** hold **3 handelsdagen** (**2 nachten**); bilateral fade. Swap **in gate** (worst-case = long-pays). No swap-credits as alfa. **Not** a VIX-term structure sleeve.

**Kosten / gate (worst-case long):**  
RT **0,83** + 2 × swap_long **2,15** = **5,13** bp → gate 3 × 5,13 = **15,39** bp.

**D-094a:** train 2021–2023. Reden **(b)**: elevated **own-asset** vol-of-vol marks liquidity / positioning stress that mean-reverts in spot gold over a few sessions; literature on RV/VoV is asset-local, not VIX-equity spillover. Distinct from VIX futures term-structure → equity (N78 dead). FTMO-M5 XAU = uitvoering. Herhaal in PREREG.

**Onderscheid:**
- ≠ **N78 VIX_TERM_VOV** FAIL_COST_GATE / C-029 **bar** (VIX9D/VIX3M + VoV10 → **US100**; this = **XAU realized VoV → XAU** MR)
- ≠ **N70** XAUUSD 5d swing **TSMOM** DIAG_FAIL (momentum vs **MR**; no VoV gate)
- ≠ **N75** XAU/XAG ratio 3d DIAG_FAIL (pair; this = **solo gold**)
- ≠ **S2-XAU_AM_FADE** / N10 / N25 / N4 (intradag gold session fades/breakouts)
- ≠ **N60/N65** XAG swings; ≠ ENERGY / UKOIL OVN-gap (N80 dead) / L60 FX / ORB

## Regel
1. Daily close ≤ **22:00 CET**: `r_t = ln(C_t / C_{t−1})`.
2. `RV10_t = sqrt(sum_{i=0..9} r_{t−i}^2)` (10d realized vol).
3. `VoV10_t = stdev({RV10_{t−j} for j=0..9})` (vol-of-vol of RV10).
4. Trade only if `VoV10_t > median(VoV10_{t−60…t−1})` (need ≥60 prior days) **and** `|sum_{i=0..2} r_{t−i}| ≥ 0,008` (≈80 bp 3d move).
5. **Fade gold:** 3d sum ret > 0 → **SHORT** XAU; 3d sum ret < 0 → **LONG** XAU. Entry next close after signal day.
6. Exit close at **t+3**. **Non-overlapping**. Pre-screen: no ATR stop (report separately in formal).
7. Alfa = signed mean **bruto prijs** bp; swap only in gate, never as credit.

## Pre-screen
- Data: `data/m5gz/XAUUSD.csv.gz` → dagclose; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **15,39** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N86. FAIL → STOP (geen VoV-window grid, geen VIX substitute, geen US100 twin, geen softer gate, geen XAG twin).
