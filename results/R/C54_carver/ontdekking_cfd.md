# C54_carver — Carver-forecastcombinatie: EWMAC(8,32/16,64/32,128/64,256) + FX-carry, 16 instrumenten, vol-target per instrument 10% (trend+carry (multi-asset))
Mechanisme: Trend (onder-reactie, hedgers) en carry (risicopremie) over veel weinig-gecorreleerde markten; diversificatie is de hefboom.
Bron: Carver (2015) 'Systematic Trading'; Hurst–Ooi–Pedersen (2017); Koijen e.a. (2018)

## variant qa {'start_jaar': 1990, 'excl': ['WTI_F']} — vehikel cfd
- ontdekking ≤ 2024: 9107 dagen, 54097 positie-wijzigingen, netto +0.02 bp/dag, SR +0.01 (90%-CI -0.26…+0.27)
- t: dag +0.09 | Newey-West +0.08 | blok-bootstrap +0.09 | H1 +1.11 | H2 -1.11 | +50% spread (NW) +0.05
- skew -0.43 | max dagverlies 1.82% (P99 0.79%) | maxDD 22.3% (1× notional)
- corr: ORB -0.05, RSI2 +0.30 | SPX > SMA200: +0.16 bp/dag, daaronder -1.03
- per instrument t: FX_EURUSD +1.32, FX_GBPUSD +0.88, FX_USDJPY +0.36, FX_AUDUSD +0.23, FX_USDCAD +0.10, FX_USDCHF -1.72, GOLD_F +0.07, SILVER_F -0.66, WTI_F +nan, COPPER_F +nan, SPX -0.11, NDX +0.59, DAX +0.20, N225 -0.72, FTSE -3.38, BOND10_SYN +nan
- per jaar (%): 1990:-2.4 1991:-2.0 1992:-2.3 1993:-1.1 1994:-5.8 1995:+6.1 1996:+1.6 1997:+6.2 1998:+3.4 1999:+2.4 2000:-3.6 2001:+4.1 2002:+3.8 2003:+7.5 2004:-1.2 2005:+1.4 2006:+0.9 2007:-2.1 2008:+1.7 2009:-0.4 2010:+1.1 2011:-1.7 2012:-2.7 2013:+5.3 2014:-3.2 2015:-2.5 2016:-4.1 2017:-0.5 2018:-0.2 2019:-3.5 2020:+0.7 2021:-2.7 2022:-1.5 2023:-3.2 2024:+2.7
- kosten: bruto +541.5% | spread/commissie 16.5% | financiering +674.1% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 43% (3/7)
- G-benchmark (vehikel cfd): regel SR +0.01, CAGR -0.0%, maxDD 22.3%, Calmar -0.00 | buy-and-hold (60/40 SPX/BOND10_SYN) SR +0.26, CAGR +2.3%, maxDD 50.5%, Calmar 0.04 → niet beter
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
