# RUNLOG_STRATEEG — Strateeg op `claude/trusting-faraday-34tsmg`

## 2026-10-01 12:42 Europe/Amsterdam — C-028 closes L60 FX-med family

**Branch:** `claude/trusting-faraday-34tsmg` (worktree `/workspace/ai-trading-faraday`; ff-pull first, already up to date).
**Trigger:** CTO C-028 binding after both medium-term FX sleeves failed formal tests: USDJPY_MED **FAIL_T**, U2 `910d6ff` (TRIAL 454→455), followed by EURJPY_MED **FAIL_T**, U2 `65a9b23` (TRIAL 455→456).

### Geleverd
- **BARRED/STOP:** N72 EURJPY_MED, N73 USDCAD L60/H10, and N74 USDCHF L60/H10; L60 FX-med family is closed, with no more pair-forks.
- Updated each `VOORSTEL_PRESCREEN_N72/N73/N74.md` status with both U2 SHAs and **TRIAL_COUNT 456**.
- Updated `STRATEGIE_CATALOGUS.md` §9/§10: USDJPY_MED + EURJPY_MED dead; N72–N74 barred; ranking drops MED sleeves; live OPEN = **N75–N77**; **TRIAL_COUNT 456**.
- Updated `STRATEGIE_LOG.md` (~12:42 CEST).

**Niet gedaan:** geen nieuwe VOORSTELs (N75–N77 already OPEN), geen PREREG, geen agent/Sandro message, geen 2025-reserve.


## 2026-10-01 12:40 Europe/Amsterdam — C-028 Lane-B NEW_FAMILY N75–N77

**Branch:** `claude/trusting-faraday-34tsmg` (worktree `/workspace/ai-trading-faraday`; ff-pull tip was `78673d0`).  
**Binding:** CTO **C-028** Lane-B — PREREGs only from Lane-A survivors OR honest-RT intradag w/ D-100; novelty ≥2/3 NEW_FAMILY; freeze further L60 FX-med forks if EURJPY_MED-style FAIL (N72–N74 stay OPEN, no N75+ as L60 FX longs). D-094 FREEZE OFF; D-094a; D-097; D-100.

### Inputs gelezen
- `STRATEGIE_CATALOGUS.md` §9/§10 tip (N72–N74 OPEN; TRIAL **454**; USDJPY_MED live PREREG).
- `COSTS_FTMO.csv` + `results/screen_cost_vol.csv`.
- `results/ceo/swap_side_map.csv` via `git show origin/claude/ftmo-trading-strategy-98mplz:...` (cached locally for reference; not required for U2).

### Geleverd (geen PREREG)
| ID | Family | Symbol(s) | Gate bp | NEW_FAMILY |
|----|--------|-----------|--------:|:----------:|
| N75 | metal ratio MR 3d | XAUUSD+XAGUSD | 30,60 | Y |
| N76 | commodity inv-window | UKOILcash | 50,00 | Y |
| N77 | vol-timed XS rank-rev 5d | FX6 majors | 46,29 | Y |

N72–N74 remain **OPEN** (L60 med); **no** more EURJPY/USDCAD/USDCHF/USDJPY L60 forks. Catalog §9/§10 + STRATEGIE_LOG updated. Train 2021–2023; N≥150; signed mean bruto; D-094a + D-100 notes in VOORSTELlen.

### Niet gedaan
- Geen `PREREG_FTMO_*` (Lane-B: no own PASS).
- Geen L60 FX pair-forks; geen dead-sleeve restart; geen 2025-reserve; Quiet (geen agent/Sandro message).

## 2026-09-30 21:41 Europe/Amsterdam — D-090 re-kickoff cyclus

**Branch:** `claude/trusting-faraday-34tsmg` (tracking `origin/claude/trusting-faraday-34tsmg`).  
**Doel cyclus:** FASE 3 FTMO — PREREG-gaps, B1/A2 stubs, catalogus §9/§10, log.

### BESLUITEN gelezen
- Bron: `git show origin/claude/upbeat-dirac-g2810q:BESLUITEN.md`
- Tail relevant: **D-083** (Doel v3 = FTMO €80k), **D-084** (reserve geschorst), **D-085** (FASE 3 FTMO-EV), **D-086** (teamacties; Strateeg = plan v4 + catalogus herordenen).
- Bestand eindigt bij D-086 (211 regels). **D-087 / D-088 / D-090** staan in `origin/main:GROK_CTO_INSTRUCTIE.md` en `NEXT_STEPS` v35, maar **nog niet** als genummerde entries in BESLUITEN op dirac → Manager/CEO: sync BESLUITEN.

### PREREG-status na cyclus
| Bestand | Status |
|---------|--------|
| `PREREG_FTMO_C17.md` (A4) | Gaps gevuld; OPEN §1a regel V-CAT1 vs V-PRE (default V-CAT1); gemeten kosten; trial/BH |
| `PREREG_FTMO_FX_INTRADAG.md` (A5) | Gaps gevuld; EURUSD-first; U3-afbakening; wacht GBP/JPY M5 |
| `PREREG_FTMO_B1.md` (B1) | **Stub** — OPEN universum / swap-vs-carry / sizing |
| `PREREG_FTMO_A2.md` (A2) | **Stub** — OPEN poortgetal / 1 variant / trial-ja-nee |

### §10 one-liner
Faraday A4/A5 run-klarer dan Strateeg-2 zolang strateeg-2 geen eigen PREREG/hypotheses heeft gecommit.

### Niet gedaan (bewust)
- Geen backtest, geen FTMO-EV-cijfers verzonnen, geen 2025-reserve, geen force-push/amend.

### Git (deze cyclus)
Commit op `claude/trusting-faraday-34tsmg` + push `-u origin`.

## 2026-09-30 22:01 Europe/Amsterdam — CTO-deblokker (Grok): train/test-freeze

**Waarom:** CTO-deblokker voor Grok Strateeg. Conflict D-030 (oudere testvenster-taal doorlopend voorbij 2024) vs D-084 (reserve geschorst) opgelost door test te krimpen.

**Bevroren vensters (PREREG_FTMO_C17 + PREREG_FTMO_FX_INTRADAG):**
- Train: 2021-01-01 … 2023-12-31 (2021–2023)
- Test: 2024-01-01 … 2024-12-31 (volledig 2024; plafond ≤ 2024-12-31)
- Reserve: 2025-01-01 → ONAANGERAAKT / UNTOUCHED (niet openen, niet gebruiken)

**Geen CEO 2025-vrijgave nodig** voor dit amendement. Geen backtest, geen 2025-data, geen trial-resultaten.

## 2026-09-30 22:08 Europe/Amsterdam — B1 PREREG bevroren (post-A4)

**Context:** A4 C17 kostenpoort FAIL (`43b6ba2`). Manager NEXT_STEPS v37: B1 eerst, A2 parallel. Strateeg-2 akkoord B1→A2; S2-M5 ná B1.

**Geleverd:** `PREREG_FTMO_B1.md` van stub → volledige freeze:
- Universe: EURUSD/GBPUSD/USDJPY/AUDUSD/USDCAD/USDCHF (NZDUSD uit)
- Regel: C05 TSMOM-mix 21/63/252 × 0,10/σ60 cap 3, maandeinde
- Kosten: COSTS_FTMO RT + swap bp/nacht-tabel; poort 3×; +50% swap-gevoeligheid
- Venster: train 2021–2023 / test 2024 / reserve 2025 ONAANGERAAKT
- Sizing: p95 dagverlies ≤ 2%; FTMO-EV via engine/ftmo.py
- ≠ B2/C12

**Niet gedaan:** geen backtest, geen A2-upgrade deze commit, geen 2025-touch.

## 2026-09-30 22:15 Europe/Amsterdam — Hourly FTMO (:10): A2 freeze + B1 poort-align + catalog §9/§10

**Branch:** `claude/trusting-faraday-34tsmg` (D-090 Strateeg).  
**Fetch/pull:** tip was `05caced` (B1 freeze); deze cyclus bouwt daarop.

### BESLUITEN (CEO `upbeat-dirac`, tail)
- D-083…D-086 bindend: FTMO-prop €80k, maatstaf FTMO-EV, reserve 2025 geschorst, SymbolList_FTMO.
- Geen nieuwere D-09x-tekst in BESLUITEN.md zelf; Manager NEXT_STEPS v38 op main verwijst D-087…D-090 + post-A4 prio.
- **A4 C17 GESTOPT** (`43b6ba2` U2): kostenpoort TRAIN FAIL — geen herstart zonder CEO.

### Geleverd
1. `PREREG_FTMO_A2.md` stub → **volledige freeze** (OR-richting, stop 10% ATR14, EOD; D-012 gemiddelde-poort; US41 RT uit `COSTS_FTMO_alle.csv` median 6,41 / mean 8,99 bp; train/test/reserve zoals CTO-freeze; FTMO-EV ≥ €80; 1 variant).
2. `PREREG_FTMO_B1.md` poort-amend: **getekend gemiddelde** bruto (NEXT_STEPS v38), niet mediaan |bruto|.
3. `PREREG_FTMO_C17.md` status → FORMEEL GESTOPT (verwijs `43b6ba2`).
4. `PREREG_FTMO_FX_INTRADAG.md` → GEPARKEERD tot M5 (v38).
5. `STRATEGIE_CATALOGUS.md` §9 A2/A4/A5/B1 statuses; §10 herschreven + sterkte-rang (S2-XAU > B1 prio-fit > A2 > …).

### Strateeg-2 vergelijking (§10c)
Sterkste *nieuwe* sleeve op kosten/distinctheid: **S2-XAU_OVERLAP**. Programma-prio blijft **B1 dan A2** (Manager). Faraday leidend voor A/B-tier; Strateeg-2 voor FDR-diversificatie.

### Niet gedaan
- Geen backtest / geen FTMO-EV-cijfers verzonnen / geen 2025-touch / geen A4-herstart.

## 2026-09-30 23:15 Europe/Amsterdam — Hourly FTMO (:10): post-A5/S2 STOP catalog sync

**Fetch:** `origin/claude/trusting-faraday-34tsmg` @ `5a66435` (fast-forward). Tip was Strateeg-log 22:50.

**BESLUITEN (origin/claude/upbeat-dirac-g2810q):** D-083 DOEL v3 FTMO €80k; D-084 reserve 2025+ geschorst; D-085 FASE 3 FTMO-EV; D-086 teamacties. Geen D-087+ in BESLUITEN.md; operationeel leidend = CEO_LOG 23:15 + NEXT_STEPS v41 (`2b2492c`).

**Uitkomsten sinds vorige cyclus (niet door Strateeg gedraaid):**
- A5 FX London-ORB kostenpoort FAIL (`ce5abdc`, median bruto −5,91 bp < 3× 3,93 bp).
- S2 XAU/GER40/USDJPY cost-gate FAIL (`7bac598`).
- B1 al STOP (`18c7996`); A4 al STOP (`43b6ba2`).
- M5gz 24 symbolen op main; **US41 equity M5 ontbreekt** → A2 geblokkeerd.

**Geleverd deze commit:**
1. `PREREG_FTMO_FX_INTRADAG.md` status → FORMEEL GESTOPT (`ce5abdc`).
2. `PREREG_FTMO_B1.md` status → FORMEEL GESTOPT (`18c7996`).
3. `PREREG_FTMO_A2.md` runtime → wacht US41-M5gz (v41 prio-1).
4. `STRATEGIE_CATALOGUS.md` §9 A2/A5/B1 + §10a–d herschreven (sterkte: A2 programma-prio; GS01 research-fit; S2-BTC/USOIL open).
5. `STRATEGIE_LOG.md` cyclusregel.

**Niet gedaan:** geen backtest; geen nieuwe PREREG; geen overnight sleeve; geen 2025-data; geen merge van U2-resultaten (alleen status-sync).

## 2026-09-30 23:55 Europe/Amsterdam — D-091 nacht: 2 niet-kloon PREREGs + GS01-erratum

**Context:** A-tier/B1 dood op kosten; CTO/Sandro: doordraaien, out-of-box, geen ORB-klonen. Screen top (lokaal `results/screen_cost_vol.csv`): US100/US30/GER40/US500/XAU.

**Geleverd:**
1. `PREREG_FTMO_N1_OPEN_FADE.md` — fade na 30-min ATR-drive (US100/US30/US500); ≠ ORB.
2. `PREREG_FTMO_N2_REL_FLAT.md` — US100↔US500 relative morning, EOD flat; ≠ ORB/richting.
3. `PREREG_GS01_ERRATUM.md` — test alleen 2024; reserve 2025 dicht (D-091.5).

**Niet gedaan:** geen backtest; wacht U2-push screen + CTO gate op S2b (Strateeg-2). U2 mag N1/N2 kostenpoort na merge/SHA.

## 2026-10-01 00:10 Europe/Amsterdam — Hourly FTMO (:10): sync post nacht-queue

**Fetch:** `origin/claude/trusting-faraday-34tsmg` @ `474a33c` (up to date). Branch confirmed Faraday (not grok/strateeg-1).

**BESLUITEN:**
- `origin/claude/upbeat-dirac-g2810q` BESLUITEN.md eindigt D-086 (FTMO-pivot).
- D-087…D-091 via `origin/claude/ftmo-trading-strategy-98mplz` + CEO_LOG / NEXT_STEPS v44.
- **D-091** (00:05 CEST): S2b BTC+ETH → cost/vol-screen → 2 non-clone PREREGs/Strateeg → CTO ambition SR×skew; GS01 test=2024; **geen Sandro-richtingvraag** (D-091.6 → D-092 na 4 cycli zonder poort+power).

**Uitkomsten sinds vorige Strateeg-commit (niet door Strateeg gedraaid):**
- A2 SIP-ORB kostenpoort FAIL (`bba5c0c`; mean +3,77 < 26,74 bp).
- N1 STOP n=0; N2 FAIL −0,84 bp; MIDDAY_VWAP FAIL n=3; **XAU_AM_FADE gate PASS** +18,70 bp maar N=12≪120 (`8c7a8e1`).
- S2b ETH leg FAIL → STOP (CTO C-005 / `18a266a`).
- TRIAL_COUNT blijft 444; reserve 2025→ onaangeraakt.

**Geleverd deze commit:**
1. `PREREG_FTMO_A2.md` status → FORMEEL GESTOPT (`bba5c0c`).
2. `PREREG_FTMO_N1_OPEN_FADE.md` / `N2_REL_FLAT.md` status → GESTOPT (`8c7a8e1`).
3. `STRATEGIE_CATALOGUS.md` §9 A2/N1/N2 + §10a–d herschreven (prio: XAU_AM_FADE > GS01 > dood).
4. C17 / FX_INTRADAG / B1 PREREGs gecontroleerd — compleet, ongewijzigd (al STOP).

**Strateeg-2 vergelijking (§10c):** enige open gate-PASS = XAU_AM_FADE (power-blokker); Faraday A/B+N dood; S2b dicht.

**Niet gedaan:** geen backtest; geen N1-retune; geen 2025-touch; geen Sandro-ping (D-091.6 verbiedt richtingvraag; geen materieel nieuw bewijs dat Sandro moet zien).

## 2026-10-01 08:05 Europe/Amsterdam — D-094 FREEZE OFF: tracks 2+4 VOORSTELs

**Branch:** `claude/trusting-faraday-34tsmg`.  
**BESLUITEN:** `origin/claude/ftmo-trading-strategy-98mplz` — **D-094** (freeze off; breed zoeken; Strateeg tracks 2+4) + **D-094a** (min 5y of schriftelijke (a)/(b)/(c)). D-093/D-092.6 stopregel ingetrokken.

**Stand:** TRIAL_COUNT **447** (ongewijzigd). Geen cost pre-screen PASS deze cyclus → **geen PREREG**. Dead set ongewijzigd (ORB/A4/A5/B1/N1–N19/…). Ranking: F2-ORB/A1 > S2-XAU_AM_FADE watch > S2-BTC > GS01.

**Geleverd:**
1. `VOORSTEL_PRESCREEN_N20.md` — status **OPEN** (D-094 lifts D-093.2); US30cash; gate **1,35 bp**; D-094a (b).
2. `VOORSTEL_PRESCREEN_N21.md` — status **OPEN**; GER40cash; gate **2,16 bp**; D-094a (b).
3. `VOORSTEL_PRESCREEN_N22.md` — **NEW track 2** UKOILcash London→NY MR; gate **8,13 bp**; ≠ S2-USOIL EIA; swap 0.
4. `VOORSTEL_PRESCREEN_N23.md` — **NEW track 4** US100cash 2d TSMOM; gate **13,68 bp** (RT+2×swap_long); ≠ B1; D-094a (b).
5. `STRATEGIE_CATALOGUS.md` §9/§10 D-094 sync; `results/screen_cost_vol.csv` gekopieerd indien ontbrak.

**Niet gedaan:** geen PREREG; geen U2/Sandro/agent-ping (parent); geen 2025-reserve; geen ORB-klonen.

## 2026-10-01 08:12 Europe/Amsterdam — D-094: N20–N23 FAIL sync + N24–N27 vervangers

**Branch:** `claude/trusting-faraday-34tsmg`.  
**Trigger:** U2 `a1756a7` op `claude/uitvoerder2-r` — D-092.1 train pre-screen **alle FAIL** vs VOORSTELs @ `f54ad28`. CTO: geen PREREG; geen dunnere UKOIL Lon-AM / 2d-TSMOM klonen.

**U2 uitslagen (train 2021–2023):**
| Code | N | mean bp | gate | uitslag |
|------|---|--------:|-----:|---------|
| N20 US30 AM→PM cont | 384 | −2,26 | 1,35 | FAIL |
| N21 GER40 afternoon fade | 234 | −2,45 | 2,16 | FAIL |
| N22 UKOIL Lon-AM fade | 345 | −1,67 | 8,13 | FAIL |
| N23 US100 2d TSMOM | 377 | +4,46 (long +10,83) | 13,68 | FAIL |

**Stand:** TRIAL_COUNT **447** (ongewijzigd; pre-screen FAIL ≠ formal trial). D-094 nog actief. Geen PREREG.

**Geleverd:**
1. VOORSTEL N20–N23 status → **geen PREREG — U2 D-092.1 FAIL** (cite `a1756a7`).
2. `STRATEGIE_CATALOGUS.md` §9/§10 FAIL-rijen + header D-094 actief + TRIAL 447.
3. **NEW** VOORSTEL_PRESCREEN_N24 (US500 lunch-fade, gate 2,34, track 2) / N25 (XAU NY-PM fade, 2,49, track 2) / N26 (XS 1d reversal basket 5, 4,83, track 4 + D-094a(c)) / N27 (AUDUSD H4 MR, 3,66, track 4).
4. RUNLOG + STRATEGIE_LOG append.

**Niet gedaan:** geen PREREG; geen agent/Sandro-ping (parent); geen 2025-touch; geen herstart N20–N23.

## 2026-10-01 09:30 Europe/Amsterdam — D-094 FAIL_T sync TRIAL453 + N46–N48

**Branch:** `claude/trusting-faraday-34tsmg` (worktree faraday; tip was `6ef46a7`).  
**Trigger:** U2 `a498a69` (N35/N36/GBPJPY FAIL_T → 451) + U2 `5b3db74` (N40 FAIL_STRESS trial 452; N41 FAIL_T NW 1,85 trial 453 → **TRIAL_COUNT 453**).

### Marked STOP FAIL_T
| ID | Uitkomst | Cite |
|----|----------|------|
| N35 | FAIL_T (t≈1,22) | `a498a69` trial 450 |
| N36 | FAIL_STRESS→FAIL_T | `a498a69` trial 451 |
| S2-GBPJPY | FAIL_STRESS→FAIL_T | `a498a69` trial 449 (catalog only) |
| N40 | FAIL_STRESS→FAIL_T | `5b3db74` trial 452 |
| N41 | FAIL_T (NW 1,85; test −4,39) | `5b3db74` trial 453 |

N44 **BARRED** (EU→US clone of dead N35/N41). N45 blijft OPEN (≠ N40/N41).

### New OPEN VOORSTELs (D-094 ≥3 non-clone; tracks 2+4)
| ID | Track | Instrument | Gate | Mechanisme |
|----|-------|------------|-----:|------------|
| N46 | 2 | EURGBP | 3,12 | Lon fix extension **fade** |
| N47 | 2 | USDCHF | 3,03 | Asia→London handoff **cont** |
| N48 | 4 | USDJPY | 7,08 | 1d TSMOM overnight (swap in gate) |

≠ N35/N36/N40/N41/GBPJPY/ORB. D-094a (b); train 2021–23; N≥150; 3×RT.

**Niet gedaan:** geen PREREG; geen U2/Sandro ping (Quiet; CTO: wake U2 only PASS→PREREG); geen 2025-reserve.
