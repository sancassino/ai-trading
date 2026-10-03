# C-045 — absorb main v105 + Faraday 218eb11; Lane-B diag N164/N165 (0 CTO trials)

**When:** 2026-10-03 ~23:30 Europe/Amsterdam. **TRIAL_COUNT:** 471. **FREEZE:** OFF. **Track-3:** PAUSED. **Live PREREG:** none.

## Absorb

- Main `31af9f2` NEXT_STEPS **v105** (~23:09): C-044 N162/N163 DIAG_FAIL_CLONE; OPEN empty; U2 IDLE TRIAL 471; Faraday tip still `7c1a880`.
- Faraday `218eb11` (~23:23): absorb C-044; OPEN **N164 US2000_NY_IMPULSE_FADE CG** / **N165 EURCHF_LONDON_HAVEN_FADE CH**; commit n162_n163_prescreen (FAIL_CLONE both).
- U2 `69c1a34` (~23:15): IDLE/HOLD absorb v105; TRIAL **471**; no live PREREG (after N161 FAIL_T `03a1a1d`).
- S2 `51b24bf` XLK consumed. Prior CTO C-044 `02ed02b`. CEO `7cb6731` no new D-*. Reserve 2025+ untouched.

## Lane-B diagnostic N164/N165 (train 2021–2023; ≤2024; 0 CTO trials)

| Idee | mean_bp | n | gate | day_t | h1 | h2 | L/S | years | clones | Verdict |
|------|--------:|--:|-----:|------:|---:|---:|----:|-------|--------|---------|
| N164_US2000_NY_IMPULSE_FADE | 1.567 | 493 | 9.43 | 0.402 | 7.459 | -4.3 | 254/239 | 2021:4.297/2022:3.55/2023:-3.715 | — | **DIAG_FAIL** |
| N165_EURCHF_LONDON_HAVEN_FADE | -2.233 | 259 | 3.45 | -1.868 | -2.015 | -2.449 | 137/122 | 2021:-1.437/2022:-3.188/2023:-1.227 | — | **DIAG_FAIL** |

### Clone detail

- N164 vs US500 same-window: {'peer': 'US500_same_window_twin_BARRED', 'sign_agree': 0.9716, 'cover': 0.357, 'n_cand': 493, 'n_both': 176, 'clone': False}
- N164 vs US30 same-window: {'peer': 'US30_same_window_twin_BARRED', 'sign_agree': 0.9402, 'cover': 0.3732, 'n_cand': 493, 'n_both': 184, 'clone': False}
- N164 vs US100 same-window: {'peer': 'US100_same_window_twin_BARRED', 'sign_agree': 0.8356, 'cover': 0.4442, 'n_cand': 493, 'n_both': 219, 'clone': False}
- N165 vs GBPCHF same-window: {'peer': 'GBPCHF_same_window_twin_BARRED', 'sign_agree': 0.9176, 'cover': 0.6564, 'n_cand': 259, 'n_both': 170, 'clone': False}
- N165 vs USDCHF same-window: {'peer': 'USDCHF_same_window_twin_BARRED', 'sign_agree': 0.8214, 'cover': 0.5405, 'n_cand': 259, 'n_both': 140, 'clone': False}
- N165 vs AUDCHF same-window: {'peer': 'AUDCHF_same_window_twin_BARRED', 'sign_agree': 0.8779, 'cover': 0.6641, 'n_cand': 259, 'n_both': 172, 'clone': False}

### Notes

- N164: US2000cash NY-hour impulse 15:30→17:00 fade ±35 bp; entry@17:00 flat 21:00; gate=9.43 (3×RT_est 3.14; not in COSTS); NEW_FAMILY CG.
- N165: EURCHF London-AM impulse 08:00→11:30 fade ±15 bp; entry@11:30 flat 15:00; gate=3.45 (3×RT_est 1.15; not in COSTS); NEW_FAMILY CH.
- Formal OPEN after this cycle = **empty** (neither DIAG_PASS) OR promote if DIAG_PASS.
- No thr-grid / no overnight / no soft gate / no twin remap.

## Verdict summary

- **N164_US2000_NY_IMPULSE_FADE**: **DIAG_FAIL** (n=493, mean=1.567, gate=9.43)
- **N165_EURCHF_LONDON_HAVEN_FADE**: **DIAG_FAIL** (n=259, mean=-2.233, gate=3.45)

**Promote to PREREG:** none.

