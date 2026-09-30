# C12_carry_trend — FX-carry G7 met 3m-trendfilter (carry)
Mechanisme: Carry = compensatie voor crashrisico; trendfilter vermijdt carry-crashes.
Bron: Lustig–Roussanov–Verdelhan (2011); Menkhoff e.a. (2012)

## variant basis {}
- ontdekking ≤ 2024: 13547 dagen, 456 positie-wijzigingen, netto +0.01 bp/dag, SR +0.01 (90%-CI -0.20…+0.22)
- t: dag +0.09 | Newey-West +0.09 | blok-bootstrap +0.10 | H1 +nan | H2 +0.09 | +50% spread (NW) +0.08
- skew -0.77 | max dagverlies 1.72% (P99 0.47%) | maxDD 19.0% (1× notional)
- corr: ORB -0.00, RSI2 +0.10 | SPX > SMA200: +0.12 bp/dag, daaronder -0.27
- per instrument t: FX_EURUSD +1.44, FX_GBPUSD +0.12, FX_USDJPY +1.01, FX_AUDUSD -0.46, FX_USDCAD -1.20, FX_USDCHF -0.58
- per jaar (%): 1971:+0.0 1972:+0.0 1973:+0.0 1974:+0.0 1975:+0.0 1976:+0.0 1977:+0.0 1978:+0.0 1979:+0.0 1980:+0.0 1981:+0.0 1982:+0.0 1983:+0.0 1984:+0.0 1985:+0.0 1986:+0.0 1987:+0.0 1988:+0.0 1989:+0.0 1990:+0.0 1991:+0.0 1992:+0.0 1993:+0.0 1994:+0.0 1995:+0.0 1996:+0.0 1997:+0.0 1998:+0.0 1999:+0.0 2000:+0.0 2001:+0.0 2002:+2.9 2003:+4.2 2004:+0.5 2005:+3.8 2006:-0.7 2007:+2.2 2008:-0.4 2009:+4.9 2010:+0.3 2011:-0.8 2012:-1.9 2013:+1.0 2014:+3.1 2015:-3.8 2016:-2.5 2017:-2.9 2018:-1.8 2019:-2.5 2020:-1.0 2021:-1.9 2022:+0.4 2023:-0.5 2024:-1.0
- kosten: bruto +71.4% | spread/commissie 2.0% | financiering +60.9% (som over instrument-dagen) → kostenpoort FAALT
- 5-jaarsvensters positief: 20% (2/10)
- beslissing: stop: kostenpoort (geen trial) (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
