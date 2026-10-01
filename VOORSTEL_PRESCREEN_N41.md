# VOORSTEL_PRESCREEN_N41 — US30cash Europe→US Open Continuation

**Status:** **PASS → PREREG_FTMO_N41 landed** — Strateeg `n41_n43_prescreen` (N=160, +8,65≥1,35). Formele gate volgt U2.
**Auteur:** Strateeg (Grok).  
**Instrument:** `US30cash` (RT **0,45 bp** → gate **1,35 bp**).  
**Track 2:** index — Europe-hours trend on US30 (09:00–15:00 CET) continues into first US hour (15:30–17:00).  
**Grond:** Same handoff-microstructure as N35 US100 but **distinct instrument** (Dow industrials vs Nasdaq). Swap 0.

**D-094a:** train 2021–2023. Reden **(b)**: index session-handoff; FTMO-M5 = kosten.

**Onderscheid:** ≠ N35 US100 (ander instrument — parallel ok, geen kloon van dode sleeve); ≠ N20 US30 PM cont FAIL; ≠ N32 IB breakout FAIL; ≠ ORB/LUNCH_OPEN.

## Regel
- eu_bp = 1e4×(C_1500−C_0900)/C_0900; |eu|≥40 → side=sign; entry 15:30; stop 1×ATR14; flat **17:00 CET**.

## Pre-screen
- Data: `US30cash` m5gz train 2021–2023. Gate ≥ **1,35 bp**, N≥150. PASS → PREREG_FTMO_N41.
