# NEXT_STEPS / BACKLOG — supervisor, 2026-09-29 22:55 Amsterdam

Lees eerst `COORDINATION.md`. Sandro wil doorgaan en hogere doorloopsnelheid. Werk de backlog af **in volgorde**, push na elke taak, wacht niet op mij.

## Gap-analyse: wat ontbrak in de tests tot nu toe
1. **Te weinig onafhankelijke waarnemingen.** Momentum/trend/carry-tests hadden 26–27 jaaruitkomsten per test; Sharpe-standaardfout ≈ 0,2 → we kunnen alleen "geen groot effect" concluderen. Voor een edge die het doel haalt (Sharpe ≳1,5) is **hoge frequentie/breedte** nodig: honderden onafhankelijke trades per jaar (dan is 5 jaar MT5-data statistisch wél genoeg). Alles tot nu toe was laagfrequent (maandelijkse rebalans).
2. **Marktbeta maskeert de factor.** Long-only top-K: bottom-K was ook positief (bevinding uit eerdere test), SPY b&h evenaart het resultaat. Een **dollar-neutrale long/short**-versie is nooit getest; daarmee is het factoreffect zuiver meetbaar.
3. **Geen multiple-testing-correctie.** We hebben tientallen–honderden varianten getest en kozen achteraf. Geen gedeflateerde Sharpe, geen trial-teller.
4. **Geen zelfstandige economie-check.** Nooit doorgerekend wat een Sharpe/vol-niveau oplevert per FTMO-challenge (kosten, slaagkans, uitbetaling).
5. **Kostenmodel te grof voor kortere horizons.** Spread/commissie/swap per instrument uit echte FTMO-specs is nodig zodra we intraday gaan.
6. **MT5 is gebruikt als zoekmachine** (traag → 2–3 acties/dag). Python-screening ontbreekt als snelle eerste stap voor nieuwe families.

## BACKLOG (prioriteit 1 = eerst). Elke taak: pre-registratie → run → RUNLOG-entry → push.

**B1 (≤45 min) — `stats_tools.py` + TRIAL_COUNT.md.** Functies: Sharpe met standaardfout en betrouwbaarheidsinterval (block-bootstrap), gedeflateerde Sharpe (Bailey–López de Prado) met `n_trials`, t-stat, minimale trackrecordlengte. Pas retroactief toe op alle eerdere families (ronde 1 momentum-ensemble, T10, familie 1 en 2) met een eerlijke schatting van het aantal geteste varianten. Verwacht: alle "positieve" 2021–26-resultaten hebben gedeflateerde Sharpe ≈ 0 of negatief. Lever ook `required_sharpe(target_eur_per_month, account=80000, max_dd=0.10)`.

**B2 (≤2 u) — Dagfrequente edges op lange gratis data (Yahoo/Stooq, 1990–2026, indices ^GSPC ^NDX ^GDAXI ^FTSE ^N225 + goud), Python.** Pre-registreer vooraf, vaste literatuurparameters, GEEN grid: (a) IBS-reversal: long als IBS<0,2 (close-positie in dagrange), exit bij close>vorige high of na 5 dagen; (b) RSI(2)<10 met close>SMA200, exit RSI>70; (c) intraday-vs-overnight-splitsing: rendement open→close vs close→open per index, netto van kosten; (d) turn-of-month (laatste 1 + eerste 3 handelsdagen). Kosten: 0,02% spread/kant + financiering (DTB3 + 2% markup) alleen voor overnight-posities. Beslisregel: netto t-stat ≥ 3 over ≥25 jaar, positief in BEIDE helften (1995–2010 / 2011–2026), ≥ 300 trades, max DD < 15% bij positiegrootte 100% notional. Verwacht: (a)/(b) zwak positief maar verzwakt na 2015; (c) overnight-effect verdwijnt na financiering. Het gaat om te zien of er íets is met hoge breedte.

**B3 (≤2 u) — Dollar-neutrale long/short momentum op universum B (point-in-time top-10, `universe_pit_top10.csv`) en A (26 ETF's), 2000–2026.** Zelfde regels als ronde 1 (9 configs), maar long top-K / short bottom-K, gelijk kapitaal per been, vol-target 10%. Pre-registratie eerst. Verwacht: als momentum als factor bestaat is de long/short-Sharpe > 0,3 en niet gedreven door beta; als het ≈ 0 is, is momentum-familie definitief dood. Rapporteer ook correlatie met SPY.

**B4 (≤2 u, alleen data-export op VM, daarna Python) — Intraday op FTMO-data 2021–2026, hoge breedte.** Exporteer M5 (mt5_export_rates.py) voor US500, US100, US30, GER40, UK100, XAUUSD, EURUSD. Pre-registreer 3 literatuurstrategieën, één parameterset: (a) opening-range breakout (eerste 30 min, stop = andere kant, exit sessie-einde), (b) laatste-30-minuten-momentum (rendement eerste 30 min + rest van dag voorspelt laatste 30), (c) eerste-uur-reversal na gap >0,5%. Echte FTMO-spreads (M1-spread uit export) + commissie uit `swap_specs_FTMO.csv`/symbol_info. Rapporteer N trades, expectancy in R, t-stat, per jaar, train 2021–23 / test 2024–26. Beslisregel: t-stat ≥ 3 in train én test, N ≥ 500, expectancy na kosten > 0 per jaar in ≥ 4/6 jaren. Verwacht: kosten eten de meeste edge op indices; ORB werkt beter op goud/US100.

**B5 (≤1 u) — FTMO-economie.** Voor een PnL-dagreeks (input: csv): slaagkans fase 1/2 (10%/5%, 5% dag, 10% totaal, geen tijdslimiet), verwachte payout/maand bij 80% split, en break-even challenge-fee (parameter `FEE_EUR`, standaard 540 — controleer werkelijke fee voor €80k op ftmo.com). Draai op elk B2–B4-resultaat dat de beslisregel haalt.

**B6 (lopend) — Elke taak eindigt met** bijwerken van `TRIAL_COUNT.md` en een RUNLOG-entry. Gebruik `log_run.sh`.

## Beslisregels op portefeuilleniveau
- Slaagt ≥1 van B2/B3/B4 hun beslisregel → ik schrijf een vervolgopdracht (robuustheid, MT5-implementatie, correlatie tussen edges, combinatie).
- Slaagt niets → ik stel uiterlijk het volgende uur nieuwe families voor (bv. volatility risk premium/opties zijn niet handelbaar op FTMO; overweeg dan CFD-pairs/stat-arb tussen tickers in dezelfde sector, ADR-basis, earnings-drift).
