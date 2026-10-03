# VOORSTEL_PRESCREEN_N169 — GBPUSD_LONDON_FIX_RESIDUAL_FADE session-flat (NEW_FAMILY CL)

**Status:** **OPEN** — D-094 refill after N166 FAIL_CLONE + N167 FAIL (filed 2026-10-04 ~00:01 CEST). Not cost-screened. Not a pre-screen.
**Auteur:** Strateeg (Grok). **NEW_FAMILY CL** (cable **London-fix residual fade**, one G10 major, not a cross).
**Signal:** M5 impulse on **GBPUSD** 17:00→18:00 broker time (London 16:00 year-round; broker is UTC+2/+3). **Trade:** fade that hour, flat by **20:30**. Threshold **±15** bp frozen a priori.
**Mechanism:** the hour into the London fix overshoots; the residual reverts before the late US session. Not an opening-range breakout.

**Gate (`COSTS_FTMO.csv`):** GBPUSD RT **0,70** → gate 3 × 0,70 = **2,10** bp. Not the US500 2,34 gate. Swap nights 0 inside the gate (flat before the roll). Both swap sides pay (long 0,46 / short 0,30); there is no credit to treat as alpha.

**D-094a reason (b):** GBPUSD M5 from 2021-01-04; archive through 2026 > 5y. Intraday fix residual; no pre-2021 daily factor required.

**Onderscheid (not screened):**
- ≠ N29 GBPUSD London midday fade (flat by 15:00; this book starts at 17:00)
- ≠ N38 London-morning continuation (ends 14:30)
- ≠ N46 EURGBP fix (barred cross; this is the major, one leg)
- ≠ N163 AUD NY-impulse (15:30–17:00) and not a same-window twin
- ≠ G10 cross XS, L60, EWY→EUR, EURCHF London-haven

**Future clone bar:** FAIL_CLONE if (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N29, N38, N46's GBP leg, or a EURUSD/AUDUSD 17:00–18:00 same-window fade.
