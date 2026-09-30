# INDEX — Geparkte eigen-kapitaal-bestanden

**Status:** GEPARKEERD (D-083, 2026-09-30). Doel v3 = FTMO-prop €80k. Deze lijn is ingetrokken; inhoud blijft in de repo voor historische referentie. Geen nieuwe acties op deze bestanden.

## Geparkte bestanden (niet verwijderd, wel inactief)

### Allocatie / verwachting
- `ALLOCATIE_V1.md` — allocatie-specificatie v1 (Strateeg + Manager)
- `ALLOCATIE_V1.1`, `ALLOCATIE_V1.2`, `ALLOCATIE_V1.3` — varianten (op andere branches / Strateeg-sessie)
- `VERWACHTING.md` — premie-gebaseerde verwachting P-ETF (Strateeg)
- `VEHICLE_ANALYSE.md` — vehikelanalyse UCITS/ETF/box 3 (Strateeg)
- `EINDVERSLAG.md` — samenvatting voor Sandro (eigen-kapitaal-deel; FTMO-deel blijft actief)

### S10b / H-poorten (eigen-kapitaal-variant)
- S10b — scoringskaart H1–H8 voor eigen-kapitaal-forward; vervangen door FTMO-EV-variant (S10 FTMO)

### P-ETF portefeuilles
- `PREREG_PORT.md` — P-ETF-a/b/P1/P-breed (PREREG bevroren; backtest-data blijft)
- `PREREG_PORT2.md` — P-ETF+ (bevroren)
- `PREREG_PORT3.md` — P-ETF-a drempelvariant D1 (bevroren)
- `PREREG_PORT4.md` — P-ETF-lite (bevroren)
- `results/port/PORT3_backtest.md`, `results/port/PORT4_backtest.md` — backtest-resultaten

### Forward-papier (passief, loopt door)
- `forward/portfolio_daily.csv`, `forward/portfolio2_daily.csv`, `forward/portfolio3_daily.csv`, `forward/portfolio4_daily.csv` — dagelijkse mark-to-market; cron loopt maar dit is **geen hoofdspoor**
- `forward_portfolio.py`, `forward_portfolio.sh` — code; geen nieuwe aanpassingen nodig

### NL-retail kosten / box 3
- `COSTS_FTMO.csv`, `COSTS_FTMO_per_uur.csv` — FTMO-kosten (blijven actief voor FTMO-EV)
- Box 3-berekeningen en NL-retailtarieven (€3,50/transactie) — niet meer relevant als doelmaat

### Ingetrokken besluiten (eigen-kapitaal-basis)
- D-032 (eigen kapitaal), D-033 (vehikelanalyse), D-035, D-055/D-060 (haircut EUR-cash), D-061, D-070…D-082

## Wat blijft actief (niet geparkeerd)
- `engine/` — FTMO-engine, inclusief `engine/ftmo.py` (Grok CTO)
- Catalogusmethodiek (BH-FDR, nul-kalibratie, PREREG vóór resultaat, TRIALS.csv)
- D2/D2b dagdata
- FTMO-kostenmodel (S0 + swap, vehikel `cfd`)
- Trial-teller / TRIAL_COUNT.md
- Q1b / `ftmo_economics.py` / `mc_daily_ftmo.py`
- Auditor (AUDIT_1.md)
- ORB/B4a, FX-intradag, FOMC-cyclus (A-tier catalogus)
