# C-044 — absorb main v104 + Faraday 7c1a880; Lane-B diag N162/N163 (0 CTO trials)

**When:** 2026-10-03 ~22:57 Europe/Amsterdam. **TRIAL_COUNT:** 471. **FREEZE:** OFF. **Track-3:** PAUSED. **Live PREREG:** none.

## Absorb

- Main `95624bb` NEXT_STEPS **v104** (~02:07): Faraday tip `7c1a880` N154–N160 FAIL + N161 PASS→PREREG; U2 `03a1a1d` N161 FAIL_T **TRIAL 471**; OPEN N162/N163; C-043.
- Faraday `7c1a880` (~02:02): **N160 FAIL** (−7.15 < 15.21) / **N161 PASS→PREREG** (then FAIL_T @ U2); OPEN **N162 US500_CASH_CLOSE_FADE CE** / **N163 AUDUSD_NY_IMPULSE_FADE CF**. WT left `results/R2/n162_n163_prescreen/` uncommitted (both FAIL_CLONE).
- U2 `03a1a1d` (~02:04): **N161 FAIL_T** (TRIAL **470→471**); IDLE/HOLD; no live PREREG.
- S2 `51b24bf` XLK_TECH consumed via N161. Prior CTO C-043 `c27849d`: N158/N159 DIAG_FAIL. Reserve 2025+ untouched.
- Catch-up: prior CTO routine ~22:25 CEST FAILED; this cycle absorbs ~21h of teammate tips.

## Lane-B diagnostic N162/N163 (train 2021–2023; ≤2024; 0 CTO trials)

| Idee | mean_bp | n | gate | day_t | h1 | h2 | L/S | years | clones | Verdict |
|------|--------:|--:|-----:|------:|---:|---:|----:|-------|--------|---------|
| N162_US500_CASH_CLOSE_FADE | -0.308 | 217 | 2.34 | -0.182 | -2.458 | 1.822 | 114/103 | 2021:-3.98/2022:-0.326/2023:0.651 | US30_same_window_twin_BARRED,US100_same_window_twin_BARRED | **DIAG_FAIL_CLONE** |
| N163_AUDUSD_NY_IMPULSE_FADE | -1.674 | 296 | 3.66 | -0.76 | 1.472 | -4.821 | 147/149 | 2021:-2.606/2022:-0.498/2023:-2.322 | NZD_same_window_twin_BARRED | **DIAG_FAIL_CLONE** |

### Clone detail

- N162 vs US30 same-window: {'peer': 'US30_same_window_twin_BARRED', 'sign_agree': 1.0, 'cover': 0.7926, 'n_cand': 217, 'n_both': 172, 'clone': True}
- N162 vs US100 same-window: {'peer': 'US100_same_window_twin_BARRED', 'sign_agree': 1.0, 'cover': 0.8986, 'n_cand': 217, 'n_both': 195, 'clone': True}
- N163 vs NZD same-window: {'peer': 'NZD_same_window_twin_BARRED', 'sign_agree': 1.0, 'cover': 0.7973, 'n_cand': 296, 'n_both': 236, 'clone': True}

### Notes

- N162: US500cash cash-close impulse 19:00→20:30 fade ±25 bp; entry@20:30 flat 21:00; gate=3×0.78=2.34; NEW_FAMILY CE.
- N163: AUDUSD NY-hour impulse 15:30→17:00 fade ±20 bp; entry@17:00 flat 21:00; gate=3×1.22=3.66 (NOT US500 2.34); NEW_FAMILY CF.
- Absorbed Faraday N154–N161 FAIL/FAIL_CLONE/FAIL_T (no re-run). Formal OPEN after this cycle = **empty**.
- Agrees Faraday uncommitted WT prescreen (both FAIL_CLONE + mean < gate).
- No thr-grid / no overnight / no soft gate / no twin remap / no PREREG.

**Promote candidates (DIAG_PASS):** none.

Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.
