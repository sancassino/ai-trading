# PREREG_PORT — portefeuilleregel (CEO D-052; Strateeg-input v2.5; methode r2_portfolio.py) — vastgelegd 2026-09-30 vóór forward en reserve-run

Geschreven door Uitvoerder-1 op last van de CEO (D-052: Uitvoerder-2 idle). Geen nieuwe signalen, geen optimalisatie, geen trial. Deze regel geldt voor
het forward-papier (D-050, `forward_portfolio.py`) én voor de gezamenlijke reserve-run (D-038/D-042). Na commit niet meer wijzigen (SHA in RUNLOG).

## 1. Sleeves (reeks = engine-dagreeks per regel/variant/vehikel; overschotrendement x = totaal − rf)
| sleeve | regel / variant | vehikel |
|---|---|---|
| S_C52L | C52_allweather / lang | etf |
| S_C52B | C52_allweather / basis | etf |
| S_C02 | C02_faber / basis | etf |
| S_C17 | C17_fomc_cycle / basis | future (D-042/D-052: alleen V2/V3) |
| S_C54Q | C54_carver / qa | future |
| S_C54B | C54_carver / basis | future |

## 2. Portefeuilles (drie, vooraf; geen selectie achteraf)
- **P-ETF** = S_C52L + S_C02 (C17 niet ETF-uitvoerbaar volgens D-042/D-052). Twee varianten:
  - **P-ETF-a (ongehefeld; adviesbasis/ondergrens):** gewichten ∝ 1/σ_s (σ_s = standaarddeviatie van de 60 laatste dagelijkse overschotrendementen
    vóór de herwegingsdag, ×√252), genormaliseerd tot som 1; geen hefboom; resultaat zoals het valt (vol ≈ 5–7%).
  - **P-ETF-b (gehefeld):** P-ETF-a × k, k = min(2, 0,10 / σ_P) met σ_P = 60-daagse vol van P-ETF-a vóór de herwegingsdag (en k ≥ 1 alleen als
    σ_P < 10%; anders k = 0,10/σ_P < 1); geleend deel (k − 1)⁺ gefinancierd tegen **rf + 1,5%**; hefboom ≤ 2×.
- **P1 (bovengrens)** = S_C54Q + S_C52L + S_C02 + S_C17.
- **P-breed (tegen winnaarsvloek)** = alle catalogus-rijen die G-ontdekking haalden (TRIALS.csv, 30-09): S_C02, S_C52B, S_C52L, S_C54B, S_C54Q.
- **P1/P-breed-methode:** elke sleeve naar 10% vol (k_s = min(3, 0,10/σ_s)), gelijk gewogen gemiddelde, daarna portefeuille naar 10% vol
  (k_P = min(3, 0,10/σ_P)); totale hefboom per sleeve k_s·k_P ≤ 3. Financiering: future-sleeves impliciet (geen opslag; totaal = rf + k·x);
  etf-sleeves met k > 1: opslag 1,5%/jr op het geleende deel (k − 1)⁺.

## 3. Herweging, kosten, valuta, rf
- **Herweging maandelijks op de eerste handelsdag** (slot); σ's met de 60 dagen t/m de vorige handelsdag (geen lookahead); geen drempelregel;
  tussen herwegingen blijven de hefboomfactoren/gewichten vast (gewichten drijven niet mee — vereenvoudiging, vermeld).
- **Kosten:** sleeve-reeksen bevatten hun eigen handels-/TER-/rolkosten (engine). Herwegingskosten tussen sleeves: Σ|Δ(gewicht × hefboom)| × halve
  rondreis van het vehikel (etf 13 bp → 6,5 bp per eenheid; future 1 bp → 0,5 bp).
- **Vehikelset (één set, U-005):** engine sinds 31f34c1 — etf 13 bp rondreis, TER 0,07%, SPX_TR voor SPX; future volgens de R2-fix (D-045);
  cfd_retail niet in deze portefeuilles. Alle sleeve-reeksen worden met deze set herberekend (engine/forward.py), niet uit oude R2-dumps.
- **rf:** engine.rf_on — FRED DTB3 t/m 25-09-2026, daarna US Treasury 3m (officieel; verschil mediaan +6 bp, sinds 2024 +15 bp/jr).
- **Valuta:** hoofdrapport **ongehedged in EUR** (r_EUR = (1 + r_USD) · EURUSD_{t−1}/EURUSD_t − 1; EURUSD uit data/daily/EURUSD, Yahoo =X);
  gehedged (r_USD + (i_EUR − i_USD)/365 per kalendernacht; 3m-rentes IR3TIB, na FRED-einde laatste waarde) als gevoeligheid. Rapport ook in USD.
- **FRED-vervangers (forward):** FX-sleeves (C54) gebruiken FRED-FX_* t/m 25-09-2026; voor de forward-periode worden FX_*-reeksen aangevuld met Yahoo =X
  (zelfde paar); FX-carry houdt de laatste bekende maandrente.

## 4. Forward-papier (D-050)
- Start **2026-10-01** (eerste handelsdag). Dagelijks na de data-update (22:05 UTC): alle sleeve-reeksen opnieuw met engine/forward.py t/m de laatste
  complete dag; portefeuilles volgens §2–3; `forward/portfolio_daily.csv` (datum; per portefeuille dag- en cumulatief rendement USD/EUR; hefboom;
  herwegingskosten) — append-only; data-snapshots in forward/data_snapshots/.
- **Tracking-band:** dagelijks wordt het forward-rendement van de vorige dagen herberekend; een afwijking > 1 bp tussen eerder gelogde en herberekende
  dagrendementen wordt gelogd (oorzaak: data-herziening Yahoo); de eerst gelogde waarde blijft de officiële.

## 5. Vooraf vastgelegde verwachting (D-052/D-054 — niet achteraf mooier maken)
- **P-ETF-a:** ≈ CAGR 4–6,5% op de ontdekkingsset ⇒ ≈ €270–430/mnd op €80k **vóór** live-haircut (30–50%) en box 3 → **onder het €400–500-doel**.
- **P-ETF-b:** hoger rendement met hogere DD en financieringskosten (rf + 1,5% op ≤ 1× geleend).
- **P1:** ontdekking SR ≈ 0,84 = bovengrens (winnaarsvloek; C54 bij €80k als micro-future nauwelijks uitvoerbaar, D-047).
- Forward-papier van 3 maanden heeft geen statistische power (SR-SE ≈ 2); het dient als uitvoerings-/datacontrole, niet als bewijs.
