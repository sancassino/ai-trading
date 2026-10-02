# D-092.1 N150/N151 pre-screen (train 2021–2023)

- **N150 XAGUSD_US30_METAL_INDUSTRIAL_XS**: N=225 mean=10.0457 med=3.5882 gate=16.56 → **FAIL_CLONE** years={'2021': 13.1446, '2022': -7.5645, '2023': 29.2181} L/S=131/94 hits=['SILVER_GOLD_N113'] meta={'n_signal_days': 225, 'n_skip_missing_bar': 0, 'n_ratio_days': 773, 'ratio_first': '2021-01-04', 'ratio_last': '2023-12-29', 'train_days': {'XAGUSD': 774, 'US30cash': 775}, 'rt_in_costs': True, 'swap_bp': 0, 'session': '15:30-21:00 CET cheapest side (overnight swap excluded)'}
- **N151 EURJPY_USDCHF_FUNDING_XS**: N=221 mean=-0.5972 med=-1.4905 gate=6.33 → **FAIL** years={'2021': 1.207, '2022': 4.685, '2023': -5.4296} L/S=77/144 hits=[] meta={'n_signal_days': 221, 'n_skip_missing_bar': 0, 'n_ratio_days': 778, 'ratio_first': '2021-01-04', 'ratio_last': '2023-12-29', 'train_days': {'EURJPY': 778, 'USDCHF': 778}, 'rt_in_costs': True, 'swap_bp': 0, 'session': '15:30-21:00 CET cheapest side (overnight swap excluded)'}

Gates from COSTS_FTMO.csv round-trips. Session-flat so swap=0 is in the gate. No thr-grid. No 2024+ selection. No softer session spread. No inline replacement.
