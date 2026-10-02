# PREREG — nieuws-reactie drift zonder consensus (2 okt 2026)
Mechanisme: het prijsverloop in de eerste 10 min na een scheduled release toont de verrassing; vervolg-drift (informatie-verwerking/liquiditeit) kan doorlopen. Alleen gratis tijdstippen: NFP en CPI (ALFRED first-release data, 2021–2024, 8:30 ET = server 15:30), FOMC-statement (14:00 ET = server 21:00; 32 datums 2021–2024).
Regel (1 set): r1 = close(T+10min)/close(T−5min) −1 (M5-bars); positie sign(r1) van T+10 tot T+70 min. |r1| > 1 spreadkost vereist (anders geen trade). Instrumenten: US500, US100, XAUUSD, EURUSD, GBPUSD, USDJPY. Kosten: rondreis uit COSTS (+ extra 1 bp slippage).
Train 2021–2023, test 2024. 2025+ ongebruikt. PASS: gepoold netto >0, event-geclusterde t>=2 in train én test, ≥4/6 instrumenten positief. Trials +3 eventtypen x 6 instrumenten = 18 (CEO-T15).
Beperking: M5 mist de eerste minuten; funded-regel ±2 min geldt niet in challenge (te verifiëren door Sandro).
