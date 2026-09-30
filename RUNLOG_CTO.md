# RUNLOG_CTO — Grok CTO (branch `grok/cto-1`)

## Kickoff — 2026-09-30 21:09 Europe/Amsterdam (CET / UTC+2)

**Branch:** `grok/cto-1` from `main` @ `8e0aa3b` (Verslag backlog v34).  
**Repo:** `/workspace/ai-trading` (clone `sancassino/ai-trading`).  
**Scope this kickoff:** Priority 1 = `engine/ftmo.py` + this log. No reserve-period data touched. No FTMO accounts opened. No secrets committed.

### Context read

| Source | Takeaway |
|---|---|
| `origin/claude/upbeat-dirac-g2810q:BESLUITEN.md` (tail / D-047…D-086) | **D-083 KOERSCORRECTIE:** goal is FTMO prop €80k (2-Step), **not** own capital. Ambition ≈ €800–900/m payout; €400–500 ok if robust. Own-capital work (ALLOCATIE/VERWACHTING/P-ETF/S10b/box 3) → park. **D-084:** reserve-run 01-10 **suspended**. **D-085 FASE 3 — FTMO-EV:** metric = FTMO-EV (P pass1/2, P survive funded, €/m payout, fee/attempts, net EV); module **`engine/ftmo.py`**; vehicle `cfd` + FTMO costs/swaps; universe = `SymbolList_FTMO.csv`. **D-086:** Uitvoerder-2 builds `engine/ftmo.py`; Auditor retargets FTMO; no more “beat 60/40/cash” as goal metric. |
| `NEXT_STEPS.md` (v34 on main) | Still largely own-capital cadence; header warning (20:50) that goal is FTMO €80k. CEO D-085 asks Manager for NEXT_STEPS v32+ FTMO program — **main not yet fully pivoted**; CTO treats D-083…D-086 as binding over stale NEXT_STEPS body. |
| `RUNLOG.md` (tail) | Uitvoerder-1 data/QA/forward/PORT3–4 work; eigen-kapitaal MC/kosten. Useful data pipelines remain; goal framing superseded by D-083. |
| `origin/claude/uitvoerder2-r:RUNLOG_R2.md` (tail) | Catalog runs 2–8, frontiers, S11 cross-market (“C02 = DD filter only”), reserve script ready but **D-084 suspends** ETF reserve burn. No `engine/ftmo.py` on that branch yet. |
| `COSTS_FTMO.csv` | Per-symbol median/P90 spread bp + commission + swap long/short bp/night (S0, 2026-09-30). Indices ~0.5–1 bp RT; swaps material for overnight longs. |
| `swap_specs_FTMO.csv` | Raw MT5 swap mode/long/short + implied %/yr (e.g. US500 long ≈ −5%/yr). |
| `SymbolList_FTMO.csv` | FTMO instrument universe (equities/FX/crypto/indices CFDs) — search space for FASE 3. |
| Related code | `q1_frontier.py` (vectorized MC, restart, fee refund), `q1b_products.py`, `mc_daily_ftmo.py` (month blocks + floating min equity), `ftmo_economics.py` (close-only daily, single attempt), `monte_carlo_ftmo.py` (monthly), `engine/run_rule.py` (cfd costs). |

### Decisions inferred (for FTMO-EV module)

1. **API surface** = `ftmo_ev(...)` returning at least `p_pass_1, p_pass_2, p_survive, exp_payout_monthly, net_ev` (D-085 + kickoff signature).
2. **Rules:** phase targets 10%/5%, min 4 days, max daily loss 5% of *initial* (static) **including floating P&L** when `daily_drawdowns` supplied, max DD 10% static, split 80%, fee €540 (unverified assumption, D-083), account €80k.
3. **Align implementation** with `q1_frontier` (numpy block-bootstrap, restart-on-breach, fee refund on first payout) so EV is comparable to Q1 income frontier; close-only proxy when no intraday trough series (same caveat as `ftmo_economics`).
4. **Do not** scale recommendations above 4% daily-loss risk (D-016 / D-085); `scale` is an analysis knob only.
5. **Do not** open reserve 2025-01→ or own-capital portfolio work in this kickoff.

### `engine/ftmo.py` status — DONE (kickoff)

- Module: `engine/ftmo.py`
- Entry: `ftmo_ev(daily_returns, fee=540, account=80000, split=0.8, phase1_target=0.10, phase2_target=0.05, max_daily_loss=0.05, max_dd=0.10, min_days=4, **opts)`
- Helpers: `load_daily_equity_csv` (q1-compatible daily equity log), CLI `__main__`
- Smoke (2026-09-30 CET):
  - `python3 -m engine.ftmo --paths 3000` → synthetic positive-drift path prints full dict
  - `python3 -m engine.ftmo --csv results/f/F1_RSI2_swapcorr_daily.csv --scale 1.0 --paths 5000` → runs; at scale 1 low funded rate / negative net_ev (expected for unsized sleeve — not a claim)
- Next (not this commit): wire catalog sleeves / daily series → FTMO-EV; cfd vehicle re-eval per D-085.2; Strateeg plan v4 search directions.

### Git

```
git add engine/ftmo.py RUNLOG_CTO.md
git commit -m "CTO: init log and engine/ftmo.py FTMO-EV simulator"
git push -u origin grok/cto-1
```

## Wake cycle — 2026-09-30 22:05 Europe/Amsterdam (CET / UTC+2)

**Branch:** `grok/cto-1` (worktree `/workspace/ai-trading-cto`; primary clone was mid-U2 cycle on `claude/uitvoerder2-r`).  
**No reserve 2025-01→ opened. No TRIALS.csv writes. No formal PREREG trial claimed.**

### 1) A4 unblock — PREREG test windows frozen (C-001 closed)

Uitvoerder-2 hard-blocked on Test 2024–2026 vs D-084. CTO default under D-084 (no CEO wait):

| Window | Dates |
|---|---|
| Train | 2021-01-01 … 2023-12-31 |
| Test | 2024-01-01 … 2024-12-31 |
| Reserve | 2025-01-01 → ONAANGERAAKT |

- Documented closed in `VRAGEN_CTO.md` (C-001).
- Strateeg already pushed freeze @ `5fc3fb9` on `claude/trusting-faraday-34tsmg` (22:02). **No second push to Strateeg** (would race; their amend is authoritative for U2 to re-fetch).
- Same window wording + residual C17 data-line “2021–2026” → plafond ≤2024-12-31 landed on `grok/cto-1` (`PREREG_FTMO_C17.md`, `PREREG_FTMO_FX_INTRADAG.md`).
- U2 tip `d72bb91` still carries pre-freeze PREREG text; they must re-read Strateeg tip or CTO copies.

### 2) Sync with main

Merged `origin/main` @ `d75f59d` (NEXT_STEPS v36 / D-089–D-090) into `grok/cto-1`. Kept `engine/ftmo.py` + `RUNLOG_CTO.md`.

### 3) `engine/ftmo.py` — p_survive right-censoring fix

U2 note: late-funded paths that never finish `live_months` were counted as survived.

**Fix (API stable — `ftmo_ev` signature unchanged):**
- Exclude right-censored incompletes: funded ∧ (funded_day + live_days > horizon) ∧ ¬breach_live.
- Eligible for `p_survive` / `breach12_given_funded` = funded ∧ ¬incomplete (breaches during observed live still count as failures).
- New diagnostics: `n_funded`, `n_survive_eligible`, `n_funded_incomplete`.

**Smoke (this cycle):**
- `python3 -m engine.ftmo --paths 2000` → p_pass_1=97.4% p_pass_2=92.0% **p_survive=74.5%** (was ~82.4% pre-fix); n_funded=1839 eligible=1272 incomplete=567; net_ev_monthly≈€428.
- `--csv results/f/F1_RSI2_swapcorr_daily.csv --paths 2000` → low fund rate / negative EV (expected unsized); n_funded=13 eligible=3 incomplete=10.
- Short-horizon unit check (horizon=60, live_months=12): all funded incomplete → p_survive=nan.

### 4) A4 path readiness (informational only — not a formal trial)

On shared box (U2 working tree / untracked prep, not committed here):
- `data/daily/{US500,US100,GER40}cash.csv` + `data/fomc_dates.csv` present (D1 path for A4 viable; series files extend past 2024 — **analysis must clip ≤2024-12-31**).
- `results/R2/a4_prep/cost_gate_c17_train.*` PRE-trial kostenpoort on train 2021–2023: **FAIL** (pooled median bruto ≈20.8 bp vs 3× median cost ≈45.1 bp). GER40 alone PASS; US500/US100 FAIL.
- Per PREREG: kostenpoort fail → STOP, no formal trial / no TRIALS append until rule/cost amendment.
- `data/m5/` still missing → A5 FX intradag remains blocked.
- Formal A4 trial ownership: Uitvoerder-2 after re-fetch of frozen windows; CTO owns engine + can co-run FTMO-EV once poort/rule path is clear.

### 5) Optional

- Stubbed `CTO_AUDIT.md` outline → next item = ORB/S3 audit via `PREREG_S3.md` / `RUNLOG.md`.

### Remaining blockers

1. U2 must re-fetch Strateeg `5fc3fb9` (or CTO PREREG copies) — window blocker obsolete.
2. A4 formal trial blocked on **kostenpoort FAIL** (train) unless Strateeg amends poort/rule or vehicle.
3. A5 blocked on missing `data/m5/`.
4. BESLUITEN.md on CEO branch still ends ~D-086; D-087…D-090 live in NEXT_STEPS v36 only.

## Wake cycle — 2026-09-30 22:32 Europe/Amsterdam (CET / UTC+2)

**Branch:** `grok/cto-1` (worktree `/workspace/ai-trading-cto`).  
**No reserve 2025-01→ opened. No TRIALS.csv writes. No formal PREREG trial claimed.**

### Team snapshot (read)

| Source | Takeaway |
|---|---|
| `origin/main` NEXT_STEPS **v38** | A4 STOP; B1 was prio 1 (PREREG groen); A2 parallel; A5 tot M5; A1 skip. |
| U2 `18c7996` (22:26) | `ftmo.py` re-validate PASS (censor blob); **B1 kostenpoort FAIL** → STOP; TRIAL_COUNT 444. |
| Strateeg | `PREREG_FTMO_B1` + `PREREG_FTMO_A2` frozen; C17 gestopt. |
| Strateeg-2 | S2 PREREGs + BTC_USOPEN; waiting post-B1/M5. |
| U-006 (main) | Ask M5 into repo (`data/m5gz/`); US41 spreads already on main. |

Merged `origin/main` (v38) into `grok/cto-1` this cycle.

### Work executed

1. **Informational FTMO-EV grid on published F2 ORB** (`results/f/F2_ORB_daily.csv`) via `engine/ftmo.py` — not a trial. Compliant scale (~max dip 4% → ×2.8) ≈ **€286/m** net EV; p95-dip≤2% scale ≈ **€40/m**. Old €484@5× is rule-size lottery. Artefact: `results/cto/orb_f2_ftmo_ev_grid.json`.
2. **`CTO_AUDIT.md`** — full ORB/S3 audit + overnight cost-gate pattern (A4+B1) + portfolio redirect to intradag.
3. **`VRAGEN_CTO.md` C-002** — B1 STOP; deprioritize overnight sleeves; A2/M5 next; endorse U-006 option A (+ US41 M5 for A2).

### Remaining blockers

1. A2/A5/S2-* need M5 (Debian or `data/m5gz/` via Sandro/U-006).
2. S3/A1 need `data/long_m1/` (no ping this cycle).
3. Manager NEXT_STEPS still lists B1 as prio 1 — superseded by U2 FAIL + C-002 (Manager bump next).

### Git

```
git add CTO_AUDIT.md VRAGEN_CTO.md RUNLOG_CTO.md results/cto/orb_f2_ftmo_ev_grid.json
git commit -m "CTO: ORB FTMO-EV audit + post-B1 intradag redirect (C-002)"
git push origin grok/cto-1
```
