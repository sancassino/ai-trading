# C57_gtaa — Faber-GTAA: 10-mnd-SMA long/kas op 5 klassen (VS, ex-VS, obligatie, goud, grondstoffen), 1/5 per klasse (trend/allocatie)
Mechanisme: Trend per klasse met eigen (lage-correlatie) rendementsbron; kas als terugvaloptie.
Bron: Faber (2007) 'A Quantitative Approach to Tactical Asset Allocation'

## variant basis {} — vehikel etf
- ontdekking ≤ 2024: 5537 dagen, 184 positie-wijzigingen, netto +1.76 bp/dag, SR +0.64 (90%-CI +0.34…+0.92)
- t: dag +2.99 | Newey-West +3.11 | blok-bootstrap +3.52 | H1 +2.65 | H2 +1.46 | +50% spread (NW) +3.07
- skew -0.36 | max dagverlies 2.93% (P99 1.28%) | maxDD 11.9% (1× notional)
- corr: ORB -0.02, RSI2 +0.45 | SPX > SMA200: +2.97 bp/dag, daaronder -2.36
- per instrument t: SPY +3.52, EFA +2.65, IEF +1.69, GLD +2.18, DBC +0.93
- per jaar (%): 2003:+10.2 2004:+5.3 2005:+4.8 2006:+7.6 2007:+11.1 2008:+4.8 2009:+12.5 2010:+4.2 2011:+2.4 2012:-2.7 2013:+8.5 2014:+0.2 2015:-3.5 2016:+1.2 2017:+7.8 2018:-2.1 2019:+6.4 2020:+7.3 2021:+10.5 2022:-4.4 2023:-0.6 2024:+5.9
- kosten: bruto +124.4% | spread/commissie 2.4% | financiering +1.0% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 100% (4/4)
- G-benchmark (vehikel etf): regel SR +0.64, CAGR +5.9%, maxDD 11.9%, Calmar 0.50 | buy-and-hold (60/40 SPY/IEF) SR +0.66, CAGR +8.4%, maxDD 31.5%, Calmar 0.27 → niet beter
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
