# RUNLOG

Kort verslag per run/test, nieuwste onderaan.

## 2026-09-29 12:30 — Sessie 28 sep: regimefilter, dag-equity, guard, breed universum

Getest: regimefilter SMA10 over 9 plateau-configs; dagelijkse equity-log in EA; FTMO-dagregel (balance 00:00 − 5%); daily/total equity-guard; exposure 45/60%; train/test-split over 36 runs; plateau-ensemble; breed universum (65 instr.) ruw en vol-gecorrigeerd.
Resultaat: teken robuust (36/36 test positief) maar parameterkeuze niet (Spearman −0,28); FTMO-veilig ~$350–500/mnd per $100k; breed universum verliest → 16-resultaat deels hindsight-selectie. Details: Bevindingen_MomentumRotatie.md.
Volgende stap: alles herrekenen naar het echte account (€80.000 EUR).
