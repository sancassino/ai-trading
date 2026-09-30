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

## Research cycle 1 — 2026-09-30 21:42 Europe/Amsterdam (CEST / UTC+2)

**Branch tip before:** `77f7266`. **Scope:** public-web research (ORB decay, FX London–NY overlap, funded-trader reports, cost-aware intraday-flat) + catalog diff vs Claude Strateeg. No backtests. No 2025+ reserve. No real money.

### Repo skim (read-only)

| Source | Takeaway |
|---|---|
| This log kickoff | Routine + FTMO-EV goal; next = this cycle. |
| `origin/claude/trusting-faraday-34tsmg` STRATEGIE_LOG / CATALOGUS / VOORSTEL_S8–S11 | ORB only daily-flat +skew survivor; S8 EV ≈ €150–300/m at allowed scale; S9 vol-regime does **not** explain edge; U3 London-open ORB FX cost-gate FAIL; S1 reject; S2 cost STOP; catalog §G intraday mostly T/dead; Claude already drafted `PREREG_FTMO_FX_INTRADAG` (London-open breakout A5) ≈ U3 duplicate risk. |
| `COSTS_FTMO.csv` | Indices RT 0.45–0.78 bp; FX majors 0.63–1.22; XAU 0.83. Cost wall for ORB bruto ≈ 2.5–3 bp. |
| `COSTS_FTMO_per_uur.csv` | Spreads tighter mid-US session; usable for session-cost overlays (not a new signal). |
| `NEXT_STEPS` v35 | D-087: Strateeg A4/A5 PREREG format; CTO wires sleeves → `ftmo_ev()`; reserve D-084 suspended. |
| `TRIAL_COUNT` | ≈ 440 (+ catalog runs). Append-only. |
| `origin/grok/cto-1` | `engine/ftmo.py` live @ `7148ab3`; next = sleeve wiring. |
| `BESLUITEN.md` | Not on `grok/strateeg-1` tip; D-083…D-088 content confirmed via NEXT_STEPS + CTO log (CEO branch). |

### Web sources fetched / searched (public only)

| URL / search | Status | Use |
|---|---|---|
| https://truetrader.net/opening-range-breakout | OK (full) | Primary ORB measurement study 2020–08/2026 |
| https://concretumgroup.substack.com/p/improving-the-opening-range-breakout | Partial (paid body) | Plain-vanilla ORB fails net-of-fees on SPY 2008–2025; filters claimed to help (paywalled details → not used) |
| http://www.econ.umu.se/ueslpnr/ues845.pdf | OK (Holmberg–Lönnbark–Lundström) | ORB profitability not robust across subperiods; high-vol period drives results |
| https://www.diva-portal.org/smash/get/diva2:732318/FULLTEXT02.pdf | Indexed (vol-state ORB) | ORB returns rise with vol states (oil / ES futures) — aligns S9 mechanism hypothesis (already tested: vol does **not** cleanly explain our edge) |
| https://tobycrabel.substack.com/p/opening-range-breakout-a-century | Snippet | Century futures ORB Sharpe decay (2000s 2.92 → 2010s 0.91); modern era still + but much smaller |
| https://fxeresearch.substack.com/p/session-volatility-in-fx-where-price | OK | LN–NY overlap peak vol; profile stable 2005–09 vs 2020–24 (r=0.987); **vol structure ≠ directional edge** |
| https://fxbacktest.app/research/forex-volatility-by-hour/ | **Blocked** (Cloudflare) | Hourly FX vol claim in SERP only; not used as citation |
| https://www.quantifiedstrategies.com/london-breakout-strategies/ | **403** | London/Asian breakout backtest page blocked; not bypassed |
| https://ftmo.com/en/blog/precise-risk-management-turned-gold-into-a-77249-profit-in-2-weeks/ | OK | Funded story pattern: WR≈32%, RRR≈4.9, XAU focus, size to daily loss |
| Related FTMO stories (search hits) | Titles/snippets | Recurrent: high RRR / low WR, gold, session timing; no aggregate strategy success rates published |

### Key takeaways

1. **ORB decay / cost wall (external):** TrueTrader: classic 5-min ORB on 104 US names 2020–08/2026 ≈ PF 1.03, +0.011R/trade (conservative fills); ~29¢/$ of published edge is fill assumption; **edge concentrates in long + gap-aligned**; shorts ≈0; SPY itself PF 0.94; regime year-gap ≫ parameter gap. Concretum teaser: plain SPY ORB net-of-fees mediocre. Holmberg et al.: oil ORB significance driven by high-vol subsample. Crabel century note: secular Sharpe decay. **Matches repo:** day-clustered t≈1.81; S8 €150–300/m; 2024–26 near cost wall.
2. **FX LN–NY overlap:** Strong **volatility / liquidity** regularity (FXE RP-003), not a free directional edge. D1 already tested Breedon–Ranaldo-style session seasonality on EURUSD. U3 London-open ORB cost-gate FAIL. Claude A5 PREREG ≈ same London-open family → treat as covered/redundant, not net-new.
3. **Funded-trader public reports:** FTMO publishes case studies, not population stats. Recurring compatible pattern: **positive skew via high RRR + hard daily-loss sizing**, liquid names (esp. XAU), session concentration. Compatible with ORB-like payoff if winners not capped too tightly; incompatible with high-frequency taker MR (spread death).
4. **Cost-aware intraday-flat:** Literature/practice: taker short-horizon MR dies at spread (HFT-book style); ORB near cost wall when traded every session; fill tax hits momentum stops hardest. Design implications: fewer, filtered trades; conservative fills; session-aware spreads from `COSTS_FTMO_per_uur.csv`.

### Catalog diff (vs Claude catalog + executed trials)

| Finding / angle | Verdict |
|---|---|
| Plain ORB decay / cost wall | **Already covered** (B4a/F2, S8, S9, RESULTATEN_GECLUSTERD) |
| Vol-regime ORB filter | **Already tested** (S9: vol does not explain) |
| London-open FX ORB / A5 | **Rejected / redundant** (U3 FAIL; Claude PREREG_FTMO_FX_INTRADAG ≈ duplicate) |
| D1 FX session seasonality | **Already tested** |
| Gap reversal / gap continuation first-hour | **Rejected** (B4c, J2/Q2 family) |
| Stocks-in-play ORB | **STOP** cost gate (S2) |
| Noise-area / ORB+RSI2 | **Rejected** (S1, Q7) |
| **Gap-aligned long-only ORB filter on index CFDs** (TrueTrader cell) | **NET-NEW** → `PREREG_GS01` + `VOORSTEL_GS01` |
| **Asian-range reclaim fade (FX), not London OR breakout** | **NET-NEW (cautious)** → `VOORSTEL_GS02` + `PREREG_GS02` (cost gate first; QuantifiedStrategies blocked) |
| High-RRR ORB exit rewrite (prop WR/RRR pattern) | **Deferred** — changes payoff vs frozen B4a; revisit only after GS01 cost/EV screen; gambling-scale risk |
| Session-hour cost overlay only | **Note** for CTO/Uitvoerder (not a trial) |

### PREREG opened this cycle?

**Yes:** `PREREG_GS01.md` (gap-aligned long-only ORB), `PREREG_GS02.md` (Asian-range fade FX). **No computation** until Manager/Uitvoerder schedules; proposals in `VOORSTEL_GS01.md` / `VOORSTEL_GS02.md`. Denser notes: `STRATEGIE_NOTES_GROK.md`. Claude `STRATEGIE_LOG.md` left untouched.


### Coordination with Strateeg-2 (`grok/strateeg-2` @ 7c844c2)

Strateeg-2 independently opened XAU overlap **breakout**, GER40 Frankfurt open-drive, USOIL EIA window — **distinct** from GS01 (gap-aligned index ORB) and GS02 (FX Asian-range **fade**). No merge conflict; Manager should FDR-count separately.

### Next actions

1. Manager/Uitvoerder: schedule **cost-gate-only** screen for GS01 (existing `B4_a_ORB_trades.csv` + overnight gap from M5) before full trial count; GS02 needs EURUSD(+GBPUSD) M5 Asian-range construction.
2. CTO (`grok/cto-1`): when wiring A1 ORB → `ftmo_ev()`, flag fill-conservatism + optional GS01 sleeve if cost gate passes; do **not** treat Claude A5 London FX as net-new vs U3.
3. Strateeg next cycle: if GS01/GS02 blocked or fail gate, search non-ORB intraday-flat (XAU session ORB already weak in B4a; oil costly) — stay quiet unless material.

### Blockers

- `fxbacktest.app` Cloudflare; QuantifiedStrategies 403; Concretum paid body — noted, not bypassed.
- `BESLUITEN.md` not on this branch tip (content via NEXT_STEPS/CTO log).
- No Sandro ping (research cycle complete; proposals only).
