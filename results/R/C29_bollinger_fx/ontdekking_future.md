# C29_bollinger_fx — Z-score(20d) ±2 omkeer op FX-kruisen, 5 dagen vast (mean-reversion)
Mechanisme: FX-kruisen keren in range-regimes terug naar hun 20d-gemiddelde; liquiditeitsverschaffing.
Bron: klassieke Bollinger-omkeer; catalogus C29

## variant basis {} — vehikel future
- ontdekking ≤ 2024: 5470 dagen, 1426 positie-wijzigingen, netto +0.45 bp/dag, SR +0.37 (90%-CI +0.09…+0.63)
- t: dag +1.71 | Newey-West +1.97 | blok-bootstrap +2.19 | H1 +1.35 | H2 +1.06 | +50% spread (NW) +1.87
- skew +2.88 | max dagverlies 1.88% (P99 0.57%) | maxDD 5.4% (1× notional)
- corr: ORB -0.01, RSI2 +0.05 | SPX > SMA200: +0.31 bp/dag, daaronder +1.65
- per instrument t: EURGBP +3.82, EURJPY +1.47, EURCHF +2.74
- per jaar (%): 2004:+1.4 2005:-0.1 2006:+2.3 2007:+1.8 2008:-2.8 2009:+3.5 2010:-1.0 2011:+6.5 2012:+0.3 2013:+2.5 2014:+0.9 2015:+2.0 2016:-3.7 2017:+1.4 2018:-1.4 2019:+2.6 2020:+1.0 2021:+2.4 2022:+6.7 2023:+1.1 2024:-2.8
- kosten: bruto +79.3% | spread/commissie 7.2% | financiering -99.5% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 75% (3/4)
- G-benchmark (vehikel future): regel SR +0.37, CAGR +2.7%, maxDD 5.4%, Calmar 0.49 | buy-and-hold (gelijk gewogen) SR +0.09, CAGR +1.9%, maxDD 22.2%, Calmar 0.09 → BETER (SR én maxDD)
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
