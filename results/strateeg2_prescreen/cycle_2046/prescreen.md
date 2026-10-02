# Strateeg-2 Lane-A pre-screen — cycle_2046 (C-028 + POST-N78 cost stress)

**When:** 2026-10-02 ~20:46 Europe/Amsterdam (CEST).
**Branch:** `grok/strateeg-2`. **Trials:** 0. Reserve 2025+: untouched.
**Recovers:** failed ~19:49 CEST attempt (no partial artefacts; prior tip STALE).

## Families (all NEW_FAMILY vs last-30d dead + prior Lane-A + Faraday N90–N92)

| Family | Best symbols | lookback/hold | years | mean_bp | day_t | n | cost | promote |
|--------|--------------|---------------|------:|--------:|------:|--:|------|:-------:|
| BREAKEVEN_REALRATE | TIP/IEF→GLD | z40/thr1.5/tip_rich_long_gold|hold=1d | 19.91 | 3.577 | 1.192 | 1656 | N/A_NO_BRUTO | no |
| COPPER_GOLD_MACRO | COPPER_F/GOLD_F→SPY | z120/thr0.5/z_level|hold=1d | 19.83 | 2.281 | 1.123 | 3868 | N/A_NO_BRUTO | no |
| PC_RATIO_STRESS | CBOE_PUT→NDX | z120/put_trend|hold=1d | 19.83 | 2.522 | 1.598 | 4987 | N/A_NO_BRUTO | no |
| SECTOR_DISP_ROTATION | XL*disp→NDX | lb10/disp_fade_spy|hold=1d | 19.62 | 6.016 | 2.108 | 2558 | COST_OK | yes |

**Configs tested:** 84. **Promote configs:** 1. **Promote families:** 1. **Bruto-ok but COST_HOSTILE:** 0.

## Promote rule (POST-N78)
day_t ≥ 2 bruto (trade-conditional), n_days ≥ 80, train_years ≥ 5, mean_bp > 0, **and** early FTMO stress: mean_bp ≥ 3×RT and net_after_drag (RT+swap_night) ≥ 1 bp. Agri/index CFD cost traps flagged. Survivors → VOORSTEL (no PREREG by S2).

## Dead-set / clone guard
Barred: ORB, classic TSMOM, L60 FX-med, ENERGY, IDX_SHORT, FX_EUR_SHORT, USDJPY_MED, EURJPY_MED, TSMOM_DIV, **VIX_TERM_VOV**, CORN-as-FTMO, UKOIL-OVN, ORB-meta, N87. Not re-run: CTO COMMODITY_SEASONALITY / OVERNIGHT_GAP_FADE / XASSET_VOL_TIMING / FX_CARRY_TREND_RESIDUAL; prior S2 CREDIT/RATE_CURVE/EM_DM; N75–N77; N92 NY 2h mom.

## Survivors (cost-stressed)
- **SECTOR_DISP_ROTATION** `XL*disp→NDX` lb10/disp_fade_spy|hold=1d: day_t=2.108, mean=6.016 bp, n=2558, yrs=19.62, FTMO=US100cash, RT=0.66, drag=2.611, net=3.405, flag=COST_OK
