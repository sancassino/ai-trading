# C-027 — USDJPY_MED FAIL_T absorb + EURJPY_MED PREREG

**Time:** 2026-10-01 ~12:30 Europe/Amsterdam (CEST).  
**Branch:** `grok/cto-1`. Reserve 2025+: **untouched**.

## Absorbed (U2 formal)

| Item | Value |
|------|------:|
| PREREG | `PREREG_FTMO_FX_USDJPY_MED_TSMOM` |
| U2 tip | `910d6ff` |
| Outcome | **FAIL_T** (counts_as_trial=true) |
| TRIAL_COUNT | **454 → 455** |
| Train N / bruto / gate | 237 / +10.97 bp / 2.34 **PASS** |
| Train t day-clust / NW-L5 | **1.15 / 1.16** (<2) |
| Test N / bruto / h1 | 121 / +17.25 / **−11.88** |

CTO independent re-run concordant. No `ftmo_ev`. No clones.

## Family B L60 diag (0 trials; ≤2024)

| Code | Sym | Train N | bruto | gate | pass | t | Notes |
|------|-----|--------:|------:|-----:|:----:|--:|-------|
| N72 | EURJPY | 209 | +7.81 | 3.30 | YES | 0.55 | both halves >0; test halves >0 |
| N73 | USDCAD | 235 | +0.73 | 2.40 | NO | 0.11 | DIAG_FAIL |
| N74 | USDCHF | 215 | −7.57 | 3.03 | NO | −0.21 | DIAG_FAIL |

## Next

Freeze `PREREG_FTMO_FX_EURJPY_MED_TSMOM` (solo EURJPY L60/H10 long; ≠ USDJPY_MED pair).  
Prior: weak (diag t≈0.55) — honesty over optimism. If FAIL_T → pivot off L60 FX-med family.
