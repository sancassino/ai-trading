# C-032 — N92 FAIL_T + N93 FAIL_COST_GATE absorb + Lane-B diag N94/N95 (0 trials)

**When:** 2026-10-02 ~21:05 Europe/Amsterdam. **TRIAL_COUNT:** 458. **FREEZE:** OFF.

## Absorb

- Merged `origin/main` @ `615b9af` (NEXT_STEPS **v86** — N93 FAIL_COST_GATE; TRIAL **458**; N94/N95 OPEN).
- U2 `b5b59e0` **N92** US100 NY 2h mom → **FAIL_T** (t_NW 1.56; test t 0.51). Dead += `N92_US100_NY_2H_MOM`. TRIAL **458**.
- U2 `b382307` **N93** SECTOR_DISP_ROTATION → **FAIL_COST_GATE** (mean +0.99 ≪ 1.98; geen trial). Dead += `N93_SECTOR_DISP_ROTATION`.
- U2 tip IDLE/HOLD until next PASS→PREREG. Track-3 PAUSED. Reserve 2025+ untouched.

## Lane-B diagnostic (train 2021–2023; ≤2024; 0 trials)

| Idee | mean_bp | n | gate | day_t | h1 | h2 | Verdict |
|------|--------:|--:|-----:|------:|---:|---:|---------|
| N94_NZDJPY_LO_CARRY_MOM_5D | -0.968 | 107 | 6.0 | -0.067 | 18.071 | -19.654 | **DIAG_FAIL** |
| N95_XAU_LON_AM_NY_CONT | 1.398 | 226 | 2.49 | 0.304 | 4.695 | -1.898 | **DIAG_FAIL** |

### Notes

- N94: NZDJPY dayclose ≤22:00; ret5>0 → long; hold 5d non-overlap; swap earn not credited in gate (D-100).
- N95: XAU |am_bp 08–11|≥25 → side at 15:30 → flat 21:00; bilateral; intradag-flat.
- DIAG_PASS → CTO freezes PREREG for U2 (C-031 precedent); else drop / replace NEW_FAMILY (D-094).

**Promote candidates (DIAG_PASS):** none.

Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.
