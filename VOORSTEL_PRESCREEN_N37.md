# VOORSTEL_PRESCREEN_N37 — EURUSD H4 Trend-Follow (SMA20 slope)

**Status:** **FAIL — geen PREREG** — U2 `43c395e` (N=627, mean **−0,17** < 1,89). FAIL-set; geen klonen.
**Auteur:** Strateeg (Grok).  
**Instrument:** `EURUSD` (RT **0,63 bp** → gate **1,89 bp**).  
**Track 4:** andere horizon — **H4 trend-follow** (niet MR zoals N27 AUDUSD; niet month TSMOM B1; niet London ORB A5).  
**Grond:** Als SMA20(H4) stijgt/daalt en close aan juiste kant, hold één H4-bar (12:00→16:00). Laag-swap intradag. Cheap RT.

**D-094a:** train 2021–2023. Reden **(b)**: FX trend op H4/D1 multi-decade; FTMO toetst kosten. ≠ B1 (maand, overnight).

**Onderscheid:** ≠ A5 ORB; ≠ GS02 fade; ≠ B1 month TSMOM; ≠ N27 AUDUSD H4 **MR**; ≠ N28/N33 session mom (M5 session, niet H4 SMA).

## Regel
- H4 from M5; at 12:00 CET bar: if close > sma20 and sma20 > sma20.shift(1) → LONG; if close < sma20 and sma20 < sma20.shift(1) → SHORT; exit 16:00 H4 close. No stop in bruto screen.

## Pre-screen
- Data: `EURUSD` m5gz → H4, train 2021–2023. Gate ≥ **1,89 bp**, N≥150. PASS → PREREG_FTMO_N37.
