# C33_trend_lowvol — TSMOM-mix alleen in laag-vol-regime (σ60 < eigen mediane σ60 tot t) (trend/regime)
Mechanisme: Trends zijn betrouwbaarder in rustige regimes; hoge vol = reversals/crashes.
Bron: catalogus C33; Moreira–Muir-idee toegepast als regime-filter

## variant basis {} — vehikel cfd
- ontdekking ≤ 2024: 24868 dagen, 2975 positie-wijzigingen, netto +0.30 bp/dag, SR +0.14 (90%-CI -0.02…+0.32)
- t: dag +1.44 | Newey-West +1.41 | blok-bootstrap +1.47 | H1 +1.19 | H2 +0.95 | +50% spread (NW) +1.39
- skew -0.51 | max dagverlies 6.18% (P99 1.04%) | maxDD 28.8% (1× notional)
- corr: ORB +0.01, RSI2 +0.26 | SPX > SMA200: +0.72 bp/dag, daaronder -0.70
- per instrument t: FX_EURUSD +0.82, FX_GBPUSD +0.91, FX_USDJPY -0.27, FX_AUDUSD -0.12, FX_USDCAD +0.64, FX_USDCHF -1.05, GOLD_F +0.94, SILVER_F -0.91, SPX +0.58, NDX +0.57, DAX +0.67, N225 +1.46
- per jaar (%): 1927:+0.0 1928:+0.0 1929:-3.3 1930:+0.4 1931:+0.0 1932:+0.0 1933:+0.0 1934:-4.1 1935:+4.5 1936:+4.6 1937:-1.6 1938:+0.0 1939:-16.3 1940:-9.4 1941:+10.1 1942:+4.7 1943:+11.1 1944:+3.5 1945:+8.5 1946:+0.9 1947:-4.0 1948:-15.1 1949:+4.0 1950:+4.7 1951:-3.4 1952:-1.2 1953:-5.2 1954:+24.4 1955:+7.9 1956:-9.1 1957:+0.3 1958:+15.1 1959:+1.3 1960:-22.1 1961:+9.8 1962:+11.3 1963:-3.7 1964:+8.2 1965:+1.0 1966:-0.1 1967:-7.0 1968:+5.4 1969:+6.1 1970:+5.9 1971:-4.7 1972:+11.5 1973:-0.5 1974:+2.1 1975:+1.1 1976:+2.9 1977:-1.7 1978:+1.7 1979:-0.9 1980:-4.7 1981:-1.5 1982:-3.1 1983:+2.3 1984:-0.3 1985:+5.0 1986:+3.0 1987:+3.8 1988:+0.8 1989:+7.9 1990:-1.5 1991:-1.0 1992:+1.7 1993:+1.2 1994:-3.9 1995:+2.6 1996:+5.0 1997:-0.2 1998:-0.5 1999:-0.2 2000:+0.6 2001:-0.4 2002:+3.5 2003:+2.6 2004:+2.3 2005:-1.1 2006:+0.7 2007:+2.2 2008:-2.3 2009:+0.5 2010:+1.9 2011:+0.1 2012:-1.5 2013:+5.5 2014:-2.0 2015:-1.7 2016:-2.2 2017:+1.5 2018:+1.1 2019:-6.5 2020:+0.6 2021:-3.5 2022:-0.2 2023:-1.7 2024:-0.5
- kosten: bruto +835.8% | spread/commissie 10.0% | financiering +630.3% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 63% (12/19)
- G-benchmark (vehikel cfd): regel SR +0.14, CAGR +0.6%, maxDD 28.8%, Calmar 0.02 | buy-and-hold (gelijk gewogen) SR +0.14, CAGR +1.0%, maxDD 88.0%, Calmar 0.01 → BETER (SR én maxDD)
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
