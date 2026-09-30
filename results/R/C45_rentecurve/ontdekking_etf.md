# C45_rentecurve — Rentecurve-regime: (10j − 3m) > 0 → SPX lang, anders kas (cross-asset)
Mechanisme: Omgekeerde curve voorspelt recessie; risicopremie-timing. (T10Y2Y niet beschikbaar → 10j − 3m uit TNX/IRX.)
Bron: catalogus C45; Estrella–Mishkin (1998)

## variant basis {} — vehikel etf
- ontdekking ≤ 2024: 15858 dagen, 35 positie-wijzigingen, netto +2.27 bp/dag, SR +0.38 (90%-CI +0.18…+0.58)
- t: dag +2.98 | Newey-West +3.06 | blok-bootstrap +3.26 | H1 +1.40 | H2 +2.69 | +50% spread (NW) +3.05
- skew -0.67 | max dagverlies 20.52% (P99 2.65%) | maxDD 55.3% (1× notional)
- corr: ORB -0.03, RSI2 +0.27 | SPX > SMA200: +6.59 bp/dag, daaronder -8.09
- per instrument t: SPX +5.31
- per jaar (%): 1962:-10.0 1963:+14.4 1964:+8.7 1965:+4.9 1966:-22.0 1967:+7.1 1968:+2.3 1969:-5.7 1970:-1.4 1971:+6.4 1972:+10.7 1973:-15.1 1974:-6.3 1975:+22.8 1976:+13.1 1977:-17.1 1978:-6.3 1979:+0.0 1980:+13.9 1981:-1.1 1982:+4.8 1983:+8.2 1984:-7.4 1985:+16.4 1986:+8.7 1987:+1.7 1988:+10.1 1989:+21.3 1990:-9.5 1991:+22.2 1992:+4.3 1993:+6.9 1994:-2.5 1995:+26.7 1996:+16.3 1997:+25.3 1998:+22.4 1999:+16.0 2000:+1.8 2001:-17.2 2002:-23.3 2003:+25.6 2004:+9.5 2005:+2.1 2006:+2.8 2007:-6.0 2008:-39.2 2009:+27.0 2010:+15.5 2011:+4.7 2012:+15.5 2013:+28.6 2014:+13.4 2015:+2.4 2016:+11.8 2017:+19.0 2018:-5.1 2019:+15.7 2020:+31.8 2021:+26.0 2022:-13.1 2023:+0.0 2024:-0.1
- kosten: bruto +584.0% | spread/commissie 2.3% | financiering -57.9% (som over instrument-dagen) → kostenpoort (bruto ≥ 3× spread/commissie) DOOR
- 5-jaarsvensters positief: 83% (10/12)
- G-benchmark (vehikel etf): regel SR +0.38, CAGR +9.4%, maxDD 55.3%, Calmar 0.17 | buy-and-hold (gelijk gewogen) SR +0.31, CAGR +8.5%, maxDD 55.3%, Calmar 0.15 → niet beter
- beslissing: door G-ontdekking (poort; min(NW, bootstrap) ≥ 3; H1, H2 > 0; SR ≥ 0,3; ≥ 60% 5j-vensters +; N ≥ 500 of lage omloop)
