# C17_fomc_cycle — FOMC-cyclus: lang in even weken (kalender/Fed)
Mechanisme: Fed-informatiestroom en informele communicatie in de even weken van de FOMC-cyclus.
Bron: Cieslak, Morse, Vissing-Jorgensen (2019)

## variant basis {} — vehikel etf
- ontdekking ≤ 2024: 8066 dagen, 7531 positie-wijzigingen, netto +3.72 bp/dag, SR +0.70 (90%-CI +0.42…+0.98)
- t: dag +3.94 | Newey-West +3.82 | blok-bootstrap +4.09 | H1 +2.63 | H2 +3.01 | +50% spread (NW) +3.67
- skew +0.50 | max dagverlies 8.98% (P99 2.51%) | maxDD 33.5% (1× notional)
- corr: ORB -0.07, RSI2 +0.33 | SPX > SMA200: +5.64 bp/dag, daaronder -2.69
- per instrument t: SPX +4.06, NDX +4.21, DJI +3.86, DAX +3.61, N225 +1.88
- per jaar (%): 1994:-0.2 1995:+1.8 1996:+7.5 1997:+21.5 1998:+41.6 1999:+21.4 2000:+4.1 2001:-2.0 2002:-27.4 2003:+44.1 2004:-2.2 2005:+10.5 2006:+1.6 2007:+10.6 2008:+10.4 2009:+20.1 2010:+17.2 2011:+0.0 2012:+19.9 2013:+21.2 2014:+3.1 2015:+15.7 2016:+13.3 2017:+9.3 2018:-14.8 2019:+12.6 2020:+12.7 2021:+7.6 2022:+3.5 2023:+9.2 2024:+5.8
- kosten: bruto +1701.1% | spread/commissie 113.0% | financiering -126.4% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 100% (6/6)
- G-benchmark (vehikel etf): regel SR +0.70, CAGR +11.4%, maxDD 33.5%, Calmar 0.34 | buy-and-hold (gelijk gewogen) SR +0.53, CAGR +10.3%, maxDD 61.9%, Calmar 0.17 → BETER (SR én maxDD)
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
