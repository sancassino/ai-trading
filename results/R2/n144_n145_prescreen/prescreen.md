# D-092.1 N144/N145 pre-screen (train 2021–2023)

- **N144 XPT_XPD_PGM_XS**: N=228 mean=-0.6917 med=14.5741 gate=205.0584 stated=202.71 → **FAIL** years={'2021': -10.4454, '2022': -21.0687, '2023': 27.298} L/S=71/157 hits=[] meta={'n_signal_days': 228, 'n_skip_missing_bar': 0, 'n_ratio_days': 773, 'ratio_first': '2021-01-04', 'ratio_last': '2023-12-29', 'train_days_xpt': 773, 'train_days_xpd': 773, 'symbol_history_XPT_d1_bars': 0, 'symbol_history_note': "symbol_history_FTMO.csv XPTUSD first_d1='-' bars=0; M5 gz is populated"}
- **N145 BTC_ETH_CRYPTO_XS**: N=293 mean=-9.6529 med=-9.1658 gate=64.3104 stated=23.25 → **FAIL** years={'2021': -24.5886, '2022': -2.0217, '2023': -4.8914} L/S=114/179 hits=[] meta={'n_signal_days': 332, 'n_skip_missing_bar': 39, 'n_ratio_days': 1092, 'ratio_first': '2021-01-01', 'ratio_last': '2023-12-31', 'train_days_btc': 1092, 'train_days_eth': 1092, 'in_symbol_list': True, 'in_costs_ftmo': False}

Honest RT = all-hours median spread (spread>0, 2024-01-01..2026-09-30) + commission. Session medians logged, not used. No thr-grid. No 2024+ selection.

RT XPT 24.0199 (spread 23.6265 + 2×0.1967) / XPD 44.3329 (spread 43.942 + 2×0.1955).
RT BTC 7.3531 (spread 0.8531 + 2×3.25; zero-spread share 0.0629) / ETH 14.0837 (spread 7.5837 + 2×3.25).
