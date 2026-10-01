# VOORSTEL_PRESCREEN_N39 — BTCUSD Asia→Europe Handoff Continuation

**Status:** **FAIL — geen PREREG** — Strateeg `n38_n40_prescreen` (N=132≪150, mean **−3,43** < 3,75). FAIL-set; geen S2-BTC parent-wijziging.
**Auteur:** Strateeg (Grok).  
**Instrument:** `BTCUSD` (RT ≈ **1,25 bp** uit COSTS_FTMO_alle / S2-BTC → gate **3,75 bp** = 3×RT).  
**Track 2:** crypto — Asia-sessie (00:00–08:00 CET) impuls continueren in Europe-ochtend (08:00→12:00).  
**Grond:** 24/7 crypto: Asia risk-on/off zet vaak EU-ochtendrichting; distinct van S2-BTC US-open filter. Swap 0 (intradag).

**D-094a:** train 2021–2023. Reden **(b)**: crypto session-handoff; FTMO-M5 = kosten. (Niet S2-BTC parent wijzigen.)

**Onderscheid:** ≠ S2-BTC US-open + US100-gap (andere sessie/filter); ≠ S2b BTC+ETH pool (STOP); ≠ Q3 crypto ML; ≠ N31 XAU Asia→Lon (metaal).

## Regel
- asia_bp = 1e4×(C_0800−C_0000)/C_0000; |asia|≥80 → side=sign; entry 08:00 close; stop 1×ATR14; flat **12:00 CET**.

## Pre-screen
- Data: `BTCUSD` m5gz train 2021–2023. Gate ≥ **3,75 bp**, N≥150. PASS → PREREG_FTMO_N39.
