# Strateeg-2 Lane-A pre-screen — cycle_0147 (C-028 + POST-N78/N93; non-overlap holds)

**When:** 2026-10-03 ~01:47 Europe/Amsterdam (CEST).
**Branch:** `grok/strateeg-2`. **Trials:** 0. Reserve 2025+: untouched.
**Prior tip:** `5a21939` (XLE_ENERGY_EQUITY_STRESS → N143 FAIL_CLONE of DBC; family now DEAD).
**NEXT_STEPS:** v103 @ `ddb929c` (N138–N153 FAIL; OPEN N154/N155; C-041+C-042; TRIAL 470; FREEZE OFF).
**Method:** non-overlapping multi-day trades; drag = RT + swap_night×hold; promote = COST_OK only.

## Families (all NEW_FAMILY)

| Family | Best symbols | lookback/hold | years | mean_bp | day_t | n | cost | promote |
|--------|--------------|---------------|------:|--------:|------:|--:|------|:-------:|
| AUDUSD_COMMODITY_FX | AUDUSD->EURUSD | z120/thr1.5/mom_confirm|hold=3d | 18.47 | 5.344 | 1.29 | 570 | N/A_NO_BRUTO | no |
| COCOA_FOOD_SOFT_MACRO | COCOA->SPY | z60/thr0.5/fade_extreme|hold=1d | 19.91 | 3.54 | 1.827 | 3791 | N/A_NO_BRUTO | no |
| XLK_TECH_SECTOR_STRESS | XLK->NDX | z120/thr0.5/mom_confirm|hold=3d | 19.82 | 12.228 | 2.046 | 1246 | COST_OK | yes |
| XLV_HEALTHCARE_STRESS | XLV->NDX | z40/thr1.5/fade_extreme|hold=1d | 19.91 | 6.577 | 1.783 | 1693 | N/A_NO_BRUTO | no |

**Configs:** 1350. **Promote configs:** 1. **Promote families:** 1. **COST_HOSTILE bruto-ok:** 0. **COST_TIGHT bruto-ok:** 0.

## Survivors (cost-stressed)
- **XLK_TECH_SECTOR_STRESS** `XLK->NDX` z120/thr0.5/mom_confirm|hold=3d: day_t=2.046, mean=12.228 bp, n=1246, yrs=19.82, FTMO=US100cash, drag=6.512, net=5.716, COST_OK
