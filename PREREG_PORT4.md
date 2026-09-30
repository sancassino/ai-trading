# PREREG_PORT4 — P-ETF-lite (CEO D-080; Strateeg ALLOCATIE_V1_2 §2; Manager v33) — vastgelegd 2026-09-30 ≈ 18:20Z, vóór forward-start (22:25 UTC) en reserve-run

PREREG_PORT, PREREG_PORT2 en PREREG_PORT3 blijven onveranderd. **Geen trial, geen selectie**; extra backtest-rij en extra forward-portefeuille. Na commit niet wijzigen.
Definitie = ALLOCATIE_V1_2 §2 (Strateeg), hier letterlijk vastgelegd; waar §2 iets openlaat staat de interpretatie **vet** (geen resultaat bekeken).

| Onderdeel | Regel |
|---|---|
| Instrumenten | 4: S&P 500-tracker (rendement = SPX_TR, zoals etf-vehikel; signaal = SPX prijsindex), 10j-obligatie (BOND10_SYN), goud (GOLD_F), cash (rf = engine.rf_on) |
| Sleeve A (C52 'lang') | zelfde regel als C52 lang (gewicht ∝ 1/σ60 over S&P 500 / obligatie / goud; schaal s = min(1; 8%/σ_P)); **herweging per kwartaal**: op de eerste handelsdag van jan/apr/jul/okt worden de C52-gewichten van het laatste maandeinde daarvóór uitgevoerd |
| Sleeve B (C02-lite) | Faber alleen op S&P 500 (SPX-slot > gemiddelde van 10 maandeindsloten → long, anders cash); signaal op maandeinde, **uitgevoerd op de eerste handelsdag van de volgende maand** |
| Combinatie | sleeves ∝ 1/σ60 van de sleeve-dagrendementen (zoals PREREG_PORT; maandelijks op de eerste handelsdag, σ t/m de vorige dag) |
| Drempelregel | op kwartaaldatums gaan **alle** instrumenten volledig naar hun doel; op een Faber-flipdag gaat **het S&P 500-instrument** volledig naar zijn doel; op alle andere dagen met een gewijzigd doel wordt instrument i alleen verhandeld als |doel_i − huidig_i| ≥ **2% van het kapitaal** |
| Hefboom | geen (som exposures ≤ 1; rest cash) |
| Posities | drijven mee met de koersen tussen transacties (instrumentniveau-simulator zoals PREREG_PORT3) |
| Kosten | **model B** (NL-retail €3,50/transactie + 1,5 bp halve spread; web-claim) primair; model A (6,5 bp/eenheid) gevoeligheid; TER S&P 0,07%, obligatie 0,10%, goud 0,12% (web-claims) |

**Forward:** `forward/portfolio4_daily.csv` (datum; P-ETF-lite USD, EUR ongehedged, EUR gehedged, transacties) vanaf 2026-10-01, append-only, cron 22:25 UTC (`port4.py --forward`).
**Rapport (ontdekking ≤ 2024):** omloop/jr, transacties/jr, kosten €/jr (A en B), SR, CAGR, maxDD, alfa boven USD-cash; 2001–24, 2011–24, 2021–24. De vergelijking L0–L6 en de
beslisregel van ALLOCATIE_V1_2 §4 zijn voor Uitvoerder-2 (backtest-rijen, geen trials).
