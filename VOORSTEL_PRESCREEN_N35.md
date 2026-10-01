# VOORSTEL_PRESCREEN_N35 — US100cash Europe-Session Momentum → US Open Continuation

**Status:** **PASS_may_PREREG** — D-092.1 PASS (U2 `43c395e`; mean +6,60 bp > 1,98 bp; N=214). PREREG_FTMO_N35 bevroren. (**D-094** track 2; queue na N24–N34 FAIL; filed 2026-10-01 08:28).  
**Auteur:** Strateeg (Grok).  
**Instrument:** `US100cash` (RT **0,66 bp** → gate **1,98 bp**).  
**Track 2:** index — Europe-hours trend on US100 cash (09:00–15:00 CET) continues into first US hour (15:30–17:00). ≠ ORB, ≠ N3 close-drive, ≠ N14 pre-market mom, ≠ N20/N23.  
**Grond:** US100 handelt liquid in Europa; EU-macro zet richting die NY-cash-open vaak vervolgt eerste 90 min. Swap 0.

**D-094a:** train 2021–2023. Reden **(b)**: index session-handoff microstructure (proxy NQ); FTMO-M5 = kosten.

**Onderscheid:** ≠ A1/N11/N15–17 ORB; ≠ N3 close-drive; ≠ N14 NY pre-market; ≠ N20 US30 PM cont; ≠ LUNCH_OPEN fade.

## Regel
- eu_bp = 1e4×(C_1500−C_0900)/C_0900; |eu|≥40 → side=sign; entry 15:30; stop 1×ATR14; flat **17:00 CET**.

## Pre-screen
- Data: `US100cash` m5gz train 2021–2023. Gate ≥ **1,98 bp**, N≥150. Geen test/reserve. PASS → PREREG_FTMO_N35.
