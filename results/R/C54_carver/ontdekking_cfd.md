# C54_carver — Carver-forecastcombinatie: EWMAC(8,32/16,64/32,128/64,256) + FX-carry, 16 instrumenten, vol-target per instrument 10% (trend+carry (multi-asset))
Mechanisme: Trend (onder-reactie, hedgers) en carry (risicopremie) over veel weinig-gecorreleerde markten; diversificatie is de hefboom.
Bron: Carver (2015) 'Systematic Trading'; Hurst–Ooi–Pedersen (2017); Koijen e.a. (2018)

## variant basis {} — vehikel cfd
- ontdekking ≤ 2024: 24868 dagen, 77607 positie-wijzigingen, netto +0.62 bp/dag, SR +0.19 (90%-CI +0.03…+0.36)
- t: dag +1.90 | Newey-West +1.82 | blok-bootstrap +1.84 | H1 +1.29 | H2 +1.84 | +50% spread (NW) +1.80
- skew -1.51 | max dagverlies 12.99% (P99 1.60%) | maxDD 40.6% (1× notional)
- corr: ORB -0.04, RSI2 +0.30 | SPX > SMA200: +1.01 bp/dag, daaronder -0.54
- per instrument t: FX_EURUSD +1.32, FX_GBPUSD +3.45, FX_USDJPY +0.36, FX_AUDUSD +0.15, FX_USDCAD +1.39, FX_USDCHF -1.72, GOLD_F +0.07, SILVER_F -0.66, WTI_F -0.22, COPPER_F +nan, SPX +0.55, NDX +0.55, DAX +0.20, N225 +1.09, FTSE -2.71, BOND10_SYN +nan
- per jaar (%): 1927:+0.0 1928:+0.0 1929:+1.2 1930:+6.2 1931:+18.7 1932:+6.1 1933:-3.5 1934:-6.6 1935:+5.4 1936:+3.0 1937:+5.7 1938:-9.6 1939:-11.0 1940:-6.0 1941:+2.7 1942:+5.6 1943:+14.5 1944:-4.3 1945:+6.9 1946:-4.7 1947:-8.1 1948:-4.5 1949:+2.6 1950:+8.2 1951:-5.6 1952:-0.2 1953:-15.0 1954:+49.2 1955:+9.6 1956:-10.7 1957:+1.0 1958:+26.3 1959:-6.9 1960:-16.6 1961:+26.9 1962:-0.1 1963:+7.1 1964:+7.0 1965:+1.1 1966:-10.7 1967:-4.2 1968:+8.0 1969:+0.6 1970:+1.7 1971:-0.2 1972:+17.5 1973:-4.6 1974:-4.7 1975:-2.0 1976:-4.8 1977:+3.4 1978:+6.2 1979:-3.8 1980:-3.2 1981:-1.2 1982:+0.5 1983:+8.3 1984:+2.2 1985:+2.9 1986:+9.7 1987:+14.1 1988:+4.6 1989:+10.6 1990:-2.4 1991:-2.0 1992:-2.3 1993:-1.1 1994:-5.8 1995:+6.1 1996:+1.6 1997:+6.2 1998:+3.4 1999:+2.4 2000:-3.6 2001:+3.8 2002:+3.4 2003:+6.8 2004:-0.8 2005:+1.6 2006:+0.5 2007:-1.3 2008:+2.7 2009:-1.1 2010:+0.7 2011:-2.3 2012:-3.3 2013:+4.7 2014:-2.6 2015:-3.6 2016:-4.5 2017:-0.7 2018:+0.6 2019:-4.5 2020:+4.2 2021:-1.5 2022:-1.4 2023:-4.0 2024:+1.7
- kosten: bruto +1426.6% | spread/commissie 25.2% | financiering +1136.7% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 68% (13/19)
- G-benchmark (vehikel cfd): regel SR +0.19, CAGR +1.2%, maxDD 40.6%, Calmar 0.03 | buy-and-hold (60/40 SPX/BOND10_SYN) SR +0.15, CAGR +1.1%, maxDD 70.3%, Calmar 0.01 → BETER (SR én maxDD)
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)

## variant qa {'start_jaar': 1990, 'excl': ['WTI_F']} — vehikel cfd
- ontdekking ≤ 2024: 9107 dagen, 54097 positie-wijzigingen, netto +0.02 bp/dag, SR +0.01 (90%-CI -0.26…+0.27)
- t: dag +0.09 | Newey-West +0.08 | blok-bootstrap +0.09 | H1 +1.11 | H2 -1.11 | +50% spread (NW) +0.05
- skew -0.43 | max dagverlies 1.82% (P99 0.79%) | maxDD 22.3% (1× notional)
- corr: ORB -0.05, RSI2 +0.30 | SPX > SMA200: +0.16 bp/dag, daaronder -1.03
- per instrument t: FX_EURUSD +1.32, FX_GBPUSD +0.88, FX_USDJPY +0.36, FX_AUDUSD +0.23, FX_USDCAD +0.10, FX_USDCHF -1.72, GOLD_F +0.07, SILVER_F -0.66, WTI_F +nan, COPPER_F +nan, SPX -0.11, NDX +0.59, DAX +0.20, N225 -0.72, FTSE -3.38, BOND10_SYN +nan
- per jaar (%): 1990:-2.4 1991:-2.0 1992:-2.3 1993:-1.1 1994:-5.8 1995:+6.1 1996:+1.6 1997:+6.2 1998:+3.4 1999:+2.4 2000:-3.6 2001:+4.1 2002:+3.8 2003:+7.5 2004:-1.2 2005:+1.4 2006:+0.9 2007:-2.1 2008:+1.7 2009:-0.4 2010:+1.1 2011:-1.7 2012:-2.7 2013:+5.3 2014:-3.2 2015:-2.5 2016:-4.1 2017:-0.5 2018:-0.2 2019:-3.5 2020:+0.7 2021:-2.7 2022:-1.5 2023:-3.2 2024:+2.7
- kosten: bruto +541.5% | spread/commissie 16.5% | financiering +674.1% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 43% (3/7)
- G-benchmark (vehikel cfd): regel SR +0.01, CAGR -0.0%, maxDD 22.3%, Calmar -0.00 | buy-and-hold (60/40 SPX/BOND10_SYN) SR +0.26, CAGR +2.3%, maxDD 50.5%, Calmar 0.04 → niet beter
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
