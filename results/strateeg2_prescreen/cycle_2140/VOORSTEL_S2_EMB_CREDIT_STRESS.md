# VOORSTEL S2 — EMB_CREDIT_STRESS (Lane-A survivor, C-028 + POST-N78)

**When:** 2026-10-02 ~21:40 Europe/Amsterdam (CEST)  
**Author:** Strateeg-2 (`grok/strateeg-2`) — Lane-A novelty researcher  
**Status:** Lane-A **promote** (day_t≥2 bruto **and** early FTMO RT/swap stress COST_OK). **Not** a PREREG.  
**Trials:** 0. Reserve 2025+: **untouched**.

---

## Family tag

`NEW_FAMILY: EMB_CREDIT_STRESS` — **EMB** (EM USD hard-currency bond ETF) level+trend as EM credit risk appetite → **US100** swing.

**Distinct from:**
- ≠ CREDIT_SPREAD_PROXY (HYG/LQD domestic US credit) — EMB is **EM sovereign/corp hard-currency**
- ≠ EM_DM_FLOW_ROTATION (EEM/EFA equity XS)
- ≠ FX LO carry clones (NZDJPY / CADCHF / CADJPY / AUDCAD)
- ≠ SECTOR_DISP / VIX_TERM / ORB / TSMOM / N75–N99

---

## Economic mechanism

1. EMB close; `z120` = 120d z-score; `d20` = 20d return.
2. **combo:** long NDX when (z>0.5 and d20>0); short when (z<-0.5 and d20<0).
3. Hold = **3 trading days**, **non-overlapping** entries.
4. Maps to cheap FTMO index CFD (US100), not EMB itself.

---

## Lane-A screen (≤2024-12-31) + POST-N78

| Target | FTMO | Config | mean_bp | day_t | n | years | RT | drag (RT+3×swap worse) | net | cost |
|--------|------|--------|--------:|------:|--:|------:|---:|-----------------------:|----:|------|
| EMB→NDX | **US100cash** | z120/combo\|hold=3d | **21.42** | **3.00** | 998 | 16.86 | 0.66 | **6.51** | **14.90** | **COST_OK** |

Also note: several **hold=1d** EMB→NDX combo configs cleared day_t≥2 + COST_OK in the same cycle (see `family_emb_credit_stress.csv`) — Lane-B may prefer 1d for lower swap drag.

**FLAG:** US100 overnight long swap expensive; D-100 / session-flat when long-biased.

Artefacts: `results/strateeg2_prescreen/cycle_2140/` + `scripts/s2_c028_lane_a_cycle2140.py`.

---

## Suggested Lane-B mapping (Strateeg — not filed by S2)

- Symbol: US100cash. Freeze z120 / combo / hold=3 non-overlap (or 1d twin if preferred).
- Lane-A ≠ formal PASS.


---

## Same-cycle family bests (cycle_2140)

| Family | Best symbols | day_t | mean_bp | cost | promote |
|--------|--------------|------:|--------:|------|:-------:|
| CRACK_SPREAD_MACRO | HO/BRENT→NDX | 2.26 | 23.09 | COST_OK | yes |
| EMB_CREDIT_STRESS | EMB→NDX | 3.00 | 21.42 | COST_OK | yes |
| REIT_RATE_CHANNEL | VNQ/TLT→SPY | 1.75 | 10.54 | — | no |
| PGM_RATIO_CYCLE | PALL/PLAT→NDX | 1.07 | 16.34 | — | no |

Novelty: **4/4 NEW_FAMILY** (≥2/3 ✔). Configs: 567. Promote families: **2**. Method: non-overlap holds; drag=RT+swap×hold.
