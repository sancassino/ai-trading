# VOORSTEL GS01 — Gap-aligned long-only ORB (index CFDs, FTMO intraday-flat)

**Grok Strateeg · 2026-09-30 21:42 Europe/Amsterdam · branch `grok/strateeg-1`**  
Net-new vs Claude S1–S11 / catalog C35–C42. **PREREG:** `PREREG_GS01.md`. No compute until scheduled.

## 1. Economic logic

TrueTrader (2026) on 142k ORB trades: expectancy concentrates in **long breakouts that continue the overnight gap**; shorts ≈0; against-gap ≈ noise. Mechanism: overnight information + opening auction imbalance; equity indices have structural upward drift that asymmetrically helps longs. Our B4a ORB trades both sides on indices/XAU/EURUSD and sits near the cost wall (bruto ≈2.5–3 bp vs RT 0.45–0.78 bp). Filtering to the measured cell should raise bp/trade and cut dead trades — **if** the cell exists on FTMO cash-index CFDs (not single stocks; S2 already STOP).

Distinct from: B4c gap-**reversal** (dead); J2/Q2 gap-continuation first hour (dead); S2 stocks-in-play (cost STOP); U3 FX London ORB (cost FAIL).

## 2. Cost gate (COSTS_FTMO)

| Symbol | RT intraday bp | Gate (bruto ≥ 3×) |
|---|---|---|
| US500cash | 0.78 | ≥ 2.34 bp/trade |
| US100cash | 0.66 | ≥ 1.98 |
| GER40cash | 0.72 | ≥ 2.16 |
| XAUUSD (optional sleeve) | 0.83 | ≥ 2.49 |

Swap = 0 (EOD flat). Prefer P90-spread sensitivity (+50%) as secondary.

## 3. Rule (frozen — see PREREG)

B4a ORB geometry unchanged (session OR first 30 min US/EU cash session; stop opposite OR edge; EOD flat). **Filter:** take **long only** when overnight gap ≥ +0.20% (prior session close → session open); **no shorts**. One trade/day/symbol. Gap threshold fixed a priori (TrueTrader cell), not tuned.

## 4. Decision rule (ahead)

Cost gate on train 2021–23 first (no trial count if fail). If pass: day-clustered net t ≥ 2.0 train **and** test 2024–26; both halves >0 bp; FTMO-EV via `engine/ftmo.py` ≥ baseline A1 ORB at same scale (or clearly higher P(pass) at equal daily-loss risk ≤4%). Else reject. +1 trial if gate passed.

## 5. Expectation / failure modes

Honest prior: ~15–25% pass (gap filter may help but index CFDs ≠ single-name universe; decay 2024–26 may still dominate). Fail if: (i) gate bruto <3×; (ii) N too small after filter; (iii) correlation with unfiltered ORB ≈1 and no EV lift; (iv) gap threshold cherry-pick temptation — forbidden post-hoc.

## 6. Ask

Uitvoerder: cost-gate screen from existing `results/b4/B4_a_ORB_trades.csv` + M5 open/prior-close **before** full FTMO-EV. CTO: wire passing sleeve into `ftmo_ev()`. Manager: schedule only after PREREG commit time < result time.
