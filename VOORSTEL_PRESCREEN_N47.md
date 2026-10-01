# VOORSTEL_PRESCREEN_N47 — USDCHF Asia→London Handoff Continuation

**Status:** **OPEN** — awaiting cost pre-screen (**D-094** track 2; replace N36 FAIL_T; filed 2026-10-01 ~09:26).  
**Auteur:** Strateeg (Grok).  
**Instrument:** `USDCHF` (RT **1,01 bp** → gate **3,03 bp**).  
**Track 2:** FX major — Asia-sessie impuls continueren in vroege London (vóór Lon midday). Swap 0.

**D-094a:** train 2021–2023. Reden **(b)**: FX Asia→London handoff microstructure (BIS session volumes); FTMO-M5 = kosten.

**Onderscheid:**
- ≠ **S2-USDJPY** Tokyo-**range** London-handoff STOP (ander paar; range-BO vs continuous Asia mom)
- ≠ **N31** XAU Asia→Lon FAIL; ≠ **N39/N45** crypto Asia handoff
- ≠ **N38/N42** Lon morning mom (andere paren + start 08:00 zonder Asia-signaal)
- ≠ **S2-GBPJPY** FAIL_T; ≠ **N35** EU→US index FAIL_T; ≠ ORB


- ≠ **N40** GER mid-morn FAIL_T; ≠ **N41** EU→US index FAIL_T

## Regel
- `asia_bp = 1e4×(C_0800−C_0000)/C_0000`
- `|asia| ≥ 35` → side=sign; entry 08:00 close; stop 1×ATR14; flat **11:30 CET**
- Max 1/dag; swap 0

## Pre-screen
- Data: `data/m5gz/USDCHF.csv.gz`, train 2021–2023. Gate ≥ **3,03 bp**, N≥150.
- PASS → PREREG_FTMO_N47. FAIL → STOP.
