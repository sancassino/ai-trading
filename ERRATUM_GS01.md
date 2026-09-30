# ERRATUM GS01 — Testvenster gecorrigeerd

**Datum:** 2026-09-30 / 2026-10-01 Amsterdam  
**Auteur:** Strateeg (Claude), branch `claude/trusting-faraday-34tsmg`  
**Aanleiding:** D-091 (Manager, 23:45 CEST), NEXT_STEPS v42 prio 5.

---

## Correctie

**PREREG_GS01.md** (op `grok/strateeg-1`) vermeldt:
> "test 2024–26 reported separately"  
> "use 2024–26 as labeled test split"

**Dit is te ruim.** De 2025-01→ reserve is geschorst (D-084). Om de reserve onaangeraakt te laten, geldt:

**Gecorrigeerd testvenster (bindend vóór elke GS01-run):**
- Train: 2021-01-01 … 2023-12-31
- Test: 2024-01-01 … **2024-12-31** (ontdekkingsplafond ≤ 2024-12)
- Reserve: 2025-01-01 → **ONAANGERAAKT** (geen gebruik tot CEO-vrijgave, D-084/D-091.5)

Elke run die 2025-data gebruikt voor kost-gate, t-test of FTMO-EV-berekening is **ongeldig**. Dit geldt ook voor de XAUUSD report-only sleeve.

---

## Status

- Geen resultaten gezien vóór dit commit.
- Geen aanpassing aan de strategie-regel, alleen het testvenster.
- Grok CTO en Uitvoerder-2: gebruik alleen data ≤ 2024-12-31 voor elke GS01-berekening.
