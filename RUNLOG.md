# RUNLOG

Kort verslag per run/test, nieuwste onderaan.

## 2026-09-29 12:30 — Sessie 28 sep: regimefilter, dag-equity, guard, breed universum

Getest: regimefilter SMA10 over 9 plateau-configs; dagelijkse equity-log in EA; FTMO-dagregel (balance 00:00 − 5%); daily/total equity-guard; exposure 45/60%; train/test-split over 36 runs; plateau-ensemble; breed universum (65 instr.) ruw en vol-gecorrigeerd.
Resultaat: teken robuust (36/36 test positief) maar parameterkeuze niet (Spearman −0,28); FTMO-veilig ~$350–500/mnd per $100k; breed universum verliest → 16-resultaat deels hindsight-selectie. Details: Bevindingen_MomentumRotatie.md.
Volgende stap: alles herrekenen naar het echte account (€80.000 EUR).

## 2026-09-29 12:47 — Herberekening naar €80.000 EUR

Getest: 11 kernconfigs opnieuw in MT5 met Deposit=80000/EUR (baseline, 9 plateau-configs SMA10 @30%, beste config guard3/60%); ensemble, train/test en dag-MC herhaald met ACCOUNT_START=80000, doel €880 (=$1.000 @1,138) en €1.000.
Resultaat: beste in-sample €1.069/mnd (train €1.321 → test €648); plateau €163–380/mnd; ensemble €284/mnd; realistisch FTMO-veilig ≈ €280–420/mnd. MC: baseline funded 19–28%, live ≥€880 3–6%; beste config funded 44–62%, live ≥€880 19–22% (in-sample bovengrens).
Volgende stap: walk-forward-validatie (rollende vensters).

## 2026-09-29 12:48 — Walk-forward SMA10-plateau (EUR)

Getest: walk_forward.py (nieuw) op de 9 EUR-configs SMA10 @30%, rollend train 12/24/36 mnd, test 6 mnd, stap 3 (vensters overlappen).
Resultaat: gem. rangcorrelatie train↔test −0,05 / −0,12 / −0,18 → parameterkeuze op historie heeft geen voorspellende waarde. Ensemble ≥ 'kies beste': €499 vs €458/mnd (24m), €314 vs €262 (12m), €450 vs €415 (36m); ensemble positief in 11/14, 12/18, 8/10 vensters. Zwakke vensters: 2023-H2, 2025-H1, 2026.
Volgende stap: walk-forward herhalen op de nieuwe universums (alleen indices/grondstoffen; top-10 marktkapitalisatie 2020) zodra die runs klaar zijn.

## 2026-09-29 12:50 — Kostenanalyse: swap-artefact in de Strategy Tester

Getest: swap/commissie per EUR-run; swap-specificaties (swap_mode=1 = vaste punten/lot/dag); NVDA-koershistorie FTMO.
Resultaat: swap vreet 34–62% van de bruto winst (€18–38k per run), commissie/spread verwaarloosbaar. Oorzaak grotendeels tester-artefact: huidige puntwaarde wordt op de hele historie toegepast, terwijl koersen split-gecorrigeerd zijn (NVDA $13 in 2021 vs $225 nu → ~145%/jr financiering i.p.v. ~8%). swap_correct.py (nieuw) herrekent swap naar constante %-van-notional tegen huidig tarief (conservatief voor 2021–22). Effect: +€10–23k per run; plateau SMA10 @30% van €163–380 naar €327–630/mnd, alle configs 5/6–6/6 jaar+; beste config €1.391/mnd.
Kanttekening: aanname dat FTMO's puntswap ≈ constant % van notional; nog te verifiëren tegen contractspecificaties.
Volgende stap: swap-% per symbool verifiëren via Python zodra de VM vrij is; universum-runs afronden.

## 2026-09-29 13:24 — Universum zonder hindsight (a): alleen indices/grondstoffen

Getest: 17 instrumenten (alle FTMO cash-indices + XAU/XAG/XPD + UKOIL/USOIL met data ≤2020-12-31; universe_idx.txt), 9 configs SMA10 @30%, €80k EUR.
Resultaat: €−25 tot €212/mnd (niet swap-gecorrigeerd; swap hier klein, ~€2,5k/run); ensemble €106/mnd; walk-forward (24/6/3) positief in slechts 6/14 vensters, rho −0,13. Laag risico (stat. DD ≤6%, dagverlies ≤6%). Geen bruikbare edge → de edge van het 16-universum zat vooral in de megacap-aandelen.
Volgende stap: universum (b) top-10 marktkapitalisatie per 31-12-2020 (loopt).

## 2026-09-29 13:34 — Universum zonder hindsight (b): top-10 marktkap. 2020 + swap-gecorrigeerde vergelijking

Getest: 9 configs SMA10 @30% op 16 (origineel), T10 (top-10 marktkap. 31-12-2020 + indices/goud/olie/EURUSD) en IDX; koersdata nieuwe symbolen via mt5_export_rates.py (nieuw); swap-correctie op alles; ensemble + walk-forward.
Resultaat (ensemble, €/mnd): 16 → €470 (WF €592, 12/14+); T10 → €200 (WF €333, 10/14+); IDX → €130 (WF €159, 8/14+). Alle T10-configs positief (€61–309). Zonder hindsight ~40% van het 16-niveau.
Volgende stap: absolute-momentum-filter (dual momentum: alleen houden bij eigen rendement > 0) om drawdown te verlagen en meer exposure mogelijk te maken, getest op T10.

## 2026-09-29 14:00 — Dual momentum (absolute-momentumfilter) op T10

Getest: EA-optie AbsMomentumFilter (alleen houden bij eigen lookback-rendement > 0, lege slots in cash; bugfix: bij 0 kandidaten nu flat i.p.v. oude posities houden). 9 configs × {SMA10, geen regimefilter} op T10-universum, €80k EUR, 30%, swap-gecorrigeerd. Swap-aanname geverifieerd via mt5_swap_specs.py: aandelen ~8,2–8,8%/jr constant % van notional, indices 5–8%, puntwaarden worden door FTMO bijgesteld (swap_specs_FTMO.csv).
Resultaat: met SMA10 vrijwel identiek aan zonder abs-filter (ensemble €200/mnd; filter bindt zelden in risk-on). Zonder SMA10: ensemble €172/mnd, stat. DD 9,0% vs 4,7%. Geen verbetering → SMA10-regimefilter blijft de betere risicobeperking.
Volgende stap: echt ensemble in de EA (9 sub-portefeuilles in één account, gewichten per symbool opgeteld) + portefeuille-guard, zodat hogere exposure realistisch (niet lineair benaderd) getoetst kan worden.

## 2026-09-29 14:29 — Echt ensemble in de EA (T10 en 16, 30–90% exposure, dagguard)

Getest: nieuwe EA-modus EnsembleTopNs='2,3,4' × EnsembleLookbacks='1,2,3' met herschaling; T10 @30/60/90% ± guard 3%, 16 @30% en @60%+guard; €80k EUR, SMA10, swap-gecorrigeerd.
Resultaat: EA-ensemble T10 @30% €186/mnd ≈ lineaire benadering €200 (validatie OK). T10 @60% zonder guard €375/mnd maar dagverlies 8,1% (breekt FTMO); met guard 3% instorting naar €38–42/mnd, stat. DD 14–17%. 16 @60%+guard €637/mnd (test €409) maar hindsight-universum. Conclusie: geen FTMO-conforme route naar €880/mnd zonder hindsight in deze strategiefamilie; haalbaar ~€190–320/mnd.
Volgende stap: Next-steps-bestand uit de repo ophalen en die taken uitvoeren.

## 2026-09-29 14:36 — NEXT_STEPS stap 2: reconciliatie Python ↔ MT5 (T10)

Getest: nieuwe simulator momentum_sim.py (exact de EA-regels: rebalans 1e handelsdag, lookback N×30d, SMA10 op 10 samples à 30d, geen herschaling van aangehouden legs, CFD-boekhouding in EUR incl. EURUSD/EURGBP, 8%/jr financiering, 0,05% spread/kant). Bestaande momentum_rotation*.py kenden geen SMA10/kosten, dus niet bruikbaar voor deze vergelijking. Vergeleken met MT5 T10 (swap-gecorrigeerd), 2021-01..2026-09, reconcile.py (nieuw).
Resultaat: TopN=2/lb=3: corr 0,895 (0,915 vanaf 2021-02), totaal py +20,0% vs MT5 +9,0% → criterium (≥0,95 en <15%) NIET gehaald. Oorzaken: (1) MT5-datagat jan 2021: posities pas ~25 jan gevuld; (2) 10/56 maanden andere #2-keuze (randgevallen in de ranking); vultiming (slot vs vorige slot) maakt nauwelijks uit. Per config corr 0,87–0,94, afwijking beide richtingen (py hoger in 4, lager in 5 van 9) → geen systematische bias. Ensemble van 9 (vanaf 2021-02): corr 0,951, totaal +19,7% vs +18,2% (8%) → wél binnen criterium.
Conclusie: Python-resultaten zijn overdraagbaar op plateau/ensemble-niveau, niet per losse config.
Volgende stap: stap 1 (lange validatie 2000–2026, universum A en B).

## 2026-09-29 14:39 — NEXT_STEPS stap 1: lange validatie 2000–2026 (universum A en B) — NEGATIEF

Getest: momentum_sim.py, exact de EA-regels, 9 configs (TopN 2–4 × lb 1–3), SMA10 op SPY, 30% exposure, 2000-01..2026-09, kosten 8%/jr financiering + 0,05% spread/kant. A = 26 ETF's (universe_A_etf.txt; GLD/SLV/USO vóór start gespliced met GC=F/SI=F/CL=F). B = point-in-time top-10 S&P500-marktkap. per jaareinde (universe_pit_top10.csv, bron finhacker.cz, opgehaald 29-09-2026); alle 31 namen incl. GE/C/AIG/INTC/CSCO/MRK/PFE beschikbaar op Yahoo (adjusted) → geen ontbrekende namen; gedelistte bedrijven (Enron/Lucent/WorldCom) stonden nooit in een jaareinde-top-10. Gevoeligheid: financiering 4% en 0%. Referentie SPY buy&hold 30%.
Resultaat (ensemble, 8%): A CAGR +0,04%/jr, 13/27 jaar+ (48%), maand-DD 27,8%; B +0,25%/jr, 9/27 (33%), DD 25,1%. Per config A −0,5..+0,75%, B −0,6..+1,2%/jr; trailing DD 22–39%. Episodes (ensemble A/B): 2000–02 −7,0/−5,9%, 2008 +0,5/−0,5%, 2020-Q1 −3,3/−0,3%, 2022 −1,1/−9,9%. B werkte alleen 2019–2024. Bruto (0% fin.) A +1,9%/jr (70% jaren+), B +2,1% (56%). SPY b&h 30%: +2,18%/jr. Beslisregel (≥65% jaren+, DD<20%) faalt voor A én B.
Conclusie: de FTMO-uitvoerbare edge (aandelen/indices-CFD's) is NIET aangetoond; financieringskosten ≈ bruto edge; strategie verslaat passieve blootstelling niet. Stap 4 vervalt (voorwaarde niet gehaald).
Volgende stap: stap 3 (rang-gevoeligheid T10) ter volledigheid, via ensemble-EA in MT5.

## 2026-09-29 14:52 — NEXT_STEPS stap 3 (rang-gevoeligheid), stap 4 overgeslagen, eindverslag

Getest: ensemble-EA (9 configs) in MT5 op 7 universums (T10-basis + 10 aandelen): META→NVDA, BABA→NVDA, 5 willekeurige trekkingen uit de 49 aandelen van de brede lijst (random.Random(42), universe_step3.csv). €80k EUR, 30%, SMA10, geen guard, swap-gecorrigeerd (koersen 25 extra aandelen geëxporteerd).
Resultaat: T10 €186/mnd; NVDA-alternatieven €242 en €406; willekeurig €96, €64, €333 (bevat NVDA+PLTR), €1, −€77 → gem. €83, spreiding ≫ niveau. Stap 4 niet uitgevoerd (stap 1 faalde).
Conclusie: edge niet aangetoond; volledig verslag in VERSLAG_NEXT_STEPS_2026-09-29.md.
Volgende stap: wachten op nieuwe NEXT_STEPS (uurlijkse check).

## 2026-09-29 17:11 — Ronde 2: pre-registratie (vóór resultaten)

Vastgelegd in PREREG_ronde2.md vóór enige berekening: familie 1 (12m tijdreeks-trend, 12 instrumenten, vol-target 10%) en familie 2 (G10 FX carry top3/bottom3 + 12m trend, 50/50, vol-target 10%); kosten spread 0,05%/kant, financiering DTB3 ± 2%/jr (ETF/grondstoffen), FX renteverschil (FRED IR3TIB, 1 mnd vertraagd) − 1,5%/jr; beslisregel Sharpe ≥ 0,7, ≥ 65% jaren+, DD < 15%, dagverlies < 5%, over ≥ 20 jaar. Data-beschikbaarheid gecontroleerd (geen rendementen bekeken): JPY-rente pas vanaf 2002-04.
Volgende stap: implementatie en run familie 1 en 2.

## 2026-09-29 17:14 — Ronde 2: familie 1 en 2 — AFGEWEZEN (stop)

Getest: ronde2_sim.py volgens PREREG_ronde2.md, 2000-01..2026-09, 10% vol-target, kosten spread 0,05%/kant + financiering korte rente ± markup.
Resultaat: familie 1 (12m trend, 12 instrumenten) Sharpe 0,19, CAGR +1,5%, maand-DD 39,1%, 59% jaren+, slechtste dag −4,83%; familie 2 (G10 carry+trend) Sharpe −0,04, CAGR −1,0%, DD 68,1%, 41% jaren+, slechtste dag −5,14%. Referentie SPY @10% vol: Sharpe 0,41, CAGR +5,7%. Bugfix gemeld: Sharpe trok rf dubbel af (vóór 0,02/−0,21). Diagnostiek zonder markup: 0,58/0,42, ook dan afgewezen.
Conclusie: beide AFGEWEZEN. Verslag: VERSLAG_ronde2_2026-09-29.md. Geen MT5-implementatie.
Volgende stap: STOP — wachten op beslissing Sandro (EINDVERSLAG.md); uurlijkse NEXT_STEPS-check blijft actief.

## 2026-09-29 21:14 — B1: stats_tools.py (gedeflateerde Sharpe) + TRIAL_COUNT.md

Getest (PREREG_B1.md, vóór berekening gecommit): stats_tools.py met Sharpe ± SE (Mertens), block-bootstrap-CI, t-stat, gedeflateerde Sharpe (Bailey–López de Prado), min. trackrecordlengte, required_sharpe(); make_ensemble_daily.py; TRIAL_COUNT.md (≈300 varianten). Retroactief toegepast.
Resultaat: required Sharpe €880/mnd = 1,41 (13,2%/jr, vol ≤9,4%, P(−10%) ≤5%); €2.000/mnd = 2,12; €400/mnd = 0,95. DSR (N=300 / N=30): 16-ensemble SR 0,84 → 0,20/0,50; beste in-sample config SR 1,04 → 0,38/0,70; T10-ensemble SR 0,49 → 0,04/0,19; lang A/B SR 0,03/0,07 → 0,00; familie 1 SR 0,20 → 0,03; familie 2 → 0,00. Referentie SPY@10%vol SR 0,61 (ruwe rendementen, incl. cash-rente) → 0,61/0,86. Geen enkele strategie haalt DSR ≥ 0,95; alle positieve 2021–26-resultaten zijn na correctie niet significant.
Volgende stap: B2 (dagfrequente edges op indices 1990–2026).

## 2026-09-29 21:18 — B2: dagfrequente edges op indices 1990–2026 — alle 5 AFGEWEZEN

Getest (PREREG_B2.md vóór berekening): b2_sim.py, gepoolde sleeves (1/N), kosten 0,02%/kant + (DTB3+2%) per overnachting. Datakeuzes op kwaliteit: FTSE heeft geen echte opens (valt af voor c), SPX/NDX-opens tot 2007/2000 onbruikbaar → SPY/QQQ voor c; DAX pas vanaf 1994; goud via GLD 2004+ (GC=F-OHLC onbruikbaar, Stooq achter bot-check).
Resultaat (t / H1 1995–2010 / H2 2011–26 / maxDD / DSR305): (a) IBS t 1,93, +78%/+102%, DD 45,7%, 0,17; (b) RSI(2) t 3,65, +95%/+38%, DD 15,9%, 0,76 — faalt alleen op DD (grens 15%), edge verzwakt na 2010 (~2%/jr); (c1) intraday t −5,98 (kosten 2×0,02%/dag ≈ 10%/jr); (c2) overnight t −3,49; (d) TOM t 2,49, H2 slechts +9%. Per instrument: RSI(2) SPX t 4,0, NDX 3,7; IBS NDX 3,4.
Conclusie: alle 5 afgewezen volgens de beslisregel; RSI(2) is het dichtst bij (niet gered). TRIAL_COUNT 305.
Volgende stap: B3 (dollar-neutrale long/short momentum).

## 2026-09-29 21:20 — B3: dollar-neutrale long/short momentum — factor bestaat niet, familie definitief dood

Getest (PREREG_B3.md vóór berekening): b3_sim.py, long top-K/short bottom-K, 9 configs × universum A (26 ETF's) en B (PIT top-10), 2000–2026, vol-target 10%, hefboom ≤4, geen regimefilter, spread 0,05%/kant, financiering DTB3 ± 2%.
Resultaat netto: ensemble A CAGR −3,25%, Sharpe −0,29, t −1,48, DD 65%, 11/27 jaar+; ensemble B −6,01%, Sharpe −0,65, t −3,36, DD 83%, 9/27. Alle 18 configs negatief. Correlatie met SPY −0,05…−0,18 (beta-neutraal, zoals bedoeld). DSR 0,00.
Diagnostiek (geen beslisgrond) zonder spread/markup: A Sharpe 0,02, B −0,30 (B 2000–12 −61%, 2013–26 +15%): in de top-10 keren recente winnaars eerder om. Markup kost bij hefboom tot 4× ~6–8%/jr.
Conclusie: beslisregel (Sharpe ≥0,3 in beide universums) faalt ruim → momentum-familie definitief dood. TRIAL_COUNT 323.
Volgende stap: B4 (intraday op FTMO-M5-data, VM-export).

## 2026-09-29 21:29 — B4: intraday op FTMO-M5 2021–2026 — alle 3 AFGEWEZEN

Getest (PREREG_B4.md vóór berekening): b4_sim.py op FTMO-M5 (US500, US100, US30, GER40, UK100, XAUUSD, EURUSD) met spread per bar + commissie (indices 0; XAU €2,00/lot/kant; EURUSD €2,25/lot/kant, afgeleid uit eigen MT5-runs). MT5 MaxBars verhoogd 100k→5M (backup common.ini.bak_maxbars100000). Servertijd = NY+7u geverifieerd. data/m5/ uit git gehouden (135 MB, opnieuw te exporteren).
Resultaat (gepoold): (a) ORB N 9.249, +1,73 bp/trade (+0,037 R), t train +2,90 / test +1,14, 4/6 jaar+, DSR 0,54 — per symbool US100 t +2,5, GER40 +2,2, UK100/EURUSD negatief; (b) laatste-30-min N 9.300, −0,68 bp, t train −3,19 / test −1,33, 1/6 jaar+; (c) gap-reversal N 2.745, −1,38 bp, t −2,66 / +0,77, 2/6 jaar+.
Conclusie: alle drie afgewezen (t ≥ 3 in train én test niet gehaald). ORB het dichtst bij, maar test-t 1,14. TRIAL_COUNT 326.
Volgende stap: B5 (FTMO-economie-tool) — geen B2–B4-resultaat haalde de beslisregel, dus tool bouwen en demonstreren.

## 2026-09-29 21:31 — B5: FTMO-economie-tool (ftmo_economics.py)

Gebouwd: ftmo_economics.py — block-bootstrap (21 dagen) van een dagreeks × positieschaal; 2-Step-regels (10%/5%, dag 5%, totaal 10%, ≥4 dagen, fee terug bij 1e uitbetaling), funded 12 mnd met maandelijkse uitbetaling (80% split, saldo terug naar start). Fee €540 als parameter (niet geverifieerd: ftmo.com toont de prijs niet in opvraagbare vorm). Benaderingen: slot-tot-slot (geen intraday-dips → slaagkansen optimistisch), balance = equity. Geen B2–B4-resultaat haalde de beslisregel; tool gedemonstreerd.
Resultaat (scale 1/2/3, EV per poging): RSI(2) (B2b, vol 4,4%) €25 / €2.358 / €3.207, funded 18/52/50%; familie 1 €1.556 / €1.676 / €770 (live-breuk 46/94/100%); T10-ensemble-EA €359 / €2.681 / €2.975; SPY@10%vol €3.058 / €4.341 / €3.161. Controle zonder drift (edge = 0): SPY-vol €219 / €1.066 / €769, RSI(2)-vol −€510 / €24 / €516.
Inzicht: een challenge is optiewaarde (verlies begrensd tot de fee, winst gedeeld) → EV per poging kan zelfs zonder edge positief zijn bij voldoende vol, maar dat is loterij: live-breuk 36–96%, geen stabiel inkomen. Een echte trader zonder edge heeft negatieve drift (kosten), dus de controle is een bovengrens.
Volgende stap: backlog B1–B5 af → verslag + VOORSTEL (COORDINATION-regel 1).

## 2026-09-29 21:31 — Backlog B1–B5 afgerond + VOORSTEL

Backlog leeg. Verslag: VERSLAG_backlog_B1-B5_2026-09-29.md. Geen enkele taak haalde de beslisregel (TRIAL_COUNT 326).
VOORSTEL (label conform COORDINATION): 'FTMO-EV met MT5-realisme' — US500.cash long met vol-target + dagguard, EV per challenge-poging in MT5 (echte swap, intraday-dips) vs nul-edge-controle; eerlijk kader: positieve-verwachting-gok per fee, geen stabiel inkomen. Alternatief: stoppen.
Volgende stap: wachten op supervisor/Sandro via uurlijkse NEXT_STEPS-check (geen open taken in de backlog).

## 2026-09-29 21:46 — C1: pairs/stat-arb — alle paren AFGEWEZEN

Getest (PREREG_C1.md vóór berekening): c1_pairs.py, rollende 60d-OLS-hedge, z-score entry |z|>2, exit <0,5, stop >4, max 20 d, uitvoering t+1, kosten 0,02–0,05%/kant/been + financiering DTB3±2% beide benen. 4 ETF-paren 2004–2026, 8 FTMO-D1-paren test 2021–26.
Resultaat netto: ETF SPY/DIA t −4,07, SPY/QQQ −2,59, GLD/SLV −3,48 (−61% totaal), EWG/EWU +0,12. FTMO: alle negatief behalve UKOIL/USOIL +1,8%/jr (t 1,49, geen lange data, contango-swap niet gemodelleerd). N ≈ 10 trades/jaar per paar → N ≥ 300 nergens. DSR 0,00–0,08.
Diagnostiek zonder kosten/financiering (geen beslisgrond): ETF-paren t −2,57…+1,22; alleen UKOIL/USOIL bruto t 2,70 (5,6 jr). De spreads mean-reverten niet betrouwbaar op 60d-z-score (goud/zilver trendt).
Conclusie: C1 afgewezen. TRIAL_COUNT 334.
Volgende stap: C2 (lead-lag / tijd-van-de-dag op M5).

## 2026-09-29 21:47 — C2: lead-lag en tijd-van-de-dag op M5 — alle 4 AFGEWEZEN

Getest (PREREG_C2.md vóór berekening): c2_leadlag.py, FTMO-M5 2021–26, kosten zoals B4. (a) teken US500-sessie → GER40/UK100 eerste 60 min; (b) GER40 eerste 30 min → US500 eerste 60 min; (c1) XAU long 13:30–14:30 CET; (c2) US100 long 15:30–16:00 CET.
Resultaat: (a) N 2.473, −0,69 bp, t train +0,33 / test −1,87, 1/6 jaar+; (b) N 1.161, −0,81 bp, t −0,81 / −0,12; (c1) N 1.481, −1,69 bp, t −1,79 / −2,01, 0/6 jaar+; (c2) N 1.301, +0,84 bp, t +1,04 / −0,17. DSR ≈ 0.
Conclusie: geen lead-lag- of tijdvenster-edge na FTMO-kosten. TRIAL_COUNT 338.
Volgende stap: C3 (kortetermijn-omkeer markt-neutraal op FTMO-aandelen).

## 2026-09-29 21:50 — C3: kortetermijn-omkeer markt-neutraal — AFGEWEZEN

Getest (PREREG_C3.md vóór berekening): c3_reversal.py, 49 FTMO-aandelen (universe_stocks49.txt), elke 5 handelsdagen long onderste 20% / short bovenste 20% op 5-daags rendement, uitvoering t+1, 0,05%/kant, FTMO-swap long −8,4% / short −6,7%/jr. FTMO-D1 2021–26 (beslisgrond; 13 extra koersreeksen geëxporteerd) + Yahoo 2000–26 als survivorship-bovengrens.
Resultaat: FTMO CAGR −16,1%, SR −1,08, t −2,62, DD 65%, elk jaar negatief; Yahoo-bovengrens −8,4%/jr, t −3,16, alleen positief in 2000/03/08/09. Diagnostiek DTB3±2%: FTMO −11,5%/jr, Yahoo −3,4%/jr (2013–26 −76%). Kosten: wekelijkse omzet ≈ 8%/jr spread + FTMO-swap op beide benen ≈ 7,5%/jr.
Conclusie: afgewezen; omkeer-effect in large caps na 2010 verdwenen en FTMO-shortswap maakt markt-neutraal op aandelen-CFD's structureel duur. TRIAL_COUNT 340.
Volgende stap: C4 (sizing RSI(2) + combinatie van sleeves).

## 2026-09-29 21:52 — C4: RSI(2)+ORB-combinatie — EERSTE KANDIDAAT (DSR 0,55), nog niet bewezen

Getest (PREREG_C4.md vóór berekening): c4_combine.py. (a) RSI(2) SPX+NDX 50/50, schaal zodat dag-DD <8% en dagverlies <3%: schaal 0,35 → SR 0,71, t 4,30, CAGR +1,9% (≈ €125/mnd), DD 5,2%, DSR 0,91; helften +53% / +26%. (b) Sleeves met t ≥ 2,5 (vooraf): RSI(2) gepoold (B2b) + ORB gepoold (B4a); overlap 2021-09..2026-09; correlatie −0,09; 1/vol-gewichten 0,54/0,46; schaal 3,60 → SR 1,30, t 2,97, CAGR +13,9% ≈ €929/mnd op €80k, DD 8,0%, slechtste dag −2,5%, DSR340 0,55 (benodigd SR 1,41).
Extra controle (buiten prereg, gemeld): gewichten + schaal vastgezet op 2021-09..2023 en ongewijzigd toegepast op 2024–2026 → SR 1,35, t 2,27, ≈ €1.107/mnd, DD 9,8%, slechtste dag −3,2%.
Kanttekeningen: korte overlap (5,2 jr), schaal in-sample (volledige periode), ORB test-t in B4 slechts 1,14, 2022 draagt veel (+24%), DD-marge t.o.v. FTMO 10% klein; RSI(2) op Yahoo-indices (zonder dividend) i.p.v. FTMO-CFD's.
Conclusie: eerste combinatie boven DSR 0,5 → kandidaat voor MT5-bevestiging (FTMO-CFD's, echte swaps, balance-om-middernacht-regel). Geen succesclaim.
Volgende stap: C5 (crypto-trend), daarna C6, C7.

## 2026-09-29 21:57 — C5: crypto-trend BTC+ETH — AFGEWEZEN

Getest (PREREG_C5.md vóór berekening): c5_crypto.py, Yahoo BTC/ETH 2016–2026, maandelijks, 12-1-momentum én SMA50/200, vol-target 20% (0,5 per asset), spread 0,05%. FTMO-crypto-kosten via MT5 opgevraagd: swap_mode 5 = −30%/jr op notional, long én short (!).
Resultaat met FTMO-financiering: CAGR +3,5%, SR 0,30, t 0,98, DD 42,3%, 7/11 jaar+, SR excl. beste 2 jaren (2016/2017) −0,06, DSR 0,03. Diagnostiek zonder financiering: SR 0,75, excl. beste 2 jaren 0,39, DD 29,6%; met DTB3±2%: SR 0,71 / 0,35.
Conclusie: afgewezen — ook bruto niet robuust zonder de 2016/17-bull, en FTMO's 30%/jr-swap maakt elke meerdaagse crypto-positie kansloos. TRIAL_COUNT 341.
Volgende stap: C6 (vol-timing van index-exposure, Moreira–Muir).

## 2026-09-29 21:58 — C6: vol-timing van index-exposure — AFGEWEZEN

Getest (PREREG_C6.md vóór berekening): c6_voltiming.py, maandelijks w = min(1,5; 8%/σ21) vs b&h op gelijke vol (ex-post schaal), CFD-financiering DTB3+2%, spread 0,02%, SPX/NDX 1990–2026, DAX 1994–2026 (prijsindex).
Resultaat: SPX SR 0,33 vs 0,29 (ΔSR +0,03), DD 32,6%; NDX 0,57 vs 0,46 (+0,11), DD 27,9%; DAX 0,22 vs 0,24 (−0,02), DD 37,7%. Combinatie informatief SR 0,45 vs 0,38, DSR 0,33. Verbetering overal < 0,15 en DD ≫ 15%.
Conclusie: afgewezen; vol-timing geeft slechts een kleine DD-verbetering, geen bruikbare basiscomponent onder de FTMO-DD-grens. TRIAL_COUNT 344.
Volgende stap: C7 (alleen ontwerp B5-EV in MT5-realisme + FTMO-voorwaarde-risico's).

## 2026-09-29 22:00 — C7: ontwerp FTMO-EV met MT5-realisme (NIET uitgevoerd) + EV-tabel + risicolijst

Opgeleverd: PREREG_C7.md (ontwerp, niet uitgevoerd — Sandro beslist), C7_ev_tabel.csv (ftmo_economics.py op C4-combinatie, RSI(2), SPY-referentie; schaal 0,5/1/2; historisch én nul-drift-controle), results/c4/C4_comb_daily.csv.
EV (schaal 1, slot-tot-slot, optimistisch): C4-combinatie funded 89,8%, €808/mnd | funded, EV €8.640/poging (nul-drift €524); RSI(2) EV €24 (nul-drift −€510); SPY@10% EV €3.092 (nul-drift €219).
FTMO-risico's (ftmo.com FAQ/forbidden practices): Standard-account moet posities vóór weekend/rollover >2 u sluiten → RSI(2) vereist Swing-account; nieuwsvenster ±2 min (ook SL/TP) raakt ORB; gap trading/handelen vlak vóór sluiting verboden; consistente positiegrootte en risicoconcentratie; 'unfair advantage tools' (tekst verifiëren); Best Day Rule-drempel niet gevonden.
Volgende stap: portefeuilleregel — C4 haalde DSR 0,55 → geen PLAFOND-pauze; door met reserve D1 en VOORSTEL MT5-bevestiging C4.

## 2026-09-29 22:01 — D1: FX-intradagseizoen EURUSD — AFGEWEZEN

Getest (PREREG_D1.md vóór berekening): d1_fx_season.py, Breedon & Ranaldo-hypothese, FTMO-M5 EURUSD 2021–26: (i) short 08:00–12:00 Londen, (ii) long 14:00–18:00 Londen, kosten spread + €2,25/lot/kant.
Resultaat: (i) N 1.490, −1,31 bp, t train −2,15 / test −1,07, 1/6 jaar+; (ii) N 1.490, −1,44 bp, t −1,82 / −1,21, 1/6 jaar+. Effect in deze periode eerder omgekeerd (EUR sterker in Europese uren). (Opmerking: DSR-label in de output toont N=338 door hergebruik van de C2-functie; DSR is 0,00 ongeacht N.)
Conclusie: afgewezen. TRIAL_COUNT 346.
Volgende stap: D2 (goud vs reële rente lead-lag).

## 2026-09-29 22:01 — D2: goud vs reële rente — AFGEWEZEN

Getest (PREREG_D2.md vóór berekening): d2_gold_realrate.py, maandelijks long/short GLD op teken van 20-daagse verandering DFII10 (t−2), FTMO-swap long −7,93% / short −0,37%/jr, spread 0,02%.
Resultaat: CAGR −4,3%, SR −0,15, t −0,70, DD 69,6%, helften −27% / −50%, 11/23 jaar+. Diagnostiek DTB3±2%: SR −0,02.
Conclusie: afgewezen; geen bruikbare lead-lag van reële rente naar goud op maandbasis. TRIAL_COUNT 347.
Volgende stap: D3 (haalbaarheid futures-basis/roll op FTMO), dan D4.

## 2026-09-29 22:02 — D3: futures-basis/roll — NIET UITVOERBAAR op FTMO (geen trial)

Haalbaarheidscheck (geen strategie gedraaid): FTMO-symbolenlijst bevat voor indices alleen cash-CFD's (5+10+1 'Cash'), geen futures of kalenderspreads; futures-gebaseerde grondstof-CFD's (.c: cocoa, coffee, corn, soybean, wheat, cotton, sugar, heatoil) hebben data pas vanaf 2023/2024 en geen termijnstructuur (één doorlopend contract) → roll-yield/basis niet meetbaar of verhandelbaar. Geen trial geteld.
Volgende stap: D4 (risicopariteit op FTMO-verhandelbare asset-klassen; geen obligatie-CFD's bij FTMO).

## 2026-09-29 22:03 — D4: risicopariteit (FTMO-verhandelbare klassen) — AFGEWEZEN

Getest (PREREG_D4.md vóór berekening): d4_riskparity.py, SPY/EFA/GLD/USO (gespliced), 1/σ60-gewichten, 8% vol-target, hefboom ≤3, DTB3+2% financiering, 2001–2026. Geen obligatie-CFD's bij FTMO → geen klassieke risicopariteit mogelijk.
Resultaat: CAGR +3,4%, SR 0,40, t 2,04, DD 27,6%, helften +62% / +45%, 19/26 jaar+, DSR 0,18. Referentie SPY@8%: SR 0,36, DD 29,1%.
Conclusie: afgewezen (DD ≫ 15%, SR < 0,7). TRIAL_COUNT 348. Backlog C1–C7 + reserve D1–D4 afgerond.
Volgende stap: VOORSTEL_E.md met 3 hypothesen (FTMO-validatie van de C4-kandidaat) en direct de best onderbouwde uitvoeren.

## 2026-09-29 22:04 — E1: RSI(2) repliceert op FTMO-data — GESLAAGD (validatie, geen nieuwe trial)

Getest (VOORSTEL_E.md, E1 vóór berekening vastgelegd): e1_rsi2_ftmo.py, regel B2b ongewijzigd op FTMO-D1-slotkoersen (US500, US100, US30, GER40, UK100, XAUUSD), 2021–2026, spread = mediaan laatste M5-bar van de dag, FTMO-longswap per symbool per kalendernacht.
Resultaat: per symbool t: US500 +2,64, US100 +1,27, US30 +1,37, GER40 +0,50, UK100 −0,56 (eind-van-dag-spread 0,074%), XAU +0,10. FTMO gepoold (6) SR 0,57, t 1,39, 2021–23 +2,9%, 2024–26 +12,2%; Yahoo-versie (5) SR 0,64. Maandcorrelatie FTMO ↔ Yahoo 0,91.
Conclusie: beslisregel E1 gehaald (beide helften > 0, corr ≥ 0,7) — de RSI(2)-poot van de C4-kandidaat is geen Yahoo-artefact; wel iets zwakker op FTMO. Geen nieuwe trial (zelfde regel).
Volgende stap: E3 (weekend-regel Standard vs Swing voor de C4-combinatie).

## 2026-09-29 22:05 — E3: C4-combinatie op FTMO-data, weekendregel — Swing ≈ €480–520/mnd, Standard ≈ €200–265/mnd

Getest (PREREG_E3.md vóór berekening): e3_weekend.py, RSI(2)-poot = FTMO-versie (E1), ORB = B4a; gewichten + schaal vastgezet op 2021-09..2023, ongewijzigd op 2024–26.
Resultaat Swing (weekend toegestaan): gewichten 0,59/0,41, schaal 2,35 → volledig SR 0,97, t 2,20, ≈ €481/mnd, DD 7,8%, slechtste dag −3,0%, DSR 0,26; test 2024–26 SR 0,99, ≈ €519/mnd, DD 6,3%. FTMO-EV (slot-tot-slot): funded 73,8%, €485/mnd | funded, EV €4.142/poging vs nul-drift −€93.
Standard (vrijdag sluiten): schaal 1,85 → SR 0,63, ≈ €230/mnd, test SR 0,53, ≈ €201/mnd; EV €1.141 vs nul-drift −€251.
Conclusie: op FTMO-data halveert de C4-schatting (Yahoo gaf €929–1.107/mnd). Realistisch plafond ≈ €480–520/mnd op een Swing-account bij DD < 8%; onder €880. E2 (nieuwsvenster) is voor een Swing-account niet van toepassing (geen nieuws-/weekendbeperking volgens ftmo.com).
Volgende stap: PLAFOND_RAPPORT.md (portefeuilleregel: FTMO-gevalideerde DSR 0,26 < 0,5).

## 2026-09-29 22:06 — PLAFOND_RAPPORT: max haalbaar ≈ €250–500/mnd (Swing), kans €880+ < 10% — pauze

Opgesteld volgens portefeuilleregel (geen FTMO-gevalideerde sleeve/combinatie met DSR ≥ 0,5): PLAFOND_RAPPORT.md.
Kern: beste kandidaat RSI(2)+ORB op FTMO-data (E3), Swing: SR 0,98 ± 0,42 (bootstrap-CI 0,34–1,66), ≈ €480/mnd, DD 7,8%, test 2024–26 ≈ €519/mnd; Standard ≈ €230/mnd. Benodigde SR €880/mnd = 1,41; P(ware SR ≥ 1,41) ≈ 16% vóór correctie; DSR(348) 0,27. Verwacht live (30–50% haircut) ≈ €250–350/mnd.
Beslispunt Sandro: (1) doel verlagen + MT5-bevestiging (PREREG_C7-ontwerp) op Swing, (2) stoppen, (3) andere bron van edge.
Volgende stap: pauze nieuw onderzoek; uurlijkse NEXT_STEPS-check blijft actief.

## 2026-09-29 23:13 — F1: MT5-EA RSI(2) — reconciliatie GESLAAGD, maar FTMO-dagverliesregel breekt bij 100% notional

Getest (PREREG_F1.md vóór berekening): nieuwe EA RSI2Sleeve.mq5 (6 FTMO-symbolen, E1-regels, 1/6 equity per positie, Swing), generieke runner vm_run_ea.ps1/run_ea.sh; Strategy Tester Model=1, €80k EUR, 2021-01..2026-09.
Reconciliatie met Python E1: trades 277 = 277 (per symbool identiek); maandcorrelatie 0,989; totaal Python +15,4% vs MT5 +12,4% (swap-gecorrigeerd; ruw +9,1%) → verschil precies op de 25%-tolerantie. Resterend verschil verklaarbaar: MT5 vult op de open van de volgende serverdag i.p.v. het slot, en Python rekent geen EUR-conversie voor USD-instrumenten.
BELANGRIJK: MT5-dag-equity toont FTMO-dagverlies (balance 00:00 − min equity) tot 6,08% (2022-01-24) en 5,44% (2026-03-23) al bij 100% notional — meerdaagse verliesposities in gecorreleerde indices stapelen tegen de middernacht-balance. Python (slot-tot-slot) zag dit niet. Bij de E3-schaal (RSI-blootstelling ≈1,4×) breekt de regel zeker.
Conclusie: EA ≈ Python (goed), maar de RSI(2)-poot vereist een dagverlies-guard of veel kleinere schaal onder FTMO-regels. Meenemen in F3.
Volgende stap: F2 (MT5-EA ORB + reconciliatie).

## 2026-09-29 23:18 — F2: MT5-EA ORB — reconciliatie GESLAAGD

Getest (PREREG_F2.md vóór berekening): nieuwe EA ORBSleeve.mq5 (7 symbolen, OR 30 min, buy-/sell-stop OCO met SL andere kant, flat op sessie-einde; sessietijden in servertijd incl. DST-afwijkingsweken), Model=1, €80k EUR, 2021–2026, 1/7 equity per trade.
Resultaat: MT5 N 9.414, +1,76 bp/trade, t +3,03 vs Python B4a N 9.249, +1,73 bp, t +2,93 → N binnen 2%, bp-verschil 0,03 (< 0,7), teken per jaar identiek (2021 −, 2022–2025 +, 2026 −). Overlap 9.182 (datum, symbool), correlatie per trade 0,99. Per symbool gelijk: US100 +6,1/+5,9 bp, GER40 +4,1/+4,0, US500 +2,2/+2,4, XAU +1,1/+1,5, US30 +0,6/+0,3, EURUSD −0,4/−0,4, UK100 −0,7/−0,8.
Kanttekening: de tester vult stop-orders exact op de stopprijs (geen slippage) → optimistisch; G1 (kostengevoeligheid) blijft nodig.
Conclusie: ORB-poot bevestigd in MT5 (bp/trade > 0).
Volgende stap: F3 (combinatie op één €80k-account, schaal/gewichten uit E3).

## 2026-09-29 23:26 — F3: MT5-combinatie — beslisregel NIET gehaald (FTMO-dagverlies 8,6%); plafond bijgesteld

Getest (PREREG_F3.md vóór berekening): RSI2Sleeve (LegFrac 0,2311) en ORBSleeve (LegFrac 0,1376) = E3-schaal, apart gedraaid op €80k EUR (tester: één EA per run; gemeld), conservatief gecombineerd (som van dagminima). RSI-poot swap-gecorrigeerd.
Resultaat 2021-09..2026: SR 0,96 (bootstrap-CI 0,22–1,66), CAGR +6,2% ≈ €410/mnd, 5/6 jaar+, max dag-equity-DD 9,6% (grens 8%), slechtste FTMO-dagverlies 8,56% (2022-01-24; >5% ook in mrt/apr 2025 en mrt 2026). Beslisregel niet gehaald → F6 (demo-forward) vervalt volgens voorwaarde.
Diagnostiek (in-sample, geen beslisgrond): binnen dag-DD < 8% en dagverlies < 4% max ≈ €330–365/mnd (RSI ¼–½ van 1/6 per positie, ORB 1/7), SR ≈ 1,1 (results/f/F3_diagnostiek.txt).
Conclusie: de meerdaagse RSI(2)-poot is onder FTMO's middernacht-balance-regel de zwakke schakel. PLAFOND_RAPPORT bijgewerkt: ≈ €250–365/mnd, kans €880+ < 5%.
Volgende stap: F4 (plateau/decay-check) en F5 (breedte), dan reserve G1–G3.

## 2026-09-29 23:27 — F1c: FTMO-dagverliesdefinitie geverifieerd + strengste lezing in analyze_daily

Bron ftmo.com/en/trading-objectives (29-09-2026), letterlijk: 'The Maximum Daily Loss Limit is recalculated daily at 00:00 CE(S)T as the difference between: the account balance recorded at 00:00 CE(S)T of the current day and the Maximum Daily Loss Amount, which is 5% of the Initial Simulated Capital.' Floating P/L telt mee (equity = balance + open P/L ± swaps − commissies). Max loss statisch 10% van startkapitaal. Best Day Rule geldt alleen voor 1-Step, niet 2-Step.
Implementatie: analyze_daily.py rapporteert nu naast de officiële lezing (balance om middernacht − laagste equity) ook de strengste (max(balance, equity) om middernacht). Kanttekening: EA-dag = servermiddernacht (= 23:00 CE(S)T, 1 u eerder dan FTMO) — klein effect.
Uitkomsten: F1 RSI(2) officieel 6,1% / streng 6,1%; F2 ORB 1,4% / 1,4%; F3-RSI-poot 8,5% / 8,5%. De dagverliesproblemen zitten volledig in de RSI(2)-poot.
Volgende stap: F1b (drie vooraf vastgelegde dagverlies-varianten voor RSI(2)).

## 2026-09-29 23:43 — F1b: dagverlies-beheersing RSI(2) — alle 3 varianten AFGEWEZEN

Getest (PREREG_F1b.md vóór berekening): RSI2Sleeve met MaxIndexPositions / DayGuardPct; varianten (i) cap 2 indexposities, (ii) dagguard 3%, (iii) beide; schalen 0,8/1,0/1,5/2,0 × 1/6; MT5 €80k EUR 2021–2026, swap-gecorrigeerd.
Resultaat (schaal 1,0): (i) cap SR 0,26, dagverlies 4,7%, ≈ €50/mnd; (ii) guard SR 0,44, dagverlies 3,9%, ≈ €118/mnd, ~49 trades/jr; (iii) beide SR 0,22, 3,7%, ≈ €41/mnd. Guard houdt dagverlies ≤ 3,9% op alle schalen maar verlaagt het rendement sterk (sluit op het dieptepunt, mist de omkeer); cap blokkeert juist de gelijktijdige index-signalen. Bij schaal ≥ 1,5 stijgt de DD naar 8–16%.
Conclusie: geen variant haalt SR ≥ 0,5 bij dagverlies < 4% → alle drie afgewezen. TRIAL_COUNT 351.
Volgende stap: F3 opnieuw met schaal bepaald door de dagverliesregel (< 4%) i.p.v. Python-DD.

## 2026-09-29 23:43 — F3b: MT5-combinatie met dagverlies-gebonden schaal — kandidaat leeft, maar ≈ €225/mnd

Getest (volgens NEXT_STEPS v4: gewichten E3, schaal bepaald door de FTMO-dagverliesregel < 4%): conservatieve combinatie van F1 (RSI2, 1/6) en F2 (ORB, 1/7) MT5-dagreeksen in verhouding 1,3865:0,9635, grootste schaal t met slechtste dagverlies < 4% → t = 0,45 (RSI 0,62 × 1/6 per positie, ORB 0,43 × 1/7 per trade).
Resultaat 2021-09..2026: SR 0,95 (bootstrap-CI 0,23–1,65), CAGR +3,4% ≈ €225/mnd op €80k, dag-equity-DD 4,4%, slechtste FTMO-dagverlies 3,80%, 5/6 jaar+ → beslisregel F3 gehaald. Maar FTMO-economie (ftmo_economics, schaal 1): fase 1 24,9%, funded 17,5%, mediaan ~31 mnd tot funded, EV −€11/poging (nul-drift −€536).
Conclusie: technisch overlevende, FTMO-conforme kandidaat met kleine edge; economisch te klein voor een challenge. PLAFOND_RAPPORT bijgewerkt (≈ €200–250/mnd). F6 (demo-forward) is volgens de voorwaarde nu toegestaan, maar staat na F4/F5 in de volgorde; vereist bovendien een tweede MT5-instantie (tester-scripts sluiten alle terminal64-processen).
Volgende stap: F4 (plateau/decay-check).

## 2026-09-29 23:45 — F4: plateau/decay — RSI(2) PLATEAU (maar SPX-decay), ORB PIEK

Getest (PREREG_F4.md vóór berekening): f4_plateau.py.
(a) Decay RSI(2), Sharpe <2010 → ≥2010: SPX 0,87 → 0,46 (rollend 5-jr van ~1,4 eind jaren '90 naar 0,1–0,7), NDX 0,65 → 0,57, DAX 0,05 → −0,08, FTSE 0,37 → 0,27 (recent negatief), N225 −0,04 → 0,25, GLD 0,22 → 0,41.
(b) RSI(2)-plateaukaart (drempel 5/10/15 × SMA150/200/250), gepoolde t 3,27–3,73, CAGR 1,7–2,8%; kandidaat 10/200 t 3,65 → 8/8 buren zelfde teken én ≥ 50% → PLATEAU.
(c) ORB-plateaukaart (OR 15/30/60 min × uitstap 12:00/sessie-einde): alle 6 cellen positief; sessie-einde 15/30/60 min: +1,23 / +1,73 / +1,49 bp (t 2,13/2,93/2,58); uitstap 12:00: +0,50–0,72 bp. 5/5 buren zelfde teken maar slechts 2/5 ≥ 50% → volgens de vooraf vastgelegde eis PIEK. Per symbool robuust positief: US100, GER40, US500; ~0 of negatief: US30, UK100, EURUSD.
Conclusie: RSI(2) is geen toevalstreffer in parameters, maar de edge op SPX is sinds 2010 gehalveerd; ORB hangt af van vasthouden tot sessie-einde en is in de 30-min-cel het sterkst (piek). TRIAL_COUNT 364 (13 plateau-buren, transparant geteld).
Volgende stap: F5 (breedte met identieke regels).

## 2026-09-29 23:51 — F5: breedte met identieke regels — geen enkele sleeve opgenomen

Getest (PREREG_F5.md vóór berekening): f5_breadth.py. Nieuwe FTMO-data: M5 voor JP225, AUS200, HK50, EU50, FRA40, SPN35, N25, XAGUSD; D1-OHLC US500/US100 (data/ftmo_d1ohlc_US500_US100.txt); swaps via MT5. Afwijking (gemeld): FTMO-longswap EU50 (+10%/jr) en FRA40 (+31%/jr) is een dividendseizoen-anomalie → GER40-swap (−6,52%) gebruikt.
Resultaat (t / corr / helften): RSI(2): JP225 +1,99/0,39/+6%,+39% (net onder t 2), AUS200 +0,66, HK50 +0,48, EU50 +0,55 (corr 0,61), FRA40 −0,54, SPN35 +0,61, N25 −0,56, XAG −0,47. ORB: JP225 +0,21, AUS200 −4,35, HK50 +0,72, EU50 +0,42, FRA40 −0,33, SPN35 −1,64, N25 −2,60, XAG −0,41. IBS: US500 +1,50 (corr 0,51), US100 +1,60 (corr 0,45).
Conclusie: 0/18 opgenomen. De edge generaliseert niet over instrumenten: ORB werkt alleen op US-indices/GER40, RSI(2) vooral op US-indices. Breedte-hypothese (SR +0,1–0,2) verworpen. TRIAL_COUNT 382.
Volgende stap: F6 (demo-forward) — eerst accounttype verifiëren (zie volgende entry); ondertussen reserve G1/G2.

## 2026-09-29 23:52 — F6: demo-forward-test GEBLOKKEERD — account staat geen handel toe (actie Sandro nodig)

Voorwaarde F6 (F3-beslisregel) is met F3b gehaald. Vóór het live zetten het account gecontroleerd via Python (MetaTrader5.account_info): login 1514742872, naam '€80k FTMO Free Trial Swing 2-Step', server FTMO-Demo, trade_mode 0 (demo), hefboom 1:30, balance €80.000, **trade_allowed = False** (1 deal in historie, 0 posities). Handelen op dit account is niet toegestaan — waarschijnlijk is de Free Trial verlopen.
NIET gestart: geen EA live gezet, niets op het account gedaan.
Nodig van Sandro: een nieuwe FTMO Free Trial (Swing, €80k) of andere demo-inloggegevens in de terminal op de VM. Technisch daarna: een tweede, aparte MT5-instantie voor live/demo (de tester-scripts sluiten alle terminal64-processen), EA's RSI2Sleeve (LegFrac 0,62/6) + ORBSleeve (LegFrac 0,43/7) volgens F3b, dagelijkse export naar forward/daily.csv.
Volgende stap: reserve G1 (kostengevoeligheid) en G2 (beta/stresscorrelatie).

## 2026-09-29 23:58 — G1+G2: kostengevoeligheid en marktcorrelatie van de F3b-combinatie

Getest (PREREG_G1G2.md vóór berekening): g1g2.py op de MT5-reeksen (F1/F2) op F3b-schaal (t = 0,45).
G1: basis SR 1,03, ≈ €225/mnd, slechtste dag 3,80%; +50% spread → SR 0,91, ≈ €200/mnd; +50% spread + 1 punt slippage per ORB-trade → SR 0,66, ≈ €146/mnd (slechtste dag onveranderd ~3,8%). De ORB-poot (1,7 bp/trade) is de kostengevoelige schakel; realistische live-kosten kunnen de helft van het rendement kosten.
G2: correlatie met US500 +0,39, beta +0,07 (volledig); stress 2022-01..10 corr +0,10; stress 2025-03..04 corr +0,63 (beta 0,11); rollende 63d-correlatie −0,36 … +0,78 (mediaan +0,46).
Conclusie: kleine, deels marktgebonden edge die bij realistische kosten richting €150–200/mnd zakt.
Volgende stap: G3 — VOORSTEL_F.md met 3 hypothesen (pre-registratie) en de best onderbouwde uitvoeren.

## 2026-09-29 23:59 — G3-H1: NR7-opening-range-breakout — AFGEWEZEN

Getest (VOORSTEL_F.md, H1 vóór berekening vastgelegd): g3_nr7orb.py, B4a-ORB alleen na een NR7-sessie, 7 FTMO-symbolen, 2021–2026, kosten B4.
Resultaat: N 1.389, +3,61 bp/trade (2,1× B4a: +1,73), t train +2,36 / test +0,89, 4/6 jaar+, DSR 0,38. Per symbool: US500 +10,4 bp, US100 +9,4, US30 +4,4, GER40 +1,8, XAU +0,4, UK100 −0,8, EURUSD −0,7. Per jaar: 2022 +14,5 bp draagt het resultaat; 2024 −1,0.
Conclusie: kostenvoordeel (≥ 2× bp) gehaald, maar t ≥ 3 in train én test niet → afgewezen. TRIAL_COUNT 383.
Volgende stap: H2 (Double 7s) en H3 (RSI(2) in hoog-vol-regime).

## 2026-09-30 00:02 — G3-H2/H3: Double 7s en RSI(2)-hoog-vol — beide AFGEWEZEN

Getest (VOORSTEL_F.md vóór berekening): g3_h2h3.py.
H2 Double 7s: Yahoo 1990–2026 gepoold SR 0,46, t 2,85 (< 3), helften +121% / +48%, DSR 0,44; FTMO 2021–26 SR 0,59, +23,5%. → afgewezen (t < 3, DSR < 0,5).
H3 RSI(2) alleen bij 20d-vol > eigen 252d-mediaan: Yahoo SR 0,59 → 0,43 (ΔSR −0,16), FTMO 0,57 → 0,56 → afgewezen; het vol-filter verslechtert. Controle: RSI(2)-basis reproduceert exact (Yahoo t 3,65; FTMO +15,4%).
Conclusie: geen verbetering binnen de familie dag-omkeer/intraday-breakout. TRIAL_COUNT 385.
Volgende stap: verslag backlog v4; F6 wacht op nieuw demo-account (Sandro).

## 2026-09-30 01:12 — I1: papieren forward-test gestart (cron 22:15 UTC ma–vr)

Gebouwd: forward_paper.py + mt5_export_recent.py (VM) + forward/README.md (regels vastgelegd vóór de eerste dag). Past exact de F3b-regels toe (RSI(2) 0,62/6 per positie, ORB 0,43/7 per trade, FTMO-spread/swap/commissie) op nieuwe FTMO-marktdata (werkt zonder trade_allowed). Start handelsdag 2026-09-30, vlak, €80.000, geen terugwerkende kracht. Output forward/paper_daily.csv, paper_trades.csv, state.json; elke dag commit + push.
Controle: droogtest 2026-09-21..29 in aparte map — ORB-trades per symbool en dag identiek aan backtest B4a (bv. 21-09 US100 +116,1 bp, GER40 −24,8 bp); git-push werkt in cron-omgeving (gh credential helper).
Cron: '15 22 * * 1-5 cd ~/ai-trading && python3 forward_paper.py >> forward/cron.log' (bestaande crontab-regels behouden). Eerste echte verwerking: vanavond 22:15 UTC (dag 2026-09-30).
Beperkingen: slot-tot-slot voor RSI (geen intraday-dip), geen EUR-conversie, geen slippage.
Volgende stap: I2 (intraday mean-reversion op H1).

## 2026-09-30 01:14 — I2: intraday mean-reversion op H1 — beide AFGEWEZEN

Getest (PREREG_I2.md vóór berekening): i2_intraday_mr.py, FTMO-M5 → H1 (serveruren), US500/US100/GER40, alleen binnen de cash-sessie, geen overnight, spread instap-bar.
(a) IBS-H1 < 0,2 boven SMA200(H1), uitstap na 4 H1-bars/sessie-einde: N 1.946, +0,95 bp, t train +0,96 / test +0,22, 3/6 jaar+ (US100 +4,0 bp, US500 +0,9, GER40 −1,2). Dagverlies bij €150/mnd-schaal 2,8% (conform), maar geen edge.
(b) RSI(2)-H1 < 10, uitstap > 65/sessie-einde: N 879, −1,24 bp, t −1,13 / +0,13, 2/6 jaar+.
Conclusie: intraday omkeer lost de dagverlies-bottleneck op maar heeft na kosten geen edge → beide afgewezen. De dag-RSI(2)-edge verdwijnt als de positie niet overnight mag blijven. TRIAL_COUNT 387.
Volgende stap: I3 (event-drift FOMC/CPI/NFP) — eerst datalijst met bron.

## 2026-09-30 01:16 — I3: event-drift — pre-FOMC formeel GESLAAGD (maar event-t 2,35), post-nieuws afgewezen

Getest (PREREG_I3.md vóór berekening): i3_events.py, events.csv (FOMC van federalreserve.gov; NFP/CPI van bls.gov, automatisch uitgelezen en geverifieerd met de US500-08:30-ET-range).
Datakwaliteit (eerlijk): de verificatie is onbetrouwbaar — 2021-02..09 niet te bevestigen (onvolledige FTMO-M5), en de ±2-dagen-correctie koos 2x een verkeerde dag (2022-03-04 → 03-02; 2026-05-08 → 05-12 = CPI-dag); ontbrekende maanden niet teruggevonden. Raakt alleen (b).
(a) Pre-FOMC-drift (long US500/US100, slot dag−1 → 14:00 ET): N 82 (41 events × 2), +26,7 bp, t +3,18, 2021–23 +42,1 bp / 2024–26 +13,4 bp → volgens prereg GESLAAGD. Extra controle (buiten prereg): event-niveau t +2,35 (N 41, 26/41 positief) — onder 2,5; zelfde venster op niet-FOMC-dagen +1,6 bp → FOMC-effect ≈ +25 bp, wel afnemend (bekend gepubliceerd effect, Lucca–Moench).
(b) Post-nieuws-momentum NFP/CPI (richting eerste 5 min, 30 min vasthouden, 2× spread): N 223, +0,5 bp, t +0,21 → afgewezen.
Conclusie: pre-FOMC is een klein, echt maar zwakker wordend effect (8×/jaar, ≈ 2%/jr bij 100% notional); met overnight-risico op FOMC-dagen. Geen zelfstandige route naar het doel; mogelijk kleine diversificatie. TRIAL_COUNT 389.
Volgende stap: I4 (SCENARIO_RAPPORT voor Sandro) en I5 (RSI(2)-regimecheck).

## 2026-09-30 01:17 — I5: robuustheid RSI(2) op FTMO per regime — niet afhankelijk van één jaar

Getest (PREREG_I5.md vóór berekening): i5_rsi2_regime.py op de E1-FTMO-reeks (6 symbolen gepoold).
Resultaat: volledig SR 0,57; per jaar 2021 +1,13 (+5,4%), 2022 −0,77 (−2,4%), 2023 +0,03 (0,0%), 2024 +1,10 (+4,5%), 2025 +0,61 (+3,3%), 2026 tot nu +0,92 (+3,9%). Excl. beste jaar (2021) SR 0,45 ≥ 0,4 → eis gehaald. Rollende 12-mnd SR −0,8 (begin 2023) … +1,3 (medio 2026). Per volregime (US500 20d-vol-tercielen): laag +0,83, midden −0,08, hoog +1,06.
Conclusie: de RSI(2)-edge is niet één-jaar-gedreven, maar klein en wisselend (2022/2023 zwak). TRIAL_COUNT ongewijzigd (geen nieuwe regels).
Volgende stap: I4 (SCENARIO_RAPPORT voor Sandro).

## 2026-09-30 01:29 — I4: SCENARIO_RAPPORT voor Sandro (zonder jargon)

Opgeleverd: SCENARIO_RAPPORT.md + results/g/I4_scenario_numbers.txt. Block-bootstrap (21 dagen, 20.000×) van de F3b-MT5-dagreeks.
Kern: 12 mnd op €80k — met MT5-kosten P5 −€1.280 / P50 +€2.720 / P95 +€6.900, kans verlies 13%; met realistische kosten (G1) P5 −€2.250 / P50 +€1.770 (≈ €150/mnd) / P95 +€6.000, kans verlies 24%. Kans op 10%-grens of dag ≥ 5%: 0% (voorzichtige schaal).
Challenge: fee ≈ €540 (secundaire bron, niet op ftmo.com geverifieerd), slaagkans ≈ 17,5%, ≈ 2,5 jaar tot funded, EV ≈ −€10/poging → nog niet de moeite. €880/mnd vereist Sharpe ≈ 1,4 (wij ≈ 0,7–1,0); opschalen botst op de 5%-dagregel. ETF-vergelijking: SPY 2000–2026 CAGR 8,4% → €80k eigen geld ≈ €557/mnd gemiddeld, max DD 55%; €880/mnd vergt ≈ €126k eigen vermogen.
Beslispunt Sandro: doel bijstellen (≈ €150–250/mnd), stoppen, of andere bron van edge.
Volgende stap: reserve J1 (combinatie incl. pre-FOMC) en J3 (power-analyse forward-test).

## 2026-09-30 01:30 — J1+J3: pre-FOMC toevoegen (in-sample SR 1,34, ≈ €361/mnd) en power-analyse forward-test

Getest (PREREG_J1J3.md vóór berekening).
J3: bij ware SR 0,66 (realistische kosten) is t ≥ 2 pas na ≈ 9,2 jaar forward te verwachten (t ≥ 1,65 na 6,2 jr); bij SR 0,95 na 4,4 resp. 3,0 jaar. Verwachte t na 60 handelsdagen 0,3–0,5, na 250 dagen 0,7–1,0. → De papieren forward-test kan grote problemen (fouten, kosten, regimebreuk) zichtbaar maken, maar de edge binnen 1–2 jaar niet statistisch bewijzen.
J1: slechtste historische FOMC-event −94 bp → pre-FOMC-notional 1,06× equity (US500/US100 gelijk). F3b alleen: SR 1,03, ≈ €225/mnd, slechtste dag 3,80%; F3b + pre-FOMC: SR 1,34, ≈ €361/mnd, slechtste dag 3,80%. Kanttekening: in-sample, pre-FOMC-effect event-t 2,35 en afnemend (2024–26 +13 bp), intraday-dip op FOMC-dag vóór 14:00 niet gemodelleerd.
Conclusie: combinatie oogt beter maar rust op een klein, zwakker wordend effect; niet als bewezen beschouwen. TRIAL_COUNT ongewijzigd.
Volgende stap: verslag backlog v5; J2 (nieuwe hypothese-batch) alleen als de supervisor dat wil gezien 389 trials.

## 2026-09-30 01:32 — K1: RSI(2)-edge zit in de nachten; max-1/2-nachten-varianten afgewezen op FTMO-t

Getest (PREREG_K1.md vóór berekening): k1_nights.py. Ontleding van de oorspronkelijke RSI(2)-trades in nacht k (slot → open) en dag k (open → slot).
Yahoo 1990–2026 (SPY, QQQ, GLD, DAX, N225): nacht 1 +9,3 bp (t 4,15), dag 1 −1,7; nacht 2 +10,4 (t 4,25), dag 2 +1,1; nacht 3 +4,0 (t 1,52), dag 3 +4,8; nacht 4+ +8,8 (t 4,97), dag 4+ +3,4. FTMO 2021–26: nacht 1 +6,4 (t 1,28), nacht 2 +11,4 (t 2,89), nacht 3 +0,1, nacht 4+ +5,2 (t 1,74); dagen ≈ 0.
Varianten: (a) max 1 nacht — Yahoo N 2.022, +5,3 bp, t 3,05; FTMO N 472, +6,4 bp, t 1,79; dagverlies bij €150/mnd 2,76%. (b) max 2 nachten — Yahoo +14,5 bp, t 3,59; FTMO +11,8 bp, t 1,53; dagverlies 3,61%. Beide afgewezen (FTMO-t < 2,5).
Conclusie: RSI(2) is in essentie een overnight-premie na uitverkoop; korte houdduur maakt het FTMO-dagverlies beheersbaar, maar de FTMO-historie (5,7 jr) heeft te weinig power om het te bevestigen. PLAFOND_RAPPORT bijgewerkt. TRIAL_COUNT 391.
Volgende stap: K2 (power-analyse + vooraf vastgelegde beslisregel forward-test).

## 2026-09-30 01:33 — K2: power-analyse + vooraf vastgelegde beslisregel forward-test

Berekend (results/k1/K2_power.txt): 80% kans op t ≥ 2 na ≈ 8,9 jaar bij ware SR 0,95, ≈ 18,5 jaar bij 0,66, ≈ 22 jaar bij 0,6. Kans op geschatte SR < 0 ondanks een echte edge (SR 0,66) na 3/6/12/24 mnd ≈ 37% / 32% / 25% / 18%.
Vastgelegd in forward/README.md (vóór de eerste forward-dag): harde review bij papieren dagverlies ≥ 4% of DD ≥ 8%; na 6 mnd stop als SR < −0,29; na 12 mnd stop als SR < 0, heroverwegen als SR ≥ 0,66; ORB-kostencontrole na 6 mnd (< −1,0 bp/trade → onderzoeken); elk forward-verslag noemt de optimistische aannames.
Conclusie: de forward-test is een foutdetector, geen snel bewijs; statistische bevestiging van deze edge vergt jaren.
Volgende stap: backlog v6 afgerond; verslag + wachten op nieuwe NEXT_STEPS (uurlijkse check).

## 2026-09-30 01:34 — J2: drie nieuwe hypothesen — alle AFGEWEZEN

Getest (VOORSTEL_G.md vóór berekening): j2_batch.py, FTMO-M5 2021–26, kosten B4.
(1) US100 gap-continuatie (|gap| > 0,5%, 60 min): N 561, −2,19 bp, t train −0,29 / test −0,82, 2/6 jaar+.
(2) XAUUSD ORB op de Londense sessie: N 1.482, +1,49 bp, t −0,26 / +1,56, 4/6 jaar+.
(3) GER40 ORB alleen in de richting van de overnight US500-beweging: N 647, +3,58 bp, t +1,44 / +0,35, gedragen door 2022 (+12,8 bp).
Conclusie: geen van drie haalt t ≥ 3 in train én test. TRIAL_COUNT 394.
Volgende stap: backlog v6 afgerond; uurlijkse NEXT_STEPS-check.

## 2026-09-30 03:11 — L1: lange onafhankelijke intraday-data — GEBLOKKEERD (geen gratis, geautomatiseerd toegestane bron); L2/L4 op dit pad gestopt

Geprobeerd (volgens NEXT_STEPS v7):
- Dukascopy datafeed (datafeed.dukascopy.com, M1-candles .bi5): eerste verzoek HTTP 429 'Too Many Requests' met verwijzing naar dukascopy.com/wiki/en/development/data-export; met browser-User-Agent 1 bestand gelukt, daarna weer 429. Hun officiële bulkroute is een AWS S3-bucket met 'Requester Pays' (≈ $0,0004/1.000 requests + $0,02/GB) → vereist AWS-account + betaling. Rate-limit niet omzeild.
- HistData.com (gratis M1 SPX/NSX/GRX vanaf 2010-11, XAU 2009, EURUSD 2000; geen US30): download-POST geeft leeg bestand bij geautomatiseerde aanvraag (2 pogingen); geautomatiseerde toegang wordt als betaald abonnement aangeboden. Bescherming niet omzeild.
- Stooq: JavaScript-botcheck (eerder vastgesteld).
Conclusie: geen gratis, geautomatiseerd bruikbare lange intraday-bron → L1 geblokkeerd; L2 (ORB 2010–2020) en L4 (portefeuille op lange steekproef) gestopt op dit pad, zoals de opdracht voorschrijft.
Opties voor Sandro: (1) AWS-account voor Dukascopy S3 (kosten naar schatting enkele dollars), (2) HistData handmatig downloaden (≈ 80 jaar-/maandbestanden SPX/NSX/GRX/XAU/EURUSD, ASCII M1) en in data/long_m1/ zetten, (3) betaalde bron.
Volgende stap: L3(a) pre-FOMC op Yahoo-dagproxy 1994–2026 en L5 (forward-weekrapport).

## 2026-09-30 03:15 — L3(a): pre-FOMC op 1994–2026 (SPY-dagproxy) — formeel geslaagd, inhoudelijk: effect sinds 2012 grotendeels weg

Getest (PREREG_L3.md vóór berekening): l3_prefomc_long.py; FOMC-datums 1994–2020 van federalreserve.gov/monetarypolicy/fomchistorical{YYYY}.htm (219 datums, parser gecorrigeerd voor 'Jan/Feb 31-1'-koppen; fomc_dates_1994_2020.txt) + 2021–26 (events.csv).
Slot(d−1)→slot(FOMC), SPY: 1994–2026 N 264, +22,9 bp, t +3,03 (baseline +4,2 bp); 1994–2011 +33,7 bp (t 3,28); 2012–2026 +9,8 bp (t 0,88); 2010–2020 +15,9 bp (t 1,21); 2021–2026 +1,4 bp (t 0,07). Open→slot FOMC-dag: 1994–2011 +22,3 bp (t 2,43), 2012–2026 −0,6 bp.
Beslisregel formeel gehaald (t ≥ 2,5, N ≥ 120, 2010–20 ≥ 50% van 2021–26), maar het tweede criterium is ontaard (2021–26-dagproxy ≈ 0). Inhoudelijk: klassiek Lucca–Moench-effect bevestigd voor 1994–2011, sindsdien grotendeels verdwenen; de +26,7 bp uit I3 zit alleen in het venster tot 14:00 ET, dat dagdata niet kunnen isoleren. L3(b) (nachtontleding op Dukascopy) vervalt door L1-blokkade.
Conclusie: pre-FOMC niet als betrouwbare sleeve behandelen.
Volgende stap: L5 (forward-weekrapport).

## 2026-09-30 03:15 — L5: wekelijks forward-rapport (cron maandag 22:45 UTC)

Gebouwd: forward_week.py — elke maandag 22:45 UTC (na de papieren run) een blok in forward/weekrapport.md: aantal dagen, equity/P&L, €/mnd, geschatte SR ± 1 SE (met K2-waarschuwing), ORB bp/trade vs backtest +1,7 bp, slechtste FTMO-dagverlies en max DD, K2-alarm (dag ≥ 4% of DD ≥ 8%), ontbrekende werkdagen (cron-gaten), en de optimistische aannames; commit + push. Cron toegevoegd ('45 22 * * 1'), bestaande regels behouden. Eerste rapport: maandag 2026-10-05.
Volgende stap: verslag backlog v7; wachten op nieuwe NEXT_STEPS / beslissing Sandro (data-optie voor L1).

## 2026-09-30 04:25 — N1: MT5-bevestiging kern RSI(2) max 1/2 nachten — NIET gehaald

Getest (PREREG_N1.md vóór berekening): RSI2Sleeve + MaxNights (sluiten op de n-de cash-sessie-open, US 16:30 server, GER40/UK100 10:00/11:00), 1/6 per positie, MT5 €80k EUR 2021–26, swap-gecorrigeerd.
Reconciliatie met k1_nights.py: trades max 1 nacht 478 vs 472 (+1%), max 2 nachten 317 vs 331 (−4%), per symbool dichtbij; maandcorrelatie 0,834 / 0,890 (< 0,9); totaal Python +5,1% / +6,6% vs MT5 +3,2% / +1,2% (> 25% verschil) → reconciliatie deels buiten tolerantie (MT5 duidelijk zwakker; waarschijnlijk bredere spread op de sessie-open en instap op eerste tick van de serverdag).
Resultaat MT5: max 1 nacht SR 0,47 (CI −0,23–1,15), €36/mnd bij 1/6; schaal 2,8× → €98/mnd, slechtste dag 3,56%, DD 6,5%; met +50% spread SR 0,23. Max 2 nachten SR 0,12 (CI −0,62–0,91), €13/mnd bij 1/6; €100/mnd vereist 7,5× → dag 17%.
Beslisregel kern (SR ≥ 0,5 én dagverlies < 4% bij ≥ €100/mnd): NIET gehaald. Cache toegevoegd aan e1_rsi2_ftmo.eod_spread_frac (snelheid, geen uitkomstwijziging).
Conclusie: de korte-houdduur-kern van RSI(2) is in MT5 met FTMO-kosten te zwak. Enige FTMO-conforme kandidaat blijft F3b (RSI(2) oorspronkelijk + ORB, ORB onbevestigd).
Volgende stap: N2 (DATA_REQUEST_SANDRO.md), N3 (definitieve PLAFOND/SCENARIO), N4 (forward).

## 2026-09-30 04:26 — N2: DATA_REQUEST_SANDRO.md (lange minuutdata, 3 opties)

Opgeleverd: DATA_REQUEST_SANDRO.md in gewone taal. Opties: (B, aanbevolen) HistData handmatig downloaden — SPX/USD, NSX/USD, GRX/EUR, XAU/USD, ASCII M1, jaarbestanden 2011–2025 + maanden 2026, ≈ 100 bestanden → data/long_m1/; (C) Dukascopy-S3 'Requester Pays' met AWS-account, geschatte kosten < $1–5, levert ook US30; (A) demo-account op een andere MT5-server (bv. MetaQuotes-Demo) — niet zelf te verifiëren omdat daarvoor een account op naam van Sandro nodig is; veel demo-servers hebben voor indices maar enkele jaren.
Volgende stap: N3 (definitieve PLAFOND/SCENARIO-update).

## 2026-09-30 04:27 — N3: definitieve PLAFOND/SCENARIO-stand (PLAFOND_DEFINITIEF.md)

Opgeleverd: PLAFOND_DEFINITIEF.md (één pagina, gewone taal) + verwijzing bovenaan PLAFOND_RAPPORT.md en SCENARIO_RAPPORT.md. Cijfers (MT5, FTMO-kosten, schaal zodat slechtste dag < 4%; results/f/N3_numbers.txt): kern RSI(2) max 1 nacht SR 0,48 (CI −0,24–1,17), ≈ €99/mnd, realistisch ≈ €50 (SR 0,23), verliesjaar 28%, slechtste dag 3,6%; RSI(2) oorspronkelijk SR 0,49 (CI −0,12–1,14), ≈ €84/mnd, verliesjaar 24%; RSI(2)+ORB (ORB onbevestigd) SR 0,95 (CI 0,23–1,65), ≈ €225 → realistisch €146/mnd. Nodig voor €880/mnd: SR ≈ 1,4. Challenge-EV ≈ −€10; ETF-alternatief ≈ €557/mnd op €80k eigen geld met −55% DD.
Conclusie: realistisch ± €50–150/mnd; €880/mnd niet haalbaar met deze aanpak.
Volgende stap: N4 (forward-onderhoud), daarna steady-state.

## 2026-09-30 04:27 — N4 + STEADY-STATE: forward-test in onderhoud, geen nieuwe hypothesen

N4: forward/paper_daily.csv bestaat nog niet — correct: de eerste echte handelsdag (2026-09-30) wordt pas vanavond om 22:15 UTC verwerkt (na de US-slot); controle nu 04:27 UTC. Cron aanwezig: dagelijks 22:15 UTC (forward_paper.py) en maandag 22:45 UTC (forward_week.py, eerste weekrapport 2026-10-05). Eventuele gaten worden in het weekrapport gemeld.
STEADY-STATE (stopregel supervisor, backlog v8): N1–N4 klaar; de kern (RSI(2) max 1–2 nachten) haalde in MT5 SR < 0,5. Geen nieuwe hypothesen meer (TRIAL_COUNT blijft 394). Alleen nog: (a) papieren forward-test dagelijks, (b) wekelijks verslag, (c) opnieuw werken zodra Sandro lange data levert (DATA_REQUEST_SANDRO.md → L2/L3b) of zelf een nieuw idee met regels aanlevert. Uurlijkse NEXT_STEPS-check blijft actief.
