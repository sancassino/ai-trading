# C54_carver — Carver-forecastcombinatie: EWMAC(8,32/16,64/32,128/64,256) + FX-carry, 16 instrumenten, vol-target per instrument 10% (trend+carry (multi-asset))
Mechanisme: Trend (onder-reactie, hedgers) en carry (risicopremie) over veel weinig-gecorreleerde markten; diversificatie is de hefboom.
Bron: Carver (2015) 'Systematic Trading'; Hurst–Ooi–Pedersen (2017); Koijen e.a. (2018)

## variant basis {} — vehikel future
- ontdekking ≤ 2024: 24869 dagen, 96020 positie-wijzigingen, netto +1.34 bp/dag, SR +0.44 (90%-CI +0.27…+0.61)
- t: dag +4.36 | Newey-West +4.22 | blok-bootstrap +4.15 | H1 +2.87 | H2 +4.52 | +50% spread (NW) +4.19
- skew -1.51 | max dagverlies 12.94% (P99 1.49%) | maxDD 23.3% (1× notional)
- corr: ORB -0.04, RSI2 +0.26 | SPX > SMA200: +1.71 bp/dag, daaronder +0.26
- per instrument t: FX_EURUSD +3.53, FX_GBPUSD +6.42, FX_USDJPY +7.57, FX_AUDUSD +2.70, FX_USDCAD +8.26, FX_USDCHF +6.55, GOLD_F +2.08, SILVER_F +1.07, WTI_F +1.69, COPPER_F +2.29, SPX +5.21, NDX +3.58, DAX +2.88, N225 +5.10, FTSE +1.17, BOND10_SYN +6.28
- per jaar (%): 1927:+0.0 1928:+0.0 1929:+3.0 1930:+7.3 1931:+19.9 1932:+7.0 1933:-3.0 1934:-5.9 1935:+6.6 1936:+5.2 1937:+7.1 1938:-8.8 1939:-10.4 1940:-5.2 1941:+4.8 1942:+8.1 1943:+18.0 1944:-1.4 1945:+10.7 1946:-3.0 1947:-7.0 1948:-2.6 1949:+5.1 1950:+12.1 1951:-2.0 1952:+4.3 1953:-12.1 1954:+56.7 1955:+12.7 1956:-9.0 1957:+4.2 1958:+30.1 1959:-4.6 1960:-14.5 1961:+30.6 1962:+1.1 1963:+2.8 1964:+6.1 1965:+0.7 1966:-5.4 1967:-1.6 1968:+5.8 1969:+5.4 1970:+8.2 1971:+1.8 1972:+16.9 1973:+1.1 1974:-1.2 1975:-2.7 1976:+2.9 1977:+7.9 1978:+6.3 1979:-3.1 1980:-6.3 1981:+2.1 1982:+5.9 1983:+4.6 1984:+3.8 1985:+8.7 1986:+12.4 1987:+12.3 1988:+1.9 1989:+11.0 1990:-1.9 1991:+2.5 1992:-0.8 1993:+3.1 1994:-3.1 1995:+9.8 1996:-0.1 1997:+6.0 1998:+4.1 1999:+2.9 2000:-1.6 2001:+5.1 2002:+3.3 2003:+7.5 2004:+0.9 2005:+3.0 2006:+2.8 2007:-1.3 2008:+4.8 2009:-0.4 2010:+2.8 2011:-0.5 2012:-1.6 2013:+6.4 2014:+0.4 2015:-0.0 2016:-3.0 2017:+2.6 2018:+1.6 2019:-1.6 2020:+6.9 2021:+1.6 2022:+0.2 2023:-3.1 2024:+1.6
- kosten: bruto +1467.2% | spread/commissie 25.9% | financiering -2649.1% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 95% (18/19)
- G-benchmark (vehikel future): regel SR +0.44, CAGR +6.7%, maxDD 23.3%, Calmar 0.29 | buy-and-hold (60/40 SPX/BOND10_SYN) SR +0.26, CAGR +5.9%, maxDD 67.3%, Calmar 0.09 → BETER (SR én maxDD)
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
