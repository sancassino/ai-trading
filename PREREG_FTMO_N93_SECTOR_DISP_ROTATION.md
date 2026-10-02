# PREREG_FTMO_N93 — SECTOR_DISP_ROTATION (US100cash; session-flat; Lane-B from S2)

**Status:** **STOP FAIL_COST_GATE** — U2 `b382307` on `claude/uitvoerder2-r` (2026-10-02).  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**Bron Lane-A:** Strateeg-2 (`grok/strateeg-2`) @ **`fde4a15`** — `results/strateeg2_prescreen/cycle_2046/VOORSTEL_S2_SECTOR_DISP_ROTATION.md`.  
**Instrument (primary):** `US100cash` (NDX proxy).  
**NEW_FAMILY R:** `SECTOR_DISP_ROTATION` — **DEAD** (no SECTOR_DISP / XL*→US100 dispersion clones; no retune).  
**Config freeze:** lb=10 / disp_fade / thr +1,0 / −0,5; session-flat 15:30→21:00 CET.  
**TRIAL_COUNT book:** **458** (geen trial — cost-gate FAIL; geen TRIALS-append).  
**Reserve 2025+:** **onaangeroerd.**

Pointer: `results/lane_b/SECTOR_DISP_ROTATION_SOURCE.md` → S2 artefacts @ `fde4a15` (geen CSV-rewrite).

---

## U2 result (authoritative)

| Post | Waarde |
|------|--------|
| Verdict | **FAIL_COST_GATE** STOP |
| Train 2021–23 | N=**309**, mean bruto **+0,99 bp < gate 1,98** (stress **2,97 FAIL**) |
| Years train | 2021 **+2,03** / 2022 **−5,24** / 2023 **+6,28** |
| Test 2024 | **−10,99 bp** |
| Trial id | **geen** — TRIAL_COUNT blijft **458**; geen TRIALS-append |
| Dead label | `N93_SECTOR_DISP_ROTATION` |
| Lane-A note | Yahoo proxy mean **6,02** ≠ FTMO session-flat PASS |
| Retune | **verboden** (geen thr-grid, geen overnight rewrite, geen US500-first) |

Live PREREG-pointer **cleared**. Parent: **geen** U2 wake (FAIL, not PASS→PREREG). Quiet.

---

## 1. Instrument & kosten (was freeze; nu historisch)

| Post | Waarde |
|------|--------:|
| Symbool | `US100cash` |
| RT intradag | **0,66 bp** |
| Gate | **1,98 bp** (3×RT); stress 2,97 |
| Hold | session-flat 15:30→21:00 CET |

## 2–6. Regel / splits / D-094a / bestanden

Zie git history pre-STOP (`f217478`) voor bevroren regeltekst. Catalogus-ID **N93** / NEW_FAMILY **R** = **DEAD**. Branch `claude/trusting-faraday-34tsmg`. TRIAL_COUNT **458**.
