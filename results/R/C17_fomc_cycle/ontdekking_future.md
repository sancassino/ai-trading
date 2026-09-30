# C17_fomc_cycle — FOMC-cyclus: lang in even weken (kalender/Fed)
Mechanisme: Fed-informatiestroom en informele communicatie in de even weken van de FOMC-cyclus.
Bron: Cieslak, Morse, Vissing-Jorgensen (2019)

## variant basis {} — vehikel future
- ontdekking ≤ 2024: 8066 dagen, 7531 positie-wijzigingen, netto +3.93 bp/dag, SR +0.74 (90%-CI +0.46…+1.02)
- t: dag +4.16 | Newey-West +4.03 | blok-bootstrap +4.32 | H1 +2.77 | H2 +3.19 | +50% spread (NW) +3.98
- skew +0.49 | max dagverlies 8.98% (P99 2.51%) | maxDD 32.7% (1× notional)
- corr: ORB -0.07, RSI2 +0.33 | SPX > SMA200: +5.85 bp/dag, daaronder -2.47
- per instrument t: SPX +4.26, NDX +4.35, DJI +4.07, DAX +3.78, N225 +2.04
- per jaar (%): 1994:+0.3 1995:+2.3 1996:+8.1 1997:+22.1 1998:+42.1 1999:+22.0 2000:+4.7 2001:-1.5 2002:-26.8 2003:+44.6 2004:-1.6 2005:+11.1 2006:+2.2 2007:+11.2 2008:+10.9 2009:+20.6 2010:+17.8 2011:+0.6 2012:+20.5 2013:+21.8 2014:+3.6 2015:+16.2 2016:+13.9 2017:+9.8 2018:-14.2 2019:+13.1 2020:+13.2 2021:+8.1 2022:+4.0 2023:+9.8 2024:+6.4
- kosten: bruto +1465.0% | spread/commissie 37.7% | financiering -370.2% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 100% (6/6)
- G-benchmark (vehikel future): regel SR +0.74, CAGR +12.0%, maxDD 32.7%, Calmar 0.37 | buy-and-hold (gelijk gewogen) SR +0.53, CAGR +10.4%, maxDD 61.8%, Calmar 0.17 → BETER (SR én maxDD)
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
