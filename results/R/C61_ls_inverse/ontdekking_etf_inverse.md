# C61_ls_inverse — SPX Faber long / −1× inverse (dagelijks gereset, TER 0,50%) onder de 10-mnd-SMA (trend (long/short))
Mechanisme: Long in uptrend; in downtrend inverse-ETF → verdient in bearmarkten, lagere correlatie in drawdowns dan C02.
Bron: Faber (2007) + UCITS-inverse (Xtrackers S&P 500 Inverse Daily Swap, TER 0,50% = web-claim)

## variant basis {} — vehikel etf_inverse
- ontdekking ≤ 2024: 24366 dagen, 143 positie-wijzigingen, netto +1.61 bp/dag, SR +0.21 (90%-CI +0.05…+0.39)
- t: dag +2.11 | Newey-West +2.14 | blok-bootstrap +2.17 | H1 +1.92 | H2 +1.00 | +50% spread (NW) +2.09
- skew -0.58 | max dagverlies 20.52% (P99 3.48%) | maxDD 80.7% (1× notional)
- corr: ORB -0.07, RSI2 +0.39 | SPX > SMA200: +3.52 bp/dag, daaronder -2.39
- per instrument t: SPX +3.90
- per jaar (%): 1928:+14.1 1929:+11.7 1930:+29.1 1931:+54.5 1932:-39.1 1933:-25.0 1934:-4.0 1935:+38.9 1936:+25.1 1937:+35.7 1938:+1.8 1939:-37.9 1940:-0.2 1941:-0.0 1942:+13.2 1943:+5.6 1944:+5.2 1945:+26.2 1946:+2.2 1947:-9.2 1948:-31.2 1949:+10.8 1950:+19.3 1951:+14.3 1952:+5.2 1953:-3.8 1954:+36.6 1955:+22.8 1956:-5.0 1957:+3.9 1958:+14.3 1959:+0.5 1960:-22.4 1961:+18.9 1962:-6.0 1963:+14.4 1964:+8.7 1965:-2.0 1966:-6.8 1967:-0.6 1968:-8.2 1969:-14.2 1970:+14.9 1971:-9.6 1972:+10.7 1973:+5.4 1974:+32.4 1975:-12.4 1976:+2.9 1977:+0.5 1978:-13.1 1979:-23.4 1980:-3.4 1981:-4.4 1982:+15.6 1983:+8.2 1984:-7.3 1985:+8.3 1986:-2.0 1987:-19.9 1988:-13.3 1989:+20.2 1990:-35.2 1991:-8.1 1992:+4.3 1993:+6.9 1994:-19.8 1995:+26.7 1996:+16.3 1997:+25.3 1998:-6.8 1999:+3.3 2000:+3.2 2001:+9.9 2002:+8.4 2003:+14.6 2004:+3.2 2005:+2.1 2006:+10.4 2007:+3.4 2008:+37.3 2009:+14.5 2010:-6.2 2011:-5.8 2012:+6.5 2013:+28.6 2014:+13.4 2015:-9.8 2016:+8.1 2017:+19.0 2018:-9.6 2019:-9.7 2020:+5.8 2021:+26.0 2022:-29.8 2023:-10.6 2024:+18.1
- kosten: bruto +649.2% | spread/commissie 18.5% | financiering -94.3% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 68% (13/19)
- G-benchmark (vehikel etf_inverse): regel SR +0.21, CAGR +5.9%, maxDD 80.7%, Calmar 0.07 | buy-and-hold (gelijk gewogen) SR +0.27, CAGR +7.0%, maxDD 86.2%, Calmar 0.08 → niet beter
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
