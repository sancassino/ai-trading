# DATA_CATALOGUS (Uitvoerder; bijgewerkt 2026-09-30)

## D2 — lange dagdata `data/daily/` (Yahoo chart-API, eerlijke UA, 3 s/verzoek; in de repo)
Kolommen: date;open;high;low;close;adjclose;volume (6 sign. cijfers). Checksums: data/CHECKSUMS_daily.sha256.

| reeks | van | tot | dagen | dubbel | gaten > 7 d | OHLC-inconsistent | zonder OHLC | ≤ 0 | sprongen > 20% |
|---|---|---|---|---|---|---|---|---|---|
| AGG | 2003-09-29 | 2026-09-21 | 5781 | 0 | 0 | 0 | 0 | 0 | 0 |
| AUDUSD | 2006-05-15 | 2026-09-20 | 5293 | 0 | 0 | 146 | 0 | 0 | 0 |
| BRENT_F | 2007-07-30 | 2026-09-21 | 4765 | 0 | 1 | 69 | 0 | 0 | 3 |
| BUND_ETF | 2008-01-02 | 2026-09-21 | 4753 | 0 | 0 | 4 | 0 | 0 | 0 |
| BWX | 2007-10-11 | 2026-09-21 | 4765 | 0 | 0 | 0 | 0 | 0 | 0 |
| CAC40 | 1990-03-01 | 2026-09-21 | 9285 | 0 | 0 | 0 | 0 | 0 | 0 |
| CATTLE_F | 2001-03-01 | 2026-09-21 | 6405 | 0 | 1 | 244 | 0 | 0 | 0 |
| COFFEE_F | 2000-01-03 | 2026-09-21 | 6698 | 0 | 0 | 719 | 0 | 0 | 0 |
| COPPER_F | 2000-08-30 | 2026-09-21 | 6543 | 0 | 0 | 300 | 0 | 0 | 1 |
| CORN_F | 2000-07-17 | 2026-09-21 | 6550 | 0 | 2 | 831 | 0 | 0 | 1 |
| COTTON_F | 2000-01-03 | 2026-09-21 | 6700 | 0 | 0 | 569 | 0 | 0 | 1 |
| CPER | 2011-11-15 | 2026-09-21 | 3732 | 0 | 0 | 0 | 0 | 0 | 4 |
| CPI_US | 1913-01-01 | 2026-08-01 | 1363 | 0 | 1362 | 0 | 1363 | 0 | 0 |
| DAX | 1987-12-30 | 2026-09-21 | 9793 | 0 | 0 | 0 | 0 | 0 | 0 |
| DBA | 2007-01-05 | 2026-09-21 | 4958 | 0 | 0 | 0 | 0 | 0 | 0 |
| DBC | 2006-02-06 | 2026-09-21 | 5188 | 0 | 0 | 0 | 0 | 0 | 0 |
| DJI | 1992-01-02 | 2026-09-21 | 8741 | 0 | 0 | 0 | 0 | 0 | 0 |
| DXY | 1971-01-04 | 2026-09-21 | 14147 | 0 | 0 | 0 | 0 | 0 | 0 |
| EEM | 2003-04-14 | 2026-09-21 | 5897 | 0 | 0 | 0 | 0 | 0 | 2 |
| EFA | 2001-08-27 | 2026-09-21 | 6303 | 0 | 0 | 0 | 0 | 0 | 0 |
| EMB | 2007-12-19 | 2026-09-21 | 4717 | 0 | 0 | 0 | 0 | 0 | 0 |
| EURCHF | 2003-01-23 | 2026-09-20 | 6140 | 0 | 1 | 80 | 0 | 0 | 0 |
| EURGBP | 1999-01-04 | 2026-09-20 | 7217 | 0 | 0 | 69 | 0 | 0 | 0 |
| EURJPY | 2003-01-23 | 2026-09-20 | 6142 | 0 | 1 | 233 | 0 | 0 | 0 |
| EURUSD | 2003-12-01 | 2026-09-20 | 5917 | 0 | 2 | 127 | 0 | 0 | 0 |
| FTSE | 1984-01-03 | 2026-09-21 | 10791 | 0 | 0 | 0 | 0 | 0 | 0 |
| FVX_5Y | 1962-01-02 | 2026-09-21 | 16167 | 0 | 0 | 0 | 0 | 0 | 16 |
| FX_AUDUSD | 1971-01-04 | 2026-09-25 | 13969 | 0 | 1 | 0 | 13969 | 0 | 0 |
| FX_EURUSD | 1999-01-04 | 2026-09-25 | 6955 | 0 | 0 | 0 | 6955 | 0 | 0 |
| FX_GBPUSD | 1971-01-04 | 2026-09-25 | 13976 | 0 | 1 | 0 | 13976 | 0 | 0 |
| FX_NZDUSD | 1971-01-04 | 2026-09-25 | 13960 | 0 | 2 | 0 | 13960 | 0 | 0 |
| FX_USDCAD | 1971-01-04 | 2026-09-25 | 13982 | 0 | 0 | 0 | 13982 | 0 | 0 |
| FX_USDCHF | 1971-01-04 | 2026-09-25 | 13976 | 0 | 1 | 0 | 13976 | 0 | 0 |
| FX_USDJPY | 1971-01-04 | 2026-09-25 | 13970 | 0 | 1 | 0 | 13970 | 0 | 0 |
| GASOLINE_F | 2000-11-01 | 2026-09-21 | 6502 | 0 | 0 | 4 | 0 | 0 | 10 |
| GBPUSD | 2003-12-01 | 2026-09-20 | 5929 | 0 | 0 | 103 | 0 | 0 | 0 |
| GILT_ETF | 2008-01-02 | 2026-09-21 | 4729 | 0 | 0 | 84 | 0 | 0 | 0 |
| GLD | 2004-11-18 | 2026-09-21 | 5493 | 0 | 0 | 0 | 0 | 0 | 0 |
| GOLD_F | 2000-08-30 | 2026-09-21 | 6539 | 0 | 0 | 441 | 0 | 0 | 0 |
| HEATOIL_F | 2000-09-01 | 2026-09-21 | 6541 | 0 | 0 | 8 | 0 | 0 | 1 |
| HSI | 1986-12-31 | 2026-09-21 | 9803 | 0 | 0 | 0 | 0 | 0 | 2 |
| HYG | 2007-04-11 | 2026-09-21 | 4893 | 0 | 0 | 0 | 0 | 0 | 0 |
| IEF | 2002-07-30 | 2026-09-21 | 6075 | 0 | 0 | 0 | 0 | 0 | 0 |
| IRX_3M | 1960-01-04 | 2026-09-21 | 16664 | 0 | 0 | 0 | 0 | 7 | 611 |
| IWM | 2000-05-26 | 2026-09-21 | 6618 | 0 | 0 | 0 | 0 | 0 | 0 |
| LQD | 2002-07-30 | 2026-09-21 | 6075 | 0 | 0 | 0 | 0 | 0 | 0 |
| N225 | 1965-01-05 | 2026-09-18 | 15171 | 0 | 3 | 0 | 0 | 0 | 0 |
| NASDAQ_COMP | 1971-02-05 | 2026-09-21 | 14023 | 0 | 0 | 0 | 0 | 0 | 0 |
| NATGAS_F | 2000-08-30 | 2026-09-21 | 6544 | 0 | 0 | 32 | 0 | 0 | 15 |
| NDX | 1985-10-01 | 2026-09-21 | 10322 | 0 | 0 | 0 | 0 | 0 | 0 |
| NZDUSD | 2003-12-01 | 2026-09-20 | 5918 | 0 | 0 | 367 | 0 | 0 | 0 |
| PALL_F | 1998-09-28 | 2026-09-21 | 6577 | 0 | 21 | 508 | 0 | 0 | 4 |
| PLAT_F | 1997-10-29 | 2026-09-21 | 6566 | 0 | 22 | 473 | 0 | 0 | 4 |
| PPLT | 2010-01-08 | 2026-09-21 | 4200 | 0 | 0 | 0 | 0 | 0 | 0 |
| RUT | 1987-09-10 | 2026-09-21 | 9831 | 0 | 0 | 0 | 0 | 0 | 0 |
| SHY | 2002-07-30 | 2026-09-21 | 6075 | 0 | 0 | 0 | 0 | 0 | 0 |
| SILVER_F | 2000-08-30 | 2026-09-21 | 6540 | 0 | 0 | 243 | 0 | 0 | 1 |
| SLV | 2006-04-28 | 2026-09-21 | 5131 | 0 | 0 | 0 | 0 | 0 | 1 |
| SOY_F | 2000-09-15 | 2026-09-21 | 6542 | 0 | 0 | 847 | 0 | 0 | 2 |
| SPX | 1927-12-30 | 2026-09-21 | 24797 | 0 | 1 | 0 | 0 | 0 | 1 |
| SPX_EQW | 2003-05-01 | 2026-09-21 | 5885 | 0 | 0 | 0 | 0 | 0 | 0 |
| SPX_TR | 1988-01-04 | 2026-09-21 | 9752 | 0 | 0 | 0 | 0 | 0 | 0 |
| SPY | 1993-01-29 | 2026-09-21 | 8468 | 0 | 0 | 0 | 0 | 0 | 0 |
| STOXX50 | 2007-03-30 | 2026-09-21 | 4882 | 0 | 0 | 0 | 0 | 0 | 0 |
| SUGAR_F | 2000-03-01 | 2026-09-21 | 6661 | 0 | 0 | 11 | 0 | 0 | 1 |
| TIP | 2003-12-05 | 2026-09-21 | 5733 | 0 | 0 | 0 | 0 | 0 | 0 |
| TLT | 2002-07-30 | 2026-09-21 | 6075 | 0 | 0 | 0 | 0 | 0 | 0 |
| TNX_10Y | 1962-01-02 | 2026-09-21 | 16167 | 0 | 0 | 0 | 0 | 0 | 6 |
| TYX_30Y | 1977-02-15 | 2026-09-21 | 12425 | 0 | 0 | 0 | 0 | 0 | 3 |
| UNG | 2007-04-18 | 2026-09-21 | 4888 | 0 | 0 | 0 | 0 | 0 | 1 |
| USDCAD | 2003-09-16 | 2026-09-20 | 5985 | 0 | 0 | 114 | 0 | 0 | 0 |
| USDCHF | 2003-09-16 | 2026-09-20 | 5983 | 0 | 0 | 102 | 0 | 0 | 0 |
| USDJPY | 1996-10-30 | 2026-09-20 | 7751 | 0 | 2 | 277 | 0 | 0 | 0 |
| USDNOK | 2001-07-15 | 2026-09-20 | 6376 | 0 | 3 | 96 | 0 | 0 | 2 |
| USDSEK | 2001-07-15 | 2026-09-20 | 6376 | 0 | 3 | 97 | 0 | 0 | 0 |
| USO | 2006-04-10 | 2026-09-21 | 5144 | 0 | 0 | 0 | 0 | 0 | 2 |
| VIX | 1990-01-02 | 2026-09-21 | 9249 | 0 | 0 | 0 | 0 | 0 | 152 |
| VNQ | 2004-09-29 | 2026-09-21 | 5529 | 0 | 0 | 0 | 0 | 0 | 0 |
| WHEAT_F | 2000-07-17 | 2026-09-21 | 6562 | 0 | 1 | 835 | 0 | 0 | 1 |
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
| YLD_DE10Y | 1997-08-07 | 2026-09-30 | 7399 | 0 | 0 | 0 | 7399 | 809 | 238 |
| YLD_JP10Y | 1986-07-05 | 2026-08-31 | 9929 | 0 | 2 | 0 | 9929 | 455 | 451 |
| YLD_UK10Y | 1982-01-04 | 2026-09-28 | 11307 | 0 | 0 | 0 | 11307 | 0 | 37 |
| YLD_US10Y | 1990-01-02 | 2026-09-29 | 9192 | 0 | 0 | 0 | 9192 | 0 | 4 |
| YLD_US2Y | 1990-01-02 | 2026-09-29 | 9192 | 0 | 0 | 0 | 9192 | 0 | 36 |
| YLD_US30Y | 1990-01-02 | 2026-09-29 | 8198 | 0 | 1 | 0 | 8198 | 0 | 3 |
| YLD_US3M | 1990-01-02 | 2026-09-29 | 9189 | 0 | 0 | 0 | 9189 | 18 | 612 |

**Overlap met FTMO (2022–26, dagrendementen slot-op-slot):**

| Yahoo | FTMO | dagen | corr | mediaan |niveauverschil| % |
|---|---|---|---|---|
| SPX | US500cash | 1166 | 0.999 | 0.02 |
| NDX | US100cash | 1166 | 0.999 | 0.02 |
| DAX | GER40cash | 1203 | 0.992 | 0.05 |
| GOLD_F | XAUUSD | 1176 | 0.913 | 0.46 |

NB: Yahoo-indices zijn cash-indexslotkoersen; futures (GC=F e.d.) zijn doorlopende front-month-reeksen (rolsprongen mogelijk); FX (=X) vanaf 1996/2003. Dagen zonder OHLC (alleen slot) komen vooral voor in vroege jaren.

**Uitbreiding D-044 (2026-09-30):** (b) C54-universum: FX USDSEK, USDNOK, EURGBP, EURJPY, EURCHF (Yahoo =X, 1999/2001/2003→); agri/energie/metaal-futures
CORN_F, WHEAT_F, SOY_F, COFFEE_F, SUGAR_F, COTTON_F, CATTLE_F, HEATOIL_F, GASOLINE_F, BRENT_F, PLAT_F, PALL_F (doorlopend front-month, rolsprongen!);
obligatieproxy's BUND_ETF (EXX6.DE), GILT_ETF (IGLT.L), BWX, EMB; SPX_EQW (RSP). (c) roll-inclusieve ETF-proxy's CPER (koper, 2011→), UNG (gas, 2007→),
USO (olie, 2006→), PPLT (platina, 2010→), DBA (agri, 2007→) — de ETF draagt de rolkosten, dus 'roll-schoon' als rendementsreeks.
(d) FRED is ook vanaf Debian geblokkeerd (verbinding direct geweigerd; de API vereist een account/sleutel → niet gebruikt). Vervangen door officiële openbare bronnen
(fetch_official.py, eerlijke UA, 3 s/verzoek): **YLD_US3M/2Y/10Y/30Y** (US Treasury daily par yield curve, 1990→, publiek domein),
**YLD_JP10Y** (Ministry of Finance Japan, 1986→), **YLD_UK10Y** (Bank of England IUDMNZC, 1982→; BoE-voorwaarden: vrij gebruik met bronvermelding),
**YLD_DE10Y** (Deutsche Bundesbank, Svensson 10j, 1997→; vrij met bronvermelding), **CPI_US** (BLS CPI-U, 1913→, maandelijks, publiek domein).
(a) total return: SPX_TR (1988→); DAX is al een performance-index; NDX-TR niet vrij beschikbaar (Yahoo ^XNDX 422) → prijsindex, dividend genegeerd (vermeld).
Let op: rendementsreeksen van yields (YLD_*) zijn niveaus in %, geen prijzen — regels moeten ze als signaal of via duratie-benadering gebruiken.

**EUR-geldmarkt (ECB Data Portal, officieel, openbaar):** YLD_ESTR (€STR dagelijks, 2019-10→), YLD_EURIBOR3M (maandgemiddelde, 1994→).

## D1 — Dukascopy-intraday `data/long_m1/` (lokaal, niet in repo)
Zie results/p0/p0_log.txt; SPX 2011 niet op de feed; 2012→ loopt. Wordt bijgewerkt zodra jaren compleet zijn.
