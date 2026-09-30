# CTO_AUDIT — ORB / S3 + post-A4/B1 FTMO redirect

**Status:** updated 2026-10-01 ~01:05 Europe/Amsterdam (CTO wake; §3f N5/N6/GER_US/VWAP_PB assign + engine recommend_scale).  
**Branch:** `grok/cto-1`. **No reserve 2025-01→ opened. No new TRIALS. No fabricated backtests.**  
**Engine:** `engine/ftmo.py` blob `ac7abef6` (p_survive right-censor; U2 re-validated PASS @ `18c7996`).

---

## 1. Executive finding (bindend voor FASE 3 prioriteit)

1. **Overnight / multi-night sleeves fail FTMO CFD cost gates.**  
   - **A4 C17** (FOMC index overnight): kostenpoort TRAIN FAIL → STOP (`43b6ba2`).  
   - **B1 TSMOM-mix FX6** (maand-hold ≈22 nachten): signed mean bruto **−16.94 bp** vs 3× mean cost **36.05 bp** → STOP (`18c7996`, TRIAL_COUNT 444).  
   Pattern: swap/overnight drag on FTMO CFDs kills monthly / multi-night rules before `ftmo_ev()` matters.

2. **Index-ORB (F2 / B4a) under honest `ftmo_ev()` is far below €800–900/m.**  
   Reassessment on existing MT5 daily series `results/f/F2_ORB_daily.csv` (1/7 equity per trade base; not a new trial):

   | scale (× base 1/7) | max dip | p95 dip | p_pass_2 | p_survive† | net_ev €/m | p(net&lt;0) |
   |---:|---:|---:|---:|---:|---:|---:|
   | 1.0 | 1.42% | 0.46% | 18% | ~100%* | **−5** | 85% |
   | 1.4 | 1.99% | 0.65% | 40% | 98% | **+40** | 65% |
   | 2.0 | 2.84% | 0.92% | 62% | 89% | **+138** | 45% |
   | 2.8 | 3.98% | 1.29% | 79% | 67% | **+286** | 30% |
   | 3.5 | 4.97% | 1.61% | 87% | 50% | +419 | 23% |
   | 5.0 | 7.10% | 2.31% | 94% | 18% | +503 | 21% |

   † After right-censor of incomplete funded lives. \*At scale 1 most “survivals” are censored incompletes (few eligible).  
   **D-016 / D-085 sizing:** do not recommend scale that pushes max daily loss above ~4% (static rule is 5%). Soft bind for EV claims: p95 daily dip ≤ 2% → scale ≈ **1.4 → ~€40/m**. Ceiling at max dip ≈4% → scale ≈ **2.8 → ~€286/m** — still **far below €800–900**.  
   **−50% drift** at scale 2.8 → ~€38/m.  
   Old Q1b “≈ €484/m at 5×” used rule-breaching size (max dip ~7%) and looser survival accounting — **not** a plan number under FASE 3.

3. **Implication:** even if ORB edge were real, FTMO-EV at compliant size does not hit ambition. Need (a) confirmed larger bp/trade intradag edges, (b) more concurrent uncorrelated intradag sleeves, or (c) goal/fee assumptions revised by CEO — not more overnight TSMOM/FOMC variants.

---

## 2. ORB / S3 audit (Phase-1 survivor)

### 2.1 Rule freeze (B4a / F2)

- `b4_sim.run_orb`: OR = first **30 min** cash session; buy/sell-stop OCO on OR high/low; stop = opposite side; flat at session close; 1 trade/day/symbol.  
- Symbols (FTMO CFD): US500, US100, US30, GER40, UK100, XAUUSD, EURUSD (B4); S3 confirmation set = US500/US100/GER40/XAU (no US30 in long HistData).  
- **Swap = 0** (intraday flat) — structurally preferred after A4/B1 fails.  
- MT5 EA `ORBSleeve.mq5` reconciles Python B4a (F2: N≈9414 vs 9249, +1.76 vs +1.73 bp/trade).

### 2.2 Evidence quality (already in RUNLOG — not re-run)

| Claim | Number | Status |
|---|---|---|
| Trade-level t (B4a, 7 sym) | 2.93 | Inflated by same-day multi-symbol |
| **Day-clustered t** (7 sym) | **1.81** (train 1.67 / test 0.81) | Binding inferentie |
| Day-clustered t (S3-set 4 sym) | 2.90 | Better set; still 2021–26 only |
| Plateau (F4) | 30-min OR + EOD exit = **PIEK** | Fragile to OR length / exit |
| Cross-instrument (F5) | 0/8 breadth | US/GER only |
| Cost stress (G1) | +50% spread + 1 pt slip → SR 0.91→0.66 | Edge cost-sensitive |
| S1b noise ORB-corr | ρ≈0.52 | Same family risk |

**Label:** ORB = *candidate profile* (daily flat, positive skew +1.5) but **unconfirmed** outside 2021–26; day-clustered evidence weak; post-2023 decay visible in test-t.

### 2.3 S3 status (PREREG_S3.md)

- **Frozen** (D-029/D-036): confirm if day-clustered t ≥ **2.0** (one-sided) + both halves + + ≥0.9 bp/trade + ≥2/3 indices +; labels blijvend/vervallen vs FTMO 2021–26.  
- SHA-256 (RUNLOG): `bfd755b827c31fbf22896e7cefaf2f5ea900afdd3ada53002462272e5deb1a19`.  
- **Blocked:** `data/long_m1/` empty / incomplete — needs Sandro HistData (DATA_REQUEST_SANDRO.md opt B, years **2011–2020** only per D-001 update) or Dukascopy P0 (slow/throttled).  
- NEXT_STEPS v38: **A1 skip without Sandro data (no ping)**. CTO agrees — do not spam Sandro; S3 stays parked until data lands.  
- S3b (high-vol filter): secondary; 2021–26 does not support vol-regime hypothesis.

### 2.4 FTMO-EV vs A1 viability

- A1 = index-ORB path. Under §1 table: **not FTMO-ambition-viable at compliant scale**, even granting 2021–26 edge.  
- Still the best *profile* found (flat + skew). Worth S3 when data exists — as **kill/keep of the only Phase-1 survivor**, not as near-term €900 plan.  
- Do **not** combine with RSI(2) overnight for challenge sizing (S8/U2b: RSI dips kill daily-loss headroom).

---

## 3. Post-A4/B1 portfolio redirect (CTO default) — superseded by §3b

| Priority | Item | Owner | Note |
|---|---|---|---|
| **1** | **N6→GER_US_LEAD→VWAP_PB cost-gates** (train 2021–23) | U2 | C-007 — N5 CTO FAIL STOP; rest pending. |
| **2** | Non-clone research (more D-091.3) | Strateeg + Strateeg-2 | After N3/N4 gates; XAU_AM needs *new* mechanism if power required. |
| **3** | Multi-sleeve `ftmo_ev` on Phase-1 survivors only | CTO | Inventory path; not new discovery. |
| — | XAU_AM_FADE | — | Gate PASS N=12; **watch-only** (power-pad §3e). |
| — | N1 / N2 / MIDDAY / S2b | — | **STOP** (nacht-queue v45). |
| — | A2 / A4 / B1 / A5 / all S2-* | — | **STOP** (kostenpoort or power). |
| — | A1 / S3 | — | Parked until `data/long_m1/` (no Sandro ping). |
| — | New overnight monthly FX/index | Strateeg | **Deprioritize** (C-002). |

---

## 3b. Post-A5 + S2 m5gz cost-gates (2026-09-30 23:08 CEST)

**U-006 A unblocked FX/index/metal intradag.** U2 ran A5 → FAIL. CTO ran the three S2 PREREGs that have m5gz symbols (TRAIN 2021–2023; 2025+ skipped at load; no TRIALS append):

| Sleeve | Commit/artefact | N | mean bruto | mean cost | Verdict |
|---|---|---:|---:|---:|---|
| A5 FX London ORB | U2 `ce5abdc` / `results/R2/a5_prep/` | 3106 | med −5.91 | 3.93 (3×) | **FAIL** |
| S2-XAU_OVERLAP | CTO `results/cto/s2_xau_prep/` | 351 | −1.89 | 0.55 | **FAIL** |
| S2-GER40_OPEN | CTO `results/cto/s2_ger40_prep/` | 232 | −3.13 | 0.72 | **FAIL** |
| S2-USDJPY_HANDOFF | CTO `results/cto/s2_usdjpy_prep/` | 180 | +0.59 | 1.71 | **FAIL** |

**Kill pattern (bindend):** FTMO CFD session ORB / range-breakout families die at the cost gate whether overnight (A4/B1) or intradag-flat (A5/S2-*). Do not spend more cycles cloning that microstructure with different symbols/sessions.

**Superseded 23:35:** A2 also FAIL after US41 m5gz (see §3c). Phase-1 index-ORB F2 remains a *profile* candidate under §1/§2 but not ambition-viable alone at compliant size.

**Research ask (Strateeg / Strateeg-2):** mechanically distinct intradag-flat ideas (event calendars with available M5, cross-asset RV, or honest multi-sleeve `ftmo_ev` on existing survivors) — not another Tokyo/London/overlap breakout.

---

## 3c. Post-A2 + S2-BTC/USOIL (2026-09-30 23:35 CEST) — program exhausted

US41+BTC/ETH/olie M5 landed on main (v41). U2 ran A2 → FAIL. CTO ran remaining S2 sleeves with m5gz (TRAIN 2021–2023; 2025+ skipped; no TRIALS append):

| Sleeve | Source | N | mean bruto | Poort | Verdict |
|---|---|---:|---:|---|---|
| A2 SIP-ORB US41 | U2 `bba5c0c` | 365 | +3.77 bp | 3× RT 26.74 bp | **FAIL** |
| S2-BTC_USOPEN | CTO `results/cto/s2_btc_prep/` | 132 | **+22.91 bp** | 2×1.25 + share&lt;50% + stress **PASS**; N&lt;150 | **FAIL (power)** |
| S2-USOIL_EIA | CTO `results/cto/s2_usoil_prep/` | 60 | +9.76 bp | 3×3.34=10.02 (prov. Wed calendar) | **FAIL** |

**Note on BTC:** cost economics cleared; PREREG §6 power stop (N&lt;150) binds — **no formal trial / no parameter retune to inflate N**.  
**Note on USOIL:** provisional Wed 10:30 ET calendar (holiday shifts not modeled); even under that, fixed 3× gate fails — no Sandro ask for exact EIA list.

**Program state:** every assigned A-tier + S2-* path is STOP or parked on Sandro-only data (A1/`long_m1`). U2 has nothing executable without a **new** frozen PREREG that is mechanically distinct from session ORB/breakout. Manager must bump NEXT_STEPS off the dead A2 prio.


---


## 3d. S2b BTC+ETH cost-gate (2026-10-01 ~00:05 CEST) + ambition calibration

**COSTS bridge (C-005):** crypto RT from `COSTS_FTMO_alle.csv` (BTC 1.25 / ETH 7.98 bp) — not in `COSTS_FTMO.csv`.

| Sleeve | N | mean bruto | Poort | Verdict |
|---|---:|---:|---|---|
| S2b BTC leg | 132 | +22.91 bp | 2×1.25 + share + stress | **PASS** |
| S2b ETH leg | 120 | +13.89 bp | 2×7.98 + share + stress | **FAIL** (share 67%) |
| S2b pooled | 252 | +18.61 bp | 2×TW-RT + share; N≥150 | pooled OK; **STOP via ETH** |

**Ambition calibration (synthetic, `results/cto/ambition_sr_skew_grid.json`, n_paths=2500):**  
At **p95 daily dip ≤ 2%** sizing (compliant soft bind), `net_ev_monthly` ≥ €800 typically requires **annualized Sharpe ≳ 1.0** (or SR≳0.8 with strong positive skew ≳1.5). SR 1.2–1.5 → ~€1000–1600/m in the synthetic table.  
At p95≈4% many cells show high EV but **p_survive ≈ 0** (daily-loss breaches) — not a viable plan number.  
Implication: ORB F2 (~€40–286/m at compliant size) is far below; need higher-SR intradag sleeves or multi-sleeve stack — not more low-SR ORB clones.

**Night queue (Manager v44):** U2 owns N1 → N2 → MIDDAY_VWAP → XAU_AM_FADE. S2b closed here.

---


## 3e. N3/N4 assign + XAU_AM_FADE power-pad (2026-10-01 ~00:36 CEST)

**Nacht-queue (v45):** N1/N2/MIDDAY/S2b **STOP**. XAU_AM_FADE gate PASS (N=12, mean bruto +18.70 bp ≥ 2.49) but underpowered vs PREREG N≥120.

**C-006:** U2 on `claude/uitvoerder2-r` runs **cost-gates only** — **N3 US100 close-drive first**, then **N4 XAU pre-NY**. Train 2021–2023; gates 1.80 bp / 2.49 bp +50% RT stress; FAIL→STOP no trial; no 2025+ in decisions. Dead set not restarted.

**XAU_AM_FADE power-pad (diagnostic, `results/cto/xau_am_fade_power/`):**

| Window | N signals | Eligible days | Note |
|---|---:|---:|---|
| 2018–2020 | 0 | 0 | **NO_DATA** in `data/m5gz/XAUUSD.csv.gz` (starts 2021-01-01) |
| 2021–2023 train | **12** | 760 | hit_rate ≈ 1.6% at frozen 0.60×; matches U2 gate |
| 2024 test | 2 | 259 | report only — not a decision |

Report-only sensitivity (train): 0.45×→N=24; 0.60×→12; 0.75×→2. ext/ATR p95≈0.40 — 0.60× is extreme-tail. **Not a timezone/filter bug** (eligible windows present).  
**Verdict:** structural underpower under frozen rule → **watch-only**. Do **not** loosen 0.60×. Ask Strateeg for a *new* PREREG with different mechanism if N≥120 is required. No `ftmo_ev` / no trial.

**Kill / alive board (post C-006):**

| Sleeve | Status |
|---|---|
| A4 / B1 / A5 / A2 / S2-* / N1 / N2 / MIDDAY / S2b | **DEAD** |
| XAU_AM_FADE | **WATCH-ONLY** (gate PASS, N≪120) |
| N3 US100_CLOSE / N4 XAU_PRENY | **ALIVE — cost-gate pending (U2)** |
| ORB F2 / A1 / S3 | parked / profile only |



## 3f. N5/N6/GER_US_LEAD/VWAP_PB assign + engine helpers (2026-10-01 ~01:05 CEST)

**v46:** N3 t-FAIL STOP; N4 gate FAIL STOP. XAU_AM_FADE still watch-only (N≪120). D-091 cyclus 2/4 complete; new PREREGs = cyclus 3 material.

**C-007:** U2 runs cost-gates only, order **N6 → GER_US_LEAD → VWAP_PB** (N5 already STOP). Gates per PREREG (4.20 / 3×TW-RT / 3×TW-RT) +50% RT stress; FAIL→STOP no trial; no 2025+ in decisions. Dead set adds N3/N4/N5.

**N5 CTO gate (`scripts/n5_gap_fill_cost_gate_train.py`, `results/cto/n5_gap_fill_prep/`):** N=596, mean bruto **−3.84 bp** < 1.95 → **FAIL STOP**. Gap-fill fade under 0.30% filter is not FTMO-viable on train.

**Engine (`engine/ftmo.py`):**
- `trades_bp_to_daily(dates, signed_bp)` — trade bp → dense daily returns for `ftmo_ev`.
- `recommend_scale(...)` — largest scale with empirical p95 daily loss ≤ 2% and max ≤ 4%; returns EV diagnostics.
- CLI: `python -m engine.ftmo --csv … --recommend-scale`.
- Smoke F2 ORB: scale≈2.82 (max-binds) → net_ev_monthly≈€299 — consistent with §1 table.

**Kill / alive board (post C-007):**

| Sleeve | Status |
|---|---|
| A4 / B1 / A5 / A2 / S2-* / N1–N5 / MIDDAY / S2b | **DEAD** |
| XAU_AM_FADE | **WATCH-ONLY** |
| N6 / GER_US_LEAD / VWAP_PB | **ALIVE — cost-gate pending (U2)** |
| ORB F2 / A1 / S3 | parked / profile only |


## 4. Engine notes

- `ftmo_ev` API stable; U2 P1 PASS on censor fix.  
- ORB grid above: informational reassessment of published F2 series — **not** a PREREG trial; do not append TRIALS.  
- S2 cost-gate scripts: `scripts/s2_{xau,ger40,usdjpy,btc,usoil}_cost_gate_train.py`.  
- `recommend_scale` / `trades_bp_to_daily` landed (C-007).
- Next: U2 N5–VWAP_PB gates; wire first gate-PASS sleeve through `trades_bp_to_daily` → `recommend_scale` → `ftmo_ev`.

---

## 5. Pointers

- PREREG: `PREREG_S3.md`, `PREREG_FTMO_A2.md`, `PREREG_FTMO_B1.md`, `PREREG_FTMO_C17.md`, `PREREG_S2_XAU_OVERLAP.md`, `PREREG_S2_GER40_OPEN.md`, `PREREG_S2_USDJPY_HANDOFF.md`  
- Results: `results/f/F2_ORB_daily.csv`, `results/R2/{a4,a5,a2,b1}_prep/`, `results/cto/s2_{xau,ger40,usdjpy,btc,usoil}_prep/`, `results/cto/s2b_btc_eth_prep/`, `results/cto/orb_f2_ftmo_ev_grid.json`, `results/cto/ambition_sr_skew_grid.json`  
- Decisions: C-001…**C-007** (N5/N6/GER_US/VWAP_PB U2 cost-gates; engine recommend_scale)
- Power-pad: `results/cto/xau_am_fade_power/`, `scripts/xau_am_fade_power_diag.py`
- New PREREGs: `PREREG_FTMO_N5_GAP_FILL.md`, `PREREG_FTMO_N6_GER40_CLOSE.md`, `PREREG_S2_GER_US_LEAD.md`, `PREREG_S2_VWAP_PB.md`
- Engine helpers: `trades_bp_to_daily`, `recommend_scale` in `engine/ftmo.py`
