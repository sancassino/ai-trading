# PREREG_FTMO_N125 — DEFENSIVE_CYCLICAL (US500cash twin; session-flat; Lane-B from S2)

**Status:** **OPEN** — frozen for U2 cost-gate + formal trial (Lane-B D-092.1 PASS).  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**Bron Lane-A:** Strateeg-2 (`grok/strateeg-2`) @ **`13fe10c`** — cycle_2346.  
**VOORSTEL:** `VOORSTEL_PRESCREEN_N125.md`.  
**Instrument (primary):** `US500cash` (**US500 twin** per S2 FLAG — **not** US100 overnight). Signal-only XLU/XLI (no sector CFD trade leg).  
**NEW_FAMILY AT:** `DEFENSIVE_CYCLICAL` — XLU/XLI relative → equity session-flat.  
**Hold:** **session-flat** entry ≈15:30 CET → flat ≈21:00 CET (D-100).  
**TRIAL_COUNT book:** **464** (deze PREREG telt nog niet).  
**Reserve 2025+:** **onaangeroerd.**  
**Geen retune** na freeze.

Pre-screen: `results/R2/n124_n125_prescreen/` — N125 **PASS** train N=**478** mean bruto **+5,48** ≥ gate **2,34**.

Pointer: `results/lane_b/DEFENSIVE_CYCLICAL_SOURCE.md` → S2 @ `13fe10c`.

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze

| Post | Waarde | Bron |
|------|--------:|------|
| Signal | Yahoo/proxy **XLU/XLI** relative (adjclose) | S2 cycle_2346 / `data/daily/` |
| Trade | `US500cash` (US500 twin; **not** US100) | FTMO / S2 FLAG |
| Round-trip intradag (RT) | **0,78 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (EOD flat same CET day) | D-100 session-flat |
| Hold | entry first M5 **[15:30, 15:45] CET** → flat **21:00 CET** | bevroren |
| **Gate (binding)** | **3 × 0,78 = 2,34 bp** | pure intradag |
| Stress (informeel) | **1,5 × 2,34 = 3,51 bp** | vóór formal t |

**Lane-A context (niet de formele poort):** Best day_t landed on XLU/XLI→NDX/US100 short-bias (day_t 2,08 / mean 19,75 / drag 1,69 / net 18,07 COST_OK). **S2 FLAG:** US100 overnight long swap expensive — **prefer US500 twin** (same config day_t=2,02 / mean 16,48 / drag 4,82 / net 11,66 COST_OK). Lane-B maps to **US500 session-flat** (D-100). Alfa = signed mean **bruto prijs**.

---

## 2. Economisch mechanisme (NEW_FAMILY AT — DEFENSIVE_CYCLICAL)

`NEW_FAMILY: DEFENSIVE_CYCLICAL` — utilities-vs-industrials relative as **defensive-vs-cyclical risk-appetite** proxy:

1. `ratio_t = XLU_adj_t / XLI_adj_t`.
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)` (min_periods = max(20, 13)).
3. **defensive_high (freeze):** `z40 > +0,5` → **SHORT** US500 (defensive outperforming = risk-off); `z40 < −0,5` → **LONG** (cyclicals leading = risk-on); else skip.
4. Maps to **US500cash** (not US100; not XLU/XLI CFD).

**Distinct / dead-set guard:**
- ≠ **N93 SECTOR_DISP_ROTATION** FAIL_COST_GATE (XL* cross-sectional dispersion ≠ XLU/XLI *relative level*)
- ≠ **N119 IWM_SMALLCAP** / **N81** pair RV / ORB / L60 / N75–N123 clones
- ≠ US100 overnight long rewrite (S2 FLAG hostile); soft gate; thr-grid; sector CFD trade leg

---

## 3. Bevroren regel (geen retune)

**Signal (dag t, na US ETF close ≈22:00 CET):**
1. Data: Yahoo/proxy dagclose **XLU**, **XLI** (adjclose).
2. `ratio`, `z40` as §2.
3. defensive_high long/short/skip as §2.

**Execution (dag t+1, FTMO M5 `US500cash`) — D-100 session-flat:**
4. Entry: close van eerste M5-bar ≥ **15:30 CET** (span ≤15 min). Ontbreekt → skip day.
5. Exit: close van laatste M5-bar ≤ **21:00 CET** same day. **Geen overnight. Geen sector CFD leg. Geen US100 rewrite.**
6. PnL: `pnl_bp = position × (P_exit / P_entry − 1) × 1e4`.
7. Non-overlapping (≤1 trade/dag).
8. **Verboden:** thr-grid op 2025+; overnight hold; US100-first overnight; SECTOR_DISP rewrite → N93 clone; soft gate; XLU/XLI CFD.

---

## 4. D-092.1 pre-screen (train-only; binding for PREREG eligibility)

| Metric | Value |
|--------|------:|
| Train | 2021-01-01 … 2023-12-31 |
| N | **478** (≥150) |
| Mean bruto | **+5,48 bp** (≥ 2,34) |
| Median | +4,81 bp |
| Hit-rate | 0,54 |
| Long / short | 249 / 229 |
| Years | 2021 **+0,90** / 2022 **+8,84** / 2023 **+3,72** |
| Stress (info) | mean ≥ 3,51 → informal PASS |
| Verdict | **PASS_may_PREREG** |
| Artifacts | `results/R2/n124_n125_prescreen/prescreen.json` + `n125_trades_train.csv` |

**D-094a reden (b):** Defensive-vs-cyclical relative (XLU/XLI) as risk-appetite timing into DM equity beta — distinct from SECTOR_DISP cross-sectional dispersion; FTMO-M5 for costs. Lane-A proxy span ~20y ✔. US500 twin per S2 FLAG (avoid US100 overnight long swap).

---

## 5. Splits / anti-kloon

- **Train:** 2021–2023. **Test:** 2024 (U2). **Reserve 2025+:** untouched.
- FAIL → STOP (geen thr-grid, geen US100 overnight rewrite, geen SECTOR_DISP clone, geen soft gate). Dead label `N125_DEFENSIVE_CYCLICAL`.

---

## 6. Bestanden / catalogus-ID

- **PREREG:** `PREREG_FTMO_N125_DEFENSIVE_CYCLICAL.md` (**N125** — **OPEN**)
- **VOORSTEL:** `VOORSTEL_PRESCREEN_N125.md`
- **Source pointer:** `results/lane_b/DEFENSIVE_CYCLICAL_SOURCE.md`
- **Screen:** `results/R2/n124_n125_prescreen/`
- **Lane-A:** `git show 13fe10c:results/strateeg2_prescreen/cycle_2346/…`
- **Catalogus-ID:** **N125** / NEW_FAMILY **AT**
- Branch: `claude/trusting-faraday-34tsmg`
- **TRIAL_COUNT (book):** **464**
