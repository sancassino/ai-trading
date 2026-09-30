# VERSLAG backlog v32 (Uitvoerder-1, 2026-09-30 ≈ 20:30 Amsterdam)
- **QA-1 PREREG_PORT3** (SHA in RUNLOG) vóór forward-start vastgelegd: drempelvariant P-ETF-a op instrumentniveau. Backtest (model B, 2001–24): drempel 0 → 153 transacties/jr, kosten €268/jr, SR 0,86; drempel 1% → 57/jr, €116/jr, SR 0,91 (alfa +€21/mnd). Forward forward/portfolio3_daily.csv vanaf 01-10 (cron 22:25 UTC). Geen trial, geen selectie.
- **QA-3 valuta:** forward logt USD, EUR ongehedged én gehedged voor alle portefeuilles (portfolio_daily/2/3).
- **QA-5 R2-007:** ^PUT, VIX9D, VIX3M binnen (privé, licentienotitie); ^BXM/^WPUT niet beschikbaar; Ken French en Shiller alleen citeren (geen licentie) — niets gecommit.
- **Cron-script** robuuster (git add per bestand).
- **Open:** QA-6 controle forward-bestanden na 22:25 UTC; QA-7 merge Uitvoerder-2 vóór 01-10 09:00.
