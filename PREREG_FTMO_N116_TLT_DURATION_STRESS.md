# PREREG_FTMO_N116 — TLT_DURATION_STRESS (US500cash; session-flat; NEW_FAMILY AK)

**Status:** **STOP FAIL_T** — U2 tip `d0aa317` on `claude/uitvoerder2-r` (TRIAL **462→463**).  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**VOORSTEL:** `VOORSTEL_PRESCREEN_N116.md`.  
**Signal:** Yahoo/proxy **TLT** (20+y UST ETF). **Trade:** `US500cash`.  
**NEW_FAMILY AK:** **DEAD** (no TLT→US500 / IEF twin / TIP rewrite / overnight / soft-gate clones; TIP≠TLT).  
**Hold:** session-flat 15:30→21:00 CET (was freeze).  
**TRIAL_COUNT book:** **463** after this trial.  
**Reserve 2025+:** **onaangeroerd.**  
**Dead += N116.** No retune.

Board: U2 `results/R2/n116_tlt_duration_stress/` (tip chain → `d8b97d0`). Faraday tip at PREREG freeze: `754e24e`.

---

## U2 result (authoritative)

| Post | Waarde |
|------|--------|
| Verdict | **FAIL_T** (cost+stress **PASS**) |
| Train 2021–23 | N=**386**, mean bruto **+6,01** ≥2,34/3,51; t/NW **1,16/1,17** <2 |
| Years | 2021 **+3,39** / 2022 **+9,62** / 2023 **+1,92** |
| Test 2024 | N=**124**, bruto **+3,46** |
| Trial | **462→463**; counts_as_trial=true |
| Retune | **verboden** (geen thr-grid, geen IEF twin, geen TIP rewrite→N118, geen overnight, geen soft gate) |

Live PREREG-pointer **cleared**.

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze (was)

| Post | Waarde | Bron |
|------|--------:|------|
| Signal | Yahoo/proxy **TLT** dagclose | `data/daily/TLT.csv` |
| Trade | `US500cash` | FTMO |
| Round-trip intradag (RT) | **0,78 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (EOD flat same CET day) | D-100 session-flat |
| Hold | entry first M5 **[15:30, 15:45] CET** → flat **21:00 CET** | was freeze |
| **Gate (binding)** | **3 × 0,78 = 2,34 bp** | pure intradag |
| Stress (informeel) | **1,5 × 2,34 = 3,51 bp** | vóór formal t |

---

## 2. Economisch mechanisme (NEW_FAMILY AK — DEAD)

`NEW_FAMILY: AK` — TLT close as **US long-end rates/duration** risk-appetite proxy into DM equity beta. Combo z120±0,5 + d20 sign → US500 session-flat. **DEAD** after FAIL_T; no TLT/IEF/TIP clones.

---

## 3. Bestanden / catalogus-ID

- **PREREG:** `PREREG_FTMO_N116_TLT_DURATION_STRESS.md` (**N116** — **STOP FAIL_T**)
- **VOORSTEL:** `VOORSTEL_PRESCREEN_N116.md`
- **Screen:** `results/R2/n116_n117_prescreen/` + U2 `results/R2/n116_tlt_duration_stress/`
- **Catalogus-ID:** **N116** / NEW_FAMILY **AK** DEAD
- Branch: `claude/trusting-faraday-34tsmg`
- **TRIAL_COUNT (book):** **463**
