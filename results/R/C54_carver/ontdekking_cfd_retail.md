# C54_carver — Carver-forecastcombinatie: EWMAC(8,32/16,64/32,128/64,256) + FX-carry, 16 instrumenten, vol-target per instrument 10% (trend+carry (multi-asset))
Mechanisme: Trend (onder-reactie, hedgers) en carry (risicopremie) over veel weinig-gecorreleerde markten; diversificatie is de hefboom.
Bron: Carver (2015) 'Systematic Trading'; Hurst–Ooi–Pedersen (2017); Koijen e.a. (2018)

## variant basis {} — vehikel cfd_retail
- ontdekking ≤ 2024: 24869 dagen, 88910 positie-wijzigingen, netto +0.99 bp/dag, SR +0.32 (90%-CI +0.14…+0.49)
- t: dag +3.18 | Newey-West +3.07 | blok-bootstrap +3.05 | H1 +1.98 | H2 +3.48 | +50% spread (NW) +3.03
- skew -1.56 | max dagverlies 12.97% (P99 1.50%) | maxDD 24.2% (1× notional)
- corr: ORB -0.04, RSI2 +0.26 | SPX > SMA200: +1.37 bp/dag, daaronder -0.14
- per instrument t: FX_EURUSD +2.95, FX_GBPUSD +7.77, FX_USDJPY +1.65, FX_AUDUSD +4.27, FX_USDCAD +6.80, FX_USDCHF +0.39, GOLD_F +2.04, SILVER_F +0.93, WTI_F +1.61, COPPER_F +2.11, SPX +4.67, NDX +3.17, DAX +2.45, N225 +4.46, FTSE +0.53, BOND10_SYN +4.59
- per jaar (%): 1927:+0.0 1928:+0.0 1929:+2.2 1930:+6.9 1931:+19.5 1932:+6.7 1933:-3.2 1934:-6.2 1935:+6.2 1936:+4.3 1937:+6.6 1938:-9.1 1939:-10.6 1940:-5.4 1941:+4.1 1942:+7.2 1943:+16.6 1944:-2.6 1945:+9.1 1946:-3.7 1947:-7.4 1948:-3.3 1949:+4.1 1950:+10.5 1951:-3.4 1952:+2.4 1953:-13.2 1954:+53.9 1955:+11.3 1956:-10.0 1957:+3.0 1958:+28.3 1959:-6.3 1960:-15.3 1961:+28.5 1962:+0.6 1963:-0.7 1964:+2.1 1965:-1.6 1966:-7.0 1967:-3.6 1968:+3.7 1969:+3.8 1970:+6.8 1971:+2.3 1972:+14.5 1973:-3.9 1974:-2.1 1975:-2.6 1976:+0.5 1977:+0.8 1978:+4.1 1979:-6.2 1980:-4.3 1981:-2.6 1982:+4.8 1983:+4.0 1984:+3.6 1985:+6.3 1986:+10.5 1987:+11.6 1988:+3.4 1989:+9.8 1990:-2.3 1991:+2.3 1992:-0.8 1993:+2.9 1994:-3.8 1995:+10.0 1996:+0.7 1997:+7.1 1998:+5.7 1999:+1.9 2000:-1.8 2001:+4.3 2002:+3.3 2003:+7.5 2004:+0.7 2005:+3.0 2006:+3.1 2007:-0.5 2008:+4.6 2009:-0.8 2010:+2.4 2011:-1.0 2012:-2.1 2013:+5.7 2014:-0.5 2015:-0.7 2016:-3.5 2017:+1.9 2018:+1.3 2019:-1.8 2020:+6.3 2021:+0.8 2022:-0.2 2023:-2.7 2024:+2.4
- kosten: bruto +1629.6% | spread/commissie 38.6% | financiering -1567.5% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 79% (15/19)
- G-benchmark (vehikel cfd_retail): regel SR +0.32, CAGR +5.7%, maxDD 24.2%, Calmar 0.24 | buy-and-hold (60/40 SPX/BOND10_SYN) SR +0.19, CAGR +5.0%, maxDD 68.1%, Calmar 0.07 → BETER (SR én maxDD)
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)

## variant qa {'start_jaar': 1990, 'excl': ['WTI_F']} — vehikel cfd_retail
- ontdekking ≤ 2024: 9108 dagen, 62050 positie-wijzigingen, netto +0.57 bp/dag, SR +0.37 (90%-CI +0.10…+0.64)
- t: dag +2.21 | Newey-West +2.13 | blok-bootstrap +2.20 | H1 +2.59 | H2 +0.39 | +50% spread (NW) +2.09
- skew -0.36 | max dagverlies 1.73% (P99 0.74%) | maxDD 7.8% (1× notional)
- corr: ORB -0.05, RSI2 +0.27 | SPX > SMA200: +0.70 bp/dag, daaronder -0.48
- per instrument t: FX_EURUSD +2.95, FX_GBPUSD +3.22, FX_USDJPY +1.65, FX_AUDUSD +2.91, FX_USDCAD +2.89, FX_USDCHF +0.39, GOLD_F +2.04, SILVER_F +0.93, WTI_F +55.38, COPPER_F +2.11, SPX +2.43, NDX +2.92, DAX +2.32, N225 +1.77, FTSE -0.53, BOND10_SYN +3.23
- per jaar (%): 1990:-2.2 1991:+2.3 1992:-0.8 1993:+2.9 1994:-3.8 1995:+10.0 1996:+0.7 1997:+7.1 1998:+5.7 1999:+1.9 2000:-1.8 2001:+4.2 2002:+3.7 2003:+8.0 2004:+0.6 2005:+3.0 2006:+3.2 2007:-1.1 2008:+3.7 2009:-0.3 2010:+2.8 2011:-0.4 2012:-2.0 2013:+6.1 2014:-2.0 2015:-1.2 2016:-3.4 2017:+2.0 2018:+0.8 2019:-1.2 2020:+3.0 2021:+0.2 2022:-0.5 2023:-2.4 2024:+2.9
- kosten: bruto +821.6% | spread/commissie 24.6% | financiering -736.2% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 71% (5/7)
- G-benchmark (vehikel cfd_retail): regel SR +0.37, CAGR +4.0%, maxDD 7.8%, Calmar 0.52 | buy-and-hold (60/40 SPX/BOND10_SYN) SR +0.46, CAGR +7.2%, maxDD 32.7%, Calmar 0.22 → niet beter
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
