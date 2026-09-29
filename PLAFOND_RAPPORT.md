# PLAFOND_RAPPORT — wat is maximaal haalbaar onder FTMO-regels? (2026-09-29)

Opgesteld volgens de portefeuille-beslisregel in NEXT_STEPS (backlog v2): na C1–C6 (+ reserve D1–D4 en validatie E1/E3)
haalt geen enkele **op FTMO-data gevalideerde** sleeve of combinatie een gedeflateerde Sharpe ≥ 0,5.
Totaal ≈ 348 geteste varianten (TRIAL_COUNT.md), alle met pre-registratie sinds ronde 2.

## Beste kandidaat
**RSI(2)-mean-reversion (6 FTMO-indices/goud, gepoold) + opening-range-breakout (7 FTMO-symbolen), gelijk risico.**
Gewichten en schaal vastgezet op 2021-09..2023, ongewijzigd toegepast op 2024–2026 (E3, FTMO-data, FTMO-kosten).

| Account-type | Sharpe (2021-09..2026) | ≈ €/mnd op €80k | Max DD | Slechtste dag | Test 2024–26 |
|---|---|---|---|---|---|
| **Swing** (weekend/nieuws toegestaan) | 0,98 (± 0,42; bootstrap-CI 0,34–1,66) | **≈ €480** | 7,8% | −3,0% | SR 0,99, ≈ €519/mnd |
| Standard (vrijdag sluiten) | 0,64 (± 0,42) | ≈ €230 | 7,9% | −2,4% | SR 0,53, ≈ €201/mnd |

- Benodigde Sharpe voor €880/mnd bij max 10% verlies (kans ≤ 5%): **1,41** (stats_tools.required_sharpe).
- Kans dat de ware Sharpe ≥ 1,41, **vóór** correctie voor ~348 pogingen: ≈ 16%. Gedeflateerde Sharpe (N = 348): **0,27**
  (= kans dat de ware Sharpe zelfs maar > 0 is, na correctie, ≈ 27%).
- Gebruikelijke daling backtest → live (30–50%) → verwacht live-niveau ≈ Sharpe 0,5–0,7 → **≈ €250–350/mnd** (Swing).

## Plafond (eerlijke inschatting)
- **Maximaal haalbaar onder FTMO-regels met wat nu getest is: ≈ €250–500/mnd op €80k (Swing), met grote onzekerheid;
  Standard-account ≈ €100–250/mnd.**
- **Kans op duurzaam ≥ €880/mnd: < 10%** (na correctie voor multiple testing eerder ≈ 5%).
- FTMO-EV per challenge-poging (Python, slot-tot-slot, optimistisch): Swing €4.142 vs nul-drift-controle −€93 →
  er lijkt een kleine echte edge in te zitten, maar de schatting rust op 5,2 jaar.

## Wat is uitgesloten (samenvatting)
Momentum-rotatie (lang, L/S, alle universums), tijdreeks-trend, FX-carry, pairs/stat-arb, kortetermijn-omkeer,
lead-lag, tijdvensters, FX-intradagseizoen, goud vs reële rente, crypto-trend (FTMO-swap −30%/jr), vol-timing,
risicopariteit (geen obligatie-CFD's), IBS, turn-of-month, intraday/overnight-splitsing, laatste-30-min, gap-reversal.
Structureel bij FTMO: swaps op aandelen-CFD's (long −8%, short −7%/jr), crypto −30%/jr, geen obligaties/futures.

## Beslispunt voor Sandro
1. **Doel verlagen** naar ≈ €250–500/mnd en de RSI(2)+ORB-combinatie in MT5 bevestigen op een Swing-account-opzet
   (C7-ontwerp, `PREREG_C7.md`), daarna eventueel één challenge als live-test; of
2. **stoppen** met dit onderzoek; of
3. een **fundamenteel andere bron van edge** aanleveren (eigen discretionaire regels, orderflow).
Advies uitvoerder: optie 1 alleen met het besef dat het doel €880+ met deze aanpak waarschijnlijk niet gehaald wordt.

De uitvoerder pauzeert nieuw onderzoek (portefeuilleregel) en blijft elk uur controleren op nieuwe NEXT_STEPS.
