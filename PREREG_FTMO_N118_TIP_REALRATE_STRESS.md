# PREREG_FTMO_N118 — TIP_REALRATE_STRESS (US500cash; session-flat; NEW_FAMILY AM)

**Status:** **STOP FAIL_T** — U2 tip `9e928af` / material `9a00524` on `claude/uitvoerder2-r` (TRIAL **463→464**).  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**VOORSTEL:** `VOORSTEL_PRESCREEN_N118.md`.  
**Signal:** Yahoo/proxy **TIP** (TIPS ETF). **Trade:** `US500cash`.  
**NEW_FAMILY AM:** **DEAD** (no TIP→US500 / IEF twin / TLT rewrite / overnight / soft-gate clones; TIP≠TLT).  
**Hold:** session-flat 15:30→21:00 CET (was freeze).  
**TRIAL_COUNT book:** **464** after this trial.  
**Reserve 2025+:** **onaangeroerd.**  
**Dead += N118.** No retune.

Board: U2 `results/R2/n118_tip_realrate_stress/` (tip `9e928af`). Faraday tip at PREREG freeze: `ce7ce12` / material `42b29e5`.

---

## U2 result (authoritative)

| Post | Waarde |
|------|--------|
| Verdict | **FAIL_T** (cost+stress **PASS**) |
| Train 2021–23 | N=**359**, mean bruto **+5,38** ≥2,34/3,51; t/NW **0,99/0,99** <2 |
| Years | 2021 **−7,40** / 2022 **+7,92** / 2023 **+5,27** |
| Test 2024 | N=**123**, bruto **−4,20** |
| Trial | **463→464**; counts_as_trial=true |
| Retune | **verboden** (geen thr-grid, geen IEF twin, geen TLT rewrite→N116, geen overnight, geen soft gate) |

Live PREREG-pointer **cleared**.

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze (was)

| Post | Waarde | Bron |
|------|--------:|------|
| Signal | Yahoo/proxy **TIP** dagclose | `data/daily/TIP.csv` |
| Trade | `US500cash` | FTMO |
| Round-trip intradag (RT) | **0,78 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (EOD flat same CET day) | D-100 session-flat |
| Hold | entry first M5 **[15:30, 15:45] CET** → flat **21:00 CET** | was freeze |
| **Gate (binding)** | **3 × 0,78 = 2,34 bp** | pure intradag |
| Stress (informeel) | **1,5 × 2,34 = 3,51 bp** | vóór formal t |

---

## 2. Economisch mechanisme (NEW_FAMILY AM — DEAD)

`NEW_FAMILY: AM` — TIP close as **US real-rate / inflation-expectations** risk-appetite proxy into DM equity beta. Combo z120±0,5 + d20 sign → US500 session-flat. **DEAD** after FAIL_T; no TIP/TLT/IEF clones; TIP≠TLT still.

---

## 3. Bestanden / catalogus-ID

- **PREREG:** `PREREG_FTMO_N118_TIP_REALRATE_STRESS.md` (**N118** — **STOP FAIL_T**)
- **VOORSTEL:** `VOORSTEL_PRESCREEN_N118.md`
- **Screen:** `results/R2/n118_n119_prescreen/` + U2 `results/R2/n118_tip_realrate_stress/`
- **Catalogus-ID:** **N118** / NEW_FAMILY **AM** DEAD
- Branch: `claude/trusting-faraday-34tsmg`
- **TRIAL_COUNT (book):** **464**
