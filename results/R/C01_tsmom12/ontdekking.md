# C01_tsmom12 — TSMOM 12m multi-asset (vol-geschaald) (trend)
Mechanisme: Onder-reactie en hedgers die een risicopremie betalen; trends in futures-rendementen.
Bron: Moskowitz, Ooi, Pedersen (2012)

## variant basis {}
- ontdekking ≤ 2024: 24868 dagen, 5941 positie-wijzigingen, netto -0.04 bp/dag, SR -0.01 (90%-CI -0.19…+0.16)
- t: dag -0.12 | Newey-West -0.12 | blok-bootstrap -0.12 | H1 -0.61 | H2 +0.91 | +50% spread (NW) -0.13
- skew -0.66 | max dagverlies 7.63% (P99 1.50%) | maxDD 64.4% (1× notional)
- corr: ORB -0.04, RSI2 +0.26 | SPX > SMA200: +1.06 bp/dag, daaronder -2.60
- per instrument t: FX_EURUSD -1.02, FX_GBPUSD -0.18, FX_USDJPY +1.00, FX_AUDUSD -0.09, FX_USDCAD -0.43, FX_USDCHF -2.63, GOLD_F +1.04, SILVER_F -0.57, SPX +0.33, NDX +1.67, DAX +0.18, N225 +0.50
- per jaar (%): 1927:+0.0 1928:+0.0 1929:-7.2 1930:-4.8 1931:+13.4 1932:+1.1 1933:+2.0 1934:-2.1 1935:+6.1 1936:+9.9 1937:-6.7 1938:-8.0 1939:-14.6 1940:-31.1 1941:+22.1 1942:-5.4 1943:+11.9 1944:+8.9 1945:+18.0 1946:-15.6 1947:-1.3 1948:-17.7 1949:-0.5 1950:+10.8 1951:+6.9 1952:+5.3 1953:-15.6 1954:+24.4 1955:+15.0 1956:-6.9 1957:-1.5 1958:-6.4 1959:+3.3 1960:-16.7 1961:+5.2 1962:-9.5 1963:-8.2 1964:+10.9 1965:+0.2 1966:-11.7 1967:-11.7 1968:-12.3 1969:+1.6 1970:-3.4 1971:-5.8 1972:+14.7 1973:-11.1 1974:-8.7 1975:+1.1 1976:+10.2 1977:-6.8 1978:+6.9 1979:-3.0 1980:-0.5 1981:-10.9 1982:+4.9 1983:+9.4 1984:+2.6 1985:+9.5 1986:-0.3 1987:+6.5 1988:+7.6 1989:+11.4 1990:-4.4 1991:-9.7 1992:+3.8 1993:-6.3 1994:-4.5 1995:+0.1 1996:+2.7 1997:+8.5 1998:+4.9 1999:+2.2 2000:-1.3 2001:+5.1 2002:+6.5 2003:+8.7 2004:+5.4 2005:+0.1 2006:-1.4 2007:+4.6 2008:+1.9 2009:-7.0 2010:-0.7 2011:-4.9 2012:-3.7 2013:+12.3 2014:-0.7 2015:+3.5 2016:-11.9 2017:+0.5 2018:-2.3 2019:-6.0 2020:-1.6 2021:-2.0 2022:-2.0 2023:-5.0 2024:-1.1
- kosten: bruto +1651.4% | spread/commissie 10.0% | financiering +1609.5% (som over instrument-dagen) → kostenpoort FAALT
- 5-jaarsvensters positief: 47% (9/19)
- beslissing: stop: kostenpoort (geen trial) (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
