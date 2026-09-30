# C05_tsmom_mix — TSMOM-mix 1/3/12m (vol-geschaald) (trend)
Mechanisme: Als C01, diversificatie over horizons.
Bron: Hurst, Ooi, Pedersen (2017)

## variant basis {} — vehikel cfd_retail_hi
- ontdekking ≤ 2024: 24868 dagen, 6022 positie-wijzigingen, netto +0.41 bp/dag, SR +0.16 (90%-CI -0.00…+0.32)
- t: dag +1.60 | Newey-West +1.58 | blok-bootstrap +1.58 | H1 +1.32 | H2 +0.94 | +50% spread (NW) +1.54
- skew +0.12 | max dagverlies 6.17% (P99 1.20%) | maxDD 35.2% (1× notional)
- corr: ORB -0.01, RSI2 +0.23 | SPX > SMA200: +0.88 bp/dag, daaronder -0.74
- per instrument t: FX_EURUSD +1.61, FX_GBPUSD +4.25, FX_USDJPY +0.75, FX_AUDUSD +3.56, FX_USDCAD +2.34, FX_USDCHF -0.02, GOLD_F +2.45, SILVER_F +0.29, SPX +5.31, NDX +3.53, DAX +2.87, N225 +4.76
- per jaar (%): 1927:+0.0 1928:+0.0 1929:-2.5 1930:+4.4 1931:-5.1 1932:+10.2 1933:-3.6 1934:-1.0 1935:+7.6 1936:+5.0 1937:+5.5 1938:-13.0 1939:-18.9 1940:-12.3 1941:+10.8 1942:+5.2 1943:+11.8 1944:+4.3 1945:+9.3 1946:+3.4 1947:-3.2 1948:-16.0 1949:+4.6 1950:+6.9 1951:-2.7 1952:-0.1 1953:-4.4 1954:+25.9 1955:+5.1 1956:-8.8 1957:+0.8 1958:+13.2 1959:+0.9 1960:-20.8 1961:+9.1 1962:+10.1 1963:-3.2 1964:+6.4 1965:+0.3 1966:-0.7 1967:-7.4 1968:+3.8 1969:+4.8 1970:+0.4 1971:-2.7 1972:+12.6 1973:-2.5 1974:+5.9 1975:+7.2 1976:+8.6 1977:+1.1 1978:+4.2 1979:-6.3 1980:-8.0 1981:-6.9 1982:+8.4 1983:+6.0 1984:+0.6 1985:+7.2 1986:+1.5 1987:+8.0 1988:+2.4 1989:+4.9 1990:-2.1 1991:-4.1 1992:+0.5 1993:-2.2 1994:-3.2 1995:+0.2 1996:+3.9 1997:+2.3 1998:+1.7 1999:+1.8 2000:-2.0 2001:+2.2 2002:+4.4 2003:+7.8 2004:+2.7 2005:-1.4 2006:+1.0 2007:+2.1 2008:+2.1 2009:+0.0 2010:-0.4 2011:-1.5 2012:-2.0 2013:+8.7 2014:-0.3 2015:-2.5 2016:-4.7 2017:+0.6 2018:+2.1 2019:-6.3 2020:+0.9 2021:-2.7 2022:-2.4 2023:-3.5 2024:-0.1
- kosten: bruto +1158.8% | spread/commissie 34.0% | financiering -890.5% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 58% (11/19)
- G-benchmark (vehikel cfd_retail_hi): regel SR +0.16, CAGR +4.3%, maxDD 35.2%, Calmar 0.12 | buy-and-hold (gelijk gewogen) SR +0.16, CAGR +4.8%, maxDD 87.1%, Calmar 0.06 → niet beter
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
