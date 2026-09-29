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
