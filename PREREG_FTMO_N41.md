# PREREG_FTMO_N41 — US30cash Europe→US Open Continuation

**Status:** **PREREG BEVROREN** — D-092.1 PASS Strateeg `n41_n43_prescreen` (N=160, mean bruto **+8,65 bp** ≥ gate **1,35**; train 2021–2023). Formele gate volgt U2.  
**Auteur:** Strateeg (Grok).  
**Datum bevriezing:** 2026-10-01 ~09:28 Europe/Amsterdam.  
**Instrument:** `US30cash`. RT **0,45 bp** → gate **1,35 bp**.  
**≠** N35 US100 (ander instrument); ≠ N20 US30 PM FAIL; ≠ N32 IB FAIL; ≠ ORB/LUNCH_OPEN.

---

## 0. D-092.1 pre-screen

| Sleeve | N | mean bruto | gate | Uitkomst |
|--------|--:|----------:|-----:|----------|
| N41 | **160** | **+8,65 bp** | **1,35** | **PASS** |

Artefacts: `results/R2/n41_n43_prescreen/`. Reserve 2025+ onaangeraakt.

### D-094a
Reden **(b):** index Europe→US handoff microstructure; FTMO-M5 = kosten.

---

## 1–2. Regel (bevroren)

- `eu_bp = 1e4 × (C_1500 − C_0900) / C_0900`
- `|eu| ≥ 40` → side=sign; entry 15:30 close; stop 1×ATR14; flat **17:00 CET**.
- Max 1/dag; swap 0.

---

## 3. Kosten

RT 0,45; gate **1,35**; stress 3×0,675=**2,025**.

---

## 4–5. Data / U2

Train 2021–2023 OPEN; 2024/2025+ ONAANGERAAKT. U2: cost-gate → stress → dag-clust t≥2,0. Geen retune.
