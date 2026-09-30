# C17_fomc_cycle — FOMC-cyclus: lang in even weken (kalender/Fed)
Mechanisme: Fed-informatiestroom en informele communicatie in de even weken van de FOMC-cyclus.
Bron: Cieslak, Morse, Vissing-Jorgensen (2019)

## variant basis {} — vehikel cfd_retail_hi
- ontdekking ≤ 2024: 8066 dagen, 7531 positie-wijzigingen, netto +3.32 bp/dag, SR +0.62 (90%-CI +0.35…+0.90)
- t: dag +3.52 | Newey-West +3.41 | blok-bootstrap +3.65 | H1 +2.34 | H2 +2.70 | +50% spread (NW) +3.32
- skew +0.48 | max dagverlies 9.00% (P99 2.52%) | maxDD 35.2% (1× notional)
- corr: ORB -0.06, RSI2 +0.33 | SPX > SMA200: +5.26 bp/dag, daaronder -3.07
- per instrument t: SPX +4.08, NDX +3.94, DJI +3.48, DAX +3.26, N225 +1.38
- per jaar (%): 1994:-1.1 1995:+0.8 1996:+6.5 1997:+20.4 1998:+40.4 1999:+20.3 2000:+2.9 2001:-3.3 2002:-28.5 2003:+42.9 2004:-3.3 2005:+9.3 2006:+0.5 2007:+9.4 2008:+9.4 2009:+19.2 2010:+16.2 2011:-0.9 2012:+19.0 2013:+20.3 2014:+2.1 2015:+14.7 2016:+12.5 2017:+8.3 2018:-15.8 2019:+11.7 2020:+11.7 2021:+6.6 2022:+2.5 2023:+8.2 2024:+4.8
- kosten: bruto +1502.3% | spread/commissie 66.1% | financiering -129.5% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 100% (6/6)
- G-benchmark (vehikel cfd_retail_hi): regel SR +0.62, CAGR +10.3%, maxDD 35.2%, Calmar 0.29 | buy-and-hold (gelijk gewogen) SR +0.40, CAGR +8.0%, maxDD 64.0%, Calmar 0.13 → BETER (SR én maxDD)
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
