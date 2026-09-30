# VERSLAG backlog v18 — fase 2 (Uitvoerder, 2026-09-30 ≈ 13:00 Amsterdam)

| Taak | Uitkomst |
|---|---|
| S3-drempel terug | PREREG_S3 + s3_run.py → dag-geclusterd t ≥ 2,5 (M-009 ingetrokken); data/long_m1 was leeg; power-annex blijft |
| D1 Dukascopy-lake | volgorde SPX → GRX → NSX → XAU; SPX 2011 niet op de feed; 2012: 14 dagen binnen, daarna resets/503 (throttling) → downloader wacht netjes, stopt vanzelf; herstart trager (30 s) gepland |
| D2 lange dagdata | 34 Yahoo-reeksen (1927–2026) + 7 FRED-FX (1971–) in `data/daily/` (in repo), QA + `data/DATA_CATALOGUS.md`; overlap FTMO: corr 0,999 (SPX, NDX), 0,992 (DAX) |
| R0 engine | `engine/run_rule.py`: één kostenmodel (spread + FX-carry historisch / FTMO-swap constant), identieke output, reserve-OOS afgeschermd, TRIALS.csv + BH-FDR; B2b-replicatie klopt (t 3,21 NW) |
| R1 CAT1 (7 regels) | alleen **C02 Faber** (t 3,14, SR 0,32) en **C17 FOMC-cyclus** (t 2,85/3,05, SR 0,52) iets; rest ≈ 0. **Kostenpoort-definitie in mijn PREREG wijkt af van het template → U-004 aan CEO** (standaard: template, C02 naar reserve-OOS) |
| F forward | eerste run vanavond 22:15 UTC; controle volgt |

Open: U-004 (CEO), P0-throttling, forward-controle.
