# C54_carver — Carver-forecastcombinatie: EWMAC(8,32/16,64/32,128/64,256) + FX-carry, 16 instrumenten, vol-target per instrument 10% (trend+carry (multi-asset))
Mechanisme: Trend (onder-reactie, hedgers) en carry (risicopremie) over veel weinig-gecorreleerde markten; diversificatie is de hefboom.
Bron: Carver (2015) 'Systematic Trading'; Hurst–Ooi–Pedersen (2017); Koijen e.a. (2018)

## variant qa {'start_jaar': 1990, 'excl': ['WTI_F']} — vehikel future
- ontdekking ≤ 2024: 9108 dagen, 64738 positie-wijzigingen, netto +0.63 bp/dag, SR +0.42 (90%-CI +0.15…+0.69)
- t: dag +2.54 | Newey-West +2.45 | blok-bootstrap +2.51 | H1 +2.71 | H2 +0.81 | +50% spread (NW) +2.43
- skew -0.37 | max dagverlies 1.72% (P99 0.72%) | maxDD 7.0% (1× notional)
- corr: ORB -0.05, RSI2 +0.27 | SPX > SMA200: +0.72 bp/dag, daaronder -0.33
- per instrument t: FX_EURUSD +3.53, FX_GBPUSD +2.42, FX_USDJPY +2.68, FX_AUDUSD +2.03, FX_USDCAD +3.11, FX_USDCHF +1.29, GOLD_F +2.08, SILVER_F +1.07, WTI_F +55.38, COPPER_F +2.29, SPX +2.34, NDX +3.30, DAX +2.75, N225 +2.13, FTSE +0.08, BOND10_SYN +4.35
- per jaar (%): 1990:-1.8 1991:+2.5 1992:-0.8 1993:+3.1 1994:-3.1 1995:+9.8 1996:-0.1 1997:+6.0 1998:+4.1 1999:+2.9 2000:-1.6 2001:+5.0 2002:+3.7 2003:+8.0 2004:+0.8 2005:+3.1 2006:+2.8 2007:-1.9 2008:+3.9 2009:+0.1 2010:+3.2 2011:-0.0 2012:-1.5 2013:+6.8 2014:-1.1 2015:-0.5 2016:-2.8 2017:+2.7 2018:+1.1 2019:-0.9 2020:+3.6 2021:+1.0 2022:-0.0 2023:-2.9 2024:+2.1
- kosten: bruto +537.7% | spread/commissie 15.7% | financiering -1241.5% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 71% (5/7)
- G-benchmark (vehikel future): regel SR +0.42, CAGR +4.2%, maxDD 7.0%, Calmar 0.60 | buy-and-hold (60/40 SPX/BOND10_SYN) SR +0.49, CAGR +7.5%, maxDD 32.7%, Calmar 0.23 → niet beter
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
