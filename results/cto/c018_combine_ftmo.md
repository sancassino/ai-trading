# C-018 — D-094 tracks 3+5: combine + FTMO sizing (CTO)

- When: 2026-10-01 ~08:10 Europe/Amsterdam (CEST / UTC+2)
- Branch: `grok/cto-1`
- Reserve 2025+: **not used**
- No PREREG trial / no TRIALS append / no dead-sleeve solo reopen
- Integrity: PREREG-before-results, append-only TRIALS, day-clustered t, FDR, FTMO costs

## Inventory (weak-positive / near-pass)

| Sleeve | Role | Status | Solo reopen? |
|---|---|---|---|
| F2_ORB | anchor / weak-positive reference | reference_edge (HistData M1 blocked for longer replicate) | NO |
| S2_BTC | power-fail diversifier (high bruto, N<150) | power_FAIL N=132<150; cost gate PASS | NO |
| XAU_AM_FADE | watch-only underpowered | watch_only N=12≪120 | NO |
| N11_GER40_XETRA_ORB | portfolio diagnostic only (gate PASS → FAIL_STRESS/FAIL_T) | FAIL_STRESS_then_FAIL_T (t_day≈0.92); DEAD — no solo reopen/clone | NO |
| N18_US500_OVN_GAP_CONT | portfolio diagnostic only (gate+stress PASS → FAIL_T) | FAIL_T (t_day≈0.64; 2023 mean−12bp); DEAD — no solo reopen/clone | NO |
| LUNCH_OPEN | portfolio diagnostic only (cost PASS → FAIL_T; positive skew) | FAIL_T (t_train≈1.14, t_test≈0.05); DEAD — no solo reopen/clone | NO |

## Correlations (train 2021–2023, dense ORB calendar)

| Pair | ρ |
|---|---:|
| BTC ↔ LUNCH | -0.075 |
| BTC ↔ N11 | 0.046 |
| BTC ↔ N18 | -0.199 |
| BTC ↔ XAU | 0.030 |
| N11 ↔ LUNCH | -0.000 |
| N11 ↔ N18 | 0.060 |
| N18 ↔ LUNCH | -0.154 |
| ORB ↔ BTC | 0.113 |
| ORB ↔ LUNCH | -0.095 |
| ORB ↔ N11 | 0.017 |
| ORB ↔ N18 | 0.015 |
| ORB ↔ XAU | 0.100 |
| XAU ↔ LUNCH | 0.026 |
| XAU ↔ N11 | -0.060 |
| XAU ↔ N18 | 0.001 |

## Track 3a — singles + portfolio blends (`recommend_scale` → `ftmo_ev`)

| Sleeve | Window / label | N_act | ann SR | skew | scale | p95 dip | max dip | p1·p2 | p_survive | €/m net EV |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| F2_ORB | F2_ORB_reference_le2024 | 1025 | 0.90 | 1.20 | 4.16 | 1.83% | 4.00% | 0.906 | 0.413 | 513 |
| F2_ORB | F2_ORB_train_2021_2023 | 765 | 1.06 | 1.17 | 4.16 | 1.95% | 4.00% | 0.942 | 0.433 | 683 |
| F2_ORB | sleeve_train | 765 | 1.06 | 1.17 | 4.16 | 1.95% | 4.00% | 0.942 | 0.433 | 683 |
| S2_BTC | sleeve_train | 131 | 0.74 | 6.86 | 2.28 | 1.26% | 4.00% | 0.845 | 0.227 | 500 |
| XAU_AM_FADE | sleeve_train | 12 | 0.66 | 11.93 | 5.85 | 0.00% | 4.00% | 0.074 | 1.000 | 7 |
| N11_GER40 | sleeve_train | 475 | 0.52 | 1.77 | 3.34 | 1.47% | 4.00% | 0.833 | 0.181 | 469 |
| N18_GAP_CONT | sleeve_train | 279 | 0.36 | -0.76 | 1.34 | 0.79% | 4.00% | 0.270 | 0.579 | 31 |
| LUNCH_OPEN | sleeve_train | 191 | 0.65 | 5.21 | 2.65 | 0.75% | 4.00% | 0.541 | 0.590 | 121 |
| ORB+BTC_eqvol | portfolio_blend_train | 765 | 1.21 | 3.74 | 7.17 | 1.64% | 4.00% | 0.977 | 0.447 | 1006 |
| ORB+BTC+XAU_eqvol | portfolio_blend_train | 765 | 1.31 | 4.81 | 4.08 | 0.63% | 4.00% | 0.759 | 0.964 | 393 |
| ORB70_BTC25_XAU5 | portfolio_blend_train | 765 | 1.24 | 1.72 | 6.13 | 1.74% | 4.00% | 0.973 | 0.501 | 965 |
| ORB+LUNCH_eqvol | portfolio_blend_train | 765 | 1.27 | 4.96 | 8.57 | 1.78% | 4.00% | 0.981 | 0.444 | 1200 |
| ORB+N18_eqvol | portfolio_blend_train | 765 | 1.00 | 1.15 | 5.29 | 1.46% | 4.00% | 0.936 | 0.511 | 543 |
| ORB+N11_eqvol | portfolio_blend_train | 765 | 1.11 | 1.17 | 5.22 | 1.41% | 4.00% | 0.888 | 0.496 | 680 |
| ORB+BTC+LUNCH_eqvol | portfolio_blend_train | 765 | 1.44 | 4.14 | 8.18 | 1.33% | 4.00% | 0.981 | 0.659 | 1088 |
| ORB60_BTC25_LUNCH15 | portfolio_blend_train | 765 | 1.36 | 2.17 | 7.78 | 1.89% | 4.00% | 0.988 | 0.473 | 1188 |
| ORB50_BTC20_LUNCH20_N18_10 | portfolio_blend_train | 765 | 1.48 | 1.97 | 9.66 | 1.97% | 4.00% | 0.993 | 0.456 | 1375 |
| WEAK5_eqvol | portfolio_blend_train | 765 | 1.62 | 2.97 | 6.28 | 0.81% | 4.00% | 0.947 | 0.908 | 616 |
| ORB+BTC_eqvol_BTCstress50 | portfolio_blend_train_cost_stress50_ | 765 | 1.15 | 3.73 | 7.12 | 1.66% | 4.00% | 0.973 | 0.418 | 939 |
| ORB60_BTC25_LUNCH15_BTCstress50 | portfolio_blend_train_cost_stress50_ | 765 | 1.33 | 2.17 | 7.78 | 1.90% | 4.00% | 0.987 | 0.461 | 1154 |

## Track 3b — ensemble / filter hypotheses (documented only)

### H-ENS-01: ORB ∩ LUNCH same-day filter
- **Status:** hypothesis_only — no PREREG this cycle; do not mine thresholds post-hoc
- **Owner:** CEO/Strateeg (D-094.7: CEO may write ensemble PREREGs)
- **Mechanism:** Trade F2-ORB only on days LUNCH_OPEN also fires in same direction (or only when LUNCH morning residual agrees with ORB breakout side).
- **Why plausible:** LUNCH_OPEN is afternoon US indices mean-reversion/continuation after morning move; ORB is morning breakout — low raw ρ expected; AND-filter may cut false ORB days and raise per-trade edge at cost of N.
- **Data note:** ρ(ORB,LUNCH) on train dense calendar ≈ -0.09468436781604284; LUNCH N_train=233; ORB active days≈765. Overlap count not claimed as edge — needs own PREREG if pursued.

### H-ENS-02: ORB + BTC regime gate
- **Status:** hypothesis_only — prefer S2b/S2c-style pre-registered pools over filters
- **Owner:** Strateeg-2
- **Mechanism:** Size ORB normally; add BTC US-open sleeve only when BTC realized vol or prior-day range ≥ median (cost/vol screen already favors BTC).
- **Why plausible:** S2-BTC has large bruto (+18.5 bp mean net) but power-FAIL; regime gate may stabilize N while keeping diversifier ρ≈0.11 with ORB.
- **Data note:** ρ(ORB,BTC)≈0.11297937765376753; BTC N=132. Power fix = more instruments (ETH/SOL pool) not threshold-mining on same 132.

### H-ENS-03: Stack small edges → SR≈1 (equal-vol book)
- **Status:** diagnostic_ceiling — Auditor may rebuild EV; no eval advice
- **Owner:** CTO (this deliverable) + Auditor
- **Mechanism:** Hold a book of 3–5 weak/near sleeves at equal vol contribution; scale book via recommend_scale for p_pass & p_survive (track 5).
- **Why plausible:** D-091 ambition grid: SR≳1 needed for €800/m. Single sleeves sit SR≈0.7–1.1; low pairwise ρ (see corr matrix) can lift book SR toward 1.2–1.3 on paper.
- **Data note:** See WEAK5_eqvol / ORB60_BTC25_LUNCH15 rows. Paper SR lift ≠ validated edge: FAIL_T legs remain unvalidated; book is diagnostic ceiling not candidate.

### H-ENS-04: N18 year-stability filter (REJECT as solo reopen)
- **Status:** REJECTED — would be result-dependent reopen of dead sleeve
- **Owner:** CTO (bar)
- **Mechanism:** Drop N18 2023 / trade only 2021–22 gap-cont.
- **Why plausible:** None post-hoc — 2023 mean −12 bp is instability, not a filter to invent.
- **Data note:** Explicit anti-pattern under integrity rules.

## Track 5 — FTMO sizing grids (optimize p_pass & p_survive; cap max daily loss ≤4%)

Method: sweep scale on each series; report `recommend_scale` anchor plus best-EV /
best (p_pass×p_survive) / best-survive-given (p1·p2≥0.35 ∧ EV>0) among scales with max loss ≤4%.

### F2_ORB_train
- ann SR≈1.06; daily skew≈1.17
- **recommend_scale:** scale=4.16 (max); p95=1.95%; max=4.00%; p_pass2=0.954; p_survive=0.425; EV≈€676/m
- **best net EV ≤4%:** scale=4.16; p1·p2=0.946; surv=0.425; EV≈€676/m; p95=1.94%; max=4.00%
- **best p_pass×p_survive ≤4%:** scale=0.50; p1·p2=0.000; surv=nan; EV≈€-22/m; p95=0.23%; max=0.48%
- **best survive | p1·p2≥0.35 & EV>0:** scale=1.50; p1·p2=0.428; surv=0.972; EV≈€78/m; p95=0.70%; max=1.44%

| scale | p1·p2 | p_survive | €/m EV | p95 | max | ≤4%? |
|---:|---:|---:|---:|---:|---:|:---:|
| 0.50 | 0.000 | nan | -22 | 0.23% | 0.48% | Y |
| 0.75 | 0.025 | 1.000 | -17 | 0.35% | 0.72% | Y |
| 1.00 | 0.138 | 1.000 | 1 | 0.47% | 0.96% | Y |
| 1.50 | 0.428 | 0.972 | 78 | 0.70% | 1.44% | Y |
| 2.00 | 0.635 | 0.899 | 183 | 0.93% | 1.92% | Y |
| 2.50 | 0.759 | 0.791 | 298 | 1.17% | 2.40% | Y |
| 3.00 | 0.851 | 0.672 | 416 | 1.40% | 2.88% | Y |
| 3.12 | 0.864 | 0.647 | 445 | 1.46% | 3.00% | Y |
| 3.50 | 0.905 | 0.565 | 533 | 1.64% | 3.36% | Y |
| 4.00 | 0.937 | 0.457 | 642 | 1.87% | 3.84% | Y |
| 4.16 | 0.946 | 0.425 | 676 | 1.94% | 4.00% | Y |
| 4.58 | 0.959 | 0.341 | 763 | 2.14% | 4.40% | N |
| 5.00 | 0.969 | 0.282 | 847 | 2.34% | 4.81% | N |
| 6.00 | 0.983 | 0.063 | 719 | 2.80% | 5.77% | N |
| 7.00 | 0.992 | 0.014 | 657 | 3.27% | 6.73% | N |
| 8.00 | 0.986 | 0.002 | 202 | 3.74% | 7.69% | N |

### F2_ORB_le2024
- ann SR≈0.9; daily skew≈1.20
- **recommend_scale:** scale=4.16 (max); p95=1.83%; max=4.00%; p_pass2=0.920; p_survive=0.417; EV≈€513/m
- **best net EV ≤4%:** scale=4.16; p1·p2=0.904; surv=0.418; EV≈€512/m; p95=1.82%; max=4.00%
- **best p_pass×p_survive ≤4%:** scale=0.50; p1·p2=0.000; surv=nan; EV≈€-22/m; p95=0.22%; max=0.48%
- **best survive | p1·p2≥0.35 & EV>0:** scale=2.00; p1·p2=0.500; surv=0.889; EV≈€117/m; p95=0.88%; max=1.92%

| scale | p1·p2 | p_survive | €/m EV | p95 | max | ≤4%? |
|---:|---:|---:|---:|---:|---:|:---:|
| 0.50 | 0.000 | nan | -22 | 0.22% | 0.48% | Y |
| 0.75 | 0.009 | 1.000 | -21 | 0.33% | 0.72% | Y |
| 1.00 | 0.059 | 1.000 | -11 | 0.44% | 0.96% | Y |
| 1.50 | 0.283 | 0.970 | 40 | 0.66% | 1.44% | Y |
| 2.00 | 0.500 | 0.889 | 117 | 0.88% | 1.92% | Y |
| 2.50 | 0.654 | 0.788 | 206 | 1.10% | 2.40% | Y |
| 3.00 | 0.767 | 0.668 | 298 | 1.32% | 2.88% | Y |
| 3.12 | 0.787 | 0.637 | 322 | 1.37% | 3.00% | Y |
| 3.50 | 0.840 | 0.542 | 393 | 1.54% | 3.36% | Y |
| 4.00 | 0.888 | 0.439 | 485 | 1.75% | 3.84% | Y |
| 4.16 | 0.904 | 0.418 | 512 | 1.82% | 4.00% | Y |
| 4.58 | 0.939 | 0.351 | 588 | 2.01% | 4.40% | N |
| 5.00 | 0.950 | 0.280 | 654 | 2.19% | 4.81% | N |
| 6.00 | 0.974 | 0.070 | 598 | 2.63% | 5.77% | N |
| 7.00 | 0.985 | 0.022 | 558 | 3.07% | 6.73% | N |
| 8.00 | 0.984 | 0.004 | 232 | 3.51% | 7.69% | N |

### LUNCH_OPEN_train
- ann SR≈0.65; daily skew≈5.21
- **recommend_scale:** scale=2.65 (max); p95=0.75%; max=4.00%; p_pass2=0.623; p_survive=0.605; EV≈€123/m
- **best net EV ≤4%:** scale=2.50; p1·p2=0.504; surv=0.643; EV≈€106/m; p95=0.71%; max=3.78%
- **best p_pass×p_survive ≤4%:** scale=0.50; p1·p2=0.000; surv=nan; EV≈€-22/m; p95=0.14%; max=0.76%
- **best survive | p1·p2≥0.35 & EV>0:** scale=1.98; p1·p2=0.351; surv=0.785; EV≈€52/m; p95=0.56%; max=2.99%

| scale | p1·p2 | p_survive | €/m EV | p95 | max | ≤4%? |
|---:|---:|---:|---:|---:|---:|:---:|
| 0.50 | 0.000 | nan | -22 | 0.14% | 0.76% | Y |
| 0.75 | 0.004 | 1.000 | -22 | 0.21% | 1.13% | Y |
| 1.00 | 0.032 | 1.000 | -17 | 0.28% | 1.51% | Y |
| 1.50 | 0.177 | 0.902 | 10 | 0.43% | 2.27% | Y |
| 1.98 | 0.351 | 0.785 | 52 | 0.56% | 2.99% | Y |
| 2.00 | 0.356 | 0.779 | 54 | 0.57% | 3.02% | Y |
| 2.50 | 0.504 | 0.643 | 106 | 0.71% | 3.78% | Y |
| 2.65 | 0.545 | 0.606 | 124 | 0.75% | 4.01% | N |
| 2.91 | 0.608 | 0.546 | 156 | 0.83% | 4.40% | N |
| 3.00 | 0.629 | 0.523 | 162 | 0.85% | 4.54% | N |
| 3.50 | 0.716 | 0.394 | 205 | 1.00% | 5.29% | N |
| 4.00 | 0.789 | 0.332 | 263 | 1.14% | 6.05% | N |
| 5.00 | 0.887 | 0.121 | 291 | 1.42% | 7.56% | N |
| 6.00 | 0.941 | 0.065 | 351 | 1.71% | 9.07% | N |
| 7.00 | 0.966 | 0.037 | 422 | 1.99% | 10.59% | N |
| 8.00 | 0.985 | 0.008 | 347 | 2.28% | 12.10% | N |

### ORB+BTC_eqvol
- ann SR≈1.21; daily skew≈3.74
- **recommend_scale:** scale=7.17 (max); p95=1.64%; max=4.00%; p_pass2=0.980; p_survive=0.446; EV≈€996/m
- **best net EV ≤4%:** scale=7.00; p1·p2=0.975; surv=0.466; EV≈€971/m; p95=1.60%; max=3.91%
- **best p_pass×p_survive ≤4%:** scale=0.50; p1·p2=0.000; surv=nan; EV≈€-22/m; p95=0.11%; max=0.28%
- **best survive | p1·p2≥0.35 & EV>0:** scale=2.00; p1·p2=0.503; surv=1.000; EV≈€89/m; p95=0.46%; max=1.12%

| scale | p1·p2 | p_survive | €/m EV | p95 | max | ≤4%? |
|---:|---:|---:|---:|---:|---:|:---:|
| 0.50 | 0.000 | nan | -22 | 0.11% | 0.28% | Y |
| 0.75 | 0.001 | nan | -22 | 0.17% | 0.42% | Y |
| 1.00 | 0.032 | 1.000 | -18 | 0.23% | 0.56% | Y |
| 1.50 | 0.255 | 1.000 | 19 | 0.34% | 0.84% | Y |
| 2.00 | 0.503 | 1.000 | 89 | 0.46% | 1.12% | Y |
| 2.50 | 0.651 | 0.997 | 173 | 0.57% | 1.40% | Y |
| 3.00 | 0.755 | 0.968 | 264 | 0.69% | 1.67% | Y |
| 3.50 | 0.821 | 0.928 | 358 | 0.80% | 1.95% | Y |
| 4.00 | 0.863 | 0.882 | 451 | 0.91% | 2.23% | Y |
| 5.00 | 0.926 | 0.748 | 637 | 1.14% | 2.79% | Y |
| 5.37 | 0.940 | 0.694 | 703 | 1.23% | 3.00% | Y |
| 6.00 | 0.957 | 0.607 | 810 | 1.37% | 3.35% | Y |
| 7.00 | 0.975 | 0.466 | 971 | 1.60% | 3.91% | Y |
| 7.17 | 0.978 | 0.446 | 996 | 1.64% | 4.00% | N |
| 7.88 | 0.986 | 0.355 | 1098 | 1.80% | 4.40% | N |
| 8.00 | 0.987 | 0.340 | 1116 | 1.83% | 4.47% | N |

### ORB60_BTC25_LUNCH15
- ann SR≈1.36; daily skew≈2.17
- **recommend_scale:** scale=7.78 (max); p95=1.89%; max=4.00%; p_pass2=0.991; p_survive=0.469; EV≈€1177/m
- **best net EV ≤4%:** scale=7.78; p1·p2=0.989; surv=0.470; EV≈€1177/m; p95=1.89%; max=4.00%
- **best p_pass×p_survive ≤4%:** scale=0.50; p1·p2=0.000; surv=nan; EV≈€-22/m; p95=0.12%; max=0.26%
- **best survive | p1·p2≥0.35 & EV>0:** scale=2.00; p1·p2=0.539; surv=0.998; EV≈€92/m; p95=0.49%; max=1.03%

| scale | p1·p2 | p_survive | €/m EV | p95 | max | ≤4%? |
|---:|---:|---:|---:|---:|---:|:---:|
| 0.50 | 0.000 | nan | -22 | 0.12% | 0.26% | Y |
| 0.75 | 0.001 | nan | -22 | 0.18% | 0.39% | Y |
| 1.00 | 0.029 | 1.000 | -18 | 0.24% | 0.51% | Y |
| 1.50 | 0.280 | 1.000 | 19 | 0.37% | 0.77% | Y |
| 2.00 | 0.539 | 0.998 | 92 | 0.49% | 1.03% | Y |
| 2.50 | 0.701 | 0.998 | 181 | 0.61% | 1.29% | Y |
| 3.00 | 0.797 | 0.990 | 277 | 0.73% | 1.54% | Y |
| 3.50 | 0.858 | 0.964 | 378 | 0.85% | 1.80% | Y |
| 4.00 | 0.899 | 0.934 | 477 | 0.97% | 2.06% | Y |
| 5.00 | 0.945 | 0.834 | 676 | 1.22% | 2.57% | Y |
| 5.84 | 0.969 | 0.738 | 838 | 1.42% | 3.00% | Y |
| 6.00 | 0.972 | 0.720 | 870 | 1.46% | 3.08% | Y |
| 7.00 | 0.983 | 0.583 | 1055 | 1.70% | 3.60% | Y |
| 7.78 | 0.989 | 0.470 | 1177 | 1.89% | 4.00% | Y |
| 8.00 | 0.990 | 0.440 | 1212 | 1.95% | 4.11% | N |
| 8.56 | 0.990 | 0.363 | 1271 | 2.08% | 4.40% | N |

### WEAK5_eqvol
- ann SR≈1.62; daily skew≈2.97
- **recommend_scale:** scale=6.28 (max); p95=0.81%; max=4.00%; p_pass2=0.954; p_survive=0.909; EV≈€614/m
- **best net EV ≤4%:** scale=6.28; p1·p2=0.944; surv=0.910; EV≈€614/m; p95=0.81%; max=4.00%
- **best p_pass×p_survive ≤4%:** scale=0.50; p1·p2=0.000; surv=nan; EV≈€-22/m; p95=0.06%; max=0.32%
- **best survive | p1·p2≥0.35 & EV>0:** scale=2.50; p1·p2=0.491; surv=1.000; EV≈€65/m; p95=0.32%; max=1.59%

| scale | p1·p2 | p_survive | €/m EV | p95 | max | ≤4%? |
|---:|---:|---:|---:|---:|---:|:---:|
| 0.50 | 0.000 | nan | -22 | 0.06% | 0.32% | Y |
| 0.75 | 0.000 | nan | -22 | 0.10% | 0.48% | Y |
| 1.00 | 0.001 | nan | -22 | 0.13% | 0.64% | Y |
| 1.50 | 0.065 | 1.000 | -15 | 0.19% | 0.96% | Y |
| 2.00 | 0.266 | 1.000 | 15 | 0.26% | 1.27% | Y |
| 2.50 | 0.491 | 1.000 | 65 | 0.32% | 1.59% | Y |
| 3.00 | 0.646 | 1.000 | 128 | 0.39% | 1.91% | Y |
| 3.50 | 0.748 | 0.999 | 198 | 0.45% | 2.23% | Y |
| 4.00 | 0.811 | 0.995 | 271 | 0.51% | 2.55% | Y |
| 4.71 | 0.875 | 0.973 | 377 | 0.61% | 3.00% | Y |
| 5.00 | 0.894 | 0.967 | 421 | 0.64% | 3.18% | Y |
| 6.00 | 0.935 | 0.923 | 572 | 0.77% | 3.82% | Y |
| 6.28 | 0.944 | 0.910 | 614 | 0.81% | 4.00% | Y |
| 6.91 | 0.957 | 0.858 | 708 | 0.89% | 4.40% | N |
| 7.00 | 0.959 | 0.851 | 722 | 0.90% | 4.46% | N |
| 8.00 | 0.974 | 0.666 | 837 | 1.03% | 5.09% | N |

## Readout (CTO)

1. **Anchor remains F2-ORB** (train SR≈1.0+, le2024 reference EV from recommend_scale).
2. **Low correlations** across ORB / BTC / LUNCH / N18 → paper diversification is real; XAU still negligible (N=12).
3. **FAIL_T legs (N11/N18/LUNCH) must not be reopened solo** — portfolio rows are diagnostic ceilings showing how stacking *could* lift SR toward ≈1.2, not candidates.
4. **Track 5:** for positive-skew sparse sleeves (LUNCH), recommend_scale often binds on **max** daily loss before p95; lower scale raises p_survive at the cost of EV — use the survive-under-gate column when ambition is pass-rate not €/m max.
5. **ORB+BTC** still the strongest *paper* two-sleeve book; +LUNCH can help survive if BTC stress-held; treat as research direction for CEO ensemble PREREG (H-ENS-01/03), not eval advice.
6. **Manager NEXT_STEPS:** v63 (`7c4b4a6`, 08:03 CEST) absorbed — D-094/D-094a FREEZE OFF; tracks 3+5 explicitly assigned to CTO. C-018 is the first CTO deliverable under v63.
7. No reserve 2025+ opened. No real money / no FTMO signup.

