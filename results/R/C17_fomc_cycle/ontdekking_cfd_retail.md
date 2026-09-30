# C17_fomc_cycle — FOMC-cyclus: lang in even weken (kalender/Fed)
Mechanisme: Fed-informatiestroom en informele communicatie in de even weken van de FOMC-cyclus.
Bron: Cieslak, Morse, Vissing-Jorgensen (2019)

## variant basis {} — vehikel cfd_retail
- ontdekking ≤ 2024: 8066 dagen, 7531 positie-wijzigingen, netto +3.66 bp/dag, SR +0.69 (90%-CI +0.41…+0.97)
- t: dag +3.88 | Newey-West +3.76 | blok-bootstrap +4.02 | H1 +2.58 | H2 +2.98 | +50% spread (NW) +3.71
- skew +0.49 | max dagverlies 8.99% (P99 2.51%) | maxDD 33.9% (1× notional)
- corr: ORB -0.06, RSI2 +0.33 | SPX > SMA200: +5.59 bp/dag, daaronder -2.73
- per instrument t: SPX +4.38, NDX +4.14, DJI +3.76, DAX +3.51, N225 +1.70
- per jaar (%): 1994:-0.3 1995:+1.7 1996:+7.4 1997:+21.3 1998:+41.3 1999:+21.2 2000:+3.9 2001:-2.3 2002:-27.6 2003:+43.8 2004:-2.4 2005:+10.3 2006:+1.4 2007:+10.4 2008:+10.2 2009:+20.1 2010:+17.1 2011:-0.0 2012:+19.8 2013:+21.2 2014:+3.0 2015:+15.6 2016:+13.3 2017:+9.2 2018:-14.9 2019:+12.5 2020:+12.5 2021:+7.4 2022:+3.4 2023:+9.1 2024:+5.6
- kosten: bruto +1502.3% | spread/commissie 33.0% | financiering -226.5% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 100% (6/6)
- G-benchmark (vehikel cfd_retail): regel SR +0.69, CAGR +11.2%, maxDD 33.9%, Calmar 0.33 | buy-and-hold (gelijk gewogen) SR +0.47, CAGR +9.1%, maxDD 63.0%, Calmar 0.14 → BETER (SR én maxDD)
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
