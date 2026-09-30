# rep_b2b_rsi2 — RSI(2)-dip boven SMA200 (replicatie B2b) (kortetermijn-omkeer)
Mechanisme: Liquiditeitsvoorziening na korte uitverkoop in een opwaartse trend; kopers worden betaald voor overnight-risico.
Bron: Connors & Alvarez (2008); eerder getest als B2b (t 3,65)

## variant basis {'entry': 10, 'exit': 70, 'sma': 200} — vehikel cfd
- ontdekking ≤ 2024: 9107 dagen, 2695 positie-wijzigingen, netto +0.93 bp/dag, SR +0.52 (90%-CI +0.28…+0.80)
- t: dag +3.12 | Newey-West +3.21 | blok-bootstrap +3.50 | H1 +3.00 | H2 +1.39 | +50% spread (NW) +3.15
- skew -0.97 | max dagverlies 3.75% (P99 0.91%) | maxDD 16.6% (1× notional)
- corr: ORB -0.02, RSI2 +0.75 | SPX > SMA200: +2.08 bp/dag, daaronder -2.44
- per instrument t: SPX +4.22, NDX +3.48, DAX -0.31, FTSE +1.70, N225 +0.12, GOLD_F +0.65
- per jaar (%): 1990:-8.6 1991:+3.6 1992:-1.9 1993:+3.5 1994:+0.6 1995:+11.5 1996:+2.2 1997:+13.9 1998:+2.7 1999:+11.5 2000:+6.9 2001:-0.5 2002:+0.2 2003:+9.2 2004:-1.2 2005:+2.3 2006:-1.2 2007:+3.7 2008:-5.5 2009:+7.6 2010:+6.9 2011:-4.1 2012:+5.0 2013:+9.0 2014:-2.3 2015:+2.6 2016:+0.5 2017:+4.1 2018:-4.9 2019:+0.4 2020:-3.4 2021:+4.9 2022:-1.2 2023:+0.7 2024:+5.5
- kosten: bruto +655.4% | spread/commissie 19.3% | financiering +187.5% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 86% (6/7)
- G-benchmark (vehikel cfd): regel SR +0.52, CAGR +2.3%, maxDD 16.6% | buy-and-hold SR +0.24, CAGR +2.4%, maxDD 62.2% → BETER (SR én maxDD)
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
