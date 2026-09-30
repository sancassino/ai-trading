# Verslag BACKLOG v5 (I1–I5, J1, J3) — 2026-09-30

| Taak | Uitkomst |
|---|---|
| I1 papieren forward-test | **Gestart.** `forward_paper.py` via cron 22:15 UTC ma–vr, F3b-regels, vanaf handelsdag 2026-09-30, pusht dagelijks naar `forward/`. Droogtest 21–29 sep: ORB-trades identiek aan backtest. |
| I2 intraday mean-reversion H1 | Afgewezen: IBS-H1 t 0,96/0,22; RSI(2)-H1 negatief. Lost dagverlies op, maar geen edge zonder overnight. |
| I3 event-drift | Pre-FOMC **formeel geslaagd** (N 82, +26,7 bp, t 3,18; beide helften +), maar event-niveau t 2,35 en afnemend (42 → 13 bp). Post-nieuws afgewezen (t 0,21). NFP/CPI-datumverificatie onbetrouwbaar (gemeld). |
| I4 SCENARIO_RAPPORT | Voor Sandro: realistisch ≈ €150/mnd (P5 −€2.250, P95 +€6.000 per jaar, 24% kans op verlies); challenge EV ≈ −€10; €880/mnd onhaalbaar (< 5%). |
| I5 RSI(2)-regimes | Niet één-jaar-afhankelijk (SR 0,45 excl. 2021); zwak in 2022/2023 en in het middelste volregime. |
| J1 + pre-FOMC | In-sample SR 1,34, ≈ €361/mnd, slechtste dag 3,8% — rust op een klein, afnemend effect. |
| J3 power-analyse | Forward-bewijs (t ≥ 2) pas na 4–9 jaar; 60 dagen zegt statistisch vrijwel niets. |

TRIAL_COUNT 389. Niets benadert Sharpe 1,41 (nodig voor €880/mnd). J2 (nieuwe hypothese-batch) niet gestart: bij 389
trials is elke nieuwe batch vooral data-mining-risico; uitvoerbaar op verzoek van de supervisor.

**Nodig van Sandro:** beslissing over het doel (SCENARIO_RAPPORT.md) en eventueel een nieuwe FTMO Free Trial voor een echte demo-test.
