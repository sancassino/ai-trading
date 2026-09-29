# PREREG B3 — dollar-neutrale long/short momentum (vastgelegd vóór berekening, 2026-09-29)

Doel: het momentum-factoreffect meten zonder marktbeta.

- Universums (ongewijzigd uit ronde 1): **A** = 26 ETF's (`universe_A_etf.txt`, GLD/SLV/USO gespliced
  met GC=F/SI=F/CL=F), **B** = point-in-time top-10 (`universe_pit_top10.csv`). Yahoo adjusted close.
- 9 configs: TopN K ∈ {2,3,4} × lookback ∈ {1,2,3} maanden (N×30 kalenderdagen), exact de
  ranking van ronde 1 (rendement t/m vorige slot, eerste handelsdag van de maand, uitvoering op slot).
- Portefeuille: long top-K (elk +1/K), short bottom-K (elk −1/K) → dollar-neutraal. **Geen
  regimefilter** (dat filter stuurt marktbeta; hier meten we de factor). Elke maand volledig
  herwogen. Vol-target 10%: schaal k = 0,10 / ex-ante vol (huidige gewichten × laatste 60
  dagrendementen), bruto hefboom ≤ 4.
- Kosten: spread 0,05% per kant over verhandelde notional; financiering CFD-stijl: long betaalt
  DTB3 + 2%/jr, short ontvangt DTB3 − 2%/jr (per kalenderdag).
- Periode 2000-01-01 t/m 2026-09-21. Instrumenten stromen in zodra lookback-historie beschikbaar is.
- Rapportage per config en per universum-ensemble (gemiddelde dagrendementen van de 9): netto CAGR,
  vol, Sharpe, t-stat, max DD, % jaren+, helften 2000–2012 / 2013–2026, **correlatie met SPY**
  (dagrendementen), DSR (N = 323 en 53).
- **Beslisregel:** momentum bestaat als factor als het ensemble in **beide** universums netto
  Sharpe ≥ 0,3 heeft, positief in beide helften, en |correlatie met SPY| < 0,3. Anders: de
  momentum-familie is definitief dood.
- Trials: +18 (9 configs × 2 universums) → TRIAL_COUNT 323.
