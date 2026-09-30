# C51_volmanaged — Vol-managed index: gewicht = min(1; 10%/σ21), maandelijks (volatiliteit/sizing)
Mechanisme: Risico/rendement is niet evenredig: bij hoge vol daalt het rendement per risico-eenheid, dus vol-schalen verbetert SR en DD.
Bron: Moreira & Muir (2017); Harvey e.a. (2018)

## variant basis {} — vehikel cfd
- ontdekking ≤ 2024: 24594 dagen, 1827 positie-wijzigingen, netto +0.79 bp/dag, SR +0.19 (90%-CI +0.01…+0.38)
- t: dag +1.91 | Newey-West +1.82 | blok-bootstrap +1.75 | H1 +0.10 | H2 +2.70 | +50% spread (NW) +1.81
- skew -0.64 | max dagverlies 10.05% (P99 1.80%) | maxDD 68.4% (1× notional)
- corr: ORB -0.02, RSI2 +0.53 | SPX > SMA200: +4.79 bp/dag, daaronder -8.07
- per instrument t: SPX +1.72, NDX +2.87, DAX +1.08
- per jaar (%): 1927:+0.0 1928:+26.0 1929:+0.8 1930:-12.7 1931:-24.5 1932:-2.6 1933:+1.1 1934:-3.8 1935:+13.5 1936:+10.9 1937:-19.2 1938:+6.8 1939:-7.1 1940:-23.3 1941:-20.5 1942:+7.2 1943:+9.9 1944:+8.4 1945:+15.2 1946:-11.8 1947:-3.8 1948:-11.7 1949:+4.5 1950:+11.5 1951:+6.7 1952:+6.0 1953:-11.1 1954:+30.7 1955:+15.5 1956:-4.0 1957:-13.8 1958:+25.8 1959:+4.1 1960:-7.9 1961:+14.7 1962:-18.7 1963:+11.7 1964:+7.4 1965:+3.6 1966:-17.4 1967:+13.2 1968:+0.8 1969:-18.0 1970:-2.5 1971:+3.5 1972:+9.8 1973:-18.7 1974:-21.7 1975:+9.9 1976:+9.9 1977:-16.4 1978:-3.6 1979:+5.6 1980:+14.3 1981:-11.7 1982:+6.4 1983:+7.9 1984:-1.8 1985:+15.7 1986:+1.2 1987:+11.6 1988:+5.0 1989:+16.4 1990:-11.8 1991:+15.0 1992:-0.4 1993:+9.8 1994:-6.7 1995:+14.5 1996:+14.0 1997:+15.9 1998:+12.3 1999:+17.8 2000:-7.5 2001:-17.2 2002:-14.6 2003:+12.5 2004:+3.2 2005:+2.4 2006:+7.4 2007:+7.4 2008:-22.6 2009:+9.8 2010:+7.1 2011:-7.1 2012:+12.0 2013:+18.5 2014:+1.4 2015:-0.8 2016:+2.4 2017:+12.8 2018:-10.4 2019:+10.8 2020:+2.2 2021:+9.9 2022:-12.5 2023:+11.7 2024:+11.4
- kosten: bruto +1136.0% | spread/commissie 1.1% | financiering +668.5% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 63% (12/19)
- G-benchmark (vehikel cfd): regel SR +0.19, CAGR +1.5%, maxDD 68.4%, Calmar 0.02 | buy-and-hold (gelijk gewogen) SR +0.18, CAGR +1.7%, maxDD 88.0%, Calmar 0.02 → BETER (SR én maxDD)
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
