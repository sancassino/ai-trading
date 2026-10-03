# VOORSTEL_PRESCREEN_N168 — US30_EUROPE_INVENTORY_FADE session-flat (NEW_FAMILY CK)

**Status:** **OPEN** — D-094 refill after N166 FAIL_CLONE + N167 FAIL (filed 2026-10-04 ~00:01 CEST). Not cost-screened. Not a pre-screen.
**Auteur:** Strateeg (Grok). **NEW_FAMILY CK** (Dow CFD **Europe-hours inventory fade**, one index leg, flat before the US cash open).
**Signal:** M5 impulse on **US30cash** 09:00→12:00 CET. **Trade:** the same leg, flat by **15:00 CET**.
**Mechanism:** Europe-session drift in the Dow CFD is thin-book inventory, not cash-session information; fade it and be out before 15:30.

**Gate (`COSTS_FTMO.csv`):** US30cash RT **0,45** → gate 3 × 0,45 = **1,35** bp. Europe-window (09:00–15:00, train 2021–2023) median spread is **0,40** bp (3× = 1,19), which is softer; the book RT **1,35** wins because it is higher. Swap 0 (flat before the cash open and before the roll).

**D-094a reason (b):** US30cash M5 from 2021-01-04 (true 5-min; archive through 2026 > 5y). The rule is an intraday inventory fade; it does not need a pre-2021 factor history. Threshold **±25** bp frozen a priori (not fit on PnL).

**Onderscheid (not screened):**
- ≠ N20 US30 PM continuation (18:00–21:00, opposite sign)
- ≠ N87 US30 cash-gap fade (entry at the cash open)
- ≠ N162 cash-close / NY-impulse 15:30–17:00 / US500 or US100 same window
- ≠ ETF→index, LQD, XLK, gold/index, oil

**Future clone bar:** FAIL_CLONE if (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N20, N87, N162, or a US500/US100 09:00–15:00 same-window fade.
