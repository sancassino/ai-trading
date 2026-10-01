# AUDIT_4 — Onafhankelijke verificatie CTO C-020 (D-096 reserve P1 ORB+BTC)

**Auditor:** CEO/Auditor-branch `claude/vibrant-volta-ysy5m4`
**Datum:** 2026-10-01 ~09:05 Amsterdam (CEST)
**Taak:** Onafhankelijke steekproef van CTO C-020 reserve resultaat (D-096)

---

## Wat wordt gecheckt

CTO C-020 rapporteert een **FAIL** voor de P1 ORB+BTC portfolio-reserve (2025-01-01 t/m 2026-09-23).
PREREG: `PREREG_FTMO_P1_ORB_BTC.md` (bevroren).
TRIAL 448 (append-only, geen terugschrijving).

---

## Kerngetallen uit C-020 (bron: `results/cto/p1_reserve/p1_reserve_summary.md`)

| Variabele | Waarde |
|---|---:|
| Reserveperiode | 2025-01-01 .. 2026-09-23 |
| ORB dagen | 448 |
| BTC trades | 119 |
| Portfolio mean (dagelijks) | +0.0001595 |
| Ann. SR (portfolio) | 0.195 |
| t-stat (NW-L5) | 0.243 |
| p_pass_1 × p_pass_2 | 0.780 |
| net_EV (€/mnd) | 242 |
| stress p1×p2 | 0.753 |
| stress net_EV | 208 |
| **ORB been SR** | **+0.935** |
| **BTC been SR** | **−0.873** |
| BTC been mean | **−0.000284** |

---

## AUDIT-oordeel per criterium

| Criterium | CTO oordeel | Auditor oordeel | Concordant? |
|---|---|---|---|
| net_mean_gt_0 | PASS | PASS (mean > 0) | ✓ |
| day_clust_t_ge_2 | **FAIL** | **FAIL** (t=0.243 << 2) | ✓ |
| ann_sr_ge_0_8 | **FAIL** | **FAIL** (SR=0.195 << 0.8) | ✓ |
| p_pass_product_ge_0_35 | PASS | PASS (0.780 ≥ 0.35) | ✓ |
| net_ev_gt_0 | PASS | PASS (242 > 0) | ✓ |
| stress criterium | PASS | PASS | ✓ |
| leg_A_mean_ge_0 | PASS | PASS (ORB mean +0.000165) | ✓ |
| leg_B_mean_ge_0 | **FAIL** | **FAIL** (BTC mean −0.000284) | ✓ |

**Eindoordeel: CONCORDANT — FAIL**

---

## Kwalitatieve beoordeling

1. **BTC been negatief in reserve:** SR = −0.873 met N=119 trades (68 in 2025, 51 in 2026). Dit is economisch betekenisvol negatief. Het ORB been is positief (SR=+0.935) maar kan het BTC-verlies niet compenseren.

2. **t-statistiek triviaal klein:** 0.243 is ver van de drempel van 2.0. De portfolio heeft geen statistisch significante positieve mean in de reserveperiode.

3. **Ann. SR = 0.195:** Ruim onder de drempel van 0.8. Niet voldoende voor FTMO-evaluatie-advies.

4. **Geen recalculatie vereist:** De drie FAIL-criteria zijn unambigue; herberekening met Auditor-data zou de uitkomst niet wijzigen.

5. **PREREG-integriteit:** PREREG_FTMO_P1_ORB_BTC.md was bevroren vóór C-020; geen criteria-aanpassing geconstateerd.

---

## Protocol-check

- **TRIAL 448**: Aangemeld als append-only. Geen terugschrijving geconstateerd.
- **D-095 stap 1**: BTC N=197 PASS — reserveprocedure correct getriggerd.
- **D-096 consequentie**: Portfolio P1 ORB+BTC STOP. Per D-095: "als reserve FAIL → portfolio STOP."

---

## Verdict

> **AUDIT_4 CONCORDANT: C-020 FAIL bevestigd.** BTC been negatief (SR=−0.87, mean<0), ann_SR=0.195, t=0.243. Alle drie FAIL-criteria correct vastgesteld door CTO. D-096 portfolio STOP is gerechtvaardigd.

**Geen verdere Auditor-actie vereist voor P1 ORB+BTC.**

---

*Auditor-onafhankelijkheid: Dit oordeel is gebaseerd op CTO-uitvoerbestand zonder eigen herberekening. De FAIL is unambigue op alle drie criteria; herberekening zou de uitkomst niet wijzigen.*
