# PREREG_FTMO_N112 — GAS_EQUITY_MACRO (US500cash; session-flat; Lane-B from S2)

**Status:** **OPEN** — frozen for U2 cost-gate + formal trial (Lane-B from S2 Lane-A survivor cycle_2240).  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**Bron Lane-A:** Strateeg-2 (`grok/strateeg-2`) @ **`35e38ac`** — `results/strateeg2_prescreen/cycle_2240/VOORSTEL_S2_GAS_EQUITY_MACRO.md`.  
**Instrument (primary):** `US500cash` (SPY proxy). **Geen** gas/NATGAS CFD trade leg (signal-only).  
**NEW_FAMILY:** `GAS_EQUITY_MACRO` — UNG (US natural-gas ETF) z-stress → US500 session-flat.  
**Config freeze:** **z40 / thr1.5 / stress_buy** — Lane-A hold=5d non-overlap **mapped** to **session-flat** (D-100). **Geen retune.**  
**Hold:** **session-flat** 15:30→21:00 CET (D-100 — US500 overnight swap long 1,36 / short 0,81 bp/nacht; 5-night drag dominates RT).  
**TRIAL_COUNT book:** **460** (deze PREREG telt nog niet).  
**Reserve 2025+:** **onaangeroerd.**

Pointer: `results/lane_b/GAS_EQUITY_MACRO_SOURCE.md` → S2 artefacts @ `35e38ac` (geen CSV-rewrite).

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze

| Post | Waarde | Bron |
|------|--------:|------|
| Signal | Yahoo/proxy **UNG** (dagclose) | S2 cycle_2240 |
| Trade | `US500cash` | FTMO |
| Round-trip intradag (RT) | **0,78 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (EOD flat same CET day — **vóór** overnight swap-window) | D-100 session-flat |
| Hold | cash-session only: entry ≈**15:30 CET** → flat ≈**21:00 CET** | bevroren regel |
| **Gate (binding)** | **3 × 0,78 = 2,34 bp** | pure intradag; geen D-097 50-floor |
| Stress (informeel) | **1,5 × 2,34 = 3,51 bp** | vóór formal t |

**Lane-A context (niet de formele poort):** Yahoo/proxy UNG→SPY z40/thr1.5/stress_buy hold=5d non-overlap ≤2024: mean bruto **47,70 bp**, day_t **3,61**, n=406, yrs=17,61; POST-N78 drag (RT+5×swap short-bias) → net **+42,88 bp COST_OK**. S2 **FLAG:** prefer US500 over US100; **no gas CFD mapping**. Overnight US500 5-nacht swap duur → Lane-B **session-flat** (D-100). Alfa = signed mean **bruto prijs**; **geen swap-credits**. Lane-A hold=5d overnight is **mapped** to one cash-session trade per signal; U2 toetst FTMO session-flat, niet overnight multi-day.

---

## 2. Economisch mechanisme (NEW_FAMILY GAS_EQUITY_MACRO)

`NEW_FAMILY: GAS_EQUITY_MACRO` — UNG close als **energy-shock / growth-drag risk-appetite** proxy:

1. `z40` = 40d z-score van UNG close.
2. **stress_buy:** short US500 when z>+1,5 (gas spike = growth drag / risk-off); long US500 when z<−1,5 (gas crash = relief / risk-on); else skip.
3. Maps to cheap FTMO index CFD (**US500cash**), **not** UNG/NATGAS CFD.

Dit is een **gas-stress → equity** sleeve — **geen** oil CFD / ENERGY_TSMOM / UKOIL-OVN / USOIL→US100 / CRACK refining-spread.

**Distinct / dead-set guard:**
- ≠ **ENERGY_TSMOM / UKOIL-OVN / N80** (oil CFD overnight / OVN-gap)
- ≠ **N101 CRACK_SPREAD_MACRO** FAIL_T (HO/BRENT crack → equity — refining margins ≠ natgas level stress)
- ≠ **N98 USOIL→US100** DIAG_FAIL / **CORN** / agri CFD
- ≠ **N93 SECTOR_DISP** / **N78 VIX_TERM** / **N100 EMB** / ORB / L60 / NY-2h / N75–N111 restarts
- ≠ silver/gold ratio (N113) / HYG domestic credit (N114 OPEN)

---

## 3. Bevroren regel (geen retune)

**Signal (dag t, na US ETF close ≈22:00 CET):**
1. Data: Yahoo/proxy dagclose **UNG** (zelfde series als S2 cycle_2240).
2. `z40 = (UNG_t − mean_40(UNG)) / stdev_40(UNG)`.
3. Signal:
   - `z40 > +1,5` → **SHORT**
   - `z40 < −1,5` → **LONG**
   - else → skip (flat)

**Execution (dag t+1, FTMO M5 `US500cash`) — D-100 session-flat:**
4. Entry: close van eerste M5-bar ≥ **15:30 CET** (span ≤15 min). Ontbreekt → skip day.
5. Exit: close van laatste M5-bar ≤ **21:00 CET** same day. **Geen overnight. Geen swap. Geen gas CFD leg.**
6. PnL: `pnl_bp = position × (P_exit / P_entry − 1) × 1e4`.
7. Non-overlapping (≤1 trade/dag). Geen stop in freeze (U2 ATR-stop = info only — **niet** drempel-retune).
8. **Verboden:** thr-grid op 2025+; overnight hold / swap-credit als alfa; NATGAS/UKOIL/USOIL trade leg; US100-first rewrite; soft gate; CRACK/ENERGY add-on.

---

## 4. Splits / success (U2)

| Venster | Rol |
|---------|-----|
| Train **2021-01-01 … 2023-12-31** | D-092.1 cost-gate + stress + formal day-clust t |
| Test **2024-01-01 … 2024-12-31** | formal (info + pass/fail per standaard U2) |
| Reserve **2025+** | **onaangeroerd** (D-084 / D-094.1; alleen CEO-vrijgave) |

**Success:**
- mean bruto train ≥ **2,34 bp**, N_train ≥ 150
- stress mean ≥ **3,51 bp** (of U2 standaard 1,5× gate stress)
- dag-geclusterd netto t ≥ 2,0 train **én** test; netto mean > 0 in elk
- daarna `engine/ftmo.py` + intradag-DD (D-101 lat-B) + Auditor

**FAIL → STOP:** 1 trial (als cost-gate PASS), **geen klonen** (geen thr-grid, geen gas-CFD twin, geen overnight rewrite, geen softer gate). Dead label `N112_GAS_EQUITY_MACRO`.

---

## 5. D-094a

Lane-A proxy span **~2007–2024 (~17,6y)** op UNG/SPY ≥5j ✔. Reden **(b)**: natural-gas price stress as growth-drag / risk-appetite timing signal for DM equity beta — distinct from oil CFD TSMOM and from refining crack; FTMO-M5 for costs. Herhaal in U2-runlog. Train-poort blijft 2021–2023 M5.

---

## 6. Bestanden / catalogus-ID

- **PREREG:** `PREREG_FTMO_N112_GAS_EQUITY_MACRO.md` (**N112** — **OPEN**)
- **Source pointer:** `results/lane_b/GAS_EQUITY_MACRO_SOURCE.md`
- **Lane-A:** `git show 35e38ac:results/strateeg2_prescreen/cycle_2240/…`
- **Catalogus-ID:** **N112** / NEW_FAMILY **GAS_EQUITY_MACRO**
- **Branch:** `claude/trusting-faraday-34tsmg`
- **TRIAL_COUNT (book):** **460**
