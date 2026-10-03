# VOORSTEL_PRESCREEN_N170 — FRA40_US_OPEN_REACTION_FADE session-flat (NEW_FAMILY CM)

**Status:** **OPEN** — D-094 refill after C-046 N168 DIAG_FAIL_CLONE / N169 DIAG_FAIL (filed 2026-10-04 ~00:20 CEST). Not cost-screened. Not a pre-screen.
**Auteur:** Strateeg (Grok). **NEW_FAMILY CM** (CAC **US-open reaction fade**, one EU peripheral index, flat same day).
**Signal:** M5 impulse on **FRA40cash** 15:30→16:30 CET (US cash open hour as seen in Paris names). **Trade:** fade that hour, flat by **18:00 CET**. Threshold **±30** bp frozen a priori.
**Mechanism:** CAC names reprice into the US cash open with thin European afternoon liquidity; the first-hour overshoot reverts before the London/NY late session. Not an ORB, not a Europe-morning inventory book.

**Gate (`COSTS_FTMO_alle.csv` on main `f0f9597`):** FRA40cash RT **1,98** → gate 3 × 1,98 = **5,94** bp. Swap 0 (flat before the roll). Not the US500 2,34 gate.

**D-094a reason (b):** FRA40cash M5 from 2021-01-04 (true 5-min; archive through 2026 > 5y). Intraday US-open reaction; no pre-2021 factor history required.

**Onderscheid (not screened):**
- ≠ N107 UK100 Lon-AM → FRA40 afternoon lead-lag (UK signal → FRA trade; this book is FRA own impulse)
- ≠ N159 GER40 Europe-close fade (close window, different index)
- ≠ N168 US30 Europe-morning inventory 09:00→12:00 (different window + different index; same-window Europe morning is barred)
- ≠ N92 / N164 US NY-impulse on US indices (this is FRA, not US2000/US100)
- ≠ N11 GER40 XETRA ORB / ETF→index stress

**Future clone bar:** FAIL_CLONE if (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N107 FRA-leg, N159 GER same 15:30–16:30 window, GER40/EU50/UK100 15:30–16:30 same-window fade, or US30/US500/US100 15:30–16:30 twin.
