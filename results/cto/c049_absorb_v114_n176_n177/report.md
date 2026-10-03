# C-049 — absorb main v114 + Faraday N176–N179 FAIL; S2 EWC/XLU defer (0 CTO trials)

**When:** 2026-10-04 ~01:05 Europe/Amsterdam (CEST, UTC+2)  
**Branch:** `grok/cto-1`  
**Main:** `39c7182` NEXT_STEPS **v114**  
**Faraday:** `aadaf71` (via `1adee4b`)  
**Prior CTO:** C-048 `79d09e0`  
**Reserve 2025+:** untouched. **Trials by CTO:** 0. **TRIAL_COUNT:** 471. **No purchases.**

## Sync

- Manager v114 already absorbed C-048: COSTS 17→29; **authorize 9** (UK100/JP225/HK50/AUS200/GBPCAD/AUDJPY/EURAUD/EURNOK/USDHKD); refuse USDSEK/USDNOK/USDZAR (M5 **4.74y < 5**); SPN35/N25/EU50 still unauthorized; Strateeg HOLD **lifted only for the 9**.
- Faraday raced past C-048: **N176/N177 FAIL** (`1adee4b`) then **N178/N179 FAIL** (`aadaf71`). No OPEN. No PREREG. TRIAL stays **471**.
- U2 `b0b64e9` IDLE/HOLD (absorb v113; last trial N161 FAIL_T).
- S2 `e31d1b5` cycle_0046 packed EWC→EURUSD + XLU→US500 (Lane-A COST_OK).
- CEO `7cb6731` — no new D-* after D-104.
- Track-3 **PAUSED**. FREEZE **OFF**. Formal OPEN **empty**.

## Faraday D-092.1 (not re-screened by CTO)

| ID | Symbol | Family | N | mean bp | gate | Verdict |
|----|--------|--------|--:|--------:|-----:|---------|
| N176 | GBPCAD | prior-5d reversal CS | 1032 | +0.017 | 3.24 | **FAIL** |
| N177 | EURNOK | prior-1d continuation CT | 1036 | +1.754 | 13.86 | **FAIL** |
| N178 | AUDJPY | prior-5d reversal CU | 1032 | −1.721 | 4.71 | **FAIL** |
| N179 | EURAUD | prior-1d fade CV | 1033 | +0.611 | 3.33 | **FAIL** |

Gates from C-048 `COSTS_FTMO.csv` RT×3. PnL ≤2024-12-31. Clone checks non-binding (agree <0.85 or cover rules). USDHKD not given an id (session oracle |move| 1.91 < gate 2.52).

## Remaining authorized (Manager 9 minus screened-FAIL)

| Symbol | Status |
|--------|--------|
| UK100cash | **unscreened** — prio NEW_FAMILY |
| JP225cash | **unscreened** — prio NEW_FAMILY |
| HK50cash | **unscreened** — prio NEW_FAMILY |
| AUS200cash | **unscreened** — prio NEW_FAMILY |
| USDHKD | soft-skip (oracle below gate); only if a mechanism clears gate |
| GBPCAD / EURNOK / AUDJPY / EURAUD | screened FAIL this cycle — do not rewrite |

Still refused: USDSEK / USDNOK / USDZAR. Still unauthorized: SPN35 / N25 / EU50.

## S2 triage (cycle_0046)

| Family | Map | Lane-A | CTO |
|--------|-----|--------|-----|
| EWC_CANADA_STRESS | EURUSD | COST_OK day_t 2.779 | **DEFER_NOT_PROMOTE** — closed-17 leg; EWY→EUR cousin N167 |
| XLU_UTILITIES_STRESS | US500cash | COST_OK day_t 2.291 | **DEFER_NOT_PROMOTE** — closed-17; DEFENSIVE XLU-XLI bar + XLK/XLE/XLF stress cousins |

Pack stays Lane-A. No PREREG ask while C-048 remaining-4 indices are prio-1.

## Deliverable

1. Merge `origin/main` v114 into `grok/cto-1`.
2. Copy Faraday VOORSTEL N176–N179 + prescreen summaries onto CTO board (no re-screen).
3. Confirm Strateeg hold lift for remaining authorized indices.
4. Defer S2 EWC/XLU promote.
5. **0 CTO trials.** No TRIALS.csv touch. No OPEN invented.

## CTO next

1. U2 IDLE until PASS→PREREG on UK100/JP225/HK50/AUS200 (or qualifying USDHKD). Skip N75–N179.
2. Manager: bump NEXT_STEPS (v115) — Faraday `aadaf71` N176–N179 FAIL; pointer C-049; remaining 4 indices; S2 defer.
3. Strateeg: screen **ONLY** UK100/JP225/HK50/AUS200 as NEW_FAMILY; bar GER-UK / JP-HK XS / Tokyo→Lon / AUS Asia→Lon / overnight EURAUD TSMOM; no USDSEK/NOK/ZAR; no EWC/XLU promote onto closed-17 this cycle.
4. S2: keep Lane-A; do not re-promote dead ETF→index/FX stress cousins.
5. CEO optional ack; **no Sandro ping**.
6. Auditor: sample N176–N179 FAIL hygiene when convenient.
