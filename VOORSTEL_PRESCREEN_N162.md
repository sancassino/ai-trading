# VOORSTEL_PRESCREEN_N162 — US500_CASH_CLOSE_FADE session-flat (NEW_FAMILY CE)

**Status:** **DIAG_FAIL_CLONE** — CTO C-044 (2026-10-03 ~22:57 CEST). CTO C-044 independent Lane-B: n=217 mean −0.308 < gate 2.34; twins US30/US100 same-window (agree 1.00 cover ≥0.79). Agrees Faraday uncommitted WT. No PREREG.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY CE** (S&P **cash-close impulse fade**, one index CFD, session-flat). Round-trip is in `COSTS_FTMO.csv`. Not a gold/index pair. Not an FX book. Not a sector ETF into Nasdaq. Not a silver leg. Not an oil sleeve. Not a GER40 session.  
**Signal:** M5 impulse on **US500cash** 19:00→20:30 CET. **Trade:** the same leg, flat by 21:00.  
**Track 2 + D-100:** the last 90 minutes of the US cash session overshoot; fade that impulse and be flat before the roll. Not the NY-open 2h, not the lunch fade of the morning impulse, not the opening gap.

**Gate (`COSTS_FTMO.csv`):** US500cash RT **0,78** → gate 3 × 0,78 = **2,34** bp. Swap 0 (session-flat). No US100 remap. No US30 twin.

**D-094a:** train 2021–2023. Reden **(b)**: US500cash M5 from 2021-01. The 90-minute close window is smaller than the NY hour (|move| train p50 **19** bp, p75 **34** bp). Threshold **±25** is frozen on that scale so a screen can clear N≥150 (217 days at ±25; not chosen on PnL). Mechanism is a same-day fade of the cash close, not N24's morning impulse, not N92's Nasdaq open, not N87's Dow gap.

**Pre-file clone check (train 2021–2023 sign only; not a cost screen):** not a clone (agree≥0,85 and cover≥0,70).  
N24 US500 AM-fade (15:30→18:00, ±40) agree **0,50**, cover **0,55**. N92 US100 NY-2h mom agree **0,53**, cover **1,00**. N87 US30 gap-fade agree **0,50**, cover **0,42**. N159 GER40 Europe-close agree **0,40**, cover **0,33**. N161 XLK→US100 book agree **0,54**, cover **0,60**.

**Same-window twins are not this screen, and must not be filed:** US30 19:00→20:30 fade agree **1,00** cover **0,79**; US100 same window agree **1,00** cover **0,90**. One index only.

**Onderscheid:**
- ≠ **N161** XLK→US100 (live PREREG; other instrument; signal is the index's own close, not XLK z120)
- ≠ **N160** XAG NY-fade (FAIL; no silver)
- ≠ **N24** US500 lunch fade of the 15:30→18:00 impulse (this window starts at 19:00)
- ≠ **N92** US100 NY-open 2h momentum (fade, not continuation; later window; S&P not Nasdaq)
- ≠ **N87** US30 opening-gap fade (not a gap vs the prior 22:00 close)
- ≠ **N20** US30 PM continuation (opposite sign)
- ≠ **N159** GER40 Europe-close / **N158** oil NY-fade
- ≠ US30 or US100 cash-close twin (clone; do not file)

## Regel
**Signal (dag t, US500cash):**
1. `P0` = first M5 ≥ **19:00 CET** (span ≤15 min). `P1` = first M5 ≥ **20:30 CET** (span ≤15 min). Either missing → skip.
2. `cls_bp = 1e4 × (P1 / P0 − 1)`.
3. **fade:** `cls_bp ≥ +25` → **SHORT** at P1; `cls_bp ≤ −25` → **LONG** at P1; else skip. Threshold frozen — no grid.

**Execution (same day) — D-100 session-flat:**
4. Entry = that 20:30 bar. Exit: last M5 ≤ **21:00 CET**. **No overnight.**
5. PnL bp = signed return of the one leg. Non-overlapping (≤1 trade/day).

**Future clone bar (precommitted):** FAIL_CLONE if (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N24, vs N92, vs N87, vs N159, vs N161's US100 side, or vs a US30/US100 same-window fade. A clone is not a PASS. Do not file the twin after a clone hit.

## Pre-screen
- Data: `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **2,34** bp, **N ≥ 150**.
- PASS → PREREG. FAIL → STOP (geen US30/US100 twin, geen XLK remap, geen gap rewrite, geen thr-grid, geen overnight, geen soft gate).
