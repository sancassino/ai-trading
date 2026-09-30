# C05_tsmom_mix — TSMOM-mix 1/3/12m (vol-geschaald) (trend)
Mechanisme: Als C01, diversificatie over horizons.
Bron: Hurst, Ooi, Pedersen (2017)

## variant basis {} — vehikel future
- ontdekking ≤ 2024: 24868 dagen, 6022 positie-wijzigingen, netto +1.05 bp/dag, SR +0.41 (90%-CI +0.25…+0.57)
- t: dag +4.10 | Newey-West +4.05 | blok-bootstrap +4.02 | H1 +2.60 | H2 +3.86 | +50% spread (NW) +4.02
- skew +0.15 | max dagverlies 6.14% (P99 1.18%) | maxDD 34.1% (1× notional)
- corr: ORB -0.01, RSI2 +0.24 | SPX > SMA200: +1.57 bp/dag, daaronder -0.21
- per instrument t: FX_EURUSD +2.94, FX_GBPUSD +6.06, FX_USDJPY +1.91, FX_AUDUSD +4.95, FX_USDCAD +5.40, FX_USDCHF +1.16, GOLD_F +3.10, SILVER_F +0.73, SPX +6.54, NDX +4.22, DAX +3.60, N225 +5.81
- per jaar (%): 1927:+0.0 1928:+0.0 1929:-1.6 1930:+4.9 1931:-4.6 1932:+10.6 1933:-3.2 1934:-0.5 1935:+8.4 1936:+6.1 1937:+6.4 1938:-12.6 1939:-18.4 1940:-11.6 1941:+11.9 1942:+6.1 1943:+13.3 1944:+6.0 1945:+11.1 1946:+4.4 1947:-2.4 1948:-14.5 1949:+5.6 1950:+8.7 1951:-1.3 1952:+2.2 1953:-3.0 1954:+28.3 1955:+6.6 1956:-7.7 1957:+2.6 1958:+15.0 1959:+2.8 1960:-19.3 1961:+11.3 1962:+11.2 1963:-1.2 1964:+10.5 1965:+2.0 1966:+0.8 1967:-5.6 1968:+5.7 1969:+6.3 1970:+1.5 1971:-2.0 1972:+16.1 1973:+0.1 1974:+8.3 1975:+10.7 1976:+11.9 1977:+3.8 1978:+7.5 1979:-2.9 1980:-4.6 1981:-4.4 1982:+11.3 1983:+8.4 1984:+3.3 1985:+9.2 1986:+3.3 1987:+10.0 1988:+4.0 1989:+6.5 1990:-0.4 1991:-2.7 1992:+2.1 1993:-0.7 1994:-1.5 1995:+1.8 1996:+6.0 1997:+4.0 1998:+3.2 1999:+2.9 2000:-0.6 2001:+3.3 2002:+6.0 2003:+9.4 2004:+4.0 2005:+0.2 2006:+2.5 2007:+4.2 2008:+3.2 2009:+0.8 2010:+0.7 2011:-0.2 2012:-0.7 2013:+10.4 2014:+1.8 2015:-1.1 2016:-3.4 2017:+2.4 2018:+4.0 2019:-4.2 2020:+2.6 2021:-0.8 2022:-0.9 2023:-2.0 2024:+1.9
- kosten: bruto +1126.9% | spread/commissie 17.2% | financiering -1757.9% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 79% (15/19)
- G-benchmark (vehikel future): regel SR +0.41, CAGR +6.0%, maxDD 34.1%, Calmar 0.18 | buy-and-hold (gelijk gewogen) SR +0.33, CAGR +7.4%, maxDD 86.2%, Calmar 0.09 → BETER (SR én maxDD)
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
