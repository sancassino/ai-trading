# C44_krediet — Krediet-signaal: HYG/IEF-ratio 3m-trend > 0 → SPY lang, anders kas (cross-asset)
Mechanisme: Kredietspreads leiden aandelen (informatie in obligatiemarkt); risk-off vroeg zichtbaar.
Bron: catalogus C44; Gilchrist–Zakrajšek (2012)

## variant basis {} — vehikel etf
- ontdekking ≤ 2024: 4279 dagen, 45 positie-wijzigingen, netto +3.54 bp/dag, SR +0.74 (90%-CI +0.37…+1.13)
- t: dag +3.06 | Newey-West +3.17 | blok-bootstrap +3.37 | H1 +1.84 | H2 +2.48 | +50% spread (NW) +3.14
- skew -0.12 | max dagverlies 4.58% (P99 2.45%) | maxDD 26.6% (1× notional)
- corr: ORB -0.01, RSI2 +0.37 | SPX > SMA200: +6.21 bp/dag, daaronder -4.80
- per instrument t: SPY +3.46
- per jaar (%): 2008:-8.2 2009:+24.7 2010:+9.4 2011:+7.5 2012:+3.1 2013:+26.0 2014:+4.8 2015:+1.4 2016:+4.7 2017:+14.8 2018:+2.0 2019:+1.3 2020:+20.4 2021:+20.4 2022:-11.5 2023:+15.6 2024:+15.3
- kosten: bruto +168.5% | spread/commissie 2.9% | financiering -5.8% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 100% (3/3)
- G-benchmark (vehikel etf): regel SR +0.74, CAGR +9.8%, maxDD 26.6%, Calmar 0.37 | buy-and-hold (gelijk gewogen) SR +0.54, CAGR +10.5%, maxDD 51.9%, Calmar 0.20 → BETER (SR én maxDD)
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
