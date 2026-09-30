# PREREG FTMO-FX-INTRADAG — London-open range-breakout (A5) — 2026-09-30

**Status:** Pre-registratie FASE 3 (D-085/D-087). Structuur compleet. **Nog geen resultaat.** Wacht op M5 voor GBPUSD/USDJPY (EURUSD M5 aanwezig) én `engine/ftmo.py`-validatie.  
**Tier:** A5.  
**Trial:** +1 (één bevroren variant). NY-open = alleen gevoeligheidsrij, geen aparte trial. Reserve 2025-01→ onaangeraakt.

## 1. Regel (exact, bevroren)
- **Instrumenten (volgorde):** (1) EURUSD alleen eerste run; (2) zodra M5 er is: EURUSD+GBPUSD+USDJPY gelijk gewicht 1/3.
- **Sessie:** London-open. Range = high/low van bars **08:00–08:30 Europe/Amsterdam** (CEST/CET zoals box-klok; documenteer DST in RUNLOG).
- **Long:** eerste M5-close **>** range_high na 08:30; **Short:** eerste M5-close **<** range_low. Geen trade bij doji-range (high−low < 5 pip EURUSD/GBPUSD; < 50 punt USDJPY — zie OPEN §1a).
- **Stop:** vaste afstand 50 pip (EURUSD/GBPUSD) / 50 punt (USDJPY) vanaf entry; **geen** trailing.
- **Exit:** min(stop, hard flat **17:00 Europe/Amsterdam** dezelfde dag). Geen herentry. Geen overnight → swap = 0.
- **Sizing:** 0,5% account-risico per open positie (stop-afstand); max 1 positie per pair; max 3 pairs → ≤ 1,5% gelijktijdig risico.

### 1a. OPEN
1. **Pip/punt USDJPY:** bevestig FTMO-contractspecificatie (digits/point) vóór multi-pair run; tot dan EURUSD-only.
2. **Overlap met U3:** D-015 U3 = London-ORB (30 min OR, stop andere kant van OR, uit 17:00) — **andere familie** (ORB-stop vs vaste 50-pip). U3 gaat door als aparte historie; deze A5 telt als **nieuwe** trial alleen als kostenpoort haalt. Rapporteer overlap-dagen (% gezamenlijke entries) informatief.

## 2. Mechanisme
London-open concentreert FX-orderstroom; range-break = microstructuur/momentum over uren. Claim; bewijs = eigen M5 + FTMO-kosten.

## 3. Dataset / vensters
| Item | Waarde |
|------|--------|
| Ontdekking | 2021-01-01 … 2024-12-31 (FTMO-M5) |
| Informatief recent | 2024 alleen (geen beslissing) |
| Reserve | 2025-01-01→ gesloten (D-084) |
| Data-status | EURUSD M5: aanwezig in repo-paden FTMO; GBPUSD/USDJPY M5: **gat** (Uitvoerder-1 / R2-007-achtige export) |

## 4. Kostenmodel (gemeten S0)
`COSTS_FTMO.csv`:

| Symbool | Rondreis intraday (bp) |
|---------|------------------------|
| EURUSD | 0,63 |
| GBPUSD | 0,70 |
| USDJPY | 0,78 |

Swap n.v.t. (intraday flat). Gevoeligheid +50% spread.  
**Kostenpoort:** gemiddelde bruto ≥ 3× rondreis (EURUSD: ≥ ≈ 1,89 bp/trade) op ontdekking; mediaan informatief (D-012: poort op gemiddelde).

## 5. Beslisregel (vooraf)
1. Kostenpoort → anders STOP zonder trial-telling als "pass".
2. Dag-geclusterde t ≥ 2,0 op ontdekking **én** beide helften 2021–22 / 2023–24 netto > 0 **én** N ≥ 500 trades (EURUSD-only mag N ≥ 300 als alleen 1 pair — label "onderpowered" als N < 500).
3. FTMO-EV via `engine/ftmo.py` (fee-aanname €540/€80k): kandidaat als FTMO_EV_netto ≥ €80/poging **én** p95 dagverlies ≤ 2% bij gekozen sizing.
4. Winrate, avg win/loss, skew, correlatie met ORB (A1) rapporteren; correlatie is geen poort.
5. BH over catalogus-TRIALS.

## 6. Verwachting (prior)
U3/London-ORB-achtige FX had lage prior (R1/R4 negatief; D-015 ≈ 10%). Swap-voordeel is nul t.o.v. andere intradag — edge moet uit microstructuur komen. Prior: vaak kostenpoort of t < 2.

## 7. Uitvoer
Per pair + gepoold: N, winrate, bp/trade bruto/netto, cluster-t, FTMO-EV-tabel, +50% spread, overlap-% met U3/ORB, M5-data-SHA.

---
**Bijgewerkt:** 2026-09-30 21:41 CEST — D-090 re-kickoff: gemeten kosten, U3-afbakening, EURUSD-first freeze, trial/BH.  
**Auteur:** Strateeg (`claude/trusting-faraday-34tsmg`)
