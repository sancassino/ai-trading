# C02_faber — Faber SMA-10-maanden long/cash op indices (trend)
Mechanisme: Trend + drawdown-beperking: vermijd lange bear-markten.
Bron: Faber (2007)

## variant basis {} — vehikel etf
- ontdekking ≤ 2024: 24868 dagen, 427 positie-wijzigingen, netto +2.16 bp/dag, SR +0.47 (90%-CI +0.28…+0.65)
- t: dag +4.62 | Newey-West +4.59 | blok-bootstrap +4.56 | H1 +2.90 | H2 +3.82 | +50% spread (NW) +4.58
- skew -0.58 | max dagverlies 12.95% (P99 2.14%) | maxDD 50.9% (1× notional)
- corr: ORB -0.01, RSI2 +0.53 | SPX > SMA200: +5.74 bp/dag, daaronder -5.72
- per instrument t: SPX +6.15, NDX +4.43, DJI +3.63, DAX +3.87, N225 +4.60
- per jaar (%): 1927:+0.0 1928:+14.1 1929:+2.5 1930:+0.0 1931:+0.0 1932:-20.3 1933:+10.9 1934:-2.8 1935:+38.4 1936:+25.1 1937:-4.4 1938:+14.6 1939:-20.1 1940:-7.1 1941:-9.2 1942:+12.8 1943:+11.5 1944:+8.8 1945:+26.2 1946:-4.2 1947:-3.9 1948:-15.4 1949:+10.6 1950:+19.3 1951:+14.3 1952:+7.8 1953:-5.1 1954:+36.6 1955:+22.8 1956:-1.7 1957:-5.5 1958:+22.9 1959:+3.3 1960:-12.5 1961:+18.9 1962:-9.0 1963:+14.4 1964:+8.7 1965:+6.7 1966:-6.4 1967:-4.2 1968:+8.3 1969:+9.9 1970:-0.9 1971:+6.5 1972:+38.1 1973:-11.3 1974:-1.6 1975:-0.8 1976:+3.9 1977:-11.3 1978:+0.6 1979:-5.0 1980:-1.0 1981:-9.2 1982:+9.7 1983:+11.4 1984:-0.0 1985:+7.5 1986:+12.2 1987:-0.5 1988:+2.6 1989:+21.2 1990:-18.5 1991:+3.6 1992:-0.7 1993:+5.3 1994:-9.9 1995:+17.1 1996:+15.3 1997:+18.3 1998:+9.8 1999:+29.5 2000:-12.1 2001:-0.8 2002:-5.3 2003:+27.7 2004:+2.2 2005:+7.7 2006:+7.5 2007:+9.5 2008:-9.8 2009:+15.0 2010:+2.9 2011:-4.3 2012:+6.4 2013:+34.1 2014:+7.4 2015:+0.9 2016:+5.5 2017:+19.1 2018:-2.9 2019:+5.5 2020:+8.2 2021:+16.5 2022:-12.1 2023:+13.9 2024:+15.2
- kosten: bruto +2090.8% | spread/commissie 6.4% | financiering -273.5% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 89% (17/19)
- G-benchmark (vehikel etf): regel SR +0.47, CAGR +8.5%, maxDD 50.9%, Calmar 0.17 | buy-and-hold (gelijk gewogen) SR +0.33, CAGR +7.9%, maxDD 86.2%, Calmar 0.09 → BETER (SR én maxDD)
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
