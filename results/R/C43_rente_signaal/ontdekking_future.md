# C43_rente_signaal — Rente-signaal: 10j-rente 3m stijgend → index kort, dalend → lang (cross-asset)
Mechanisme: Hogere discontovoet drukt aandelenwaarderingen; rente-momentum leidt aandelen.
Bron: catalogus C43; Fama–Schwert (1977) rente en aandelenrendement

## variant basis {} — vehikel future
- ontdekking ≤ 2024: 10307 dagen, 327 positie-wijzigingen, netto +1.19 bp/dag, SR +0.16 (90%-CI -0.12…+0.40)
- t: dag +1.01 | Newey-West +1.01 | blok-bootstrap +1.01 | H1 +0.89 | H2 +0.54 | +50% spread (NW) +1.00
- skew +0.29 | max dagverlies 10.34% (P99 3.29%) | maxDD 71.8% (1× notional)
- corr: ORB +0.00, RSI2 -0.19 | SPX > SMA200: +1.39 bp/dag, daaronder +1.18
- per instrument t: SPX +1.93, NDX +1.75, DAX +1.22
- per jaar (%): 1985:+9.2 1986:+0.2 1987:+53.9 1988:-5.4 1989:+3.0 1990:-23.5 1991:+21.1 1992:-4.9 1993:+4.6 1994:+4.6 1995:+20.4 1996:+6.4 1997:+5.1 1998:+37.9 1999:-43.9 2000:-38.5 2001:-17.9 2002:+39.9 2003:+2.5 2004:+1.3 2005:+1.4 2006:+14.0 2007:+11.8 2008:-33.3 2009:-27.0 2010:+6.5 2011:-21.6 2012:+24.3 2013:-10.4 2014:+9.6 2015:+26.3 2016:+20.5 2017:-0.1 2018:+12.6 2019:+22.0 2020:+7.6 2021:-22.7 2022:+14.2 2023:-12.3 2024:+3.3
- kosten: bruto +315.2% | spread/commissie 3.2% | financiering -356.1% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 62% (5/8)
- G-benchmark (vehikel future): regel SR +0.16, CAGR +4.4%, maxDD 71.8%, Calmar 0.06 | buy-and-hold (gelijk gewogen) SR +0.58, CAGR +13.0%, maxDD 69.6%, Calmar 0.19 → niet beter
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
