# RUNLOG_STRATEEG — Grok Strateeg (branch `grok/strateeg-1`)

## Kickoff — 2026-09-30 21:30 Europe/Amsterdam (CEST / UTC+2)

**Branch:** `grok/strateeg-1` from `main` @ `b071f4b` (NEXT_STEPS v35).  
**Repo:** `/workspace/ai-trading` (clone `sancassino/ai-trading`).  
**Role:** Grok Strateeg — primarily web research into professional/prop strategies that can improve the catalog and **FTMO-EV**; also read/write GitHub alongside CTO.  
**Scope this kickoff:** routine live + this log. No PREREG opened. No reserve 2025+. No real money/accounts. No secrets committed.

### Binding goal (from CTO kickoff + CEO D-083…D-086)

- FTMO prop **€80k 2-Step** only (not own capital). Ambition ≈ €800–900/m payout; €400–500 ok if robust.
- Metric = **FTMO-EV** (P pass1/2, P survive funded, €/m payout, fee/attempts, net EV). Module `engine/ftmo.py` on `grok/cto-1`.
- Vehicle `cfd` + FTMO costs/swaps; universe `SymbolList_FTMO.csv`.
- Reserve-run suspended (D-084). Pre-register before computing; append-only TRIALS.

### Routine

- **Name:** FTMO strateeg research  
- **Schedule:** `CRON_TZ=Europe/Amsterdam 8,38 * * * *` (every 30 min 24/7; stagger vs CTO :23/:53)  
- **Cadence intent:** wake → web research FTMO-compatible pro strategies (ORB decay, FX London/NY overlap, funded-trader reports, cost-aware intraday-flat) → cross-check `grok/strateeg-1` → write findings (STRATEGIE notes / this log) → PREREG before any new test proposal → message Sandro only on material results/blockers else stay quiet.

### Context skim (kickoff)

| Source | Takeaway |
|---|---|
| Claude Strateeg `STRATEGIE_LOG` / plan (branch `claude/trusting-faraday-34tsmg`) | Catalog + proposals S1–S11 path; ORB only daily-flat positive-skew survivor historically; costs are the wall; D-083 reframes goal back to FTMO-EV. |
| `COSTS_FTMO.csv` / `SymbolList_FTMO.csv` | Search space + cost wall for any new proposal. |
| `RUNLOG_CTO.md` (`grok/cto-1`) | `engine/ftmo.py` kickoff alive; next = wire sleeves → FTMO-EV. |
| `NEXT_STEPS.md` v35 on main | D-087/D-088 processed; eigen-kapitaal archived under `archief/eigen_kapitaal/`. |

### Next research cycle (not this commit)

1. Web pass: ORB decay literature, London/NY FX overlap, funded-trader public reports, intraday-flat cost-aware designs compatible with FTMO 5%/10% rules.  
2. Diff vs existing catalog / Claude Strateeg proposals — only net-new directions worth a PREREG.  
3. Coordinate with CTO on FTMO-EV scoring of any shortlist.  
4. First material finding → append here + optional STRATEGIE note; open `PREREG_*` only before a concrete test proposal.

### Git

```
git add RUNLOG_STRATEEG.md
git commit -m "Strateeg: init RUNLOG_STRATEEG.md on grok/strateeg-1"
git push -u origin grok/strateeg-1
```
