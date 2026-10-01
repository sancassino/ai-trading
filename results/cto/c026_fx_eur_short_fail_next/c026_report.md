# C-026 — FX_EUR_SHORT FAIL_T absorb + D-100 family diag + USDJPY_MED PREREG

- When: 2026-10-01 ~12:05 Europe/Amsterdam (CEST / UTC+2)
- Branch: `grok/cto-1`
- Reserve 2025+: **untouched**
- Trials appended by CTO: **0** (U2 already appended TRIAL **454** on `claude/uitvoerder2-r`)
- No FTMO signup / spend. No EINDSTAND re-nag.

## 1. FX_EUR_SHORT_TSMOM — CTO absorb (no `ftmo_ev`)

U2 `0e04df6` gated `PREREG_FTMO_FX_EUR_SHORT_TSMOM` (L20/H10 SO, EURUSD+EURAUD):

| Metric | Train 2010–2016 | Test 2017–2024 |
|--------|----------------:|---------------:|
| N_trades | 227 | 239 |
| mean bruto bp | **+21.96** | **−3.42** |
| gate 3× / stress | **PASS** / PASS | — |
| t day-clust / NW-L5 | 1.90 / 1.87 | −0.14 / −0.13 |
| counts_as_trial | **true** | |
| TRIAL_COUNT | **453 → 454** | |

EURAUD test bruto −8.09 (dual-symbol bruto≥0 FAIL). Train t just under 2.0.

**CTO action:** skip `recommend_scale` / `ftmo_ev`. Dead/FAIL += **FX_EUR_SHORT_TSMOM**.
**No clones:** no L/H grid, no EURGBP-add, no long-been, no 5d-retune.

## 2. D-100 family diagnostic (proxy ≤2024; 0 trials)

See `c026_family_diag.csv`. Honest RT from CEO `spread_bp` where no COSTS_FTMO row.

| Bucket | Finding |
|--------|---------|
| **B N69 NZDUSD long L20/H10** | train −29 bp vs gate ~33 → **DIAG_FAIL** |
| **B N71 GBPUSD short L20/H10** | train +3.8 vs gate 11.1 → **DIAG_FAIL** |
| **B EURGBP / GBP pool short** | FAIL (halves / test) |
| **C N70 XAU L5/H5 both** | long swap wall gate ~35; short L5 gate-only but h1<0 → **DIAG_FAIL** |
| **D COFFEE long L20/H10** | with C-024 rt_est=2 → looks PASS; with honest CEO spread_bp≈10.4 → gate 31 > train 14.6 → **DIAG_FAIL**; S2 already FAIL D-092.1 |
| **D soft shorts / NATGAS** | FAIL |
| **B USDJPY long L60/H10** (train 2000–2016) | N=237 mean +10.97 ≥ gate 2.34; h1/h2 both >0; test mean +17.25 (h1 test <0) → **freeze PREREG** |

Caveat: USDJPY test h1 bruto negative — prior moderate. Diagnostic ≠ formal gate.
N67 was L20/H10 DIAG_FAIL — this PREREG is **medium-term L60/H10** (C-022 D-097 FX path), not an L/H clone of N67.

## 3. Frozen PREREG — `PREREG_FTMO_FX_USDJPY_MED_TSMOM.md`

- Universe: **USDJPY** only, **long-only** when 60d momentum > 0; hold 10d
- Proxy: `FX_USDJPY` (≥10y; D-094a b); train **2000–2016** / test **2017–2024**
- Swap: long side earns in COSTS_FTMO (−0.37 bp/night) → gate zeros credit; alfa = bruto prijs
- Gate script: `scripts/fx_usdjpy_med_tsmom_gate.py`
- U2: cost-gate next; no 2025+

## 4. Flags for Strateeg / S2 / Manager

- **FX_EUR_SHORT_TSMOM** dead (FAIL_T trial 454).
- **N69 / N70 / N71** → DIAG_FAIL (do not PREREG as filed).
- Prefer non-clone D-097/D-100 screens (intradag-flat or other cheap sides with **honest** RT, not category fallback 2 bp on softs).
- Family A overnight index-short still **closed**.

## 5. CTO next

1. U2: gate `PREREG_FTMO_FX_USDJPY_MED_TSMOM` via `scripts/fx_usdjpy_med_tsmom_gate.py`.
2. On PASS → track-5 `ftmo_ev`. Track-3 still PAUSED.
3. No Sandro ping (no validated sleeve; no eval).

Artefacts: `c026_board.json`, `c026_family_diag.csv`, this report.
