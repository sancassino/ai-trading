# PREREG_FTMO_N113 — SILVER_GOLD_RATIO (US500cash; session-flat; Lane-B from S2)

**Status:** **OPEN** — frozen for U2 cost-gate + formal trial (Lane-B from S2 Lane-A survivor cycle_2240).  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**Bron Lane-A:** Strateeg-2 (`grok/strateeg-2`) @ **`35e38ac`** — `results/strateeg2_prescreen/cycle_2240/VOORSTEL_S2_SILVER_GOLD_RATIO.md`.  
**Instrument (primary):** `US500cash` (SPY proxy). **Geen** silver/XAG CFD trade leg (signal-only metals ratio).  
**NEW_FAMILY:** `SILVER_GOLD_RATIO` — SLV/GLD (silver vs gold ETF ratio) extreme fade → US500 session-flat.  
**Config freeze:** **z40 / thr1.0 / fade_extreme** — Lane-A hold=5d non-overlap **mapped** to **session-flat** (D-100). **Geen retune.**  
**Hold:** **session-flat** 15:30→21:00 CET (D-100 — US500 overnight swap long 1,36 / short 0,81 bp/nacht; 5-night worse-side drag dominates RT).  
**TRIAL_COUNT book:** **460** (deze PREREG telt nog niet).  
**Reserve 2025+:** **onaangeroerd.**

Pointer: `results/lane_b/SILVER_GOLD_RATIO_SOURCE.md` → S2 artefacts @ `35e38ac` (geen CSV-rewrite).

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze

| Post | Waarde | Bron |
|------|--------:|------|
| Signal | Yahoo/proxy **SLV** / **GLD** (dagclose ratio) | S2 cycle_2240 |
| Trade | `US500cash` | FTMO |
| Round-trip intradag (RT) | **0,78 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (EOD flat same CET day — **vóór** overnight swap-window) | D-100 session-flat |
| Hold | cash-session only: entry ≈**15:30 CET** → flat ≈**21:00 CET** | bevroren regel |
| **Gate (binding)** | **3 × 0,78 = 2,34 bp** | pure intradag; geen D-097 50-floor |
| Stress (informeel) | **1,5 × 2,34 = 3,51 bp** | vóór formal t |

**Lane-A context (niet de formele poort):** Yahoo/proxy SLV/GLD→SPY z40/thr1.0/fade_extreme hold=5d non-overlap ≤2024: mean bruto **22,41 bp**, day_t **2,10**, n=635, yrs=18,58; POST-N78 drag (RT+5×swap worse) → net **+14,84 bp COST_OK**. S2 **FLAG:** US500 preferred; **silver CFD not used** (signal-only). Overnight US500 5-nacht swap duur → Lane-B **session-flat** (D-100). Alfa = signed mean **bruto prijs**; **geen swap-credits**. Lane-A hold=5d overnight is **mapped** to one cash-session trade per signal.

---

## 2. Economisch mechanisme (NEW_FAMILY SILVER_GOLD_RATIO)

`NEW_FAMILY: SILVER_GOLD_RATIO` — SLV/GLD ratio als **industrial-vs-monetary metal risk-appetite** mean-reversion:

1. `ratio = SLV / GLD`; `z40` = 40d z-score of ratio.
2. **fade_extreme:** short US500 when z>+1,0 (Ag rich vs Au = crowded risk-on → fade); long US500 when z<−1,0 (Ag cheap vs Au = risk-off extreme → bounce); else skip.
3. Maps to **US500cash** (not silver CFD; not XAU for this best config).

Dit is een **Ag/Au ratio fade → equity** sleeve — **geen** copper/gold, **geen** PGM, **geen** XAU Lon→NY / XAG AM-Fix, **geen** N75 XAU/XAG MR trade legs.

**Distinct / dead-set guard:**
- ≠ **COPPER_GOLD_MACRO** / **PGM_RATIO_CYCLE** (prior Lane-A FAIL)
- ≠ **N75 XAU/XAG ratio MR** DIAG_FAIL (trades gold/silver CFD legs — this = **ratio→equity signal-only**)
- ≠ **N95 XAU Lon→NY** FAIL / **N82 XAG AM-Fix** DIAG_FAIL / **N86 XAU VoV** DIAG_FAIL
- ≠ **N112 GAS_EQUITY_MACRO** (gas stress ≠ metals ratio)
- ≠ **N93 SECTOR_DISP** / **N78 VIX** / **N100 EMB** / **N101 CRACK** / ORB / L60 / N75–N111 restarts

---

## 3. Bevroren regel (geen retune)

**Signal (dag t, na US ETF close ≈22:00 CET):**
1. Data: Yahoo/proxy dagcloses **SLV** + **GLD** (zelfde set als S2 cycle_2240).
2. `ratio_t = SLV_t / GLD_t`.
3. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)`.
4. Signal:
   - `z40 > +1,0` → **SHORT**
   - `z40 < −1,0` → **LONG**
   - else → skip (flat)

**Execution (dag t+1, FTMO M5 `US500cash`) — D-100 session-flat:**
5. Entry: close van eerste M5-bar ≥ **15:30 CET** (span ≤15 min). Ontbreekt → skip day.
6. Exit: close van laatste M5-bar ≤ **21:00 CET** same day. **Geen overnight. Geen swap. Geen silver/XAG CFD leg.**
7. PnL: `pnl_bp = position × (P_exit / P_entry − 1) × 1e4`.
8. Non-overlapping (≤1 trade/dag). Geen stop in freeze (U2 ATR-stop = info only — **niet** drempel-retune).
9. **Verboden:** thr-grid op 2025+; overnight hold; XAG/XAU trade leg; N75 ratio-MR rewrite; soft gate; swap-credit als alfa.

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

**FAIL → STOP:** 1 trial (als cost-gate PASS), **geen klonen** (geen thr-grid, geen XAG-CFD twin, geen overnight rewrite, geen softer gate). Dead label `N113_SILVER_GOLD_RATIO`.

---

## 5. D-094a

Lane-A proxy span **~2006–2024 (~18,6y)** op SLV/GLD/SPY ≥5j ✔. Reden **(b)**: silver/gold industrial-vs-monetary ratio extremes as risk-appetite mean-reversion into equity beta — distinct from copper/gold and from trading the metals CFDs themselves; FTMO-M5 for costs. Herhaal in U2-runlog. Train-poort blijft 2021–2023 M5.

---

## 6. Bestanden / catalogus-ID

- **PREREG:** `PREREG_FTMO_N113_SILVER_GOLD_RATIO.md` (**N113** — **OPEN**)
- **Source pointer:** `results/lane_b/SILVER_GOLD_RATIO_SOURCE.md`
- **Lane-A:** `git show 35e38ac:results/strateeg2_prescreen/cycle_2240/…`
- **Catalogus-ID:** **N113** / NEW_FAMILY **SILVER_GOLD_RATIO**
- **Branch:** `claude/trusting-faraday-34tsmg`
- **TRIAL_COUNT (book):** **460**
