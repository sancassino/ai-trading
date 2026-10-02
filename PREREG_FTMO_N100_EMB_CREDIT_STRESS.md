# PREREG_FTMO_N100 — EMB_CREDIT_STRESS (US100cash; session-flat; Lane-B from S2)

**Status:** **OPEN** — frozen for U2 cost-gate + formal trial (Lane-B from S2 Lane-A survivor cycle_2140).  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**Bron Lane-A:** Strateeg-2 (`grok/strateeg-2`) @ **`67a9be1`** — `results/strateeg2_prescreen/cycle_2140/VOORSTEL_S2_EMB_CREDIT_STRESS.md`.  
**Instrument (primary):** `US100cash` (NDX proxy).  
**NEW_FAMILY:** `EMB_CREDIT_STRESS` — EMB (EM USD hard-currency bond ETF) level+trend → US100 session-flat.  
**Config freeze:** **z120 / combo / signal-as Lane-A hold=3d non-overlap** — **execution = session-flat** (D-100). **Geen retune.**  
**Hold:** **session-flat** 15:30→21:00 CET (D-100 verplicht — US100 long overnight swap ≈1,95 bp/nacht).  
**TRIAL_COUNT book:** **458** (deze PREREG telt nog niet).  
**Reserve 2025+:** **onaangeroerd.**

Pointer: `results/lane_b/EMB_CREDIT_STRESS_SOURCE.md` → S2 artefacts @ `67a9be1` (geen CSV-rewrite).

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze

| Post | Waarde | Bron |
|------|--------:|------|
| Symbool | `US100cash` | FTMO |
| Round-trip intradag (RT) | **0,66 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (EOD flat same CET day — **vóór** overnight swap-window) | D-100 session-flat |
| Hold | cash-session only: entry ≈**15:30 CET** → flat ≈**21:00 CET** | bevroren regel |
| **Gate (binding)** | **3 × 0,66 = 1,98 bp** | pure intradag; geen D-097 50-floor |
| Stress (informeel) | **1,5 × 1,98 = 2,97 bp** | vóór formal t |

**Lane-A context (niet de formele poort):** Yahoo/proxy EMB→NDX z120/combo hold=3d non-overlap ≤2024: mean bruto **21,42 bp**, day_t **3,00**, n=998, yrs=16,86; POST-N78 drag (RT+3×swap worse) → net **+14,90 bp COST_OK**. S2 **FLAG:** US100 long overnight swap duur → Lane-B **moet** session-flat (of goedkoopste overnight-kant). Deze PREREG kiest **session-flat** — swap zit **niet** in de edge; alfa = signed mean **bruto prijs**. Lane-A hold=3d overnight is **mapped** to one cash-session trade per signal (D-100); U2 toetst FTMO session-flat, niet overnight multi-day.

---

## 2. Economisch mechanisme (NEW_FAMILY EMB_CREDIT_STRESS)

`NEW_FAMILY: EMB_CREDIT_STRESS` — EMB close als **EM hard-currency credit / risk-appetite** proxy:

1. `z120` = 120d z-score van EMB close; `d20` = 20d return.
2. **combo:** long NDX/US100 when (z>0,5 **and** d20>0); short when (z<−0,5 **and** d20<0); else skip.
3. Maps to cheap FTMO index CFD (US100), **not** EMB itself.

Dit is een **EM-credit stress / risk-on** sleeve — **geen** HYG/LQD domestic credit, **geen** EEM/EFA equity XS, **geen** FX LO carry, **geen** SECTOR_DISP / VIX_TERM / ORB / TSMOM / L60.

**Distinct / dead-set guard:**
- ≠ **CREDIT_SPREAD_PROXY** (HYG/LQD domestic US credit)
- ≠ **EM_DM_FLOW_ROTATION** (EEM/EFA equity XS)
- ≠ **N93 SECTOR_DISP** FAIL_COST_GATE / no XL*→US100 clones
- ≠ **N78 VIX_TERM_VOV** FAIL_COST_GATE / C-029 barred
- ≠ **N92** NY-2h mom FAIL_T / **N98** USOIL→US100 DIAG_FAIL / **N99** CADCHF DIAG_FAIL
- ≠ FX LO carry clones (NZDJPY / CADCHF / CADJPY / AUDCAD) / L60 / ORB-meta / UKOIL-OVN / CORN / N75–N99 restarts

---

## 3. Bevroren regel (geen retune)

**Signal (dag t, na US equity close ≈22:00 CET):**
1. Data: Yahoo/proxy dagclose **EMB** (zelfde series als S2 cycle_2140).
2. `z120 = (EMB_t − mean_120(EMB)) / stdev_120(EMB)`; `d20 = EMB_t / EMB_{t−20} − 1`.
3. Signal:
   - `(z120 > +0,5) and (d20 > 0)` → **LONG**
   - `(z120 < −0,5) and (d20 < 0)` → **SHORT**
   - else → skip (flat)

**Execution (dag t+1, FTMO M5 `US100cash`) — D-100 session-flat:**
4. Entry: close van eerste M5-bar ≥ **15:30 CET** (span ≤15 min). Ontbreekt → skip day.
5. Exit: close van laatste M5-bar ≤ **21:00 CET** same day. **Geen overnight. Geen swap.**
6. PnL: `pnl_bp = position × (P_exit / P_entry − 1) × 1e4`.
7. Non-overlapping (≤1 trade/dag). Geen stop in freeze (U2 mag formal ATR-stop enkel rapporteren als info — **niet** drempel-retune).
8. **Verboden:** threshold-grid op 2025+; overnight hold / swap-credit als alfa; HYG/LQD rewrite; EEM twin; US500-first; soft gate; SECTOR_DISP/VIX add-on.

---

## 4. Splits / success (U2)

| Venster | Rol |
|---------|-----|
| Train **2021-01-01 … 2023-12-31** | D-092.1 cost-gate + stress + formal day-clust t |
| Test **2024-01-01 … 2024-12-31** | formal (info + pass/fail per standaard U2) |
| Reserve **2025+** | **onaangeroerd** (D-084 / D-094.1; alleen CEO-vrijgave) |

**Success:**
- mean bruto train ≥ **1,98 bp**, N_train ≥ 150
- stress mean ≥ **2,97 bp** (of U2 standaard 1,5× gate stress)
- dag-geclusterd netto t ≥ 2,0 train **én** test; netto mean > 0 in elk
- daarna `engine/ftmo.py` + intradag-DD (D-101 lat-B) + Auditor

**FAIL → STOP:** 1 trial (als cost-gate PASS), **geen klonen** (geen thr-grid, geen overnight rewrite, geen EMB→US500 primary, geen softer gate). Dead label `N100_EMB_CREDIT_STRESS`.

---

## 5. D-094a

Lane-A proxy span **~2008–2024 (~16,9y)** op EMB/NDX ≥5j ✔. Reden **(b)**: EM hard-currency credit stress / risk-appetite (EMB) as timing signal for DM equity beta — distinct from domestic HYG/LQD credit and from equity EM/DM flow; FTMO-M5 for costs. Herhaal in U2-runlog. Train-poort blijft 2021–2023 M5.

---

## 6. Bestanden / catalogus-ID

- **PREREG:** `PREREG_FTMO_N100_EMB_CREDIT_STRESS.md` (**N100** — **OPEN**)
- **Source pointer:** `results/lane_b/EMB_CREDIT_STRESS_SOURCE.md`
- **Lane-A:** `git show 67a9be1:results/strateeg2_prescreen/cycle_2140/…`
- **Catalogus-ID:** **N100** / NEW_FAMILY **EMB_CREDIT_STRESS**
- **Branch:** `claude/trusting-faraday-34tsmg`
- **TRIAL_COUNT (book):** **458**
