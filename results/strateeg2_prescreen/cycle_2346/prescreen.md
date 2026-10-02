# Strateeg-2 Lane-A pre-screen — cycle_2346 (C-028 + POST-N78/N93; non-overlap holds)

**When:** 2026-10-02 ~23:46 Europe/Amsterdam (CEST).
**Branch:** `grok/strateeg-2`. **Trials:** 0. Reserve 2025+: untouched.
**Prior tip:** `35e38ac` (GAS+SILVER → N112 FAIL_T / N113 FAIL_COST_GATE; families now DEAD).
**NEXT_STEPS:** v96 @ `d6b9867` (C-038; TRIAL 464; formal OPEN empty).
**Method:** non-overlapping multi-day trades; drag = RT + swap_night×hold; promote = COST_OK only.

## Families (all NEW_FAMILY)

| Family | Best symbols | lookback/hold | years | mean_bp | day_t | n | cost | promote |
|--------|--------------|---------------|------:|--------:|------:|--:|------|:-------:|
| DEFENSIVE_CYCLICAL | XLU/XLI->NDX | z40/thr0.5/defensive_high|hold=5d | 19.89 | 19.754 | 2.077 | 911 | COST_OK | yes |
| EQW_CAP_BREADTH | EQW/SPY->SPY | z60/thr1.5/breadth_riskon|hold=1d | 19.91 | 6.81 | 1.989 | 1685 | N/A_NO_BRUTO | no |
| SOFTS_RATIO_MACRO | SUGAR/COFFEE->NDX | z120/thr0.5/softs_mom|hold=5d | 19.81 | 16.386 | 1.871 | 997 | N/A_NO_BRUTO | no |
| YIELD_CURVE_2S10S | 10Y-3M->SPY | z60/thr1.5/flatten_fade|hold=5d | 19.89 | 28.933 | 2.525 | 448 | COST_OK | yes |

**Configs:** 1377. **Promote configs:** 17. **Promote families:** 2. **COST_HOSTILE bruto-ok:** 0. **COST_TIGHT bruto-ok:** 0.

## Survivors (cost-stressed)
- **DEFENSIVE_CYCLICAL** `XLU/XLI->NDX` z40/thr0.5/defensive_high|hold=5d: day_t=2.077, mean=19.754 bp, n=911, yrs=19.89, FTMO=US100cash, drag=1.687, net=18.067, COST_OK
- **YIELD_CURVE_2S10S** `10Y-3M->SPY` z60/thr1.5/flatten_fade|hold=5d: day_t=2.525, mean=28.933 bp, n=448, yrs=19.89, FTMO=US500cash, drag=7.561, net=21.372, COST_OK
