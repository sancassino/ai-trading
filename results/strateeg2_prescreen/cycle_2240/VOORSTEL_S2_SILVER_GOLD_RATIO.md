# VOORSTEL S2 — SILVER_GOLD_RATIO (Lane-A survivor, C-028 + POST-N78/N93)

**When:** 2026-10-02 ~22:40 Europe/Amsterdam (CEST)  
**Author:** Strateeg-2 (`grok/strateeg-2`) — Lane-A novelty researcher  
**Status:** Lane-A **promote** (day_t≥2 bruto **and** early FTMO RT/swap stress COST_OK). **Not** a PREREG.  
**Trials:** 0. Reserve 2025+: **untouched**.

---

## Family tag

`NEW_FAMILY: SILVER_GOLD_RATIO` — **SLV/GLD** (silver vs gold ETF ratio) extreme fade → **US500** swing. Industrial-vs-monetary metal ratio as risk-appetite mean-reversion (≠ copper/gold).

**Distinct from:**
- ≠ COPPER_GOLD_MACRO (Cu/Au industrial — prior Lane-A FAIL)
- ≠ PGM_RATIO_CYCLE (Pd/Pt — prior Lane-A FAIL day_t)
- ≠ XAU Lon→NY / gold session clones
- ≠ SECTOR_DISP / VIX_TERM / EMB / CRACK / N75–N111

---

## Economic mechanism

1. Ratio = SLV / GLD; `z40` = 40d z-score.
2. **fade_extreme:** short SPY when z>+1.0 (Ag rich vs Au = crowded risk-on → fade); long SPY when z<−1.0 (Ag cheap vs Au = risk-off extreme → bounce).
3. Hold = **5 trading days**, **non-overlapping** entries.
4. Maps to **US500cash** (not silver CFD; not XAU for this best config).

---

## Lane-A screen (≤2024-12-31) + POST-N78/N93

| Target | FTMO | Config | mean_bp | day_t | n | years | RT | drag (RT+5×swap worse) | net | cost |
|--------|------|--------|--------:|------:|--:|------:|---:|-----------------------:|----:|------|
| SLV/GLD→SPY | **US500cash** | z40/thr1.0/fade_extreme\|hold=5d | **22.41** | **2.10** | 635 | 18.58 | 0.78 | **7.56** | **14.84** | **COST_OK** |

**FLAG:** US500 preferred over US100 overnight long. Silver CFD not used (signal-only metals ratio).

Artefacts: `results/strateeg2_prescreen/cycle_2240/` + `scripts/s2_c028_lane_a_cycle2240.py`.

---

## Suggested Lane-B mapping (Strateeg — not filed by S2)

- Symbol: US500cash. Freeze z40 / thr1.0 / fade_extreme / hold=5 non-overlap.
- Lane-A ≠ formal PASS. D-092.1 cost before PREREG.

---

## Same-cycle family bests (cycle_2240)

| Family | Best symbols | day_t | mean_bp | cost | promote |
|--------|--------------|------:|--------:|------|:-------:|
| GAS_EQUITY_MACRO | UNG→SPY | 3.61 | 47.70 | COST_OK | yes |
| SILVER_GOLD_RATIO | SLV/GLD→SPY | 2.10 | 22.41 | COST_OK | yes |
| SMALLCAP_BREADTH | IWM/SPY→NDX | 1.93 | 14.28 | — | no |
| FACTOR_QUALITY_VALUE | QUAL/USMV→SPY | 1.76 | 16.87 | — | no |

Novelty: **4/4 NEW_FAMILY** (≥2/3 ✔). Configs: 1458. Promote families: **2**. Method: non-overlap holds; drag=RT+swap×hold; promote=COST_OK only.
