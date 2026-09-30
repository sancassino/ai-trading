# C60_bondtiming — Obligatie-duurtiming: synthetische 10j-Treasury long als maandeindslot > gem. 10 maandeinden, anders kas (trend)
Mechanisme: Rente-trends (persistentie van inflatie/beleid); lage of negatieve correlatie met aandelen.
Bron: Faber (2007); Hurst–Ooi–Pedersen; catalogus C60 (test 1970–2000)

## variant basis {} — vehikel etf
- ontdekking ≤ 2024: 15488 dagen, 111 positie-wijzigingen, netto +0.68 bp/dag, SR +0.26 (90%-CI +0.02…+0.50)
- t: dag +2.06 | Newey-West +1.94 | blok-bootstrap +1.77 | H1 +1.19 | H2 +1.77 | +50% spread (NW) +1.87
- skew +0.32 | max dagverlies 3.44% (P99 1.24%) | maxDD 16.1% (1× notional)
- corr: ORB +0.03, RSI2 -0.03 | SPX > SMA200: +0.20 bp/dag, daaronder +1.84
- per instrument t: BOND10_SYN +7.50
- per jaar (%): 1963:-1.5 1964:+0.0 1965:-3.3 1966:+0.7 1967:-4.4 1968:-5.1 1969:+0.0 1970:+2.8 1971:+2.0 1972:-2.6 1973:-4.6 1974:-1.2 1975:-7.9 1976:+10.3 1977:-5.6 1978:-8.2 1979:-16.8 1980:-7.3 1981:+6.2 1982:+33.1 1983:-13.3 1984:+7.2 1985:+24.3 1986:+16.6 1987:-7.2 1988:-3.3 1989:+10.3 1990:-0.6 1991:+13.6 1992:+3.9 1993:+10.4 1994:-2.5 1995:+17.2 1996:-3.1 1997:+4.9 1998:+9.5 1999:-5.0 2000:+7.3 2001:+2.7 2002:+10.1 2003:-6.2 2004:+0.9 2005:-4.4 2006:+1.0 2007:+4.7 2008:+17.3 2009:-11.5 2010:+3.2 2011:+11.0 2012:+2.8 2013:-5.6 2014:+6.0 2015:-1.5 2016:+1.8 2017:-1.3 2018:-1.6 2019:+6.3 2020:+9.1 2021:-2.7 2022:-2.1 2023:-4.3 2024:-7.7
- kosten: bruto +301.8% | spread/commissie 7.2% | financiering -87.1% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 58% (7/12)
- G-benchmark (vehikel etf): regel SR +0.26, CAGR +6.2%, maxDD 16.1%, Calmar 0.38 | buy-and-hold (gelijk gewogen) SR +0.20, CAGR +6.0%, maxDD 28.7%, Calmar 0.21 → BETER (SR én maxDD)
- beslissing: afgewezen (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
