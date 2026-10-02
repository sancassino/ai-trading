# PREREG_FTMO_N103 — GER40 Lon-AM → US30 NY industrial lead-lag (NEW_FAMILY Z)

**Status:** **STOP FAIL_STRESS** — U2 `b9af560` (Faraday tip `7059c63`). Cost PASS (train N=286 mean +1,75 ≥ 1,35); stress FAIL vs 2,025; years 2021 +2,29 / 2022 +10,53 / 2023 −14,08; Test 2024 N=74 +1,32 (info). **geen trial**; TRIAL_COUNT **460**. Dead += N103. No retune / no US100 / no GER→US-open clones.  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**VOORSTEL:** `VOORSTEL_PRESCREEN_N103.md`.  
**Signal:** `GER40cash` (Lon-AM impulse). **Trade:** `US30cash`.  
**NEW_FAMILY Z:** EU industrial equity AM impulse → US industrial PM same-dir session-flat.  
**Hold:** **session-flat** entry ≈15:30 CET → flat ≈21:00 CET (D-100; US30 overnight swap avoided).  
**TRIAL_COUNT book:** **460** (deze PREREG telt nog niet).  
**Reserve 2025+:** **onaangeroerd.**  
**Geen retune** na freeze.

Pre-screen: `results/R2/n102_n103_prescreen/` — N103 **PASS** train N=**286** mean bruto **+1,75** ≥ gate **1,35**.

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze

| Post | Waarde | Bron |
|------|--------:|------|
| Signal | `GER40cash` | FTMO M5 |
| Trade | `US30cash` | FTMO |
| Round-trip intradag (RT) | **0,45 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (EOD flat same CET day) | D-100 session-flat |
| Hold | entry first M5 **[15:30, 15:45] CET** → flat **21:00 CET** | bevroren |
| **Gate (binding)** | **3 × 0,45 = 1,35 bp** | pure intradag; geen D-097 50-floor |
| Stress (informeel) | **1,5 × 1,35 = 2,025 bp** | vóór formal t |

Alfa = signed mean **bruto prijs**; geen swap-credit.

---

## 2. Economisch mechanisme (NEW_FAMILY Z)

`NEW_FAMILY: Z` — Lon-AM GER40 industrial risk impulse leads US industrials (Dow) into the NY cash session:

1. Europe morning risk (DAX/GER40 08:00→12:00 CET) prices industrial / cyclical risk appetite.
2. Same-direction continuation on US30 afternoon when `|ger_am| ≥ 40 bp`.
3. Session-flat avoids US30 overnight swap (long ≈2,28 bp/nacht).

**Distinct / dead-set guard:**
- ≠ **N98** USOIL→US100 DIAG_FAIL (olie→tech)
- ≠ **S2-GER_US_LEAD** STOP (GER→**US open** / US100 — ander target/window)
- ≠ **N85** US500→US100 DIAG_FAIL / **N41/N35** EU→US cont FAIL_T
- ≠ EMB / CRACK / SECTOR_DISP / VIX / ORB-meta / L60 / UKOIL-OVN / CORN / NY-2h / N75–N102 restarts

---

## 3. Bevroren regel

1. Lon-AM GER impulse: `ger_am_bp = 1e4 × (GER40cash_close@12:00 / GER40cash_close@08:00 − 1)` (first M5 in ±15 min windows).
2. Trade only if `|ger_am_bp| ≥ 40`.
3. Same-direction US30: ger_am ≥ +40 → **LONG** US30; ger_am ≤ −40 → **SHORT** US30.
4. Entry: US30 close of first M5 in **[15:30, 15:45] CET**. If missing, skip day.
5. Exit: flat at **21:00 CET** same day. **No overnight.**
6. Non-overlapping (≤1/day).

---

## 4. D-092.1 pre-screen (train-only; binding for PREREG eligibility)

| Metric | Value |
|--------|------:|
| Train | 2021-01-01 … 2023-12-31 |
| N | **286** (≥150) |
| Mean bruto | **+1,75 bp** (≥ 1,35) |
| Median | −1,13 bp |
| Hit-rate | 0,49 |
| Years | 2021 **+2,29** / 2022 **+10,53** / 2023 **−14,08** |
| Verdict | **PASS_may_PREREG** |
| Artifacts | `results/R2/n102_n103_prescreen/prescreen.json` + `n103_trades_train.csv` |

**Note for U2:** 2023 train year negative — stress/year-split may FAIL even if mean PASS; no thr-grid, no US100 substitute, no GER→US-open rewrite.

**D-094a reden (b):** cross-Atlantic industrial equity lead–lag (DAX morning risk → US industrials afternoon); FTMO-M5 both series.

---

## 5. Splits / anti-kloon

- **Train:** 2021–2023. **Test:** 2024 (U2). **Reserve 2025+:** untouched.
- FAIL → STOP (geen thr-grid, geen US100 substitute → N41/N85 clone, geen GER→US-open rewrite → S2-GER_US clone, geen overnight).

---

## 6. Bestanden / catalogus-ID

- **PREREG:** `PREREG_FTMO_N103_GER40_US30_INDUSTRIAL.md` (**N103** — **OPEN**)
- **VOORSTEL:** `VOORSTEL_PRESCREEN_N103.md`
- **Screen:** `results/R2/n102_n103_prescreen/`
- **Catalogus-ID:** **N103** / NEW_FAMILY **Z**
- Branch: `claude/trusting-faraday-34tsmg`
