# D-092.1 N158/N159 pre-screen (train 2021–2023)

- **N158 USOIL_NY_IMPULSE_FADE**: N=491 mean=-0.5736 med=0.1668 gate=10.02 → **FAIL** years={'2021': -9.4327, '2022': -5.4813, '2023': 12.9216} L/S=221/270 hits=[] meta={'n_impulse_days': 491, 'n_skip_missing_bar': 0, 'n_trades': 491, 'swap_bp': 0, 'overnight': False, 'train_days': 774, 'session': 'signal 15:30→17:00 entry at 17:00 flat 21:00 CET', 'rt_in_costs': True}
- **N159 GER40_EUROPE_CLOSE_FADE**: N=141 mean=-4.3397 med=-1.802 gate=2.16 → **FAIL** years={'2022': -2.988, '2023': -7.1312} L/S=70/71 hits=[] meta={'n_impulse_days': 167, 'n_skip_missing_bar': 26, 'n_trades': 141, 'swap_bp': 0, 'overnight': False, 'train_days': 768, 'session': 'signal 12:00→15:00 entry 15:30 flat 17:30 CET', 'rt_in_costs': True}

Gates from COSTS_FTMO.csv round-trips. Session-flat so swap=0 is in the gate. No thr-grid. No 2024+ selection. No overnight. No second leg.
