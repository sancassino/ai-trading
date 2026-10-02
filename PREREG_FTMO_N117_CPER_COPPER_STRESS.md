# PREREG_FTMO_N117 — CPER_COPPER_STRESS (US500cash; session-flat; NEW_FAMILY AL)

**Status:** **STOP FAIL_STRESS** — U2 tip `d8b97d0` on `claude/uitvoerder2-r`. Cost PASS (train N=152 mean **+2,89** ≥ 2,34); stress FAIL (**+2,89 < 3,51**); years 2021 +0,52 / 2022 +11,84 / 2023 −5,56; median **−2,21**. **geen trial**; TRIAL_COUNT **463**. Dead += N117. No retune / no copper CFD / no CuAu rewrite / no overnight.  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**VOORSTEL:** `VOORSTEL_PRESCREEN_N117.md`.  
**Signal:** Yahoo/proxy **CPER** (copper ETF). **Trade:** `US500cash`.  
**NEW_FAMILY AL:** **DEAD** (no CPER→US500 / CuAu rewrite / copper CFD / overnight / soft-gate clones).  
**Hold:** session-flat 15:30→21:00 CET (was freeze).  
**TRIAL_COUNT book:** **463** (unchanged; FAIL_STRESS ≠ trial).  
**Reserve 2025+:** **onaangeroerd.**  
**Dead += N117.** No retune.

Board: U2 `results/R2/n117_cper_copper_stress/`. Faraday tip at PREREG freeze: `754e24e`.

---

## U2 result (authoritative)

| Post | Waarde |
|------|--------|
| Verdict | **FAIL_STRESS** (cost **PASS**) |
| Train 2021–23 | N=**152**, mean bruto **+2,89** ≥2,34 but **< stress 3,51** |
| Median | **−2,21** |
| Years | 2021 **+0,52** / 2022 **+11,84** / 2023 **−5,56** |
| Trial | **blijft 463**; counts_as_trial=false (FAIL_STRESS vóór formal t) |
| Retune | **verboden** (geen thr-grid, geen copper CFD, geen CuAu rewrite, geen overnight, geen soft gate) |

Live PREREG-pointer **cleared**.

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze (was)

| Post | Waarde | Bron |
|------|--------:|------|
| Signal | Yahoo/proxy **CPER** dagclose | `data/daily/CPER.csv` |
| Trade | `US500cash` | FTMO |
| Round-trip intradag (RT) | **0,78 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (EOD flat same CET day) | D-100 session-flat |
| Hold | entry first M5 **[15:30, 15:45] CET** → flat **21:00 CET** | was freeze |
| **Gate (binding)** | **3 × 0,78 = 2,34 bp** | pure intradag |
| Stress (informeel) | **1,5 × 2,34 = 3,51 bp** | vóór formal t |

---

## 2. Economisch mechanisme (NEW_FAMILY AL — DEAD)

`NEW_FAMILY: AL` — CPER close as copper **level** / industrial growth proxy into DM equity beta. Stress_buy z40±1,5 → US500 session-flat. **DEAD** after FAIL_STRESS; no CPER/CuAu/copper-CFD clones.

---

## 3. Bestanden / catalogus-ID

- **PREREG:** `PREREG_FTMO_N117_CPER_COPPER_STRESS.md` (**N117** — **STOP FAIL_STRESS**)
- **VOORSTEL:** `VOORSTEL_PRESCREEN_N117.md`
- **Screen:** `results/R2/n116_n117_prescreen/` + U2 `results/R2/n117_cper_copper_stress/`
- **Catalogus-ID:** **N117** / NEW_FAMILY **AL** DEAD
- Branch: `claude/trusting-faraday-34tsmg`
- **TRIAL_COUNT (book):** **463**
