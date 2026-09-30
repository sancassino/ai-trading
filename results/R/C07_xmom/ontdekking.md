# C07_xmom — Cross-asset momentum 12-1, lang top-3 / kort bottom-3 (cross-sectioneel)
Mechanisme: Relatieve trend tussen markten.
Bron: Asness, Moskowitz, Pedersen (2013)

## variant basis {}
- ontdekking ≤ 2024: 24868 dagen, 1191 positie-wijzigingen, netto +0.00 bp/dag, SR +0.00 (90%-CI -0.16…+0.17)
- t: dag +0.02 | Newey-West +0.02 | blok-bootstrap +0.02 | H1 -0.75 | H2 +0.27 | +50% spread (NW) +0.01
- skew -1.41 | max dagverlies 6.32% (P99 0.86%) | maxDD 41.4% (1× notional)
- corr: ORB -0.11, RSI2 +0.21 | SPX > SMA200: +0.65 bp/dag, daaronder -1.22
- per instrument t: FX_EURUSD -0.67, FX_GBPUSD -0.86, FX_USDJPY -0.26, FX_AUDUSD -0.94, FX_USDCAD -0.87, FX_USDCHF -2.38, GOLD_F +1.20, SILVER_F +0.12, SPX +0.49, NDX +1.39, DAX -0.20, N225 +0.00
- per jaar (%): 1927:+0.0 1928:+0.0 1929:+0.0 1930:+0.0 1931:+0.0 1932:+0.0 1933:+0.0 1934:+0.0 1935:+0.0 1936:+0.0 1937:+0.0 1938:+0.0 1939:+0.0 1940:+0.0 1941:+0.0 1942:+0.0 1943:+0.0 1944:+0.0 1945:+0.0 1946:+0.0 1947:+0.0 1948:+0.0 1949:+0.0 1950:+0.0 1951:+0.0 1952:+0.0 1953:+0.0 1954:+0.0 1955:+0.0 1956:+0.0 1957:+0.0 1958:+0.0 1959:+0.0 1960:+0.0 1961:+0.0 1962:+0.0 1963:+0.0 1964:+0.0 1965:+0.0 1966:+0.0 1967:+0.0 1968:+0.0 1969:+0.0 1970:+0.0 1971:+0.0 1972:+15.4 1973:-11.1 1974:-6.4 1975:-8.1 1976:+1.8 1977:-6.5 1978:-1.2 1979:-0.3 1980:-2.0 1981:-0.9 1982:-2.2 1983:+10.7 1984:+1.2 1985:-0.4 1986:+4.9 1987:-2.7 1988:+3.9 1989:+4.8 1990:-13.2 1991:-4.9 1992:+2.6 1993:-8.2 1994:-4.0 1995:+2.0 1996:+0.2 1997:+13.4 1998:+11.6 1999:+8.6 2000:-3.3 2001:+9.2 2002:+10.4 2003:+0.9 2004:-1.2 2005:+1.2 2006:-1.1 2007:+1.5 2008:-6.2 2009:-7.0 2010:+1.1 2011:-1.6 2012:-6.6 2013:+15.5 2014:+1.0 2015:+3.0 2016:-13.1 2017:+1.7 2018:-0.4 2019:-2.0 2020:-1.4 2021:+2.4 2022:-7.2 2023:-4.8 2024:+0.3
- kosten: bruto +1166.8% | spread/commissie 7.6% | financiering +1079.6% (som over instrument-dagen) → kostenpoort FAALT
- 5-jaarsvensters positief: 21% (4/19)
- beslissing: stop: kostenpoort (geen trial) (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
