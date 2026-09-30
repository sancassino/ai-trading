# C03_donchian — Donchian 55/20 D1 met 2×ATR-stop (slotbasis) (trend)
Mechanisme: Breakout-trend (Turtle): doorbraak van een lange range kondigt een trend aan.
Bron: Faith (2007), Turtle-regels

## variant basis {} — vehikel cfd
- ontdekking ≤ 2024: 13604 dagen, 2930 positie-wijzigingen, netto +0.23 bp/dag, SR +0.13 (90%-CI -0.07…+0.36)
- t: dag +0.99 | Newey-West +0.97 | blok-bootstrap +1.00 | H1 +3.17 | H2 -1.21 | +50% spread (NW) +0.93
- skew -0.25 | max dagverlies 3.60% (P99 0.81%) | maxDD 38.3% (1× notional)
- corr: ORB -0.03, RSI2 -0.02 | SPX > SMA200: +0.15 bp/dag, daaronder +0.43
- per instrument t: FX_EURUSD +0.94, FX_GBPUSD +1.87, FX_USDJPY -0.15, FX_AUDUSD -0.02, FX_USDCAD -0.09, FX_USDCHF -1.40, GOLD_F -1.15
- per jaar (%): 1971:+3.6 1972:+3.6 1973:+2.6 1974:+1.2 1975:+5.2 1976:+3.9 1977:+5.5 1978:+1.2 1979:+2.3 1980:+2.0 1981:+3.2 1982:+6.0 1983:+2.7 1984:+6.8 1985:+3.7 1986:-0.0 1987:+5.5 1988:+2.4 1989:-1.3 1990:+1.6 1991:+2.2 1992:+7.9 1993:-5.9 1994:+1.8 1995:-4.6 1996:-1.2 1997:+0.5 1998:-3.7 1999:-4.5 2000:+1.4 2001:-5.6 2002:+3.5 2003:+4.4 2004:-3.7 2005:-2.8 2006:-3.8 2007:-1.0 2008:+10.0 2009:-1.1 2010:+1.9 2011:-3.0 2012:-2.2 2013:+2.2 2014:+0.9 2015:-2.0 2016:-2.4 2017:-6.7 2018:+2.8 2019:-1.1 2020:+1.2 2021:-4.7 2022:-1.8 2023:-5.3 2024:-4.2
- kosten: bruto +275.3% | spread/commissie 12.8% | financiering +263.8% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 60% (6/10)
- G-benchmark (vehikel cfd): regel SR +0.13, CAGR +0.5%, maxDD 38.3% | buy-and-hold SR -0.18, CAGR -0.9%, maxDD 44.9% → BETER (SR én maxDD)
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
