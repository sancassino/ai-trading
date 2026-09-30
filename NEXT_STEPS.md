# NEXT_STEPS / BACKLOG v7 — supervisor, 2026-09-30 04:16 Amsterdam

Regel blijft: pre-registratie vóór resultaat, push na elke taak, nooit wachten. Je rondt mijn backlogs in ~20 min af terwijl ik elk uur ververs → **deze backlog bevat bewust zwaar, tijdrovend werk (data-engineering, uren)**.

## Beoordeling (kritisch)
- Sterk: K1 (RSI(2) = overnight-premie, nachten 1–2 dragen; Yahoo t 3,0–3,6, FTMO t 1,5–1,8 → te weinig power), K2 (forward = foutdetector; stopregels vooraf), I4 SCENARIO_RAPPORT, J2 afgewezen, pre-FOMC eerlijk als 'event-t 2,35, afnemend'.
- **Kernprobleem is nu statistische power, niet meer ideeën:** alle intraday-/event-resultaten (ORB, pre-FOMC, K1) rusten op FTMO-data 2021–26 (5,7 jaar; ORB train-t 2,9 / test-t 1,1). Nog meer hypothesen op dezelfde 5,7 jaar = meer ruis (394 trials, DSR ≈ 0,3). Forward-test duurt 9–18 jaar voor bewijs (K2). **Dus: onafhankelijke, langere intraday-data zoeken en bestaande regels daarop bevestigen — GEEN nieuwe trials.**
- Dus geen J2-achtige batches meer tot L1–L3 klaar zijn. Vooraf vastgelegde regels ongewijzigd toepassen telt niet als nieuwe trial.

## BACKLOG (prioriteit 1 = eerst)

**L1 — Lange intraday-historie (bron onafhankelijk van FTMO).** Haal M1 (of M5) 2010–2026 voor US500, US100, US30, GER40, XAUUSD, EURUSD van **Dukascopy** (gratis; bv. `dukascopy-node`/`duka`, index-CFD-symbolen USA500IDX, USATECHIDX, USA30IDX, DEUIDX) — of, als dat niet werkt vanaf de VM, een andere gratis lange bron (Stooq/Alpha Vantage/Kibot-sample; noteer de bron, kwaliteitscontrole: gaten, sessietijden, tijdzone, DST). Sla op in `data/long_m5/` (git-ignore, 135 MB-regel) en documenteer download-script + checksum in `data/README`. Kwaliteitsrapport per symbool (bars/dag, gaten, spread-proxy). Als gratis data niet bruikbaar is: zeg dat en stop L2–L4 op dat pad.

**L2 — Bevestig ORB (B4a-regels ONGEWIJZIGD) op 2010–2020 (buiten FTMO-steekproef).** Zelfde regel: 30-min opening range, stop-orders, exit sessie-einde, 1/7 notional, kosten: realistische spread per symbool per periode (Dukascopy-spreadproxy of vaste bp: US-indices 0,8/1,0 bp, GER40 1,5, XAU 2,0 bp per kant + 1 bp slippage-aanname). Beslisregel (vooraf): op de 3 robuuste symbolen (US500, US100, GER40) én gepoold t ≥ 3 over 2010–2020, teken positief in ≥ 8/11 jaar, bp/trade ≥ 50% van FTMO (0,9 bp). Faalt dit → ORB-poot definitief afgewezen (het was al 'PIEK'); PLAFOND opnieuw zonder ORB.

**L3 — Bevestig pre-FOMC en RSI(2)-nachten op lange data.** (a) Pre-FOMC (slot dag−1 → 14:00 ET, regel ongewijzigd) 2010–2020 (~85 events) met Dukascopy en op Yahoo-daily-proxy 1994–2026 (SPY open/close rond FOMC; FOMC-datums federalreserve.gov, alle jaren); (b) K1-nachtontleding is al op Yahoo gedaan → herhaal op Dukascopy-CFD-serie 2010–2026 voor US500/US100/GER40 (nacht 1–2). Beslisregel: event-t ≥ 2,5 over ≥ 120 events, en 2010–2020 effect ≥ 50% van 2021–26. Verwacht: pre-FOMC bestond vooral 1994–2011 (Lucca–Moench), afgenomen daarna.

**L4 — Herbereken de portefeuille op de langste gemeenschappelijke steekproef.** Alleen sleeves die L2/L3 overleven (vooraf lijst: RSI(2)-overnight, ORB, pre-FOMC): gecombineerde SR, DSR (N=394; herbereken), correlaties, FTMO-dagverlies-check op dagreeks, €/mnd op €80k met realistische kosten (G1). Vergelijk 2010–2020 vs 2021–26 en rapporteer wat het plafond wordt. Update PLAFOND_RAPPORT en SCENARIO_RAPPORT.

**L5 — Forward-test onderhoud + wekelijks verslag.** Elke maandag in `forward/weekrapport.md`: dagen, hypothetische P&L, SR-schatting met CI, kosten (ORB bp/trade), dagverlies/DD-alarm volgens K2-regels. Controleer dat cron gedraaid heeft (gaten in `paper_daily.csv` = melden).

## Reserve (alleen na L1–L4; telt wél als nieuwe trials)
M1 shortlist van max 2 nieuwe hypothesen, pre-geregistreerd, direct op **2010–2026-lange data** getest (dan is t ≥ 3 met veel hogere power haalbaar): bv. overnight-premie na uitverkoop op FX-majors/goud, pre-NFP-drift. M2 ETF-/index-vergelijking van kosten van hefboom (SPY-op-marge vs CFD) voor SCENARIO_RAPPORT.

## Portefeuilleregel
Overleeft ≥ 1 sleeve L2/L3 met t ≥ 3 (resp. 2,5) over lange data → ik schrijf een MT5-/schaalopdracht en een aangepast plafond. Overleeft niets → PLAFOND_RAPPORT definitief ≈ €100–250/mnd (alleen RSI(2)-overnight), Sandro beslist.
