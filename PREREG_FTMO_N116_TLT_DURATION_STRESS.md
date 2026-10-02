# PREREG_FTMO_N116 — TLT_DURATION_STRESS (US500cash; session-flat; NEW_FAMILY AK)

**Status:** **OPEN** — frozen for U2 cost-gate + formal trial (Lane-B D-092.1 PASS).  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**VOORSTEL:** `VOORSTEL_PRESCREEN_N116.md`.  
**Signal:** Yahoo/proxy **TLT** (20+y UST ETF). **Trade:** `US500cash`.  
**NEW_FAMILY AK:** US long-duration Treasury stress → equity session-flat (rates/duration channel; ≠ HYG/EMB credit).  
**Hold:** **session-flat** entry ≈15:30 CET → flat ≈21:00 CET (D-100; US500 overnight swap avoided).  
**TRIAL_COUNT book:** **462** (deze PREREG telt nog niet).  
**Reserve 2025+:** **onaangeroerd.**  
**Geen retune** na freeze.

Pre-screen: `results/R2/n116_n117_prescreen/` — N116 **PASS** train N=**386** mean bruto **+6,01** ≥ gate **2,34**.

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze

| Post | Waarde | Bron |
|------|--------:|------|
| Signal | Yahoo/proxy **TLT** dagclose | `data/daily/TLT.csv` |
| Trade | `US500cash` | FTMO |
| Round-trip intradag (RT) | **0,78 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (EOD flat same CET day) | D-100 session-flat |
| Hold | entry first M5 **[15:30, 15:45] CET** → flat **21:00 CET** | bevroren |
| **Gate (binding)** | **3 × 0,78 = 2,34 bp** | pure intradag; geen D-097 50-floor |
| Stress (informeel) | **1,5 × 2,34 = 3,51 bp** | vóór formal t |

Alfa = signed mean **bruto prijs**; geen swap-credit.

---

## 2. Economisch mechanisme (NEW_FAMILY AK)

`NEW_FAMILY: AK` — TLT close as **US long-end rates/duration** risk-appetite proxy into DM equity beta:

1. `z120 = (TLT_t − mean_120(TLT)) / stdev_120(TLT)`; `d20 = TLT_t / TLT_{t−20} − 1`.
2. **combo:** `(z120 > +0,5) and (d20 > 0)` → **LONG** US500 (duration rally = easier financial conditions); `(z120 < −0,5) and (d20 < 0)` → **SHORT** (duration crash = rates spike / risk-off); else skip.
3. Maps to cheap FTMO index CFD (**US500cash**), not TLT/IEF CFD.

**Distinct / dead-set guard:**
- ≠ **N114 HYG_CREDIT_STRESS** FAIL_T (HY credit ≠ duration/rates)
- ≠ **N100 EMB** FAIL_T / **N112 GAS** FAIL_T / **N113 SILVER_GOLD** FAIL_COST_GATE
- ≠ REIT_RATE VNQ/TLT **ratio** (this = **TLT level** alone → equity)
- ≠ VIX / SECTOR_DISP / L60 / ORB-meta / UKOIL-OVN / CORN / N75–N115 clones / IEF twin rewrite

---

## 3. Bevroren regel

**Signal (dag t, na US ETF close ≈22:00 CET):**
1. Data: Yahoo/proxy dagclose **TLT**.
2. `z120`, `d20` as above.
3. combo long/short/skip as §2.

**Execution (dag t+1, FTMO M5 `US500cash`) — D-100 session-flat:**
4. Entry: close van eerste M5-bar ≥ **15:30 CET** (span ≤15 min). Ontbreekt → skip day.
5. Exit: close van laatste M5-bar ≤ **21:00 CET** same day. **Geen overnight. Geen TLT/IEF trade leg.**
6. PnL: `pnl_bp = position × (P_exit / P_entry − 1) × 1e4`.
7. Non-overlapping (≤1 trade/dag).
8. **Verboden:** thr-grid op 2025+; overnight hold; HYG/EMB rewrite; IEF twin; soft gate.

---

## 4. D-092.1 pre-screen (train-only; binding for PREREG eligibility)

| Metric | Value |
|--------|------:|
| Train | 2021-01-01 … 2023-12-31 |
| N | **386** (≥150) |
| Mean bruto | **+6,01 bp** (≥ 2,34) |
| Median | +5,29 bp |
| Hit-rate | 0,53 |
| Years | 2021 **+3,39** / 2022 **+9,62** / 2023 **+1,92** |
| Verdict | **PASS_may_PREREG** |
| Artifacts | `results/R2/n116_n117_prescreen/prescreen.json` + `n116_trades_train.csv` |

**D-094a reden (b):** TLT as long-end rates/duration stress proxy into equity beta — distinct from HYG domestic credit and EMB EM hard-currency; FTMO-M5 for costs.

---

## 5. Splits / anti-kloon

- **Train:** 2021–2023. **Test:** 2024 (U2). **Reserve 2025+:** untouched.
- FAIL → STOP (geen thr-grid, geen IEF twin, geen HYG rewrite, geen overnight, geen soft gate).

---

## 6. Bestanden / catalogus-ID

- **PREREG:** `PREREG_FTMO_N116_TLT_DURATION_STRESS.md` (**N116** — **OPEN**)
- **VOORSTEL:** `VOORSTEL_PRESCREEN_N116.md`
- **Screen:** `results/R2/n116_n117_prescreen/`
- **Catalogus-ID:** **N116** / NEW_FAMILY **AK**
- Branch: `claude/trusting-faraday-34tsmg`
- **TRIAL_COUNT (book):** **462**
