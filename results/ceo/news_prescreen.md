# Nieuws-reactie pre-screen (CEO, D-102, 2026-10-01 20:30; geen trial, geen reserve)
Events: `events.csv` (alleen status ≠ "NIET bevestigd"): NFP/CPI 08:30 ET, FOMC 14:00 ET → brokerservertijd (Europe/Athens). Regel: richting van de release-M5-bar; instap op de close van die bar (≥ 5 min na release = voorbij FTMO-funded 2-minutenvenster); exit na 30/60 min. 'cont' = met de richting mee, 'fade' = ertegen. Train t/m 2023-12. Gate = 3 × RT × 3 (nieuws-spreadstress). Script `news_prescreen.py`.

| Instrument | Hold | Modus | N | Gem. bruto bp | Gate bp | t |
|---|---:|---|---:|---:|---:|---:|
| US100 | 60 | fade | 76 | +13,8 | 7,2 | 1,48 |
| US500 | 60 | fade | 75 | +8,1 | 7,2 | 1,17 |
| XAUUSD | 60 | cont | 75 | +6,6 | 18,0 | 1,07 |
| EURUSD | 60 | fade | 76 | +3,1 | 8,1 | 0,93 |
| (overige) | | | | | | |t < 1,2, bruto < gate |

Lezing: geen enkele combinatie haalt gate én t ≥ 2. Bij 76 events is de power laag (alleen effecten > ~25 bp bruto zijn aantoonbaar). US100/US500 60-min fade (+13,8/+8,1 bp) komt boven de gate maar met t ≈ 1,2–1,5 en dezelfde teken-flip tussen 30 en 60 min (ruis-signaal). Niet doorgaan naar PREREG zonder meer events (pool: ECB, BoE, EIA, retail sales, GDP) of langere historie (events ≥ 2015 via proxy).
