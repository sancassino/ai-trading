# Strateeg-2 Lane-A pre-screen — cycle_2240 (C-028 + POST-N78/N93; non-overlap holds)

**When:** 2026-10-02 ~22:40 Europe/Amsterdam (CEST).
**Branch:** `grok/strateeg-2`. **Trials:** 0. Reserve 2025+: untouched.
**Prior tip:** `67a9be1` (EMB+CRACK → N100/N101 FAIL_T; families now DEAD).
**NEXT_STEPS:** v91 @ `88ad118` (C-036; TRIAL 460; formal OPEN empty).
**Method:** non-overlapping multi-day trades; drag = RT + swap_night×hold; promote = COST_OK only.

## Families (all NEW_FAMILY)

| Family | Best symbols | lookback/hold | years | mean_bp | day_t | n | cost | promote |
|--------|--------------|---------------|------:|--------:|------:|--:|------|:-------:|
| FACTOR_QUALITY_VALUE | QUAL/USMV->SPY | z60/thr0.5/mom_confirm|hold=5d | 11.36 | 16.874 | 1.756 | 520 | N/A_NO_BRUTO | no |
| GAS_EQUITY_MACRO | UNG->SPY | z40/thr1.5/stress_buy|hold=5d | 17.61 | 47.702 | 3.614 | 406 | COST_OK | yes |
| SILVER_GOLD_RATIO | SLV/GLD->SPY | z40/thr1.0/fade_extreme|hold=5d | 18.58 | 22.405 | 2.103 | 635 | COST_OK | yes |
| SMALLCAP_BREADTH | IWM/SPY->NDX | z120/thr1.0/fade_extreme|hold=3d | 19.82 | 14.281 | 1.926 | 960 | N/A_NO_BRUTO | no |

**Configs:** 1458. **Promote configs:** 128. **Promote families:** 2. **COST_HOSTILE bruto-ok:** 0. **COST_TIGHT bruto-ok:** 4.

## Survivors (cost-stressed)
- **GAS_EQUITY_MACRO** `UNG->SPY` z40/thr1.5/stress_buy|hold=5d: day_t=3.614, mean=47.702 bp, n=406, yrs=17.61, FTMO=US500cash, drag=4.821, net=42.881, COST_OK
- **SILVER_GOLD_RATIO** `SLV/GLD->SPY` z40/thr1.0/fade_extreme|hold=5d: day_t=2.103, mean=22.405 bp, n=635, yrs=18.58, FTMO=US500cash, drag=7.561, net=14.844, COST_OK

## Bruto OK but COST_TIGHT (not promoted this cycle)
- GAS_EQUITY_MACRO `UNG->SPY` z120/thr0.5/trend_follow|hold=1d: day_t=2.426 mean=4.609 drag=1.588 net=3.02
- GAS_EQUITY_MACRO `UNG->SPY` z120/thr1.0/trend_follow|hold=1d: day_t=2.426 mean=4.609 drag=1.588 net=3.02
- GAS_EQUITY_MACRO `UNG->SPY` z120/thr1.5/trend_follow|hold=1d: day_t=2.426 mean=4.609 drag=1.588 net=3.02
- GAS_EQUITY_MACRO `UNG->SPY` z120/thr0.5/stress_buy|hold=1d: day_t=2.1 mean=4.621 drag=1.588 net=3.033
