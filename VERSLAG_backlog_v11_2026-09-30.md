# Verslag BACKLOG v11 (Q1–Q5) + VOORSTEL H — 2026-09-30

**Kern: onder de echte FTMO-mechaniek levert geen enkel risiconiveau positief netto inkomen op met de gevonden edges; voor
€500 / €900 per maand is een Sharpe van ≈ 3 / ≈ 4 nodig. Alle nieuwe families (earnings, crypto, machine learning, flows)
zijn afgewezen. TRIAL_COUNT 404.**

| Taak | Uitkomst |
|---|---|
| Q1 inkomens-frontier (20.000 paden × 24 mnd, fees/herstarts, dagregel met meegedragen verlies) | RSI(2)+ORB: beste netto ≈ −€21/mnd; bij hogere schaal meer funded maar veel breuken en nieuwe fees (t = 3: 12,5 pogingen, −€160/mnd). Nul-/−50%-drift slechter. Benodigde edge: SR ≈ 3 → €507/mnd, SR ≈ 4 → €945/mnd. FTMO-voorwaarden geverifieerd (80% split, eerste reward vanaf dag 14, fee terug). |
| Q2 earnings-gaps (41 US-aandelen, yfinance-datums, FTMO-M5) | Bugfix sessietijden aandelen-CFD's (09:35-open vanaf 2024, uur-offset JPM). Continuatie +15,2 bp, t 1,35/0,91; fade t 1,08/−0,30 → afgewezen. |
| Q3 crypto intraday (BTC/ETH, geen overnight) | Bruto ≈ 0 vs kosten ≈ 8 bp → netto −7 bp, afgewezen. |
| Q4 machine learning (LightGBM, walk-forward + purging, 3 horizons) | OOS −0,66 / −1,16 / 0,00 bp per trade (t −3,7 / −3,8 / 0,0) → afgewezen; model vindt structuur kleiner dan de spread. |
| Q5 portefeuille | Geen nieuwe sleeves → = Q1 reeks A. |
| H1 maandeinde-herbalancering (SPY/TLT 2002–26) | +35,8 bp, t 2,76 (< 3), afnemend (2014–26 t 1,05) → afgewezen. |
| H2 pre-feestdag (1993–2026) | +7,9 bp, t 1,33 → afgewezen. |
| H3 RSI(2)-overnight bij VIX > 20 | Geen verbetering (t 1,58 vs ongefilterd 3,21) → afgewezen. |

Infrastructuur: `.venv` (numpy, scikit-learn, LightGBM, yfinance, pandas), FTMO-M5 voor 41 aandelen + BTC/ETH.
Niet gebruikt: SEC EDGAR (vereist contact-e-mail in User-Agent; Sandro's e-mail niet zonder toestemming gebruikt).
