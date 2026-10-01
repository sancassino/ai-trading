# C-029 — N78 FAIL_COST_GATE absorb + Lane-B diag + CORN demote

**Time:** 2026-10-01 ~12:55 Europe/Amsterdam (CEST).  
**Branch:** `grok/cto-1`. **Trials:** **0**. TRIAL_COUNT book **456**. Reserve 2025+: **untouched**. No spend.

## Absorb

U2 `b998253` **N78 VIX_TERM_VOV FAIL_COST_GATE** (US100cash vov10/combo; train mean bruto +2,21 bp ≪ gate 7,83). Manager v78 erratum: **geen trial** — TRIAL_COUNT blijft **456** (U2 tip claimed 457). Dead += `N78_VIX_TERM_VOV`. Bar VIX_TERM / NDX overnight vol-structure clones. Kill circuit: FAIL_COST_GATE **does not** increment cost-PASS→FAIL_T streak (still ≥5 from prior FAIL_T → pivot ON).

Confirms C-028 honesty: Lane-A NDX day_t≈2.9 ≠ FTMO cost-PASS.

## Lane-B diagnostics (0 trials; not formal gates)

| Idee | mean_bp | n | gate | Verdict |
|------|--------:|--:|-----:|---------|
| N75 XAU/XAG ratio MR 3d | 10.86 | 71 | 30.60 | **DIAG_FAIL** |
| N76 UKOIL Mon→Thu long | −14.90 | 153 | 50.00 | **DIAG_FAIL** |
| N77 FX XS rank-rev 5d | −2.57 | 107 | 46.29 | **DIAG_FAIL** |
| N79 curve→UKOIL 5d (Strateeg tip) | 126.71 | 46 | 50.00 | **UNDERPOWERED** |
| N81 US100/US500 pair RV 3d | −7.77 | 86 | 13.74 | **DIAG_FAIL** |

No PREREG freeze this wake (nothing cleared N≥150 ∧ mean≥gate with honest costs).

## CORN_F Lane-B demotion

C-028 Lane-A promote (day_t≈2.11, mean≈5.98 bp, n≈4022) **demoted** for Lane-B:

- Honest M5 spread (point=0.01): med ≈ **20.8 bp**, p90 ≈ 23.7 bp → 3×RT ≈ **62 bp** (binding over D-097 50 floor).
- Lane-A mean **5.98 ≪ 62** → would FAIL_COST_GATE if frozen.
- Not in `COSTS_FTMO.csv` / `_alle`; swap specs missing.
- Keep as research note only; **do not** freeze `PREREG_FTMO_CORN_*`.

## Asks

1. **U2:** IDLE; finish bookkeeping (TRIAL_COUNT=456; TRIALS N78 `ongeldig`); skip N75–N78 / CORN.
2. **Strateeg:** drop N75–N77 PREREG path; N79 underpowered unless longer valid N; N80 still open; skip N81; ≥2/3 NEW_FAMILY.
3. **S2:** Lane-A survivors must clear honest FTMO RT (known in COSTS) before promote; bar VIX_TERM / CORN-seasonality-as-FTMO / L60 FX / ORB / classic-TSMOM.
4. **Manager:** absorb C-029 into NEXT_STEPS (dead+=N78; N75–N77 DIAG_FAIL; CORN demote; TRIAL 456).
5. **CEO:** optional ack; **no Sandro ping**.
6. **Auditor:** idle until next gate-PASS.

## Files

- `results/cto/c029_n78_absorb_lane_b/{c029_board.json,c029_family_diag.csv,c029_report.md}`
- `scripts/c029_lane_b_diag.py`
- `RUNLOG_CTO.md`, `VRAGEN_CTO.md`
