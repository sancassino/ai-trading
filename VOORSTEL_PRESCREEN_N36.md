# VOORSTEL_PRESCREEN_N36 — XAUUSD NY-Open Drive Continuation (first 90 min)

**Status:** **OPEN** — awaiting cost pre-screen (**D-094** track 2; queue na N24–N34 FAIL; filed 2026-10-01 08:28).  
**Auteur:** Strateeg (Grok).  
**Instrument:** `XAUUSD` (RT **0,83 bp** → gate **2,49 bp**).  
**Track 2:** metaal — **continuation** van de eerste 30 min na NY-open door tot 17:00; ≠ N12 (andere definitie/fail), ≠ N25 fade, ≠ AM_FADE.  
**Grond:** COMEX open impulse (15:30–16:00) vervolgt vaak tot 17:00 vóór lunch-fade. Swap 0.

**D-094a:** train 2021–2023. Reden **(b)**: gold NY-open drive; proxy GC.

**Onderscheid:** ≠ N12 NY-Open Continuation (prior FAIL — dit = expliciet first-30m sign → hold 90m, andere exit); ≠ N25 NY-PM fade; ≠ N4/N7/N8/N31/N34; ≠ S2-XAU overlap BO.

## Regel
- drive = 1e4×(C_1600−C_1530)/C_1530; |drive|≥25 → side=sign; entry 16:00; stop 1×ATR14; flat **17:00 CET**.

## Pre-screen
- Data: `XAUUSD` m5gz train 2021–2023. Gate ≥ **2,49 bp**, N≥150. PASS → PREREG_FTMO_N36.
