# rep_b2b_rsi2 — RSI(2)-dip boven SMA200 (replicatie B2b) (kortetermijn-omkeer)
Mechanisme: Liquiditeitsvoorziening na korte uitverkoop in een opwaartse trend; kopers worden betaald voor overnight-risico.
Bron: Connors & Alvarez (2008); eerder getest als B2b (t 3,65)

## variant basis {'entry': 10, 'exit': 70, 'sma': 200} — vehikel future
- ontdekking ≤ 2024: 9107 dagen, 2695 positie-wijzigingen, netto +1.21 bp/dag, SR +0.68 (90%-CI +0.44…+0.97)
- t: dag +4.10 | Newey-West +4.22 | blok-bootstrap +4.61 | H1 +3.56 | H2 +2.21 | +50% spread (NW) +4.18
- skew -0.88 | max dagverlies 3.75% (P99 0.91%) | maxDD 12.9% (1× notional)
- corr: ORB -0.02, RSI2 +0.75 | SPX > SMA200: +2.40 bp/dag, daaronder -2.26
- per instrument t: SPX +6.82, NDX +5.36, DAX +1.86, FTSE +5.40, N225 +2.49, GOLD_F +2.43
- per jaar (%): 1990:-8.2 1991:+4.1 1992:-1.3 1993:+4.6 1994:+1.3 1995:+12.0 1996:+2.8 1997:+14.5 1998:+3.2 1999:+12.1 2000:+7.3 2001:-0.2 2002:+0.6 2003:+9.9 2004:-0.2 2005:+3.2 2006:-0.4 2007:+4.4 2008:-5.1 2009:+8.5 2010:+7.9 2011:-3.1 2012:+6.0 2013:+9.8 2014:-1.1 2015:+3.8 2016:+1.4 2017:+5.4 2018:-4.0 2019:+1.1 2020:-2.4 2021:+5.9 2022:-0.6 2023:+1.3 2024:+6.1
- kosten: bruto +581.3% | spread/commissie 13.5% | financiering -509.7% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 100% (7/7)
- G-benchmark (vehikel future): regel SR +0.68, CAGR +5.7%, maxDD 12.9%, Calmar 0.44 | buy-and-hold (gelijk gewogen) SR +0.54, CAGR +9.7%, maxDD 54.2%, Calmar 0.18 → BETER (SR én maxDD)
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
