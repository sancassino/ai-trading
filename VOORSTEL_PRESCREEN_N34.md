# VOORSTEL_PRESCREEN_N34 — XAUUSD Post-AM-Fix Mean-Reversion to London Open

**Status:** **geen PREREG — D-092.1 FAIL** (Strateeg screen 2026-10-01 08:26; N=148≪150, mean **−2,71** < 2,49 bp). Artifacts `results/R2/n32_n34_prescreen/`.  
**Auteur:** Strateeg (Grok).  
**Instrument:** `XAUUSD` (RT **0,83 bp** → gate **2,49 bp**).  
**Track 2:** metaal — **na** AM-fix (~13:00 CET) fade terug naar London-open; ≠ N8 Post-AM-Fix **continuation**; ≠ AM_FADE (eerder venster).  
**Grond:** Na LBMA AM-fix unwindt een deel van de ochtendextensie richting London-open vóór NY. Entry 13:00, flat 15:00 (vóór NY). Swap 0.

**D-094a:** train 2021–2023. Reden **(b)**: gold fix inventory effects; proxy GC.

**Onderscheid:** ≠ S2-XAU_AM_FADE / N10 (pre-fix); ≠ N8 continuation; ≠ N25 NY-PM; ≠ N31 Asia→Lon cont; ≠ N4/N7/N12/N19.

## Regel
- P_lon = C_0800; P_1300 = C_1300; dev = 1e4×(P_1300−P_lon)/P_lon.  
- |dev|≥40 → fade (short if +); stop 1×ATR14; flat **15:00 CET**.

## Pre-screen
- Data: `XAUUSD` m5gz train 2021–2023. Gate ≥ **2,49 bp**, N≥150. PASS → PREREG_FTMO_N34.
