# VOORSTEL_PRESCREEN_N38 — GBPUSD London Morning Momentum Continuation

**Status:** **FAIL — geen PREREG** — Strateeg `n38_n40_prescreen` (N=102≪150, mean **−1,35** < 2,10). FAIL-set; geen klonen.
**Auteur:** Strateeg (Grok).  
**Instrument:** `GBPUSD` (RT **0,70 bp** → gate **2,10 bp**).  
**Track 2:** FX major — London-ochtendimpuls (08:00→11:30) continueren tot 14:30, vóór Lon→NY handoff-familie.  
**Grond:** Session-momentum op GBPUSD is microstructure (positioning into midday); ≠ fade. Swap 0.

**D-094a:** train 2021–2023. Reden **(b)**: FX session-momentum tijdloos; FTMO-M5 = kosten.

**Onderscheid:** ≠ N29 GBPUSD midday fade (FAIL); ≠ S2 GBPJPY_EU_MOM (ander paar + andere exit/ATR-target); ≠ N28/N33 Lon→NY mom (entry 15:30); ≠ A5/GS02 London ORB; ≠ N37 EURUSD H4 TF FAIL.

## Regel
- ret_bp = 1e4×(O_1130−O_0800)/O_0800; |ret|≥30 → side=sign; entry 11:30 open; stop 0,5×ATR14; flat **14:30 CET**.

## Pre-screen
- Data: `GBPUSD` m5gz train 2021–2023. Gate ≥ **2,10 bp**, N≥150. Geen test/reserve. PASS → PREREG_FTMO_N38.
