# VOORSTEL_PRESCREEN_N42 — NZDUSD London Morning Momentum Continuation

**Status:** **FAIL — geen PREREG** — Strateeg `n41_n43_prescreen` (N=132≪150, mean **+0,31** < 5,55). FAIL-set.
**Auteur:** Strateeg (Grok).  
**Instrument:** `NZDUSD` (RT **1,85 bp** → gate **5,55 bp**).  
**Track 2:** FX — London-ochtendimpuls (08:00→11:30) continueren tot 14:30.  
**Grond:** NZD session-momentum; hoge vol t.o.v. majors; ≠ GBPUSD N38 FAIL. Swap 0.

**D-094a:** train 2021–2023. Reden **(b)**: FX session-momentum tijdloos; FTMO-M5 = kosten.

**Onderscheid:** ≠ N38 GBPUSD Lon mom FAIL; ≠ S2 GBPJPY_EU_MOM; ≠ N28/N33 Lon→NY; ≠ A5/GS02 ORB; ≠ N27 AUDUSD H4 MR FAIL.

## Regel
- ret_bp = 1e4×(O_1130−O_0800)/O_0800; |ret|≥35 → side=sign; entry 11:30 open; stop 0,5×ATR14; flat **14:30 CET**.

## Pre-screen
- Data: `NZDUSD` m5gz train 2021–2023. Gate ≥ **5,55 bp**, N≥150. PASS → PREREG_FTMO_N42.
