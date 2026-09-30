# R2 — portefeuillebouw (ontdekking ≤ 2024-12-31; reserve niet aangeraakt)
Methode: zie r2_portfolio.py. Sleeve-reeksen = overschotrendement (x − rf) uit de engine per vehikel (etf/future). Hefboom (k>1) veronderstelt future/CFD-financiering tegen rf (in x al verwerkt via rf-aftrek; geen extra opslag → optimistisch bij k>1). Geen trial.

### P1: C54(qa) + C52(lang) + C02 + C17 (start 2001)
periode 2001-01-02 → 2024-12-31 (6041 dagen); sleeves: C54_carver__qa__future, C52_allweather__lang__etf, C02_faber__basis__etf, C17_fomc_cycle__basis__etf
correlatiematrix (overschotrendement, dagelijks):
```
C54_carver__qa__future             +1.00 +0.19 +0.38 -0.04
C52_allweather__lang__etf          +0.19 +1.00 +0.33 +0.30
C02_faber__basis__etf              +0.38 +0.33 +1.00 +0.53
C17_fomc_cycle__basis__etf         -0.04 +0.30 +0.53 +1.00
```
portefeuille (sleeves elk 10% vol → gemiddelde → 10% vol, cap 3.0×): SR 0.84, vol 10.9%, CAGR 10.7%, maxDD 15.6%, Calmar 0.69, skew -0.43; gem. hefboom 1.53
per jaar (%, overschot bij 10% vol): 2001:+2.7 2002:-3.3 2003:+38.7 2004:+13.9 2005:+10.7 2006:+12.1 2007:+6.6 2008:-6.1 2009:+13.2 2010:+20.2 2011:+0.2 2012:+15.2 2013:+21.2 2014:+7.6 2015:-4.1 2016:+4.3 2017:+25.7 2018:-3.5 2019:+18.6 2020:+17.6 2021:+4.4 2022:-15.7 2023:+12.5 2024:+6.2
SR per decennium: 2000s +0.93, 2010s +0.96, 2020s +0.46
benchmark 60/40 SPX/BOND10_SYN (ongeschaald, prijs/adj): SR 0.42, vol 11.1%, CAGR 5.9%, maxDD 32.6%, Calmar 0.18 | op 10% vol: SR 0.49, CAGR 6.6%, maxDD 23.8%, Calmar 0.28
benchmark SPX buy-and-hold (ongeschaald, prijs/adj): SR 0.33, vol 19.3%, CAGR 6.4%, maxDD 56.8%, Calmar 0.11 | op 10% vol: SR 0.36, CAGR 5.1%, maxDD 31.2%, Calmar 0.17

### P2: C54(qa) + C52(lang) (start 2001)
periode 2001-01-02 → 2024-12-31 (6041 dagen); sleeves: C54_carver__qa__future, C52_allweather__lang__etf
correlatiematrix (overschotrendement, dagelijks):
```
C54_carver__qa__future             +1.00 +0.19
C52_allweather__lang__etf          +0.19 +1.00
```
portefeuille (sleeves elk 10% vol → gemiddelde → 10% vol, cap 3.0×): SR 0.86, vol 10.8%, CAGR 10.9%, maxDD 18.9%, Calmar 0.58, skew -0.49; gem. hefboom 1.43
per jaar (%, overschot bij 10% vol): 2001:+3.0 2002:+9.1 2003:+23.7 2004:+11.8 2005:+9.0 2006:+14.3 2007:+8.8 2008:+3.3 2009:+7.0 2010:+23.9 2011:+13.7 2012:+6.2 2013:+8.1 2014:+13.0 2015:-6.0 2016:+9.8 2017:+18.0 2018:-3.0 2019:+21.0 2020:+30.2 2021:-1.2 2022:-15.9 2023:+5.5 2024:+9.7
SR per decennium: 2000s +0.92, 2010s +0.97, 2020s +0.52
benchmark 60/40 SPX/BOND10_SYN (ongeschaald, prijs/adj): SR 0.42, vol 11.1%, CAGR 5.9%, maxDD 32.6%, Calmar 0.18 | op 10% vol: SR 0.49, CAGR 6.6%, maxDD 23.8%, Calmar 0.28
benchmark SPX buy-and-hold (ongeschaald, prijs/adj): SR 0.33, vol 19.3%, CAGR 6.4%, maxDD 56.8%, Calmar 0.11 | op 10% vol: SR 0.36, CAGR 5.1%, maxDD 31.2%, Calmar 0.17

### P3: C54(qa) + C02 + C17 (start 1994)
periode 1994-01-03 → 2024-12-31 (8066 dagen); sleeves: C54_carver__qa__future, C02_faber__basis__etf, C17_fomc_cycle__basis__etf
correlatiematrix (overschotrendement, dagelijks):
```
C54_carver__qa__future             +1.00 +0.42 +0.01
C02_faber__basis__etf              +0.42 +1.00 +0.56
C17_fomc_cycle__basis__etf         +0.01 +0.56 +1.00
```
portefeuille (sleeves elk 10% vol → gemiddelde → 10% vol, cap 3.0×): SR 0.81, vol 10.9%, CAGR 11.1%, maxDD 18.1%, Calmar 0.62, skew -0.35; gem. hefboom 1.43
per jaar (%, overschot bij 10% vol): 1994:-7.9 1995:+18.7 1996:+10.2 1997:+15.8 1998:+24.8 1999:+22.0 2000:-9.7 2001:+7.8 2002:-9.8 2003:+43.0 2004:+13.0 2005:+15.1 2006:+10.0 2007:+6.0 2008:-1.9 2009:+13.0 2010:+13.3 2011:-7.9 2012:+18.9 2013:+31.5 2014:+2.8 2015:+0.2 2016:-0.9 2017:+19.8 2018:-2.2 2019:+8.1 2020:+9.7 2021:+6.7 2022:-5.4 2023:+10.1 2024:+7.9
SR per decennium: 1990s +1.27, 2000s +0.79, 2010s +0.72, 2020s +0.51
benchmark 60/40 SPX/BOND10_SYN (ongeschaald, prijs/adj): SR 0.48, vol 10.8%, CAGR 7.2%, maxDD 32.6%, Calmar 0.22 | op 10% vol: SR 0.54, CAGR 7.8%, maxDD 25.5%, Calmar 0.31
benchmark SPX buy-and-hold (ongeschaald, prijs/adj): SR 0.40, vol 18.3%, CAGR 8.2%, maxDD 56.8%, Calmar 0.15 | op 10% vol: SR 0.46, CAGR 6.9%, maxDD 28.6%, Calmar 0.24

### P4: alle sleeves incl. GEM/RSI(2) (start 2003)
periode 2003-01-02 → 2024-12-31 (5537 dagen); sleeves: C54_carver__qa__future, C52_allweather__basis__etf, C53_gem__basis__etf, C02_faber__basis__etf, C17_fomc_cycle__basis__etf, rep_b2b_rsi2__basis__etf
correlatiematrix (overschotrendement, dagelijks):
```
C54_carver__qa__future             +1.00 +0.14 +0.25 +0.41 +0.04 +0.25
C52_allweather__basis__etf         +0.14 +1.00 +0.49 +0.39 +0.35 +0.30
C53_gem__basis__etf                +0.25 +0.49 +1.00 +0.71 +0.49 +0.45
C02_faber__basis__etf              +0.41 +0.39 +0.71 +1.00 +0.57 +0.57
C17_fomc_cycle__basis__etf         +0.04 +0.35 +0.49 +0.57 +1.00 +0.35
rep_b2b_rsi2__basis__etf           +0.25 +0.30 +0.45 +0.57 +0.35 +1.00
```
portefeuille (sleeves elk 10% vol → gemiddelde → 10% vol, cap 3.0×): SR 0.84, vol 11.0%, CAGR 10.7%, maxDD 17.0%, Calmar 0.63, skew -0.51; gem. hefboom 1.52
per jaar (%, overschot bij 10% vol): 2003:+39.6 2004:+15.7 2005:+10.8 2006:+12.1 2007:+4.4 2008:-4.8 2009:+15.6 2010:+17.2 2011:-6.0 2012:+16.1 2013:+21.4 2014:+1.0 2015:-5.4 2016:+2.2 2017:+27.4 2018:-6.3 2019:+16.6 2020:+12.7 2021:+10.2 2022:-14.8 2023:+8.0 2024:+9.5
SR per decennium: 2000s +1.24, 2010s +0.75, 2020s +0.46
benchmark 60/40 SPY/IEF (ongeschaald, prijs/adj): SR 0.67, vol 10.7%, CAGR 8.5%, maxDD 31.4%, Calmar 0.27 | op 10% vol: SR 0.77, CAGR 9.8%, maxDD 21.1%, Calmar 0.46
benchmark SPX buy-and-hold (ongeschaald, prijs/adj): SR 0.47, vol 18.8%, CAGR 9.0%, maxDD 56.8%, Calmar 0.16 | op 10% vol: SR 0.53, CAGR 7.0%, maxDD 23.5%, Calmar 0.30
