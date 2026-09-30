# C52_allweather — All-weather / risicopariteit: aandelen, obligaties, goud, grondstoffen (∝ 1/σ60, vol-target 8%, geen hefboom) (allocatie/risicopariteit)
Mechanisme: Diversificatie over groei-/inflatieregimes; gelijke risicobijdrage i.p.v. gelijke kapitaalbijdrage.
Bron: Dalio (All Weather); Asness–Frazzini–Pedersen (2012) risk parity

## variant basis {} — vehikel cfd
- ontdekking ≤ 2024: 5540 dagen, 264 positie-wijzigingen, netto +0.55 bp/dag, SR +0.42 (90%-CI +0.09…+0.74)
- t: dag +1.97 | Newey-West +2.15 | blok-bootstrap +2.32 | H1 +1.23 | H2 +1.62 | +50% spread (NW) +2.15
- skew -0.24 | max dagverlies 1.74% (P99 0.56%) | maxDD 10.1% (1× notional)
- corr: ORB -0.04, RSI2 +0.51 | SPX > SMA200: +1.47 bp/dag, daaronder -2.57
- per instrument t: SPY +1.97, IEF +nan, GLD +nan, DBC +nan, BOND10_SYN +nan, GOLD_F +nan
- per jaar (%): 2003:+6.6 2004:+2.0 2005:-0.4 2006:+2.3 2007:-0.1 2008:-7.0 2009:+3.9 2010:+1.9 2011:-0.4 2012:+1.4 2013:+4.9 2014:+1.6 2015:-0.9 2016:+1.3 2017:+3.9 2018:-1.0 2019:+3.0 2020:-0.5 2021:+4.0 2022:-3.7 2023:+3.8 2024:+4.2
- kosten: bruto +53.4% | spread/commissie 0.0% | financiering +22.7% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 75% (3/4)
- G-benchmark (vehikel cfd): regel SR +0.42, CAGR +1.4%, maxDD 10.1%, Calmar 0.13 | buy-and-hold (60/40 SPY/IEF) SR +0.39, CAGR +3.8%, maxDD 39.3%, Calmar 0.10 → BETER (SR én maxDD)
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)

## variant lang {'assets': ['SPY', 'BOND10_SYN', 'GOLD_F'], 'start_jaar': 2001, 'benchmark': {'naam': '60/40 SPY/BOND10_SYN', 'gewichten': {'SPY': 0.6, 'BOND10_SYN': 0.4}}} — vehikel cfd
- ontdekking ≤ 2024: 6041 dagen, 516 positie-wijzigingen, netto +0.72 bp/dag, SR +0.33 (90%-CI +0.02…+0.66)
- t: dag +1.60 | Newey-West +1.63 | blok-bootstrap +1.74 | H1 +1.13 | H2 +1.15 | +50% spread (NW) +1.63
- skew -0.30 | max dagverlies 2.83% (P99 0.98%) | maxDD 15.5% (1× notional)
- corr: ORB +0.02, RSI2 +0.38 | SPX > SMA200: +2.16 bp/dag, daaronder -2.95
- per instrument t: SPY +1.31, IEF +nan, GLD +nan, DBC +nan, BOND10_SYN +nan, GOLD_F +0.94
- per jaar (%): 2001:-4.5 2002:-8.2 2003:+8.0 2004:+0.9 2005:+4.2 2006:+7.7 2007:+4.6 2008:-9.9 2009:+9.5 2010:+8.0 2011:+1.6 2012:+2.0 2013:+0.2 2014:+0.3 2015:-5.4 2016:+4.4 2017:+4.0 2018:-3.4 2019:+5.7 2020:+2.7 2021:+3.1 2022:-7.3 2023:+6.1 2024:+9.3
- kosten: bruto +110.9% | spread/commissie 0.1% | financiering +67.2% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 75% (3/4)
- G-benchmark (vehikel cfd): regel SR +0.33, CAGR +1.7%, maxDD 15.5%, Calmar 0.11 | buy-and-hold (60/40 SPY/BOND10_SYN) SR +0.26, CAGR +2.3%, maxDD 41.3%, Calmar 0.06 → BETER (SR én maxDD)
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
