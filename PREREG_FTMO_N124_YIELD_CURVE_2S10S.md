# PREREG_FTMO_N124 — YIELD_CURVE_2S10S (US500cash; session-flat; Lane-B from S2)

**Status:** **OPEN** — frozen for U2 cost-gate + formal trial (Lane-B D-092.1 PASS).  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**Bron Lane-A:** Strateeg-2 (`grok/strateeg-2`) @ **`13fe10c`** — cycle_2346.  
**VOORSTEL:** `VOORSTEL_PRESCREEN_N124.md`.  
**Instrument (primary):** `US500cash` (SPY proxy). **Signal-only** Treasury curve (no bond CFD trade leg).  
**NEW_FAMILY AS:** `YIELD_CURVE_2S10S` — US 10Y−3M slope z → equity session-flat.  
**Hold:** **session-flat** entry ≈15:30 CET → flat ≈21:00 CET (D-100; US500 overnight swap avoided).  
**TRIAL_COUNT book:** **464** (deze PREREG telt nog niet).  
**Reserve 2025+:** **onaangeroerd.**  
**Geen retune** na freeze.

Pre-screen: `results/R2/n124_n125_prescreen/` — N124 **PASS** train N=**240** mean bruto **+8,97** ≥ gate **2,34**.

Pointer: `results/lane_b/YIELD_CURVE_2S10S_SOURCE.md` → S2 @ `13fe10c`.

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze

| Post | Waarde | Bron |
|------|--------:|------|
| Signal | US Treasury **10Y−3M** slope (`YLD_US10Y` − `YLD_US3M`) | S2 cycle_2346 / `data/daily/` |
| Trade | `US500cash` | FTMO |
| Round-trip intradag (RT) | **0,78 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (EOD flat same CET day) | D-100 session-flat |
| Hold | entry first M5 **[15:30, 15:45] CET** → flat **21:00 CET** | bevroren |
| **Gate (binding)** | **3 × 0,78 = 2,34 bp** | pure intradag; geen D-097 50-floor |
| Stress (informeel) | **1,5 × 2,34 = 3,51 bp** | vóór formal t |

**Lane-A context (niet de formele poort):** 10Y-3M→SPY z60/thr1.5/flatten_fade hold=5d non-overlap ≤2024: mean bruto **28,93 bp**, day_t **2,53**, n=448, yrs=19,89; POST-N78 drag → net **+21,37 bp COST_OK**. Overnight US500 5-nacht swap duur → Lane-B **session-flat** (D-100). Alfa = signed mean **bruto prijs**; **geen swap-credits**. Lane-A hold=5d overnight is **mapped** to one cash-session trade per signal.

---

## 2. Economisch mechanisme (NEW_FAMILY AS — YIELD_CURVE_2S10S)

`NEW_FAMILY: YIELD_CURVE_2S10S` — US Treasury 10Y−3M slope as **curve-shape / growth-expectations** risk-appetite proxy:

1. `slope_t = YLD_US10Y_t − YLD_US3M_t`.
2. `z60 = (slope_t − mean_60(slope)) / stdev_60(slope)` (min_periods = max(20, 20)).
3. **flatten_fade (freeze):** `z60 > +1,5` → **SHORT** US500 (extreme steep → fade); `z60 < −1,5` → **LONG** (extreme flatten → buy risk); else skip.
4. Maps to cheap FTMO index CFD (**US500cash**), **not** TLT/IEF/TIP bond CFD.

**Distinct / dead-set guard:**
- ≠ **N116 TLT_DURATION** FAIL_T (TLT price level ≠ curve *slope*)
- ≠ **N118 TIP_REALRATE** FAIL_T (TIPS level ≠ 10Y−3M slope)
- ≠ **N120 VNQ_REIT** / REIT_RATE VNQ/TLT ratio / **RATE_CURVE→UKOIL** N79
- ≠ **N114 HYG** / **N100 EMB** / **N93 SECTOR_DISP** / **N78 VIX** / N75–N123 clones
- ≠ overnight multi-day / soft gate / thr-grid / US100 rewrite

---

## 3. Bevroren regel (geen retune)

**Signal (dag t, na Treasury/ETF close ≈22:00 CET):**
1. Data: `data/daily/YLD_US10Y.csv` + `YLD_US3M.csv`.
2. `slope`, `z60` as §2.
3. flatten_fade long/short/skip as §2.

**Execution (dag t+1, FTMO M5 `US500cash`) — D-100 session-flat:**
4. Entry: close van eerste M5-bar ≥ **15:30 CET** (span ≤15 min). Ontbreekt → skip day.
5. Exit: close van laatste M5-bar ≤ **21:00 CET** same day. **Geen overnight. Geen bond CFD leg.**
6. PnL: `pnl_bp = position × (P_exit / P_entry − 1) × 1e4`.
7. Non-overlapping (≤1 trade/dag).
8. **Verboden:** thr-grid op 2025+; overnight hold / swap-credit als alfa; TLT/TIP/IEF rewrite; US100-first; soft gate; RATE_CURVE→oil add-on.

---

## 4. D-092.1 pre-screen (train-only; binding for PREREG eligibility)

| Metric | Value |
|--------|------:|
| Train | 2021-01-01 … 2023-12-31 |
| N | **240** (≥150) |
| Mean bruto | **+8,97 bp** (≥ 2,34) |
| Median | +9,89 bp |
| Hit-rate | 0,57 |
| Long / short | 132 / 108 |
| Years | 2021 **−2,31** / 2022 **+8,57** / 2023 **+12,41** |
| Stress (info) | mean ≥ 3,51 → informal PASS |
| Verdict | **PASS_may_PREREG** |
| Artifacts | `results/R2/n124_n125_prescreen/prescreen.json` + `n124_trades_train.csv` |

**Note for U2:** 2021 train year negative (−2,31) — year-split/stress may still FAIL; no thr-grid, no TLT/TIP rewrite, no overnight.

**D-094a reden (b):** Treasury curve slope (10Y−3M) as growth/risk-appetite timing into DM equity beta — distinct from TLT duration level and TIP real-rate; FTMO-M5 for costs. Lane-A proxy span ~20y ✔.

---

## 5. Splits / anti-kloon

- **Train:** 2021–2023. **Test:** 2024 (U2). **Reserve 2025+:** untouched.
- FAIL → STOP (geen thr-grid, geen TLT/TIP/IEF twin, geen overnight, geen soft gate). Dead label `N124_YIELD_CURVE_2S10S`.

---

## 6. Bestanden / catalogus-ID

- **PREREG:** `PREREG_FTMO_N124_YIELD_CURVE_2S10S.md` (**N124** — **OPEN**)
- **VOORSTEL:** `VOORSTEL_PRESCREEN_N124.md`
- **Source pointer:** `results/lane_b/YIELD_CURVE_2S10S_SOURCE.md`
- **Screen:** `results/R2/n124_n125_prescreen/`
- **Lane-A:** `git show 13fe10c:results/strateeg2_prescreen/cycle_2346/…`
- **Catalogus-ID:** **N124** / NEW_FAMILY **AS**
- Branch: `claude/trusting-faraday-34tsmg`
- **TRIAL_COUNT (book):** **464**
