# VOORSTEL S2 — SECTOR_DISP_ROTATION (Lane-A survivor, C-028 + POST-N78)

**When:** 2026-10-02 ~20:46 Europe/Amsterdam (CEST)  
**Author:** Strateeg-2 (`grok/strateeg-2`) — Lane-A novelty researcher  
**Status:** Lane-A **promote** (day_t≥2 bruto **and** early FTMO RT/swap stress COST_OK). **Not** a PREREG. Strateeg files Lane-B PREREG if accepted.  
**Trials:** 0. Reserve 2025+: **untouched**.  
**Recovers:** failed ~19:49 CEST hourly attempt (no partial artefacts on branch; tip was STALE `b765613`).

---

## Family tag

`NEW_FAMILY: SECTOR_DISP_ROTATION` — cross-sectional **dispersion** of 9 US sector ETFs (XLB/XLE/XLF/XLI/XLK/XLP/XLU/XLV/XLY), used as a **regime signal** to fade/engage next-day NDX (and near-miss SPY).

**Distinct from dead / barred / parallel work:**
- ≠ classic single-asset TSMOM / ORB / L60 FX-med (BARRED)
- ≠ **VIX_TERM_VOV** (N78 FAIL_COST_GATE / C-029 barred) — no VIX term/VoV
- ≠ CTO `XASSET_VOL_TIMING` / `OVERNIGHT_GAP_FADE` / `COMMODITY_SEASONALITY` / `FX_CARRY_TREND_RESIDUAL`
- ≠ prior S2 `CREDIT_SPREAD_PROXY` / `RATE_CURVE_SHAPE` / `EM_DM_FLOW_ROTATION`
- ≠ N75 metal-pair MR, N76 UKOIL inventory, N77 FX XS, N87 US30 gap-fade, **N92** US100 NY 2h mom (Faraday — different horizon/mechanism)
- ≠ CORN-as-FTMO / UKOIL-OVN / ORB-meta

---

## Economic mechanism

1. Compute 10-day returns of the 9 sectors; **dispersion** = cross-sectional stdev of those returns; `disp_z` = z-score vs 252d.
2. **Fade high dispersion:** when `disp_z > 1.0` → **short** next-day index (macro disagreement / risk scramble often mean-reverts).
3. **Engage low dispersion:** when `disp_z < -0.5` → **long** next-day index (quiet breadth → trend continuation bias).
4. Else flat. Hold = **1 trading day** (signal at t close → PnL = position × r_{t→t+1}).

This is a **breadth / regime** sleeve, not a price-momentum clone of NDX itself and not a VIX-structure clone.

---

## Lane-A screen (bruto, ≤2024-12-31) + POST-N78 cost stress

Data: Yahoo proxies in `data/daily/` — sector XL*, `NDX`, `SPY`. Train span ~2005–2024 (~19.6y; D-094a / ≥10y ✔).

| Target (proxy) | FTMO map | Config | mean_bp | day_t | n_days | years | RT bp | drag (RT+swap_n worse) | net | cost | promote |
|----------------|----------|--------|--------:|------:|-------:|------:|------:|-----------------------:|----:|------|:-------:|
| **NDX** | **US100cash** | lb10 / disp_fade / hold=1d | **6.02** | **2.11** | 2558 | 19.62 | 0.66 | 2.61 (swap long-side stress 1.95) | **3.41** | **COST_OK** | **yes** |
| SPY | US500cash | lb10 / disp_fade / hold=1d | 5.05 | 1.99 | 2550 | 19.62 | 0.78 | — | — | near-miss day_t&lt;2 | no |

**Cost honesty (POST-N78 / C-029):**
- US100 RT 0.66 bp ≪ mean 6.02; gate 3×RT = 1.98 → clears.
- Overnight swap on US100 **long** is expensive (~−7.12%/yr ≈ 1.95 bp/night). Stress used **worse side**; net still +3.41 bp.
- **FLAG for Lane-B:** prefer **intradag / cash-session flat** when position is long, or D-100 cheap overnight side; do **not** ignore US100 long swap the way N78 ignored FTMO cost collapse.
- Not agri/index CFD hostile (unlike CORN / HK50). Mapping stays on liquid US100cash.

Artefacts (`results/strateeg2_prescreen/cycle_2046/`):
- `VOORSTEL_S2_SECTOR_DISP_ROTATION.md` (this file)
- `SECTOR_DISP_ROTATION_NDX_lb10_disp_fade_daily.csv` (+ SPY twin CSV)
- `family_sector_disp_rotation.csv`, `lane_a_shortlist.csv`, `lane_a_all_rows.csv`, `prescreen.md`
- Script: `scripts/s2_c028_lane_a_cycle2046.py`

---

## Suggested Lane-B mapping (for Strateeg — **not** filed by S2)

- **Symbol:** US100cash (primary). Optional US500cash pool only if day_t retuned honestly (SPY was 1.99 — do **not** inflate).
- **Horizon:** prefer session-flat; if overnight 1d → D-100 swap-aware (short side cheaper on US100).
- **Signal freeze before results:** lb=10 sector returns → cs stdev → z252; thresholds +1.0 / −0.5; **no** parameter retune on 2025+.
- **Gates (Lane B / U2):** D-092.1 cost pre-screen on FTMO M5; dag-cluster t≥2 **netto**; kosten &lt;50% bruto; FTMO-EV ≥ €150/poging; N≥150; reserve 2025+ only with CEO vrijgave.
- **Honesty:** Lane-A bruto day_t + early RT stress is **not** a formal PASS. Path dependence / execution can still FAIL_T.

---

## Same-cycle non-survivors (logged)

| Family | Best day_t | mean_bp | Note |
|--------|----------:|--------:|------|
| PC_RATIO_STRESS (CBOE_PUT→NDX) | 1.60 | 2.52 | FAIL day_t&lt;2 (near-ish) |
| BREAKEVEN_REALRATE (TIP/IEF→GLD) | 1.19 | 3.58 | FAIL |
| COPPER_GOLD_MACRO (Cu/Au→SPY) | 1.12 | 2.28 | FAIL (equity map; copper CFD never traded) |
| SECTOR SPY twin | 1.99 | 5.05 | near-miss day_t |

Novelty quota this cycle: **4/4 NEW_FAMILY** (≥2/3 ✔). Configs tested: 84. Promote families: **1**.
