# NEXT_STEPS / BACKLOG v3 — supervisor, 2026-09-30 00:17 Amsterdam

Sandro heeft gekozen om **door te gaan** (geen stop). De pauze uit je PLAFOND_RAPPORT vervalt: er is één kandidaat met een kleine, mogelijk echte edge (RSI(2)+ORB, Swing, SR 0,98 ± 0,42, ≈ €480/mnd, DD 7,8%). Het doel blijft €880+, maar de eerlijke route is nu: (1) kandidaat hard bevestigen in MT5 en op een demo-forward-test, (2) breedte vergroten met **identieke** regels. Zelfde discipline: PREREG vóór resultaat, TRIAL_COUNT bijwerken, push na elke taak, nooit wachten.

## Beoordeling (kritisch)
- Sterk werk: 348 trials geteld, D3 terecht 'niet uitvoerbaar', E1-replicatie op FTMO-data, PLAFOND_RAPPORT eerlijk. Mijn schatting live: SR 0,5–0,7 → €250–350/mnd (Swing) — akkoord.
- Zwaktes van de kandidaat (repareren via F1–F5): (a) sleeve-selectie (t ≥ 2,5) gebeurde ná het zien van B2/B4-resultaten → optimistisch; (b) de combinatie leunt op 5,2 jaar en 2022; (c) ORB test-t slechts 1,14 en 1,7 bp/trade — extreem kosten-/slippagegevoelig; (d) RSI(2) op FTMO zwakker dan Yahoo (t 1,39 vs 3,65; UK100/XAU ≈ 0) — mogelijk decay na 2010; (e) alleen Python — nog geen MT5-bevestiging met echte fills/swaps/rollover; (f) schaal 2,35–3,6× = hefboom; slippage bij drukte niet gemodelleerd.
- B5/C7-EV-loterij blijft **niet** het doel (FTMO-risico's); MT5-bevestiging moet werken op regels en drawdown, niet op optiewaarde.

## BACKLOG (prioriteit 1 = eerst)

**F1 — MT5-EA RSI(2) (D1) + reconciliatie.** EA met exact de E1-regels (6 FTMO-symbolen, long-only, vaste regels, Swing: weekend toegestaan), Strategy Tester Model=1, €80k EUR, 2021-01..2026-09, échte swaps/spreads. Reconcile met Python e1-sim: maandcorrelatie ≥ 0,9, totaalrendement binnen 25%, trade-aantal binnen 10%. Wijkt het meer af: zoek de oorzaak (fill-tijdstip, spread, swap-triple-day) en rapporteer; corrigeer het Python-model of de EA.

**F2 — MT5-EA ORB (M5) + reconciliatie.** Exact B4a-regels, 7 symbolen. Reconcile met b4-sim: N trades binnen 10%, gemiddelde bp/trade binnen 0,7 bp, per-jaar-teken gelijk. Verwachting: MT5-kosten (spread bij open, slippage) drukken ORB verder; als bp/trade ≤ 0 → ORB-poot afgewezen en combinatie herberekenen zonder ORB (rapporteer dat expliciet).

**F3 — MT5 gecombineerd, één account €80k (schaal/gewichten vastgezet uit E3, niet opnieuw fitten).** Beide EA's samen, dagelijkse equity-/balance-log (`*_daily.csv`), FTMO-regels op equity (dagverlies = balance 00:00 CE(S)T − 5%, totaal 10%): analyze_daily.py + ftmo_economics.py (nu mét intraday-dips). Beslisregel voor 'kandidaat blijft leven': MT5-SR ≥ 0,6, max dag-equity-DD < 8%, slechtste dagverlies < 4%, ≥ 4/6 jaar positief. Rapporteer €/mnd op €80k, funded-kans, en bootstrap-CI.

**F4 — Plateau- en decay-check (GEEN selectie op P&L).** (a) RSI(2) Yahoo 1990–2026: rollende 5-jaars-Sharpe per index, trend na 2010; (b) drempels 5/10/15 en SMA150/200/250 als plateaukaart (verwacht gelijke teken); (c) ORB opening-range 15/30/60 min en exit 12:00/sessie-einde als plateaukaart, per symbool. Conclusie alleen: is de edge een plateau of een piek? Eis: ≥ 2/3 van de buren zelfde teken en ≥ 50% van het niveau. Niet 'beste' kiezen.

**F5 — Breedte met IDENTIEKE regels (pre-registreer, elk telt in TRIAL_COUNT).** RSI(2)- en ORB-regels ongewijzigd op extra FTMO-indices/goud (JP225, AUS200, HK50, EU50, FRA40, SPN35, N25, XAGUSD) en IBS<0,2 op US100/US500 als derde sleeve. Doel: vaststellen of extra breedte de gecombineerde SR verhoogt (verwacht: meer instrumenten = lagere vol per sleeve, SR +0,1–0,2 bij lage correlatie). Beslisregel: opnemen alleen als sleeve t ≥ 2 op FTMO-data én correlatie < 0,5 met bestaande én zelfde teken in beide helften; herbereken dan combinatie-DSR.

**F6 — Forward-test op FTMO-DEMO (€80k) — geen echt geld.** Zet de F3-EA's live op de demo-terminal op de VM (alleen demo!), logt dagelijks balance/equity/trades naar `forward/daily.csv` in de repo (push elke dag). Dit is de enige echte out-of-sample. Verwachting bij SR 0,6: ± €300/mnd maar zeer ruisig; pas na ≥ 60 handelsdagen conclusies. Voorwaarde: F1–F3 niet ernstig afwijkend (F3 beslisregel gehaald).

## Reserve (als F1–F6 klaar)
G1 kostengevoeligheid: herbereken combinatie met +50% spread en 1 pip extra slippage per ORB-trade; G2 correlatie combinatie met SPY-beta en rolling correlatie in stressmaanden (2022, 2025-04); G3 nieuwe hypothese-batch (`VOORSTEL_F.md`, 3 stuks, pre-registratie) in de stijl van wat werkte: kortetermijn-omkeer op dagbasis + intraday-breakout, geen carry/momentum/trend.

## Portefeuilleregel
Slaagt F3 (MT5) en blijft de combinatie SR ≥ 0,6 → ik schrijf het plan voor een echte challenge-poging (zonder loterijconstructie) en de risicoparameters. Faalt F1–F3 → PLAFOND_RAPPORT wordt aangepast naar wat MT5 laat zien en ik stel nieuwe families voor.
