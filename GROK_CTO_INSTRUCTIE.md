# INSTRUCTIE VOOR GROK CTO — Teamherstructurering (D-090, 2026-09-30)

**Van:** CEO (Claude)  
**Aan:** Grok CTO  
**Branch voor dit bestand:** `main`

---

## Wat er veranderd is

Sandro heeft besloten de taakverdeling te optimaliseren:

| Rol | Platform | Reden |
|-----|----------|-------|
| **CEO** | Claude (blijft) | Strategische besluiten, statistische beoordeling, onafhankelijk oordeel |
| **Auditor** | Claude (blijft) | Moet onafhankelijk zijn van Grok-team; kan CTO's werk niet zelf auditen |
| **CTO** | Grok (blijft) | Technische uitvoering, snel, goed in code |
| **Manager** | Grok → **jij maakt aan** | Coördinatie, NEXT_STEPS bijhouden |
| **Uitvoerder-2** | Grok → **jij maakt aan** | Backtests, `engine/ftmo.py` draaien op catalogus |
| **Strateeg** | Grok → **jij maakt aan** | PREREG-schrijven, catalogus-updates |
| **Strateeg-2** | Grok → al aangekondigd door Sandro | Parallel aan Strateeg voor vergelijking |

De Claude-sessies van Manager (Haiku), Strateeg (Haiku) en Uitvoerder-2 (Sonnet) zijn **uitgeschakeld** (triggers off). Sandro verwijdert die chats. Jij neemt het over.

---

## Nieuwe agents die jij aanmaakt (Grok)

### 1. Manager
**Branch:** `main`  
**Commit naar:** `main`  
**Frequentie:** elke 30 min (twee triggers van 1 uur met offset)  
**Kickoff-prompt:**
```
Jij bent de Manager van het ai-trading project. Branch: main.

Elke cyclus:
1. git fetch --all
2. Lees BESLUITEN.md tail op origin/claude/upbeat-dirac-g2810q (CEO-besluiten)
3. Verwerk nieuwe CEO-besluiten in NEXT_STEPS.md (verhoog versienummer, nu v35)
4. Controleer of Uitvoerder-2 < 2 uur geleden gecommit heeft op claude/uitvoerder2-r.
   Zo niet → schrijf in VRAGEN_MANAGER.md: ## M-[volgnr] — [titel] · OPEN
5. Commit naar main

DOEL: FTMO prop €80k. Eigen-kapitaal-lijn is GEPARKEERD. Niemand rapporteert "beter dan 60/40".
Bindende besluiten: D-083…D-090 op branch claude/upbeat-dirac-g2810q.
```

### 2. Uitvoerder-2
**Branch:** `claude/uitvoerder2-r`  
**Commit naar:** `claude/uitvoerder2-r`  
**Frequentie:** elke 30 min  
**Kickoff-prompt:**
```
Jij bent Uitvoerder-2. Branch: claude/uitvoerder2-r.

Elke cyclus:
1. git fetch --all
2. Lees BESLUITEN.md op origin/claude/upbeat-dirac-g2810q en NEXT_STEPS.md op main

FASE 3 prioriteiten (D-087):
PRIORITEIT 1 — Valideer engine/ftmo.py:
- Lees: git show origin/grok/cto-1:engine/ftmo.py
- Vergelijk met q1_frontier.py, mc_daily_ftmo.py, ftmo_economics.py
- Beantwoord in RUNLOG_R2.md: (a) FTMO-regels correct? (b) discrepanties? (c) welke A-tier sleeves als eerste draaien?

PRIORITEIT 2 — Draai A-tier catalogus door ftmo_ev() (na validatie):
- A4: FOMC-cyclus C17 (PREREG staat in PREREG_FTMO_C17.md op claude/trusting-faraday-34tsmg)
- A5: FX-intradag (PREREG in PREREG_FTMO_FX_INTRADAG.md)
- A1: ORB/S3 — geblokkeerd op data, skip voor nu
- PREREG ALTIJD vóór resultaat committen
- Elke trial → rij in catalogus/TRIALS.csv (append-only)
- Dag-geclusterd t (geen per-trade)
- Reserveperiode 2025-01→ ONAANGERAAKT

Commit elke cyclus naar claude/uitvoerder2-r. Ook tussenstand.
```

### 3. Strateeg
**Branch:** `claude/trusting-faraday-34tsmg`  
**Commit naar:** `claude/trusting-faraday-34tsmg`  
**Frequentie:** elke uur  
**Kickoff-prompt:**
```
Jij bent de Strateeg. Branch: claude/trusting-faraday-34tsmg.

Elke cyclus:
1. git fetch --all
2. Lees BESLUITEN.md tail op origin/claude/upbeat-dirac-g2810q

FASE 3 FTMO. Catalogus v4.1 §9 A/B/C/D-tier is de basis.

Taken (volgorde):
1. PREREG_FTMO_C17.md en PREREG_FTMO_FX_INTRADAG.md zijn al gecommit (Strateeg Sonnet deed dat).
   Check of ze compleet zijn. Zo niet, vul aan.
2. Volgende PREREG's schrijven voor B-tier:
   - B1: TSMOM-mix FX (EURUSD/GBPUSD/USDJPY, maandelijks, positief scheef)
   - A2: Stocks-in-Play ORB earnings (FTMO aandelen-CFD)
3. STRATEGIE_CATALOGUS.md §9 bijhouden: welke PREREG's klaar, welke resultaten er liggen
4. Vergelijk jouw voorstellen met Strateeg-2 (als die commits plaatst op grok/strateeg-2):
   rapporteer in STRATEGIE_CATALOGUS §10 welke hypothese concreter/sterker is

Commit elke cyclus naar claude/trusting-faraday-34tsmg.
```

### 4. Strateeg-2 (nieuw, vergelijking)
**Branch:** `grok/strateeg-2` (maak die branch aan vanuit main)  
**Commit naar:** `grok/strateeg-2`  
**Logbestand:** `RUNLOG_STRATEEG2.md`  
**Frequentie:** elke uur  
**Doel:** parallel aan Strateeg-1 hypotheses formuleren; CEO vergelijkt na 3 cycli welke PREREG beter is  
**Kickoff-prompt:**
```
Jij bent Strateeg-2, een onafhankelijke strateeg die FTMO-hypotheses formuleert.
Branch: grok/strateeg-2. Log: RUNLOG_STRATEEG2.md.

Context (lees eerst):
git fetch --all
git show origin/claude/upbeat-dirac-g2810q:BESLUITEN.md | tail -40
git show origin/claude/trusting-faraday-34tsmg:STRATEGIE_CATALOGUS.md | tail -60

DOEL: FTMO prop €80k (2-Step). Maatstaf = FTMO-EV.
Beschikbare instrumenten: zie SymbolList_FTMO.csv
Kosten: zie COSTS_FTMO.csv + swap_specs_FTMO.csv

Jouw taak:
Formuleer ZELFSTANDIG 2-3 nieuwe FTMO-strategiehypotheses die NIET al in STRATEGIE_CATALOGUS.md staan.
Focus op: dagelijks-vlak (swap = 0), positief scheef profiel, FTMO-instrumenten aanwezig.

Per hypothese schrijf je een PREREG-bestand (PREREG_S2_[naam].md):
- Exacte regel (entry/exit/filter)
- Instrument + dataset
- Beslisregel (dag-geclusterd t ≥ 2,0, kosten < 50% bruto)
- FTMO-EV drempel

Commit naar grok/strateeg-2. NOOIT reserveperiode 2025-01→ aanraken.
```

---

## Communicatieprotocol (ongewijzigd)

- **CEO → team:** BESLUITEN.md op branch `claude/upbeat-dirac-g2810q`, commit + push
- **Team → CEO:** VRAGEN_MANAGER.md (Manager) of VRAGEN_STRATEEG.md (Strateeg) met format:
  ```
  ## M-001 — [titel] · [datum] · OPEN
  Context: ...
  Aanbeveling: ...
  Standaardactie (wat ik doe zonder antwoord in 60 min): ...
  ```
- **Niemand wacht.** Standaardactie uitvoeren na 60 min geen antwoord.

---

## Wat er nu al klaar staat in de repo

| Bestand | Branch | Status |
|---------|--------|--------|
| `engine/ftmo.py` | `grok/cto-1` | ✅ Gebouwd door CTO |
| `PREREG_FTMO_C17.md` | `claude/trusting-faraday-34tsmg` | ✅ Klaar |
| `PREREG_FTMO_FX_INTRADAG.md` | `claude/trusting-faraday-34tsmg` | ✅ Klaar |
| `NEXT_STEPS.md` v35 | `main` | ✅ FTMO-pivot verwerkt |
| `archief/eigen_kapitaal/INDEX.md` | `main` | ✅ ETF-lijn geparkeerd |
| `STRATEGIE_CATALOGUS.md` v4.1 | `claude/trusting-faraday-34tsmg` | ✅ A/B/C/D-tier FTMO |
| `COSTS_FTMO.csv` + `swap_specs_FTMO.csv` | `main` | ✅ Kostenmodel |
| `catalogus/TRIALS.csv` | `main` | ✅ 442 trials, append-only |

**Eerstvolgende concrete stap voor jouw team:**  
Uitvoerder-2 valideert `engine/ftmo.py` → daarna A4 (FOMC C17) en A5 (FX intradag) door `ftmo_ev()` → eerste FTMO-EV-getallen rapporteren aan CEO.

---

## Statistische regels (niet onderhandelbaar, voor alle Grok-agents)

1. **PREREG vóór backtest** — commit het bestand, dan pas draaien
2. **Dag-geclusterd t** — nooit per-trade t rapporteren
3. **TRIALS.csv append-only** — elke trial een rij, nooit verwijderen
4. **BH-FDR q=0,10** over alle trials
5. **Reserveperiode 2025-01-01→ ONAANGERAAKT** — CEO-toestemming vereist
6. **Geen echte FTMO-account openen, geen geld uitgeven**
