# PREREG_FTMO_N125 — DEFENSIVE_CYCLICAL (US500cash twin; session-flat; Lane-B from S2)

**Status:** **STOP FAIL_T** — U2 tip `9f00f24` on `claude/uitvoerder2-r` (TRIAL **465→466**).  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**Bron Lane-A:** Strateeg-2 (`grok/strateeg-2`) @ **`13fe10c`** — cycle_2346.  
**VOORSTEL:** `VOORSTEL_PRESCREEN_N125.md`.  
**Signal:** Yahoo/proxy **XLU/XLI** relative. **Trade:** `US500cash` (US500 twin).  
**NEW_FAMILY AT:** **DEAD** (no thr-grid / US100 overnight rewrite / XLU-XLI defensive twins / SECTOR_DISP clones).  
**Hold:** session-flat 15:30→21:00 CET (was freeze).  
**TRIAL_COUNT book:** **466** after this trial.  
**Reserve 2025+:** **onaangeroerd.**  
**Dead += N125.** No retune.

Board: U2 `results/R2/n125_defensive_cyclical/` (tip `9f00f24`). Faraday tip at PREREG freeze: `b236459`.

---

## U2 result (authoritative)

| Post | Waarde |
|------|--------|
| Verdict | **FAIL_T** (cost+stress **PASS**) |
| Train 2021–23 | N=**478**, mean bruto **+5,48** ≥2,34/3,51; t_netto / t_NW5 **1,22 / 1,29** <2 |
| Test 2024 | N=**191**, bruto **−2,32** |
| Trial | **465→466**; counts_as_trial=true |
| Retune | **verboden** (geen thr-grid, geen US100 overnight rewrite, geen XLU/XLI defensive twin, geen SECTOR_DISP clone) |

Live PREREG-pointer **cleared** (with N124).

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze (was)

| Post | Waarde | Bron |
|------|--------:|------|
| Signal | Yahoo/proxy **XLU/XLI** relative (adjclose) | S2 cycle_2346 / `data/daily/` |
| Trade | `US500cash` (US500 twin; **not** US100) | FTMO / S2 FLAG |
| Round-trip intradag (RT) | **0,78 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (EOD flat same CET day) | D-100 session-flat |
| Hold | entry first M5 **[15:30, 15:45] CET** → flat **21:00 CET** | was freeze |
| **Gate (binding)** | **3 × 0,78 = 2,34 bp** | pure intradag |
| Stress (informeel) | **1,5 × 2,34 = 3,51 bp** | vóór formal t |

Pre-screen (historical): `results/R2/n124_n125_prescreen/` — N125 PASS train N=478 mean +5,48 ≥2,34.

Pointer: `results/lane_b/DEFENSIVE_CYCLICAL_SOURCE.md` → S2 @ `13fe10c`.
