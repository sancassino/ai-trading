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
