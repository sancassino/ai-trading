# VOORSTEL_PRESCREEN_N45 — ETHUSD Asia→Europe Handoff Continuation

**Status:** **OPEN** — awaiting cost pre-screen (**D-094** track 2 crypto; replace N43 FAIL; filed 2026-10-01 09:28).  
**Auteur:** Strateeg (Grok).  
**Instrument:** `ETHUSD` (RT aangenomen ≈ **1,25 bp** zoals BTC/S2 → gate **3,75 bp**; U2 bevestigt uit COSTS bij run).  
**Track 2:** crypto Asia→EU handoff; ≠ N39 BTC Asia FAIL; ≠ S2b pool STOP; ≠ S2-BTC US-open.

**D-094a:** train 2021–2023. Reden **(b)**.

**Onderscheid:** ≠ N39 BTCUSD Asia FAIL; ≠ S2b BTC+ETH STOP; ≠ S2-BTC US-open parent.

## Regel
- asia_bp = 1e4×(C_0800−C_0000)/C_0000; |asia|≥80 → side=sign; entry 08:00; stop 1×ATR14; flat **12:00 CET**.

## Pre-screen
- Gate ≥ **3,75 bp** (of 3× echte ETH RT), N≥150. PASS → PREREG_FTMO_N45.
