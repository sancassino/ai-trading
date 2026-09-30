# PREREG N5 — onafhankelijke code-audit van de kern (vastgelegd vóór berekening, 2026-09-30)
Nieuwe, zelfstandige implementatie (`audit_n5.py`, importeert géén eigen simulatoren; alleen ruwe data): RSI(2) volgens de
klassieke Wilder-definitie (seed = gemiddelde van de eerste 2 veranderingen), SMA200 inclusief de signaalbar (= EA: bar 1 is de
laatst afgesloten bar), instap op het slot van de signaaldag, uitstap (i) oorspronkelijk: slot van de eerste dag met RSI > 70,
(ii) max 1 nacht: open van de volgende dag. Vergelijking trade-voor-trade (instapdatum, uitstapdatum, bruto rendement) met
e1_rsi2_ftmo.py (FTMO-D1) en k1_nights.py (FTMO + Yahoo SPY/QQQ/GLD/DAX/N225).
Expliciete controles: (1) signaal op t gebruikt alleen data ≤ t; (2) timing instap slot t / uitstap open t+k; (3) SMA-venster
consistent met EA; (4) swap-drievoud (FTMO rollover3days) vs kalendernachten; (5) EA gebruikt afgesloten bars; (6) stop-fills.
Beslisregel: 100% trade-overeenkomst of gedocumenteerde, verklaarde verschillen. Geen nieuwe trials.
