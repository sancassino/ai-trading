# C-031 — N87 FAIL_T absorb + Lane-B diag N90–N92 (0 trials)

**When:** 2026-10-02 ~20:31 Europe/Amsterdam. **TRIAL_COUNT:** 457. **FREEZE:** OFF.

## Absorb

- Merged `origin/main` @ `054a8eb` (NEXT_STEPS **v83** — D-101…D-104 + N87 FAIL_T; TRIAL **457**).
- U2 `3a9108e` **N87** US30 opening-gap fade → **FAIL_T** (t_NW 1.63; test −17.71 bp). Dead += `N87_US30_GAP_FADE`.
- **D-104** ORB-meta reserve FAIL → ORB-as-robust-edge closed. No ORB-meta / ORB-index-ext clones.
- U2 tip `6f6ef86` IDLE/HOLD until PASS→PREREG. Track-3 PAUSED. Reserve 2025+ untouched.

## Lane-B diagnostic (train 2021–2023; ≤2024; 0 trials)

| Idee | mean_bp | n | gate | day_t | h1 | h2 | Verdict |
|------|--------:|--:|-----:|------:|---:|---:|---------|
| N90_GBPJPY_CARRY_MOM_5D | 10.154 | 113 | 2.16 | 0.843 | 22.175 | -1.657 | **UNDERPOWERED** |
| N91_AUDUSD_CARRY_MOM_5D | -18.591 | 101 | 1.35 | -1.207 | -31.68 | -5.759 | **DIAG_FAIL** |
| N92_US100_NY_2H_MOM | 5.904 | 592 | 1.98 | 1.56 | 4.181 | 7.627 | **DIAG_PASS** |

### Notes

- N90/N91: dayclose ≤22:00 from M5; ret5>0 → long; hold 5d non-overlap; swap earn not credited in gate (D-100).
- N92: NY 15:30–17:30 CET direction → hold to 22:00; bilateral; intradag-flat (≠ ORB breakout).
- DIAG_PASS → Strateeg may freeze PREREG; DIAG_FAIL/UNDERPOWERED → drop / replace with NEW_FAMILY (D-094).
- CTO does **not** freeze PREREG here (Lane-B ownership = Strateeg); diagnostic only to unblock drought.

**Promote candidates (DIAG_PASS):** ['N92_US100_NY_2H_MOM'].

Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.
