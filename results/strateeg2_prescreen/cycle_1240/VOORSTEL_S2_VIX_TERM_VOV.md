# VOORSTEL S2 — VIX_TERM_VOV (Lane-A survivor, C-028)

**When:** 2026-10-01 ~12:45 Europe/Amsterdam (CEST)  
**Author:** Strateeg-2 (`grok/strateeg-2`) — Lane-A novelty researcher  
**Status:** Lane-A **promote** (day_t≥2 bruto). **Not** a PREREG. Strateeg files Lane-B PREREG if accepted.  
**Trials:** 0. Reserve 2025+: **untouched**. No FTMO cost gate run here.

---

## Family tag

`NEW_FAMILY: VIX_TERM_VOV` — VIX term structure (VIX9D / VIX3M) + vol-of-vol regime (`|ΔVIX|` rolling mean, z vs 252d).

**Distinct from dead / barred / parallel work:**
- ≠ classic TSMOM / ORB / L60 FX-med (BARRED)
- ≠ CTO `XASSET_VOL_TIMING` (VIX *percentile* risk-on/off; this uses *term shape* + VoV)
- ≠ N75 metal-pair MR, N76 UKOIL inventory, N77 FX XS rank-rev
- ≠ CREDIT_SPREAD_PROXY / RATE_CURVE_SHAPE / EM_DM_FLOW_ROTATION (same cycle; those FAIL day_t&lt;2)

---

## Economic mechanism

1. **Term stress (backwardation):** when front implied vol (VIX9D) exceeds back (VIX3M) (`term > 1.0`), or VoV spikes (`vov_z > 1.25`), short-term equity risk premia tend to mean-revert upward → **long** next-day index.
2. **Calm contango:** when term is deep contango (`term < 0.90`) and VoV is below average (`vov_z < -0.25`) → reduced long **0.5** (mild risk-on, not full TSMOM chase).
3. Else flat. Hold = **1 trading day** (signal at t close → PnL = position × r_{t→t+1}).

This is a **regime / vol-structure** sleeve, not a price-momentum clone.

---

## Lane-A screen (bruto, ≤2024-12-31)

Data: Yahoo proxies in `data/daily/` — `VIX9D`, `VIX3M`, `VIX`, `NDX`, `SPY`. Train span ~2011–2024 (~14y; D-094a satisfied).

| Target (proxy) | FTMO map (indicative) | Config | mean_bp | day_t | n_days | years | promote |
|----------------|----------------------|--------|--------:|------:|-------:|------:|:-------:|
| **NDX** | US100.cash | vov10 / combo / hold=1d | **6.80** | **2.91** | 2327 | 13.99 | **yes** |
| **SPY** | US500.cash | vov10 / combo / hold=1d | **5.50** | **2.71** | 2320 | 13.99 | **yes** |

Primary recommend: **NDX → US100.cash** (highest day_t). SPY/US500 as secondary / pool leg.

Artefacts:
- `VIX_TERM_VOV_NDX_vov10_combo_daily.csv`
- `VIX_TERM_VOV_SPY_vov10_combo_daily.csv`
- `family_vix_term_vov.csv`, `lane_a_shortlist.csv`, `prescreen.md`
- Script: `scripts/s2_c028_lane_a_cycle1240.py`

---

## Suggested Lane-B mapping (for Strateeg — not filed by S2)

- **Symbols:** US100.cash (primary); optional US500.cash pool.
- **Horizon:** daily-flat or next-cash-session flat (swap≈0 if intradag; if overnight 1d → apply D-100 cheap side / honest swap).
- **Signal freeze before results:** term = VIX9D/VIX3M; vov = mean(|ΔVIX|,10); vov_z vs expanding/rolling 252; positions as above; **no** parameter retune on 2025+.
- **Gates (Lane B / U2):** D-092.1 cost pre-screen; dag-cluster t≥2 **netto**; kosten &lt;50% bruto; FTMO-EV ≥ €150/poging; N≥150 train; reserve 2025+ only with CEO vrijgave.
- **Honesty:** Lane-A bruto day_t is **not** a PASS. FTMO RT on US100 (~0.66 bp) is small vs 6.8 bp mean, but path dependence / overnight / execution can still FAIL_T.

---

## Same-cycle non-survivors (logged)

| Family | Best day_t | Note |
|--------|----------:|------|
| RATE_CURVE_SHAPE (TYX−TNX→SPY) | 1.79 | near-miss |
| CREDIT_SPREAD_PROXY (HYG/LQD→TLT) | 1.48 | FAIL |
| EM_DM_FLOW_ROTATION (EEM/EFA+DXY) | 1.41 | FAIL |

Novelty quota this cycle: **4/4 NEW_FAMILY** (≥2/3 ✔).
