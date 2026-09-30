# C53_gem — Dual momentum (Antonacci GEM): US / ex-US aandelen of obligaties (momentum/allocatie)
Mechanisme: Absolute momentum (aandelen vs geldmarkt) beperkt bear-markt-DD; relatieve momentum kiest de sterkste regio.
Bron: Antonacci (2014) 'Dual Momentum Investing'

## variant basis {} — vehikel etf
- ontdekking ≤ 2024: 5537 dagen, 54 positie-wijzigingen, netto +3.39 bp/dag, SR +0.56 (90%-CI +0.26…+0.89)
- t: dag +2.61 | Newey-West +2.83 | blok-bootstrap +3.11 | H1 +2.29 | H2 +1.40 | +50% spread (NW) +2.82
- skew -0.56 | max dagverlies 10.95% (P99 2.78%) | maxDD 33.7% (1× notional)
- corr: ORB -0.04, RSI2 +0.42 | SPX > SMA200: +7.34 bp/dag, daaronder -10.11
- per instrument t: SPY +2.39, EFA +2.01, IEF +0.36
- per jaar (%): 2003:+16.6 2004:+16.9 2005:+9.9 2006:+19.3 2007:+6.7 2008:+4.2 2009:+0.7 2010:+7.3 2011:+3.6 2012:+15.4 2013:+16.5 2014:+13.1 2015:-6.7 2016:+6.5 2017:+16.6 2018:-8.8 2019:+14.9 2020:+9.6 2021:+26.0 2022:-20.4 2023:+2.2 2024:+17.9
- kosten: bruto +225.3% | spread/commissie 0.8% | financiering +2.2% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 100% (4/4)
- G-benchmark (vehikel etf): regel SR +0.56, CAGR +9.3%, maxDD 33.7%, Calmar 0.28 | buy-and-hold (60/40 SPY/IEF) SR +0.66, CAGR +8.4%, maxDD 31.5%, Calmar 0.27 → niet beter
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
