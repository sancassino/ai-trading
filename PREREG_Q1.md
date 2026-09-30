# PREREG Q1 — inkomens-frontier onder FTMO-regels (vastgelegd vóór berekening, 2026-09-30)

## FTMO-regels (geciteerd/geverifieerd op ftmo.com, 30-09-2026)
- 2-Step: fase 1 +10%, fase 2 +5%, min. 4 handelsdagen, dagverlies: equity ≥ balance(00:00 CE(S)T) − 5% van startkapitaal,
  max. verlies statisch 10% (trading-objectives).
- Profit split 2-Step **80%** (90% met Scaling Plan/Premium; niet gemodelleerd). Eerste reward-aanvraag vanaf de **14e dag** na
  de eerste trade, posities gesloten (faq/how-do-i-withdraw-my-profits). Fee **100% terug** bij de eerste reward (how-it-works).
- Fee €80k 2-Step: **€540** (secundaire bronnen; niet op ftmo.com vindbaar in leesbare vorm).
- Geen gokgedrag: vaste, consistente positiegrootte per scenario, geen martingale/grid, geen HFT.

## Model
- Reeksen (MT5-dagequity, 2021-09..2026-09): A = F3b (RSI(2)+ORB, schaal t = 1 ≙ F3b-grootte), B = RSI(2) oorspronkelijk
  (F1, t = 1 ≙ 1/6 per positie). Per dag: rendement r = eind/vorige-eind − 1 en dagverlies d = (dagstart-balance − min-equity)/80.000
  (bevat meegedragen zwevend verlies = intraday-dip-realisme). Schaal t: r·t en d·t.
- Schalen t ∈ {0,3; 0,5; 0,75; 1; 1,5; 2; 2,5; 3}. Block-bootstrap blokken van 21 dagen, **20.000 paden** per (reeks, schaal, variant),
  horizon **24 maanden** (504 handelsdagen).
- Beleid per pad: fee betalen → fase 1 → fase 2 → funded. Breuk (dagverlies ≥ 5% of equity − dip ≤ 90%) in welke fase dan ook →
  nieuwe fee, opnieuw fase 1. Funded: elke 21 handelsdagen (≥ 14 dagen) winst boven start uitbetalen × 80%, saldo terug naar start;
  bij de eerste uitbetaling per funded account de fee terug.
- Rapport per schaal: P(fase 1+2 binnen 24 mnd), P(breuk binnen 12 mnd na funded), verwacht **netto** €/mnd over 24 mnd
  (uitbetalingen + terugbetaalde fees − betaalde fees), mediane tijd tot eerste uitbetaling, gemiddeld aantal pogingen,
  P(netto < 0 na 24 mnd).
- Controles: **nul-drift** (r − gemiddelde r) en **−50%-drift** (r − 0,5 × gemiddelde r).
- Doel: bij welk risiconiveau is verwacht netto inkomen ≈ €500 / €800 / €900 per maand, en wat is dan de kans op feeverlies.
