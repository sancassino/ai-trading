# PREREG — crypto intraday US-open momentum (2 okt 2026)
Mechanisme: ETF/US-institutionele stroom bij US-open (14:30 UTC) geeft richting. Swap crypto 11.9bp/dag => alleen intraday, positie dicht voor rollover.
Regel: r1 = rendement 14:30–15:00 UTC; positie = sign(r1) van 15:00 tot 17:00 UTC (2u). Alleen |r1| > mediaan afgelopen 60 dagen. BTCUSD, ETHUSD. Kosten: rondreis uit COSTS (BTC 1.25bp, ETH 8bp).
Train 2021–2023, test 2024; 2025+ ongebruikt. PASS: netto>0, dag-t>=2 train én test, beide coins. Trials +2 (CEO-T12).
