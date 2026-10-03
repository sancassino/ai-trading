# D-092.1 N172/N173 pre-screen (train 2021–2023)

Commodity swing + FX swing. Session-flat. Not N170 FRA40 NY-impulse (barred; not screened). Not N171 BTC (barred; not screened). Not a rate-carry (those cloned L60/N53 before an id).

- **N172 USOIL prior-5d swing reversal session-flat**: N=767 mean=4.5516 netto=1.2116 med=3.1411 gate=10.02 → **FAIL** years={'2021': 3.9731, '2022': 8.2054, '2023': 1.4508} span=2.96 L/S=334/433 hits=[] meta_skip=1
- **N173 USDCAD prior-1d swing continuation session-flat**: N=776 mean=-0.8991 netto=-1.6991 med=-1.0765 gate=2.4 → **FAIL** years={'2021': 1.0529, '2022': -2.6771, '2023': -1.0654} span=2.98 L/S=392/384 hits=[] meta_skip=0

Gates from COSTS_FTMO.csv round-trips. N172 RT 3.34 × 3 = 10.02. N173 RT 0.80 × 3 = 2.40, not the US500 gate. Session-flat so swap nights = 0. USDCAD long swap credit −0.09 is not alpha. Oil swap specs are not used. No thr-grid. No 2024+ selection.
