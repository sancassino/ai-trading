# C-020 — P1 ORB+BTC reserve one-shot (D-096)

**When:** 2026-10-01 ~08:57 Europe/Amsterdam (CEST / UTC+2)
**Verdict (CTO mechanical):** **FAIL**
**Auditor:** pending `AUDIT_4.md` (required for full PASS).

## Scales (frozen train 2021-2023)
- sA=3.58312  sB=1.51277  port_recommend_scale=7.1662
- target_daily_std(ORB train)=0.00288245  fB_vol=0.4222
- max daily loss (train recommend)=0.0400 (cap 0.04)

## Reserve window
- 2025-01-01..2026-09-23  (ORB days=448, BTC trades=119)

## Combined series (after frozen sA/sB)
- mean=0.000159507  ann_SR=0.1952380675418457
- day-clustered t (NW-L5)=0.24345690562593744
- ftmo_ev: p1*p2=0.7801  net_EV_eur/m=242.2  p_surv=0.101
- stress: p1*p2=0.7531  net_EV_eur/m=208.4

## Legs (unit, before sA/sB)
- ORB mean=0.000164587  SR=0.9353326310881108
- BTC mean=-0.000284398  SR=-0.8726815657850395  (active days=119)

## Criteria
- `net_mean_gt_0`: True
- `day_clust_t_ge_2`: False
- `ann_sr_ge_0_8`: False
- `p_pass_product_ge_0_35`: True
- `net_ev_gt_0`: True
- `stress_p_pass_product_ge_0_35`: True
- `stress_net_ev_gt_0`: True
- `leg_A_mean_ge_0`: True
- `leg_B_mean_ge_0`: False
- `auditor_independent_pass`: None

**Failed:** day_clust_t_ge_2, ann_sr_ge_0_8, leg_B_mean_ge_0

## Year split (informative)
| Year | port mean | ORB mean | BTC mean | BTC N |
|---|---:|---:|---:|---:|
| 2025 | 0.00010052228885346145 | 0.00032833967399447143 | -0.0007112493756452694 | 68 |
| 2026 | 0.0002403381222609991 | -5.981427379299786e-05 | 0.00030054757303387856 | 51 |

## Integrity
- PREREG before this result: `PREREG_FTMO_P1_ORB_BTC.md`
- BESLUITEN D-096 reserve vrijgave for P1 only
- TRIAL_COUNT 447 -> 448 (append-only)
- No FTMO signup / no fee spend by agents

