# C02_faber — Faber SMA-10-maanden long/cash op indices (trend)
Mechanisme: Trend + drawdown-beperking: vermijd lange bear-markten.
Bron: Faber (2007)

## variant basis {} — vehikel cfd
- ontdekking ≤ 2024: 24868 dagen, 427 positie-wijzigingen, netto +1.48 bp/dag, SR +0.32 (90%-CI +0.14…+0.49)
- t: dag +3.16 | Newey-West +3.15 | blok-bootstrap +3.14 | H1 +2.01 | H2 +2.59 | +50% spread (NW) +3.14
- skew -0.61 | max dagverlies 12.98% (P99 2.16%) | maxDD 54.0% (1× notional)
- corr: ORB -0.01, RSI2 +0.53 | SPX > SMA200: +4.81 bp/dag, daaronder -5.88
- per instrument t: SPX +2.75, NDX +2.48, DJI +0.35, DAX +1.70, N225 +1.10
- per jaar (%): 1927:+0.0 1928:+13.2 1929:-0.5 1930:+0.0 1931:+0.0 1932:-21.2 1933:+8.0 1934:-4.3 1935:+36.1 1936:+21.5 1937:-5.5 1938:+12.8 1939:-21.9 1940:-8.5 1941:-10.1 1942:+11.4 1943:+8.3 1944:+5.9 1945:+22.6 1946:-6.6 1947:-5.0 1948:-17.4 1949:+9.1 1950:+15.8 1951:+10.7 1952:+4.5 1953:-6.2 1954:+32.7 1955:+19.7 1956:-3.5 1957:-5.9 1958:+20.9 1959:+2.0 1960:-13.1 1961:+16.4 1962:-9.8 1963:+12.7 1964:+7.4 1965:+5.8 1966:-7.6 1967:-5.1 1968:+7.2 1969:+9.5 1970:-1.1 1971:+5.0 1972:+35.8 1973:-11.8 1974:-2.0 1975:-1.3 1976:+2.8 1977:-12.5 1978:+1.0 1979:-1.9 1980:+3.6 1981:-4.2 1982:+10.3 1983:+13.6 1984:+1.6 1985:+8.4 1986:+11.8 1987:-1.1 1988:+2.6 1989:+22.6 1990:-18.4 1991:+2.7 1992:-2.0 1993:+2.0 1994:-11.8 1995:+15.8 1996:+13.3 1997:+16.7 1998:+8.4 1999:+27.3 2000:-12.8 2001:-1.2 2002:-6.2 2003:+23.7 2004:-1.9 2005:+4.4 2006:+5.4 2007:+7.0 2008:-10.1 2009:+11.5 2010:-2.4 2011:-8.7 2012:+1.3 2013:+27.2 2014:+1.1 2015:-4.4 2016:+1.8 2017:+12.9 2018:-6.9 2019:+1.9 2020:+3.6 2021:+10.0 2022:-13.5 2023:+12.1 2024:+13.1
- kosten: bruto +2090.8% | spread/commissie 2.0% | financiering +1158.9% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 84% (16/19)
- G-benchmark (vehikel cfd): regel SR +0.32, CAGR +3.1%, maxDD 54.0%, Calmar 0.06 | buy-and-hold (gelijk gewogen) SR +0.18, CAGR +1.6%, maxDD 88.0%, Calmar 0.02 → BETER (SR én maxDD)
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
