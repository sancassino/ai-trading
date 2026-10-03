# VOORSTEL_PRESCREEN_N163 — AUDUSD_NY_IMPULSE_FADE session-flat (NEW_FAMILY CF)

**Status:** **geen PREREG — DIAG_FAIL_CLONE** CTO C-044 `02ed02b` + Faraday `n162_n163_prescreen` (N=296, mean **−1,674 < 3,66**; day_t −0,76; NZD same-window twin agree **1,00** cover **0,80**). Synced 2026-10-03 ~23:21 CEST. NEW_FAMILY CF dead; no NZD twin, no thr-grid, no overnight.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY CF** (AUD **NY-hour impulse fade**, one FX major, session-flat). Round-trip is in `COSTS_FTMO.csv`. Not a G10 cross (no second leg). Not a metal pair. Not an equity factor. Not an oil sleeve. Not a GER40 session. Not a silver impulse. Not XLK.  
**Signal:** M5 impulse on **AUDUSD** 15:30→17:00 CET. **Trade:** the same leg, flat by 21:00.  
**Track 2 + D-100:** the NY equity hour overshoots commodity FX; fade it inside the same session. Flat before the roll so swap is not the alpha. Not London-open ORB. Not an Asia-range fade. Not AUD/NZD relative value.

**Gate (`COSTS_FTMO.csv`):** AUDUSD RT **1,22** → gate 3 × 1,22 = **3,66** bp. Swap 0 (session-flat). No NZD twin. No XAU leg.

**D-094a:** train 2021–2023. Reden **(b)**: AUDUSD M5 from 2021-01. The NY hour on AUD is smaller than an index hour (|move| train p50 **15** bp, p75 **26** bp). Threshold **±20** is frozen on that scale (296 days at ±20; not chosen on PnL). Mechanism is a same-day fade of the NY impulse, not carry, not the AUD/NZD cross, not AUD versus gold.

**Pre-file clone check (train 2021–2023 sign only; not a cost screen):** not a clone of a filed book (agree≥0,85 and cover≥0,70).  
N92 US100 NY-2h mom agree **0,32**, cover **0,82**. AUD 5d momentum (next day) agree **0,49**, cover **0,99**. AUDNZD z40 thr ±1,5 AUD-leg (next day) agree **0,41**, cover **0,34**. AUD Asia-window fade (00:00→07:00, ±20) agree **0,53**, cover **0,48**. N87 US30 gap agree **0,52**, cover **0,38**.

**NZD same-window twin is not this screen, and must not be filed:** NZDUSD 15:30→17:00 fade agree **1,00** cover **0,80**. One AUD leg only.

**Onderscheid:**
- ≠ **N162** US500 cash-close fade (other OPEN; FX major, not an index close; do not pool)
- ≠ **N161** XLK→US100 (live PREREG; no equity ETF signal)
- ≠ **N160** XAG NY-fade (FAIL; no silver)
- ≠ **N146** AUD/XAU pair / **N84** AUDNZD stretch / **N91** AUD carry
- ≠ **FX_INTRADAG** London-open ORB (STOP) / **GS02** Asia-range fade (this window is 15:30→17:00)
- ≠ **N47** USDCHF Asia→London continuation (other pair; NY fade, not Asia continuation)
- ≠ **N152** GBP/NZD and the other G10-cross books (one leg)
- ≠ NZDUSD same-window twin (clone; do not file)
- ≠ oil-NY / GER40-close / silver-impulse / XLK-sector

## Regel
**Signal (dag t, AUDUSD):**
1. `P0` = first M5 ≥ **15:30 CET** (span ≤15 min). `P1` = first M5 ≥ **17:00 CET** (span ≤15 min). Either missing → skip.
2. `ny_bp = 1e4 × (P1 / P0 − 1)`.
3. **fade:** `ny_bp ≥ +20` → **SHORT** at P1; `ny_bp ≤ −20` → **LONG** at P1; else skip. Threshold frozen — no grid.

**Execution (same day) — D-100 session-flat:**
4. Entry = that 17:00 bar. Exit: last M5 ≤ **21:00 CET**. **No overnight.**
5. PnL bp = signed return of the one leg. Non-overlapping (≤1 trade/day).

**Future clone bar (precommitted):** FAIL_CLONE if (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N92, vs N91's AUD sign, vs the AUD leg of N146, vs N84's AUDNZD sign, vs GS02/Asia-range fade, or vs an NZDUSD same-window fade. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/AUDUSD.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **3,66** bp, **N ≥ 150**.
- PASS → PREREG. FAIL → STOP (geen NZD twin, geen XAU leg, geen cross, geen thr-grid, geen overnight, geen soft gate).
