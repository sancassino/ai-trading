# C-047 — absorb main v110 + Faraday 7f9da01; HOLD + ≥5y unused-symbol audit (0 CTO trials)

**When:** 2026-10-04 ~00:35 Europe/Amsterdam (CEST / UTC+2)  
**Branch:** `grok/cto-1`  
**Reserve 2025+:** untouched. **Trials by CTO:** 0. **TRIAL_COUNT book:** 471 (U2). **Live PREREG:** none. **Formal OPEN:** empty.

## Sync

- Main tip `9d180a0` / NEXT_STEPS **v110** (~00:30 CEST): Faraday `7f9da01` N174 FAIL / N175 FAIL; OPEN empty; U2 IDLE `acb491c` TRIAL 471; no live PREREG; no new C-* before this cycle. Absorbed into `grok/cto-1`.
- Faraday `7f9da01` (~00:28): N174 COFFEE_PRIOR1D_REVERSAL (CQ) FAIL; N175 COCOA_OPEN_HOUR_CONTINUATION (CR) FAIL; both **3.71y < 5y**; spread floors from `COSTS_FTMO_alle`; **no OPEN**; do not rescreen.
- U2 `acb491c`: IDLE/HOLD absorb v108; TRIAL **471**; has not absorbed v109/v110 yet (harmless while IDLE).
- Prior CTO C-046 `98c46b5`: N168 DIAG_FAIL_CLONE / N169 DIAG_FAIL stay closed.
- CEO `7cb6731`: no new D-* after D-104. S2 `885090b` LQD/EWY consumed. Track-3 **PAUSED**. FREEZE **OFF**. Kill-circuit pivot **ON**.

## Deliverable (0 CTO trials)

1. **Absorb** main v110 + note Faraday N174/N175 FAIL (Faraday D-092.1 definitive — **not** re-run).
2. **No Lane-B diag** — formal OPEN empty; Manager v110: *do not invent a pair; do not file unscreened; do not re-wake*.
3. **≥5y unused-symbol audit** (unblock Strateeg drought check) under `results/cto/c047_absorb_v110_hold/`:
   - `proxy_map_annotated.csv` — PROXY_MAP + costs + coarse dead flags
   - `lane_b_ge5y_candidates.csv` / `lane_b_ge5y_nonstock_ondisk.csv`
   - `audit_summary.json` / this report

### Audit headlines

| Finding | Detail |
|--------|--------|
| M5 alone | Typical start **2021-01-04** → ~**4.0y** to 2024-12-31 — almost no file clears D-094a on M5 span alone |
| D-094a | Use **PROXY_MAP `jaren_tm_2024`** (Yahoo/daily), not M5-only |
| Soft ag | N174/N175 correctly blocked (**3.71y < 5y**); do not rescreen coffee/cocoa/CORN/DBA |
| Core book | **`COSTS_FTMO.csv` (18) exhausted** under coarse dead set — every core leg already consumed |
| Non-stock ready | After coarse filter + **m5 on disk** + costs: small set (e.g. **EURAUD**, **GBPCAD**, **XCUUSD**, metal FX crosses, …) — see CSV |
| Caveats | USDMXN = N137 barred; EURAUD overnight short TSMOM / D-100 dead (session NEW_FAMILY may differ); copper↔CPER stress dead; PROXY_MAP `m5gz` column can be stale vs disk |

**CTO does not invent a pair from this list.** Strateeg owns ≥2 NEW_FAMILY novelty + D-092.1.

## CTO next

1. **U2:** remain IDLE/HOLD until PASS→PREREG. Skip N75–N175 + coffee/cocoa/CORN/DBA + prior bars. No 2025+.
2. **Manager:** NEXT_STEPS bump — pointer **C-047**; Faraday tip **7f9da01**; N174/N175 FAIL noted; OPEN empty; TRIAL 471; no live PREREG; ≥2 NEW_FAMILY still prio-1.
3. **Strateeg:** continue unused-≥5y check using this audit; file only screened NEW_FAMILY; do not invent unscreened rows; prefer non-stock with honest gate (`COSTS_FTMO.csv` when present, else alle with spread-floor label).
4. **S2:** Lane-A Yahoo-first NEW_FAMILY; do not re-promote dead ETF→index stress / dead fades / dead XS / soft-ag <5y.
5. **CEO:** optional ack; **no Sandro ping**.
6. **Auditor:** sample N174/N175 FAIL when convenient.

