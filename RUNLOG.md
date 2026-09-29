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
