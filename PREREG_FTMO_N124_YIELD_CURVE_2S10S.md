# PREREG_FTMO_N124 — YIELD_CURVE_2S10S (US500cash; session-flat; Lane-B from S2)

**Status:** **STOP FAIL_T** — U2 tip `9f00f24` on `claude/uitvoerder2-r` (TRIAL **464→465**).  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**Bron Lane-A:** Strateeg-2 (`grok/strateeg-2`) @ **`13fe10c`** — cycle_2346.  
**VOORSTEL:** `VOORSTEL_PRESCREEN_N124.md`.  
**Signal:** US Treasury **10Y−3M** slope. **Trade:** `US500cash`.  
**NEW_FAMILY AS:** **DEAD** (no thr-grid / US100 overnight rewrite / TLT-TIP-SECTOR_DISP clones / yield-curve twins).  
**Hold:** session-flat 15:30→21:00 CET (was freeze).  
**TRIAL_COUNT book:** **465** after this trial (then N125 → **466**).  
**Reserve 2025+:** **onaangeroerd.**  
**Dead += N124.** No retune.

Board: U2 `results/R2/n124_yield_curve_2s10s/` (tip `9f00f24`). Faraday tip at PREREG freeze: `b236459` (absorb S2 cycle_2346).

---

## U2 result (authoritative)

| Post | Waarde |
|------|--------|
| Verdict | **FAIL_T** (cost+stress **PASS**) |
| Train 2021–23 | N=**240**, mean bruto **+8,97** ≥2,34/3,51; t_netto / t_NW5 **1,72 / 1,82** <2 |
| Test 2024 | N=**100**, bruto **+2,89** |
| Trial | **464→465**; counts_as_trial=true |
| Retune | **verboden** (geen thr-grid, geen US100 overnight rewrite, geen TLT/TIP/SECTOR_DISP clones, geen yield-curve twin) |

Live PREREG-pointer **cleared** (with N125).

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze (was)

| Post | Waarde | Bron |
|------|--------:|------|
| Signal | US Treasury **10Y−3M** slope (`YLD_US10Y` − `YLD_US3M`) | S2 cycle_2346 / `data/daily/` |
| Trade | `US500cash` | FTMO |
| Round-trip intradag (RT) | **0,78 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (EOD flat same CET day) | D-100 session-flat |
| Hold | entry first M5 **[15:30, 15:45] CET** → flat **21:00 CET** | was freeze |
| **Gate (binding)** | **3 × 0,78 = 2,34 bp** | pure intradag |
| Stress (informeel) | **1,5 × 2,34 = 3,51 bp** | vóór formal t |

Pre-screen (historical): `results/R2/n124_n125_prescreen/` — N124 PASS train N=240 mean +8,97 ≥2,34.

Pointer: `results/lane_b/YIELD_CURVE_2S10S_SOURCE.md` → S2 @ `13fe10c`.
