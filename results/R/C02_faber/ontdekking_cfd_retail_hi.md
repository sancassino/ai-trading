# C02_faber — Faber SMA-10-maanden long/cash op indices (trend)
Mechanisme: Trend + drawdown-beperking: vermijd lange bear-markten.
Bron: Faber (2007)

## variant basis {} — vehikel cfd_retail_hi
- ontdekking ≤ 2024: 24868 dagen, 427 positie-wijzigingen, netto +1.58 bp/dag, SR +0.34 (90%-CI +0.16…+0.52)
- t: dag +3.38 | Newey-West +3.36 | blok-bootstrap +3.35 | H1 +2.10 | H2 +2.81 | +50% spread (NW) +3.35
- skew -0.60 | max dagverlies 12.97% (P99 2.16%) | maxDD 51.5% (1× notional)
- corr: ORB -0.01, RSI2 +0.53 | SPX > SMA200: +4.97 bp/dag, daaronder -5.90
- per instrument t: SPX +5.39, NDX +3.86, DJI +2.76, DAX +3.20, N225 +3.73
- per jaar (%): 1927:+0.0 1928:+13.5 1929:+0.5 1930:+0.0 1931:+0.0 1932:-20.9 1933:+8.9 1934:-3.8 1935:+36.8 1936:+22.7 1937:-5.1 1938:+13.4 1939:-21.3 1940:-8.0 1941:-9.8 1942:+11.8 1943:+9.3 1944:+6.9 1945:+23.8 1946:-5.8 1947:-4.7 1948:-16.8 1949:+9.6 1950:+16.9 1951:+11.9 1952:+5.6 1953:-5.9 1954:+34.2 1955:+20.4 1956:-3.5 1957:-6.1 1958:+21.3 1959:+1.3 1960:-13.2 1961:+16.5 1962:-10.0 1963:+12.0 1964:+6.3 1965:+5.4 1966:-7.6 1967:-5.7 1968:+6.2 1969:+8.2 1970:-1.6 1971:+4.5 1972:+35.6 1973:-12.0 1974:-1.9 1975:-2.7 1976:+1.7 1977:-12.5 1978:-1.1 1979:-7.2 1980:-3.3 1981:-10.7 1982:+9.0 1983:+8.8 1984:-1.7 1985:+5.2 1986:+10.5 1987:-2.4 1988:+1.8 1989:+19.6 1990:-19.2 1991:+2.7 1992:-1.2 1993:+3.8 1994:-11.1 1995:+15.6 1996:+13.3 1997:+16.6 1998:+8.4 1999:+27.5 2000:-13.3 2001:-0.9 2002:-5.6 2003:+26.3 2004:+0.7 2005:+5.9 2006:+5.6 2007:+7.6 2008:-9.9 2009:+13.9 2010:+1.3 2011:-5.7 2012:+5.0 2013:+32.0 2014:+5.5 2015:-0.6 2016:+4.4 2017:+17.0 2018:-4.4 2019:+4.1 2020:+6.7 2021:+14.5 2022:-12.7 2023:+12.0 2024:+13.0
- kosten: bruto +1526.6% | spread/commissie 4.1% | financiering -465.6% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 89% (17/19)
- G-benchmark (vehikel cfd_retail_hi): regel SR +0.34, CAGR +6.9%, maxDD 51.5%, Calmar 0.13 | buy-and-hold (gelijk gewogen) SR +0.20, CAGR +5.5%, maxDD 87.1%, Calmar 0.06 → BETER (SR én maxDD)
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
