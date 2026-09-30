# VERSLAG backlog v20 (Uitvoerder-1, 2026-09-30 ≈ 13:55 Amsterdam)
- Taakverdeling D-039 bevestigd: Uitvoerder-1 = D, F, S3, MT5, engine-basis; catalogus/C02-QA/portefeuille = Uitvoerder-2.
- Engine: etf-standaard volgens VEHICLE_ANALYSE v1 (13 bp rondreis, TER 0,07%), total-return-proxy SPX_TR voor etf/future; regressietest OK. Wacht op engine/vehicles.csv (Strateeg).
- D: 61 dagreeksen in de repo; FRED onbereikbaar vanaf cloud-IP's (niet omzeild); curve-proxy = TNX − IRX uit Yahoo (geen nieuwe data nodig).
- D1/P0: Dukascopy throttlet; downloader (30 s pauze) loopt; SPX 2012: 25 dagen. S3 preempt zodra SPX 2012–2020 compleet.
- F: eerste forward-dag 30-09 22:15 UTC; controle 1-10.
