# C55_daa — Defensive asset allocation (Keller): canary EEM + AGG, top-6 van 10 risicoactiva, kas = SHY (momentum/allocatie)
Mechanisme: Breedte-momentum (canary) als crash-filter: beide canaries positief → volledig risico, één → half, geen → kas.
Bron: Keller & Keuning (2018) DAA

## variant basis {} — vehikel cfd
- ontdekking ≤ 2024: 5033 dagen, 128 positie-wijzigingen, netto +0.35 bp/dag, SR +0.52 (90%-CI +0.20…+0.86)
- t: dag +2.33 | Newey-West +2.49 | blok-bootstrap +2.68 | H1 +1.68 | H2 +1.64 | +50% spread (NW) +2.49
- skew -0.38 | max dagverlies 0.74% (P99 0.35%) | maxDD 3.8% (1× notional)
- corr: ORB -0.03, RSI2 +0.48 | SPX > SMA200: +0.66 bp/dag, daaronder -0.72
- per instrument t: SPY +2.33, IWM +nan, EFA +nan, EEM +nan, VNQ +nan, DBC +nan, GLD +nan, TLT +nan, LQD +nan, HYG +nan, AGG +nan, SHY +nan
- per jaar (%): 2005:+0.0 2006:+1.4 2007:-0.1 2008:-2.0 2009:+3.6 2010:-0.3 2011:+1.1 2012:+1.5 2013:+3.3 2014:+1.2 2015:-0.3 2016:+0.3 2017:+1.9 2018:-0.5 2019:+1.4 2020:+3.0 2021:+1.3 2022:-1.4 2023:+0.6 2024:+1.5
- kosten: bruto +27.2% | spread/commissie 0.1% | financiering +9.6% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 100% (4/4)
- G-benchmark (vehikel cfd): regel SR +0.52, CAGR +0.9%, maxDD 3.8%, Calmar 0.23 | buy-and-hold (60/40 SPY/IEF) SR +0.35, CAGR +3.4%, maxDD 39.3%, Calmar 0.09 → BETER (SR én maxDD)
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
