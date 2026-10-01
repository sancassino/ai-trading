# PREREG_FTMO_N40 — GER40cash Mid-Morning Momentum Continuation

**Status:** **PREREG BEVROREN** — D-092.1 PASS Strateeg screen `n38_n40_prescreen` (N=205, mean bruto **+2,43 bp** ≥ gate **2,16**; train 2021–2023). Formele cost-gate/stress/t volgt U2.  
**Auteur:** Strateeg (Grok).  
**Datum bevriezing:** 2026-10-01 ~09:25 Europe/Amsterdam.  
**Instrument:** `GER40cash`.  
**Kosten RT:** 0,72 bp → drempel **2,16 bp**.  
**≠** N9 fade; ≠ N11 XETRA ORB FAIL_T; ≠ N13 US-Open Sync; ≠ N21 afternoon fade; ≠ S2-GER40_OPEN / GER_US_LEAD; ≠ ORB-family N15–17.

---

## 0. D-092.1 pre-screen (train only)

| Sleeve | Instrument | N | mean bruto | median | gate | Uitkomst |
|--------|------------|--:|----------:|-------:|-----:|----------|
| N40 | GER40cash | **205** | **+2,43 bp** | **−2,28 bp** | **2,16** | **PASS** |

Artefacts: `results/R2/n38_n40_prescreen/`. `date_min` 2022-01-03 (coverage). Reserve 2025+ onaangeraakt.

**Caveat (bindend):** mean PASS maar **median negatief (−2,28)** → scheef/staart-afhankelijk; formele t en stress kunnen FAIL. Eerlijk rapporteren; geen post-hoc retune.

### D-094a
Train 2021–2023. Reden **(b):** index mid-session continuation na opening-noise; proxy FDAX; FTMO-M5 = kosten.

---

## 1. Mechanisme

Na XETRA opening-noise (eerste ~30 min) zet GER40 vaak een mid-morning trend (09:30→12:00) die tot early afternoon (14:00) doorloopt — vóór US-open sync. Continuation, geen ORB-break, geen fade.

---

## 2. Regel (bevroren)

- `mom_bp = 1e4 × (C_1200 − C_0930) / C_0930`
- `|mom| ≥ 40` → side=sign; entry 12:00 close; stop 1×ATR14; flat **14:00 CET**.
- Max 1/dag; swap 0.

**Verboden na zien:** ±40, 09:30/12:00/14:00, ATR-mult, symbool.

---

## 3. Kosten

| Parameter | Waarde |
|-----------|--------|
| RT | 0,72 bp |
| Gate | **2,16 bp** |
| +50% stress | 3 × 1,08 = **3,24 bp** |

---

## 4. Dataverdeling

| Periode | Rol | Status |
|---------|-----|--------|
| 2021–2023 | Train | OPEN — U2 |
| 2024 | Test | ONAANGERAAKT tot CEO |
| 2025+ | Reserve | ONAANGERAAKT |

---

## 5. U2 instructie

1. Cost-gate ≥ 2,16. 2. Stress ≥ 3,24. 3. Dag-clust t ≥ 2,0. FAIL_T → STOP + TRIALS. Geen parameterwijziging.
