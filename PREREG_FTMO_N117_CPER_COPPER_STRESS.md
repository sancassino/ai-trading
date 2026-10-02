# PREREG_FTMO_N117 — CPER_COPPER_STRESS (US500cash; session-flat; NEW_FAMILY AL)

**Status:** **OPEN** — frozen for U2 cost-gate + formal trial (Lane-B D-092.1 PASS).  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**VOORSTEL:** `VOORSTEL_PRESCREEN_N117.md`.  
**Signal:** Yahoo/proxy **CPER** (copper ETF). **Trade:** `US500cash`.  
**NEW_FAMILY AL:** copper ETF **level** stress → equity session-flat (industrial-metal growth proxy; ≠ Ag/Au ratio; ≠ Cu/Au ratio).  
**Hold:** **session-flat** entry ≈15:30 CET → flat ≈21:00 CET (D-100).  
**TRIAL_COUNT book:** **462** (deze PREREG telt nog niet).  
**Reserve 2025+:** **onaangeroerd.**  
**Geen retune** na freeze.

Pre-screen: `results/R2/n116_n117_prescreen/` — N117 **PASS** train N=**152** mean bruto **+2,89** ≥ gate **2,34**.

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze

| Post | Waarde | Bron |
|------|--------:|------|
| Signal | Yahoo/proxy **CPER** dagclose | `data/daily/CPER.csv` |
| Trade | `US500cash` | FTMO |
| Round-trip intradag (RT) | **0,78 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (EOD flat same CET day) | D-100 session-flat |
| Hold | entry first M5 **[15:30, 15:45] CET** → flat **21:00 CET** | bevroren |
| **Gate (binding)** | **3 × 0,78 = 2,34 bp** | pure intradag; geen D-097 50-floor |
| Stress (informeel) | **1,5 × 2,34 = 3,51 bp** | vóór formal t |

Alfa = signed mean **bruto prijs**; geen swap-credit.

---

## 2. Economisch mechanisme (NEW_FAMILY AL)

`NEW_FAMILY: AL` — CPER close as **copper level / industrial growth** risk-appetite proxy into DM equity beta:

1. `z40 = (CPER_t − mean_40(CPER)) / stdev_40(CPER)`.
2. **stress_buy:** `z40 > +1,5` → **SHORT** US500 (copper spike = late-cycle / cost-push risk-off); `z40 < −1,5` → **LONG** (copper crash = growth-scare bounce / relief); else skip.
3. Maps to cheap FTMO index CFD (**US500cash**), not copper CFD.

**Distinct / dead-set guard:**
- ≠ **N113 SILVER_GOLD_RATIO** FAIL_COST_GATE (Ag/Au ratio ≠ copper **level**)
- ≠ **COPPER_GOLD_MACRO** prior Lane-A (Cu/Au **ratio** ≠ CPER level alone)
- ≠ **N112 GAS** FAIL_T / **N101 CRACK** / **N98 USOIL→US100** / copper CFD trade leg
- ≠ HYG/EMB/VIX/SECTOR_DISP / L60 / ORB-meta / UKOIL-OVN / CORN / N75–N116 clones

---

## 3. Bevroren regel

**Signal (dag t, na US ETF close ≈22:00 CET):**
1. Data: Yahoo/proxy dagclose **CPER**.
2. `z40` as above.
3. stress_buy long/short/skip as §2.

**Execution (dag t+1, FTMO M5 `US500cash`) — D-100 session-flat:**
4. Entry: close van eerste M5-bar ≥ **15:30 CET** (span ≤15 min). Ontbreekt → skip day.
5. Exit: close van laatste M5-bar ≤ **21:00 CET** same day. **Geen overnight. Geen copper CFD trade leg.**
6. PnL: `pnl_bp = position × (P_exit / P_entry − 1) × 1e4`.
7. Non-overlapping (≤1 trade/dag).
8. **Verboden:** thr-grid op 2025+; overnight hold; Cu/Au ratio rewrite; silver/gold rewrite; soft gate.

---

## 4. D-092.1 pre-screen (train-only; binding for PREREG eligibility)

| Metric | Value |
|--------|------:|
| Train | 2021-01-01 … 2023-12-31 |
| N | **152** (≥150) |
| Mean bruto | **+2,89 bp** (≥ 2,34) |
| Median | **−2,21 bp** |
| Hit-rate | 0,48 |
| Years | 2021 **+0,52** / 2022 **+11,84** / 2023 **−5,56** |
| Verdict | **PASS_may_PREREG** |
| Artifacts | `results/R2/n116_n117_prescreen/prescreen.json` + `n117_trades_train.csv` |

**Note for U2:** median **negative** (−2,21) and 2023 train year **−5,56** — skew/stress risk even though mean PASS; no thr-grid, no Cu/Au rewrite, no overnight, no soft gate.

**D-094a reden (b):** copper price stress as growth-cycle / risk-appetite signal for DM equity beta — distinct from silver/gold ratio and from copper/gold ratio; FTMO-M5 for costs.

---

## 5. Splits / anti-kloon

- **Train:** 2021–2023. **Test:** 2024 (U2). **Reserve 2025+:** untouched.
- FAIL → STOP (geen thr-grid, geen copper CFD twin, geen Cu/Au rewrite, geen overnight, geen soft gate).

---

## 6. Bestanden / catalogus-ID

- **PREREG:** `PREREG_FTMO_N117_CPER_COPPER_STRESS.md` (**N117** — **OPEN**)
- **VOORSTEL:** `VOORSTEL_PRESCREEN_N117.md`
- **Screen:** `results/R2/n116_n117_prescreen/`
- **Catalogus-ID:** **N117** / NEW_FAMILY **AL**
- Branch: `claude/trusting-faraday-34tsmg`
- **TRIAL_COUNT (book):** **462**
