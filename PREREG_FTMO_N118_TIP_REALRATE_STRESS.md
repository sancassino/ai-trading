# PREREG_FTMO_N118 — TIP_REALRATE_STRESS (US500cash; session-flat; NEW_FAMILY AM)

**Status:** **OPEN** — frozen for U2 cost-gate + formal trial (Lane-B D-092.1 PASS).  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**VOORSTEL:** `VOORSTEL_PRESCREEN_N118.md`.  
**Signal:** Yahoo/proxy **TIP** (TIPS ETF). **Trade:** `US500cash`.  
**NEW_FAMILY AM:** US TIPS / real-rate ETF stress → equity session-flat (inflation-linked real rates channel; **TIP≠TLT** nominal duration).  
**Hold:** **session-flat** entry ≈15:30 CET → flat ≈21:00 CET (D-100; US500 overnight swap avoided).  
**TRIAL_COUNT book:** **463** (deze PREREG telt nog niet).  
**Reserve 2025+:** **onaangeroerd.**  
**Geen retune** na freeze.

Pre-screen: `results/R2/n118_n119_prescreen/` — N118 **PASS** train N=**359** mean bruto **+5,38** ≥ gate **2,34**.

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze

| Post | Waarde | Bron |
|------|--------:|------|
| Signal | Yahoo/proxy **TIP** dagclose | `data/daily/TIP.csv` |
| Trade | `US500cash` | FTMO |
| Round-trip intradag (RT) | **0,78 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (EOD flat same CET day) | D-100 session-flat |
| Hold | entry first M5 **[15:30, 15:45] CET** → flat **21:00 CET** | bevroren |
| **Gate (binding)** | **3 × 0,78 = 2,34 bp** | pure intradag; geen D-097 50-floor |
| Stress (informeel) | **1,5 × 2,34 = 3,51 bp** | vóór formal t |

Alfa = signed mean **bruto prijs**; geen swap-credit.

---

## 2. Economisch mechanisme (NEW_FAMILY AM)

`NEW_FAMILY: AM` — TIP close as **US real-rate / inflation-expectations** risk-appetite proxy into DM equity beta:

1. `z120 = (TIP_t − mean_120(TIP)) / stdev_120(TIP)`; `d20 = TIP_t / TIP_{t−20} − 1`.
2. **combo:** `(z120 > +0,5) and (d20 > 0)` → **LONG** US500 (real-rate relief / easier conditions); `(z120 < −0,5) and (d20 < 0)` → **SHORT** (real-rate spike / risk-off); else skip.
3. Maps to cheap FTMO index CFD (**US500cash**), not TIP/TLT CFD.

**Distinct / dead-set guard:**
- ≠ **N116 TLT_DURATION_STRESS** FAIL_T (**TIP≠TLT** — TIPS real-rate ≠ nominal long-duration)
- ≠ **N114 HYG** FAIL_T / **N100 EMB** FAIL_T / **N112 GAS** / **N113 SILVER_GOLD**
- ≠ REIT_RATE VNQ/TLT ratio / IEF twin rewrite of N116
- ≠ VIX / SECTOR_DISP / L60 / ORB-meta / UKOIL-OVN / CORN / N75–N117 clones

---

## 3. Bevroren regel

**Signal (dag t, na US ETF close ≈22:00 CET):**
1. Data: Yahoo/proxy dagclose **TIP**.
2. `z120`, `d20` as above.
3. combo long/short/skip as §2.

**Execution (dag t+1, FTMO M5 `US500cash`) — D-100 session-flat:**
4. Entry: close van eerste M5-bar ≥ **15:30 CET** (span ≤15 min). Ontbreekt → skip day.
5. Exit: close van laatste M5-bar ≤ **21:00 CET** same day. **Geen overnight. Geen TIP/TLT trade leg.**
6. PnL: `pnl_bp = position × (P_exit / P_entry − 1) × 1e4`.
7. Non-overlapping (≤1 trade/dag).
8. **Verboden:** thr-grid op 2025+; overnight hold; TLT rewrite→N116 clone; IEF twin; soft gate.

---

## 4. D-092.1 pre-screen (train-only; binding for PREREG eligibility)

| Metric | Value |
|--------|------:|
| Train | 2021-01-01 … 2023-12-31 |
| N | **359** (≥150) |
| Mean bruto | **+5,38 bp** (≥ 2,34) |
| Median | +4,46 bp |
| Hit-rate | 0,53 |
| Years | 2021 **−7,40** / 2022 **+7,92** / 2023 **+5,27** |
| Verdict | **PASS_may_PREREG** |
| Artifacts | `results/R2/n118_n119_prescreen/prescreen.json` + `n118_trades_train.csv` |

**Note for U2:** 2021 train year negative (−7,40) — stress/year-split may FAIL even if mean PASS; no thr-grid, no TLT substitute, no overnight rewrite.

**D-094a reden (b):** TIP as real-rate / breakeven inflation proxy into equity beta — distinct from TLT nominal long-duration (N116 DEAD) and from HYG/EMB credit; FTMO-M5 for costs.

---

## 5. Splits / anti-kloon

- **Train:** 2021–2023. **Test:** 2024 (U2). **Reserve 2025+:** untouched.
- FAIL → STOP (geen thr-grid, geen TLT rewrite, geen IEF twin, geen overnight, geen soft gate).

---

## 6. Bestanden / catalogus-ID

- **PREREG:** `PREREG_FTMO_N118_TIP_REALRATE_STRESS.md` (**N118** — **OPEN**)
- **VOORSTEL:** `VOORSTEL_PRESCREEN_N118.md`
- **Screen:** `results/R2/n118_n119_prescreen/`
- **Catalogus-ID:** **N118** / NEW_FAMILY **AM**
- Branch: `claude/trusting-faraday-34tsmg`
- **TRIAL_COUNT (book):** **463**
