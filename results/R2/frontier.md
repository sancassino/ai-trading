# R2 — rendement–drawdown-frontier (D-062; ontdekking ≤ 2024; geen trial)

DD-budget (D-062): backtest-maxDD ≤ 20% **en** p95-DD (5-jaars blok-bootstrap) ≤ 25%. Alfa = geannualiseerd gemiddeld excess (na financieringsopslag); haircut op excess (D-055/D-060), EUR-cash (€STR 2,44% ≈ €163/mnd op €80k) apart. Hefboom ≤ 2× (PREREG_PORT §2).

## P-ETF-a/b (C52L + C02) — 2001-04-02 → 2024-12-31

| vol-doel | gem. hefboom | vol | alfa/jr | CAGR totaal (USD) | maxDD | p95-DD | langste DD (jr) | financieringsopslag €/jr | alfa boven cash €/mnd na haircut 30/40/50% | totaal €/mnd (+EUR-cash) 30/40/50% | binnen DD-budget |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5% | 1.01 | 5.7% | 4.6% | 6.2% | 10.5% | 13.4% | 2.1 | €197 | €212 / €182 / €152 | €375 / €345 / €314 | JA |
| 6% | 1.18 | 6.7% | 5.3% | 6.9% | 13.0% | 16.0% | 2.1 | €306 | €249 / €214 / €178 | €412 / €376 / €341 | JA |
| 7% | 1.33 | 7.6% | 6.1% | 7.7% | 14.9% | 19.0% | 2.2 | €440 | €286 / €245 / €204 | €448 / €408 / €367 | JA |
| 8% | 1.47 | 8.5% | 6.8% | 8.3% | 17.0% | 21.3% | 2.2 | €578 | €315 / €270 / €225 | €478 / €433 / €388 | JA |
| 9% | 1.59 | 9.3% | 7.3% | 8.8% | 18.7% | 22.6% | 2.2 | €712 | €341 / €292 / €244 | €504 / €455 / €406 | JA |
| 10% | 1.69 | 10.0% | 7.8% | 9.3% | 20.1% | 24.0% | 2.2 | €831 | €366 / €313 / €261 | €528 / €476 / €424 | nee |
| 12% | 1.84 | 11.1% | 8.8% | 10.2% | 21.7% | 26.2% | 2.2 | €1,015 | €409 / €351 / €292 | €572 / €513 / €455 | nee |

## P-ETF+ (C52L + C02 + C55) — 2005-04-01 → 2024-12-31

| vol-doel | gem. hefboom | vol | alfa/jr | CAGR totaal (USD) | maxDD | p95-DD | langste DD (jr) | financieringsopslag €/jr | alfa boven cash €/mnd na haircut 30/40/50% | totaal €/mnd (+EUR-cash) 30/40/50% | binnen DD-budget |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5% | 0.95 | 5.9% | 4.1% | 5.6% | 12.1% | 13.3% | 2.1 | €144 | €190 / €163 / €136 | €353 / €326 / €299 | JA |
| 6% | 1.12 | 6.9% | 4.7% | 6.3% | 14.6% | 16.0% | 2.3 | €258 | €221 / €190 / €158 | €384 / €352 / €321 | JA |
| 7% | 1.28 | 7.9% | 5.3% | 6.8% | 16.7% | 18.6% | 2.5 | €397 | €249 / €214 / €178 | €412 / €376 / €341 | JA |
| 8% | 1.42 | 8.8% | 6.0% | 7.5% | 18.2% | 20.7% | 2.5 | €533 | €281 / €241 / €201 | €444 / €404 / €364 | JA |
| 9% | 1.54 | 9.6% | 6.7% | 8.1% | 19.4% | 22.9% | 2.5 | €668 | €311 / €267 / €222 | €474 / €429 / €385 | JA |
| 10% | 1.65 | 10.3% | 7.2% | 8.6% | 19.9% | 25.1% | 2.5 | €787 | €338 / €290 / €242 | €501 / €453 / €404 | nee |
| 12% | 1.81 | 11.4% | 8.2% | 9.5% | 20.1% | 27.1% | 2.5 | €968 | €381 / €327 / €272 | €544 / €489 / €435 | nee |

Lezing: zie RUNLOG_R2 (D-062). Alle getallen zijn ontdekkings-uitkomsten van sleeves die ná zien van die data zijn gekozen (winnaarsvloek) en bevatten geen reserve-OOS.
