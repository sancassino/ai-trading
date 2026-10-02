# PREREG — fade na NFP/CPI (vastgelegd vóór reserve-run, 2 okt 2026)
Herkomst: exploratief resultaat PREREG_EVENT_DRIFT (continuation faalde; teken consistent negatief in train én test voor NFP en CPI, 0/6 instrumenten positief). Dit is een DATA-GEZIEN teken => bevestiging alleen op ongezien deel.
Regel: identiek aan EVENT_DRIFT maar positie = −sign(r1) van T+10 tot T+70 min; filter |r1| > instrumentkosten (incl. 1bp slippage). Events: NFP en CPI (ALFRED-datums), instrumenten US500, US100, XAUUSD, EURUSD, GBPUSD, USDJPY. FOMC uitgesloten (tekenwissel, N te klein).
Bevestigingsset: 2025-01-01 t/m 2026-09-30 (niet eerder bekeken voor event-studies). Eénmalige run. Trial CEO-T16.
PASS: gepoold netto > 0 bij kosten c+1bp EN event-geclusterde t >= 2.0 EN >= 4/6 instrumenten positief EN netto > 0 ook bij extra +2bp kosten (spread-stress rond nieuws).
Release van de reserve voor deze kandidaat: CEO-besluit D-105 (onder voorbehoud: ex-ante tekenkeuze op 2021–24).
