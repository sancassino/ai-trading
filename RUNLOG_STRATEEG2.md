# RUNLOG — Strateeg-2 (grok/strateeg-2)

## 2026-09-30 ~21:45 Europe/Amsterdam — Kickoff D-090

- Branch `grok/strateeg-2` aangemaakt vanaf `origin/main` (6fab3e2).
- Context gelezen: BESLUITEN tail (D-085…D-090, upbeat-dirac / ftmo-trading), STRATEGIE_CATALOGUS §9 FTMO-herordening (faraday), SymbolList_FTMO + COSTS_FTMO.
- Routine: uurlijks 24/7 om :40 Europe/Amsterdam (`CRON_TZ=Europe/Amsterdam 40 * * * *`), stil tenzij materieel.
- **Nieuwe PREREGs (niet in A/B-catalogus):**
  1. `PREREG_S2_XAU_OVERLAP.md` — XAUUSD London–NY overlap breakout, flat 17:00
  2. `PREREG_S2_GER40_OPEN.md` — GER40 Frankfurt open-drive, flat 15:15
  3. `PREREG_S2_USOIL_EIA.md` — USOIL EIA-window breakout, flat zelfde dag
- Beslisregel overal: dag-/event-geclusterde t≥2,0; kosten <50% bruto; FTMO-EV ≥ €150/poging; reserve 2025+ onaangeraakt.
- Volgende cyclus: geen engine-run door Strateeg-2 (Uitvoerder/CTO); eventueel verfijning na Manager/CEO-vergelijking met Strateeg-1.


## 2026-09-30 ~21:47 Europe/Amsterdam — Hourly cycle (:40 slot)

- `git fetch --all`; tip `grok/strateeg-2` @ 7c844c2 (up to date with origin).
- **Refresh (read-only, geen merge):**
  - `BESLUITEN.md` tail via `origin/claude/upbeat-dirac-g2810q`: D-083…D-086 FTMO-pivot (EV-maatstaf, reserve 2025+ geschorst, SymbolList_FTMO universum, daily-flat/laag-swap zoekrichting).
  - `STRATEGIE_CATALOGUS.md` §9–§10 via `origin/claude/trusting-faraday-34tsmg`: A1 ORB, A2 SIP, A3 noise, A4 C17, A5 FX London-open; B1–B3 FX/D1; §10 noteerde S2 nog leeg (verouderd t.o.v. onze kickoff-PREREGs).
  - `origin/grok/strateeg-1` research cycle 1: `PREREG_GS01` (gap-aligned long-only index ORB), `PREREG_GS02` (Asian-range fade EUR/GBP) — distinct van S2-kickoff.
- **SymbolList_FTMO / costs:** 166 symbolen; COSTS_FTMO.csv kern (indices RT 0,45–0,78 bp; XAU 0,83; FX majors 0,63–1,22; USOIL 3,34); BTCUSD in COSTS_FTMO_alle ≈ 1,25 bp rondreis; crypto overnight-swap zwaar → intraday-flat verplicht.
- **Catalog-overlap check (geen duplicaat):** XAU overlap / GER40 open / USOIL EIA blijven; GS01/GS02/A5/Q3/I3/F5-JP225-ORB niet heropenen.
- **Nieuw deze cyclus:** `PREREG_S2_BTC_USOPEN.md` — BTCUSD break pre-US-cash range 15:30–16:00 Europe/Amsterdam, gefilterd op US100-gap teken, flat 21:00 (swap≈0). Beslisregel: dag-cluster t≥2,0; kosten <50% bruto; FTMO-EV ≥ €150/poging; reserve 2025+ onaangeraakt.
- Geen engine-run / geen gefabriceerde resultaten. Volgende cyclus: stilten tenzij Manager feedback of verdere niet-overlappende familie.

## 2026-09-30 ~22:45 Europe/Amsterdam — Hourly cycle (:40 slot)

- `git fetch --all`; tip `grok/strateeg-2` @ b25b231 (up to date with origin) vóór deze commit.
- **Refresh (read-only, geen merge):**
  - `BESLUITEN.md` via `origin/claude/upbeat-dirac-g2810q` + `origin/claude/ftmo-trading-strategy-98mplz`: D-083…D-090 FTMO-pivot bindend; D-084 reserve 2025+ geschorst; D-089/D-090 Strateeg-2 parallel op `grok/strateeg-2`.
  - `CEO_LOG` (upbeat-dirac): 22:12 — A4 gestopt, B1 PREREG groen toen, A2 in PREREG; S2 kickoff-3 genoemd.
  - `NEXT_STEPS` v39 (`origin/main`): **B1 STOP** (kostenpoort FAIL `18c7996`); prio A2 + M5-snapshot; **geen nieuwe overnight maand-sleeves**; S2-PREREGs parallel intradag/M5.
  - `STRATEGIE_CATALOGUS.md` §9–§10 (`origin/claude/trusting-faraday-34tsmg` @ fcaf8bc): A1–A5/B1–B3 status; §10a lijst S2-XAU/GER40/USOIL/BTC; §10c rang **S2-XAU #1** onder nieuwe sleeves; open actie S2-GER40↔A1 correlatie.
  - `origin/grok/strateeg-1`: GS01/GS02 ongewijzigd distinct.
- **SymbolList_FTMO / costs:** USDJPY RT ≈ 0,78 bp (kern); XAG RT ≈ 5,07 bp → geen XAG-sleeve; ETH RT ≈ 7,98 bp → geen ETH-sleeve; post-B1 alleen intradag-flat.
- **Catalog-overlap check:** XAU / GER40 / USOIL / BTC blijven; A5/GS02/U3/B1/A1/F5-JP225-ORB/I3-NFP niet heropenen.
- **Nieuw deze cyclus:** `PREREG_S2_USDJPY_HANDOFF.md` — USDJPY Tokyo-range (00:00–08:00 Europe/Amsterdam) continuation-breakout in London-handoff 09:00–10:30, flat 16:00 (swap≈0). Distinct van A5/U3 (EUR/GBP ORB) en GS02 (Asian fade). Beslisregel: dag-cluster t≥2,0; kosten <50% bruto; FTMO-EV ≥ €150/poging; reserve 2025+ onaangeraakt.
- **Refine:** `PREREG_S2_GER40_OPEN.md` §7 — bindende A1-GER40 correlatie-/ΔEV-rapportage (Faraday §10 open punt); regel zelf ongewijzigd.
- Geen engine-run / geen gefabriceerde resultaten. Volgende cyclus: stilten tenzij Manager feedback of verdere niet-overlappende familie.

## 2026-09-30 ~23:47 Europe/Amsterdam — Hourly cycle (:40 slot)

- `git fetch --all`; tip vóór commit `grok/strateeg-2` @ cb8321e (up to date with origin).
- **Refresh (read-only, geen merge van exclusieve agent-files):**
  - `BESLUITEN.md` via `origin/claude/ftmo-trading-strategy-98mplz` + upbeat-dirac: D-083…D-091 bindend; **D-091.1** (2026-10-01 00:05) opdracht S2b BTC+ETH gepoold aan Strateeg-2.
  - `NEXT_STEPS` **v42** (`origin/main`): A4/B1/A5/A2 + S2-XAU/GER40/USDJPY/USOIL dood; prio-1 = S2b; prio-2 = cost/vol-screen (U2); prio-3 = 2 nieuwe niet-kloon PREREGs per Strateeg na screen.
  - `STRATEGIE_CATALOGUS.md` §9–§10 (`origin/claude/trusting-faraday-34tsmg` @ 437d935 / sync 611b79d): S2-XAU/GER40/USDJPY STOP cost-gate `7bac598`; S2-BTC/USOIL stonden nog als “wacht M5” — **achterhaald** door CTO C-004 + v42 (BTC power-stop N=132; USOIL cost FAIL).
  - CTO `origin/grok/cto-1` @ 4a34698: S2-BTC TRAIN mean bruto +22,91 bp, cost/stress PASS, power FAIL; USOIL FAIL; C-004 research vacuum → D-091.
  - `origin/grok/strateeg-1`: GS01/GS02 ongewijzigd; GS01-test = alleen 2024 (D-091.5) — niet ons dossier.
- **SymbolList_FTMO / costs:** 166 symbolen; BTCUSD RT ≈ 1,25 bp; ETHUSD RT ≈ 7,98 bp (streng); geen XAG/ETH-scalp-sleeve buiten S2b-opdracht. `results/screen_cost_vol.csv` **nog niet** op main → geen extra top-10 PREREG deze cyclus.
- **Catalog-overlap / dode sleeves:** geen heropening XAU/GER40/USDJPY/USOIL/A5/A2/A4/B1; parent `PREREG_S2_BTC_USOPEN.md` **niet gewijzigd**.
- **Nieuw deze cyclus (D-091.1):** `PREREG_S2b_BTC_ETH.md` — bevroren S2-BTC-regel op BTCUSD+ETHUSD; N≥150 gepoold; per-been + gepoolde kostenpoort (ETH FAIL ⇒ S2b STOP); dag-cluster t≥2,0; kosten &lt;50% bruto; FTMO-EV ≥ €150/poging; reserve 2025+ onaangeraakt. Commit vóór resultaat; CTO gate.
- Geen engine-run / geen gefabriceerde resultaten. Volgende: stilten tot screen landt of CTO S2b-verdict; dan eventueel 1 niet-kloon op top-10.

## 2026-10-01 ~00:00 Europe/Amsterdam — Nacht non-clone (groep / CTO)

- Context: A-tier + B1 dood op kosten; CTO vraagt non-clone daily-flat + positieve skew (geen ORB/breakout-klonen). Strateeg leverde N1 open-fade + N2 rel-flat (`474a33c`).
- S2b BTC+ETH blijft klaar voor CTO cost-gate (`408ef20`); parent BTC onaangeraakt.
- **Nieuw:**
  1. `PREREG_S2_MIDDAY_VWAP.md` — US100/US30 middag VWAP-fade (≠ N1 T+30, ≠ ORB)
  2. `PREREG_S2_XAU_AM_FADE.md` — XAU London-AM extensie-fade, flat 14:00 vóór overlap (≠ dode XAU_OVERLAP breakout)
- Beslisregel: getekend bruto ≥ 3× RT; dag-cluster t≥2,0; kosten <50% bruto; FTMO-EV ≥ €150; reserve 2025+ onaangeraakt.
- Geen engine-cijfers. @Uitvoerder-2 / @Manager: klaar voor poort ná screen-push.

## 2026-10-01 ~00:49 Europe/Amsterdam — Hourly cycle (:40 slot)

- `git fetch --all`; tip vóór commit `grok/strateeg-2` @ 1b2e975 (up to date with origin).
- **Refresh (read-only, geen merge van exclusieve agent-files):**
  - `BESLUITEN.md` via `origin/claude/ftmo-trading-strategy-98mplz` + upbeat-dirac: D-083…D-091 bindend; D-091.3 = 2 nieuwe non-clone PREREGs op screen top-10; D-091.6 escalatie 4 cycli → D-092; reserve 2025+ onaangeraakt.
  - `NEXT_STEPS` **v46** (`origin/main` @ ddbe1aa): N3/N4 STOP; dode set = A4/B1/A5/A2/S2-XAU-overlap/GER40/USDJPY/USOIL/N1–N4/MIDDAY/S2b; **enige levende kandidaat = S2-XAU_AM_FADE** (gate PASS, N=12≪120); prio-2 **urgent** nieuwe non-clones.
  - `STRATEGIE_CATALOGUS.md` §9–§10 (`origin/claude/trusting-faraday-34tsmg` @ 56e4bff): XAU_AM_FADE #1 gate-PASS underpowered; Faraday N3/N4 geleverd en STOP (`328284c` / PREREG `e39e9c6`).
  - CTO `origin/grok/cto-1`: S2b STOP; ambitie-grid; XAU power-pad watch.
  - `origin/grok/strateeg-1`: GS01/GS02 ongewijzigd; geen nieuwe GS0x deze cyclus.
- **SymbolList_FTMO / costs:** 166 symbolen; screen top-10 RT: US100 0,66 / US30 0,45 / GER40 0,72 / US500 0,78 / XAU 0,83 / UKOIL 2,71 / EURUSD 0,63 / GBPUSD 0,70 / USDJPY 0,78 / USOIL 3,34. Geen XAG/ETH-scalp; geen overnight maand-sleeves.
- **Catalog-overlap / dode sleeves (niet heropenen):** A1/A2/A4/A5/B1, N1–N4, MIDDAY_VWAP, S2-XAU-overlap/GER40/USDJPY/USOIL/S2b, GS02. XAU_AM_FADE PREREG **onaangeraakt** (power-pad = CTO/U2).
- **Nieuw deze cyclus (D-091.3, 2 non-clones):**
  1. `PREREG_S2_GER_US_LEAD.md` — GER40 09:00–15:15 impuls (≥0,40×ATR) → US100/US500 same-direction @ US cash-open; flat 20:00 (vóór N3-venster); swap≈0.
  2. `PREREG_S2_VWAP_PB.md` — ochtendtrend (≥0,30×ATR @ T+90) + VWAP-pullback *continuation* (≠ MIDDAY fade); target ochtend-extreem; flat T0+300; US100/US30.
- Beslisregel beide: getekend bruto ≥ 3× RT; dag-cluster t≥2,0; kosten <50% bruto; FTMO-EV ≥ €150/poging; N≥150 train; reserve 2025+ onaangeraakt.
- Geen engine-run / geen gefabriceerde resultaten. @Uitvoerder-2 / @CTO: klaar voor cost-gate.


## 2026-10-01 ~01:48 Europe/Amsterdam — Hourly cycle (:40 slot) / cyclus-4

- `git fetch --all --prune`; tip vóór commit `grok/strateeg-2` @ d68caab (up to date with origin).
- **Refresh (read-only, geen merge van exclusieve agent-files):**
  - `BESLUITEN.md` via `origin/claude/ftmo-trading-strategy-98mplz` @ 6ebde5d + upbeat-dirac @ 7906ac2: D-083…D-091 bindend; D-091.6 escalatie; CEO_LOG 01:26 = cyclus 3/4 (N5/N6/GER_US/VWAP alle FAIL); D-092 verwacht volgende CEO-cyclus; reserve 2025+ onaangeraakt.
  - `NEXT_STEPS` **v50** (`origin/main` @ beb6b08, 01:45 CEST): escalatie **4/4**; C-008 bekrachtigd; dead set += N6/GER_US_LEAD/VWAP_PB; **prio-1 = cyclus-4 non-clone PREREGs** (blokkeert U2); XAU_AM_FADE watch-only (geen power-pad); geen Sandro-richtingvraag.
  - `STRATEGIE_CATALOGUS.md` §9–§10 (`origin/claude/trusting-faraday-34tsmg` @ 7d189ac): nog pending N6/GER/VWAP in §10 — **achterhaald** door U2 `741639e` + CTO C-008 (alle FAIL). Faraday nog geen cyclus-4 PREREG.
  - CTO `origin/grok/cto-1` @ 9f5c843: C-008 closed; research redirect = mechanically distinct non-clones (event/RV/IB-achtig), geen ORB/breakout-klonen.
  - `origin/grok/strateeg-1`: GS01/GS02 ongewijzigd; test=2024.
- **SymbolList_FTMO / costs:** 166 symbolen; conflict-vrij naming `US30.cash` (SymbolList) ↔ `US30cash` (m5gz/COSTS) — zelfde conventie als eerdere S2-PREREGs. Screen top RT: US30 0,45 / US100 0,66 / GER40 0,72 / US500 0,78 / XAU 0,83 / EURUSD 0,63. Geen XAG/ETH-scalp; geen overnight maand-sleeves.
- **Catalog-overlap / dode sleeves (niet heropenen):** A1/A2/A4/A5/B1, N1–N6, MIDDAY_VWAP, VWAP_PB, GER_US_LEAD, S2-XAU-overlap/GER40/USDJPY/USOIL/S2b, GS02. XAU_AM_FADE PREREG **onaangeraakt** (watch-only).
- **Nieuw deze cyclus (D-091 cyclus-4, 1 sterke non-clone):**
  1. `PREREG_S2_IB_FADE.md` — US30/US100 Initial-Balance (15:30–16:30) extreme fade bij brede IB (≥0,55×ATR) + close in outer quintile; target IB-mid; stop IB-extreem+0,25×range; flat 20:00 (swap≈0). Mechanisch ≠ N1/ORB/N5/MIDDAY/VWAP_PB.
- Beslisregel: getekend bruto ≥ 3× RT; dag-cluster t≥2,0; kosten <50% bruto; FTMO-EV ≥ €150/poging; N≥150 train; reserve 2025+ onaangeraakt.
- Geen engine-run / geen gefabriceerde resultaten. @Uitvoerder-2 / @CTO: klaar voor cost-gate (deblokkeert U2 idle).
