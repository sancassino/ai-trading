# D-092.1 N146/N147 pre-screen (train 2021–2023)

- **N146 AUD_XAU_COMMODITY_XS**: N=200 mean=-1.5592 med=-2.1091 gate=6.15 → **FAIL** years={'2021': -0.5091, '2022': -0.3658, '2023': -3.1873} L/S=138/62 hits=[] meta={'n_signal_days': 200, 'n_skip_missing_bar': 0, 'n_ratio_days': 773, 'ratio_first': '2021-01-04', 'ratio_last': '2023-12-29', 'train_days': {'AUDUSD': 778, 'XAUUSD': 774}, 'rt_in_costs': True, 'swap_bp': 0, 'session': '15:30-21:00 CET cheapest side (overnight swap excluded)'}
- **N147 GBP_UKOIL_PETRO_XS**: N=188 mean=-3.2171 med=0.7085 gate=10.23 → **FAIL_CLONE** years={'2021': -45.7238, '2022': 15.8204, '2023': -8.5982} L/S=107/81 hits=['XAU_UKOIL_z40_N140', 'N140_XAU_UKOIL_sign'] meta={'n_signal_days': 231, 'n_skip_missing_bar': 43, 'n_ratio_days': 773, 'ratio_first': '2021-01-04', 'ratio_last': '2023-12-29', 'train_days': {'GBPUSD': 778, 'UKOILcash': 773}, 'rt_in_costs': True, 'swap_bp': 0, 'session': '15:30-21:00 CET cheapest side (UKOIL short swap 27.03 not in alpha)'}

Gates from COSTS_FTMO.csv round-trips. Session-flat so swap=0 is in the gate. No thr-grid. No 2024+ selection. No softer session spread.
