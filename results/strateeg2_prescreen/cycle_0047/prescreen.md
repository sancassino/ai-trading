# Strateeg-2 Lane-A pre-screen — cycle_0047 (C-028 + POST-N78/N93; non-overlap holds)

**When:** 2026-10-03 ~00:47 Europe/Amsterdam (CEST).
**Branch:** `grok/strateeg-2`. **Trials:** 0. Reserve 2025+: untouched.
**Prior tip:** `13fe10c` (YIELD_CURVE+DEFENSIVE → N124/N125 FAIL_T; families now DEAD).
**NEXT_STEPS:** v102 @ `cb1b8d1` (N134–N137 FAIL; OPEN N138/N139; C-040; TRIAL 470; FREEZE OFF).
**Method:** non-overlapping multi-day trades; drag = RT + swap_night×hold; promote = COST_OK only.

## Families (all NEW_FAMILY)

| Family | Best symbols | lookback/hold | years | mean_bp | day_t | n | cost | promote |
|--------|--------------|---------------|------:|--------:|------:|--:|------|:-------:|
| EURJPY_RISK_SENTIMENT | EURJPY->SPY | z60/thr1.0/mom_confirm|hold=3d | 19.9 | 10.635 | 1.663 | 911 | N/A_NO_BRUTO | no |
| VLUE_VALUE_FACTOR_STRESS | VLUE->SPY | z40/thr1.0/fade_extreme|hold=3d | 11.61 | 11.182 | 1.564 | 656 | N/A_NO_BRUTO | no |
| XLB_MATERIALS_STRESS | XLB->NDX | z40/thr1.5/fade_extreme|hold=1d | 19.91 | 4.471 | 1.139 | 1601 | N/A_NO_BRUTO | no |
| XLE_ENERGY_EQUITY_STRESS | XLE->SPY | z40/thr1.0/fade_extreme|hold=1d | 19.91 | 5.412 | 2.289 | 2863 | COST_OK | yes |

**Configs:** 1215. **Promote configs:** 21. **Promote families:** 1. **COST_HOSTILE bruto-ok:** 0. **COST_TIGHT bruto-ok:** 0.

## Survivors (cost-stressed)
- **XLE_ENERGY_EQUITY_STRESS** `XLE->SPY` z40/thr1.0/fade_extreme|hold=1d: day_t=2.289, mean=5.412 bp, n=2863, yrs=19.91, FTMO=US500cash, drag=1.588, net=3.824, COST_OK
