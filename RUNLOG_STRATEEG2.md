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
