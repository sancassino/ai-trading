# PREREG_FTMO_N114 — HYG_CREDIT_STRESS (US500cash; session-flat; NEW_FAMILY AI)

**Status:** **STOP FAIL_T** — U2 tip `527e46e` on `claude/uitvoerder2-r` (TRIAL **461→462**).  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**VOORSTEL:** `VOORSTEL_PRESCREEN_N114.md`.  
**Signal:** Yahoo/proxy **HYG** (US high-yield corporate bond ETF). **Trade:** `US500cash`.  
**NEW_FAMILY AI:** **DEAD** (no HYG→US500 / LQD twin / EMB rewrite / overnight / soft-gate clones; HYG≠EMB).  
**Hold:** session-flat 15:30→21:00 CET (was freeze).  
**TRIAL_COUNT book:** **462** after this trial.  
**Reserve 2025+:** **onaangeroerd.**  
**Dead += N114.** No retune.

Board: U2 `results/R2/n114_hyg_credit_stress/n114_gate_board.json`. Faraday tip at PREREG freeze: `f9f7bae`.

---

## U2 result (authoritative)

| Post | Waarde |
|------|--------|
| Verdict | **FAIL_T** (cost+stress **PASS**) |
| Train 2021–23 | N=**371**, mean bruto **+3,81** ≥2,34/3,51; t/NW **0,68/0,71** <2 |
| Years | 2021 **−10,03** / 2022 **+7,69** / 2023 **+4,82** |
| Test 2024 | N=**150**, bruto **−2,16** |
| Trial | **461→462**; counts_as_trial=true |
| Retune | **verboden** (geen thr-grid, geen LQD twin, geen EMB rewrite, geen overnight, geen soft gate) |

Live PREREG-pointer **cleared**.

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze (was)

| Post | Waarde | Bron |
|------|--------:|------|
| Signal | Yahoo/proxy **HYG** dagclose | `data/daily/HYG.csv` |
| Trade | `US500cash` | FTMO |
| Round-trip intradag (RT) | **0,78 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (EOD flat same CET day) | D-100 session-flat |
| Hold | entry first M5 **[15:30, 15:45] CET** → flat **21:00 CET** | was freeze |
| **Gate (binding)** | **3 × 0,78 = 2,34 bp** | pure intradag |
| Stress (informeel) | **1,5 × 2,34 = 3,51 bp** | vóór formal t |

---

## 2. Economisch mechanisme (NEW_FAMILY AI — DEAD)

`NEW_FAMILY: AI` — HYG close as **US domestic HY credit risk-appetite** proxy into DM equity beta (≠ EMB EM hard-currency). Combo z120±0,5 + d20 sign → US500 session-flat. **DEAD** after FAIL_T; no HYG/LQD/EMB clones.

---

## 3. Bestanden / catalogus-ID

- **PREREG:** `PREREG_FTMO_N114_HYG_CREDIT_STRESS.md` (**N114** — **STOP FAIL_T**)
- **VOORSTEL:** `VOORSTEL_PRESCREEN_N114.md`
- **Screen:** `results/R2/n114_n115_prescreen/` + U2 `results/R2/n114_hyg_credit_stress/`
- **Catalogus-ID:** **N114** / NEW_FAMILY **AI** DEAD
- Branch: `claude/trusting-faraday-34tsmg`
- **TRIAL_COUNT (book):** **462**
