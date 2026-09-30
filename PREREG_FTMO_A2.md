# PREREG FTMO-A2 — Stocks-in-Play ORB earnings (heropening) — stub — 2026-09-30

**Status:** STUB / heropening. Eerdere `PREREG_S2.md` stopte op **kostenpoort** (vaste 60-min / mediaan-poort). FASE 3 vraagt herevaluatie met cluster-t + D-012 (poort op **gemiddelde** bruto) + FTMO-EV — **niet** dezelfde trial opnieuw labelen als nieuw zonder vooraf verschil te bevriezen.  
**Tier:** A2.

## 1. Bevroren referentie (uit `PREREG_S2.md` — niet wijzigen stilzwijgend)
- Bronregel: SFI RP 24-98 / SSRN 4729284 (Zarattini–Barbon–Aziz); OR = eerste 5-min kaars; **alleen OR-richting**; stop 10% ATR14 (paper) of OR-andere-kant (variant); EOD-exit; risico 1%/trade; hefboom ≤ 4×.
- Universum: `universe_us41.txt`; FTMO-M5 2021–26; earnings uit `earnings.csv` (≤ 09:30 ET → zelfde dag, anders volgende).
- Oude poort (Manager v14): mediaan-bruto ≥ 8,7 bp train → faalde.

## 2. Wat FASE 3 wijzigt (voorstel — OPEN tot CEO/Manager akkoord)
| Punt | Oud (S2) | Voorstel A2-heropening |
|------|----------|------------------------|
| Kostenpoort | Mediaan ≥ 8,7 bp | **Gemiddelde** bruto ≥ 3× gemeten rondreis aandelen-CFD (D-012); mediaan informatief |
| Inferentie | t ≥ 3,5 trade-gebaseerd | **Dag-geclusterde** t; drempel vooraf (voorstel t ≥ 2,0 eenzijdig + helften > 0) |
| Maatstaf | SR / t | Primair **FTMO-EV** via `engine/ftmo.py` |
| Varianten | 4 (a–d) | Max **2** vooraf: (b) paper-stop 10% ATR14; (d) uit 12:00 NY — of alleen (b) als 1 trial |

## 3. OPEN (blokkeert freeze)
1. CEO/Manager: is heropening **1 nieuwe trial-familie** (FTMO-EV + cluster-t + average-poort) of informatieve herberekening zonder trial? (Aanbeveling Strateeg: **1 trial** alleen als poort+gates vooraf in dit bestand dicht zijn.)
2. Actuele aandelen-CFD rondreis: plan noemt ≈ 2,9 bp — verifieer in `COSTS_FTMO.csv` / M5 spread voor de 41 namen (niet inventeren).
3. Earnings-dekking 2024–26 compleet voor US41?
4. Welke **één** stop/exit-variant is primair? (Voorstel: paper (b) alleen.)
5. Correlatie/overlap met index-ORB (A1): rapporteer; poort correlatie ≤ 0,5? (OPEN)

## 4. Voorlopige gates (niet bindend tot OPEN dicht)
- Poort gemiddelde bruto ≥ 3× rondreis op train 2021–23.
- Dag-cluster t ≥ 2,0 train én test 2024 (test zonder reserve-2025).
- N ≥ 100 events per helft; ≥ 4/6 kalenderjaren netto > 0.
- FTMO-EV_netto ≥ €80/poging bij sizing met p95 dagverlies ≤ 2%.
- +50% spread robuustheid: t ≥ 1,5 op test (informatief als hard fail).

## 5. Data
FTMO-M5 aandelen + `earnings.csv` + dag-ATR14 zoals S2. Reserve 2025-01→ dicht.

## 6. Volgende stap
1. Uitvoerder-1: spread-tabel US41 uit M5 (gemiddelde/median rondreis).  
2. Strateeg: upgrade stub → volledige PREREG zodra poortgetal + primaire variant bevestigd.  
3. Geen run vóór die freeze.

---
**Aangemaakt:** 2026-09-30 21:41 CEST — D-090 re-kickoff.  
**Auteur:** Strateeg (`claude/trusting-faraday-34tsmg`)
