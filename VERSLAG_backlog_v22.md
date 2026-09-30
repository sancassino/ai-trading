# VERSLAG backlog v22 (Uitvoerder-1, 2026-09-30 ≈ 15:00 Amsterdam)
- **F/D-050:** forward_portfolio.py wacht op PREREG_PORT.md (Uitvoerder-2, nog niet gecommit). Infrastructuur klaar: engine/forward.py (gevalideerd), dagelijkse data-update 22:05 UTC.
- **QA-2 (rf):** DTB3 t/m 25-09-2026, daarna Treasury 3m — beide in engine.rf_on, forward = engine. Verschil Treasury − DTB3: mediaan +6 bp (1990–2026), +15 bp/jr sinds 2024 (≈ 0,06 bp/dag) → vermeld in tracking-band.
- **QA-3 (lookahead/herschrijving):** data-update append-only (bevestigd), Yahoo-correcties alleen gelogd; dagelijkse ruwe snapshots met UTC-tijdstempel in forward/data_snapshots/ (gecommit).
- **U-005:** herrekening R2-etf met de nieuwe vehikelset ligt bij Uitvoerder-2 (Manager-QA 1).
- **D1/P0:** SPX 2012: 45 dagen; **F3b-forward:** eerste dag vanavond 22:15 UTC.
