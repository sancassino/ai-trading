# NEXT_STEPS v10 — supervisor, 2026-09-30 07:17 Amsterdam — STEADY-STATE (geen nieuwe hypothesen)

## Beoordeling
- N1–N6 goed uitgevoerd en eerlijk gerapporteerd: N1 (MT5) **niet gehaald** (kern max 1 nacht SR 0,47, €36/mnd bij 1/6, ~€98 bij 2,8× schaal; max 2 nachten SR 0,12) — reconciliatie MT5 vs Python zwakker (corr 0,83/0,89; totaal +3,2% vs +5,1%), dus Python overschat, ook al klopt de logica (N5: 100% trade-overeenkomst, geen lookahead; N6: 6/6 reproduceert).
- Conclusie (mijn oordeel = PLAFOND_DEFINITIEF): realistisch **€50–150/mnd**, ~1 op 4 kans op verliesjaar, geen sleeve met bewezen edge. €880/mnd niet haalbaar met deze aanpak. Enige route naar meer: ORB bevestigen op lange data (Sandro) of een nieuw idee van Sandro.
- Steady-state is correct: **geen nieuwe trials** (394). Elke extra hypothese op dezelfde data verlaagt alleen de betrouwbaarheid.

## OPEN TAKEN (geen nieuwe trials; bereiden voor op input van Sandro)
**P1 — Klaarzetten van de bevestigingspijplijn zodat data-aankomst direct tot een uitslag leidt.** Schrijf nu `PREREG_L2L3.md` (vóór er data is; ORB B4a ongewijzigd op 2010–2020: t ≥ 3 over US500/US100/GER40 gepoold, ≥ 8/11 jaar+, bp/trade ≥ 0,9; pre-FOMC-intraday en K1-nachten idem) en een parser voor HistData-ASCII-M1 (SPXUSD/NSXUSD/GRXEUR/XAUUSD; tijdzone EST zonder DST, sessieafbakening, kwaliteitscheck) + `run_l2l3.sh`. Test de parser op een synthetische mini-bestand in HistData-formaat. Zodra `data/long_m1/` gevuld is: één commando geeft de uitslag.
**P2 — Monitoring-alarmen voor de forward-test.** Script dat dagelijks controleert: is `paper_daily.csv` bijgewerkt (gat > 1 werkdag → melding in `forward/ALARM.md`), dagverlies ≥ 4% of DD ≥ 8% (K2-regels), cron gedraaid, git-push gelukt. Eerste echte dag = 2026-09-30 22:15 UTC; controleer morgenochtend of die er is.
**P3 — Sandro-gids.** Zet in `DATA_REQUEST_SANDRO.md` bovenaan een 5-regel-samenvatting: wat hij moet doen (HistData handmatig, ~100 bestanden, of Dukascopy/AWS), hoe lang het duurt, wat het kan opleveren (alleen ORB-bevestiging → tot ~€146/mnd realistisch). Vermeld eerlijk dat het **niet** naar €880 leidt.
**P4 — Overweging voor Sandro (schrijf `ALTERNATIEF_DOEL.md`, ≤ 1 pagina).** Zonder nieuwe trials: wat is een realistisch, positief doel met deze €80k-omgeving? (a) gewoon stoppen; (b) papieren test 12 maanden laten lopen als foutdetector; (c) inzetten van eigen kapitaal in indexfonds (SCENARIO: €557/mnd gemiddeld bij €80k, DD −55%) i.p.v. FTMO; (d) een eigen, regelgebaseerd handelsidee van Sandro laten backtesten met onze pijplijn (pre-registratie, DSR, MT5). Geef voor (d) een formulier met vragen (instrument, tijdframe, in/uit-regels, stop, risico) zodat Sandro het in 10 minuten kan invullen.

## Wat ik NIET meer opdraag
Geen nieuwe hypothesen, families of parametervarianten. Alleen weer werk op nieuwe data of nieuwe input van Sandro.
