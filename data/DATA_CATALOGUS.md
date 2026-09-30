# DATA_CATALOGUS (Uitvoerder; bijgewerkt 2026-09-30)

## D2 — lange dagdata `data/daily/` (Yahoo chart-API, eerlijke UA, 3 s/verzoek; in de repo)
Kolommen: date;open;high;low;close;adjclose;volume (6 sign. cijfers). Checksums: data/CHECKSUMS_daily.sha256.

| reeks | van | tot | dagen | dubbel | gaten > 7 d | OHLC-inconsistent | zonder OHLC | ≤ 0 | sprongen > 20% |
|---|---|---|---|---|---|---|---|---|---|
| CAC40 | 1990-03-01 | 2026-09-21 | 9285 | 0 | 0 | 0 | 0 | 0 | 0 |
| COPPER_F | 2000-08-30 | 2026-09-21 | 6543 | 0 | 0 | 300 | 0 | 0 | 1 |
| DAX | 1987-12-30 | 2026-09-21 | 9793 | 0 | 0 | 0 | 0 | 0 | 0 |
| DJI | 1992-01-02 | 2026-09-21 | 8741 | 0 | 0 | 0 | 0 | 0 | 0 |
| DXY | 1971-01-04 | 2026-09-21 | 14147 | 0 | 0 | 0 | 0 | 0 | 0 |
| EURUSD | 2003-12-01 | 2026-09-20 | 5917 | 0 | 2 | 127 | 0 | 0 | 0 |
| FTSE | 1984-01-03 | 2026-09-21 | 10791 | 0 | 0 | 0 | 0 | 0 | 0 |
| GBPUSD | 2003-12-01 | 2026-09-20 | 5929 | 0 | 0 | 103 | 0 | 0 | 0 |
| GOLD_F | 2000-08-30 | 2026-09-21 | 6539 | 0 | 0 | 441 | 0 | 0 | 0 |
| HSI | 1986-12-31 | 2026-09-21 | 9803 | 0 | 0 | 0 | 0 | 0 | 2 |
| IRX_3M | 1960-01-04 | 2026-09-21 | 16664 | 0 | 0 | 0 | 0 | 7 | 611 |
| N225 | 1965-01-05 | 2026-09-18 | 15171 | 0 | 3 | 0 | 0 | 0 | 0 |
| NASDAQ_COMP | 1971-02-05 | 2026-09-21 | 14023 | 0 | 0 | 0 | 0 | 0 | 0 |
| NATGAS_F | 2000-08-30 | 2026-09-21 | 6544 | 0 | 0 | 32 | 0 | 0 | 15 |
| NDX | 1985-10-01 | 2026-09-21 | 10322 | 0 | 0 | 0 | 0 | 0 | 0 |
| RUT | 1987-09-10 | 2026-09-21 | 9831 | 0 | 0 | 0 | 0 | 0 | 0 |
| SILVER_F | 2000-08-30 | 2026-09-21 | 6540 | 0 | 0 | 243 | 0 | 0 | 1 |
| SPX | 1927-12-30 | 2026-09-21 | 24797 | 0 | 1 | 0 | 0 | 0 | 1 |
| SPY | 1993-01-29 | 2026-09-21 | 8468 | 0 | 0 | 0 | 0 | 0 | 0 |
| STOXX50 | 2007-03-30 | 2026-09-21 | 4882 | 0 | 0 | 0 | 0 | 0 | 0 |
| TLT | 2002-07-30 | 2026-09-21 | 6075 | 0 | 0 | 0 | 0 | 0 | 0 |
| TNX_10Y | 1962-01-02 | 2026-09-21 | 16167 | 0 | 0 | 0 | 0 | 0 | 6 |
| USDJPY | 1996-10-30 | 2026-09-20 | 7751 | 0 | 2 | 277 | 0 | 0 | 0 |
| VIX | 1990-01-02 | 2026-09-21 | 9249 | 0 | 0 | 0 | 0 | 0 | 152 |
| WTI_F | 2000-08-23 | 2026-09-21 | 6547 | 0 | 0 | 7 | 0 | 1 | 11 |
| XLB | 1998-12-22 | 2026-09-21 | 6978 | 0 | 0 | 0 | 0 | 0 | 0 |
| XLE | 1998-12-22 | 2026-09-21 | 6978 | 0 | 0 | 0 | 0 | 0 | 1 |
| XLF | 1998-12-22 | 2026-09-21 | 6978 | 0 | 0 | 0 | 0 | 0 | 0 |
| XLI | 1998-12-22 | 2026-09-21 | 6978 | 0 | 0 | 0 | 0 | 0 | 0 |
| XLK | 1998-12-22 | 2026-09-21 | 6978 | 0 | 0 | 0 | 0 | 0 | 0 |
| XLP | 1998-12-22 | 2026-09-21 | 6978 | 0 | 0 | 0 | 0 | 0 | 0 |
| XLU | 1998-12-22 | 2026-09-21 | 6978 | 0 | 0 | 0 | 0 | 0 | 0 |
| XLV | 1998-12-22 | 2026-09-21 | 6978 | 0 | 0 | 0 | 0 | 0 | 0 |
| XLY | 1998-12-22 | 2026-09-21 | 6978 | 0 | 0 | 0 | 0 | 0 | 0 |

**Overlap met FTMO (2022–26, dagrendementen slot-op-slot):**

| Yahoo | FTMO | dagen | corr | mediaan niveauverschil % |
|---|---|---|---|---|
| SPX | US500cash | 1166 | 0.999 | 0.02 |
| NDX | US100cash | 1166 | 0.999 | 0.02 |
| DAX | GER40cash | 1203 | 0.992 | 0.05 |
| GOLD_F | XAUUSD | 1176 | 0.913 | 0.46 |

NB: Yahoo-indices zijn cash-indexslotkoersen; futures (GC=F e.d.) zijn doorlopende front-month-reeksen (rolsprongen mogelijk); FX (=X) vanaf 1996/2003. Dagen zonder OHLC (alleen slot) komen vooral voor in vroege jaren.

## D1 — Dukascopy-intraday `data/long_m1/` (lokaal, niet in repo)
Zie results/p0/p0_log.txt; SPX 2011 niet op de feed; 2012→ loopt. Wordt bijgewerkt zodra jaren compleet zijn.
