# A5 FORMEEL — kostenpoort STOP (geen TRIAL_COUNT)

**PREREG:** `PREREG_FTMO_FX_INTRADAG.md` (SHA-256 `4f53e17c…`)  
**Data:** `data/m5gz/` U-006 A (merged from `origin/main` @ `5254704`)  
**Train only:** 2021-01-01 … 2023-12-31; CET OR 08:00–08:30; flat ≤ 12:00; majors EURUSD/GBPUSD/USDJPY/USDCHF.  
**Script:** `scripts/a5_cost_gate_fx_train.py`  
**Artefacts:** `cost_gate_a5_train.{md,json,csv}`

## Poort
| Metric | Waarde |
|--------|-------:|
| N trades | 3106 |
| Median bruto | −5.91 bp |
| Mean bruto | +0.62 bp |
| Mean cost (spread+2×€2.25) | 1.31 bp |
| 3× mean cost | 3.93 bp |
| Median cost | 0.61 bp |
| Abs. PREREG-note (≥ 2.1 bp) | FAIL |

**Verdict: FAIL → STOP.** Geen `ftmo_ev()`, geen test-2024.  
Per PREREG §5: kostenpoort-fail → **geen** TRIAL_COUNT-increment (anders dan A4/B1 die wél telden). Wel catalogus-regel in `TRIALS.csv` (append-only audit).

Reserve **2025-01→ onaangeraakt**.
