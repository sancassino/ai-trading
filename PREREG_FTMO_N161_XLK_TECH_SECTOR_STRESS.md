# PREREG_FTMO_N161 — XLK_TECH_SECTOR_STRESS (US100cash; session-flat; Lane-B from S2)

**Status:** **STOP FAIL_T** — U2 `03a1a1d` (cost+stress PASS train N=383 mean +5,42≥1,98; formal FAIL_T t 0,84 / NW-L5 0,98; test N=192 mean −7,14). TRIAL **470→471**. Dead += N161; no XLK/overnight/SECTOR_DISP/XLE/XLF clones. Synced 2026-10-03 ~23:21 CEST.  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**Bron Lane-A:** Strateeg-2 (`grok/strateeg-2`) @ **`51b24bf`** — cycle_0147.  
**VOORSTEL:** `VOORSTEL_PRESCREEN_N161.md`.  
**Signal:** daily **XLK** `z120` / thr **0,5** / **mom_confirm**. **Trade:** `US100cash` only.  
**NEW_FAMILY CD:** tech-sector level plus momentum into the Nasdaq **cash session**. Not SECTOR_DISP. Not XLE/DBC. Not XLF. Not XLU/XLI. Not GAS.  
**Hold:** session-flat 15:30→21:00 CET. **Not** S2 hold=3d. **Not** overnight long US100 (long-swap 1,95 is hostile; swap in this book is 0).  
**TRIAL_COUNT book:** **471** (U2 FAIL_T append).  
**Reserve 2025+:** **onaangeroerd.**

Pointer: `results/lane_b/XLK_TECH_SECTOR_STRESS_SOURCE.md` → S2 @ `51b24bf`.  
Pre-screen: `results/R2/n160_n161_prescreen/`.

Lane-A day_t **2,05** / hold=3d mean is **not** this PASS.

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze

| Post | Waarde | Bron |
|------|--------:|------|
| Signal | Yahoo/proxy **XLK** daily adjclose | S2 cycle_0147 / `data/daily/XLK.csv` |
| Trade | `US100cash` only | FTMO / S2 FLAG (no US500 twin cleared) |
| Round-trip intradag (RT) | **0,66 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (flat same CET day, before the roll) | D-100 session-flat |
| Hold | entry first M5 **[15:30, 15:45] CET** → last M5 **≤ 21:00 CET** | freeze |
| **Gate (binding)** | **3 × 0,66 = 1,98 bp** | pure intradag |
| Stress (informeel) | **1,5 × 1,98 = 2,97 bp** | vóór formal t |

**D-092.1 train 2021–2023 (entry dates):** N=**383**, mean bruto **+5,42 ≥ 1,98** and ≥ stress 2,97 (med +9,77; hit 0,54; years **−10,68 / +6,84 / +9,26**; L/S 242/141). 520 signals reached a session day; 137 skipped for a missing bar. Not DIAG. Not a soft-pass.

**Clone (binding, re-checked on the actual mom_confirm book):** not DEFENSIVE XLU/XLI (trade-date agree **0,73**, cover **0,84** — cover over 0,70, agree under 0,85). Not N92 US100 NY-open 2h momentum (agree **0,49**, cover **1,00**). Signal-day |z| and sign: SECTOR_DISP z **−0,14** agree 0,67 cover 0,59; XLE z40 fade z **−0,16** agree 0,49 cover 0,56; DBC z40 fade z **−0,07** agree 0,43 cover 0,55; XLF z40 fade z **0,45** agree 0,07 cover 0,33; XLU/XLI z40 thr 0,5 z **−0,24** agree 0,64 cover 0,81; UNG z40 stress z **−0,03** agree 0,41 cover 0,38. Bar is |z|≥0,90 or (agree≥0,85 and cover≥0,70). None hit.

---

## 2. Economisch mechanisme

`NEW_FAMILY: XLK_TECH_SECTOR_STRESS` — the Nasdaq cash session follows a stretched **and** momentum-confirmed XLK level. Stretched without the 20-day sign does not trade. The book is one session, so the S2 3-day overnight drag is not the alpha.

**Distinct / dead-set guard:**
- ≠ **N93 SECTOR_DISP** (dispersion of many XL*, not the XLK level)
- ≠ **N143 XLE / DBC** (energy and broad commodity)
- ≠ **N134 XLF** (financials)
- ≠ **N125 DEFENSIVE XLU/XLI** (agree 0,73 on the actual trades; cover high, not a clone)
- ≠ **N112 GAS / UNG**
- ≠ **N92** US100 NY-open 2h momentum (agree 0,49)
- ≠ **N160** XAG NY-fade (FAIL this cycle; no silver leg)
- ≠ gold/index, FX-cross, metal–oil, oil-overnight, GER40-session, factor thr-grid
- ≠ overnight long US100 and ≠ a 3-day hold

---

## 3. Bevroren regel (geen retune)

**Signal (dag t, XLK daily close; frozen — no grid):**
1. `z120 = (XLK_t − mean_120) / stdev_120` (ddof=0). `d20 = XLK_t / XLK_{t−20} − 1`.
2. **mom_confirm:** `z120 > +0,5` and `d20 > 0` → **LONG** US100; `z120 < −0,5` and `d20 < 0` → **SHORT** US100; else skip.

**Execution (dag t+1, FTMO M5 `US100cash`) — D-100 session-flat, one leg:**
3. Entry: close of first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
4. Exit: close of last M5 ≤ **21:00 CET** the same day. **No overnight. Not a 3-day hold.**
5. `pnl_bp = position × (P_exit / P_entry − 1) × 1e4`. Non-overlapping (≤1 trade/day).
6. A signal older than 5 calendar days does not carry.

**Verboden:** thr-grid; US500 remap; XLK CFD leg; XLE/DBC/XLF/XLU-XLI/UNG/SECTOR_DISP rewrite; overnight long US100; treating Lane-A day_t 2,05 as a PASS; softer gate.

---

## 4. Splits

| Venster | Rol |
|---------|-----|
| Train **2021-01-01 … 2023-12-31** | D-092.1 cost gate (deze PASS) + U2 bevestiging |
| Test **2024** | alleen ná cost-gate PASS, in de formal t |
| Reserve **2025+** | onaangeroerd |

**D-094a (b):** XLK daily is long; US100cash M5 from 2021-01. Mechanism is tech-sector level plus momentum into one Nasdaq cash session.

---

## 5. FAIL

Cost-gate FAIL → STOP, geen trial. Cost-gate PASS maar t/NW < 2 → FAIL_T, één trial. Een clone is niet een PASS (al gecheckt; niet gehit). Geen retune.
