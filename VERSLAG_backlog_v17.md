# VERSLAG backlog v17 (Uitvoerder, 2026-09-30 ≈ 12:30 Amsterdam)

| Taak | Uitkomst | Trials |
|---|---|---|
| P0 lange data | gelogd vóór 13:36 (routes + uitkomst); Dukascopy-downloader herstart met betere 503-afhandeling (controledatum), loopt; 2011 ontbreekt op de feed | 0 |
| N8 power S3 | S3-set (4 symbolen) FTMO 2021–26: +3,38 bp, dag-geclusterd t 2,90. P(bevestigd) 9 jaar: vol effect 88% (t ≥ 2,5) / 95% (eenzijdig t ≥ 2,0); gehalveerd 18% / 33%; nul 0%. **PREREG_S3 → eenzijdig t ≥ 2,0 (M-009 C), vóór data** | 0 |
| N7 cluster-audit | RESULTATEN_GECLUSTERD.md: ORB 7 symbolen 2,93 → 1,81; S3-set 3,73 → 2,90; S1 2,19 → 2,05; K1-FTMO 1,79 → 0,43; B2b-dagreeks overleeft (NW 3,80). Labelcorrectie: B4a = 7 symbolen | 0 |
| U2b MT5-reconciliatie | vaste notional ×4: €509/mnd (nul-drift €105; max dip 4,57%); 0,5%-risico: €1.136 (nul-drift €389, max dip 3,50%) — Python bevestigd. Toegestane schaal (S8): ≈ €150–300. Alleen techniek; edge onbevestigd | 0 |
| Q6 forward | eerste dag vanavond 22:15 UTC; controle morgen | 0 |

TRIAL_COUNT 414. Alles wacht op S3 (Dukascopy-data 2012–20); `run_s3.sh` draait zodra zips in data/long_m1/ staan.
