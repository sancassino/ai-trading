# PREREG_FTMO_N93 — SECTOR_DISP_ROTATION (US100cash; session-flat; Lane-B from S2)

**Status:** **OPEN** — frozen for U2 cost-gate + formal trial (Lane-B C-028 from S2 Lane-A survivor).  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**Bron Lane-A:** Strateeg-2 (`grok/strateeg-2`) @ **`fde4a15`** — `results/strateeg2_prescreen/cycle_2046/VOORSTEL_S2_SECTOR_DISP_ROTATION.md`.  
**Instrument (primary):** `US100cash` (NDX proxy). **Geen** US500cash primary (SPY day_t 1,99 near-miss — niet opblazen).  
**NEW_FAMILY R:** `SECTOR_DISP_ROTATION` — cross-sectionele XL* sector-dispersie → NDX/US100 cash-session.  
**Config freeze:** **lb=10 / disp_fade / thr +1,0 / −0,5** only. **Geen retune.**  
**Hold:** **session-flat** (D-100 verplicht — US100 long overnight swap duur ≈1,95 bp/nacht).  
**TRIAL_COUNT book:** **458** (U2 N92 FAIL_T; deze PREREG telt nog niet).  
**Reserve 2025+:** **onaangeroerd.**

Pointer: `results/lane_b/SECTOR_DISP_ROTATION_SOURCE.md` → S2 artefacts @ `fde4a15` (geen CSV-rewrite).

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze

| Post | Waarde | Bron |
|------|--------:|------|
| Symbool | `US100cash` | FTMO |
| Round-trip intradag (RT) | **0,66 bp** | `COSTS_FTMO.csv` / `COSTS_FTMO_alle` |
| Swap | **0** (EOD flat same CET day — **vóór** overnight swap-window) | D-100 session-flat |
| Hold | cash-session only: entry ≈15:30 CET → flat ≈21:00 CET | bevroren regel |
| **Gate (binding)** | **3 × 0,66 = 1,98 bp** | pure intradag; geen D-097 50-floor |
| Stress (informeel) | **1,5 × 1,98 = 2,97 bp** | vóór formal t |

**Lane-A context (niet de formele poort):** Yahoo proxy NDX lb10/disp_fade hold=1d overnight: mean bruto **6,02 bp**, day_t **2,11**, n=2558, yrs=19,62; POST-N78 drag (RT+swap_n worse) → net **+3,41 bp COST_OK**. S2 **FLAG:** US100 long overnight swap duur → Lane-B **moet** session-flat (of goedkoopste overnight-kant). Deze PREREG kiest **session-flat** — swap zit **niet** in de edge; alfa = signed mean **bruto prijs**.

---

## 2. Economisch mechanisme (NEW_FAMILY R)

`NEW_FAMILY: SECTOR_DISP_ROTATION` — cross-sectionele **dispersie** van 9 US sector-ETFs (XLB/XLE/XLF/XLI/XLK/XLP/XLU/XLV/XLY) als **regime-signaal**:

1. Hoge dispersie (`disp_z > 1,0`) → **short** index (macro-onenigheid / risk-scramble mean-reverts).
2. Lage dispersie (`disp_z < −0,5`) → **long** index (quiet breadth → trend-continuation bias).
3. Anders flat.

Dit is een **breadth / regime**-sleeve, **geen** price-momentum van NDX zelf, **geen** VIX-term/VoV, **geen** ORB, **geen** classic TSMOM, **geen** L60 FX-med.

**Distinct / dead-set guard:**
- ≠ **N78 VIX_TERM_VOV** FAIL_COST_GATE / C-029 barred
- ≠ **N92** US100 NY 2h mom FAIL_T (TRIAL **458**) — ander mechanisme/horizon (price-mom vs sector-disp regime)
- ≠ N87 gap-fade / N80 UKOIL-OVN / ORB-meta / L60 FX-med / CORN / ENERGY / IDX_SHORT
- ≠ CTO XASSET_VOL_TIMING / OVERNIGHT_GAP_FADE / COMMODITY_SEASONALITY
- ≠ prior S2 CREDIT_SPREAD_PROXY / RATE_CURVE_SHAPE / EM_DM_FLOW_ROTATION
- ≠ N75–N77 / N81–N86 DIAG paths

---

## 3. Bevroren regel (geen retune)

**Signal (dag t, na US equity close ≈22:00 CET):**
1. Data: Yahoo/proxy dagcloses van XLB, XLE, XLF, XLI, XLK, XLP, XLU, XLV, XLY (zelfde set als S2 cycle_2046).
2. `ret10_i = close_t / close_{t−10} − 1` per sector.
3. `disp = stdev_cross_section(ret10_i)` (9 sectoren).
4. `disp_z = (disp − mean_252(disp)) / stdev_252(disp)` (rolling 252 handelsdagen; min periods zoals S2 script).
5. Signal:
   - `disp_z > +1,0` → **SHORT**
   - `disp_z < −0,5` → **LONG**
   - else → skip (flat)

**Execution (dag t+1, FTMO M5 `US100cash`):**
6. Entry: close van eerste M5-bar ≥ **15:30 CET** (span ≤15 min). Ontbreekt → skip day.
7. Exit: close van laatste M5-bar ≤ **21:00 CET** same day. **Geen overnight. Geen swap.**
8. PnL: `pnl_bp = position × (P_exit / P_entry − 1) × 1e4`.
9. Non-overlapping (≤1 trade/dag). Geen stop in freeze (U2 mag formal ATR-stop enkel rapporteren als info — **niet** drempel-retune).
10. **Verboden:** threshold-grid op 2025+; SPY/US500 primary; overnight hold; swap-credit als alfa; vov/VIX-add-on; ORB-range rewrite.

---

## 4. Splits / success (U2)

| Venster | Rol |
|---------|-----|
| Train **2021-01-01 … 2023-12-31** | D-092.1 cost-gate + stress + formal day-clust t |
| Test **2024-01-01 … 2024-12-31** | formal (info + pass/fail per standaard U2) |
| Reserve **2025+** | **onaangeroerd** (D-084 / D-094.1; alleen CEO-vrijgave) |

**Success:**
- mean bruto train ≥ **1,98 bp**, N_train ≥ 150
- stress mean ≥ **2,97 bp** (of U2 standaard 1,5×RT stress)
- dag-geclusterd netto t ≥ 2,0 train **én** test; netto mean > 0 in elk
- daarna `engine/ftmo.py` + intradag-DD (D-101 lat-B) + Auditor

**FAIL → STOP:** 1 trial (als cost-gate PASS), **geen klonen** (geen thr-grid, geen overnight rewrite, geen US500-first, geen softer gate). Dead label `N93_SECTOR_DISP_ROTATION`.

---

## 5. D-094a

Lane-A proxy span **~2005–2024 (~19,6y)** op Yahoo XL*/NDX ≥10j ✔. Reden **(b)**: cross-sectionele sector-dispersie / breadth-regime als timing-signaal voor index (Moskowitz–Grinblatt industrie-lead-lag literatuurlijn; dispersie als disagreement/risk-scramble proxy) + FTMO-M5 voor kosten. Herhaal in U2-runlog. Train-poort blijft 2021–2023 M5.

---

## 6. Bestanden / catalogus-ID

- **PREREG:** `PREREG_FTMO_N93_SECTOR_DISP_ROTATION.md` (**N93** — **OPEN**)
- **Source pointer:** `results/lane_b/SECTOR_DISP_ROTATION_SOURCE.md`
- **Lane-A:** `git show fde4a15:results/strateeg2_prescreen/cycle_2046/…`
- **Catalogus-ID:** **N93** / NEW_FAMILY **R**
- **Branch:** `claude/trusting-faraday-34tsmg`
- **TRIAL_COUNT (book):** **458**
