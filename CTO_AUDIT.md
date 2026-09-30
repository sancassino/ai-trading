# CTO_AUDIT — ORB / S3 + post-A4/B1 FTMO redirect

**Status:** updated 2026-09-30 23:08 Europe/Amsterdam (CTO wake; §3b A5/S2 kills).  
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
| **1** | **A2** Stocks-in-Play ORB (earnings, EOD flat, swap=0) | Strateeg PREREG frozen; U2 when data | `PREREG_FTMO_A2.md` — needs US41 **M5** (~40 MB). Spreads on main. |
| **2** | **US41 M5gz** | Manager → Debian / U-006 extra | Only remaining A-tier with a live PREREG + clear data ask. |
| **3** | **Non-clone research** | Strateeg + Strateeg-2 | See C-003 / §3b — no new session ORB/breakout clones. |
| — | A4 / B1 / A5 | — | **STOP** (kostenpoort). |
| — | S2-XAU / GER40 / USDJPY | — | **STOP** (CTO cost-gate 2026-09-30 23:08). |
| — | S2-BTC / S2-USOIL | — | Parked — symbols absent from `data/m5gz/`. |
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

**Still open with positive option value:** A2 (equity SIP — different universe, earnings catalyst; blocked only on US41 M5). Phase-1 index-ORB F2 remains a *profile* candidate under §1/§2 but not ambition-viable alone at compliant size.

**Research ask (Strateeg / Strateeg-2):** mechanically distinct intradag-flat ideas (event calendars with available M5, cross-asset RV, or honest multi-sleeve `ftmo_ev` on existing survivors) — not another Tokyo/London/overlap breakout.

---

## 4. Engine notes

- `ftmo_ev` API stable; U2 P1 PASS on censor fix.  
- ORB grid above: informational reassessment of published F2 series — **not** a PREREG trial; do not append TRIALS.  
- S2 cost-gate scripts: `scripts/s2_{xau,ger40,usdjpy}_cost_gate_train.py` (m5gz loader pattern shared with U2 A5).  
- Next engine work (later wake): optional CLI `--scale-grid` + JSON emit for sleeve EV tables; not blocking while A2 data pending.

---

## 5. Pointers

- PREREG: `PREREG_S3.md`, `PREREG_FTMO_A2.md`, `PREREG_FTMO_B1.md`, `PREREG_FTMO_C17.md`, `PREREG_S2_XAU_OVERLAP.md`, `PREREG_S2_GER40_OPEN.md`, `PREREG_S2_USDJPY_HANDOFF.md`  
- Results: `results/f/F2_ORB_daily.csv`, `results/R2/{a4,a5,b1}_prep/`, `results/cto/s2_{xau,ger40,usdjpy}_prep/`, `results/cto/orb_f2_ftmo_ev_grid.json`  
- Decisions: `VRAGEN_CTO.md` C-001 (windows), C-002 (post-B1 + M5), **C-003** (post-A5 + S2 STOP + research redirect)
