RUNLOG-regel: 2026-09-30 ~19:10Z · AUDITOR-1 · AUDIT_1 deel 1 gepusht. 2026-09-30 ~21:30Z · AUDIT_1 deel 2 (FTMO-engine validatie D-087 + reserve-hygiëne post-D-084) gepusht op claude/auditor-1.

# AUDIT_1 — onafhankelijke audit (red team), deel 1

Eigen code in `audit/` (geen import van engine/ of catalogus/ in de replicatie). Data afgekapt op ≤ 2024-12-31 (`audit/common.py`). Reproduceren: `audit/run_all.sh` (nog niet gedraaid; uitvoer per script is wel te reproduceren).
**Openbaarmaking:** door een debug-print zag ik één keer de jaar-excess van P-ETF-a voor 2025 (+12,3%) en 2026 t/m nu (−0,5%). Niet gebruikt; code kapt sindsdien af op 2024. Reserve is door mij verder niet aangeraakt.

## Scorekaart
| # | Punt | Oordeel | Bewijs |
|---|---|---|---|
| 1 | Replicatie P-ETF-a (SR 0,94 / CAGR 7,4% / maxDD 11,2%) | **PASS** | Mijn code, engine-gedrag nagebootst: SR 0,935, CAGR 7,37%, maxDD 11,23%, zelfde start 2001-04-02, n=5979. C02-sleeve identiek (verschil 0,0), C52-sleeve 4e cijfer achter de komma. `audit/rep_petf.py` |
| 2a | Lookahead in signalen | **PASS** | Onafhankelijk uit de spec herleid; geen toekomstinformatie (σ t/m i−1, signaal t/m slot t, positie werkt vanaf t+1). |
| 2b | Uitvoeringstijd (signaal en uitvoering op dezelfde slotkoers) | **TWIJFEL** | 1 dag later uitvoeren: SR 0,929→0,882 (2 dagen: 0,877). Fase van het maandraster (beslisdag = maandeinde ±15 d): SR min 0,77 / mediaan 0,84 / max 0,93; het kalendermaandeinde is de top van de buurt (C02-sleeve 0,72 vs 0,54–0,64 elders). Realistisch verwachtingsgetal ≈ 0,85, niet 0,94. `rep_petf.py`, `rep_phase.py` |
| 2c | Dividend/adjclose | **PASS (conservatief)** | NDX/DJI/N225 zonder dividend: toevoegen geeft SR 0,968. SPY vs SPX_TR in C52: SR 0,928 vs 0,929. SPY-adjclose wijkt dagelijks af van SPX_TR (std 17 bp, 2008: 48 bp; max 294 bp op 2008-10-13) maar zonder effect op het resultaat. |
| 2d | Synthetische obligatie | **PASS** | Eigen herbouw uit ^TNX (D=8, C=80) identiek aan data/derived. Echte IEF (vanaf 2002-11): SR 1,016 vs synthetisch 0,980 → synthetisch is conservatief. Zonder obligatiepoot SR 0,80; zonder goud 0,81. |
| 2e | Feestdag-/kalendergaten | **FAIL (klein)** | `catalogus/C52_allweather.py:20-21`: een activum met één ontbrekende dag in het 60d-venster krijgt die maand gewicht 0. 51 van 288 maandeinden getroffen (30× 1 asset weg, 21× ≤1 asset beschikbaar). Effect +0,006 SR (schoon 0,929 vs quirk 0,935). C02 vaste 1/5-weging: 0,923. |
| 2f | Dubbeltelling kasrente / excess | **PASS** | Excess = totaal − rf op eigen kalender per sleeve; kasrente één keer. rf-bron (DTB3, ^IRX, US3M): SR 0,923–0,931. |
| 2g | Survivorship | **TWIJFEL** | Indexreeksen zelf survivorship-vrij, maar universum (SPX/NDX/DJI/DAX/N225 + obligatie + goud) is gekozen ná `trend-research.md` (24-09) op dezelfde data, en de steekproef 2001–2024 heeft obligatie- en goudbull. Decompositie: SR 2001–10 1,07; 2011–24 0,84; 2021–24 0,53; 2015–24 0,66. |
| 2h | Reserve 2025→ vóór vrijgave aangeraakt | **TWIJFEL** | Nieuwe-stijl: PASS — geen TRIALS-rij `reserve`, geen reserve_run.md/log, `r2_reserve.py` geblokkeerd (guard), alle onderzochte scripts kappen op 2024 (r5/r6/r7/r8, qa_*, r2_*, port3/4), forward-bestanden alleen header. **Maar** `trend-research.md` (24-09, "2000–2026") en `Bevindingen_MomentumRotatie.md` gebruikten 2025–26-data voor trend op SP500/Nasdaq/DAX/Dow + goud/obligaties; de hypothese is dus al met reservedata gevormd. D-031 ("door niemand aangeraakt") is te sterk. |
| 2i | Forward-papier: laatste rij telt als maandeinde | **FAIL** | `catalogus/_common.py:12` (`np.r_[..., True]`). Test `audit/forward_lastday.py` (afgekapte data vs volledige run): dagrendement laatste dag wijkt −0,3…−0,45 bp af voor C52L en −1,3 bp voor C02 bij een schijn-flip (>1 bp-band); eerdere dagen exact gelijk. Eerst gelogde waarde is "officieel" → structurele negatieve afwijking in forward-log. |
| 2j | Stale dump | **TWIJFEL (klein)** | `results/R2/series/*` (R2-export) wijkt af van `engine/forward.series` (P-ETF-a SR 0,925 vs 0,935 via dezelfde pijplijn; adjclose-herzieningen). |
| 3a | BH-FDR | **PASS** | Eigen BH op TRIALS.csv: max |q−q_eigen| = 5e-5 (main m=27, uitvoerder2-r m=29). Hogere familie (+414 nulhyp p=0,5): C52 lang q 0,010; C02/C55/C44 q ≈ 0,045 → blijft < 0,10. |
| 3b | Trial-teller | **PASS met opmerkingen** | 440 = 414 + 26 (CAT1 7, CAT2 6, CAT3 8, CAT4 5); op uitvoerder2-r 442 (S11, C67). Opmerkingen: `rep_b2b_rsi2` staat met p in BH maar telt niet mee (conservatief); BH-familie (27–29) ≠ TRIAL_COUNT (440); vehikelkeuze niet geteld: C02 primair cfd (t 3,14, SR 0,32) maar P-ETF-a gebruikt etf (SR 0,465) als "vehikelrapport"; C17 staat als "afgewezen" (TRIALS.csv:9) maar zit in shortlist/P1; C45 "door G-ontdekking" maar valt af. Niet-gedraaide prereg-regels (C13, C14, C23/24/28/31, C46/47, C62–64, C65/C66/C68) zijn met reden gedocumenteerd. |
| 3c | t-waarden ("dag-geclusterd") | **PASS (label TWIJFEL)** | t is min(NW L=5, blokbootstrap 21) op de dagreeks (`engine/run_rule.py:365`), niet geclusterd. Mijn t: C52L plain 3,94, NW21 4,03, NW63 4,16, boot 4,1–4,2; C02 3,3–3,8; P-ETF-a 4,4–5,0. Autocorrelatie ≈ 0. Engine-t is dus eerder te laag dan te hoog. |
| 3d | DSR | **TWIJFEL** | Mijn benadering (SR-SE 0,25): P-ETF-a DSR 0,99 (N=8), 0,96 (26), 0,95 (40), **0,78 (N=440)**; C52 lang 0,66 bij N=440. Beperking: benadering, varianties gelijk verondersteld. `stat_t.py` |
| 3e | Nul-kalibratie `r5_crossmarket.py` | **PASS (methode) / TWIJFEL (kracht)** | Stationaire bootstrap klopt (`:64-68`). Maar de test vergelijkt de 21-daagse benadering (waargenomen ΔSR +0,006, nul −0,006 ± 0,085, p 0,459) terwijl de exacte maandeinde-regel +0,101 geeft (`:106-108`). Die kloof van ≈ 0,1 SR = dezelfde fase-gevoeligheid als 2b: het "effect" zit in het kalendermaandeinde, niet in trendvolging. Blokken van gemiddeld 252 d behouden jaarschaal-trend, dus weinig power (90%-BI −0,06…+0,27). Conclusie van het team ("niet gerepliceerd op SR, alleen DD-beschermend") wordt ondersteund. |
| 3f | Alfa of bètapremie | **TWIJFEL** | P-ETF-a SR 0,93 vs 60/40 0,56 (zelfde dagen); alfa vs 60/40 3,5%/jr (t 3,7), vs B&H 5 indices 4,0%/jr (t 4,1), beta 0,2–0,35; C02 alfa vs B&H 3,8% (t 2,45). De "ontdekking"-H0 (excess > 0) wordt door elke long-gebiaste regel gehaald (equity-/obligatiepremie). |

## Ernstigste risico's voor de conclusies (volgorde)
1. **Te hoog verwachtingsgetal:** SR 0,94 is de gunstigste fase/uitvoering. Realistisch ≈ 0,85 (fasemediaan) of 0,88 (+1 dag), en 2021–24 slechts 0,53. Dit geldt boven op winnaarsvloek (DSR 0,78 bij N=440).
2. **Reserve niet zuiver:** hypothese (trend op deze indices + goud/obligaties) is gevormd op data t/m 2026; de eenmalige reserve-toets is daarmee zwakker dan gepresenteerd. Formuleer de reserve-uitkomst dienovereenkomstig.
3. **C02 is geen bewezen timing-alfa:** cross-market nul-kalibratie p 0,46; exact-vs-raster kloof ≈ 0,1 SR; ontdekking = equity-premie met 65% blootstelling.
4. **Forward-papier systematisch te laag gelogd** (laatste-rij-maandeinde, −0,4 tot −1,3 bp/dag) — herstel vóór de 3 maanden papier als "controle" worden gebruikt.
5. **Steekproefperiode:** obligatie- en goudbull 2001–2024; synthetische obligatie is conservatief, maar de assetkeuze is ex post.
6. **Forking paths niet in de teller:** vehikelswitch cfd→etf (C02), C17/C45 inconsistent, portefeuillekeuze P-ETF = C52L + C02 na zien van resultaten.
7. Klein: C52 asset-drop bij kalendergaten; stale R2-dumps.

## Niet gedaan (retarget 19:00Z, D-083…D-086)
De nieuwe prioriteit (cfd-vehikel en FTMO-kosten/swaps, FTMO-simulatoren Q1b/ftmo_economics/mc_daily_ftmo, ORB/B4a cluster-t 2,93→1,81, hygiëne) is **niet** onderzocht: de sessie is door de eigenaar gepauzeerd om credits te sparen. Zie RUNLOG-regel bovenaan; hervatten alleen op aanwijzing van Sandro.

---

# Deel 2 — FTMO-engine validatie (D-087) + reserve-hygiëne post-D-084

Eigen code in `audit/ftmo_compare.py`. Geen import van `engine/` of `catalogus/` in mijn replicatie. CTO-code geladen vanuit een losse kopie (`/tmp/ftmo_cto.py`) van `git show origin/grok/cto-1:engine/ftmo.py`.

## 2A — Onafhankelijke FTMO mini-implementatie

### Geïmplementeerde regels
| Regel | Implementatie in `ftmo_mini()` | Bron |
|---|---|---|
| Dagverlies-limiet | `dd = max(0, −r) × eq`; breach als `dd >= 0.05` (fraction van initial) | FTMO 2-Step spec |
| Max drawdown vloer | statisch: `floor = 1 − 0.10 = 0.90`; breach als `eq − dd ≤ floor` of `eq ≤ floor` | FTMO 2-Step spec |
| Fase 1 | `eq >= 1.10` EN `days_in >= 4`, reset equity=1.0 en teller=0 bij slagen | D-087 |
| Fase 2 | `eq >= 1.05` EN `days_in >= 4`, vanuit gereset startpunt 1.0 | D-087 |
| Volgorde per dag | trough-check → return toepassen → floor-check → teller+1 → breach-reset → fase-check | CTO-volgorde nagemeten |

Implementatie: 44 uitvoerbare regels (exclusief lege regels / commentaar), vectorized NumPy.

### Vergelijkingsresultaten (5 synthetische scenario's, n_paths=20.000, block=21)

| scenario | mini p_pass_1 | mini p_pass_2 | cto p_pass_1 | cto p_pass_2 | Δp1 | Δp2 | oordeel |
|---|---|---|---|---|---|---|---|
| drift+ (μ=+0,08%/d, σ=0,80%) | 0,9718 | 0,9031 | 0,9718 | 0,9031 | 0,0000 | 0,0000 | **PASS** |
| flat (μ=0, σ=0,80%) | 0,3380 | 0,1135 | 0,3380 | 0,1135 | 0,0000 | 0,0000 | **PASS** |
| high-vol (μ=+0,08%/d, σ=1,80%) | 0,9981 | 0,9480 | 0,9981 | 0,9480 | 0,0000 | 0,0000 | **PASS** |
| low-vol (μ=+0,06%/d, σ=0,40%) | 1,0000 | 0,9991 | 1,0000 | 0,9991 | 0,0000 | 0,0000 | **PASS** |
| neg-drift (μ=−0,05%/d, σ=0,80%) | 0,5524 | 0,2424 | 0,5524 | 0,2424 | 0,0000 | 0,0000 | **PASS** |

Cross-seed controle (seed 7, 13, 99, 200, 999; n_paths=10.000): Δp1=Δp2=0.00000 bij alle seeds.

### Grensgedrag (aanvullende controles)
| test | verwacht | mini | cto | OK? |
|---|---|---|---|---|
| Dagverlies exact −5,0% (eq=1.0) | breach (dd=0.05 ≥ 0.05) → p_pass_1=0 | 0,0000 | 0,0000 | ✓ |
| Totaalverlies −10,01% op dag 1 | breach (eq=0.899 < floor 0.90) → p_pass_1=0 | 0,0000 | 0,0000 | ✓ |
| Doelstelling bereikt na 3 dagen (< min_days=4) | geen fase-1-pas | 0,0000 | 0,0000 | ✓ |
| Statische vloer: patroon −8%/+1%×20 (eq nooit < 0.90) | paden kunnen fase 1 halen | 1,0000 | 1,0000 | ✓ |

**Opmerking statische vloer:** vloer is 0,90 ongeacht de piekequity. Na een piek van 1,09 is de vloer nog steeds 0,90 (niet 1,09 × 0,90 = 0,981). Dit is het correcte FTMO-gedrag en is goed geïmplementeerd in `ftmo_ev()`.

### Verdict Prioriteit 1

**PASS** — beide implementaties komen bit-voor-bit overeen (Δ=0,0000) op alle 5 scenarios, 5 seeds en 4 grenstests. Geen fundamentele fout gevonden in `engine/ftmo.py`. Regels (vloer-definitie, dagverlies-limiet, min_days, fase-reset) zijn correct geïmplementeerd.

---

## 2B — Reserve-hygiëne na D-084

**Opschorting D-084:** 2026-09-30 ~20:44 CEST = ~18:44 UTC. Gecontroleerd: alle commits na 18:44 UTC op alle branches.

### Post-opschortings commits (na 18:44 UTC op 2026-09-30)

| commit | tijdstip (UTC) | bestanden | bevat 2025→-data? |
|---|---|---|---|
| `7148ab3` | 19:12 | `engine/ftmo.py` (nieuw) | Nee — code |
| `6ea527d` | 19:14 | `NEXT_STEPS.md` | Nee — log |
| `902d8d0` | 19:16 | `data/ftmo_specs/2026-09-30.csv` (nieuw) | Zie opmerking ① |
| `52fb9d8` | 19:17 | `data/ftmo_specs/2026-09-30.csv` (update) | Zie opmerking ① |
| `3862f0b` | 19:17 | `ftmo_snapshot.sh`, `mt5_symbol_snapshot.py` | Nee — scripts |
| `005b85f` | 19:17 | `RUNLOG.md` | Nee — log |
| `87a1305` | 19:21 | `STRATEGIE_LOG.md` | Nee — log |
| `ca25968` | 19:24 | `BESLUITEN.md`, `CEO_LOG.md` | Nee — beslislog |

**① `data/ftmo_specs/2026-09-30.csv`:** snapshot van FTMO-broker specs (swap-tarieven, bid/ask-spreads, contractgrootten voor 166 symbolen, timestamp 2026-09-30T19:14Z). Dit zijn **broker-operationele parameters** — géén backtesting-koersenreeksen. De "reserve" is de terugtest-koersenreeks vanaf 2025-01-01 (dagsloten indices/ETF's/obligaties/goud). De specs-data zijn categorisch anders: ze gaan over tradingkosten voor het FTMO-live-evaluatieproject, niet over de P-ETF-a backtest.

**Backtesting-koersenbestanden** (`data/daily/`, `data/yahoo/`, `data/derived/`, `data/fred/`, `data/ohlc/`, `data/monthly/`): de laatste commit die één van deze directories aanraakte was vóór D-084-opschorting (`cdecff7` om 14:17 UTC, `8c6e034` om 23:51 UTC vorige dag).

**`data/ftmo_d1ohlc_US500_US100.txt`** (bevat US100-data t/m 2026-09-30): laatste commit om 14:17 UTC — **vóór** opschorting. Wordt gebruikt voor FTMO-live-analyse (forward periode), niet voor de P-ETF-a backtesting reserve. Pre-bestaande situatie, niet nieuw post-D-084.

### Verdict Prioriteit 2

**PASS** — na D-084-opschorting zijn géén backtesting-koersenbestanden (de eigenlijke "reserve" vanaf 2025-01-01) aangeraakt. `data/ftmo_specs/` is broker-operationele data, geen onderdeel van de backtesting-reserve. De pre-bestaande reserve-twijfel (punt 2h uit deel 1: `trend-research.md` gebruikte 2025–26-data vóór de reserve-aanwijzing) is **onveranderd** — dat is een eerder gedocumenteerde schending, niet nieuw.

---

## Overzicht deel 2

| prioriteit | onderwerp | oordeel |
|---|---|---|
| P1 | `engine/ftmo.py` validatie (FTMO 2-Step regels) | **PASS** (Δ=0 op alle tests) |
| P2 | Reserve-hygiëne na D-084-opschorting | **PASS** (geen koersendata aangeraakt) |

Auditor: AUDITOR-1 (claude/auditor-1). Eigen code: `audit/ftmo_compare.py`. Geen engine/-import in replicatie.
