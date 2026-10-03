# VOORSTEL_PRESCREEN_N171 — BTCUSD_EU_MORNING_IMPULSE_FADE session-flat (NEW_FAMILY CN)

**Status:** **OPEN** — D-094 refill after C-046 N168 DIAG_FAIL_CLONE / N169 DIAG_FAIL (filed 2026-10-04 ~00:20 CEST). Not cost-screened. Not a pre-screen.
**Auteur:** Strateeg (Grok). **NEW_FAMILY CN** (crypto **Europe-morning own-impulse fade**, one BTC leg, flat before US cash).
**Signal:** M5 impulse on **BTCUSD** 08:00→10:00 CET. **Trade:** fade that 2h impulse, flat by **12:00 CET**. Threshold **±50** bp frozen a priori.
**Mechanism:** BTC Europe morning liquidity surge overshoots; fade and be flat before the US cash open. D-102 risk-reactive sleeve candidate (vol-reactive, session-flat). Not an Asia handoff continuation and not the US-open BTC book.

**Gate (`COSTS_FTMO_alle.csv` on main `f0f9597`):** BTCUSD RT **1,25** (spread med 0,85 + 2×0,20 commissie) → gate 3 × 1,25 = **3,75** bp. Swap 0 (flat before the roll). Not the US500 2,34 gate.

**D-094a reason (b):** BTCUSD M5 from 2021-01-01 (true 5-min; archive through 2026 > 5y). Intraday own-impulse fade; no pre-2021 factor required. (S2-BTC US-open is a different window and already power-limited historically — this book does not reopen that PREREG.)

**Onderscheid (not screened):**
- ≠ N39 BTC Asia→Europe handoff **continuation** (00:00–08:00 → flat 12:00; opposite mechanism + different signal window)
- ≠ S2-BTC / S2b US-open BTC (entry around US cash open)
- ≠ N145 BTC/ETH crypto XS (two-leg ratio)
- ≠ N169 GBP London-fix / N168 Europe inventory / ETF→index

**Future clone bar:** FAIL_CLONE if (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N39 trade-side (fade would be anti-correlated — still check), ETHUSD 08:00–10:00 same-window fade, or S2-BTC US-open day-sign.
