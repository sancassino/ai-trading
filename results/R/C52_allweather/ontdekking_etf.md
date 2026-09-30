# C52_allweather — All-weather / risicopariteit: aandelen, obligaties, goud, grondstoffen (∝ 1/σ60, vol-target 8%, geen hefboom) (allocatie/risicopariteit)
Mechanisme: Diversificatie over groei-/inflatieregimes; gelijke risicobijdrage i.p.v. gelijke kapitaalbijdrage.
Bron: Dalio (All Weather); Asness–Frazzini–Pedersen (2012) risk parity

## variant basis {} — vehikel etf
- ontdekking ≤ 2024: 5540 dagen, 991 positie-wijzigingen, netto +1.68 bp/dag, SR +0.65 (90%-CI +0.31…+1.02)
- t: dag +3.05 | Newey-West +3.03 | blok-bootstrap +3.15 | H1 +2.90 | H2 +1.36 | +50% spread (NW) +3.02
- skew -0.33 | max dagverlies 3.08% (P99 1.10%) | maxDD 16.2% (1× notional)
- corr: ORB +0.04, RSI2 +0.29 | SPX > SMA200: +2.28 bp/dag, daaronder -0.36
- per instrument t: SPY +3.40, IEF +2.32, GLD +2.88, DBC +0.17, BOND10_SYN +nan, GOLD_F +nan
- per jaar (%): 2003:+10.5 2004:+4.7 2005:+2.9 2006:+3.3 2007:+11.3 2008:-3.9 2009:+9.6 2010:+14.8 2011:+9.2 2012:+5.5 2013:-3.2 2014:-0.4 2015:-6.5 2016:+6.5 2017:+7.7 2018:-3.3 2019:+10.3 2020:+4.9 2021:+8.2 2022:-7.2 2023:+3.0 2024:+5.3
- kosten: bruto +129.0% | spread/commissie 0.3% | financiering +2.1% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 100% (4/4)
- G-benchmark (vehikel etf): regel SR +0.65, CAGR +5.8%, maxDD 16.2%, Calmar 0.36 | buy-and-hold (60/40 SPY/IEF) SR +0.66, CAGR +8.4%, maxDD 31.5%, Calmar 0.27 → niet beter
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)

## variant lang {'assets': ['SPY', 'BOND10_SYN', 'GOLD_F'], 'start_jaar': 2001, 'benchmark': {'naam': '60/40 SPY/BOND10_SYN', 'gewichten': {'SPY': 0.6, 'BOND10_SYN': 0.4}}} — vehikel etf
- ontdekking ≤ 2024: 6041 dagen, 781 positie-wijzigingen, netto +2.00 bp/dag, SR +0.79 (90%-CI +0.45…+1.13)
- t: dag +3.85 | Newey-West +3.83 | blok-bootstrap +3.96 | H1 +3.52 | H2 +1.86 | +50% spread (NW) +3.82
- skew -0.25 | max dagverlies 2.99% (P99 1.11%) | maxDD 15.3% (1× notional)
- corr: ORB +0.06, RSI2 +0.25 | SPX > SMA200: +2.62 bp/dag, daaronder +0.37
- per instrument t: SPY +2.74, IEF +nan, GLD +nan, DBC +nan, BOND10_SYN +2.62, GOLD_F +2.99
- per jaar (%): 2001:-1.3 2002:+2.4 2003:+10.6 2004:+4.8 2005:+4.5 2006:+7.9 2007:+8.4 2008:-0.7 2009:+8.2 2010:+18.0 2011:+12.2 2012:+6.0 2013:-2.2 2014:+8.2 2015:-1.7 2016:+6.4 2017:+7.3 2018:-2.1 2019:+11.3 2020:+8.5 2021:+3.5 2022:-13.3 2023:+6.7 2024:+7.0
- kosten: bruto +161.6% | spread/commissie 0.4% | financiering +2.3% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 100% (4/4)
- G-benchmark (vehikel etf): regel SR +0.79, CAGR +6.7%, maxDD 15.3%, Calmar 0.44 | buy-and-hold (60/40 SPY/BOND10_SYN) SR +0.52, CAGR +7.0%, maxDD 31.4%, Calmar 0.22 → BETER (SR én maxDD)
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
