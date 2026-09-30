# C44_krediet — Krediet-signaal: HYG/IEF-ratio 3m-trend > 0 → SPY lang, anders kas (cross-asset)
Mechanisme: Kredietspreads leiden aandelen (informatie in obligatiemarkt); risk-off vroeg zichtbaar.
Bron: catalogus C44; Gilchrist–Zakrajšek (2012)

## variant basis {} — vehikel cfd
- ontdekking ≤ 2024: 4279 dagen, 45 positie-wijzigingen, netto +2.72 bp/dag, SR +0.57 (90%-CI +0.20…+0.95)
- t: dag +2.34 | Newey-West +2.44 | blok-bootstrap +2.59 | H1 +1.25 | H2 +2.06 | +50% spread (NW) +2.43
- skew -0.15 | max dagverlies 4.59% (P99 2.46%) | maxDD 27.8% (1× notional)
- corr: ORB -0.01, RSI2 +0.37 | SPX > SMA200: +5.22 bp/dag, daaronder -5.14
- per instrument t: SPY +2.34
- per jaar (%): 2008:-8.9 2009:+20.9 2010:+6.4 2011:+5.7 2012:+0.1 2013:+21.7 2014:+2.9 2015:+0.4 2016:+1.4 2017:+12.1 2018:-0.5 2019:+0.6 2020:+17.9 2021:+17.4 2022:-13.2 2023:+16.0 2024:+15.5
- kosten: bruto +168.5% | spread/commissie 0.2% | financiering +52.2% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 100% (3/3)
- G-benchmark (vehikel cfd): regel SR +0.57, CAGR +6.3%, maxDD 27.8%, Calmar 0.23 | buy-and-hold (gelijk gewogen) SR +0.36, CAGR +5.2%, maxDD 54.6%, Calmar 0.10 → BETER (SR én maxDD)
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
