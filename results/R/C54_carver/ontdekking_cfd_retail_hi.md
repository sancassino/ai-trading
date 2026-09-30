# C54_carver — Carver-forecastcombinatie: EWMAC(8,32/16,64/32,128/64,256) + FX-carry, 16 instrumenten, vol-target per instrument 10% (trend+carry (multi-asset))
Mechanisme: Trend (onder-reactie, hedgers) en carry (risicopremie) over veel weinig-gecorreleerde markten; diversificatie is de hefboom.
Bron: Carver (2015) 'Systematic Trading'; Hurst–Ooi–Pedersen (2017); Koijen e.a. (2018)

## variant basis {} — vehikel cfd_retail_hi
- ontdekking ≤ 2024: 24869 dagen, 88910 positie-wijzigingen, netto +0.65 bp/dag, SR +0.21 (90%-CI +0.04…+0.39)
- t: dag +2.10 | Newey-West +2.03 | blok-bootstrap +2.03 | H1 +1.35 | H2 +2.19 | +50% spread (NW) +1.96
- skew -1.58 | max dagverlies 12.99% (P99 1.50%) | maxDD 25.2% (1× notional)
- corr: ORB -0.04, RSI2 +0.26 | SPX > SMA200: +0.99 bp/dag, daaronder -0.38
- per instrument t: FX_EURUSD +2.45, FX_GBPUSD +7.07, FX_USDJPY +1.22, FX_AUDUSD +3.59, FX_USDCAD +5.45, FX_USDCHF -0.05, GOLD_F +1.80, SILVER_F +0.75, WTI_F +1.51, COPPER_F +1.92, SPX +3.98, NDX +2.88, DAX +2.14, N225 +4.01, FTSE +0.05, BOND10_SYN +3.36
- per jaar (%): 1927:+0.0 1928:+0.0 1929:+1.7 1930:+6.6 1931:+19.2 1932:+6.4 1933:-3.3 1934:-6.4 1935:+5.8 1936:+3.7 1937:+6.2 1938:-9.3 1939:-10.8 1940:-5.6 1941:+3.5 1942:+6.5 1943:+15.6 1944:-3.4 1945:+8.0 1946:-4.1 1947:-7.7 1948:-3.9 1949:+3.5 1950:+9.4 1951:-4.5 1952:+1.1 1953:-13.9 1954:+52.0 1955:+10.3 1956:-10.6 1957:+2.1 1958:+27.0 1959:-7.6 1960:-15.8 1961:+27.0 1962:+0.3 1963:-3.1 1964:-0.7 1965:-3.3 1966:-8.2 1967:-5.0 1968:+2.2 1969:+2.6 1970:+5.7 1971:+1.6 1972:+12.5 1973:-5.1 1974:-3.6 1975:-3.7 1976:-1.1 1977:-0.5 1978:+2.5 1979:-7.7 1980:-5.8 1981:-3.5 1982:+3.9 1983:+2.8 1984:+2.8 1985:+5.3 1986:+9.5 1987:+10.4 1988:+2.5 1989:+8.6 1990:-3.2 1991:+1.2 1992:-1.6 1993:+2.0 1994:-4.5 1995:+9.0 1996:-0.3 1997:+6.1 1998:+4.9 1999:+1.5 2000:-2.4 2001:+3.9 2002:+2.8 2003:+6.8 2004:+0.2 2005:+2.3 2006:+2.4 2007:-1.2 2008:+4.3 2009:-1.1 2010:+1.8 2011:-1.5 2012:-2.6 2013:+5.0 2014:-1.3 2015:-1.3 2016:-4.0 2017:+1.0 2018:+0.5 2019:-2.7 2020:+5.7 2021:+0.1 2022:-0.7 2023:-3.2 2024:+1.7
- kosten: bruto +1629.6% | spread/commissie 77.2% | financiering -1102.8% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 68% (13/19)
- G-benchmark (vehikel cfd_retail_hi): regel SR +0.21, CAGR +4.8%, maxDD 25.2%, Calmar 0.19 | buy-and-hold (60/40 SPX/BOND10_SYN) SR +0.12, CAGR +4.1%, maxDD 68.6%, Calmar 0.06 → BETER (SR én maxDD)
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)

## variant qa {'start_jaar': 1990, 'excl': ['WTI_F']} — vehikel cfd_retail_hi
- ontdekking ≤ 2024: 9108 dagen, 62050 positie-wijzigingen, netto +0.31 bp/dag, SR +0.20 (90%-CI -0.06…+0.48)
- t: dag +1.22 | Newey-West +1.18 | blok-bootstrap +1.22 | H1 +1.86 | H2 -0.28 | +50% spread (NW) +1.10
- skew -0.37 | max dagverlies 1.73% (P99 0.75%) | maxDD 9.0% (1× notional)
- corr: ORB -0.05, RSI2 +0.27 | SPX > SMA200: +0.42 bp/dag, daaronder -0.66
- per instrument t: FX_EURUSD +2.45, FX_GBPUSD +2.68, FX_USDJPY +1.22, FX_AUDUSD +2.39, FX_USDCAD +2.07, FX_USDCHF -0.05, GOLD_F +1.80, SILVER_F +0.75, WTI_F +55.38, COPPER_F +1.92, SPX +2.02, NDX +2.64, DAX +2.02, N225 +1.51, FTSE -0.99, BOND10_SYN +2.41
- per jaar (%): 1990:-3.1 1991:+1.2 1992:-1.6 1993:+2.0 1994:-4.5 1995:+9.0 1996:-0.3 1997:+6.1 1998:+4.9 1999:+1.5 2000:-2.4 2001:+3.8 2002:+3.2 2003:+7.4 2004:+0.1 2005:+2.3 2006:+2.5 2007:-1.8 2008:+3.3 2009:-0.6 2010:+2.3 2011:-0.9 2012:-2.5 2013:+5.5 2014:-2.8 2015:-1.7 2016:-3.8 2017:+1.2 2018:+0.0 2019:-2.0 2020:+2.4 2021:-0.5 2022:-0.9 2023:-2.9 2024:+2.2
- kosten: bruto +821.6% | spread/commissie 49.2% | financiering -465.4% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 71% (5/7)
- G-benchmark (vehikel cfd_retail_hi): regel SR +0.20, CAGR +3.4%, maxDD 9.0%, Calmar 0.38 | buy-and-hold (60/40 SPX/BOND10_SYN) SR +0.37, CAGR +6.1%, maxDD 33.6%, Calmar 0.18 → niet beter
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
