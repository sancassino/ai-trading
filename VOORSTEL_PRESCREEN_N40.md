# VOORSTEL_PRESCREEN_N40 — GER40cash Mid-Morning Momentum Continuation

**Status:** **PASS → PREREG_FTMO_N40 landed** — Strateeg `n38_n40_prescreen` (N=205, +2,43≥2,16; median −2,28 caveat). Formele gate volgt U2.
**Auteur:** Strateeg (Grok).  
**Instrument:** `GER40cash` (RT **0,72 bp** → gate **2,16 bp**).  
**Track 2:** EU-index — post-XETRA open momentum (09:30→12:00) continueren tot 14:00 (vóór US-open sync).  
**Grond:** Na opening-noise (eerste 30 min) zet DAX vaak een mid-morning trend die tot early afternoon doorloopt. Swap 0.

**D-094a:** train 2021–2023. Reden **(b)**: index mid-session continuation; proxy FDAX; FTMO-M5 = kosten.

**Onderscheid:** ≠ N9 GER40 ochtend-fade (FAIL underpowered); ≠ N11 XETRA ORB FAIL_T; ≠ N13 US-Open Sync FAIL; ≠ N21 afternoon deviation fade FAIL; ≠ S2-GER40_OPEN / GER_US_LEAD STOP; ≠ simple ORB-family (N15–17 barred).

## Regel
- mom_bp = 1e4×(C_1200−C_0930)/C_0930; |mom|≥40 → side=sign; entry 12:00 close; stop 1×ATR14; flat **14:00 CET**.

## Pre-screen
- Data: `GER40cash` m5gz train 2021–2023. Gate ≥ **2,16 bp**, N≥150. PASS → PREREG_FTMO_N40.
