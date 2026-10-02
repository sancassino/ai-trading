# PREREG_FTMO_N101 — CRACK_SPREAD_MACRO (US100cash; session-flat; Lane-B from S2)

**Status:** **STOP FAIL_T** — U2 tip `d09d00a` on `claude/uitvoerder2-r` (TRIAL **459→460**).  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**Bron Lane-A:** Strateeg-2 (`grok/strateeg-2`) @ **`67a9be1`** — cycle_2140.  
**Instrument (primary):** `US100cash` (NDX proxy). **Geen** UKOIL/USOIL trade leg.  
**NEW_FAMILY:** `CRACK_SPREAD_MACRO` — **DEAD** (no HO/BRENT crack→NDX / oil CFD clones; no retune).  
**Hold:** session-flat 15:30→21:00 CET (was freeze).  
**TRIAL_COUNT book:** **460**.  
**Reserve 2025+:** **onaangeroerd.**  
**Dead += N101.** No crack-spread / oil-CFD-leg clones.

Pointer: `results/lane_b/CRACK_SPREAD_MACRO_SOURCE.md` → S2 @ `67a9be1`. Board: U2 `results/R2/n101_crack_spread_macro/n101_gate_board.json`.

---

## U2 result (authoritative)

| Post | Waarde |
|------|--------|
| Verdict | **FAIL_T** (cost+stress **PASS**) |
| Train 2021–23 | N=**436**, mean bruto **+6,30** ≥1,98/2,97; t/NW **1,05/1,21** <2 |
| Test 2024 | N=**184**, bruto **−5,00** |
| Trial | **459→460**; counts_as_trial=true |
| Retune | **verboden** (geen oil CFD clones) |

Live PREREG-pointer **cleared**.

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

**Lane-A context (niet de formele poort):** Yahoo/proxy HO/BRENT→NDX z60/thr0.5/crack_fade hold=5d non-overlap ≤2024: mean bruto **23,09 bp**, day_t **2,26**, n=773, yrs=17,33; POST-N78 drag (RT+5×swap worse) → net **+12,68 bp COST_OK**. S2 **FLAG:** 5-night US100 worse-side swap dominates RT → Lane-B **moet** session-flat / cheap overnight side. Deze PREREG kiest **session-flat**. Lane-A hold=5d overnight is **mapped** to one cash-session trade per signal (D-100); trade **equity index CFD only** — never UKOIL/USOIL (POST-N78 / ENERGY lesson).

---

## 2. Economisch mechanisme (NEW_FAMILY CRACK_SPREAD_MACRO)

`NEW_FAMILY: CRACK_SPREAD_MACRO` — refining **crack** (product vs crude) as demand/margins macro signal:

1. Crack = HEATOIL_F / BRENT_F.
2. `z60` = 60d z-score of crack; threshold ±0,5.
3. **crack_fade:** crack rich (z>0,5) → **short** NDX/US100; crack cheap (z<−0,5) → **long** NDX/US100 (fade extreme refining margins / demand extremes).
4. Else skip.

Dit is een **daily crack-level fade → equity**, **geen** oil CFD overnight sleeve, **geen** Lon-AM oil→US100 same-dir lead-lag (N98 DIAG_FAIL), **geen** ENERGY_TSMOM / UKOIL-OVN.

**Distinct / dead-set guard:**
- ≠ **ENERGY_TSMOM / UKOIL-OVN / N80** (oil CFD overnight / OVN-gap)
- ≠ **N98 USOIL→US100** DIAG_FAIL (session lead Lon-AM→NY risk-on — this = **daily crack level fade**)
- ≠ **N93 SECTOR_DISP** / **N78 VIX_TERM** / ORB / L60 / CORN / classic TSMOM
- ≠ **N92** NY-2h mom / **N99** CADCHF / FX LO carry clones / N75–N99 restarts

---

## 3. Bevroren regel (geen retune)

**Signal (dag t, na futures/proxy close):**
1. Data: Yahoo/proxy dagcloses **HEATOIL_F** + **BRENT_F** (zelfde set als S2 cycle_2140).
2. `crack_t = HEATOIL_F_t / BRENT_F_t`.
3. `z60 = (crack_t − mean_60(crack)) / stdev_60(crack)`.
4. Signal:
   - `z60 > +0,5` → **SHORT**
   - `z60 < −0,5` → **LONG**
   - else → skip (flat)

**Execution (dag t+1, FTMO M5 `US100cash`) — D-100 session-flat:**
5. Entry: close van eerste M5-bar ≥ **15:30 CET** (span ≤15 min). Ontbreekt → skip day.
6. Exit: close van laatste M5-bar ≤ **21:00 CET** same day. **Geen overnight. Geen swap. Geen oil CFD leg.**
7. PnL: `pnl_bp = position × (P_exit / P_entry − 1) × 1e4`.
8. Non-overlapping (≤1 trade/dag). Geen stop in freeze (U2 ATR-stop = info only — **niet** drempel-retune).
9. **Verboden:** thr-grid op 2025+; overnight hold; UKOIL/USOIL trade leg; USOIL→US100 lead-lag rewrite (N98 clone); soft gate; swap-credit als alfa.

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

**FAIL → STOP:** 1 trial (als cost-gate PASS), **geen klonen** (geen thr-grid, geen oil-CFD twin, geen overnight rewrite, geen softer gate). Dead label `N101_CRACK_SPREAD_MACRO`.

---

## 5. D-094a

Lane-A proxy span **~2007–2024 (~17,3y)** op HO/BRENT/NDX ≥5j ✔. Reden **(b)**: refining crack (product/crude) as macro demand/margins signal that mean-reverts into equity risk appetite — literature on crack spreads / energy margins; FTMO-M5 for costs. Herhaal in U2-runlog. Train-poort blijft 2021–2023 M5.

---

## 6. Bestanden / catalogus-ID

- **PREREG:** `PREREG_FTMO_N101_CRACK_SPREAD_MACRO.md` (**N101** — **OPEN**)
- **Source pointer:** `results/lane_b/CRACK_SPREAD_MACRO_SOURCE.md`
- **Lane-A:** `git show 67a9be1:results/strateeg2_prescreen/cycle_2140/…`
- **Catalogus-ID:** **N101** / NEW_FAMILY **CRACK_SPREAD_MACRO**
- **Branch:** `claude/trusting-faraday-34tsmg`
- **TRIAL_COUNT (book):** **458**
