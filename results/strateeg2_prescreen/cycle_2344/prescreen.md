# Strateeg-2 Lane-A pre-screen — cycle_2344 (C-028 + POST-N78/N93; non-overlap holds)

**When:** 2026-10-03 ~23:44 Europe/Amsterdam (CEST).
**Branch:** `grok/strateeg-2`. **Trials:** 0. Reserve 2025+: untouched.
**Prior tip:** `51b24bf` (XLK_TECH_SECTOR_STRESS → N161 FAIL_T; family now DEAD).
**NEXT_STEPS:** v106 @ `03ac200` (C-045 N164/N165 DIAG_FAIL; Faraday 218eb11; OPEN empty; TRIAL 471; FREEZE OFF).
**Method:** non-overlapping multi-day trades; drag = RT + swap_night×hold; promote = COST_OK only.

## Families (all NEW_FAMILY)

| Family | Best symbols | lookback/hold | years | mean_bp | day_t | n | cost | promote |
|--------|--------------|---------------|------:|--------:|------:|--:|------|:-------:|
| EWY_KOREA_STRESS | EWY->EURUSD | z120/thr0.5/z_level|hold=3d | 19.82 | 7.485 | 2.597 | 1242 | COST_OK | yes |
| LQD_IG_CREDIT_STRESS | LQD->NDX | z120/thr0.5/mom_confirm|hold=3d | 19.82 | 27.454 | 4.218 | 1170 | COST_OK | yes |
| USDNOK_OIL_FX | USDNOK->USDNOK | z40/thr1.0/fade_extreme|hold=1d | 19.91 | 5.648 | 2.1 | 2816 | COST_HOSTILE | no |
| XLY_DISCRETIONARY_STRESS | XLY->NDX | z120/thr0.5/mom_confirm|hold=5d | 19.81 | 17.866 | 1.804 | 770 | N/A_NO_BRUTO | no |

**Configs:** 1485. **Promote configs:** 119. **Promote families:** 2. **COST_HOSTILE bruto-ok:** 4. **COST_TIGHT bruto-ok:** 7.

## Survivors (cost-stressed)
- **EWY_KOREA_STRESS** `EWY->EURUSD` z120/thr0.5/z_level|hold=3d: day_t=2.597, mean=7.485 bp, n=1242, yrs=19.82, FTMO=EURUSD, drag=4.016, net=3.469, COST_OK
- **LQD_IG_CREDIT_STRESS** `LQD->NDX` z120/thr0.5/mom_confirm|hold=3d: day_t=4.218, mean=27.454 bp, n=1170, yrs=19.82, FTMO=US100cash, drag=6.512, net=20.941, COST_OK

## Bruto OK but COST_HOSTILE
- USDNOK_OIL_FX `USDNOK->USDNOK` z40/thr1.0/fade_extreme|hold=1d: day_t=2.1 mean=5.648 drag=4.777
- USDNOK_OIL_FX `USDNOK->USDNOK` z40/thr1.0/risk_off_high|hold=1d: day_t=2.1 mean=5.648 drag=4.777
- USDNOK_OIL_FX `USDNOK->USDNOK` z120/thr1.0/fade_extreme|hold=1d: day_t=2.007 mean=5.473 drag=4.777
- USDNOK_OIL_FX `USDNOK->USDNOK` z120/thr1.0/risk_off_high|hold=1d: day_t=2.007 mean=5.473 drag=4.777

## Bruto OK but COST_TIGHT (not promoted this cycle)
- LQD_IG_CREDIT_STRESS `LQD->SPY` z40/thr0.5/mom_confirm|hold=1d: day_t=2.31 mean=4.65 drag=2.136 net=2.514
- LQD_IG_CREDIT_STRESS `LQD->SPY` z40/thr0.5/z_level|hold=1d: day_t=2.271 mean=4.478 drag=2.136 net=2.342
- EWY_KOREA_STRESS `EWY->EURUSD` z60/thr1.0/z_level|hold=1d: day_t=2.075 mean=2.978 drag=1.759 net=1.219
- EWY_KOREA_STRESS `EWY->EURUSD` z40/thr1.0/z_level|hold=1d: day_t=2.049 mean=3.003 drag=1.759 net=1.244
- EWY_KOREA_STRESS `EWY->EURUSD` z40/thr1.0/mom_confirm|hold=1d: day_t=2.032 mean=3.008 drag=1.759 net=1.249
- USDNOK_OIL_FX `USDNOK->USDNOK` z40/thr1.5/fade_extreme|hold=5d: day_t=2.019 mean=18.081 drag=4.844 net=13.238
- USDNOK_OIL_FX `USDNOK->USDNOK` z40/thr1.5/risk_off_high|hold=5d: day_t=2.019 mean=18.081 drag=4.844 net=13.238
