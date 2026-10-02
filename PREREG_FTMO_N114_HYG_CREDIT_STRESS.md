# PREREG_FTMO_N114 — HYG_CREDIT_STRESS (US500cash; session-flat; NEW_FAMILY AI)

**Status:** **OPEN** — frozen for U2 cost-gate + formal trial (Lane-B D-092.1 PASS).  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**VOORSTEL:** `VOORSTEL_PRESCREEN_N114.md`.  
**Signal:** Yahoo/proxy **HYG** (US high-yield corporate bond ETF). **Trade:** `US500cash`.  
**NEW_FAMILY AI:** US domestic HY credit level+trend → equity session-flat (≠ EMB EM hard-currency).  
**Hold:** **session-flat** entry ≈15:30 CET → flat ≈21:00 CET (D-100; US500 overnight swap avoided).  
**TRIAL_COUNT book:** **461** (deze PREREG telt nog niet).  
**Reserve 2025+:** **onaangeroerd.**  
**Geen retune** na freeze.

Pre-screen: `results/R2/n114_n115_prescreen/` — N114 **PASS** train N=**371** mean bruto **+3,81** ≥ gate **2,34**.

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze

| Post | Waarde | Bron |
|------|--------:|------|
| Signal | Yahoo/proxy **HYG** dagclose | `data/daily/HYG.csv` |
| Trade | `US500cash` | FTMO |
| Round-trip intradag (RT) | **0,78 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (EOD flat same CET day) | D-100 session-flat |
| Hold | entry first M5 **[15:30, 15:45] CET** → flat **21:00 CET** | bevroren |
| **Gate (binding)** | **3 × 0,78 = 2,34 bp** | pure intradag; geen D-097 50-floor |
| Stress (informeel) | **1,5 × 2,34 = 3,51 bp** | vóór formal t |

Alfa = signed mean **bruto prijs**; geen swap-credit.

---

## 2. Economisch mechanisme (NEW_FAMILY AI)

`NEW_FAMILY: AI` — HYG close as **US domestic HY credit risk-appetite** proxy into DM equity beta:

1. `z120 = (HYG_t − mean_120(HYG)) / stdev_120(HYG)`; `d20 = HYG_t / HYG_{t−20} − 1`.
2. **combo:** `(z120 > +0,5) and (d20 > 0)` → **LONG** US500; `(z120 < −0,5) and (d20 < 0)` → **SHORT**; else skip.
3. Maps to cheap FTMO index CFD (**US500cash**), not HYG/LQD CFD.

**Distinct / dead-set guard:**
- ≠ **N100 EMB_CREDIT_STRESS** FAIL_T (EM hard-currency bond ETF ≠ US domestic HY)
- ≠ **N93 SECTOR_DISP** / **N78 VIX_TERM** / **N112 GAS** FAIL_T / **N113 SILVER_GOLD** FAIL_COST_GATE
- ≠ LQD twin rewrite / overnight / soft gate / N75–N113 clones

---

## 3. Bevroren regel

**Signal (dag t, na US ETF close ≈22:00 CET):**
1. Data: Yahoo/proxy dagclose **HYG**.
2. `z120`, `d20` as above.
3. combo long/short/skip as §2.

**Execution (dag t+1, FTMO M5 `US500cash`) — D-100 session-flat:**
4. Entry: close van eerste M5-bar ≥ **15:30 CET** (span ≤15 min). Ontbreekt → skip day.
5. Exit: close van laatste M5-bar ≤ **21:00 CET** same day. **Geen overnight. Geen HYG/LQD trade leg.**
6. PnL: `pnl_bp = position × (P_exit / P_entry − 1) × 1e4`.
7. Non-overlapping (≤1 trade/dag).
8. **Verboden:** thr-grid op 2025+; overnight hold; EMB rewrite → N100 clone; LQD twin; soft gate.

---

## 4. D-092.1 pre-screen (train-only; binding for PREREG eligibility)

| Metric | Value |
|--------|------:|
| Train | 2021-01-01 … 2023-12-31 |
| N | **371** (≥150) |
| Mean bruto | **+3,81 bp** (≥ 2,34) |
| Median | +3,98 bp |
| Hit-rate | 0,53 |
| Years | 2021 **−10,03** / 2022 **+7,69** / 2023 **+4,82** |
| Verdict | **PASS_may_PREREG** |
| Artifacts | `results/R2/n114_n115_prescreen/prescreen.json` + `n114_trades_train.csv` |

**Note for U2:** 2021 train year negative (−10,03) — stress/year-split may FAIL even if mean PASS; no thr-grid, no EMB/LQD substitute, no overnight rewrite.

**D-094a reden (b):** US HY credit spread/level (HYG) as domestic risk-appetite signal into equity beta — literature on credit–equity co-movement; distinct from EMB; FTMO-M5 for costs.

---

## 5. Splits / anti-kloon

- **Train:** 2021–2023. **Test:** 2024 (U2). **Reserve 2025+:** untouched.
- FAIL → STOP (geen thr-grid, geen EMB rewrite, geen LQD twin, geen overnight, geen soft gate).

---

## 6. Bestanden / catalogus-ID

- **PREREG:** `PREREG_FTMO_N114_HYG_CREDIT_STRESS.md` (**N114** — **OPEN**)
- **VOORSTEL:** `VOORSTEL_PRESCREEN_N114.md`
- **Screen:** `results/R2/n114_n115_prescreen/`
- **Catalogus-ID:** **N114** / NEW_FAMILY **AI**
- Branch: `claude/trusting-faraday-34tsmg`
- **TRIAL_COUNT (book):** **461**
