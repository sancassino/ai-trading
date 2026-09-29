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
