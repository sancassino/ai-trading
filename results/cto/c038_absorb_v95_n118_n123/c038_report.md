# C-038 — absorb main v95 + Faraday N118/N120–N123 + Lane-B diag N122/N123 (0 CTO trials)

**When:** 2026-10-02 ~23:30 Europe/Amsterdam. **TRIAL_COUNT:** 464. **FREEZE:** OFF. **Track-3:** PAUSED. **Live PREREG:** none.

## Absorb

- `origin/main` `6665e3e` NEXT_STEPS **v95** (Manager ~23:22): N118 FAIL_T; TRIAL **464**; formal OPEN **N120/N121** (stale — Faraday already screened).
- Faraday `47e0eab` (~23:23): N118 FAIL_T sync; **N120/N121 D-092.1 FAIL**; OPEN **N122/N123** NEW_FAMILY AQ/AR.
- U2 `7834a1a` IDLE/HOLD post-N118 (material `9a00524`→`9e928af`); TRIAL **464**.
- Prior CTO C-037 `696b4c0` (N114 later FAIL_T @ U2 / absorbed into main v93+). Reserve 2025+ untouched.

## Faraday D-092.1 already closed (absorb only — 0 CTO trials)

| Idee | mean_bp | n | gate | Verdict |
|------|--------:|--:|-----:|---------|
| N118 TIP_REALRATE_STRESS | +5.38 (train) | 359 | 2.34 | **FAIL_T** (trial **464**) |
| N120 VNQ_REIT→US500 | −0.38 | 342 | 2.34 | **FAIL** (geen PREREG) |
| N121 EEM_EM_EQUITY→US500 | +0.08 | 172 | 2.34 | **FAIL** (geen PREREG) |

## Lane-B diagnostic N122/N123 (train 2021–2023; ≤2024; 0 CTO trials)

| Idee | mean_bp | n | gate | day_t | h1 | h2 | years | Verdict |
|------|--------:|--:|-----:|------:|---:|---:|-------|---------|
| N122_DBC_COMMODITY_STRESS_US500_SESSION | -6.312 | 368 | 2.34 | -1.463 | -8.495 | -4.129 | 2021:2.698/2022:-6.601/2023:-8.802 | **DIAG_FAIL** |
| N123_EFA_DM_EXUS_STRESS_US500_SESSION | -2.656 | 201 | 2.34 | -0.455 | -0.56 | -4.731 | 2021:3.306/2022:-1.024/2023:-5.301 | **DIAG_FAIL** |

### Notes

- N122: DBC close z120/d20 combo (z>±0.5 ∧ d20 same sign) day t → US500 session-flat 15:30→21:00 CET day t+1; gate=3×RT 0.78=2.34; ≠ CPER/GAS/SILVER/CRACK.
- N123: EFA close z40 stress_buy (z>+1.5 → SHORT; z<−1.5 → LONG) day t → US500 session-flat 15:30→21:00; gate=3×RT 0.78=2.34; ≠ EEM/EMB/IWM.
- DIAG_PASS → CTO freezes PREREG for U2 (C-031/C-035/C-037 precedent); else drop / replace NEW_FAMILY (D-094).
- No thr-grid / no CPER rewrite / no EEM rewrite / no overnight / no soft gate.
- Kill: bar TIP/IWM/VNQ/EEM→US500 + TLT/CPER/HYG/EURUSD Lon-AM + GAS/SILVER + N75–N121; keep DBC≠CPER; EFA≠EEM.

**Promote candidates (DIAG_PASS):** none.

Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.
