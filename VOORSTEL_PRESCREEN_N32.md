# VOORSTEL_PRESCREEN_N32 — US30cash Initial-Balance Breakout Continuation

**Status:** **geen PREREG — D-092.1 FAIL** (Strateeg screen 2026-10-01 08:26; N=754, mean **+0,43** < 1,35 bp). Artifacts `results/R2/n32_n34_prescreen/`.  
**Auteur:** Strateeg (Grok).  
**Instrument:** `US30cash` (RT **0,45 bp** → gate **1,35 bp**).  
**Track 2:** index — **IB continuation** (≠ S2-IB_FADE which faded IB extremes).  
**Grond:** 60-min Initial Balance (15:30–16:30 CET) definieert ochtend-value; break ná 16:30 in IB-richting vervolgt vaak tot lunch. Continuation, geen fade, geen 5-min ORB.

**D-094a:** train 2021–2023. Reden **(b)**: IB-breakout continuation is futures-microstructure (proxy YM/ES); FTMO-M5 = kosten.

**Onderscheid:** ≠ **S2-IB_FADE** (fade); ≠ ORB-familie (5–30m OR); ≠ N20 PM cont; ≠ LUNCH_OPEN.

## Regel
- IB_high/low = max/min M5 15:30–16:30 CET (excl. orphan daily bar).  
- Na 16:30: eerste close **> IB_high** → LONG; **< IB_low** → SHORT; max 1/dag.  
- Entry = break-close; stop = IB mid (of 1×ATR14 als strenger); flat **18:30 CET**. Swap 0.

## Pre-screen
- Data: `US30cash` m5gz train 2021–2023. Gate ≥ **1,35 bp**, N≥150. Geen test/reserve. PASS → PREREG_FTMO_N32.
