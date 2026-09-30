# C05_tsmom_mix — TSMOM-mix 1/3/12m (vol-geschaald) (trend)
Mechanisme: Als C01, diversificatie over horizons.
Bron: Hurst, Ooi, Pedersen (2017)

## variant basis {} — vehikel cfd_retail
- ontdekking ≤ 2024: 24868 dagen, 6022 positie-wijzigingen, netto +0.68 bp/dag, SR +0.27 (90%-CI +0.10…+0.43)
- t: dag +2.66 | Newey-West +2.63 | blok-bootstrap +2.61 | H1 +1.85 | H2 +2.20 | +50% spread (NW) +2.60
- skew +0.13 | max dagverlies 6.16% (P99 1.19%) | maxDD 34.7% (1× notional)
- corr: ORB -0.01, RSI2 +0.23 | SPX > SMA200: +1.17 bp/dag, daaronder -0.52
- per instrument t: FX_EURUSD +2.16, FX_GBPUSD +5.00, FX_USDJPY +1.23, FX_AUDUSD +4.14, FX_USDCAD +3.61, FX_USDCHF +0.47, GOLD_F +2.72, SILVER_F +0.48, SPX +5.98, NDX +3.81, DAX +3.18, N225 +5.20
- per jaar (%): 1927:+0.0 1928:+0.0 1929:-2.2 1930:+4.6 1931:-4.9 1932:+10.4 1933:-3.4 1934:-0.8 1935:+7.9 1936:+5.5 1937:+5.8 1938:-12.8 1939:-18.7 1940:-12.0 1941:+11.3 1942:+5.6 1943:+12.4 1944:+5.0 1945:+10.0 1946:+3.8 1947:-2.9 1948:-15.4 1949:+5.0 1950:+7.6 1951:-2.2 1952:+0.8 1953:-3.8 1954:+26.8 1955:+5.7 1956:-8.3 1957:+1.5 1958:+13.9 1959:+1.6 1960:-20.2 1961:+10.0 1962:+10.5 1963:-2.4 1964:+8.1 1965:+1.0 1966:-0.0 1967:-6.7 1968:+4.5 1969:+5.4 1970:+0.9 1971:-2.4 1972:+14.0 1973:-1.4 1974:+6.9 1975:+8.6 1976:+10.0 1977:+2.2 1978:+5.5 1979:-4.9 1980:-6.6 1981:-5.8 1982:+9.6 1983:+7.0 1984:+1.7 1985:+8.0 1986:+2.3 1987:+8.8 1988:+3.1 1989:+5.7 1990:-1.4 1991:-3.4 1992:+1.3 1993:-1.5 1994:-2.4 1995:+1.0 1996:+4.9 1997:+3.1 1998:+2.4 1999:+2.3 2000:-1.4 2001:+2.7 2002:+5.1 2003:+8.5 2004:+3.3 2005:-0.7 2006:+1.7 2007:+3.0 2008:+2.5 2009:+0.4 2010:+0.1 2011:-1.0 2012:-1.4 2013:+9.5 2014:+0.6 2015:-1.9 2016:-4.1 2017:+1.4 2018:+3.0 2019:-5.4 2020:+1.6 2021:-1.9 2022:-1.8 2023:-2.8 2024:+0.7
- kosten: bruto +1158.8% | spread/commissie 17.0% | financiering -1240.2% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 74% (14/19)
- G-benchmark (vehikel cfd_retail): regel SR +0.27, CAGR +5.0%, maxDD 34.7%, Calmar 0.14 | buy-and-hold (gelijk gewogen) SR +0.23, CAGR +5.9%, maxDD 86.7%, Calmar 0.07 → BETER (SR én maxDD)
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
