# S2b BTC+ETH kostenpoort TRAIN — PREREG_S2b_BTC_ETH

- Train: 2021-01-01 … 2023-12-31 (geen 2025+)
- Data: `data/m5gz/{BTCUSD,ETHUSD,US100cash}.csv.gz` (v41)
- Regel: identiek parent S2-BTC_USOPEN per instrument; gepoold N
- **COSTS bridge (C-005):** `COSTS_FTMO_alle.csv` BTC=1.25 / ETH=7.98 bp RT
- N pooled: **252** (power ≥150: True)
- **BTCUSD**: N=132; mean bruto +22.91 bp; mean cost 4.37 bp; fixed RT 1.25 bp (2×=2.50); share 19.1%; gates 2×fix=True share=True stress2x=True stress_share=True → PASS
- **ETHUSD**: N=120; mean bruto +13.89 bp; mean cost 9.35 bp; fixed RT 7.98 bp (2×=15.96); share 67.3%; gates 2×fix=False share=False stress2x=False stress_share=False → FAIL
- Pooled mean bruto: **+18.61 bp** | mean cost 6.74 bp | TW fixed RT 4.45 bp
- Pooled gates: 2×TW=True cost_share=True
- Fail reasons: ETH_leg_FAIL
- **Verdict: FAIL**

Reserve 2025→: **onaangeraakt**. Geen TRIALS-append.

