# PREREG GS01 — Gap-aligned long-only ORB (indices)

**Status:** Pre-registered 2026-09-30 21:42 Europe/Amsterdam on `grok/strateeg-1`.  
**Author:** Grok Strateeg. **No results before this commit.**

## 1. Rule (exact)

- **Universe (fixed):** US500cash, US100cash, GER40cash. Optional report-only sleeve: XAUUSD (same rule; does not change pass/fail of primary pool).
- **Session:** same as B4a / `b4_sim.run_orb` for each symbol’s cash session (DST-aware as existing ORB).
- **Opening range:** first 30 minutes (6× M5), high/low.
- **Gap:** `gap = session_open / prior_session_close − 1`. Prior close = last bar of previous cash session.
- **Entry:** **Long only** if `gap ≥ +0.0020` **and** price breaks OR high (buy-stop / first touch per existing simulator convention). **No short** entries. One trade per symbol per day. No re-entry.
- **Stop:** OR low (opposite edge). Same-bar stop/target conflict → stop wins (existing conservative rule).
- **Exit:** flatten at session end (intraday-flat). No overnight.
- **Sizing for EV:** risk scale such that expected daily loss risk ≤ 4% of initial at recommended scale (analysis may show higher as upper bound only — not a recommendation). Equal-risk across symbols in pool unless stated.

## 2. Mechanism

Overnight information / auction imbalance; continuation of gap direction through opening-range breakout; equity drift asymmetry. Source motivation: TrueTrader ORB study 2020–2026 (public). Not a claim that single-stock results transfer 1:1 to index CFDs.

## 3. Data

- FTMO M5 already used for B4a (`results/b4/`). Discovery ≤ 2024-12 for any labeling; test 2024–26 reported separately.
- **Reserve 2025+ for new shortlist only after CEO release (D-084 suspended)** — do not burn reserve for this PREREG’s primary decision; use 2024–26 as labeled test split consistent with U3/B4 practice, not as D-084 reserve burn for ETF work.
- No new scraped data.

## 4. Costs

From `COSTS_FTMO.csv`: spread of entry bar (long) / exit conventions as B4a + commission per S0. Gate: mean **gross** bp/trade ≥ 3× mean RT cost on **train 2021–23** for the pooled primary universe. Also report +50% spread sensitivity. Swap = 0.

## 5. Statistics & decision rule

1. **Gate:** if train gross < 3× costs → **STOP**, trial count +0.
2. If gate pass → trial count **+1**. Metrics: day-clustered t (Newey–West / block) on daily pooled PnL; bp/trade; skew; max daily dip; corr with B4a ORB daily series.
3. **Pass:** day-clustered net t ≥ 2.0 in train (2021–23) **and** test (2024–26); mean net bp > 0 in both halves; N_trades ≥ 200 pooled train.
4. **FTMO-EV:** run `engine/ftmo.py` (CTO) at comparable scale to A1 ORB; report p_pass_1/2, p_survive, exp_payout_monthly, net_ev. Informative for ranking; binary pass/fail remains §5.3 unless CEO changes.
5. **Forbidden:** tuning gap threshold, OR length, or adding RSI/vol filters after seeing results. Pre-declared sensitivity (report only, not selection): gap 0.15% and 0.30%.

## 6. Expected outcome / failure

Prior: modest. Likely failure modes: cost gate on reduced N; 2024–26 still ~0 after filter; index CFD ≠ single-name TrueTrader universe.

## 7. Relation to catalog

Net-new vs C35 (unfiltered ORB), C38 (gap rev/cont dead), S2 (stocks-in-play STOP). Does not reopen U3.
