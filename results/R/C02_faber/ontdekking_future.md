# C02_faber — Faber SMA-10-maanden long/cash op indices (trend)
Mechanisme: Trend + drawdown-beperking: vermijd lange bear-markten.
Bron: Faber (2007)

## variant basis {} — vehikel future
- ontdekking ≤ 2024: 24868 dagen, 427 positie-wijzigingen, netto +2.19 bp/dag, SR +0.47 (90%-CI +0.29…+0.65)
- t: dag +4.68 | Newey-West +4.65 | blok-bootstrap +4.62 | H1 +2.93 | H2 +3.87 | +50% spread (NW) +4.64
- skew -0.58 | max dagverlies 12.95% (P99 2.14%) | maxDD 50.9% (1× notional)
- corr: ORB -0.01, RSI2 +0.53 | SPX > SMA200: +5.77 bp/dag, daaronder -5.70
- per instrument t: SPX +6.20, NDX +4.45, DJI +3.67, DAX +3.90, N225 +4.64
- per jaar (%): 1927:+0.0 1928:+14.1 1929:+2.6 1930:+0.0 1931:+0.0 1932:-20.3 1933:+11.0 1934:-2.8 1935:+38.5 1936:+25.2 1937:-4.3 1938:+14.7 1939:-20.1 1940:-7.0 1941:-9.2 1942:+12.9 1943:+11.6 1944:+8.9 1945:+26.2 1946:-4.2 1947:-3.9 1948:-15.3 1949:+10.7 1950:+19.4 1951:+14.4 1952:+7.9 1953:-5.0 1954:+36.7 1955:+22.9 1956:-1.6 1957:-5.4 1958:+23.0 1959:+3.4 1960:-12.4 1961:+19.0 1962:-8.9 1963:+14.5 1964:+8.8 1965:+6.7 1966:-6.3 1967:-4.1 1968:+8.3 1969:+10.0 1970:-0.9 1971:+6.6 1972:+38.2 1973:-11.2 1974:-1.6 1975:-0.7 1976:+4.0 1977:-11.3 1978:+0.7 1979:-4.9 1980:-0.9 1981:-9.1 1982:+9.8 1983:+11.4 1984:+0.0 1985:+7.5 1986:+12.3 1987:-0.4 1988:+2.7 1989:+21.3 1990:-18.5 1991:+3.7 1992:-0.6 1993:+5.4 1994:-9.8 1995:+17.2 1996:+15.4 1997:+18.4 1998:+9.8 1999:+29.6 2000:-12.0 2001:-0.8 2002:-5.3 2003:+27.7 2004:+2.3 2005:+7.8 2006:+7.6 2007:+9.6 2008:-9.8 2009:+15.1 2010:+3.0 2011:-4.3 2012:+6.5 2013:+34.2 2014:+7.5 2015:+1.0 2016:+5.6 2017:+19.2 2018:-2.8 2019:+5.6 2020:+8.3 2021:+16.6 2022:-12.0 2023:+14.0 2024:+15.2
- kosten: bruto +1467.6% | spread/commissie 2.1% | financiering -911.0% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 89% (17/19)
- G-benchmark (vehikel future): regel SR +0.47, CAGR +8.5%, maxDD 50.9%, Calmar 0.17 | buy-and-hold (gelijk gewogen) SR +0.33, CAGR +8.0%, maxDD 86.2%, Calmar 0.09 → BETER (SR én maxDD)
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
