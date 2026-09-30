# C52_allweather — All-weather / risicopariteit: aandelen, obligaties, goud, grondstoffen (∝ 1/σ60, vol-target 8%, geen hefboom) (allocatie/risicopariteit)
Mechanisme: Diversificatie over groei-/inflatieregimes; gelijke risicobijdrage i.p.v. gelijke kapitaalbijdrage.
Bron: Dalio (All Weather); Asness–Frazzini–Pedersen (2012) risk parity

## variant basis {} — vehikel cfd_retail
- ontdekking ≤ 2024: 5540 dagen, 991 positie-wijzigingen, netto +1.15 bp/dag, SR +0.44 (90%-CI +0.11…+0.81)
- t: dag +2.07 | Newey-West +2.06 | blok-bootstrap +2.14 | H1 +2.23 | H2 +0.65 | +50% spread (NW) +2.06
- skew -0.32 | max dagverlies 3.08% (P99 1.10%) | maxDD 17.4% (1× notional)
- corr: ORB +0.04, RSI2 +0.29 | SPX > SMA200: +1.73 bp/dag, daaronder -0.85
- per instrument t: SPY +2.50, IEF +0.24, GLD +2.07, DBC -0.49, BOND10_SYN +nan, GOLD_F +nan
- per jaar (%): 2003:+9.1 2004:+3.3 2005:+1.5 2006:+1.9 2007:+9.9 2008:-5.2 2009:+8.5 2010:+13.4 2011:+7.9 2012:+4.1 2013:-4.6 2014:-1.8 2015:-7.9 2016:+5.2 2017:+6.3 2018:-4.7 2019:+8.9 2020:+3.6 2021:+6.8 2022:-8.3 2023:+1.7 2024:+3.9
- kosten: bruto +95.6% | spread/commissie 0.2% | financiering +31.9% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 75% (3/4)
- G-benchmark (vehikel cfd_retail): regel SR +0.44, CAGR +4.3%, maxDD 17.4%, Calmar 0.25 | buy-and-hold (60/40 SPY/IEF) SR +0.53, CAGR +6.8%, maxDD 32.8%, Calmar 0.21 → niet beter
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)

## variant lang {'assets': ['SPY', 'BOND10_SYN', 'GOLD_F'], 'start_jaar': 2001, 'benchmark': {'naam': '60/40 SPY/BOND10_SYN', 'gewichten': {'SPY': 0.6, 'BOND10_SYN': 0.4}}} — vehikel cfd_retail
- ontdekking ≤ 2024: 6041 dagen, 781 positie-wijzigingen, netto +1.58 bp/dag, SR +0.62 (90%-CI +0.29…+0.97)
- t: dag +3.05 | Newey-West +3.03 | blok-bootstrap +3.14 | H1 +2.96 | H2 +1.30 | +50% spread (NW) +3.03
- skew -0.25 | max dagverlies 2.99% (P99 1.11%) | maxDD 15.9% (1× notional)
- corr: ORB +0.06, RSI2 +0.25 | SPX > SMA200: +2.19 bp/dag, daaronder -0.01
- per instrument t: SPY +1.82, IEF +nan, GLD +nan, DBC +nan, BOND10_SYN +0.60, GOLD_F +2.62
- per jaar (%): 2001:-2.0 2002:+1.3 2003:+9.4 2004:+3.6 2005:+3.5 2006:+7.0 2007:+7.6 2008:-1.7 2009:+7.1 2010:+16.7 2011:+10.9 2012:+4.6 2013:-3.6 2014:+6.8 2015:-3.1 2016:+5.1 2017:+6.1 2018:-3.2 2019:+10.4 2020:+7.3 2021:+2.2 2022:-14.0 2023:+6.8 2024:+6.9
- kosten: bruto +131.0% | spread/commissie 0.3% | financiering +35.0% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 100% (4/4)
- G-benchmark (vehikel cfd_retail): regel SR +0.62, CAGR +5.6%, maxDD 15.9%, Calmar 0.35 | buy-and-hold (60/40 SPY/BOND10_SYN) SR +0.39, CAGR +5.5%, maxDD 32.6%, Calmar 0.17 → BETER (SR én maxDD)
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
