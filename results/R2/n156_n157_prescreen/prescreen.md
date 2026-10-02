# D-092.1 N156/N157 pre-screen (train 2021–2023)

- **N156 XAU_GER40_HAVEN_DAX_XS**: N=146 mean=-2.4554 med=-3.787 gate=4.65 → **FAIL** years={'2022': -13.1458, '2023': 9.4745} L/S=66/80 hits=[] meta={'n_signal_days': 205, 'n_skip_missing_bar': 59, 'n_ratio_days': 767, 'ratio_first': '2021-01-04', 'ratio_last': '2023-12-29', 'b_sign': -1, 'train_days': {'XAUUSD': 774, 'GER40cash': 768}, 'rt_in_costs': True, 'swap_bp': 0, 'session': '15:30-21:00 CET cheapest side (overnight swap excluded)'}
- **N157 XAU_US100_HAVEN_NASDAQ_XS**: N=174 mean=-1.8206 med=-1.0583 gate=4.47 → **FAIL** years={'2021': 22.7932, '2022': -3.1616, '2023': -7.0394} L/S=69/105 hits=[] meta={'n_signal_days': 216, 'n_skip_missing_bar': 42, 'n_ratio_days': 773, 'ratio_first': '2021-01-04', 'ratio_last': '2023-12-29', 'b_sign': -1, 'train_days': {'XAUUSD': 774, 'US100cash': 775}, 'rt_in_costs': True, 'swap_bp': 0, 'session': '15:30-21:00 CET cheapest side (overnight swap excluded)'}

Gates from COSTS_FTMO.csv round-trips. Session-flat so swap=0 is in the gate. No thr-grid. No 2024+ selection. No softer session spread. No single-leg rewrite.
