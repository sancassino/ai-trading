# Strateeg-2 Lane-A pre-screen — cycle_2140 (C-028 + POST-N78; non-overlap holds)

**When:** 2026-10-02 ~21:40 Europe/Amsterdam (CEST).
**Branch:** `grok/strateeg-2`. **Trials:** 0. Reserve 2025+: untouched.
**Prior tip:** `fde4a15` (SECTOR_DISP → N93 FAIL_COST; family skipped).
**Method:** non-overlapping multi-day trades; drag = RT + swap_night×hold (worse side).

## Families (all NEW_FAMILY)

| Family | Best symbols | lookback/hold | years | mean_bp | day_t | n | cost | promote |
|--------|--------------|---------------|------:|--------:|------:|--:|------|:-------:|
| CRACK_SPREAD_MACRO | HO/BRENT->NDX | z60/thr0.5/crack_fade|hold=5d | 17.33 | 23.091 | 2.26 | 773 | COST_OK | yes |
| EMB_CREDIT_STRESS | EMB->NDX | z120/combo|hold=3d | 16.86 | 21.415 | 3.002 | 998 | COST_OK | yes |
| PGM_RATIO_CYCLE | PALL/PLAT->NDX | z120/thr1.5/z_level|hold=5d | 19.81 | 16.343 | 1.069 | 357 | N/A_NO_BRUTO | no |
| REIT_RATE_CHANNEL | VNQ/TLT->SPY | z40/thr1.0/fade_extreme|hold=3d | 19.9 | 10.535 | 1.747 | 1021 | N/A_NO_BRUTO | no |

**Configs:** 567. **Promote configs:** 13. **Promote families:** 2. **COST_HOSTILE bruto-ok:** 0.

## Survivors (cost-stressed)
- **CRACK_SPREAD_MACRO** `HO/BRENT->NDX` z60/thr0.5/crack_fade|hold=5d: day_t=2.26, mean=23.091 bp, n=773, yrs=17.33, FTMO=US100cash, drag=10.413, net=12.678, COST_OK
- **EMB_CREDIT_STRESS** `EMB->NDX` z120/combo|hold=3d: day_t=3.002, mean=21.415 bp, n=998, yrs=16.86, FTMO=US100cash, drag=6.512, net=14.903, COST_OK
