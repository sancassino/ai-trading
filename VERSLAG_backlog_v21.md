# VERSLAG backlog v21 (Uitvoerder-1, 2026-09-30 ≈ 15:00 Amsterdam)

| Taak | Uitkomst |
|---|---|
| Merge Uitvoerder-2 | claude/uitvoerder2-r → main (CAT2, engine-uitbreiding); pycache uit git; regressietest OK; TRIAL_COUNT 427 (U-2) |
| D-044 data | 96 dagreeksen: + C54-instrumenten (5 FX, 12 agri/energie/metaal-futures, Bund/Gilt/intl-obligatie-ETF's), roll-inclusieve ETF's (CPER, UNG, USO, PPLT, DBA), **officiële rentes** US 3m/2j/10j/30j (1990→), JP 10j (1986→), UK 10j (1982→), DE 10j (1997→) en **CPI-U (1913→)**; FRED ook vanaf Debian geblokkeerd (niet omzeild) |
| D-045 engine | future-model-fix van Uitvoerder-2 gedocumenteerd in engine/README; rf loopt na FRED-einde door met Treasury 3m |
| D-050 forward (voorbereiding) | engine/forward.py (gevalideerd, exact op 5e-9 met de R2-export bij gelijke vehikelparameters); dagelijkse data-update via cron 22:05 UTC; **wacht op PREREG_PORT.md** (Uitvoerder-2) |
| Coördinatie | U-005: R2-etf-reeksen zijn met de oude etf-standaard (3 bp/TER 0,10%) gemaakt; huidige standaard 13 bp/TER 0,07%/SPX_TR → PREREG_PORT legt één set vast |
| D1/P0 | Dukascopy throttlet; SPX 2012 loopt (zie RUNLOG) |
| F | eerste F3b-forward-dag vanavond 22:15 UTC |
