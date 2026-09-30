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

## Update na MT5-bevestiging (F1–F3, 2026-09-29)
- F1 (RSI(2)-EA) en F2 (ORB-EA) reconciliëren uitstekend met Python (trades identiek resp. binnen 2%, maand-/tradecorrelatie 0,99).
- **F3 (combinatie op E3-schaal) faalt de beslisregel:** SR 0,96 (CI 0,22–1,66), ≈ €410/mnd, maar **FTMO-dagverlies tot 8,56%**
  (balance 00:00 − laagste equity; 5%-grens herhaaldelijk overschreden in jan 2022, mrt/apr 2025, mrt 2026) en dag-equity-DD 9,6%.
  Oorzaak: de RSI(2)-poot houdt meerdere gecorreleerde indexposities dagenlang vast; zwevend verlies stapelt tegen de middernacht-balance.
  De Python-schattingen (slot-tot-slot) misten dit.
- Diagnostiek (in-sample, geen beslisgrond): binnen FTMO-veilige grenzen (dag-DD < 8%, dagverlies < 4%) is het maximum
  ≈ **€330–365/mnd** (RSI ¼–½ van 1/6 per positie, ORB 1/7 per trade), SR ≈ 1,1.
- **Bijgesteld plafond: ≈ €250–365/mnd op €80k (Swing), vóór live-decay; kans op ≥ €880/mnd < 5%.**

## Update F1b/F1c/F3b (2026-09-30)
- FTMO-dagverliesregel geverifieerd (ftmo.com, trading objectives): limiet = balance om 00:00 CE(S)T − 5% van startkapitaal; floating telt mee.
- F1b: guard/cap-varianten voor RSI(2) alle afgewezen (SR ≤ 0,44 bij dagverlies < 4%).
- **F3b (schaal door dagverliesregel):** t = 0,45 → SR 0,95 (CI 0,23–1,65), dag-DD 4,4%, slechtste dag 3,80%, 5/6 jaar+
  → beslisregel 'kandidaat leeft' gehaald, maar **≈ €225/mnd** (+3,4%/jr). FTMO-economie: funded 17,5%, mediaan ~31 mnd
  tot fase 1, EV ≈ −€11/poging (nul-drift −€536).
- **Bijgesteld plafond onder FTMO-regels (MT5): ≈ €200–250/mnd; een challenge is met deze edge economisch niet zinvol
  (te traag om +10% te halen). Kans op ≥ €880/mnd: < 5%.**

## Update K1 (2026-09-30): waar zit de RSI(2)-edge?
Bijna volledig in de **nachten** (slot → volgende open), niet overdag: Yahoo nacht 1 +9,3 bp (t 4,2), nacht 2 +10,4 bp (t 4,3),
nacht 4+ +8,8 bp (t 5,0); dagsegmenten ≈ 0. FTMO idem maar zwakker (nacht 2 +11,4 bp, t 2,9). Varianten max 1 / max 2 nachten:
Yahoo t 3,05 / 3,59, FTMO t 1,79 / 1,53 → afgewezen op FTMO-t (te weinig power in 5,7 jaar), terwijl het dagverlies bij
€150/mnd-schaal beheersbaar is (2,8% / 3,6%). RSI(2) onder FTMO is dus geen schaalprobleem van nacht 3+, maar een kleine
overnight-premie die op de korte FTMO-historie statistisch niet hard te maken is.
