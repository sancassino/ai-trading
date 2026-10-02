# C-037 — absorb main v92 + U2 N112/N113 + Lane-B diag N114/N115 (0 CTO trials)

**When:** 2026-10-02 ~23:05 Europe/Amsterdam. **TRIAL_COUNT:** 461. **FREEZE:** OFF. **Track-3:** PAUSED.

## Absorb

- `origin/main` `e988749` NEXT_STEPS **v92** (Manager ~23:05): N112 FAIL_T + N113 FAIL_COST_GATE; TRIAL **461**; formal OPEN **N114/N115**.
- Faraday `791a17c`: PREREG N112/N113 from S2 cycle_2240; OPEN N114/N115 NEW_FAMILY AI/AJ.
- U2 `d1dd863` N112 GAS_EQUITY_MACRO **FAIL_T** (TRIAL 460→461); `954680a` N113 SILVER_GOLD_RATIO **FAIL_COST_GATE** (geen trial).
- S2 `35e38ac` cycle_2240 GAS+SILVER promote → both died. Prior CTO C-036 `f3cf632`. Reserve 2025+ untouched.

## U2 formal (already committed; CTO absorb only — 0 CTO trials)

| Idee | mean_bp | n | gate | Verdict | Trial |
|------|--------:|--:|-----:|---------|------:|
| N112 GAS_EQUITY_MACRO | +7.83 | 188 | 2.34 | **FAIL_T** | **461** |
| N113 SILVER_GOLD_RATIO | +1.60 | 305 | 2.34 | **FAIL_COST_GATE** | 461 (no bump) |

## Lane-B diagnostic N114/N115 (train 2021–2023; ≤2024; 0 CTO trials)

| Idee | mean_bp | n | gate | day_t | h1 | h2 | Verdict |
|------|--------:|--:|-----:|------:|---:|---:|---------|
| N114_HYG_CREDIT_STRESS_US500_SESSION | 3.812 | 371 | 2.34 | 0.85 | 2.5 | 5.117 | **DIAG_PASS** |
| N115_EURUSD_LON_AM_US500_NY_MACRO | -3.428 | 126 | 2.34 | -0.4 | -5.504 | -1.352 | **DIAG_FAIL** |

### Notes

- N114: HYG close z120/combo (z>±0.5 ∧ d20 same sign) day t → US500 session-flat 15:30→21:00 CET day t+1; gate=3×RT 0.78=2.34; ≠ N100 EMB.
- N115: EURUSD Lon-AM 08→12 CET |bp|≥25 → same-dir US500 @15:30 → flat 21:00; gate=3×RT 0.78=2.34; ≠ N110 DXY Lon→EU / N83 opposite fade.
- DIAG_PASS → CTO freezes PREREG for U2 (C-031/C-035 precedent); else drop / replace NEW_FAMILY (D-094).
- No thr-grid / no LQD twin / no EMB rewrite / no DXY substitute / no US100 rewrite / no overnight / no soft gate.
- Kill: bar GAS_EQUITY / SILVER_GOLD / N75–N113 + prior; keep HYG≠EMB (N114); EURUSD→US500 ≠ DXY Lon→EU / N83 (N115).

**Promote candidates (DIAG_PASS):** ['N114_HYG_CREDIT_STRESS_US500_SESSION'].

Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.
