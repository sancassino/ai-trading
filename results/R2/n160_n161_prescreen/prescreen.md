# D-092.1 N160/N161 pre-screen (train 2021–2023)

- **N160 XAG_NY_IMPULSE_FADE**: N=451 mean=-7.1513 med=-5.7519 gate=15.21 → **FAIL** years={'2021': -3.29, '2022': -8.8264, '2023': -9.027} L/S=222/229 hits=[] meta={'n_impulse_days': 451, 'n_skip_missing_bar': 0, 'n_trades': 451, 'swap_bp': 0, 'overnight': False, 'train_days': 774, 'session': 'signal 15:30→17:00 entry at 17:00 flat 21:00 CET', 'rt_in_costs': True}
- **N161 XLK_TECH_SECTOR_STRESS session-flat**: N=383 mean=5.4198 med=9.77 gate=1.98 → **PASS_may_PREREG** years={'2021': -10.6781, '2022': 6.8373, '2023': 9.2569} L/S=242/141 hits=[] meta={'n_signal_days_with_session': 520, 'n_skip_missing_bar': 137, 'n_trades': 383, 'swap_bp': 0, 'overnight': False, 'hold': 'session-flat 15:30→21:00 not 3d', 'train_days': 775, 'rt_in_costs': True, 'lane_a_day_t': 2.05, 'lane_a_day_t_is_not_a_pass': True}

Gates from COSTS_FTMO.csv round-trips. Session-flat so swap=0 is in the gate. No thr-grid. No 2024+ selection. No overnight. N161 is not a 3-day hold. Lane-A day_t 2.05 is not a PASS.
