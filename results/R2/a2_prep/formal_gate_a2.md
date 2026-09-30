# A2 formal gate — STOP

**PREREG:** `PREREG_FTMO_A2.md` blob `6aaa6238` (bevroren vóór resultaat).
**Data:** `data/m5gz/` US41 (v41 merge) + `earnings.csv` + `COSTS_FTMO_alle.csv`.
**Uitvoering:** 2026-09-30 ≈ 23:20 CEST, branch `claude/uitvoerder2-r`.

## Kostenpoort (PREREG §3, D-012)

| Maat | Waarde |
|------|-------:|
| N trades train 2021–23 | 365 |
| Mean bruto | **+3.77 bp** |
| Median bruto (informatief) | −23.78 bp |
| Trade-gewogen mean RT (tabel) | 8.91 bp |
| 3× mean RT (poort) | **26.74 bp** |
| Mean bruto zonder top-5% winnaars | −25.88 bp |
| +50% spread-poort | FAIL |

**Verdict: FAIL → STOP.** Geen `ftmo_ev()`, geen test-2024, geen TRIAL_COUNT++ (PREREG §3: FAIL telt als stop:kostenpoort zonder formele trial-telling).
TRIALS append-only. Reserve 2025→ onaangeraakt.
