# AUDIT_4 — P1 ORB+BTC Reserve Verificatie (D-096)

**Datum:** 2026-10-01  
**Branch:** claude/auditor-1  
**Autoriteit:** D-096 (CEO/Sandro, 2026-10-01 09:00 AMS)  
**CTO-referentie:** C-020 (`0a97602`)  
**Reserve 2025→:** eenmalig geopend voor P1 per D-096  

---

## Methode

Onafhankelijke herrekening met bevroren schalen uit `results/cto/p1_scales.json`  
(sA=3.583118, sB=1.512771, frozen op train 2021-2023, nooit herschat op reserve).  
Dagelijkse rendementen geladen uit `results/cto/p1_reserve/p1_reserve_daily.csv`.  
CTO-engine (`engine/ftmo.py`, validated AUDIT_1) opnieuw aangeroepen met scale=1.0.

**Schaalverificatie:** max |port_check − port_csv| = 4.86e-16 → identiek ✓

---

## Statistieken reserve-venster (2025-01-01 → 2026-09-23)

| Maatstaf | Auditor | CTO C-020 | Concordant |
|---|---:|---:|---|
| N_days | 448 | 448 | ✓ |
| port_mean | +1.60e-4 | +1.60e-4 | ✓ |
| port_std | 0.01297 | 0.01297 | ✓ |
| ann_SR | 0.195 | 0.195 | ✓ |
| t NW-L5 | 0.2434 | 0.243 | ✓ |
| leg_A_mean (ongeschaald) | +1.65e-4\* | +1.65e-4 | ✓ |
| leg_B_mean (ongeschaald) | −2.84e-4\* | −2.84e-4 | ✓ |
| p1·p2 FTMO EV | 0.776 | 0.780 | ✓ (MC-ruis) |
| net_ev_monthly | €232 | €242 | ✓ (−4%, MC-ruis) |
| stress net_ev_monthly | €223 | €208 | ✓ (MC-ruis) |
| BTC reserve N_trades | 119 | 119 | ✓ |
| BTC reserve mean bruto | −9.4 bp | −9.4 bp | ✓ |

\* Auditor computes scaled (sA×leg = +5.90e-4, sB×leg = −4.30e-4); unscaled = CTO-waarden ÷ scale. Teken gelijk.

---

## Beslisregels (PREREG_FTMO_P1_ORB_BTC §3)

| Criterium | Waarde | Drempel | Uitkomst |
|---|---:|---|---|
| net_mean > 0 | +1.60e-4 | > 0 | ✓ PASS |
| **day_clust_t ≥ 2.0** | **0.243** | **≥ 2.0** | **✗ FAIL** |
| **ann_SR ≥ 0.8** | **0.195** | **≥ 0.8** | **✗ FAIL** |
| p1·p2 ≥ 0.35 | 0.776 | ≥ 0.35 | ✓ PASS |
| net_EV > 0 | +€232/m | > 0 | ✓ PASS |
| stress p1·p2 ≥ 0.35 | 0.773 | ≥ 0.35 | ✓ PASS |
| stress net_EV > 0 | +€223/m | > 0 | ✓ PASS |
| leg_A mean ≥ 0 (ORB) | +1.65e-4 | ≥ 0 | ✓ PASS |
| **leg_B mean ≥ 0 (BTC)** | **−2.84e-4** | **≥ 0** | **✗ FAIL** |

**Gefaalde criteria (3): `day_clust_t_ge_2`, `ann_sr_ge_0_8`, `leg_B_mean_ge_0`**

---

## Auditor-verdict: **FAIL**

Volledig concordant met CTO C-020.

**Toelichting:**  
- BTC in reserve 2025-2026 is gemiddeld negatief (−9.4 bp bruto per trade, N=119); in train  
  2021-2023 was dit +22.9 bp. Het BTC-been heeft 2025-2026 mean-gereverteerd onder nul.  
- De t-statistiek (0.24) en SR (0.20) zijn veel te laag: de in-sample-edge is in het  
  reserve-venster niet aanwezig. Dit is een geldige uitkomst van de PREREG-toets.  
- Het positieve EV-getal (€232/m) wordt gedragen door de gunstige FTMO-structuur  
  (laag max-verlies door diversificatie), niet door een statistisch significante edge.  
  Onder de bevroren PREREG-regels telt dit niet als PASS.

**Reserve-hygiëne:** CTO-log (`0a97602`) bevestigt "reserve_2025_touched: true, eenmalig voor P1".  
Geen enkel ander bestand in C-020 commit raakt 2025+-data buiten de P1-run.  
Voorgaande cyclus-checks (AUDIT_2/AUDIT_3) bevestigen dat tot D-096 geen 2025+-data was gebruikt.  
**Reserve correct en volledig verbruikt voor P1.**

Per D-096.4: P1 is dood; reserve voor deze hypothese verbruikt; geen freeze.

---

## Samenvatting

| | |
|---|---|
| Concordantie CTO | **VOLLEDIG** (alle cijfers ≤ MC-ruis) |
| Reserve-hygiëne | **CLEAN** (eenmalig per D-096, niet eerder) |
| PREREG-integriteit | **OK** (schalen bevroren op train; geen herschatting) |
| Auditor-verdict | **FAIL** (3 criteria gefaald) |
