# Strateeg-2 Lane-A pre-screen — cycle_1240 (C-028)

**When:** 2026-10-01 ~12:45 Europe/Amsterdam (CEST).
**Branch:** `grok/strateeg-2`. **Trials:** 0. Reserve 2025+: untouched.

## Families (all NEW_FAMILY vs last-30d dead + CTO C-028 set + N75–N77)

| Family | Best symbols | lookback/hold | years | mean_bp | day_t | n | promote |
|--------|--------------|---------------|------:|--------:|------:|--:|:-------:|
| CREDIT_SPREAD_PROXY | HYG/LQD→TLT | z90/thr1.0|hold=1d | 17.61 | 3.11 | 1.484 | 2379 | no |
| EM_DM_FLOW_ROTATION | EEM/EFA+DXY | rel120/dxy60|hold=1d_LS | 19.52 | 2.522 | 1.414 | 2846 | no |
| RATE_CURVE_SHAPE | TYX-TNX→SPY | lvl120/d5|hold=1d | 19.81 | 3.335 | 1.788 | 4301 | no |
| VIX_TERM_VOV | VIX9D/VIX3M+VoV→NDX | vov10/combo|hold=1d | 13.99 | 6.802 | 2.906 | 2327 | yes |

**Configs tested:** 70. **Promote configs:** 7. **Promote families:** 1.

## Promote rule
day_t ≥ 2 bruto (trade-conditional), n_days ≥ 80, train_years ≥ 5, mean_bp > 0. No FTMO cost gate here (Lane A). Survivors → VOORSTEL for Strateeg Lane-B.

## Dead-set / clone guard
Barred: ORB, classic TSMOM, L60 FX-med, ENERGY, IDX_SHORT, FX_EUR_SHORT, USDJPY_MED, EURJPY_MED, TSMOM_DIV. Not re-run: CTO COMMODITY_SEASONALITY / OVERNIGHT_GAP_FADE / XASSET_VOL_TIMING / FX_CARRY_TREND_RESIDUAL. Not clone: N75 metal-pair MR, N76 UKOIL inventory, N77 FX XS rank-rev.

## Survivors
- **VIX_TERM_VOV** `VIX9D/VIX3M+VoV→NDX` vov10/combo|hold=1d: day_t=2.906, mean=6.802 bp, n=2327, yrs=13.99
