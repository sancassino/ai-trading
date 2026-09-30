# C55_daa — Defensive asset allocation (Keller): canary EEM + AGG, top-6 van 10 risicoactiva, kas = SHY (momentum/allocatie)
Mechanisme: Breedte-momentum (canary) als crash-filter: beide canaries positief → volledig risico, één → half, geen → kas.
Bron: Keller & Keuning (2018) DAA

## variant basis {} — vehikel etf
- ontdekking ≤ 2024: 5033 dagen, 1203 positie-wijzigingen, netto +2.41 bp/dag, SR +0.63 (90%-CI +0.35…+0.95)
- t: dag +2.84 | Newey-West +3.05 | blok-bootstrap +3.48 | H1 +2.65 | H2 +1.11 | +50% spread (NW) +2.89
- skew -0.23 | max dagverlies 4.65% (P99 1.87%) | maxDD 13.8% (1× notional)
- corr: ORB -0.01, RSI2 +0.38 | SPX > SMA200: +3.53 bp/dag, daaronder -1.45
- per instrument t: SPY +3.48, IWM +1.97, EFA +2.14, EEM +2.36, VNQ +1.67, DBC +0.89, GLD +2.28, TLT +0.68, LQD +1.80, HYG +1.74, AGG +nan, SHY +1.78
- per jaar (%): 2005:+6.0 2006:+15.6 2007:+11.0 2008:+2.6 2009:+28.2 2010:+8.4 2011:+5.0 2012:+8.1 2013:+9.1 2014:+2.7 2015:-3.0 2016:+3.4 2017:+9.7 2018:+0.2 2019:+6.2 2020:+12.0 2021:+6.2 2022:-10.1 2023:-0.1 2024:+0.1
- kosten: bruto +167.2% | spread/commissie 12.4% | financiering +1.4% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 100% (4/4)
- G-benchmark (vehikel etf): regel SR +0.63, CAGR +7.5%, maxDD 13.8%, Calmar 0.54 | buy-and-hold (60/40 SPY/IEF) SR +0.60, CAGR +7.9%, maxDD 31.5%, Calmar 0.25 → BETER (SR én maxDD)
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
