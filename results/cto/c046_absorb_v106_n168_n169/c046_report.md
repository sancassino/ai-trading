# C-046 — absorb main v106 + Faraday 0019de4; Lane-B diag N168/N169 (0 CTO trials)

**When:** 2026-10-04 ~00:05 Europe/Amsterdam. **TRIAL_COUNT:** 471. **FREEZE:** OFF. **Track-3:** PAUSED. **Live PREREG:** none.

## Absorb

- Main `03ac200` NEXT_STEPS **v106** (~23:37): C-045 N164/N165 DIAG_FAIL; OPEN empty; U2 IDLE TRIAL 471; Faraday tip still `218eb11`.
- Faraday `0019de4` (~00:03): S2 `885090b` → **N166 FAIL_CLONE** (HYG) / **N167 FAIL**; absorb C-045; OPEN **N168 US30_EUROPE_INVENTORY_FADE CK** / **N169 GBPUSD_LONDON_FIX_RESIDUAL_FADE CL**.
- U2 `c5a0a4d` (~23:45): IDLE/HOLD absorb v106; TRIAL **471**; no live PREREG.
- S2 `885090b` LQD+EWY consumed via N166/N167. Prior CTO C-045 `71d3b5e`. CEO `7cb6731` no new D-*. Reserve 2025+ untouched.

## Faraday N166/N167 (not re-screened)

- **N166** LQD→US500: FAIL_CLONE (HYG agree 0.95 cover 0.78); mean +7.59 ≥ 2.34 — NEW_FAMILY CI dead.
- **N167** EWY→EURUSD: FAIL (mean −1.10 < 1.89) — NEW_FAMILY CJ dead.

## Lane-B diagnostic N168/N169 (train 2021–2023; ≤2024; 0 CTO trials)

| Idee | mean_bp | n | gate | day_t | h1 | h2 | L/S | years | clones | Verdict |
|------|--------:|--:|-----:|------:|---:|---:|----:|-------|--------|---------|
| N168_US30_EUROPE_INVENTORY_FADE | 3.049 | 214 | 1.35 | 1.465 | 1.971 | 4.127 | 110/104 | 2021:1.264/2022:2.915/2023:5.891 | US500_europe_same_window_twin,US100_europe_same_window_twin | **DIAG_FAIL_CLONE** |
| N169_GBPUSD_LONDON_FIX_RESIDUAL_FADE | -0.262 | 249 | 2.0999999999999996 | -0.15 | 0.051 | -0.572 | 123/126 | 2021:-1.241/2022:2.887/2023:-5.006 | — | **DIAG_FAIL** |

### Clone detail

- N168 vs US500 europe same-window: {'peer': 'US500_europe_same_window_twin', 'sign_agree': 0.9943, 'cover': 0.8224, 'n_cand': 214, 'n_both': 176, 'clone': True}
- N168 vs US100 europe same-window: {'peer': 'US100_europe_same_window_twin', 'sign_agree': 0.9812, 'cover': 0.7477, 'n_cand': 214, 'n_both': 160, 'clone': True}
- N168 vs US30 PM N20-proxy: {'peer': 'US30_PM_window_N20_proxy', 'sign_agree': 0.4722, 'cover': 0.5047, 'n_cand': 214, 'n_both': 108, 'clone': False}
- N168 vs US30 cash-close N162-proxy: {'peer': 'US30_cash_close_N162_proxy', 'sign_agree': 0.5207, 'cover': 0.5654, 'n_cand': 214, 'n_both': 121, 'clone': False}
- N169 vs EURUSD fix same-window: {'peer': 'EURUSD_fix_same_window_twin', 'sign_agree': 0.9864, 'cover': 0.5904, 'n_cand': 249, 'n_both': 147, 'clone': False}
- N169 vs AUDUSD fix same-window: {'peer': 'AUDUSD_fix_same_window_twin', 'sign_agree': 0.9704, 'cover': 0.6787, 'n_cand': 249, 'n_both': 169, 'clone': False}
- N169 vs GBPUSD midday N29-proxy: {'peer': 'GBPUSD_midday_N29_proxy', 'sign_agree': 0.4757, 'cover': 0.4137, 'n_cand': 249, 'n_both': 103, 'clone': False}
- N169 vs GBPUSD morning N38-proxy: {'peer': 'GBPUSD_morning_N38_proxy', 'sign_agree': 0.4833, 'cover': 0.4819, 'n_cand': 249, 'n_both': 120, 'clone': False}

### Notes

- N168: US30cash Europe inventory impulse 09:00→12:00 fade ±25 bp; entry@12:00 flat 15:00; gate=1.35 (3×RT 0.45); NEW_FAMILY CK.
- N169: GBPUSD London-fix residual impulse 17:00→18:00 fade ±15 bp; entry@18:00 flat 20:30; gate=2.10 (3×RT 0.70; not US500 2.34); NEW_FAMILY CL.
- Formal OPEN after this cycle depends on DIAG verdicts.
- No thr-grid / no overnight / no soft gate / no twin remap / no 2025+.

## Verdict summary

- **N168_US30_EUROPE_INVENTORY_FADE**: **DIAG_FAIL_CLONE** (n=214, mean=3.049, gate=1.35)
- **N169_GBPUSD_LONDON_FIX_RESIDUAL_FADE**: **DIAG_FAIL** (n=249, mean=-0.262, gate=2.0999999999999996)

**Promote to PREREG:** none.

