# PREREG_FTMO_N40 — GER40cash Mid-Morning Momentum Continuation

**Status:** **STOP FAIL_T** — U2 `5b3db74` (TRIAL_COUNT **453**; formal trial **452**).  
Cost-gate PASS (mean +2,43 ≥ 2,16; N=205); stress **FAIL** (3,24) → **FAIL_STRESS_then_FAIL_T**.  
Median bruto −2,28 (caveat) bevestigd fragiel. **Geen retune / herstart zonder CEO.** Reserve 2025→ onaangeraakt.

**Auteur:** Strateeg (Grok). **Instrument:** `GER40cash`. RT 0,72 → gate 2,16.

## Regel (archief)
- mom_bp = 1e4×(C_1200−C_0930)/C_0930; |mom|≥40 → entry 12:00; flat 14:00; stop 1×ATR14.
