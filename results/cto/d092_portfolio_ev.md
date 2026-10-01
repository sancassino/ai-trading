# D-092 portfolio / reference EV (CTO)

- When: 2026-10-01 ~01:53 Europe/Amsterdam
- Reserve 2025+: **not used** for decision rows
- No PREREG trial / no TRIALS append

## Correlations (train 2021–2023, dense ORB calendar)

| Pair | ρ |
|---|---:|
| ORB ↔ BTC | 0.113 |
| ORB ↔ XAU | 0.100 |
| BTC ↔ XAU | 0.038 |

## Results

| Sleeve | Window / label | N_act | ann SR | scale | p95 dip | max dip | p1·p2 | p_survive | €/m net EV |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| F2_ORB | F2_ORB_reference_le2024 | 1025 | 0.90 | 4.16 | 1.83% | 4.00% | 0.906 | 0.413 | 513 |
| F2_ORB | F2_ORB_train_2021_2023 | 765 | 1.06 | 4.16 | 1.95% | 4.00% | 0.942 | 0.433 | 683 |
| F2_ORB | F2_ORB_diagnostic_full_csv | 1473 | 0.91 | 2.82 | 1.30% | 4.00% | 0.726 | 0.665 | 288 |
| F2_ORB | sleeve_train | 765 | 1.06 | 4.16 | 1.95% | 4.00% | 0.942 | 0.433 | 683 |
| S2_BTC | sleeve_train | 131 | 0.74 | 2.28 | 1.26% | 4.00% | 0.845 | 0.227 | 500 |
| XAU_AM_FADE | sleeve_train | 12 | 0.66 | 5.85 | 0.00% | 4.00% | 0.074 | 1.000 | 7 |
| ORB+BTC_eqvol | portfolio_blend_train | 765 | 1.21 | 7.17 | 1.64% | 4.00% | 0.977 | 0.447 | 1006 |
| ORB+XAU_eqvol | portfolio_blend_train | 765 | 1.16 | 2.72 | 0.52% | 4.00% | 0.511 | 0.980 | 200 |
| ORB+BTC+XAU_eqvol | portfolio_blend_train | 765 | 1.31 | 4.08 | 0.63% | 4.00% | 0.759 | 0.964 | 393 |
| ORB70_BTC25_XAU5 | portfolio_blend_train | 765 | 1.24 | 6.13 | 1.74% | 4.00% | 0.973 | 0.501 | 965 |
| ORB+BTC_eqvol_BTCstress50 | portfolio_blend_train_cost_stress50_btc | 765 | 1.15 | 7.12 | 1.66% | 4.00% | 0.973 | 0.418 | 939 |

## Readout (CTO)

1. **F2-ORB ≤2024** is the binding reference: recommend_scale + trough DD → see JSON row `F2_ORB_reference_le2024`. Full-CSV (~€290 at scale≈2.8) is diagnostic decay only.
2. Correlations are **low** (ρ≈0.04–0.11) → diversification is real on paper.
3. **XAU_AM_FADE** remains structurally underpowered (N=12); it barely moves portfolio EV.
4. **S2-BTC** lifts SR in eqvol blend but is still power-FAIL alone; stress-50 BTC blend must stay >0 EV to count under D-092.5 cost stress.
5. No new trial claimed. Strateeg path = D-092.1 pre-screen + D-092.2 S2c XAU+XAG PREREG.

