# A4 FORMEEL — PREREG_FTMO_C17 (amend 5fc3fb9)

**Datum:** 2026-09-30 22:04 CEST Europe/Amsterdam  
**Branch:** `claude/uitvoerder2-r`  
**PREREG:** amend SHA `5fc3fb9c09812b141934c48c2e5b110eb5268fe9` (train 2021–2023, test=2024, reserve 2025 ONAANGERAAKT)  
**Engine:** `engine/ftmo.py` blob `f13a5d11` (CTO) — niet aangeroepen (stop vóór FTMO-EV)  
**A5:** geparkeerd (M5 ontbreekt)

## Vensters (bevestigd uit amend)
- Train: 2021-01-01 … 2023-12-31
- Test: 2024-01-01 … 2024-12-31
- Reserve: 2025-01-01 → ONAANGERAAKT (geen bars gelezen voor trial/gate)

## Data-prep
- `data/fomc_dates.csv` — 265 FOMC-data (1994→2026 kalender; alleen ≤2023 gebruikt in gate)
- `data/daily/US500cash.csv`, `US100cash.csv` uit `data/ftmo_d1ohlc_US500_US100.txt`
- `data/daily/GER40cash.csv` — DAX-proxy (geen FTMO GER40 D1 op branch); kosten = GER40cash

## Kostenpoort (TRAIN only) — PRE → formeel beslis

Script: `scripts/a4_cost_gate_c17_train.py`  
Artefacts: `results/R2/a4_prep/cost_gate_c17_train.{json,md,trades.csv}`

| Metric | Waarde |
|--------|--------|
| N trades (3 symbolen, entry&exit in train) | 221 |
| Pooled median bruto | 20.79 bp |
| Pooled median cost (RT + nights×swap_long) | 15.04 bp |
| 3× median cost | 45.12 bp |
| Pooled median netto | 7.73 bp |
| Mean nights | 8.63 (PREREG ≈5 was onderschatting; WINDOWS −1…4 ≈6 handelsdagen + weekend) |
| Gate: median bruto ≥ 3× cost incl. swap | **FAIL** |
| Secundair: ≥ ≈15 bp (PREREG-parenthese) | PASS (20.79) |
| Swap +50% sensitivity | FAIL |

Per symbool: US500 FAIL (14.55 vs 34.98), US100 FAIL (−10.94 vs 48.78), GER40 PASS (55.31 vs 45.12).

## Beslissing (PREREG §4)
**STOP: kostenpoort** — netto mediaan-bruto < 3× rondreis-kosten inclusief swap op train.  
Telt als trial; **geen** test-t, **geen** FTMO-EV, **geen** 2025-reserve.  
`catalogus/TRIALS.csv` append-only rij toegevoegd.

## Niet gedaan
- A5 FX intradag (CTO-park; M5 ontbreekt)
- Formele test 2024 analyse / `ftmo_ev()` (geblokkeerd door poort)
