# C52_allweather — All-weather / risicopariteit: aandelen, obligaties, goud, grondstoffen (∝ 1/σ60, vol-target 8%, geen hefboom) (allocatie/risicopariteit)
Mechanisme: Diversificatie over groei-/inflatieregimes; gelijke risicobijdrage i.p.v. gelijke kapitaalbijdrage.
Bron: Dalio (All Weather); Asness–Frazzini–Pedersen (2012) risk parity

## variant basis {} — vehikel cfd_retail_hi
- ontdekking ≤ 2024: 5540 dagen, 991 positie-wijzigingen, netto +0.76 bp/dag, SR +0.29 (90%-CI -0.04…+0.66)
- t: dag +1.37 | Newey-West +1.36 | blok-bootstrap +1.42 | H1 +1.75 | H2 +0.13 | +50% spread (NW) +1.35
- skew -0.32 | max dagverlies 3.08% (P99 1.11%) | maxDD 20.1% (1× notional)
- corr: ORB +0.04, RSI2 +0.29 | SPX > SMA200: +1.33 bp/dag, daaronder -1.21
- per instrument t: SPY +2.21, IEF -0.47, GLD +1.80, DBC -0.73, BOND10_SYN +nan, GOLD_F +nan
- per jaar (%): 2003:+8.1 2004:+2.3 2005:+0.5 2006:+0.9 2007:+8.9 2008:-6.1 2009:+7.8 2010:+12.4 2011:+6.9 2012:+3.0 2013:-5.6 2014:-2.8 2015:-8.9 2016:+4.1 2017:+5.3 2018:-5.7 2019:+7.9 2020:+2.7 2021:+5.8 2022:-9.1 2023:+0.7 2024:+2.9
- kosten: bruto +95.6% | spread/commissie 0.5% | financiering +53.2% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 75% (3/4)
- G-benchmark (vehikel cfd_retail_hi): regel SR +0.29, CAGR +3.3%, maxDD 20.1%, Calmar 0.17 | buy-and-hold (60/40 SPY/IEF) SR +0.43, CAGR +5.8%, maxDD 33.7%, Calmar 0.17 → niet beter
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)

## variant lang {'assets': ['SPY', 'BOND10_SYN', 'GOLD_F'], 'start_jaar': 2001, 'benchmark': {'naam': '60/40 SPY/BOND10_SYN', 'gewichten': {'SPY': 0.6, 'BOND10_SYN': 0.4}}} — vehikel cfd_retail_hi
- ontdekking ≤ 2024: 6041 dagen, 781 positie-wijzigingen, netto +1.19 bp/dag, SR +0.47 (90%-CI +0.14…+0.81)
- t: dag +2.30 | Newey-West +2.29 | blok-bootstrap +2.37 | H1 +2.45 | H2 +0.75 | +50% spread (NW) +2.28
- skew -0.25 | max dagverlies 2.99% (P99 1.11%) | maxDD 17.6% (1× notional)
- corr: ORB +0.06, RSI2 +0.25 | SPX > SMA200: +1.79 bp/dag, daaronder -0.39
- per instrument t: SPY +1.53, IEF +nan, GLD +nan, DBC +nan, BOND10_SYN -0.08, GOLD_F +2.36
- per jaar (%): 2001:-3.1 2002:+0.3 2003:+8.4 2004:+2.6 2005:+2.5 2006:+6.0 2007:+6.6 2008:-2.6 2009:+6.3 2010:+15.7 2011:+9.9 2012:+3.6 2013:-4.6 2014:+5.8 2015:-4.1 2016:+4.1 2017:+5.1 2018:-4.2 2019:+9.4 2020:+6.4 2021:+1.1 2022:-14.9 2023:+5.9 2024:+5.9
- kosten: bruto +131.0% | spread/commissie 0.5% | financiering +58.3% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 100% (4/4)
- G-benchmark (vehikel cfd_retail_hi): regel SR +0.47, CAGR +4.5%, maxDD 17.6%, Calmar 0.26 | buy-and-hold (60/40 SPY/BOND10_SYN) SR +0.30, CAGR +4.4%, maxDD 33.4%, Calmar 0.13 → BETER (SR én maxDD)
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
