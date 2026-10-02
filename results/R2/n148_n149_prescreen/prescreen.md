# D-092.1 N148/N149 pre-screen (train 2021–2023)

- **N148 USDJPY_US100_RISK_XS**: N=217 mean=3.3053 med=0.9616 gate=4.32 → **FAIL** years={'2021': 23.984, '2022': 8.5469, '2023': -6.6712} L/S=106/111 hits=[] meta={'n_signal_days': 262, 'n_skip_missing_bar': 45, 'n_ratio_days': 775, 'ratio_first': '2021-01-04', 'ratio_last': '2023-12-29', 'train_days': {'USDJPY': 778, 'US100cash': 775}, 'rt_in_costs': True, 'swap_bp': 0, 'session': '15:30-21:00 CET cheapest side (overnight swap excluded)'}
- **N149 EURUSD_GER40_EUROPE_XS**: N=140 mean=2.0462 med=5.3309 gate=4.05 → **FAIL** years={'2022': 1.2005, '2023': 3.3148} L/S=70/70 hits=[] meta={'n_signal_days': 215, 'n_skip_missing_bar': 75, 'n_ratio_days': 768, 'ratio_first': '2021-01-04', 'ratio_last': '2023-12-29', 'train_days': {'EURUSD': 778, 'GER40cash': 768}, 'rt_in_costs': True, 'swap_bp': 0, 'session': '15:30-21:00 CET cheapest side (overnight swap excluded)'}

Gates from COSTS_FTMO.csv round-trips. Session-flat so swap=0 is in the gate. No thr-grid. No 2024+ selection. No softer session spread.
