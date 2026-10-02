# PREREG_FTMO_P1_ORB_BTC — portefeuille ORB (index) + BTC US-open (CEO, D-094 spoor 3b)

**Status:** Pre-registratie 2026-10-01 ~08:40 Europe/Amsterdam, branch `claude/ftmo-trading-strategy-98mplz`. Geen resultaat van deze exacte portefeuille gezien vóór deze commit.
**Waarom:** CTO C-018 en AUDIT_3 laten op papier SR ≈ 1,2 en ≈ €1.000/mnd zien voor ORB + BTC (ρ = 0,11). Maar beide benen zijn individueel zwak/onbevestigd (ORB t ≈ 1,8; BTC N = 132 < 150) en de papierwaarden zijn in-sample op train. Dit PREREG maakt er één bevroren hypothese van die op ongeziene data wordt getoetst.

## 1. Bevroren regel
- **Been A (ORB):** F2-ORB zoals bevroren in `results/f/` / B4a-simulator (US500, US100, GER40 cash; OR 30 min; stop OR-laag; flat sessie-einde). Geen parameter wijzigt.
- **Been B (BTC):** `PREREG_S2_BTC_USOPEN.md` ongewijzigd (BTCUSD, pre-range 14:30–15:30 AMS, entry 15:30–16:00, mid-stop, flat 21:00, 1 trade/dag, filter |US100-gap| ≥ 0,15% gelijkteken).
- **Weging:** gelijke dagelijkse volatiliteit; de twee schaalconstanten worden eenmalig vastgelegd uit train 2021-01 → 2023-12 en daarna **niet meer herschat**. Sizing (`recommend_scale`) idem uit train; max dagverlies ≤ 4% van initieel.
- **Geen** derde been, geen filter, geen herweging na resultaten.

## 2. Toetsfasen (strikt in volgorde)
1. **Stap 1 — Power BTC:** S2-BTC op 2021–2024-12 (kostenpoort + stress) zodat N ≥ 150 mogelijk is. Faalt de poort of N < 150 → portefeuille STOP (geen trial).
2. **Stap 2 — Reserve-run, één keer:** CEO geeft de reserve 2025-01-01 → heden vrij **uitsluitend voor deze portefeuille** (D-084, per kandidaat). De portefeuille loopt in één run over de reserve met de bevroren constanten. Geen tweede blik.
3. **Stap 3 — Forward-papier:** vanaf deze commit loopt dagelijks papier met de bevroren regel (Uitvoerder-1 / CTO), als aanvullend bewijs.

## 3. Beslisregel (reserve, gecombineerde dagreeks na kosten)
PASS alleen als **alle** gelden:
- netto gemiddelde > 0 en dag-geclusterd t ≥ 2,0 (eenzijdig) over de reserve;
- jaarlijkse SR(reserve) ≥ 0,8;
- `ftmo_ev()` op de reserve-reeks: p_pass_1·p_pass_2 ≥ 0,35, net EV > 0, ook bij +50% spread-/kostenstress;
- elk been apart netto-gemiddelde ≥ 0 (geen been dat de ander draagt);
- **Auditor onafhankelijk herberekent** en geeft PASS.

Bij PASS: advies "evaluatie kopen" gaat via CEO naar Sandro (agents kopen/openen nooit iets). Bij FAIL: portefeuille dood, telt als 1 trial (TRIAL_COUNT +1), reserve is dan verbruikt voor deze hypothese en wordt niet hergebruikt voor klonen.

## 4. Verwachting / falen
Prior: bescheiden. Faalmodi: ORB-effect in 2025+ ~0 (de ETF-reserve 2025 liet ook weinig zien); BTC-edge rond US-open is regimeafhankelijk; ρ stijgt in stress. Mislukking is een geldige uitkomst.
