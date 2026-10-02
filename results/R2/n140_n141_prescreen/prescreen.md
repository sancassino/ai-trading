# D-092.1 N140/N141 pre-screen (train 2021–2023)

- **N140 XAU_UKOIL_XS**: N=203 mean=4.7151 med=10.9706 gate=10.62 → **FAIL** years={'2021': -28.2672, '2022': 27.3885, '2023': -8.8535} L/S=112/91 hits=[] meta={'n_signal_days': 239, 'n_skip_missing_bar': 36}
- **N141 XAG_UKOIL_XS**: N=208 mean=6.3541 med=15.3308 gate=23.34 → **FAIL_CLONE** years={'2021': -30.8099, '2022': 23.8045, '2023': 3.8256} L/S=111/97 hits=['N140_XAU_UKOIL'] meta={'n_signal_days': 239, 'n_skip_missing_bar': 31}
- **REPL USDCHF_USDJPY_XS**: N=227 mean=-3.1949 med=-1.7135 gate=5.37 → **FAIL_CLONE** years={'2021': -4.3024, '2022': -3.8498, '2023': -1.5955} L/S=173/54 hits=['USDJPY_ret5'] meta={'n_signal_days': 227, 'n_skip_missing_bar': 0}

Clone detail is in prescreen.json. No thr-grid. No 2024+ selection.
