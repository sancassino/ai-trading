# SCENARIO_RAPPORT — wat levert de beste strategie realistisch op? (voor Sandro, 2026-09-30)

> **Definitieve stand (2026-09-30): zie PLAFOND_DEFINITIEF.md** — kern RSI(2) in MT5 SR ≈ 0,5, ≈ €50–150/mnd; ORB-variant ≈ €146–225/mnd maar onbevestigd buiten 2021–26.


In gewone taal. Alle cijfers voor een FTMO-account van **€80.000**, op basis van de beste strategie die we hebben gevonden en
in MetaTrader 5 hebben nagebouwd (een combinatie van "koop na een scherpe daling" op indices en "volg de uitbraak na het
eerste half uur"), zo ingesteld dat de dagelijkse verliesgrens van FTMO niet wordt geraakt.

## 1. Wat kun je in 12 maanden verwachten?
Gesimuleerd door de echte dagresultaten 2021–2026 20.000 keer in willekeurige volgorde af te spelen:

| | Slecht jaar (1 op 20) | Normaal jaar (mediaan) | Goed jaar (1 op 20) | Kans op verlies over het jaar |
|---|---|---|---|---|
| Met de kosten uit de backtest | −€1.280 | +€2.720 (≈ €225/mnd) | +€6.900 | 13% |
| Met realistische kosten (ruimere spreads, slippage) | −€2.250 | **+€1.770 (≈ €150/mnd)** | +€6.000 | **24%** |

De grens van 10% verlies (−€8.000) en de dagelijkse grens van 5% werden in geen enkele simulatie geraakt: de strategie
is voorzichtig ingesteld. Maar daardoor is de opbrengst ook klein.

## 2. Wat kost/levert een FTMO-challenge op?
- Fee: **≈ €540** voor de €80k-2-Step (secundaire bronnen, o.a. jptradingcapital.com; niet op ftmo.com zelf geverifieerd).
  Je krijgt de fee terug bij de eerste uitbetaling als je slaagt.
- Om te slagen moet je eerst +10% (€8.000) en daarna +5% halen. Met deze strategie duurt dat in de simulatie **gemiddeld
  ongeveer 2,5 jaar**, en slaagt maar **≈ 1 op de 6 pogingen** (17,5%) binnen redelijke tijd.
- Verwachte opbrengst per poging (fee meegerekend): **≈ −€10**, dus ongeveer quitte. **Een challenge is met deze strategie
  economisch (nog) niet de moeite waard.**

## 3. Wat zou er waar moeten zijn voor €880 per maand?
- €880/mnd = 13% per jaar op €80k, terwijl het verlies nooit boven 10% mag komen. Daarvoor moet de strategie ongeveer
  **anderhalf tot twee keer zo "goed"** zijn als wat we hebben (vaktaal: Sharpe ≈ 1,4 nodig, wij hebben ≈ 0,7–1,0).
- Simpelweg groter handelen kan niet: bij ~4× de huidige grootte zou één slechte dag al ~15% kosten, en FTMO sluit het
  account bij 5% verlies op één dag.
- Na ruim 390 geteste varianten (trend, momentum, carry, pairs, omkeer, seizoenen, crypto, nieuws) is er geen enkele
  gevonden die in de buurt komt. De kans dat deze aanpak €880+/mnd haalt schat ik op **minder dan 5%**.

## 4. Vergelijking zonder FTMO
- Wie €80.000 eigen geld in een breed aandelenfonds (S&P 500) had gestoken, verdiende 2000–2026 gemiddeld ≈ 8,4% per jaar
  ≈ **€557/mnd** — maar met tussentijdse dalingen tot **−55%** (2008) en jaren met verlies.
- Voor gemiddeld €880/mnd uit zo'n fonds is ≈ **€126.000** eigen vermogen nodig, met hetzelfde dalingsrisico.
- FTMO gebruikt geen eigen vermogen (alleen de fee), maar de regels (max 5% verlies per dag, 10% totaal) maken hoge
  opbrengsten met de gevonden strategieën onmogelijk.

## 5. Wat loopt er nu?
- Een **papieren test vooruit in de tijd** (vanaf 30 sep 2026, elke werkdag automatisch, resultaten in `forward/`). Dat is de
  enige echte test op nieuwe data. Eerste indicatie na ± 3 maanden, betrouwbaarder na 6–12 maanden.
- Voor een echte demo-test op FTMO is een nieuw proefaccount nodig (het huidige staat handelen niet meer toe).

## Beslissing voor jou
1. **Doel bijstellen** naar ± €150–250/mnd (dan is de huidige strategie + de papieren test een redelijke route), of
2. **stoppen** met deze zoektocht, of
3. een **heel andere bron van voordeel** aandragen (bijvoorbeeld je eigen handelsregels die we kunnen testen).
