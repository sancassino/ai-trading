# VERSLAG backlog v19 (Uitvoerder-1, 2026-09-30 ≈ 13:40 Amsterdam)

| Taak | Uitkomst |
|---|---|
| S3-drempel (D-029/D-036) | definitief eenzijdig dag-geclusterd t ≥ 2,0, bevroren vóór data; SHA-256 van PREREG_S3.md en s3_run.py in RUNLOG |
| U-004 / D-037 | CAT1 opnieuw met template-kostenpoort: 7 trials (TRIAL_COUNT 421); **C02 Faber door G-ontdekking** (t 3,14, SR 0,32, BH-q 0,003; beter dan B&H: SR 0,32 vs 0,18, maxDD 54% vs 88%); C17 FOMC-cyclus net niet (t 2,85; BH-q 0,006) |
| D-038 engine | vehicle-parameter (cfd/etf/future, standaardkosten tot engine/vehicles.csv), G-benchmark (B&H, zelfde vehikel), vehikelrapporten zonder extra trial; README + regressietest (B2b OK) |
| D2 uitbreiding | 61 dagreeksen (+ SPX_TR, obligatie/krediet-ETF's, internationaal, grondstof-ETF's, FX, 5j/30j-rente); FRED onbereikbaar vanaf cloud-IP's (niet omzeild); NDX-TR niet beschikbaar |
| D1 Dukascopy | throttling; downloader herstart met 30 s pauze (PID 337810); SPX 2012: 21 dagen binnen |
| F forward | eerste run 22:15 UTC vanavond; controle volgt |

Taakverdeling D-039: catalogusruns/C02-QA/portefeuille → Uitvoerder-2; Uitvoerder-1 → D, F, S3, MT5, engine-basis.
