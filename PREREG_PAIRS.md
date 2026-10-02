# PREREG — Relatieve waarde indices (2 okt 2026)
Paren (vooraf): NDX–SPX, DAX–STOXX50, DJI–SPX, DAX–FTSE. Spread-dagrendement s = r_A − r_B. Signaal: z = som s over 5 d / (std s * sqrt5), uit data t/m gisteren. Mean-reversion: positie = −sign(z) als |z|>1.5, houd 1 dag. Variant 2: houd 5 dagen. Gate: bruto per trade >= 3x kosten (≈ 2.6bp per dag-rebalance + swap ~2.4bp/dag).
Train 1995–2015, test 2016–2024. PASS: netto>0, t>=2 in train én test, >=3/4 paren. Trials +8.
