# Strateeg-2 Lane-A pre-screen — cycle_0046 (C-028 + POST-N78/N93; non-overlap holds)

**When:** 2026-10-04 ~00:46 Europe/Amsterdam (CEST).
**Branch:** `grok/strateeg-2`. **Trials:** 0. Reserve 2025+: untouched.
**Prior tip:** `885090b` (LQD_IG_CREDIT_STRESS + EWY_KOREA_STRESS → N166 FAIL_CLONE / N167 FAIL; families now DEAD).
**NEXT_STEPS:** v113 @ `400d401` (HOLD Strateeg; C-047 NEW_FAMILY ask stale; OPEN empty; TRIAL 471; FREEZE OFF).
**Method:** non-overlapping multi-day trades; drag = RT + swap_night×hold; promote = COST_OK only.
**Note:** Strateeg Lane-B = HOLD — survivors packed for later, not immediate PREREG ask.

## Families (all NEW_FAMILY)

| Family | Best symbols | lookback/hold | years | mean_bp | day_t | n | cost | promote |
|--------|--------------|---------------|------:|--------:|------:|--:|------|:-------:|
| EWA_AUSTRALIA_STRESS | EWA->EURUSD | z40/thr1.0/z_level|hold=1d | 19.91 | 2.272 | 1.585 | 2466 | N/A_NO_BRUTO | no |
| EWC_CANADA_STRESS | EWC->EURUSD | z60/thr1.0/mom_confirm|hold=5d | 19.89 | 14.215 | 2.779 | 604 | COST_OK | yes |
| XLI_INDUSTRIALS_STRESS | XLI->NDX | z120/thr0.5/z_level|hold=3d | 19.82 | 7.343 | 1.265 | 1468 | N/A_NO_BRUTO | no |
| XLP_STAPLES_STRESS | XLP->NDX | z40/thr1.5/fade_extreme|hold=1d | 19.91 | 6.038 | 1.698 | 1705 | N/A_NO_BRUTO | no |
| XLU_UTILITIES_STRESS | XLU->SPY | z40/thr1.5/fade_extreme|hold=3d | 19.9 | 17.053 | 2.291 | 708 | COST_OK | yes |

**Configs:** 1215. **Promote configs:** 9. **Promote families:** 2. **COST_HOSTILE bruto-ok:** 0. **COST_TIGHT bruto-ok:** 0.

## Survivors (cost-stressed)
- **EWC_CANADA_STRESS** `EWC->EURUSD` z60/thr1.0/mom_confirm|hold=5d: day_t=2.779, mean=14.215 bp, n=604, yrs=19.89, FTMO=EURUSD, drag=6.274, net=7.941, COST_OK
- **XLU_UTILITIES_STRESS** `XLU->SPY` z40/thr1.5/stress_buy|hold=3d: day_t=2.291, mean=17.053 bp, n=708, yrs=19.9, FTMO=US500cash, drag=4.848, net=12.205, COST_OK
