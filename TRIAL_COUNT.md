# TRIAL_COUNT — aantal geteste varianten (voor multiple-testing-correctie)

Telling 2026-09-29 (eerlijke schatting; sterk gecorreleerde varianten tellen elk mee).

| Blok | Varianten | Bron |
|---|---|---|
| Overdrachtsdocument mean-reversion (edelmetalen), niet in repo | ~20 (schatting) | Bevindingen/trend-research |
| Python/Yahoo trend-grid (trend 100–250 × ATR 2–4) | ~20 (schatting) | trend-research.md |
| MT5-runs vorige sessies (root-CSV's: TrendFollow TP/ATR/Donchian/regime/buffer, MomRot, MR/TRAIN/TEST) | 89 | root-CSV's |
| Plateau USD (r0/r10/guard/exposure) | 45 | results/plateau |
| EUR-herberekening | 19 | results/eur |
| Breed universum, vol-gecorr., IDX, T10, dual momentum | 51 (+3 ongeldig) | results/wide |
| Ensemble-EA + stap-3-universums | 13 | results/ens |
| Lange validatie A/B (kostengevoeligheid niet apart geteld) | 18 | results/long |
| Ronde 2 (familie 1, 2) | 2 | results/ronde2 |
| **Totaal** | **≈ 300** | |

Gebruik in `stats_tools.py`: N = 300 (eerlijk) en N = 30 (grove schatting "effectief onafhankelijk",
omdat veel varianten buren van elkaar zijn). Bijwerken na elke nieuwe test.

## Log van nieuwe trials (vanaf B1)
| Datum | Taak | Nieuwe varianten | Lopend totaal |
|---|---|---|---|
| 2026-09-29 | B1 (alleen statistiek, geen nieuwe strategie) | 0 | 300 |
| 2026-09-29 | B2 dagfrequent (a IBS, b RSI2, c1 intraday, c2 overnight, d TOM), gepoold | 5 | 305 |
| 2026-09-29 | B3 dollar-neutrale L/S momentum (9 configs × universum A en B) | 18 | 323 |
| 2026-09-29 | B4 intraday FTMO-M5 (ORB, laatste-30-min, gap-reversal), gepoold over 7 symbolen | 3 | 326 |
| 2026-09-29 | C1 pairs/stat-arb (8 paren; ETF-versie = zelfde regel) | 8 | 334 |
| 2026-09-29 | C2 lead-lag (a,b) + vaste vensters (c1 XAU, c2 US100) | 4 | 338 |
| 2026-09-29 | C3 kortetermijn-omkeer markt-neutraal (FTMO-set + Yahoo-bovengrens) | 2 | 340 |
| 2026-09-29 | C4 sizing/combinatie bestaande sleeves (geen nieuwe signalen) | 0 | 340 |
| 2026-09-29 | C5 crypto-trend BTC+ETH | 1 | 341 |
| 2026-09-29 | C6 vol-timing SPX/NDX/DAX | 3 | 344 |
| 2026-09-29 | C7 alleen ontwerp (geen trial) | 0 | 344 |
| 2026-09-29 | D1 EURUSD-intradagseizoen (2 vaste vensters) | 2 | 346 |
