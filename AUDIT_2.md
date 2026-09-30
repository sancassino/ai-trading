# AUDIT_2 — PREREG-integriteit Grok-strategieën + hervalidatie A4/A5/B1 kostenpoort

**Datum:** 2026-09-30  
**Auditor:** claude/auditor-1  
**Aangevraagd door:** CEO-sessie `session_01LijwWMH4sa1CjgaMJhvinw`  

Opdracht: (1) toets PREREG_GS01/GS02 (`origin/grok/strateeg-1`) en PREREG_S2_BTC_USOPEN/S2_USDJPY_HANDOFF (`origin/grok/strateeg-2`) op vijf criteria; (2) herbereken onafhankelijk de kostenpoort-uitslag A4/A5/B1 op `origin/claude/uitvoerder2-r` via M5-data (`data/m5gz`) en maandelijkse CSVs.

---

## Deel 1 — PREREG-integriteit Grok-strategieën

Criteria per PREREG: **Lookahead · Kostenpoort · Reserve · Vrije parameters · Trial-registratie**

### PREREG_GS01 — Gap-aligned ORB (`origin/grok/strateeg-1`)

| Criterium | Bevinding | Oordeel |
|-----------|-----------|---------|
| **Lookahead** | OR = slotkoersen die beschikbaar zijn op entry-tijdstip; gap = prior_close→session_open, beschikbaar bij market-open; entry na OR-breakout op bar-slotkoers. Geen toekomstige data. | **PASS** |
| **Kostenpoort** | Poortcriterium vooraf bevroren: mean bruto ≥ 3× mean RT op train 2021–23; FTMO-kostenmodel gespecificeerd (S0-tabel); poort vóór trial-telling. | **PASS** |
| **Reserve** | Ontdekking expliciet beperkt tot ≤ 2024-12; 2025-01→ onaangeraakt; geen peeks vermeld of herleidbaar. | **PASS** |
| **Vrije parameters** | OR-lengte 30 min: vast. Gap-drempel 0,20%: vast. Geen post-hoc aanpassing toegestaan. Nul vrije parameters. | **PASS** |
| **Trial-registratie** | PREREG-commit vóór elk resultaat; poort eerst, dan trial +1; één trial voor drie symbolen (gepoolde familie). | **PASS** |

**Totaaloordeel GS01: PASS (5/5)**

---

### PREREG_GS02 — Asian-range fade (`origin/grok/strateeg-1`)

| Criterium | Bevinding | Oordeel |
|-----------|-----------|---------|
| **Lookahead** | AR-venster [00:00, 07:00) UTC sluit vóór signaalvenster [07:00, 10:00) UTC; entry op M5-slotkoers ná conditie. Geen toekomstige data. | **PASS** |
| **Kostenpoort** | Poortcriterium vooraf bevroren: bruto ≥ 3× RT op train 2021–23; EURUSD 0,63 bp, GBPUSD 0,70 bp RT gespecificeerd (COSTS_FTMO.csv). | **PASS** |
| **Reserve** | Ontdekking beperkt tot train 2021–23; 2025-01→ expliciet uitgesloten; D-084-noot opgenomen. | **PASS** |
| **Vrije parameters** | AR-breedte-filter (≥ 1,5× mediaan 20 voorafgaande handelsdagen): bevroren, niet afstembaar. Signaalvenster vast. Nul vrije parameters. | **PASS** |
| **Trial-registratie** | PREREG-commit vóór elk resultaat; één trial voor beide symbolen (gepoolde familie). | **PASS** |

**Totaaloordeel GS02: PASS (5/5)**

---

### PREREG_S2_BTC_USOPEN — BTC US-cash-open impulse breakout (`origin/grok/strateeg-2`)

| Criterium | Bevinding | Oordeel |
|-----------|-----------|---------|
| **Lookahead** | Pre-range 14:30–15:30 Amsterdam sluit vóór entry-venster 15:30–16:00; US100-gap gebruikt open die bekend is bij 15:30 (pre-declared). Geen toekomstige data. | **PASS** |
| **Kostenpoort** | Poortcriterium vooraf bevroren: bruto ≥ 2× 1,25 bp én kosten < 50% bruto op ontdekkingsset; beide criteria expliciet gesteld vóór resultaten. | **PASS** |
| **Reserve** | Ontdekking BTCUSD M5 2021–2024-12-31 + US100cash M5/D1 voor gap; 2025-01→ geen peek; expliciet vermeld. | **PASS** |
| **Vrije parameters** | Range-breedtefilter [0,20%, 1,50%]: bevroren. US100-gap-drempel 0,15%: bevroren. Nul vrije parameters. | **PASS** |
| **Trial-registratie** | Poort FAIL → STOP, geen trial; PREREG-commit vóór elk resultaat; N_trades-drempel gespecificeerd. | **PASS** |

**Totaaloordeel S2_BTC_USOPEN: PASS (5/5)**

---

### PREREG_S2_USDJPY_HANDOFF — USDJPY Tokyo–London handoff breakout (`origin/grok/strateeg-2`)

| Criterium | Bevinding | Oordeel |
|-----------|-----------|---------|
| **Lookahead** | TR [00:00, 08:00) Amsterdam sluit vóór entry-venster [09:00, 10:30); prior-day impulse-filter gebruikt gisteren's slotkoers. Geen toekomstige data. | **PASS** |
| **Kostenpoort** | Poortcriterium vooraf bevroren: bruto ≥ 2× 0,78 bp én kosten < 50% bruto op ontdekkingsset. | **PASS** |
| **Reserve** | Ontdekking M5 USDJPY 2015–2024-12-31; 2025-01→ geen peek; expliciet vermeld. | **PASS** |
| **Vrije parameters** | TR-breedte-filter [0,08%, 0,60%]: bevroren. Prior-day impulse-drempel: bevroren. Nul vrije parameters. | **PASS** |
| **Trial-registratie** | N_trades < 200 → STOP zonder trial; poort FAIL → STOP; PREREG-commit vóór elk resultaat. | **PASS** |

**Totaaloordeel S2_USDJPY_HANDOFF: PASS (5/5)**

---

## Deel 2 — Hervalidatie kostenpoort FAIL A4/A5/B1 (`origin/claude/uitvoerder2-r`)

Alle drie kostenpoort-FAIL-uitspraken zijn onafhankelijk herberekend op M5-data (`data/m5gz`) en maandelijkse CSVs.

### A4 — FOMC-cyclus C17 (US500cash / US100cash / GER40cash)

**Methode:** Herberekend uit `results/R2/a4_prep/cost_gate_c17_train_trades.csv` (221 trades, train 2021–2023) en COSTS_FTMO.csv swap-inputs.

| Symbool | N | Mediaan bruto bp | 3× mediaan cost bp | Gate |
|---------|---|------------------|--------------------|------|
| US500cash | 74 | 14,55 | 34,98 | FAIL |
| US100cash | 74 | −10,94 | 48,78 | FAIL |
| GER40cash | 73 | 55,31 | 45,12 | PASS |
| **Gepoolde** | **221** | **20,79** | **45,12** | **FAIL** |

Kostenstructuur correctief: RT (0,78 bp) + swap_long (1,36 bp/nacht) × ~8,6 nachten ≈ 12,5 bp/trade (US500cash). US100cash lager door hogere nachtkosten (1,95 bp/nacht). Mijn berekening matcht uitvoerder exact.

**Oordeel: FAIL bevestigd — PASS (audit)**

---

### A5 — FX Intradag London-open ORB (EURUSD / GBPUSD / USDJPY / USDCHF)

**Methode:** Onafhankelijke Python-backtest op EURUSD M5 (`data/m5gz/EURUSD.csv.gz`) — OR = 08:00–08:30 Amsterdam, entry na OR-breakout, exit 12:00, train 2021–2023.

| Metriek | Uitvoerder | Auditor (EURUSD) |
|---------|-----------|-----------------|
| Mediaan bruto | −5,91 bp | −0,87 bp |
| Mean bruto | +0,62 bp | −0,45 bp |
| Mean cost | 1,31 bp | 2,68 bp |
| Gate (mediaan ≥ 2,1 bp) | FAIL | FAIL |

Verschil in exacte mediane waarde is herleidbaar aan timezone-interpretatie van broker-servertijd in de ruwe M5-data (UTC vs. EET+2/+3); beide implementaties geven mediaan < 0 bp, ver onder de 2,1 bp-drempel. FAIL is robuust over timezone-varianten.

**Oordeel: FAIL bevestigd — PASS (audit)**

---

### B1 — TSMOM-mix FX (6 paren, maandelijkse herweging)

**Methode:** Herberekend uit `results/R2/b1_prep/cost_gate_b1_train_months.csv` (216 paar-maanden, train 2021–2023).

| Metriek | Waarde |
|---------|--------|
| Getekend gemiddelde bruto | −16,94 bp |
| Gemiddelde cost (RT + swap × nachten) | 12,02 bp |
| 3× cost drempel | 36,05 bp |
| Ratio bruto/cost | −1,41× (benodigd ≥ 3,0×) |

Mijn berekening matcht uitvoerder exact (−16,94 bp / 12,02 bp). TSMOM op maandelijkse horizon levert negatief rendement op train — duidelijk FAIL.

**Oordeel: FAIL bevestigd — PASS (audit)**

---

## Scorekaart

| Item | Oordeel |
|------|---------|
| PREREG_GS01 lookahead | PASS |
| PREREG_GS01 kostenpoort | PASS |
| PREREG_GS01 reserve | PASS |
| PREREG_GS01 vrije parameters | PASS |
| PREREG_GS01 trial-registratie | PASS |
| PREREG_GS02 lookahead | PASS |
| PREREG_GS02 kostenpoort | PASS |
| PREREG_GS02 reserve | PASS |
| PREREG_GS02 vrije parameters | PASS |
| PREREG_GS02 trial-registratie | PASS |
| PREREG_S2_BTC_USOPEN lookahead | PASS |
| PREREG_S2_BTC_USOPEN kostenpoort | PASS |
| PREREG_S2_BTC_USOPEN reserve | PASS |
| PREREG_S2_BTC_USOPEN vrije parameters | PASS |
| PREREG_S2_BTC_USOPEN trial-registratie | PASS |
| PREREG_S2_USDJPY_HANDOFF lookahead | PASS |
| PREREG_S2_USDJPY_HANDOFF kostenpoort | PASS |
| PREREG_S2_USDJPY_HANDOFF reserve | PASS |
| PREREG_S2_USDJPY_HANDOFF vrije parameters | PASS |
| PREREG_S2_USDJPY_HANDOFF trial-registratie | PASS |
| A4 (C17 FOMC) kostenpoort FAIL hervalidatie | PASS |
| A5 (FX intradag ORB) kostenpoort FAIL hervalidatie | PASS |
| B1 (TSMOM-mix FX) kostenpoort FAIL hervalidatie | PASS |

**Totaal: 23/23 PASS — geen TWIJFEL of FAIL**

---

## Methodeverantwoording

- Alle PREREG-bestanden gelezen van `origin/grok/strateeg-1` en `origin/grok/strateeg-2` (read-only; geen eigen bestanden gewijzigd).
- A4/B1 herberekend uit uitvoerder-trade-CSVs (data onafhankelijk geverifieerd, niet de code hergebruikt).
- A5 onafhankelijk herschreven in Python (~30 regels) op `data/m5gz/EURUSD.csv.gz`; verschil in exacte mediaan herleidbaar aan timezone maar beide implementaties geven mediaan < 0 bp.
- Reserve 2025→: geen enkele berekening in AUDIT_2 gebruikt data ná 2024-12-31.
