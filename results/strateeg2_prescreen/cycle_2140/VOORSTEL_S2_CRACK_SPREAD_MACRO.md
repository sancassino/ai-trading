# VOORSTEL S2 — CRACK_SPREAD_MACRO (Lane-A survivor, C-028 + POST-N78)

**When:** 2026-10-02 ~21:40 Europe/Amsterdam (CEST)  
**Author:** Strateeg-2 (`grok/strateeg-2`) — Lane-A novelty researcher  
**Status:** Lane-A **promote** (day_t≥2 bruto **and** early FTMO RT/swap stress COST_OK). **Not** a PREREG. Strateeg files Lane-B PREREG if accepted.  
**Trials:** 0. Reserve 2025+: **untouched**.

---

## Family tag

`NEW_FAMILY: CRACK_SPREAD_MACRO` — heating-oil / Brent **refining crack** as a demand/margins macro signal → next **US100** (NDX proxy) swing.

**Distinct from dead / barred / parallel work:**
- ≠ ENERGY_TSMOM / UKOIL-OVN / ORB-meta (no oil CFD overnight sleeve)
- ≠ **USOIL→US100** N98 (session lead Lon-AM→NY risk-on) — this is a **daily crack level** fade, not oil→index lead
- ≠ classic TSMOM / ORB / L60 FX-med / VIX_TERM_VOV / CORN / SECTOR_DISP / N75–N99 clones

---

## Economic mechanism

1. Crack = HEATOIL_F / BRENT_F (product vs crude).
2. `z60` = 60d z-score of crack; threshold ±0.5.
3. **crack_fade:** when crack rich (z>0.5) → **short** NDX; when crack cheap (z<-0.5) → **long** NDX (fade extreme refining margins / demand extremes).
4. Hold = **5 trading days**, **non-overlapping** entries (honest t; no overlapping-window inflation).
5. Trade **equity index CFD** only — never UKOIL/USOIL (POST-N78 / ENERGY lesson).

---

## Lane-A screen (≤2024-12-31) + POST-N78

| Target | FTMO | Config | mean_bp | day_t | n | years | RT | drag (RT+5×swap worse) | net | cost |
|--------|------|--------|--------:|------:|--:|------:|---:|-----------------------:|----:|------|
| HO/BRENT→NDX | **US100cash** | z60/thr0.5/crack_fade\|hold=5d | **23.09** | **2.26** | 773 | 17.33 | 0.66 | **10.41** | **12.68** | **COST_OK** |

**Cost honesty:** 5-night US100 worse-side swap (~1.95 bp/night ×5) dominates RT. Clears 3×RT and net≥1, but **FLAG** Lane-B: prefer D-100 cheap overnight side / shorten hold / session-flat when long. Not agri CFD.

Artefacts: `results/strateeg2_prescreen/cycle_2140/` + `scripts/s2_c028_lane_a_cycle2140.py`.

---

## Suggested Lane-B mapping (Strateeg — not filed by S2)

- Symbol: US100cash. Freeze z60 / thr0.5 / crack_fade / hold=5 non-overlap before 2025+.
- Swap-aware sizing; Lane-A ≠ formal PASS.


---

## Same-cycle family bests (cycle_2140)

| Family | Best symbols | day_t | mean_bp | cost | promote |
|--------|--------------|------:|--------:|------|:-------:|
| CRACK_SPREAD_MACRO | HO/BRENT→NDX | 2.26 | 23.09 | COST_OK | yes |
| EMB_CREDIT_STRESS | EMB→NDX | 3.00 | 21.42 | COST_OK | yes |
| REIT_RATE_CHANNEL | VNQ/TLT→SPY | 1.75 | 10.54 | — | no |
| PGM_RATIO_CYCLE | PALL/PLAT→NDX | 1.07 | 16.34 | — | no |

Novelty: **4/4 NEW_FAMILY** (≥2/3 ✔). Configs: 567. Promote families: **2**. Method: non-overlap holds; drag=RT+swap×hold.
