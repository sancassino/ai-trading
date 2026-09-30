# STRATEGIE_NOTES_GROK — literature / prop research (Grok Strateeg)

Parallel notes file. Does **not** replace Claude `STRATEGIE_LOG.md` / `STRATEGIE_CATALOGUS.md`.  
Branch: `grok/strateeg-1`. Goal metric: **FTMO-EV** (€80k 2-Step). No fabricated citations.

---

## 2026-09-30 — Cycle 1 literature digest

### 1. ORB edge decay & microstructure

**TrueTrader (2026-08-18), “Opening Range Breakout: What 142,348 Trades Actually Show”**  
https://truetrader.net/opening-range-breakout

- Spec pinned: 5-min OR, stop at opposite edge, scale-out 0.5R/1.0R, EOD flat 15:49 ET, 104 liquid US stocks/ETFs, Jan 2020–Aug 2026.
- Conservative fills (next-bar open): PF **1.031**, **+0.011R**/trade, N=142,348. Level-fill assumption doubles apparent edge (~+0.023R); measured 1-sec fills ≈ +0.016R → **~29% of level-fill “edge” is fill fiction**.
- Structural fill tax: median slippage ~0; **95th pct ≈ +0.13R** — paid on the fastest (best) breaks. Momentum stop entries pay worst cost on best signals.
- Concentration: **longs PF 1.054 / +0.019R** vs shorts PF 1.009 / +0.003R; **gap-aligned** (gap>0.2% with breakout) PF 1.058 / +0.020R vs against-gap 1.017 / against-gap +0.006R; no-gap ~0.
- Index dilution: **SPY PF 0.94**, −0.023R — edge in single-name dispersion, not the basket average.
- Regime ≫ params: year PF span ~13 pts; 5/15/30-min OR variants ~3 pts. Day-of-week effects within noise.
- Repo mapping: our B4a ORB includes shorts + indices + EURUSD; day-t 1.81; cost wall 0.45–0.78 bp indices. **GS01** = test the TrueTrader cell on FTMO index CFDs (gap-aligned long-only), not stocks-in-play (S2 already STOP).

**Concretum Research (2026-07-08), “Improving the Opening Range Breakout on SPY”**  
https://concretumgroup.substack.com/p/improving-the-opening-range-breakout  
(Free teaser only; body paid — **not bypassed**.)

- Plain 5-min ORB SPY 2008–2025: net-of-fee returns mediocre (CAGR ~1%, Sharpe ~0.14 in teaser).
- Claim: selection filters + trade management + dynamic sizing lift CAGR/Sharpe/alpha without new ORB signal. **Details unpaid → do not implement claimed filters.** Directionally consistent with “filter, don’t invent.”

**Holmberg, Lönnbark, Lundström (Umeå), “Assessing the profitability of intraday opening range breakout strategies”**  
http://www.econ.umu.se/ueslpnr/ues845.pdf

- Daily OHLC bootstrap test on crude oil futures 1983–2011; ORB thresholds from normal-tail ρ.
- Full-sample positive; **subperiod split shows result driven by 2001–2011 (high vol)** — not time-robust.
- Explicit: ORB ≈ long-vol / expansion days (Crabel C–E). Aligns S9 economic story; our S9 diagnose already found vol does **not** cleanly explain FTMO ORB edge → decay/arbitration remains primary reading for 2024–26.

**Lundström et al. companion (diva-portal PDF indexed)**  
https://www.diva-portal.org/smash/get/diva2:732318/FULLTEXT02.pdf  
ORB returns increase across volatility states (~150–200 bp/day high vs low state in their futures sample). Useful mechanism paper; does not overturn S9 repo result.

**Crabel Substack century baseline (snippet)**  
https://tobycrabel.substack.com/p/opening-range-breakout-a-century  
0.8×10d-range stretch, hold to next open, 84 futures, ~1923–2025: Sharpe era decay (2000s ~2.92 → 2010s ~0.91); modern still positive but much smaller. Overnight hold → **swap-incompatible** as FTMO sleeve without swap accounting; use only as decay evidence.

### 2. FX London–NY overlap

**FXE Research RP-003 (2026-03-15)**  
https://fxeresearch.substack.com/p/session-volatility-in-fx-where-price

- 8 pairs, minute bars ~2005–2026; sessions fixed UTC (Asia 00–08, London 08–16, NY 13–21, overlap **13–16**).
- Peak hour 14:00 UTC ~27 pips avg range (~2.3× quietest); overlap 25.92 pips = 1.21× London-only.
- Pair heterogeneity: EURGBP London/Asia ~1.79×; AUDJPY ~1.02×.
- **Stability:** hourly profile corr **r=0.987** between 2005–09 and 2020–24 → structural liquidity geography, not a fading “anomaly edge.”
- Limitation stated by authors: **range ≠ spread**; no directional return claim.
- Repo: D1 already tested fixed London/NY windows on EURUSD (Breedon–Ranaldo seasonality). U3 London-open ORB cost FAIL. **Do not re-propose London-open ORB.** Overlap is an **execution / vol venue**, not GS-signal by itself.

**Blocked:** fxbacktest.app hourly study (Cloudflare); QuantifiedStrategies London breakout page (403).

### 3. Funded / prop public patterns (FTMO)

FTMO “Successful Trader Stories” are marketing case studies, not population inference. Extractable **compatible patterns** (examples):

| Story | Pattern notes |
|---|---|
| https://ftmo.com/en/blog/precise-risk-management-turned-gold-into-a-77249-profit-in-2-weeks/ | WR ~32%, RRR ~4.89, PF 2.30; mostly XAU long; sized so worst days stay under max daily loss; morning/early session entries |
| Sibling titles (search): shorts+high RRR gold; US500 with heavy DD control; scalpers on gold | Recurring: **asymmetric payoff + daily-loss discipline + liquid metals/indices** |

FTMO-compatible design checklist from these + rules:

- Prefer **intraday-flat** or swap-aware overnight.
- Positive skew / high RRR more important than high WR for challenge math.
- Size from **5% daily / 10% max DD**, not from “account label.”
- Avoid gambling-scale (D-016/D-085: no recommend scale >4% daily-loss risk).

### 4. Cost-aware intraday-flat design principles

- Taker short-horizon mean-reversion typically **dies at half-spread×2** (microstructure literature / practitioner HFT notes).
- ORB every-session participation maximizes cost exposure (Concretum + TrueTrader + our S0).
- Filters that cut N without raising expectancy are cosmetics (TrueTrader: buffer raises WR, not R).
- Useful overlays without new signal trials: hour-of-day spread from `COSTS_FTMO_per_uur.csv`; conservative stop-fill assumptions (already in `b4_sim` / G1G2 spirit).

### 5. Net-new proposals opened

| ID | File | One-liner |
|---|---|---|
| GS01 | `PREREG_GS01.md` / `VOORSTEL_GS01.md` | Gap-aligned **long-only** ORB on US500/US100/GER40(+XAU optional), EOD flat |
| GS02 | `PREREG_GS02.md` / `VOORSTEL_GS02.md` | Asian-range **fade** after failed London sweep (EURUSD/GBPUSD), EOD flat — cost gate first |

Deferred: high-RRR ORB exit rewrite; XAU-only prop clone (B4a XAU already weak); oil (RT 2.7–3.3 bp).

### CTO coordination note

- Score GS01 (if gate passes) with `engine/ftmo.py` alongside A1 ORB baseline; report fill-sensitivity.
- Treat Claude `PREREG_FTMO_FX_INTRADAG` as **U3-class**, not a third London-ORB trial, unless hypothesis is explicitly non-ORB (then prefer GS02).
