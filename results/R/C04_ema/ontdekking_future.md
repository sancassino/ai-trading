# C04_ema — EMA 50/200-kruising (FX-majors + goud), vol-geschaald (trend)
Mechanisme: Trendvolging op weken-horizon; onder-reactie op informatie.
Bron: klassieke MA-crossover; Neely e.a. (FX-technische regels)

## variant basis {} — vehikel future
- ontdekking ≤ 2024: 8841 dagen, 50201 positie-wijzigingen, netto +0.77 bp/dag, SR +0.31 (90%-CI +0.04…+0.60)
- t: dag +1.84 | Newey-West +1.81 | blok-bootstrap +1.85 | H1 +2.31 | H2 +0.24 | +50% spread (NW) +1.79
- skew -0.28 | max dagverlies 2.66% (P99 1.08%) | maxDD 18.5% (1× notional)
- corr: ORB -0.01, RSI2 +0.06 | SPX > SMA200: +0.90 bp/dag, daaronder +0.37
- per instrument t: FX_EURUSD +2.27, FX_GBPUSD +2.31, FX_USDJPY +1.63, FX_AUDUSD +2.22, FX_USDCAD +2.56, FX_USDCHF +0.44, GOLD_F +3.59
- per jaar (%): 1990:+1.0 1991:-2.2 1992:+8.8 1993:+1.1 1994:+5.7 1995:-7.8 1996:+5.0 1997:+4.1 1998:+4.7 1999:-0.4 2000:+4.0 2001:+0.1 2002:+8.0 2003:+19.8 2004:+4.0 2005:+2.3 2006:-1.2 2007:+6.9 2008:+6.2 2009:+1.3 2010:+3.4 2011:+3.0 2012:-7.0 2013:+5.6 2014:+7.9 2015:+5.0 2016:-6.6 2017:-7.8 2018:-3.7 2019:-0.3 2020:+4.7 2021:-7.2 2022:+8.6 2023:-4.2 2024:-4.7
- kosten: bruto +401.6% | spread/commissie 7.5% | financiering -450.4% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 71% (5/7)
- G-benchmark (vehikel future): regel SR +0.31, CAGR +4.5%, maxDD 18.5%, Calmar 0.24 | buy-and-hold (gelijk gewogen) SR +0.49, CAGR +4.8%, maxDD 14.6%, Calmar 0.33 → niet beter
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
