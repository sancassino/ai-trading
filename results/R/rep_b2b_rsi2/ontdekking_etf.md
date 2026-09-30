# rep_b2b_rsi2 — RSI(2)-dip boven SMA200 (replicatie B2b) (kortetermijn-omkeer)
Mechanisme: Liquiditeitsvoorziening na korte uitverkoop in een opwaartse trend; kopers worden betaald voor overnight-risico.
Bron: Connors & Alvarez (2008); eerder getest als B2b (t 3,65)

## variant basis {'entry': 10, 'exit': 70, 'sma': 200} — vehikel etf
- ontdekking ≤ 2024: 9107 dagen, 2695 positie-wijzigingen, netto +1.16 bp/dag, SR +0.65 (90%-CI +0.41…+0.94)
- t: dag +3.90 | Newey-West +4.02 | blok-bootstrap +4.40 | H1 +3.42 | H2 +2.08 | +50% spread (NW) +3.89
- skew -0.90 | max dagverlies 3.75% (P99 0.91%) | maxDD 12.9% (1× notional)
- corr: ORB -0.03, RSI2 +0.75 | SPX > SMA200: +2.33 bp/dag, daaronder -2.28
- per instrument t: SPX +6.68, NDX +5.27, DAX +1.77, FTSE +5.25, N225 +2.41, GOLD_F +2.34
- per jaar (%): 1990:-8.3 1991:+4.0 1992:-1.4 1993:+4.3 1994:+1.2 1995:+11.8 1996:+2.6 1997:+14.2 1998:+3.0 1999:+11.9 2000:+7.2 2001:-0.2 2002:+0.6 2003:+9.8 2004:-0.3 2005:+3.0 2006:-0.6 2007:+4.3 2008:-5.1 2009:+8.3 2010:+7.7 2011:-3.2 2012:+5.8 2013:+9.6 2014:-1.2 2015:+3.6 2016:+1.3 2017:+5.2 2018:-4.1 2019:+1.0 2020:-2.6 2021:+5.7 2022:-0.7 2023:+1.1 2024:+5.9
- kosten: bruto +655.4% | spread/commissie 40.4% | financiering -433.3% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 86% (6/7)
- G-benchmark (vehikel etf): regel SR +0.65, CAGR +5.6%, maxDD 12.9%, Calmar 0.43 | buy-and-hold (gelijk gewogen) SR +0.54, CAGR +9.6%, maxDD 54.3%, Calmar 0.18 → BETER (SR én maxDD)
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
