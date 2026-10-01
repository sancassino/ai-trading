# PREREG_FTMO_N87 — US30cash opening-gap fade, intradag-flat (CEO, D-094/D-100)

**Status:** Pre-registratie 2026-10-01 ~15:50 Europe/Amsterdam, branch `claude/ftmo-trading-strategy-98mplz`. Train-pre-screen (`results/ceo/prescreen_n87_n89.md`, 2021–2023) is vóór deze commit uitgevoerd (kostenpoort-vorm, geen test/reserve). Formele toets nog niet gedraaid.
**Basis:** `VOORSTEL_PRESCREEN_N87.md` (Strateeg). Tijd eenduidig gemaakt in **brokerservertijd**.

## 1. Bevroren regel
- Instrument US30cash (M5 `data/m5gz/US30cash.csv.gz`). Dagen ma–vr.
- `prev_close` = close van de laatste M5-bar ≤ 23:00 servertijd van de vorige handelsdag.
- `open` = open van de eerste M5-bar ≥ 08:00 servertijd van de dag.
- `gap_bp = 1e4 × (open − prev_close) / prev_close`.
- `gap_bp > +30` → SHORT op `open`; `gap_bp < −30` → LONG op `open`; anders geen trade.
- Exit: close van de laatste M5-bar ≤ 22:55 servertijd (intradag-flat, **geen swap**). Geen stop. Max 1 trade/dag.
- Drempel 30 bp, tijden en richting zijn bevroren; geen tuning.

## 2. Kosten en poort
RT 0,45 bp (COSTS_FTMO); gate 3×RT = 1,35 bp bruto/trade op train 2021–2023, N ≥ 150, +50%-spread-stress.

## 3. Beslisregel
Train 2021–2023 en test 2024: dag-geclusterd netto t ≥ 2,0 in elk, netto gemiddelde > 0 in elk; N_train ≥ 150. Reserve 2025+ onaangeroerd (D-084; vrijgave alleen via CEO-besluit). Daarna `engine/ftmo.py` + Auditor. Bij FAIL: 1 trial (TRIAL +1), geen klonen (geen drempel-/tijd-variatie).

## 4. Verwachting
Prior laag: dag-t train ≈ 1,1 in pre-screen. Faalmodi: weinig onafhankelijke gap-dagen, drift van gap-gedrag 2024+, tijdinterpretatie van de open.
