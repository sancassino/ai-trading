# NEXT_STEPS v92 — Manager, 2026-10-02 23:05 CEST (Faraday N112/N113 PREREG + OPEN N114/N115; U2 N112 FAIL_T + N113 FAIL_COST_GATE; TRIAL 461) — FASE 3: FTMO-EV, doel = FTMO-prop €80k

> **⚠ DOEL v3 (D-083 / **D-101**, bindend):** FTMO-account €80.000 (2-Step). Ambitie €800–900/mnd blijft streef; **D-101** herijkt lat: kandidaten mogen (A) bewezen alfa (t ≥ 2,0) **óf** (B) literatuur-gedragen premie met `ftmo_ev()` EV>0 + overleving ≥0,5 over meerdere periodes + intradag-DD-correctie + forward-papier — altijd gelabeld "beta, geen edge". Eigen-kapitaal GEPARKEERD → `archief/eigen_kapitaal/INDEX.md`.

> **⚠ RESERVE (D-084 / D-094.1):** ETF-reserve geparkeerd. FTMO-kandidaten: reserve 2025+ alleen per CEO-vrijgave. **P1-reserve verbruikt (FAIL).** **ORB-meta reserve verbruikt (D-104 FAIL).**

> **⚠ FORWARD ETF-PAPIER:** loopt door (geen hoofdspoor). Uitvoerder-1 cron.

> **⚠ TEAM (D-090):** Claude = CEO + Auditor. Grok = CTO + Manager + Uitvoerder-2 + Strateeg + Strateeg-2. Kickoffs: `GROK_CTO_INSTRUCTIE.md` op main. Informele Grok-pauze (~01–04 okt) tijdens CEO RISK-REACTIVE/SHOCK-batch — **Manager cadans actief** (v92); D-094 verbiedt stilstand.

> **⚠ BESLUITEN-bron:** tip `origin/claude/upbeat-dirac-g2810q:BESLUITEN.md` eindigt op D-086; D-087…**D-104** op `claude/ftmo-trading-strategy-98mplz` (`8e25e3c` D-104 / `a3c2518` D-103 / `824213f` D-102 / `41e0c44` D-101 / `615bca0` D-100 …). **D-094 + D-094a + D-097…D-104 actief** + **C-028** + **C-029** + **C-030** + **C-031** (`8a68951`) + **C-032** (`f6b0c60`) + **C-033** (`9536912`) + **C-034** (`3ebdea2`) + **C-035** (`f7af392`) + **C-036** (`f3cf632`). CEO tip `7cb6731` ~13:13 CEST 2026-10-02 (geen nieuw D-* na D-104). `EINDSTAND_FTMO.md` = **tussenstand**, geen einde. `VRAGEN_SANDRO_CEO.md` = CEO→Sandro (niet-blokkerend per D-102.4).

> **⚠ D-094 — NOOIT MEER STOPPEN:** Alleen Sandro mag stoppen. Sterft een spoor → ≥2 nieuwe in dezelfde cyclus. Geen agent FTMO-signup / fee-spend.

> **⚠ C-028 — EDGE SEARCH UPGRADE (bindend):** Lane **A** = Yahoo/proxy discovery; Lane **B** = survivors → PREREG + U2. Novelty **≥2/3 NEW_FAMILY**/cyclus. Kill circuit: **5×** cost-gate-PASS→FAIL_T → mandatory family pivot. Zie `EDGE_SEARCH_UPGRADE.md`.

> **⚠ D-102 — RISK-REACTIVE:** FTMO = call-optie-structuur; koers = positief-scheve / vol-reactieve systemen met bewuste schaal. Kern-onderzoek F2-ORB + intradag-DD (CEO tijdens Grok-pauze). Geen agent opent/koopt.

Bindend: D-083…**D-104** (CEO) + **C-028** + **C-029** + **C-030** + **C-031** + **C-032** + **C-033** + **C-034** + **C-035** + **C-036**. Integriteit ongewijzigd: PREREG vóór resultaat, TRIALS append-only, dag-geclusterd t, FDR, echte FTMO-kosten, Auditor onafhankelijk. Dead set niet heropenen als klonen. Lane-A diagnostic ≠ trial. CEO-research trials → `results/ceo/TRIALS_CEO.csv` (aparte boekhouding).

## 0. FASE 3 — FTMO-EV: prioriteiten (D-085…D-104 + C-028…C-036) — **ACTIEF**

**Doel:** P(slagen fase 1+2), P(funded overleven), netto-EV €/mnd, fee/pogingen — `engine/ftmo.py`. Lat = D-101 (A of B).

### Cyclus-uitslag (Manager, 2026-10-02 23:05 CEST — Faraday `791a17c` PREREG N112/N113 + OPEN N114/N115; U2 N112 FAIL_T + N113 FAIL_COST_GATE; TRIAL_COUNT **461**; formal OPEN **N114/N115**)

**Nieuwe D-*:** **geen** (CEO tip blijft `7cb6731`; D-104 `8e25e3c` tip besluit). **Nieuwe C-*:** **geen** (CTO tip blijft `f3cf632` C-036; geen concurrent tip-race op `origin/grok/cto-1` na fetch).

**Faraday `791a17c` (~22:58 CEST):** absorb C-036 N110/N111 DIAG_FAIL. Lane-B PREREG from S2 `35e38ac` cycle_2240:
- **N112** GAS_EQUITY_MACRO (UNG z40/thr±1.5/stress_buy → US500cash session-flat 15:30→21:00 CET; gate 2.34; NEW_FAMILY) — `PREREG_FTMO_N112_GAS_EQUITY_MACRO.md`
- **N113** SILVER_GOLD_RATIO (SLV/GLD z40/thr±1.0/fade_extreme → US500cash session-flat; gate 2.34; NEW_FAMILY) — `PREREG_FTMO_N113_SILVER_GOLD_RATIO.md`
- Filed OPEN **N114** HYG_CREDIT_STRESS → US500cash session-flat — NEW_FAMILY **AI**; gate **2,34**; `VOORSTEL_PRESCREEN_N114.md`
- Filed OPEN **N115** EURUSD Lon-AM → US500 NY macro-beta session-flat — NEW_FAMILY **AJ**; gate **2,34**; `VOORSTEL_PRESCREEN_N115.md`
Both N114/N115 need Strateeg **D-092.1** → PASS→PREREG (do **not** invent PASS/FAIL).

**U2 `d1dd863` → tip `954680a`:**
- **N112** GAS_EQUITY_MACRO **FAIL_T** @ `d1dd863`: cost-gate PASS train N=188 mean +7.83 bp ≥ 2.34; stress PASS; formal FAIL_T day-clust t 1.07 / t_NW 1.04 <2; test N=71 bruto −4.34 → **TRIAL_COUNT 460→461** (only N112 counted).
- **N113** SILVER_GOLD_RATIO **FAIL_COST_GATE** @ `954680a`: train N=305 mean +1.60 < gate 2.34 (**geen trial**; TRIAL blijft **461**).
- Tip `954680a` **IDLE/HOLD** until next PASS→PREREG. Quiet to Sandro.

Dead += **N112_GAS_EQUITY_MACRO** (FAIL_T) + **N113_SILVER_GOLD_RATIO** (FAIL_COST_GATE). Formal OPEN = **N114 / N115**. Freeze **OFF**. Track-3 **PAUSED**.

**Prior (v91):** C-036 + N104–N111 closed; Faraday `107e502`; U2 tip `a70dc8b` IDLE; TRIAL 460; formal OPEN empty.

**Formal FAIL batch:** …→ N87 **457** → N92 FAIL_T **458** → **N100 FAIL_T 459** → **N101 FAIL_T 460** → **N112 FAIL_T 461**. Cost/stress STOP (geen trial): TSMOM_DIV · ENERGY · IDX_SHORT · N78 · N80 · **N93** · **N103** · **N113**. Pre-screen/DIAG FAIL (geen trial): **N94 · N95 · N97 · N98 · N99 · N102 · N105–N108 · N110 · N111**. UNDERPOWERED: **N96 · N104 · N109** (+ N79 · N83 · N90). TRIAL_COUNT **461**.

**Reeds bevestigd:** L60 FX-med **BARRED**; kill-circuit pivot **ON**; ORB-as-robust-edge **closed**; VIX_TERM / UKOIL-OVN / CORN-as-FTMO **BARRED**.

**Dood (niet herstarten / geen klonen):** A4 · B1 · A5 · A2 · S2 XAU-overlap/GER40-open/USDJPY/USOIL · **N1 · N2 · MIDDAY_VWAP · S2b · N3 · N4 · N5 · N6 · GER_US_LEAD · VWAP_PB · IB_FADE · S2c-shape · LUNCH_OPEN · N10 · N12 · N11 · N15 · N16 · N17 · N18 · P1 · GBPJPY_EU_MOM · N35 · N36 · N40 · N41 · N44 · TSMOM_DIV · ENERGY_TSMOM · IDX_SHORT_TSMOM · FX_EUR_SHORT_TSMOM · FX_USDJPY_MED_TSMOM · FX_EURJPY_MED_TSMOM · N72 · N78_VIX_TERM_VOV · N80 · N87_US30_GAP_FADE · **N92_US100_NY_2H_MOM · N93_SECTOR_DISP_ROTATION · N100_EMB_CREDIT_STRESS · N101_CRACK_SPREAD_MACRO · N103_GER40_US30_INDUSTRIAL · N112_GAS_EQUITY_MACRO · N113_SILVER_GOLD_RATIO** · ORB_META (D-104)**. Pre-screen FAIL/DIAG: PLM / NR7→ORB / Failed-OR / GS01-pooled; XAU N7+N8; N9; N10; N12–N14; N15–N17; N19; **N20–N34 · N37 · N38 · N39 · N42 · N43 · N45 · N48–N57 · N58 · N60–N65 · N67 · N69–N71 · N73 · N74 · N75 · N76 · N77 · N81 · N82 · N84 · N85 · N86 · N88 · N89 · N91 · N94 · N95 · N97 · N98 · N99 · N102 · N105 · N106 · N107 · N108 · N110 · N111** + CEO T5–T16 (TOM/pairs/XS/crypto/hour/event). UNDERPOWERED: **N79 · N83 · N90 · N96 · N104 · N109**. BARRED: **N46 · N47 · N59 · N68** + **L60 FX-med** + **VIX_TERM clones** + **UKOIL OVN-gap clones** + **ORB-meta / ORB-index-ext clones** + **EURNZD-LO / UK→FRA40 / AUS Asia→Lon / GBPCHF-LO / JP225 Tokyo→Lon / CHFJPY-LO / DXY Lon→EU-PM / GBPAUD-LO clones** + **GAS_EQUITY / UNG→US500 / SILVER_GOLD / SLV-GLD ratio clones**. SWAP_HOSTILE: **N58**. Family A overnight index-short **closed**. CORN_F **DEMOTE_LANE_B**. *(N114 HYG≠EMB twin; N115 EURUSD→US500 ≠ DXY Lon→EU / N83 opposite — both still OPEN.)*

### Wekelijkse sporen-tabel (D-094.7 / **D-097–D-104** / **C-028…C-036** — Manager houdt bij)

| Spoor | Inhoud | Eigenaar | Cadans-eis | Status 2026-10-02 |
|------|--------|----------|------------|-------------------|
| **1** | Kortere historie / walk-forward; ≥5j default; D-094a; pool N≥150; forward-papier | **Uitvoerder-2** | Gates + land PREREGs | **OPEN** — tip `954680a` **IDLE/HOLD**; TRIAL **461**; last N112 FAIL_T + N113 FAIL_COST_GATE; next = PASS→PREREG |
| **2** | **Lane-B** FTMO markets → PREREG | **Strateeg** + **S2** feed | ≥3 screens/cyclus; **≥2/3 NEW_FAMILY** | **OPEN** — formal OPEN **N114/N115** (AI/AJ); D-092.1 → PASS→PREREG; bar N75–N113 + GAS/SILVER_GOLD + prior clones |
| **3** | Combineren weak+ / ensembles | **CTO** / CEO 3b | Parallel | **PAUSED** tot solo t≥2 (D-097.3) |
| **4** | **Lane-A→B** + D-102 RISK-REACTIVE / D-103 SHOCK / D-100 carry | **Strateeg + S2** | ≥3; **≥2/3 NEW_FAMILY**; kill circuit | **OPEN** — Faraday `791a17c` AI/AJ live; S2 tip `35e38ac` cycle_2240 (GAS+SILVER promoted → died) |
| **5** | FTMO sizing / `recommend_scale` / lat-B `ftmo_ev` | **CTO** | Parallel | **OPEN** — C-036 DELIVERED (0 trials); tip `f3cf632` |
| **6** | Lane-A data; PROXY_MAP; FTMO-M5; COSTS 166; HistData A-001; calendar-archief | Team / Sandro | Doorlopend | **OPEN** — COSTS_FTMO_alle **166** op main (`f0f9597`); A-001 OPEN; N110 DXYcash M5 gap noted |
| **7** | Coördinatie; novelty + kill circuit; D-*/C-* absorb | **Manager** | :05/:35 | **OPEN** — **v92** |

**C-028…C-036 enforce (Manager):**
- Novelty: Faraday filed AI/AJ (N114/N115) after GAS/SILVER died at U2 — **Strateeg run D-092.1 on N114/N115** → PASS→PREREG ✔ pending.
- Kill circuit: streak cost-PASS→FAIL_T **≥5** → pivot **ON** (N100+N101+N112); N103 = cost-PASS→FAIL_STRESS; N113 = FAIL_COST_GATE. Bar L60 / ORB-robust / VIX_TERM / CORN-as-FTMO / UKOIL-OVN / ORB-meta / N87 / N92–N113 / EMB / CRACK / SECTOR_DISP / NZDJPY-LO / XAU-Lon→NY / USOIL→US100 / CADCHF-LO / CADJPY-LO / AUDCAD / USDCHF-LO / GER40→US30 / EURNZD-LO / UK→FRA40 / AUS Asia→Lon / GBPCHF-LO / JP225 Tokyo→Lon / CHFJPY-LO / DXY Lon→EU-PM / GBPAUD-LO / **GAS_EQUITY / UNG→US500 / SILVER_GOLD / SLV-GLD** clones. Keep HYG≠EMB (N114); EURUSD→US500 ≠ DXY Lon→EU / N83 opposite (N115).
- Roles: **S2 = Lane-A**; **Strateeg = Lane-B** D-092.1 on N114/N115 → PASS→PREREG; U2 IDLE until then.

| Prio | Item | Eigenaar | Status |
|------|------|----------|--------|
| **1** | **D-092.1** on **N114/N115** → PASS→PREREG; **geen** N75–N113 / GAS_EQUITY / UNG→US500 / SILVER_GOLD / SLV-GLD / EMB / CRACK / CORN / VIX / L60 / UKOIL-OVN / ORB-meta / SECTOR_DISP / NZDJPY-LO / XAU-Lon→NY / USOIL→US100 / CADCHF-LO / CADJPY-LO / AUDCAD / USDCHF-LO / GER40→US30 / EURNZD-LO / UK→FRA40 / AUS Asia→Lon / GBPCHF-LO / JP225 Tokyo→Lon / CHFJPY-LO / DXY Lon→EU-PM / GBPAUD-LO clones | **Strateeg** / **S2** (U2 pas na PREREG) | **OPEN — prio** |
| — | Faraday PREREG N112/N113 + OPEN N114/N115 NEW_FAMILY AI/AJ | Strateeg | **DELIVERED** `791a17c` |
| — | **N113** SILVER_GOLD_RATIO FAIL_COST_GATE (**geen trial**; TRIAL 461) | U2 | **DELIVERED** `954680a` |
| — | **N112** GAS_EQUITY_MACRO FAIL_T (**TRIAL 461**) | U2 | **DELIVERED** `d1dd863` |
| — | S2 GAS+SILVER promote (cycle_2240) | S2 | **DELIVERED** `35e38ac` |
| — | **C-036** N104 UNDERPOWERED / N105–N108 FAIL / N109 UNDERPOWERED / N110–N111 DIAG_FAIL (0 trials) | CTO | **DELIVERED** `f3cf632` |
| — | Faraday N106–N109 D-092.1 + OPEN N110/N111 NEW_FAMILY AG/AH | Strateeg | **DELIVERED** `107e502` |
| — | Faraday N104 UNDERPOWERED / N105 FAIL + OPEN N106/N107 | Strateeg | **DELIVERED** `7d2d48a` |
| — | U2 IDLE absorb v90 (hold N110/N111) | U2 | **DELIVERED** `a70dc8b` |
| — | **N103** GER40_US30_INDUSTRIAL FAIL_STRESS (**geen trial**; TRIAL 460) | U2 | **DELIVERED** `b9af560` |
| — | Faraday N103 PREREG + OPEN N104/N105 NEW_FAMILY AA/AB | Strateeg | **DELIVERED** `7059c63` |
| — | **C-035** N102 DIAG_FAIL / N103 DIAG_PASS → PREREG (0 trials) | CTO | **DELIVERED** `f7af392` |
| — | Faraday PREREG N100/N101 + OPEN N102/N103 NEW_FAMILY Y/Z | Strateeg | **DELIVERED** `edbd2ee` |
| — | **N101** CRACK_SPREAD_MACRO FAIL_T (**TRIAL 460**) | U2 | **DELIVERED** `d09d00a` |
| — | **N100** EMB_CREDIT_STRESS FAIL_T (**TRIAL 459**) | U2 | **DELIVERED** `2ffb9af` |
| — | S2 EMB+CRACK promote (cycle_2140) | S2 | **DELIVERED** `67a9be1` |
| — | **C-034** N98/N99 Lane-B DIAG_FAIL (0 trials) | CTO | **DELIVERED** `3ebdea2` |
| — | Faraday N96 UNDERPOWERED + N97 FAIL + OPEN N98/N99 NEW_FAMILY W/X | Strateeg | **DELIVERED** `4a5ec7c` |
| — | **C-033** N96 UNDERPOWERED / N97 DIAG_FAIL (0 trials) | CTO | **DELIVERED** `9536912` |
| — | **C-032** N92/N93 absorb + N94/N95 Lane-B DIAG_FAIL (0 trials) | CTO | **DELIVERED** `f6b0c60` |
| — | Faraday N94/N95 D-092.1 FAIL + OPEN N96/N97 NEW_FAMILY U/V | Strateeg | **DELIVERED** `b2ab614` |
| — | **N93** SECTOR_DISP_ROTATION FAIL_COST_GATE (**geen trial**; TRIAL 458) | U2 | **DELIVERED** `b382307` |
| — | **N92** US100 NY 2h mom FAIL_T (**TRIAL 458**) | U2 | **DELIVERED** `b5b59e0` |
| — | **C-031** N90 UNDERPOWERED / N91 DIAG_FAIL / N92 PREREG (0 trials) | CTO | **DELIVERED** `8a68951` |
| — | **D-101…D-104** absorb (doel/lat-B, RISK-REACTIVE, SHOCK, ORB-meta FAIL) | Manager | **DELIVERED** v83 |
| — | **N87** US30 gap-fade FAIL_T (**TRIAL 457**) | U2 | **DELIVERED** `3a9108e` |
| — | CEO T1–T16 batch all null/FAIL | CEO | **DELIVERED** tip `7cb6731` |
| — | COSTS_FTMO_alle → 166 symb (Spoor 6) | U1 | **DELIVERED** `f0f9597` |
| — | `VRAGEN_SANDRO_CEO.md` / HistData A-001 / integriteit | CEO / Sandro | OPEN (niet-blokkerend); A-001 OPEN |
| — | Dead/FAIL + bars t/m N113 + N112 + N111 + N110 + N109 + N108 + N107 + N106 + N105 + N104 + N103 + N102 + N101 + N100 + ORB-meta + CEO T-batch | — | Gesloten als klonen |

### Acties (bindend; D-094 / **D-097–D-104** / **C-028…C-036**)

1. **Uitvoerder-2 (`claude/uitvoerder2-r`) — IDLE/HOLD:**
   - Tip `954680a`: N112 FAIL_T (TRIAL **461**) + N113 FAIL_COST_GATE. **HOLD** tot next PASS→PREREG. Skip N75–N113 / GAS_EQUITY / UNG→US500 / SILVER_GOLD / SLV-GLD / EMB / CRACK / CORN / VIX / L60 / UKOIL-OVN / ORB-meta / SECTOR_DISP / USDCHF-LO / GER40→US30 / EURNZD-LO / UK→FRA40 / AUS Asia→Lon / GBPCHF-LO / JP225 Tokyo→Lon / CHFJPY-LO / DXY Lon→EU-PM / GBPAUD-LO. No 2025+. Cadans :15/:45. Freeze **OFF**. Track-3 **PAUSED**.

2. **Grok CTO (`grok/cto-1`) — tip C-036 (`f3cf632`); FYI absorb v92:**
   - Support D-101 lat-B/`ftmo_ev`; absorb next ≥2 NEW_FAMILY if PASS→PREREG on N114/N115. Track-3 blijft PAUSED. Geen Sandro eval/spend.

3. **Strateeg (`claude/trusting-faraday-34tsmg`) — Lane-B:**
   - Tip `791a17c`: PREREG N112/N113 delivered (both died at U2); OPEN **N114/N115** NEW_FAMILY AI/AJ. **Run D-092.1 on N114/N115** → PASS→PREREG. Geen L60 / ORB / VIX / CORN / UKOIL-OVN / ORB-meta / N87 / N92–N113 / EMB / CRACK / SECTOR_DISP / USOIL→US100 / CADCHF / CADJPY / AUDCAD / USDCHF-LO / GER40→US30 / EURNZD-LO / UK→FRA40 / AUS Asia→Lon / GBPCHF-LO / JP225 Tokyo→Lon / CHFJPY-LO / DXY Lon→EU-PM / GBPAUD-LO / GAS_EQUITY / SILVER_GOLD clones. Keep HYG≠EMB; EURUSD→US500 ≠ DXY Lon→EU / N83 opposite.

4. **Strateeg-2 (`grok/strateeg-2`) — Lane-A:**
   - Tip `35e38ac` GAS+SILVER (→ N112 FAIL_T / N113 FAIL_COST_GATE). Keep ≥2/3 NEW_FAMILY feed; honest FTMO RT in COSTS vóór promote (Lane-A day_t ≠ PASS).

5. **Auditor — ACTIEF:** steekproef N112 FAIL_T (TRIAL 461) / N113 FAIL_COST_GATE; novelty/kill flags (N100+N101+N112 cost-PASS→FAIL_T; N103 cost-PASS→FAIL_STRESS; N113 cost-gate STOP).

6. **Manager (`main`) — volle cadans :05/:35:**
   - Absorbeer D-*/C-*/U2; enforce novelty + kill; U2-freshness; nooit zelf bevriezen. CEO-Sandro-vragen **niet** door Manager herhaald (CEO-kanaal). Cadans **v92**.

### Model-beleid (D-089)
- Haiku-klasse: Manager, Strateeg (coördinatie/schrijfwerk).
- Sonnet-klasse: Uitvoerder-2, Auditor, CEO (Python/MC/statistisch oordeel).
- Enige maatstaf = voortgang FTMO-edge. Geen stilstand (D-094).
- Platform-minimum trigger = 1 uur; Grok dekt fijnere cadans.

### Teamcadans (D-088 / D-090 / **D-094 volle cadans**)
- CEO (Claude): elke 30 min; beslist + BESLUITEN; lat-B / SHOCK / ensemble-PREREGs (3b)
- Auditor (Claude): elke 30 min / steekproef
- Manager (Grok → `main`): elke 30 min (:05/:35) — **v92**
- Uitvoerder-2 (Grok → `claude/uitvoerder2-r`): elke 30 min (:15/:45) — gates + spoor 1 (**IDLE**)
- Strateeg (Grok → `claude/trusting-faraday-34tsmg`): elke cyclus — sporen 2+4
- Strateeg-2 (Grok → `grok/strateeg-2`): elke cyclus — sporen 2+4
- CTO (Grok → `grok/cto-1`): elke cyclus — sporen 3+5


---

## 0z. Eigen-kapitaal-stukken — GEPARKEERD (D-083)

De volgende onderwerpen zijn **niet langer actief**. Inhoud is bewaard in de repo; zie `archief/eigen_kapitaal/INDEX.md` voor de lijst van geparkte bestanden. Geen nieuwe acties; geen rapportage meer richting Sandro op deze onderwerpen.

**Geparkeerd:** ALLOCATIE_V1/V1.1/V1.2/V1.3, VERWACHTING.md, VEHICLE_ANALYSE.md, S10b, P-ETF-portefeuilles (PREREG_PORT, PORT2, PORT3, PORT4), box-3/NL-retail-kosten, reserve-run (D-084 geschorst), forward-ETF (passief), D-032/D-033/D-035/D-055/D-060/D-061/D-070…D-082 voor zover eigen kapitaal als basis.

---

## 0a. Coördinatie (Manager-QA op wat er ligt)
- **Uitvoerder-2 werkt op branch `claude/uitvoerder2-r`, niet op main** (RUNLOG_R2, results/R2, TRIAL_COUNT 427). Beide Uitvoerders: `git fetch --all`, elkaar lezen; Uitvoerder-2 merged `origin/main` minstens elk uur in zijn branch; Uitvoerder-1 merged `claude/uitvoerder2-r` in main na elke afgeronde run (fast conflict-vrij: eigen bestanden). **TRIALS.csv/TRIAL_COUNT.md:** main zegt 421, U-2-branch 427 → bij merge = aantal geldige rijen; "ongeldig, telt niet"-rijen blijven buiten BH (D-045).
- **Manager-QA-bevindingen catalogusrun 2 (rapportage, geen blokkade):**
  1. **G-benchmark inconsistent toegepast:** C52 *basis* haalt SR 0,65 vs 60/40 0,66 (niet beter) maar staat 'door G-ontdekking'. Volgens D-038 (SR én maxDD beter) is dat een **fail op SR**; label 'door met voorbehoud: DD-voordeel, geen SR-voordeel' of CEO beslist. Rapporteer beslissing expliciet in TRIALS.csv.
  2. **C54 qa is post-hoc gekozen na zien van basis** (beide tellen als trial ✔). Behandel C54 basis niet als bewijs (artefacten: WTI<0, FX-pegs); alleen qa telt, en dan nog met winnaarsvloek-korting.
  3. **Winnaarsvloek P1:** sleeves gekozen na zien van ontdekkingsdata; SR 0,84 is een bovengrens. Rapporteer ook **P-ETF** (zonder futures/hefboom; Strateeg H5: micro-futures onuitvoerbaar bij €80k voor indices/goud) als eerlijke ondergrens en **P-ETF met 13 bp rondreis**.
  4. **Hefboom ≤ 3× tegen rf + 1,5% (D-042)** i.p.v. gratis rf; kosten per vehikel; herrekenen vóór iets over CAGR wordt gezegd.
  5. **Reserve-OOS-power:** 1,75 jr → SR-standaardfout ≈ 0,75; een 'pass' is nauwelijks informatief. Rapporteer puntschatting + CI (D-042), en zeg vooraf dat forward-paper (F) het echte bewijs levert.
  6. **Kapitaal-check doel:** met 2020s-SR ≈ 0,5 ≈ 5% CAGR bij 10% vol = ≈ €330/mnd bruto vóór belasting → onder de €400-drempel; nooit 'ontdekking-CAGR' als verwachting labelen.

## 0b. Direct (Uitvoerder-2, uiterlijk 01-10 12:00, D-042)
1. **Portefeuilleregel vooraf committen** (PREREG_PORT.md): sleeves elk 10% vol, gelijk gewogen, geen optimalisatie, hefboom ≤ 3× tegen rf + 1,5%, kosten per vehikel; commit (SHA in RUNLOG) vóór enige reserve-run.
2. **Run 3 (PREREG vóór resultaat):** C04, C13, C16, C29, C33, C43–C45, C24 + catalogus v1.1-nieuwkomers (trend/vol-managed/dual-momentum).
3. **Regime-stress (D-043):** alles op 1970–2000 (stijgende rente; TNX_10Y vanaf 1962), 2022 en de jaren 70 apart; rolling-SR + DD-duur; wat drijft 2022?
4. **H5 (D-043/Strateeg):** contracten per instrument bij 10% vol, afrondingsfout, marge, geen contract > 25% kapitaal; anders C54 alleen als 'grove legs via ETF/CFD' herformuleren.
5. Winnaarsvloek-log: per sleeve wanneer/waarom in shortlist.

## 0c. Direct (Uitvoerder-1)
1. **D2-uitbreiding (D-044, ≤ 3 u):** (a) TR/dividend (S&P, DAX, NDX) binnen bronvoorwaarden; (b) ≥ 20 instrumenten voor C54 (NZD/SEK/NOK-FX, Bund/JGB/Gilt-proxy's, agri/energie); (c) roll-schone zilver/koper/gas; (d) **FRED vanaf Debian ophalen en committen** (rentes, goud/CPI, FX); rate-limit, eerlijke UA, niets omzeilen.
2. **Engine (D-045):** future-model-fix (FX = spot + renteverschil; doorlopende futures zonder rf-aftrek) blijft; opnemen in engine/README + ENGINE_TEMPLATE (Manager werkt ENGINE_TEMPLATE bij: zie §V).
3. S3/P0 en F (forward) volgens bestaande punten hieronder.

## 0p. ALLOCATIE_V1.3 + run 8 + PORT3/PORT4-uitkomst — Manager-QA
**Stand:** P-ETF-lite (PREREG_PORT4; 18 trades/jr, kosten ≈ €27/jr) faalt 3 van 4 vooraf vastgelegde criteria (ΔSR −0,06; maxDD 15,2% > 14,4%; 2021–24 SR 0,25 vs 0,42) → **niet geselecteerd als vervanging** (Strateeg V1.3, correct toegepast). Drempel 1% (PORT3 'D1'): SR 0,91, 57 trades/jr, kosten ≈ €116/jr (ref. €268), alfa 5,4%/jr — beste kosten/SR-verhouding. Run 8 (EM + USD-rijen, informatief): Faber in USD/EM zelfde beeld als run 5 (DD-bescherming in 6/7 markten, ΔSR +0,13 niet significant); label ongewijzigd.
**Manager-QA:**
1. **Winnaarsvloek bij D1:** D1 is de beste van 3 in-sample varianten; economisch logisch (minder trades), maar **geen selectie tot forward-resultaat + ≥ 3 maanden**; specificatie blijft L0 tot CEO anders besluit; D1 alleen als 'kandidaat-verbetering' labelen. Rapporteer alle varianten.
2. **Simulator-SR-verschil (0,86 vs 0,94):** vergelijkingen alleen binnen één simulator; in EINDVERSLAG/Sandro-getallen nooit simulator-getallen met PREREG_PORT-getallen mengen.
3. **Reserve-run-scope (Uitvoerder-2, vóór 09:00 bevroren lijst):** `r2_reserve.py` gebruikt `all_portfolios(1)+(2)`; P-ETF-lite (port4.py) en PORT3-drempelvariant staan er niet in. Kies één van: (a) toevoegen als **informatieve rijen** (alleen als dat zonder codewijziging aan bestaande rijen kan; nieuw script-SHA vastleggen vóór vrijgave; testen op ontdekking), of (b) expliciet in het reserve-rapport vermelden dat ze niet zijn meegenomen. Geen late aanpassing na 09:00.
4. **Forward-volledigheid:** controleer 22:25 UTC dat alle pre-geregistreerde portefeuilles (a, b, +, breed, PORT3 'D1', PORT4-lite) in `forward/portfolio_daily.csv` staan, met hedged/ongehedged-kolommen.
5. **Run 9-voorstel (Uitvoerder-2; laagste prioriteit, geen trial):** frontier/DD-budget en MC opnieuw **met L1 (drempel 1%) en model B** als gevoeligheid naast L0, zodat het €-getal in de rapportage de realistische kosten weerspiegelt.

## 0o. D-080/D-081, ALLOCATIE_V1.2 (P-ETF-lite), R2-007 — Manager-QA
**Naamconflict PREREG_PORT3 (oplossen vóór 01-10 12:00):** Uitvoerder-1 heeft `PREREG_PORT3.md` (drempelvariant van P-ETF-a, mijn v32 QA-1) al gecommit en bevroren; D-080 noemt **P-ETF-lite** óók PREREG_PORT3. Regel (precedent D-052: vroegste commit geldt): **PORT3 = drempelvariant (blijft)**, **P-ETF-lite = `PREREG_PORT4.md`** (exacte definitie: Strateeg ALLOCATIE_V1_2 §2 — 4 instrumenten, sleeve A kwartaalherweging, Faber alleen SPX, drempel 2%, geen hefboom; eigen SHA in RUNLOG). Uitvoerder-1 committeert PORT4 vóór 01-10 12:00 en neemt beide in `forward_portfolio.py` op vóór de eerste run (22:25 UTC); Uitvoerder-2 backtest-rijen L0–L3 + lite (geen trials). Niets bevroren wijzigen.
**QA:**
1. **Kiesrisico bij 6+ forward-portefeuilles** (P-ETF-a, b, +, breed, PORT3, lite): alle vooraf vastgelegd ✔, maar **rapporteer altijd alle**; geen 'beste achteraf' als advies; beslissing over welke variant (indien ooit) pas na ≥ 3 maanden forward en met BH/prior-correctie voor het aantal varianten.
2. **Lite ≠ verbeterde regel:** Faber op alleen SPX is een andere regel (DD-effect en cross-market-bewijs gelden voor de 5-indexversie/andere markten) → lite apart beoordelen (ΔDD, Δalfa, kosten model B), niet 'erven' van eerdere bewijsstatus.
3. **Kostenmodel:** beide varianten met model B (NL-retail €3,50/trade + 1,5 bp) én model A; toon omloop, trades/jr, €/mnd kosten, netto alfa. Doel: is netto alfa boven cash nu > €0 met margin (bandbreedte), niet 'mooier maken'.
4. **R2-007:** ^PUT/VIX9D/VIX3M binnen (privé, licentienotitie); ^BXM/^WPUT niet via Yahoo; Ken French en Shiller-CAPE **alleen citeren** (geen expliciete licentie) → C66 PutWrite-substitutie op ^PUT; C65/C68 op citaten + prijsproxy (pre-geregistreerd). Uitvoerder-2 draait C65–C68 nu; 30–60% haircut vóór €/mnd; **geen bestanden committen waarvan de licentie niet is vastgesteld**.
5. **Controles morgen:** 09:00 shortlist-commit · 12:00/≥12:25 reserve-run (raw-output, SHA, één keer) · 22:25 UTC forward-bestanden (alle portefeuilles, hedged+ongehedged).

## 0n. ALLOCATIE_V1.1, kosten NL-retail, run 7 — Manager-QA
**Stand:** V1.1 (Strateeg) verwerkt mijn review (5-indexversie blijft specificatie; EUR-backtest; 'niet geselecteerd'; SHA's; H-status). **Kosten NL-retail (Uitvoerder-1, QA v31):** omloop 2,36×/jr ≈ 118 transacties/jr → vaste €3,50/trade eet ≈ €26/mnd extra → **netto alfa boven cash midden ≈ €32/mnd, totaal ≈ €195 (laag €100, hoog €280)**. EUR-backtest (gerealiseerde premies): ongehedged CAGR 8,4% (vol 12,3%, DD 16,6%), gehedged 6,7% (vol 6,3%, DD 11,8%). Run 7: C66 VRP-evidentie (variantieswap-proxy SR 1,66, skew −4,7, 5 maanden = 15% van de winst, maxDD 42% bij 5% notional — proxy optimistisch); **C67 landenrotatie afgewezen** (ΔSR −0,07; TRIAL_COUNT 442); C65/C68/PutWrite wachten op data (R2-007).
**Manager-QA / taken (geen blokkade):**
1. **Omloop is de grootste kostenschroef:** 118 transacties/jr voor 8 ETF's. Leg **vóór 01-10 12:00** een aanvullende vooraf-geregistreerde **gevoeligheidsvariant** vast (`PREREG_PORT3.md`, eigen SHA; `PREREG_PORT`/`PORT2` blijven onaangeroerd): P-ETF-a met **drempelregel** (geen trade bij < 1% gewichtsverschil; evt. kwartaalherweging) — uitsluitend als extra forward-portefeuille/backtest-rij, **geen trial, geen selectie**; rapporteer omloop, kosten (model B) en ΔSR/Δalfa. Uitvoerder-1 (forward) + Uitvoerder-2 (backtest). Zonder pre-registratie vóór de forward-start (22:25 UTC) is de variant later niet meer 'schoon' toe te voegen.
2. **Expectations-rapportage (overal consistent, nu al gedaan in V1.1 en EINDVERSLAG):** netto-alfa €32 (na realistische retail-kosten), totaal ≈ €195; kosten-model B is de basis, A gevoeligheid.
3. **Valutabeleid blijft Sandro's keuze:** ongehedged verdubbelt de vol en hangt aan EUR/USD; gehedged past bij het DD-budget. In forward: hoofdrapport ongehedged (PREREG_PORT §4), gehedged als gevoeligheid — **beide dagelijks loggen** (controle Uitvoerder-1).
4. **C66 (VRP) lezen met zware caveat:** variantieswap-proxy SR 1,66 is niet uitvoerbaar; vertaling naar €/mnd alleen via **echte PutWrite-/optie-P&L** (^PUT/^BXM/^WPUT, privé-repo, licentienotitie) met 30–60% haircut en staarttest. Als licentie/bron niet schoon beschikbaar is: rapporteer C66 als evidentie zonder €-claim en sluit de lijn (geen jacht op bronnen via omwegen). Vergelijk altijd met de kosten (optiespreads, UCITS-covered-call TER).
5. **R2-007 (Uitvoerder-1/Strateeg):** ^PUT/^BXM/^WPUT (Yahoo, privé), Ken French-licentiecheck (citeren/evidentie), CAPE-bron (Shiller/Yale, licentie) — binnen bronvoorwaarden; bij onduidelijke licentie: alleen citeren, geen bestanden committen.
6. **Reserve-run 01-10 12:00 (uitvoering ≥ 12:25 Amsterdam) en forward 22:25 UTC:** Manager controleert na afloop (a) of `r2_reserve.py` gelaten is met onveranderde raw-output en SHA's, (b) of `forward/portfolio_daily.csv` bestaat voor alle portefeuilles incl. hedged/ongehedged-kolommen.
7. **TRIAL_COUNT 442** (U-2-branch): Uitvoerder-1 merged opnieuw in main vóór 09:00; BH-familie 'portefeuilles' apart (PORTFOLIOS.csv).

## 0m. D-077…D-079 + ALLOCATIE_V1 (Strateeg v1) — Manager-review (compliance/QA)
**Bindend:** run 7 (Uitvoerder-2): C65 factor-evidentie (geen trial; FF-licentie vóór gebruik) → C66 VRP-proxy + PutWrite-substitutie (25% aandelenbeta in P-ETF-a; ^PUT/^BXM alleen privé-repo met licentienotitie; WisdomTree-PutWrite-UCITS = route, TER/historie onbevestigd; **haircut 30–60% (McLean-Pontiff) vóór €/mnd**) → C67 landenrotatie (1 trial) → C68 CAPE-multiplier; PREREG vóór resultaat. MC (Uitvoerder-1, v30 QA-1): p(totaal ≥ €400) 0,4–13% (waarderingsprior) vs 6–28% (historische prior) → nooit één getal. **D-078:** `ALLOCATIE_V1.md` = deliverable (Strateeg + Manager); Sandro-samenvatting in EINDVERSLAG (klaar, 19:10). D-079: CEO kan ritme na de reserve-run verlagen; Manager houdt :05/:35 tot CEO anders bepaalt, korte 'geen nieuws'-rondes toegestaan.
**Manager-review ALLOCATIE_V1 (verwerken door Strateeg in v1.1; Uitvoerder-1 voor data):**
1. **Uitvoerbaarheid Faber in de praktijk:** backtest = 5 indices (SPX, NDX, DJI, DAX, N225; gelijk gewogen long/cash); UCITS-trackers voor NDX/DJI/DAX/N225 zijn 'te identificeren'. Specificeer of live de 5-indexversie of een vereenvoudiging (bijv. alleen SPX + DAX/Nikkei via breed ETF) wordt gebruikt — **vereenvoudiging = andere regel** → eerst als gevoeligheidsrun (geen trial) en in de forward meenemen. Signaal op prijsindex, belegging in accumulerend ETF: dividend-effect documenteren.
2. **Valuta (USD-activa, EUR-belegger):** ALLOCATIE_V1 noemt het; voeg een **EUR-backtest van de hele allocatie** toe (ongehedged én hedged = renteverschil), met €/mnd-uitkomst in EUR. Niet alleen een EUR-rij.
3. **Kosten/omloop per jaar:** turnover, transactiekosten (€3–3,75/trade NL-retail, web-claim), TER per bouwsteen, spreads; leg het jaarlijkse kostenbedrag in €/€80k vast en trek het af van alfa-verwachting (nu −0,20%/jr aangenomen) — Uitvoerder-1 uit `forward_portfolio.py`.
4. **Compliance-formulering:** 'niet aanbevolen bij huidig excess' (P-ETF-b) → 'niet geselecteerd'; vermijd 'aanbeveling' voor instrumenten; ISIN/TER expliciet 'web-claim, onbevestigd' (staat er); geen individuele belegging-/belastingadvies; versienummer + SHA van code/PREREG's waarop de specificatie rust (reproduceerbaarheid); wijzigingen alleen via nieuwe versie.
5. **H-status consistent houden met EINDVERSLAG** (H4 niet gehaald; H7 Auditor nog niet gestart); Auditor pas bij kandidaat (CEO-besluit) — Manager houdt dit bij.
6. **Reserve-run 01-10 12:00 / forward 22:25 UTC:** ongewijzigd; controleer na 22:25 UTC of `forward/portfolio_daily.csv` bestaat en noteer gaten.

## 0l. D-073…D-076 + run 6 + MC + catalogus v2 — Manager-QA
**Stand:** CEO (D-073): verwachting ≈ €240/mnd totaal (€140–340), waarvan ≈ €163 EUR-cash, alfa boven cash ≈ €80; kans robuust €400–500 met deze aanpak ≈ 5–10% (was 20–25%), €800–900 ≈ 1%; project gaat door (alleen Sandro beslist). MC (Uitvoerder-1, D-075): p(totaal ≥ €400) ≈ 0,4–5% (parameter), 12–13% incl. 10-jr-toeval; mediaan ≈ €220. Run 6 (Uitvoerder-2, geen trials): plateau C02/C52 (geen pieken); **lange historie 1976–2024: risicopariteit SR 0,51 = 60/40 SR 0,51, maxDD 14% vs 29%, CAGR 7,7% vs 9,4%** → structuur = DD-beheersing, geen SR-alfa. Catalogus v2 (Strateeg): geen premie afzonderlijk > ≈ €10–30/mnd; gestapeld ≈ +€55 → ≈ €295 totaal, < €400.
**Manager-QA (geen blokkade):**
1. **MC-aannamen:** de MC centreert op VERWACHTING-midden (aannames/web-claims, waardering CAPE ≈ 41). Voeg een tweede MC toe met **historische lange-termijn-premies zonder waarderingscorrectie** (aandelen ≈ 4,3–4,7%, obligaties ≈ 1,2%, goud ≈ 0–1%) en toon p(≥ €400) onder beide priors naast elkaar; label 'prior-afhankelijk'. Geen enkel getal als 'de' kans.
2. **Run 6-caveats overnemen in frontier/verwachting:** SPX vóór 1988 zonder dividend (verzwakt 60/40-vergelijking in jaren 70/80), Pink Sheet maandgemiddelden (vol onderschat), synthetische obligatie, maandherweging. Frontier-rapporten: 'RP ≈ 60/40 qua SR (48 jr), halve DD' als hoofdconclusie; 2001–24-SR alleen als 'regime-afhankelijk'.
3. **Catalogus v2 — uitvoering (Uitvoerder-2, één PREREG per premie, vóór resultaat):** C65 factor-evidentie (**geen trial**; licentie FF: citeren, niet herdistribueren), C66 VRP-proxy (VIX vs realized; **geen optie-P&L-claim uit VIX alleen**; ^PUT/^BXM via Yahoo alleen privé, met licentie-notitie en **impliciete kosten/bied-laat-spreads van echte optieverkoop of UCITS-covered-call (TER ≈ 0,35%) meenemen**; staarttest worst-month/DD-duur/crisiscorrelatie; DD-budget bindend), C67 landenrotatie (1 trial), C68 CAPE-multiplier (pre-geregistreerd, decennia; 14 onafhankelijke decennia ⇒ lage power, label). BH over alle trials (nu 441+).
4. **Verwachte waarde:** catalogus v2 schat elke premie op €10–30/mnd; **rapporteer vooraf per premie de minimale effectgrootte die het verschil maakt** (extra €/mnd vs ruis) en stop-regel per premie-lijn ('geen ΔSR/ΔDD-verbetering op P-ETF-a → afgehandeld'); tijd besteden naar verwachte waarde (Manager/CEO-afweging, geen stopvoorstel voor het project).
5. **Reserve-run 01-10 12:00 en forward 22:25 UTC:** ongewijzigd; forward = het echte out-of-sample; H2 (D-076) = allocatie na kosten beter dan **cash + 60/40**.
6. **EINDVERSLAG:** D-073 letterlijk als tussenresultaat (klaar).
7. **Uitvoerder-1:** R2-006 (EM-FX) en D2b afronden; per bron licentie in RUNLOG.

## 0k. D-070…D-072 + QA-2 + VERWACHTING.md — Manager-QA
**Stand:** herlabeling (D-070): C02 = DD-filter, P-ETF-a = risicogestuurde allocatie (geen bewezen alfa); waarde = robuust rendement per DD binnen budget, verwachting op **premies**. Uitvoerder-1 (QA-2): P-ETF-a met C02→B&H: 2001–24 SR 0,94→0,79 (maxDD 11,2→19,2%), **2011–24 SR 0,83 vs 0,85, alfa 5,1 vs 6,1%** → C02 verbetert DD (−8 pp), niet SR/alfa; ondergrens 2021–24 ongehefeld ≈ alfa €112–162 + EUR-cash €163 ≈ **€275–325/mnd**. Strateeg (VERWACHTING v1, web-claims/aannames): premie-gebaseerd **P-ETF-a ≈ €140/€240/€340 totaal (laag/midden/hoog), alfa boven cash midden ≈ €79/mnd**; hefboom loont alleen bij excess/eenheid > 1,5%. → onder €400 in alle scenario's; CEO meldt dit aan Sandro als tussenresultaat (D-072). **Belangrijkste boodschap voor rapportage: cash alleen ≈ €163 (EUR) tot ≈ €270 (USD); toegevoegde waarde boven cash is klein en onzeker; het project levert vooral lager risico per rendement.** Dit is een uitkomst, geen aanleiding voor stop/freeze (alleen Sandro beslist).
**Manager-QA op VERWACHTING (Strateeg; geen blokkade):**
1. **Lineaire premie × exposure mist structuureffecten** (herweging/diversificatierendement, vol-target-timing): benader dat effect met een simulatie op **premie-gecentreerde** data (historische paden herschaald naar de forward-premies, correlaties/vols behouden) i.p.v. alleen som(exposure × premie). Rapporteer beide.
2. **Goud-midden −0,25% en aandelen-midden 2,0% zijn aannames** met brede spreiding; toon **gevoeligheid** (tornado: elke premie ±1σ) en het **Monte-Carlo p(totaal ≥ €400)** (Strateeg §7.3) met **echte gemiddelde exposures** (Uitvoerder-1/2, §7.1–7.2). Goud is een diversifier, niet een premie-bron → zijn rol in DD-reductie apart houden van de rendementsverwachting.
3. **Eerlijke vergelijking op gelijke DD:** wat levert een simpele portefeuille (bijv. 40% wereldaandelen-ETF + 60% geldmarkt, of 60/40 met vol-target) forward-looking bij hetzelfde DD-budget (maxDD ≤ 20%, p95 ≤ 25%)? Pas dan is 'P-ETF-a levert lager risico per rendement' een claim (S10b-H2). Uitvoerder-2, geen trial.
4. **Twee beelden naast elkaar in elk rapport:** (a) backtest-frontier (2001–24 / 2011–24 / 2021–24), (b) premie-gebaseerd; label 'gerealiseerde bull-premie' vs 'forward'. Nooit één getal.
5. **Run 6 (D-071, volgorde bindend):** plateau/gevoeligheid C02+C52 (geen optimalisatie) → lange-historie-toets structuur 1960/70→ (Pink Sheet, TNX) incl. jaren 70 en 2022 → EM (na FX, Uitvoerder-1) → prio-4-resten vervallen tenzij tijd over; daarna **diversifier-screen op D2b** (geen trial).
6. **Reserve-run 01-10 12:00:** ongewijzigd (toetst allocatie op tekenfouten; CI; 'falen'-definitie vooraf). Forward-papier start 01-10 22:25 UTC.
7. **S10b v2 (Strateeg, H1/H2/H4 volgens D-070)** kritisch lezen door Manager in volgende cyclus; H4 = alfa boven cash en totaal; **premie-gebaseerd** primair.

## 0j. Run 5 (cross-market-replicatie) — uitkomst en Manager-QA
**Uitkomst (Uitvoerder-2, PREREG_CAT5 vóór resultaat, 1 trial → 441):** C02 Faber op 12 primaire buitenlandse markten: SR(excess) > 0 in 12/12, ΔmaxDD < 0 in 12/12 (−27,6 pp), gepoold ΔSR +0,10 (90%-BI −0,06…+0,27), maar **nul-kalibratie p = 0,46 en de DD-reductie is op nulpaden even groot** → label **'niet gerepliceerd op SR, alleen DD-beschermend'**: **C02 = risicobeheerder, geen aangetoonde alfa** buiten de VS-ontdekking. Regionale C52: beter dan 60/40 in 9/9 (ΔSR +0,33, ΔDD −15…−27 pp) maar p(nul) = 0,52 → structuur-effect (risicopariteit + goud-bull/obligatie-bull), geen timing-alfa. CEO (D-068): dit is een volwaardig, nuttig resultaat; S10b-H1/H2 aanpassen (DD-filter ≠ alfa). Manager-erratum (DAX/N225 in-sample) is door de Strateeg en de PREREG overgenomen ✔.
**Manager-QA (bindend, geen extra trial):**
1. **Nul-kalibratie like-with-like met exacte uitvoering:** waargenomen ΔSR is +0,10 met exacte maandeinde-uitvoering maar +0,006 met de 21-daagse benadering waarop de nulverdeling rust. Draai de nul-kalibratie ook met **exacte maandeinde-signalen op bootstrap-paden** (bijv. blokbootstrap op maandrendementen + dagreeks-reconstructie, of exacte regel per replica) en rapporteer beide p-waarden; het label 'alleen DD-beschermend' mag pas 'definitief' heten als beide dezelfde kant op wijzen. Tot dan: 'voorlopig'.
2. **Impact op de kandidaat P-ETF-a/frontier (belangrijkste gevolg):** SR 0,94 leunt deels op C02-'alfa' uit de VS-ontdekking. Rapporteer P-ETF-a met **C02 vervangen door aandelen-B&H met dezelfde vol** (en C02 alleen als DD-filter-overlay) → wat blijft van SR/CAGR/maxDD en van €/mnd alfa boven cash? Herrekenen frontier/D-062 op die basis, met 2011–24 en 2021–24. Dit is de eerlijke ondergrens vóór de reserve-run.
3. **Labels overal:** 'C02 = DD-filter (niet-gerepliceerde alfa)', 'C52 = structuur (60/40 verbeteren), regime-afhankelijk (goud-/obligatiebull)'. Geen 'edge' meer in rapportage naar Sandro voor C02; C17 (FOMC) en C55/C44/C16/C33 idem: eerst dezelfde vraag 'alfa of mechanica' voordat ze als bron gelden (nul-kalibratie waar zinvol, geen extra trial voor rapportage).
4. **Reserve-run 01-10:** `r2_reserve.py` draait 10:00 UTC (≥ 10:25 UTC eerste cyclus = 12:25 Amsterdam) — acceptabel; shortlist bevroren 09:00 UTC+2 blijft; **voeg C02-als-DD-filter-analyse toe** (reserve-uitkomst voor C02 lezen als DD-filter: ΔmaxDD, niet SR). 'Falen'-definitie (S11 §5) ongewijzigd.
5. **Run 6 (Uitvoerder-2):** prio-4-resten (C06, C08, C23, C28, C31, C46, C47) met PREREG vóór resultaat; EM-markten pas na FX (R2-006, Uitvoerder-1 zoekt BRL/MXN/IDR/INR binnen bronvoorwaarden).
6. **Uitvoerder-1:** R2-006 (EM-FX) + D2b afronden (RUNLOG per bron met licentie ✔); forward-papier 01-10 22:25 UTC controleren.
7. **Strateeg:** volgende gap-analyse na run 5: wat is de bron van rendement nu? (aandelenbeta + risicopariteitsstructuur + DD-filter) en wat is dan de realistische verwachting; S10b-H1/H2 verduidelijken (DD-filter ≠ alfa; kern-eis = 'DD-budget gehaald bij bewezen beta-/structuurrendement').

## 0i. D-065…D-067 + VOORSTEL_S11 (Strateeg) — Manager-QA (bindend voor PREREG run 5)
**Bindend (CEO):** reserve-run `r2_reserve.py` eenmalig **01-10 12:00 Amsterdam** door Uitvoerder-2 (shortlist bevroren 09:00; C57 informatief; CI + cash/60-40-benchmarks; uitkomst wijzigt geen regels/drempels; technische fout → uitstel met melding). **Run 5:** (1) cross-market-replicatie C02 + regionale C52, (2) prio-4-resten, (3) D2b-data (Uitvoerder-1, ≤ 4 u).
**Manager-oordeel S11:** ontwerp sterk (nul-kalibratie met blokgeschudde paden; markt-geclusterde bootstrap; lokale valuta/rf gelabeld; beslisregel vooraf). **Eén fout in het universum die de PREREG moet corrigeren:**
1. **C02 is ontdekt op SPX, NDX, DJI, DAX, N225 (PREREG_CAT1 §Indices).** DAX en N225 zijn dus **geen onafhankelijke replicatie** (zelfde markten, zelfde periode ≤ 2024). S11 telt ze mee in '≥ 4 van 5'. **Onafhankelijk zijn alleen FTSE, CAC (1990→), HSI (1986→)** (+ STOXX50 informatief, 17 jr). Vereist in de PREREG: DAX/N225 tonen als 'ontdekkingsmarkt — in-sample, telt niet mee'; beslisregel herschrijven voor **n = 3 onafhankelijke markten** (bijv. ≥ 2 van 3 netto SR(excess) > 0 én ΔmaxDD < 0 in ≥ 2 van 3, plus gepoold nul-gekalibreerd p ≤ 0,10); eerlijk vermelden dat 3 zwak-onafhankelijke markten (crises gelijktijdig) een lage power hebben. Zoek extra onafhankelijke markten in D2b (EM/Europa-brede indices, Australië/Canada/Zwitserland/Zweden/Korea indices, Yahoo-lange reeksen) — vooraf lijst vastleggen.
2. **Tijdsoverlap:** ook de onafhankelijke markten liggen in dezelfde kalenderperiode als de ontdekking (ontdekkingsset ≤ 2024) → dit toetst 'andere markt', niet 'andere tijd'. Gebruik daarnaast **oude periodes van de eigen markten voor 1988** (SPX 1927–87 is al gebruikt in ontdekking; N225 1965→ ook) en rapporteer 'pre-1990' apart voor FTSE/N225/DAX.
3. **Selectiebias:** C52 is na zien van data gekozen; regionale C52 telt als 'poging tot replicatie', maar de USD-obligatie-/goudpoot maakt hem geen onafhankelijke test van de aandelentiming → rapporteer aandelenpoot en obligatie-/goudpoot apart.
4. **Uitkomst-labels vooraf:** 'gerepliceerd' / 'niet gerepliceerd op SR, alleen DD-beschermend' (S11) — en **'onvoldoende power'** als het BI van gepoold ΔSR nul en +0,3 omvat. Geen conclusie 'edge bevestigd' op basis van 3 markten.
5. **D2b (Uitvoerder-1):** volgorde S11 §4 (World Bank Pink Sheet CC BY 4.0, lokale rentes/obligatierendementen, dan ETF-proxies met 'korte N'); **niet** bewaren: ICE-BofA-kredietreeksen via FRED (licentie), niet scrapen (MSCI e.d.); Yahoo alleen in privé-repo. Melding in RUNLOG per bron met licentie.
6. **Reserve-run 'falen' vooraf (Strateeg §5):** 'verdacht' = gepoold excess < 0 over het venster én onderkant 90%-BI < −1,0 SR; anders 'niet informatief'. Overnemen in `r2_reserve.py`-rapportage (vóór 09:00 vastleggen).

## 0h. D-060…D-064 + run 4/frontier — Manager-QA (bindend voor uitvoering)
**Stand:** run 4 (C57–C61; TRIAL_COUNT 440): geen nieuwe sleeve slaagt voor poort + benchmark + diversifier-screen (0 van 5). C57 Faber-GTAA haalt G-ontdekking maar niet SR-benchmark → **informatief** in de reserve-run. Decompositie: obligatiebron (synthetisch/IEF/TLT) doet er niet toe; **SR 0,94 = ontdekkingscijfer, 2021–24 = 0,53**. Frontier (DD-budget maxDD ≤ 20%, p95 ≤ 25%, D-062): vol 9% (hefboom ≈ 1,6×) → alfa €244–341 + EUR-cash €163 = **€406–504/mnd** (haircut 50–30%); zonder hefboom €375–412 bij haircut 30%; P-ETF+ niet beter. PREREG_PORT2 (SHA b1a2f3f2…) staat.
**Manager-QA (geen trials):**
1. **Frontier is ontdekkingsdata:** de 9%-vol/1,6×-uitkomst wordt door de 2021–24-SR (≈ 0,5) bijna gehalveerd en het maxDD-budget is dan niet meer gegarandeerd. Voeg toe: frontier ook op **2011–2024** en **2021–24** apart; **p95-DD-methode** (bootstrap? blokgrootte? aantal paden) vastleggen in het rapport; 2022-DD van P-ETF-b (−18,5% bij 1× vol-doel) naast het budget zetten.
2. **Hefboom bij eigen kapitaal:** 'margin-lening tegen rf + 1,5%' is een aanname; beschikbaarheid/kosten/margin-calls (ETF in NL/EU-broker, forced liquidation in 2020/2022-type gap) niet gemeten → in elk €-getal met hefboom expliciet 'onbevestigd (broker)', en de **portefeuille zonder hefboom is de adviesbasis** (D-047); hefboomvariant alleen als 'optie/bovengrens'.
3. **Reserve-run integriteit (01-10 09:00/12:00):** (a) shortlist-bestand committen om 09:00 met SHA (individueel: C52, C02, C17, C54qa, C55, C44, C16, C33; + C57 informatief; portefeuilles: PREREG_PORT (4) + P-ETF+); (b) `r2_reserve.py` SHA vastleggen vóór vrijgave; (c) uitvoeren **één keer**, output onveranderd committen (raw), CI + teken-criterium; (d) niemand kijkt naar 2025→ voordien; (e) P-ETF+ en P-breed-2 tellen mee als extra rijen (geen selectie).
4. **Trial-boekhouding:** TRIAL_COUNT 440 (U-2-branch) vs main: Uitvoerder-1 merged `claude/uitvoerder2-r` → main vóór 09:00 en meldt de gemeenschappelijke stand; PREREG_PORT2/portefeuille-backtests = geen trials maar in BH-familie 'portefeuilles' noteren.
5. **Uitvoerder-1 (D):** D2-uitbreiding af vóór 09:00 of status melden (RUNLOG); forward-papier 01-10 start controleren (bestand `forward/portfolio_daily.csv` bestaat na 22:25 UTC; meld gaten).
6. **Run 5 (Uitvoerder-2):** prio-4-resten (C06, C08, C23, C28, C31, C46, C47) met PREREG vóór resultaat; sleeves die na 09:00 slagen wachten op nieuwe forward-periode (D-064), niet 2025→ hergebruiken.
7. **Strateeg:** C61 uitkomst = negatief (geen inverse-ETF-sleeve); C64 (managed-futures-UCITS) watch-list; volgende gap-analyse: wat levert de doelvariant (€400–500 totaal) op zonder hefboom? Alleen via ≥ 1 echte diversifier, die met huidige data niet gevonden is.

## 0g. D-055…D-059 (bindend) + Manager-QA — tijdlijn reserve-run
**Tijdlijn:** shortlist bevroren **01-10 09:00**, één gezamenlijke reserve-run **01-10 12:00 Amsterdam** (individueel + de vier PREREG_PORT-portefeuilles; PREREG_PORT blijft bevroren; nieuwe sleeves → P2/PREREG_PORT2 ná de run). Forward-papier start 01-10 (cron 22:25 UTC). Rapportage reserve-run met CI (SR-SE ≈ 0,75): pass/fail alleen op teken + niet-significant-afwijkend.
**Standaard in elk rapport (D-055):** drie regels — (1) cash-only nulbenchmark (T-bill/ESTR, USD én EUR), (2) 60/40, (3) strategie; oordeel = **alfa boven cash in €/mnd**, totaal ernaast; haircut 30–50% op excess. M-012 = BESLOTEN (D-055, optie C).
**Stand decompositie (Uitvoerder-1, geen trial):** P-ETF-a SR 0,94 = diversificatie (C52 lang 0,81 + C02 0,47, lage corr.) + obligatiebull; zonder obligatie SR 0,79/DD 16,9%; 2001–10 1,09 · 2011–20 0,97 · **2021–24 0,53**; EUR: alfa €188–264 + EUR-cash ≈ €163 → ≈ €350–427/mnd vóór box 3; cash-only EUR ≈ €163.
**QA-taken (geen trials):**
1. **D-056 afmaken (Uitvoerder-2, `results/R2/decompositie.md`):** obligatieleg vervangen door échte IEF/TLT-reeksen (2002→) naast synthetisch en verschil rapporteren; 1970–2000 en 2022 apart; alles op excess.
2. **Valuta-consistentie (Manager-opmerking):** alfa is berekend op USD-excess (t.o.v. USD-rf) en cash apart in EUR opgeteld → mengt USD-excess en EUR-cash. Rapporteer één consistent EUR-perspectief: EUR-belegger krijgt USD-ETF-excess ± valutaresultaat (ongehedged EURUSD-volatiliteit) of gehedged (kosten = renteverschil). Twee getallen (ongehedged/gehedged) i.p.v. één 'alfa'.
3. **2021–24 SR 0,53** is de meest recente en dus meest representatieve (regime rente hoog); geef bij de verwachting expliciet 'ontdekking vs 2011–24 vs 2021–24' naast elkaar; oordeelsgetal = de conservatiefste redelijke.
4. **D2-uitbreiding (Uitvoerder-1) af vóór 01-10 09:00** (TR/dividend, extra instrumenten C54, FRED-vervangers); anders draait de reserve-run zonder en wordt dat vermeld (D-057).
5. **Run 4 (Uitvoerder-2):** prio-4 + v1.1-resten + Strateeg-v1.2-diversifiers (corr < 0,3 met C02/C52; uitvoerbaar bij €80k vooraf) — PREREG vóór resultaat; C16 (decay) en C44 (kleine N) krijgen labels.
6. **EINDVERSLAG/H4 (Manager, klaar):** Sandro krijgt beide getallen (totaal en boven cash).

## 0f. Stand 15:40 + Manager-QA (bindend voor Uitvoerder-1/2; CEO-besluit over haircut: zie M-012)
Uitvoerder-2 is weer actief (commit 15:32); PREREG_PORT staat (Uitvoerder-1, D-052, SHA `9f17d335…`, bevroren); forward-papier start 2026-10-01 (cron 22:25 UTC). Run 3: 435 trials; door de poort C16, C33, C44, C45, C55.
**QA-taken (geen trials):**
1. **Verdacht hoge SR P-ETF-a (0,94, ongehefeld, 2 sleeves) — decompositie (Strateeg v2.6 punt 1, Manager-akkoord):** rendement en SR per asset (aandelen/obligatie/goud/cash) en per decennium; P-ETF-a **zonder obligatiepoot** (synthetische D=8/C=80 in de rentedaling 2001–2020); P-ETF-a met C02 op price-index i.p.v. adjclose; 2001–2010/2011–2024 apart. Zonder deze uitsplitsing geldt 0,94 niet als uitgangspunt voor verwachtingen (Uitvoerder-1 of -2, wie het eerst pakt; meld welke).
2. **Haircut-definitie (M-012):** haircut op **excess-rendement (x−rf)**, cash-rente apart opgeteld in de eigen valuta (EUR: ESTR/EUR-geldmarkt, niet USD-IRX); rapporteer altijd **cash-only nulbenchmark** naast 60/40 en 'alfa boven cash' in €/mnd. Tot de CEO beslist: beide berekeningen (haircut op totaal én op excess) tonen, met labels.
3. **Run-3-labels (G-benchmark):** C45 haalt de benchmark niet (DD = B&H) en C33 voegt niets toe aan C05 (corr 0,64) → in TRIALS.csv/shortlist expliciet 'geen kandidaat'. C16 Halloween = gepubliceerd seizoenseffect (decay-risico) → alleen als bijsleeve bekijken, niet als eigenstandige. C44: 17 jr/45 wijzigingen = kleine effectieve N.
4. **Frozen PREREG_PORT:** run-3-sleeves (C55 DAA, C44, C16, …) niet in PREREG_PORT wijzigen; alleen als apart, vooraf gecommit **P-breed-v2** (eigen PREREG + SHA) na de reserve-run-voorbereiding. Nooit 'P-breed' achteraf herdefiniëren.
5. **C54:** op 2015–2024 fractionele SR met 15 instrumenten 0,09; retail-CFD niet beter dan 60/40 → C54 blijft 'bovengrens/onbewezen'; niet in de adviesbasis. Sub-selecties 6/8 instrumenten zijn a priori op micro-beschikbaarheid gekozen: als extra trials tellen in BH.
6. **Reserve-run (D-042: uiterlijk 01-10 12:00):** pas na 1–5 gerapporteerd; drie portefeuilles + per sleeve, CI, geen selectie achteraf. Uitvoerder-2 meldt als hij methodisch uitstelt.
7. **Sessie-bewaking (D-051/D-053):** Uitvoerder-2 commit < 90 min ✔; melden bij `disconnected`.

## 0e. D-051 + Strateeg-input PREREG_PORT (v2.5) — Manager-akkoord
- **Uitvoerder-2 was idle** (laatste commit 13:26 Amsterdam); CEO heeft hem gewekt + uurroutine (:25). **Manager-controle elke cyclus:** heeft `claude/uitvoerder2-r` een commit < 90 min? Zo niet → melding in VRAGEN_MANAGER (CEO wekt). Uitvoerder-2: begin elke beurt met `git fetch --all`, lees NEXT_STEPS/BESLUITEN, commit minstens per uur (ook tussenstand), zodat idle zichtbaar is.
- **PREREG_PORT.md eerst (prioriteit 1, blokkeert forward D-050):** neem de Strateeg-punten over: 'P-ETF geen hefboom' ⟂ 'sleeves 10% vol' zijn tegenstrijdig (ongehefeld ≈ 4–7% vol). Leg vooraf vast **P-ETF-a ongehefeld** (adviesbasis/ondergrens; resultaat zoals het valt) en **P-ETF-b gehefeld** tot 10% vol (rente rf + 1,0–1,5% op geleend deel, ≤ 3×); plus rebalance maandelijks, geen trade < 1% gewichtsverschil, één valutabeleid (hedged óf ongehedged), één vehikelset (13 bp, TER 0,07%, SPX_TR). Vooraf vermelden: P-ETF-a ≈ CAGR 4–6,5% ontdekking ⇒ ≈ €270–430/mnd vóór haircut/box 3 → **onder het €400–500-doel**; niet achteraf als 'bijna gehaald' lezen. SHA vastleggen in RUNLOG_R2.
- **Uitvoerder-1:** forward pas starten na commit PREREG_PORT; tot dan `forward/paper_daily.csv` (F3b) blijven loggen en data-snapshots (✔ append-only, ruw, tijdstempel) doorlopen.
- VRAGEN_MANAGER: M-010/M-011 op BESLOTEN gezet.

## 0d. D-047…D-050 (bindend) + Manager-QA
**Uitvoerder-2 (vóór de reserve-run, naast run 3; geen extra trials, alleen vehikelrapporten):** (1) `cfd_retail` (−1,5%/jr op |notional|, beide kanten, + spread; 2× S0 gevoeligheid) voor C54qa, C05, C02, C17, C52; (2) `future_rounded` (hele micro-contracten bij €80k; 16 én 6–8 instrumenten; tracking-error, aantal nul-contracten); (3) **drie portefeuilles overal naast elkaar: P-ETF** (C52 lang + C02 + C17, geen hefboom/shorts; **dit is de adviesbasis**), **P1** (bovengrens) en **P-breed** (alle sleeves gelijk); (4) EUR-perspectief incl. hedged-variant; (5) live-haircut 30–50% expliciet in elk rapport.
**Uitvoerder-1 (F, D-050):** `forward/portfolio_daily.csv` (P-ETF/P1/P-breed), sleeves + regel **exact** zoals in PREREG_PORT.md (levert Uitvoerder-2 binnen 1 cyclus), dagelijks mark-to-market, kosten per vehikel, vergelijking met engine (tracking-band). Papier, geen orders.
**Manager-QA:**
1. **Eén vehikelset vastleggen in PREREG_PORT.md (U-005):** de R2-etf-reeksen zijn gemaakt met oude standaard (3 bp, TER 0,10%, prijsindex); nu 13 bp, TER 0,07%, SPX_TR → **herrekenen met de nieuwe set vóór de portefeuilleregel/SHA**. Nooit twee vehikelsets in één rapport.
2. **rf-definitie forward ≠ engine (DTB3 vs Treasury 3m via Yahoo):** vastleggen welke bron waar geldt, en het verschil (bp) rapporteren zodat tracking-afwijking niet ten onrechte als signaalfout wordt gelezen.
3. **Forward-data zonder lookahead/restatement:** log per dag de gebruikte ruwe slotkoersen + tijdstempel van de download; adjclose achteraf kan herschreven worden (dividend) → forward-signalen op ruwe slot + apart TR-bijschrift; bewaar de dagelijkse bestanden onveranderd (data/daily-cron 22:05 UTC is append-only? bevestig).
4. **Reserve-run-drempel:** alleen vrijgeven als D-047-rapporten er zijn én PREREG_PORT gecommit is; Uitvoerder-2 mag uitstellen met methodische reden (D-049). Meerdere portefeuilles = één gezamenlijke run, drie vooraf genoemde uitkomsten, geen selectie achteraf.
5. **Broker-kosten:** alleen 'web-claim, onbevestigd' (D-048); geen omzeiling van 403.

## R — Catalogus (werkstroom R; volgorde D-032; ontdekking ≤ 2024-12-31, reserve-OOS 2025→ onaangeraakt)
1. **C02-QA (Uitvoerder-2; CFD-benchmark al ✔: SR 0,32 vs 0,18, maxDD 54% vs 88%). Nog te doen per vehikel etf/future (geen reserve-OOS):** (a) vergelijk met **buy-and-hold** (SR, maxDD, DD-duur, CAGR) op dezelfde 5 indices; (b) **total return** (adjclose) i.p.v. price-index en **rente op cash** (IRX) in de vlakke maanden; (c) signaal bij maand-slot, uitvoering volgende handelsdag (geen lookahead), **switch-kosten** per vehikel; (d) effectieve N: 5 indices zijn sterk gecorreleerd → dag-/maandgeclusterde bootstrap over de gepoolde reeks, en 1 index tegelijk (SPX 1927–2024, N225, DAX) als robuustheidscheck; (e) subperiodes (decennia) en 'verloren decennia'; (f) publicatie 2007: rapporteer 2008→2024 apart als quasi-out-of-sample.
2. **Engine `vehicle`-parameter (D-033):** `etf` (TER 0,07–0,12%, geen swap, long-only, deelbaar, adjclose), `future` (micro; roll/financiering in prijs; granulariteit), `cfd` (S0-kosten + financiering benchmark ± 1,5%). Standaardwaarden staan erin; Strateeg levert `engine/vehicles.csv` + retail-broker-kostencheck (D-041) → engine vervangt de standaarden, vermeld in RUNLOG.
3. **Catalogusrun 2 (Uitvoerder-2, één PREREG vóór resultaten; Strateeg levert klassen in catalogus v1.1):** vol-managed aandelenindex, risk-parity/all-weather, dual momentum (Antonacci), Carver-forecast-combinatie over ≥ 20 instrumenten, defensive asset allocation; daarna eerder prio-2/3-regels. Regels die al in de 414+7 trials zitten niet opnieuw testen.
4. Kandidaat-criteria (D-030 §5): netto SR ≥ 0,4 op ontdekking, positief in ≥ 2/3 decennia/regimes, kosten+swap, BH-significant (q = 0,10), lage correlatie met bestaande sleeves; **+ benchmark-vergelijking (D-032)**.

## D — Data
- P0 Dukascopy: voortgang in RUNLOG/`data/DATA_CATALOGUS.md`. D2: 61 reeksen in de repo ✔ (FRED onbereikbaar vanaf cloud-IP, niet omzeilen). Nog: NDX/andere total-return, bond-/credit-/sector-proxy's is gedaan; mis: DGS10/T10Y2Y-vervangers (alleen vrije bron met licentie), uitbreiden (obligatie-/rente-/credit-proxy's, sectoren, meer FX, grondstoffen, total-return-varianten waar vrij beschikbaar) met licentie-vermelding (D-030 §6). S3 blijft laagste prioriteit binnen R maar preempt zodra SPX 2012–2020 compleet is.
## V — Vehikel-analyse (Strateeg eigenaar; Manager QA)
- `VEHICLE_ANALYSE.md` v1 gelezen: goede structuur, bronnen gemarkeerd. **Manager-QA:** (1) 'ᵉ eigen kennis' cijfers (spreads, micro-contractkosten, valutakosten) moeten door brokerdocumentatie geverifieerd of expliciet als aanname in het kostenmodel; (2) box-3-berekening blijft 'niet geverifieerd, geen advies' (wetgeving/ingangsdatum onzeker) — niet in het bruto-doel verwerken; (3) UCITS-historie < 2012: proxy-reeks + TER, niet 'echte ETF-data'. **S10b** (Strateeg, ≤ 2 cycli): DD-budget, min. bewijs (≥ 20 jr, BH, reserve-OOS), vehikelkosten, forward-papier ≥ 3 mnd, Auditor.
## F — Forward/MT5
- Forward-paper (F3b) dagelijks; eerste dag 30-09 22:15 UTC → `forward/paper_daily.csv` moet er 1-10 zijn; meld gaten. Laagste prioriteit binnen het programma (Doel v2 heeft eigen-kapitaal-forward nodig, zie S10b).
