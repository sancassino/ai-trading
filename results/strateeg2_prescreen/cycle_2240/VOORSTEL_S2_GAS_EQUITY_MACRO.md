# VOORSTEL S2 — GAS_EQUITY_MACRO (Lane-A survivor, C-028 + POST-N78/N93)

**When:** 2026-10-02 ~22:40 Europe/Amsterdam (CEST)  
**Author:** Strateeg-2 (`grok/strateeg-2`) — Lane-A novelty researcher  
**Status:** Lane-A **promote** (day_t≥2 bruto **and** early FTMO RT/swap stress COST_OK). **Not** a PREREG.  
**Trials:** 0. Reserve 2025+: **untouched**.

---

## Family tag

`NEW_FAMILY: GAS_EQUITY_MACRO` — **UNG** (US natural-gas ETF) z-stress as energy-shock risk-appetite signal → **US500** swing. **Signal-only** — never map trade to gas CFD (gas CFD cost-hostile).

**Distinct from:**
- ≠ ENERGY_TSMOM / UKOIL-OVN / USOIL→US100 (oil CFD / oil TSMOM)
- ≠ CRACK_SPREAD_MACRO (refining crack HO/BRENT — **DEAD** N101 FAIL_T)
- ≠ CORN-as-FTMO / agri CFD
- ≠ SECTOR_DISP / VIX_TERM / ORB / TSMOM / EMB / N75–N111

---

## Economic mechanism

1. UNG close; `z40` = 40d z-score.
2. **stress_buy:** short SPY when z>+1.5 (gas spike = growth drag / risk-off); long SPY when z<−1.5 (gas crash = relief).
3. Hold = **5 trading days**, **non-overlapping** entries.
4. Maps to cheap FTMO index CFD (**US500cash**), not UNG/NATGAS CFD. Short-bias stress side uses cheaper overnight swap than US100 long.

---

## Lane-A screen (≤2024-12-31) + POST-N78/N93

| Target | FTMO | Config | mean_bp | day_t | n | years | RT | drag (RT+5×swap short-bias) | net | cost |
|--------|------|--------|--------:|------:|--:|------:|---:|----------------------------:|----:|------|
| UNG→SPY | **US500cash** | z40/thr1.5/stress_buy\|hold=5d | **47.70** | **3.61** | 406 | 17.61 | 0.78 | **4.82** | **42.88** | **COST_OK** |

Also: several hold=1d UNG→SPY configs cleared day_t≥2 but only **COST_TIGHT** (mean≈4.6 ≪ 2×3RT) — not promoted this cycle.

**FLAG:** Prefer US500 over US100 for this sleeve (lower long-swap drag if positions flip long). No gas CFD mapping.

Artefacts: `results/strateeg2_prescreen/cycle_2240/` + `scripts/s2_c028_lane_a_cycle2240.py`.

---

## Suggested Lane-B mapping (Strateeg — not filed by S2)

- Symbol: US500cash. Freeze z40 / thr1.5 / stress_buy / hold=5 non-overlap.
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
