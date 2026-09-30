# C33_trend_lowvol — TSMOM-mix alleen in laag-vol-regime (σ60 < eigen mediane σ60 tot t) (trend/regime)
Mechanisme: Trends zijn betrouwbaarder in rustige regimes; hoge vol = reversals/crashes.
Bron: catalogus C33; Moreira–Muir-idee toegepast als regime-filter

## variant basis {} — vehikel future
- ontdekking ≤ 2024: 24868 dagen, 2975 positie-wijzigingen, netto +0.79 bp/dag, SR +0.37 (90%-CI +0.21…+0.55)
- t: dag +3.72 | Newey-West +3.64 | blok-bootstrap +3.76 | H1 +2.63 | H2 +3.65 | +50% spread (NW) +3.62
- skew -0.43 | max dagverlies 6.14% (P99 1.02%) | maxDD 23.8% (1× notional)
- corr: ORB +0.01, RSI2 +0.26 | SPX > SMA200: +1.24 bp/dag, daaronder -0.27
- per instrument t: FX_EURUSD +3.12, FX_GBPUSD +7.16, FX_USDJPY +1.62, FX_AUDUSD +8.58, FX_USDCAD +11.06, FX_USDCHF +1.56, GOLD_F +3.24, SILVER_F +1.05, SPX +7.44, NDX +4.73, DAX +4.41, N225 +7.31
- per jaar (%): 1927:+0.0 1928:+0.0 1929:-3.1 1930:+0.5 1931:+0.0 1932:+0.0 1933:+0.0 1934:-3.3 1935:+5.6 1936:+6.1 1937:-0.6 1938:+0.0 1939:-15.8 1940:-8.5 1941:+11.9 1942:+6.1 1943:+13.3 1944:+6.0 1945:+11.1 1946:+1.9 1947:-2.8 1948:-13.0 1949:+5.6 1950:+7.3 1951:-1.3 1952:+2.2 1953:-3.0 1954:+28.3 1955:+9.6 1956:-7.7 1957:+2.6 1958:+17.0 1959:+2.8 1960:-19.3 1961:+12.0 1962:+12.5 1963:-2.3 1964:+10.5 1965:+2.0 1966:+1.7 1967:-5.2 1968:+6.6 1969:+7.8 1970:+8.1 1971:-3.8 1972:+13.3 1973:+0.3 1974:+3.2 1975:+2.1 1976:+3.9 1977:+0.8 1978:+2.5 1979:-1.1 1980:-5.2 1981:-1.5 1982:-1.5 1983:+2.8 1984:+1.1 1985:+5.4 1986:+3.6 1987:+4.3 1988:+1.4 1989:+8.2 1990:-0.8 1991:-0.1 1992:+2.7 1993:+2.3 1994:-2.7 1995:+3.7 1996:+6.4 1997:+0.3 1998:-0.1 1999:+0.2 2000:+1.1 2001:+0.0 2002:+4.3 2003:+3.2 2004:+3.3 2005:+0.8 2006:+1.8 2007:+3.9 2008:-2.0 2009:+0.9 2010:+2.6 2011:+1.3 2012:-0.3 2013:+7.3 2014:+0.2 2015:-0.8 2016:-1.3 2017:+4.4 2018:+3.2 2019:-4.2 2020:+2.0 2021:-1.7 2022:+0.4 2023:-0.4 2024:+1.3
- kosten: bruto +685.0% | spread/commissie 10.3% | financiering -1761.3% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 79% (15/19)
- G-benchmark (vehikel future): regel SR +0.37, CAGR +5.4%, maxDD 23.8%, Calmar 0.22 | buy-and-hold (gelijk gewogen) SR +0.33, CAGR +7.5%, maxDD 86.2%, Calmar 0.09 → BETER (SR én maxDD)
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
