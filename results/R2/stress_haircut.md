# R2 — regime-stress, rolling-SR, DD-duur, live-haircut (D-043/D-047; ontdekking ≤ 2024-12-31; geen trial)

## 1. Regime-stress: lange proxies (rente stijgend 1970–1981)
Aanname/beperking: SPX-prijsindex vóór 1988 zonder dividend (SPX_TR pas vanaf 1988) → aandelen in de jaren 70/80 onderschat (≈ 3–5%/jr); obligatie = synthetisch uit ^TNX (D=8, C=80); goud pas vanaf 2000 → geen 3e activum.

**C52 all-weather, 2-activa (SPX + obligatie, ∝ 1/σ60, vol-target 8%, geen hefboom; etf) vs 60/40**

| periode | SR (overschot) | CAGR totaal | maxDD |
|---|---|---|---|
| 1970s | -0.32 | +4.3% | 14.9% |
| 1980s | +0.38 | +12.7% | 15.7% |
| 1990s | +0.86 | +11.4% | 9.5% |
| 2000s | +0.43 | +5.4% | 10.1% |
| 2010s | +1.35 | +7.0% | 5.5% |
| 2020–24 | +0.07 | +2.8% | 16.8% |
| 2022 | -1.90 | -13.6% | 16.2% |
| alles | +0.45 | +7.6% | 18.3% |

60/40 SPX/BOND10_SYN (zelfde dagen):

**60/40**

| periode | SR (overschot) | CAGR totaal | maxDD |
|---|---|---|---|
| 1970s | -0.28 | +3.5% | 32.3% |
| 1980s | +0.36 | +13.4% | 24.0% |
| 1990s | +0.78 | +12.7% | 13.0% |
| 2000s | -0.01 | +1.8% | 32.6% |
| 2010s | +1.01 | +8.8% | 11.2% |
| 2020–24 | +0.43 | +7.5% | 21.4% |
| 2022 | -1.25 | -17.0% | 21.1% |
| alles | +0.34 | +7.9% | 32.6% |

**C02 Faber (5 indices, etf) — vanaf 1927**

| periode | SR (overschot) | CAGR totaal | maxDD |
|---|---|---|---|
| 1970s | +0.23 | +7.8% | 13.9% |
| 1980s | +0.51 | +14.2% | 30.0% |
| 1990s | +0.68 | +11.9% | 21.6% |
| 2000s | +0.44 | +6.5% | 17.3% |
| 2010s | +0.72 | +7.8% | 17.0% |
| 2020–24 | +0.77 | +10.6% | 16.5% |
| 2022 | -1.90 | -9.5% | 11.3% |
| alles | +0.47 | +8.5% | 51.0% |

**C54 Carver 'basis' (future; 1971→, FX-pegs/WTI-artefact-gevoelig!) — leest de jaren 70/80 met voorzichtigheid**

| periode | SR (overschot) | CAGR totaal | maxDD |
|---|---|---|---|
| 1970s | +0.63 | +9.7% | 7.0% |
| 1980s | +1.19 | +15.5% | 6.1% |
| 1990s | +0.80 | +8.4% | 3.9% |
| 2000s | +0.73 | +5.7% | 5.0% |
| 2010s | +0.27 | +1.5% | 6.9% |
| 2020–24 | +0.56 | +4.5% | 3.1% |
| 2022 | +0.10 | +2.3% | 2.7% |
| alles | +0.47 | +7.0% | 23.3% |

## 2. Portefeuilles (PREREG_PORT-methode, forward_portfolio.py; ontdekking)

| portefeuille | SR | CAGR USD | maxDD | langste DD-duur (jaren) | rolling-3j-SR min / mediaan / laatste | 2022 | CAGR na haircut 30% / 50% | € per maand (na 30% / 50%, vóór box 3) |
|---|---|---|---|---|---|---|---|---|
| P-ETF-a | 0.94 | 7.4% | 11.2% | 1.8 | +0.02 / +0.97 / +0.53 | -9.5% | 5.2% / 3.7% | €344 / €246 |
| P-ETF-b | 0.79 | 9.4% | 20.0% | 2.2 | -0.29 / +0.80 / +0.36 | -18.5% | 6.6% / 4.7% | €440 / €314 |
| P1 | 0.79 | 9.6% | 15.9% | 2.1 | -0.08 / +0.76 / +0.40 | -13.9% | 6.7% / 4.8% | €447 / €320 |
| P-breed | 0.70 | 8.0% | 17.4% | 2.5 | -0.25 / +0.63 / +0.33 | -13.4% | 5.6% / 4.0% | €374 / €267 |

**P-ETF-a per decennium**

| periode | SR (overschot) | CAGR totaal | maxDD |
|---|---|---|---|
| 2000s | +0.99 | +7.9% | 7.0% |
| 2010s | +1.12 | +7.2% | 7.3% |
| 2020–24 | +0.58 | +6.6% | 11.2% |
| 2022 | -2.27 | -9.5% | 9.6% |
| alles | +0.94 | +7.4% | 11.2% |

**P1 per decennium**

| periode | SR (overschot) | CAGR totaal | maxDD |
|---|---|---|---|
| 2000s | +0.80 | +10.1% | 15.0% |
| 2010s | +0.93 | +10.3% | 15.0% |
| 2020–24 | +0.48 | +7.3% | 15.9% |
| 2022 | -1.76 | -13.9% | 14.7% |
| alles | +0.79 | +9.6% | 15.9% |
