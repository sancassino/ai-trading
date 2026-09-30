# C54_carver — Carver-forecastcombinatie: EWMAC(8,32/16,64/32,128/64,256) + FX-carry, 16 instrumenten, vol-target per instrument 10% (trend+carry (multi-asset))
Mechanisme: Trend (onder-reactie, hedgers) en carry (risicopremie) over veel weinig-gecorreleerde markten; diversificatie is de hefboom.
Bron: Carver (2015) 'Systematic Trading'; Hurst–Ooi–Pedersen (2017); Koijen e.a. (2018)

## variant basis {} — vehikel future
- ontdekking ≤ 2024: 24869 dagen, 88910 positie-wijzigingen, netto +1.44 bp/dag, SR +0.47 (90%-CI +0.29…+0.64)
- t: dag +4.63 | Newey-West +4.47 | blok-bootstrap +4.43 | H1 +2.87 | H2 +5.14 | +50% spread (NW) +4.44
- skew -1.53 | max dagverlies 12.94% (P99 1.49%) | maxDD 23.3% (1× notional)
- corr: ORB -0.05, RSI2 +0.26 | SPX > SMA200: +1.89 bp/dag, daaronder +0.19
- per instrument t: FX_EURUSD +3.67, FX_GBPUSD +8.77, FX_USDJPY +2.26, FX_AUDUSD +5.23, FX_USDCAD +8.72, FX_USDCHF +1.01, GOLD_F +2.38, SILVER_F +1.15, WTI_F +1.74, COPPER_F +2.35, SPX +5.21, NDX +3.58, DAX +2.88, N225 +5.10, FTSE +1.17, BOND10_SYN +6.28
- per jaar (%): 1927:+0.0 1928:+0.0 1929:+3.0 1930:+7.3 1931:+19.9 1932:+7.0 1933:-3.0 1934:-5.9 1935:+6.6 1936:+5.2 1937:+7.1 1938:-8.8 1939:-10.4 1940:-5.2 1941:+4.8 1942:+8.1 1943:+18.0 1944:-1.4 1945:+10.7 1946:-3.0 1947:-7.0 1948:-2.6 1949:+5.1 1950:+12.1 1951:-2.0 1952:+4.3 1953:-12.1 1954:+56.7 1955:+12.7 1956:-9.0 1957:+4.2 1958:+30.1 1959:-4.6 1960:-14.5 1961:+30.6 1962:+1.1 1963:+2.8 1964:+6.1 1965:+0.7 1966:-5.4 1967:-1.6 1968:+5.8 1969:+5.4 1970:+8.2 1971:+3.3 1972:+17.4 1973:-2.1 1974:+0.1 1975:-1.0 1976:+2.6 1977:+2.8 1978:+6.3 1979:-4.2 1980:-2.1 1981:-1.3 1982:+5.9 1983:+5.7 1984:+4.9 1985:+7.6 1986:+11.9 1987:+13.3 1988:+4.6 1989:+11.2 1990:-1.0 1991:+3.7 1992:-0.0 1993:+3.8 1994:-3.0 1995:+10.9 1996:+1.9 1997:+8.3 1998:+6.8 1999:+2.4 2000:-1.0 2001:+4.9 2002:+4.1 2003:+8.3 2004:+1.4 2005:+3.9 2006:+4.0 2007:+0.5 2008:+5.2 2009:-0.3 2010:+3.0 2011:-0.3 2012:-1.4 2013:+6.4 2014:+0.5 2015:-0.1 2016:-2.9 2017:+2.7 2018:+2.3 2019:-0.7 2020:+7.0 2021:+1.7 2022:+0.4 2023:-2.0 2024:+3.4
- kosten: bruto +1583.6% | spread/commissie 24.3% | financiering -2255.3% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 95% (18/19)
- G-benchmark (vehikel future): regel SR +0.47, CAGR +6.9%, maxDD 23.3%, Calmar 0.30 | buy-and-hold (60/40 SPX/BOND10_SYN) SR +0.26, CAGR +5.9%, maxDD 67.3%, Calmar 0.09 → BETER (SR én maxDD)
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)

## variant qa {'start_jaar': 1990, 'excl': ['WTI_F']} — vehikel future
- ontdekking ≤ 2024: 9108 dagen, 62050 positie-wijzigingen, netto +0.89 bp/dag, SR +0.57 (90%-CI +0.30…+0.85)
- t: dag +3.44 | Newey-West +3.32 | blok-bootstrap +3.40 | H1 +3.50 | H2 +1.22 | +50% spread (NW) +3.29
- skew -0.35 | max dagverlies 1.72% (P99 0.74%) | maxDD 6.9% (1× notional)
- corr: ORB -0.05, RSI2 +0.27 | SPX > SMA200: +1.02 bp/dag, daaronder -0.21
- per instrument t: FX_EURUSD +3.67, FX_GBPUSD +4.00, FX_USDJPY +2.26, FX_AUDUSD +3.63, FX_USDCAD +4.04, FX_USDCHF +1.01, GOLD_F +2.38, SILVER_F +1.15, WTI_F +55.38, COPPER_F +2.35, SPX +2.34, NDX +3.30, DAX +2.75, N225 +2.13, FTSE +0.08, BOND10_SYN +4.35
- per jaar (%): 1990:-0.9 1991:+3.7 1992:-0.0 1993:+3.8 1994:-3.0 1995:+10.9 1996:+1.9 1997:+8.3 1998:+6.8 1999:+2.4 2000:-1.0 2001:+4.8 2002:+4.5 2003:+8.8 2004:+1.3 2005:+3.9 2006:+4.1 2007:-0.1 2008:+4.2 2009:+0.2 2010:+3.4 2011:+0.2 2012:-1.4 2013:+6.8 2014:-1.1 2015:-0.5 2016:-2.8 2017:+2.9 2018:+1.8 2019:-0.1 2020:+3.7 2021:+1.0 2022:+0.1 2023:-1.8 2024:+3.8
- kosten: bruto +779.2% | spread/commissie 15.2% | financiering -1136.8% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 100% (7/7)
- G-benchmark (vehikel future): regel SR +0.57, CAGR +4.9%, maxDD 6.9%, Calmar 0.70 | buy-and-hold (60/40 SPX/BOND10_SYN) SR +0.49, CAGR +7.5%, maxDD 32.7%, Calmar 0.23 → BETER (SR én maxDD)
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
