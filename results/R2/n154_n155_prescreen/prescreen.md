# D-092.1 N154/N155 pre-screen (train 2021–2023)

- **N154 US100_GER40_TRANSATLANTIC_XS**: N=177 mean=-2.7903 med=-0.4891 gate=4.14 → **FAIL** years={'2022': -6.8322, '2023': 2.2236} L/S=87/90 hits=[] meta={'n_signal_days': 239, 'n_skip_missing_bar': 62, 'n_ratio_days': 767, 'ratio_first': '2021-01-04', 'ratio_last': '2023-12-29', 'b_sign': -1, 'train_days': {'US100cash': 775, 'GER40cash': 768}, 'rt_in_costs': True, 'swap_bp': 0, 'session': '15:30-21:00 CET cheapest side (overnight swap excluded)'}
- **N155 US30_UKOIL_INDUSTRIAL_CRUDE_XS**: N=206 mean=-4.3081 med=-10.6065 gate=9.48 → **FAIL_CLONE** years={'2021': -40.1362, '2022': 11.5349, '2023': -9.2382} L/S=111/95 hits=['GBP_UKOIL_z40_N147', 'N147_sign'] meta={'n_signal_days': 250, 'n_skip_missing_bar': 44, 'n_ratio_days': 773, 'ratio_first': '2021-01-04', 'ratio_last': '2023-12-29', 'b_sign': -1, 'train_days': {'US30cash': 775, 'UKOILcash': 773}, 'rt_in_costs': True, 'swap_bp': 0, 'session': '15:30-21:00 CET cheapest side (overnight swap excluded)'}

Gates from COSTS_FTMO.csv round-trips. Session-flat so swap=0 is in the gate. No thr-grid. No 2024+ selection. No softer session spread. No single-leg rewrite.
