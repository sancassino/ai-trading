# EVALUATIE — wat ging goed, wat kan beter, wat ging fout (manager, 2026-09-30)

Periode: 29 sep 2026 ~12:30 t/m 30 sep ~10:15. ~404 vooraf-vastgelegde varianten, ~60 verslagen, 4 supervisor-cycli.

## Wat ging goed (behouden)
1. **Onderzoeksdiscipline:** pre-registratie vóór berekening, TRIAL_COUNT + gedeflateerde Sharpe, train/test (2021–23 / 2024–26), eis t ≥ 3. Negatieve resultaten eerlijk gerapporteerd (bijna alles).
2. **Fouten zelf gevonden en gemeld:** swap-artefact in de tester, hindsight-universum (NVDA/META/TSLA), Sharpe-bug, aandelen-sessietijden, FTMO-dagverliesregel (Python zag hem niet, MT5 wel).
3. **Verificatielaag:** MT5-reconciliatie (277=277 trades), onafhankelijke code-audit (100% overeenkomst), `reproduce.sh` 6/6, FTMO-regels letterlijk geciteerd.
4. **Economie vóór hoop:** Q1/Q1b rekenen de echte FTMO-mechaniek (fees, herstarts, payouts, dagregel) door en laten zien dat de lat veel hoger ligt (SR 3–4 voor €500–900 bij het echte RSI(2)+ORB-dipprofiel), en R3 dat het **dip-profiel** en de **scheefheid** de lat bepalen.
5. **Ritme:** de agent pakt nu binnen minuten nieuwe taken op (cron */10); mijn uurlijkse cyclus draaide 8/8.

## Wat kan beter
1. **Hypothese-generatie was ad hoc:** ~400 trials waren vooral 'bekende anomalieën uit het hoofd' (momentum, RSI2, ORB, FOMC, …). Gepubliceerde, kort-geleden-bekende effecten zijn na kosten dood — dat was voorspelbaar. Nodig: **economische logica eerst** (wie betaalt ons, waarom?) en **kosten-eerst-screening** (bruto per trade ≥ 3× kosten vóór we testen).
2. **Doel zonder economie:** €1.000–2.000/mnd werd gesteld vóór iemand de FTMO-mechaniek doorrekende. Pas na ~12 uur (Q1) bleek SR 3–4 nodig. De doelstelling en het productkeuze (2-Step/1-Step/Scaling/andere prop firms) hoorden vooraan.
3. **Kandidaat-selectie achteraf:** RSI(2)+ORB (sleeves 'met t ≥ 2,5') is na het zien van de data gekozen; ORB is onbevestigd buiten 2021–26 en 'piek'. Optimistisch tot bewezen.
4. **Data was niemands taak:** lange intraday-data (ORB/pre-FOMC bevestigen) bleek geblokkeerd en niemand bezat het probleem; Sandro kreeg pas laat een dataverzoek.
5. **Zoekruimte is smal:** instrumenten = FTMO-CFD's, 5,7 jaar M5. Geen andere assets/venues/brokers, geen alternatieve prop-firm-mechaniek, geen structurele (niet-statistische) bronnen.
6. **Documenthygiëne:** 359 bestanden, EINDVERSLAG met 10 gestapelde banners (door mij) → onleesbaar. Nu opgeruimd (archief/).
7. **Eén 'supervisor' deed drie petten:** ritme/planning, kritische statistiek én strategie. Daardoor te weinig diepgang in strategie-ontwerp.

## Wat ging fout
1. **Steady-state (mijn fout):** stopregel te vroeg en zonder overleg; ~1 uur stilstand, tegen jouw opdracht.
2. **Vroege ritme-problemen:** te kleine backlogs (agent klaar in 20 min), sessie-wakeups die niet afgingen (15:29, 20:10) en fase-verschil met de agent-check. Opgelost met server-routine + */10.
3. **B5-EV te optimistisch gepresenteerd:** loterij-/optiewaarde-effect (R3: nul-edge al positief bij schone dips) kan misleiden; is niet wat we willen (FTMO verbiedt gokgedrag; echte kosten geven negatieve drift).
4. **Demo-account verlopen ongemerkt** (`trade_allowed=False`) — nooit gecontroleerd tot F6.
5. **Multiple testing uitgeput:** met 404 trials is DSR ≈ 0,3 voor de beste; elke extra 'gepubliceerde' anomalie maakt het erger.

## Belangrijkste inzichten
- Kosten (spread + commissie + swap) zijn de muur: voorspelbare bewegingen < spread (Q4).
- De lat hangt sterk af van het **dip-profiel**: elke-dag-vlak + positief scheef (ORB-achtig) → vereiste SR ≈ 1; overnight-mean-reversion (RSI(2)) → SR 3–4. Richting: dagelijks-vlak, positief-scheef, kosten-laag.
- ORB alleen: historisch ≈ €484–513/mnd, met realistische kosten ≈ €155–164, maar **onbevestigd** → data-toets heeft de hoogste waarde/kosten-verhouding.

## Voorstel: wie missen we? (zie ORGANISATIE.md)
1. **Strateeg / Head of Research** (nieuw, aparte Claude-chat): hypothesen met economische logica, instrument-/markt-/productselectie, gaten in de data, kosten-eerst.
2. **Manager (ik)** wordt specifieker: COO + Risk/Compliance + statistische kwaliteit + rapportage aan Sandro.
3. **Uitvoerder (Debian-agent):** quant/engineer + data.
4. **Onafhankelijke Auditor** (optioneel, later, aparte chat, op afroep): alleen wanneer een kandidaat een beslisregel haalt.
