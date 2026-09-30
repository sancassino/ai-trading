# C51_volmanaged — Vol-managed index: gewicht = min(1; 10%/σ21), maandelijks (volatiliteit/sizing)
Mechanisme: Risico/rendement is niet evenredig: bij hoge vol daalt het rendement per risico-eenheid, dus vol-schalen verbetert SR en DD.
Bron: Moreira & Muir (2017); Harvey e.a. (2018)

## variant basis {} — vehikel future
- ontdekking ≤ 2024: 24594 dagen, 1827 positie-wijzigingen, netto +1.32 bp/dag, SR +0.32 (90%-CI +0.14…+0.51)
- t: dag +3.17 | Newey-West +3.01 | blok-bootstrap +2.89 | H1 +1.16 | H2 +3.41 | +50% spread (NW) +3.00
- skew -0.64 | max dagverlies 10.05% (P99 1.79%) | maxDD 54.2% (1× notional)
- corr: ORB -0.02, RSI2 +0.53 | SPX > SMA200: +5.42 bp/dag, daaronder -7.81
- per instrument t: SPX +5.79, NDX +5.79, DAX +3.78
- per jaar (%): 1927:+0.0 1928:+28.6 1929:+2.6 1930:-11.1 1931:-23.4 1932:-1.9 1933:+2.0 1934:-2.3 1935:+15.3 1936:+12.9 1937:-17.4 1938:+7.9 1939:-5.4 1940:-20.9 1941:-17.7 1942:+9.8 1943:+12.9 1944:+11.9 1945:+18.3 1946:-9.6 1947:-1.2 1948:-9.0 1949:+7.6 1950:+14.5 1951:+9.8 1952:+9.6 1953:-7.7 1954:+34.6 1955:+17.8 1956:-2.0 1957:-12.4 1958:+28.8 1959:+5.6 1960:-6.0 1961:+17.1 1962:-16.9 1963:+13.4 1964:+8.8 1965:+4.6 1966:-17.3 1967:+13.8 1968:+0.4 1969:-19.7 1970:-3.6 1971:+4.1 1972:+10.7 1973:-20.2 1974:-23.2 1975:+9.3 1976:+9.9 1977:-16.7 1978:-5.5 1979:+1.1 1980:+9.9 1981:-18.6 1982:+2.4 1983:+5.1 1984:-5.7 1985:+13.5 1986:+1.2 1987:+11.8 1988:+4.8 1989:+15.1 1990:-12.4 1991:+15.7 1992:+1.8 1993:+12.4 1994:-5.1 1995:+15.2 1996:+15.0 1997:+16.5 1998:+13.0 1999:+18.6 2000:-7.3 2001:-16.1 2002:-13.0 2003:+14.9 2004:+6.6 2005:+5.1 2006:+8.7 2007:+8.8 2008:-20.7 2009:+12.3 2010:+11.0 2011:-3.4 2012:+16.3 2013:+23.7 2014:+6.4 2015:+3.1 2016:+6.5 2017:+17.9 2018:-7.2 2019:+14.0 2020:+4.9 2021:+14.6 2022:-10.7 2023:+12.7 2024:+12.4
- kosten: bruto +738.6% | spread/commissie 1.5% | financiering -561.4% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 68% (13/19)
- G-benchmark (vehikel future): regel SR +0.32, CAGR +6.4%, maxDD 54.2%, Calmar 0.12 | buy-and-hold (gelijk gewogen) SR +0.29, CAGR +7.4%, maxDD 86.2%, Calmar 0.09 → BETER (SR én maxDD)
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
