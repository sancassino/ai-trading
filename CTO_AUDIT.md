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




## 3g. C-007 complete — N6/GER_US_LEAD/VWAP_PB FAIL (2026-10-01 ~01:28 CEST)

**Binding:** U2 `741639e` (AMS-wall m5gz). CTO parallel N6/GER also FAIL; do not use any non-AMS VWAP figure.

| Sleeve | N | mean bruto | gate | Uitkomst |
|---|---:|---:|---:|---|
| N6 GER40 Close | 251 | −2.05 bp | 4.20 bp | **FAIL STOP** |
| GER_US_LEAD | 314 | −1.43 bp | 2.16 bp | **FAIL STOP** |
| VWAP_PB | 179 | −2.68 bp | 1.64 bp | **FAIL STOP** |

No TRIALS append. D-091 cyclus **3/4** done without kostenpoort+power PASS.

**Kill / alive board (post C-008):**

| Sleeve | Status |
|---|---|
| A4 / B1 / A5 / A2 / S2-* / N1–N6 / MIDDAY / S2b / GER_US_LEAD / VWAP_PB | **DEAD** |
| XAU_AM_FADE | **WATCH-ONLY** (only prior gate-PASS; N≪120) |
| ORB F2 / A1 / S3 | parked / profile only (~€288–299/m at recommend_scale; ≪ €800–900) |

**Ops:** m5gz cost-gates use **Amsterdam wall clock** timestamps (U2 convention). Research redirect → Strateeg cyclus 4 (C-008). Artefact: `results/cto/c007_kill_board.json`.


## 4. Engine notes

- `ftmo_ev` API stable; U2 P1 PASS on censor fix.  
- ORB grid above: informational reassessment of published F2 series — **not** a PREREG trial; do not append TRIALS.  
- S2 cost-gate scripts: `scripts/s2_{xau,ger40,usdjpy,btc,usoil}_cost_gate_train.py`.  
- `recommend_scale` / `trades_bp_to_daily` landed (C-007).
- Next: D-092 pre-screen→PREREG only; S2c closed; Manager lands D-092 in NEXT_STEPS; optional Auditor on `engine/ftmo.py` + portfolio table.

---

## 5. Pointers

- PREREG: `PREREG_S3.md`, `PREREG_FTMO_A2.md`, `PREREG_FTMO_B1.md`, `PREREG_FTMO_C17.md`, `PREREG_S2_XAU_OVERLAP.md`, `PREREG_S2_GER40_OPEN.md`, `PREREG_S2_USDJPY_HANDOFF.md`  
- Results: `results/f/F2_ORB_daily.csv`, `results/R2/{a4,a5,a2,b1}_prep/`, `results/cto/s2_{xau,ger40,usdjpy,btc,usoil}_prep/`, `results/cto/s2b_btc_eth_prep/`, `results/cto/orb_f2_ftmo_ev_grid.json`, `results/cto/ambition_sr_skew_grid.json`  
- Decisions: C-001…**C-011** (LUNCH_OPEN FAIL_T; N9 underpowered / N10 FAIL; D-092.6 watch confirm)
- Power-pad: `results/cto/xau_am_fade_power/`, `scripts/xau_am_fade_power_diag.py`
- New PREREGs: `PREREG_FTMO_N5_GAP_FILL.md`, `PREREG_FTMO_N6_GER40_CLOSE.md`, `PREREG_S2_GER_US_LEAD.md`, `PREREG_S2_VWAP_PB.md`
- Engine helpers: `trades_bp_to_daily`, `recommend_scale` in `engine/ftmo.py`


## 3h. C-009 IB_FADE FAIL + D-092 portfolio / XAG pre-screen (2026-10-01 ~01:58 CEST)

**Escalatie:** D-091.6 = **4/4**. CEO **D-092** (`5348fd5` on `claude/ftmo-trading-strategy-98mplz`).

**IB_FADE (U2 `b8cf28a`):** N=42, mean bruto −3.54 bp < 1.62 → **FAIL STOP**. First cyclus-4 PREREG dead on arrival.

**D-092.3 F2-ORB reference (recommend_scale, trough DD, n_paths=5000):**

| Window | scale | p95 dip | max dip | p1·p2 | p_survive | €/m net EV | Role |
|---|---:|---:|---:|---:|---:|---:|---|
| 2021–2024 | 4.16 | 1.83% | 4.00% | 0.906 | 0.413 | **≈513** | **Binding reference** |
| 2021–2023 train | 4.16 | — | 4.00% | 0.942 | 0.433 | ≈683 | Train align |
| Full CSV→2026-09 | 2.82 | — | 4.00% | 0.726 | 0.665 | ≈288 | Diagnostic decay only (D-084: not for selection) |

**D-092.4 weak-sleeve portfolio (train 2021–23; vol-match to ORB daily std):**

| Blend | ann SR | €/m | p1·p2 | Note |
|---|---:|---:|---:|---|
| ORB alone | 1.06 | ≈683 | 0.94 | Reference edge |
| S2-BTC alone | 0.74 | ≈500 | 0.85 | Power-FAIL N=132 |
| XAU_AM_FADE alone | 0.66 | ≈7 | 0.07 | Watch-only N=12 |
| ORB+BTC eqvol | 1.21 | ≈1006 | 0.98 | Diversification real (ρ≈0.11) |
| ORB+BTC stress50 | 1.15 | ≈939 | 0.97 | BTC gross−1.5×cost |
| ORB+BTC+XAU eqvol | 1.31 | ≈393 | 0.76 | XAU dilutes €/m |

Artefacts: `results/cto/d092_portfolio_ev.{json,md}`, `scripts/d092_portfolio_ev.py`.

**D-092.1 XAG / S2c pre-screen:** XAG mean −21.57 bp < 15.21; pooled XAU+XAG −2.24 < 9.10 → **FAIL — no S2c PREREG**. `results/cto/d092_xag_prescreen/`.

**Kill / alive board (post C-009):**

| Sleeve | Status |
|---|---|
| A4 / B1 / A5 / A2 / S2-* / N1–N6 / MIDDAY / S2b / GER_US / VWAP_PB / **IB_FADE** / **S2c-shape** | **DEAD** |
| XAU_AM_FADE | **WATCH-ONLY** (alone; S2c rescue closed) |
| S2-BTC | power-FAIL watch (portfolio diversifier only — no solo trial) |
| ORB F2 | **reference** ≤2024 ≈€513/m (ambition band €300–500 ok per D-092.5) |

**Ops:** pre-screen before PREREG is now mandatory (D-092.1). No Sandro ping.

## 3i. C-010 N7/N8 XAU D-092.1 pre-screen FAIL (2026-10-01 ~02:35 CEST)

Strateeg `988cbde` filed `VOORSTEL_PRESCREEN_N7.md` (XAU Pre-London Range Breakout) and `N8.md` (XAU Post-AM-Fix Continuation). CTO ran free train-only screens (`scripts/n7_n8_xau_prescreen.py`):

| Idee | N | mean bruto | gate | Verdict |
|---|---:|---:|---:|---|
| N7 PLR BO | 684 | −1.18 bp | 2.49 | **FAIL — no PREREG** |
| N8 AM-Fix Cont | 204 | −1.47 bp | 2.49 | **FAIL — no PREREG** |

Both negative mean vs 3× RT. Distinct from earlier index N7/N8 FAILs (`2adb8ab`). U2 stays IDLE. XAU_AM_FADE remains sole watch-only gate-PASS. Artefacts: `results/cto/n7_n8_xau_prescreen/`.

## 3j. C-011 LUNCH_OPEN FAIL_T + N9/N10 pre-screen (2026-10-01 ~03:05 CEST)

**LUNCH_OPEN (U2 `2a4f28e`):** first post-D-092 PREREG to clear D-092.1 + cost-gate. Formal day-clust t train 1.14 / test 0.05 → **FAIL_T STOP**. TRIAL_COUNT 445. Dead set += LUNCH_OPEN.

**D-092.6:** Manager soft-call (v54) that cost-gate PASS (not formal PASS) resets 8-cyclus drought watch → **CTO confirms**. Watch **0/8**.

**N9 / N10 D-092.1** (`scripts/n9_n10_prescreen.py`, Strateeg `bbcd232`):

| Idee | N | mean bruto | gate | Verdict |
|---|---:|---:|---:|---|
| N9 GER40 Ochtend-Fade | 61 | +4.32 bp | 4.20 | mean-PASS; **N≪150 → NO PREREG** |
| N10 XAU Mid-London Fade | 182 | −0.82 bp | 2.49 | **FAIL — no PREREG** |

N9 mean is skew-fragile (median −11 bp). Precedent: UK_AM_FADE N=86 PASS → no PREREG (Strateeg-2 LUNCH §6).

**Kill / alive board (post C-011):**

| Sleeve | Status |
|---|---|
| A4 / B1 / A5 / A2 / S2-* / N1–N6 / MIDDAY / S2b / GER_US / VWAP_PB / IB_FADE / S2c / **LUNCH_OPEN** / N7–N8 / **N10** | **DEAD** |
| N9 GER40 ochtend-fade | underpowered mean-PASS — **no PREREG** |
| XAU_AM_FADE | **WATCH-ONLY** |
| S2-BTC | power-FAIL watch (portfolio diversifier only) |
| ORB F2 | **reference** ≤2024 ≈€513/m |

Artefacts: `results/cto/n9_n10_prescreen/`, `results/cto/c011_board.json`.

## 3k. C-012 N11 PASS (COSTS RT fix) + N12 FAIL (2026-10-01 ~03:40 CEST)

**Context:** After C-011, Strateeg filed N11 (GER40 XETRA ORB) + N12 (XAU NY-open continuation). U2 `2ac8e86` screened both FAIL vs VOORSTEL gates; TRIAL_COUNT 445 unchanged.

**GER40 RT correction:** `COSTS_FTMO.csv` GER40cash = **0.72 bp** RT → D-092.1 gate **2.16 bp**. The N6/N9/N11 "1.40→4.20" figure mis-cites that file. S2-GER40_OPEN already used 0.72. CTO binds GER40 intradag screens to COSTS RT.

| Idee | N | mean bruto | Binding gate | Verdict |
|---|---:|---:|---:|---|
| N11 GER40 XETRA ORB | 496 | +3.33 bp | 2.16 | **PASS_may_PREREG** |
| N12 XAU NY-Open Cont | 303 | +0.59 bp | 2.49 | **FAIL — no PREREG** |

N11 median −14 bp (skew-fragile). Strateeg → `PREREG_FTMO_N11` (gate 2.16); U2 cost-gate next. N9 still underpowered. Watch **0/8**. Artefacts: `results/cto/c012_board.json`, `results/cto/n11_n12_prescreen/`.

**Kill / alive board (post C-012):**

| Sleeve | Status |
|---|---|
| A4 / B1 / A5 / A2 / S2-* / N1–N6 / MIDDAY / S2b / GER_US / VWAP_PB / IB_FADE / S2c / LUNCH_OPEN / N7–N8 / N10 / **N12** | **DEAD** |
| N9 GER40 ochtend-fade | underpowered — **no PREREG** |
| **N11 GER40 XETRA ORB** | **PASS_may_PREREG** — awaiting Strateeg PREREG + U2 formal |
| XAU_AM_FADE | **WATCH-ONLY** |
| S2-BTC | power-FAIL watch (portfolio diversifier only) |
| ORB F2 | **reference** ≤2024 ≈€513/m |

## 3l. C-013 N11 FAIL_T + venue-ORB N15/N16/N17 FAIL (2026-10-01 ~04:15 CEST)

**N11 (U2 `d4cefff` / PREREG Strateeg `e8f261f`):** cost-gate PASS (mean +2.74 ≥ 2.16) → stress FAIL → formal day-clust t 0.92 → **FAIL_T STOP**. TRIAL_COUNT **446**. Dead set += N11. Median −14 / stop_share 0.52 — skew caveat from C-012 realized.

**N13/N14:** pre-screen FAIL (U2). **D-092.6:** CTO affirms cost-gate PASS resets watch → **0/8**.

**CTO venue-ORB exploration (free D-092.1):** UK100 / JP225 / US30 (+ US100/US500 companions) all **FAIL** on train 2021–23 under COSTS RT. Bars simple single-symbol ORB clones without new mechanism.

**Kill / alive board (post C-013):**

| Sleeve | Status |
|---|---|
| A4 / B1 / A5 / A2 / S2-* / N1–N14 / MIDDAY / LUNCH_OPEN / IB_FADE / S2c / **N11** / **N15–N17** | **DEAD / FAIL-pre-screen** |
| N9 GER40 ochtend-fade | underpowered — **no PREREG** |
| XAU_AM_FADE | **WATCH-ONLY** |
| S2-BTC | power-FAIL watch (portfolio diversifier only) |
| ORB F2 | **reference** ≤2024 ≈€513/m |

Artefacts: `results/cto/c013_board.json`, `results/cto/n11_prep/`, `results/cto/n15_n16_prescreen/`.

## 3m. C-014 N18 PASS + N19 FAIL; PREREG_N18 (2026-10-01 ~04:30 CEST)

**Trigger:** Strateeg `50561ab` non-ORB VOORSTEL N18/N19 after C-013 ORB family barred; U2 idle TRIAL_COUNT 446; main v59.

| Idee | N | mean bruto | median | gate | Uitkomst |
|------|---|------------|--------|------|----------|
| N18 US500 OVN Gap Cont | 279 | +3.52 | +2.77 | 2.34 | **PASS_may_PREREG** → `PREREG_FTMO_N18.md` |
| N19 XAU OVN Gap Fill | 228 | +2.03 | +2.42 | 2.49 | **FAIL** |

Train 2021–23 only; reserve 2025+ untouched. N18 year skew (2023 −12.17) + wide ATR-stop → report in U2 path; still honest D-092.1 PASS (N≥150, mean≥gate, median>0).

**Binding:** U2 executes N18 cost-gate next. N19 no PREREG. Watch 0/8 unchanged. No Sandro/CEO ask.



## 3n. C-015 N18 FAIL_T + D-093 freeze (2026-10-01 ~05:00 CEST)

**Trigger:** U2 completed N18 formal path; CEO issued D-093 freeze + EINDSTAND; Manager v61 missed D-093.

| Item | Uitkomst |
|------|----------|
| N18 US500 OVN Gap Cont | cost PASS / stress PASS / **FAIL_T** (t 0.64) — TRIAL **447** |
| D-093.1 watch reset | only full gate+stress+t — **8/8 frozen** (C-013 cost-gate reset superseded) |
| D-093.2 search | **frozen** — no new PREREG/pre-screen; maintenance 1×/4u |
| N20/N21 VOORSTEL | filed by Strateeg — **barred** until reopen |
| EINDSTAND | eval NIET kopen; reopen = HistData / other rules / stop |

Artefacts: `results/cto/c015_board.json`, `results/cto/n18_formal/`, `EINDSTAND_FTMO.md` (mirrored from CEO).

## 3o. C-018 D-094 tracks 3+5 combine + sizing (2026-10-01 ~08:15 CEST)

- **D-094/D-094a** freeze OFF; NEXT_STEPS **v63** absorbed; CTO owns combining (3) + FTMO sizing (5).
- Inventory: F2_ORB anchor; S2-BTC power-FAIL diversifier; XAU watch-only; N11/N18/LUNCH_OPEN FAIL_T → **portfolio diagnostics only** (no solo reopen).
- Artefacts: `scripts/c018_combine_ftmo.py`, `results/cto/c018_combine_ftmo.{json,md}`, `results/cto/c018_board.json`.
- Paper: ORB+BTC SR≈1.21 EV≈€1006/m; ORB60/BTC25/LUNCH15 SR≈1.36 EV≈€1188/m; WEAK5 diag SR≈1.62 surv≈0.91. ρ(ORB,LUNCH)≈−0.10.
- Track 5: recommend_scale vs survive tradeoff documented (lower scale → higher p_survive).
- Ensemble H-ENS-01…04 documented; N18 year-filter **REJECTED**. Reserve 2025+ untouched. No TRIALS append. No eval advice.
