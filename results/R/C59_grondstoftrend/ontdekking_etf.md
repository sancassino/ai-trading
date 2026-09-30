# C59_grondstoftrend — Grondstoffen-trend: long DBC als maandeindslot > gem. 10 maandeinden, anders kas (trend)
Mechanisme: Grondstoffenindex trendt (contango zit in de index); lage correlatie met obligaties.
Bron: Faber (2007); catalogus C59 (korte reeks 2006→)

## variant basis {} — vehikel etf
- ontdekking ≤ 2024: 4530 dagen, 31 positie-wijzigingen, netto +0.96 bp/dag, SR +0.18 (90%-CI -0.17…+0.60)
- t: dag +0.75 | Newey-West +0.76 | blok-bootstrap +0.76 | H1 +0.08 | H2 +1.01 | +50% spread (NW) +0.74
- skew -0.64 | max dagverlies 7.95% (P99 2.74%) | maxDD 48.3% (1× notional)
- corr: ORB -0.00, RSI2 +0.13 | SPX > SMA200: +1.45 bp/dag, daaronder -0.59
- per instrument t: DBC +1.17
- per jaar (%): 2007:+19.8 2008:+8.8 2009:+7.5 2010:-1.4 2011:-5.2 2012:-20.5 2013:-2.4 2014:-3.2 2015:+0.0 2016:+8.9 2017:+0.4 2018:+1.1 2019:-0.1 2020:-10.5 2021:+36.5 2022:+15.8 2023:-8.4 2024:-3.4
- kosten: bruto +59.4% | spread/commissie 2.0% | financiering -10.4% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 67% (2/3)
- G-benchmark (vehikel etf): regel SR +0.18, CAGR +2.9%, maxDD 48.3%, Calmar 0.06 | buy-and-hold (gelijk gewogen) SR +0.03, CAGR +0.1%, maxDD 76.6%, Calmar 0.00 → BETER (SR én maxDD)
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
