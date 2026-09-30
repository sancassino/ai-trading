# C02_faber — Faber SMA-10-maanden long/cash op indices (trend)
Mechanisme: Trend + drawdown-beperking: vermijd lange bear-markten.
Bron: Faber (2007)

## variant basis {} — vehikel cfd_retail
- ontdekking ≤ 2024: 24868 dagen, 427 positie-wijzigingen, netto +1.85 bp/dag, SR +0.40 (90%-CI +0.22…+0.58)
- t: dag +3.95 | Newey-West +3.93 | blok-bootstrap +3.91 | H1 +2.44 | H2 +3.31 | +50% spread (NW) +3.92
- skew -0.59 | max dagverlies 12.96% (P99 2.15%) | maxDD 51.2% (1× notional)
- corr: ORB -0.01, RSI2 +0.53 | SPX > SMA200: +5.32 bp/dag, daaronder -5.81
- per instrument t: SPX +5.91, NDX +4.10, DJI +3.13, DAX +3.48, N225 +4.10
- per jaar (%): 1927:+0.0 1928:+13.7 1929:+1.3 1930:+0.0 1931:+0.0 1932:-20.6 1933:+9.8 1934:-3.4 1935:+37.5 1936:+23.7 1937:-4.8 1938:+13.9 1939:-20.8 1940:-7.6 1941:-9.5 1942:+12.2 1943:+10.3 1944:+7.7 1945:+24.8 1946:-5.2 1947:-4.3 1948:-16.2 1949:+10.0 1950:+17.9 1951:+12.9 1952:+6.5 1953:-5.5 1954:+35.2 1955:+21.4 1956:-2.7 1957:-5.8 1958:+22.0 1959:+2.1 1960:-12.9 1961:+17.5 1962:-9.5 1963:+13.0 1964:+7.3 1965:+5.9 1966:-7.1 1967:-5.1 1968:+7.1 1969:+8.9 1970:-1.3 1971:+5.4 1972:+36.6 1973:-11.7 1974:-1.8 1975:-1.9 1976:+2.6 1977:-12.0 1978:-0.4 1979:-6.2 1980:-2.4 1981:-10.1 1982:+9.3 1983:+9.9 1984:-1.0 1985:+6.1 1986:+11.2 1987:-1.6 1988:+2.4 1989:+20.6 1990:-18.8 1991:+3.4 1992:-0.7 1993:+4.7 1994:-10.5 1995:+16.5 1996:+14.3 1997:+17.5 1998:+9.1 1999:+28.5 2000:-12.7 2001:-0.9 2002:-5.5 2003:+27.0 2004:+1.4 2005:+6.8 2006:+6.6 2007:+8.5 2008:-9.9 2009:+14.5 2010:+2.1 2011:-5.0 2012:+5.8 2013:+33.1 2014:+6.5 2015:+0.2 2016:+5.0 2017:+18.0 2018:-3.6 2019:+4.8 2020:+7.5 2021:+15.5 2022:-12.3 2023:+12.9 2024:+14.0
- kosten: bruto +1526.6% | spread/commissie 2.0% | financiering -645.2% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 89% (17/19)
- G-benchmark (vehikel cfd_retail): regel SR +0.40, CAGR +7.6%, maxDD 51.2%, Calmar 0.15 | buy-and-hold (gelijk gewogen) SR +0.26, CAGR +6.5%, maxDD 86.7%, Calmar 0.08 → BETER (SR én maxDD)
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
