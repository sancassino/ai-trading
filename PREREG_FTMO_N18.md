# PREREG_FTMO_N18 — US500 Overnight Gap Continuation

**Status:** PREREG bevroren — wacht U2 cost-gate.  
**Auteur:** CTO (land na Strateeg VOORSTEL `50561ab`); regel = VOORSTEL_PRESCREEN_N18 (geen post-hoc retune).  
**Datum bevriezing:** 2026-10-01 ~04:30 Europe/Amsterdam.  
**Instrument:** `US500cash`.  
**Kosten RT (COSTS_FTMO.csv):** 0,78 bp → D-092.1 drempel 3 × 0,78 = **2,34 bp**.  
**D-092.1 pre-screen:** **PASS_may_PREREG** (CTO C-014): N=279, mean bruto **+3,52 bp** ≥ 2,34; median **+2,77**; stop_share 0,00; skew_fragile=false.  
**Caveats (bindend in rapportage):** (a) stop 1,5×ATR14 is breed t.o.v. 3u-venster → exits vrijwel altijd flat (geen stop-hit in train); (b) year-split mean 2021 +12,97 / 2022 +6,66 / **2023 −12,17** — formele t kan FAIL_T; toch één eerlijke trial onder bevroren regel.

---

## 1. Mechanisme

Grote overnight gaps (≥ ±50 bp vs prior 22:00 CET close) in US500 weerspiegelen hoge-convictie institutionele positie-opbouw. Bij NY-cash-open (15:30 CET) volgt continuation typisch 2–3 uur. **Tegengesteld** aan N5 gap-fade (FAIL). Non-ORB; distinct van N14 / ORB-familie (N11–N17 dead/FAIL).

**Onderscheid van dode / FAIL sleeves:**
- ≠ N5 (gap FADE ≥ 30 bp; dit = CONTINUATION ≥ 50 bp)
- ≠ N14 US100 NY-Open PM (andere anchor/venster)
- ≠ N11–N17 ORB-familie (geen opening-range; anchor = overnight gap)
- ≠ LUNCH_OPEN

---

## 2. Regel (bevroren)

**Overnight gap (M5, Europe/Amsterdam wall = m5gz):**
- `P_prior_close` = M5-close van de **22:00 CET** bar van de vorige handelsdag
- `P_open` = M5-close van de **15:30 CET** bar (eerste NY cash bar)
- `gap_bp = 1e4 × (P_open − P_prior_close) / P_prior_close`

**Signalen (max 1 trade/dag):**
- `gap_bp ≥ +50` → **LONG** op 15:30 CET close
- `gap_bp ≤ −50` → **SHORT** op 15:30 CET close
- Anders → geen trade

**Stop:** 1,5 × ATR14 (dag; prior complete days) vanaf instapprijs.  
**Exit:** hard flat **18:30 CET**. Geen target. Swap = 0 (intradag).

---

## 3. Kosten en drempel

| Parameter | Waarde |
|-----------|--------|
| Instrument | US500cash |
| RT-kosten | 0,78 bp (COSTS_FTMO.csv) |
| D-092.1 drempel | 3 × 0,78 = **2,34 bp** |
| +50% stress | 3 × 1,17 = **3,51 bp** |
| Pre-screen | +3,52 bp mean bruto; N=279 (C-014) |

---

## 4. Dataverdeling (D-084/D-091.5, bindend)

| Periode | Rol | Status |
|---------|-----|--------|
| 2021-01-01 … 2023-12-31 | Train (U2 cost-gate + formele t) | OPEN — U2 |
| 2024-01-01 … 2024-12-31 | Test (alleen na CEO-vrijgave) | ONAANGERAAKT |
| 2025-01-01 → | Reserve | ONAANGERAAKT |

---

## 5. Uitvoerder-2 instructie

**Volgorde (D-092.1):**
1. **Cost-gate train:** mean bruto (bp) op train 2021–2023 met §2. Gate = **2,34**. PASS → stap 2. FAIL → STOP.
2. **Stress-gate (+50%):** gate_stress = **3,51**. PASS → stap 3. FAIL → vermelding; optioneel formele t.
3. **Formele t-test (dag-geclusterd, Newey-West L=5):** t ≥ 2,0. PASS → shortlist. FAIL_T → STOP.
4. **Test (2024):** alleen na CEO-vrijgave; nu ONAANGERAAKT.

Regel identiek aan §2 — geen parameterwijziging na dit PREREG. **TRIAL_COUNT:** append TRIALS.csv bij stap 3. Stand bij bevriezing: **446**. Reserve 2025+ onaangeraakt.
