# PREREG GS02 — Asian-range fade (EURUSD, GBPUSD)

**Status:** Pre-registered 2026-09-30 21:42 Europe/Amsterdam on `grok/strateeg-1`.  
**Author:** Grok Strateeg. **No results before this commit.**  
**Not** U3 / not London-open ORB breakout.

## 1. Rule (exact)

- **Symbols:** EURUSD, GBPUSD (FTMO M5).
- **Asian range (AR):** high and low of all M5 bars with timestamp in **[00:00, 07:00) UTC** on the calendar day (UTC date of the bar open). Fixed UTC — no London DST adjustment for AR bounds.
- **Signal window:** [07:00, 10:00) UTC same day.
- **Short fade:** (i) some bar’s high > AR_high; (ii) later in window, an M5 **close ≤ AR_high**; (iii) enter short at open of next M5 bar. Stop = max(sweep high, AR_high) + 0 (stop at sweep extreme high of the signal window up to entry). 
- **Long fade:** symmetric (low < AR_low, then close ≥ AR_low; stop at sweep low).
- **Targets / exit:** scale 50% at AR midpoint; remainder at opposite AR bound; **hard flat at 16:00 UTC** (overlap end / pre-NY afternoon). If stop and target same bar → stop wins.
- **Caps:** at most one position per symbol per day; no pyramiding; skip day if AR width < 1.5× median AR width of prior 20 days (liquidity/noise filter — **frozen**, not tuned).
- **Intraday-flat:** no position after 16:00 UTC.

## 2. Mechanism

Failed stop-run / inventory reversion after Asian-range sweep at London open; fade only on reclaim close, not on first touch.

## 3. Data / costs

FTMO M5 2021–26. Costs: S0 spread+commission as B4a/U3. Gate: train 2021–23 mean gross ≥ 3× mean RT (EURUSD 0.63 bp, GBPUSD 0.70 bp). +50% spread sensitivity. Swap 0.

## 4. Decision rule

1. Gate fail → STOP, +0 trials.  
2. Gate pass → +1 trial (pooled family of 1 across 2 symbols).  
3. Pass criteria: day-clustered net t ≥ 2.0 in train and in test 2024–26; mean net > 0 both halves; N ≥ 150 train trades pooled.  
4. Report corr with D1 daily PnL and with U3 (if any trades exist).  
5. **Forbidden post-hoc:** flipping to breakout continuation; changing AR hours; adding news filter after results.

## 5. Reserve

D-084: do not use 2025+ as exclusive OOS burn for pass/fail beyond the labeled 2024–26 test split used elsewhere for FTMO intraday. No ETF reserve interaction.

## 6. Expected outcome

Low prior. Primary risk: popularization decay + trend days where sweeps continue through overlap.
