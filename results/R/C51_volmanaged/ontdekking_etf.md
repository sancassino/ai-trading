# C51_volmanaged — Vol-managed index: gewicht = min(1; 10%/σ21), maandelijks (volatiliteit/sizing)
Mechanisme: Risico/rendement is niet evenredig: bij hoge vol daalt het rendement per risico-eenheid, dus vol-schalen verbetert SR en DD.
Bron: Moreira & Muir (2017); Harvey e.a. (2018)

## variant basis {} — vehikel etf
- ontdekking ≤ 2024: 24594 dagen, 1827 positie-wijzigingen, netto +1.29 bp/dag, SR +0.31 (90%-CI +0.13…+0.50)
- t: dag +3.10 | Newey-West +2.94 | blok-bootstrap +2.83 | H1 +1.11 | H2 +3.36 | +50% spread (NW) +2.93
- skew -0.64 | max dagverlies 10.05% (P99 1.79%) | maxDD 54.5% (1× notional)
- corr: ORB -0.02, RSI2 +0.53 | SPX > SMA200: +5.39 bp/dag, daaronder -7.83
- per instrument t: SPX +5.72, NDX +5.75, DAX +3.75
- per jaar (%): 1927:+0.0 1928:+28.5 1929:+2.5 1930:-11.1 1931:-23.5 1932:-1.9 1933:+1.9 1934:-2.4 1935:+15.2 1936:+12.8 1937:-17.5 1938:+7.8 1939:-5.4 1940:-20.9 1941:-17.7 1942:+9.7 1943:+12.8 1944:+11.9 1945:+18.2 1946:-9.7 1947:-1.2 1948:-9.1 1949:+7.5 1950:+14.4 1951:+9.7 1952:+9.5 1953:-7.8 1954:+34.5 1955:+17.8 1956:-2.1 1957:-12.5 1958:+28.7 1959:+5.5 1960:-6.1 1961:+17.0 1962:-17.0 1963:+13.4 1964:+8.7 1965:+4.5 1966:-17.4 1967:+13.8 1968:+0.3 1969:-19.8 1970:-3.7 1971:+4.0 1972:+10.6 1973:-20.3 1974:-23.3 1975:+9.3 1976:+9.8 1977:-16.8 1978:-5.5 1979:+1.1 1980:+9.8 1981:-18.6 1982:+2.3 1983:+5.0 1984:-5.8 1985:+13.4 1986:+1.1 1987:+11.7 1988:+4.7 1989:+15.0 1990:-12.5 1991:+15.6 1992:+1.7 1993:+12.3 1994:-5.2 1995:+15.1 1996:+14.9 1997:+16.5 1998:+12.9 1999:+18.5 2000:-7.3 2001:-16.2 2002:-13.0 2003:+14.8 2004:+6.5 2005:+5.0 2006:+8.6 2007:+8.7 2008:-20.7 2009:+12.3 2010:+11.0 2011:-3.5 2012:+16.2 2013:+23.6 2014:+6.3 2015:+3.0 2016:+6.4 2017:+17.8 2018:-7.3 2019:+13.9 2020:+4.8 2021:+14.5 2022:-10.7 2023:+12.6 2024:+12.4
- kosten: bruto +1136.0% | spread/commissie 4.4% | financiering -154.6% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 68% (13/19)
- G-benchmark (vehikel etf): regel SR +0.31, CAGR +6.3%, maxDD 54.5%, Calmar 0.12 | buy-and-hold (gelijk gewogen) SR +0.29, CAGR +7.3%, maxDD 86.2%, Calmar 0.09 → BETER (SR én maxDD)
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
