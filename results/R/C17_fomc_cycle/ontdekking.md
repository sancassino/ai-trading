# C17_fomc_cycle — FOMC-cyclus: lang in even weken (kalender/Fed)
Mechanisme: Fed-informatiestroom en informele communicatie in de even weken van de FOMC-cyclus.
Bron: Cieslak, Morse, Vissing-Jorgensen (2019)

## variant basis {}
- ontdekking ≤ 2024: 8066 dagen, 7531 positie-wijzigingen, netto +2.77 bp/dag, SR +0.52 (90%-CI +0.24…+0.80)
- t: dag +2.94 | Newey-West +2.85 | blok-bootstrap +3.05 | H1 +2.15 | H2 +2.01 | +50% spread (NW) +2.81
- skew +0.46 | max dagverlies 9.03% (P99 2.54%) | maxDD 41.7% (1× notional)
- corr: ORB -0.06, RSI2 +0.33 | SPX > SMA200: +4.75 bp/dag, daaronder -3.68
- per instrument t: SPX +2.81, NDX +3.03, DJI +1.78, DAX +2.24, N225 +0.32
- per jaar (%): 1994:-1.5 1995:+1.2 1996:+6.7 1997:+20.7 1998:+40.5 1999:+20.3 2000:+3.8 2001:-4.2 2002:-30.5 2003:+40.4 2004:-5.4 2005:+8.3 2006:+0.5 2007:+9.1 2008:+7.2 2009:+16.6 2010:+13.3 2011:-3.7 2012:+16.2 2013:+17.5 2014:-0.7 2015:+11.9 2016:+9.8 2017:+6.1 2018:-17.5 2019:+10.0 2020:+9.2 2021:+3.9 2022:+0.9 2023:+8.4 2024:+4.9
- kosten: bruto +1701.1% | spread/commissie 33.0% | financiering +664.8% (som over instrument-dagen) → kostenpoort FAALT
- 5-jaarsvensters positief: 100% (6/6)
- beslissing: stop: kostenpoort (geen trial) (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
