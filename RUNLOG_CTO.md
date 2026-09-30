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
