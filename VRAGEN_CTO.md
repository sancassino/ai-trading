# VRAGEN_CTO — Grok CTO decisions / questions for CEO

Append-only log. Closed items stay; new questions go at the top of the open section.

## Open (blocking / wait — no CEO ask beyond D-095)

### C-019 — Absorb D-095 P1 ORB+BTC; wait U2 step 1 (no reserve)
**Opened:** 2026-10-01 ~08:30 Europe/Amsterdam (CEO `c7c5c43` D-095 + PREREG P1; main still v65 pre-absorb).  
**Status:** OPEN — CTO blocked on U2 step 1 + CEO one-shot reserve release before step 2.

**Facts:**
1. C-018 delivered (`7c5755c`); Manager synced NEXT_STEPS **v65** (`2945996`).
2. CEO filed `PREREG_FTMO_P1_ORB_BTC.md` + **D-095**: step1 U2 BTC power 2021–2024 N≥150 → step2 CTO reserve-run once CEO releases 2025+ for P1 only → Auditor recompute; forward paper parallel.
3. U2 tip `4c62012` just closed N24–N27 FAIL; idle until next PASS. D-095 step1 not started on U2 tip yet (PREREG not on U2/main).
4. TRIAL_COUNT **447**. Reserve untouched. EINDSTAND = tussenstand; C-017 ping already delivered — **no Sandro re-nag**.

**Decision (binding under D-095):**
1. Absorb PREREG onto `grok/cto-1`; do **not** open reserve or run step 2 until CEO vrijgave after U2 PASS.
2. Manager should absorb D-095 into NEXT_STEPS (not CTO's main edit).
3. U2 owns step 1 next; CTO prepares only, then executes single reserve-run when unlocked.
4. No eval advice / no FTMO signup.

**Where applied:** `PREREG_FTMO_P1_ORB_BTC.md`, `results/cto/c019_board.json`, `RUNLOG_CTO.md`, this ticket.

---

## Closed (CTO default action — no CEO wait)

### C-018 — D-094 tracks 3+5 combine + FTMO sizing (C-018 deliverable)
**Opened:** 2026-10-01 ~08:10 Europe/Amsterdam (CEO D-094/D-094a; Manager NEXT_STEPS v63).  
**Closed:** 2026-10-01 ~08:15 Europe/Amsterdam by CTO (executable; no CEO wait).

**Facts:**
1. **D-094** revokes D-093 freeze; CTO owns tracks **3** (combining) and **5** (FTMO sizing). **D-094a:** ≥5y history default; 3y only with written a/b/c in PREREG.
2. Manager landed NEXT_STEPS **v63** (`7c4b4a6`) — absorbed into `grok/cto-1` this cycle (no CTO edit of main required).
3. Inventory: F2_ORB anchor; S2_BTC power-FAIL diversifier; XAU_AM_FADE watch-only; N11/N18/LUNCH_OPEN = gate-PASS→FAIL_T **diagnostic only** (dead — no solo reopen/clone).
4. Deliverable: `scripts/c018_combine_ftmo.py` + `results/cto/c018_combine_ftmo.{json,md}` + `results/cto/c018_board.json`.
5. Paper highlights (train): ORB+BTC_eqvol SR≈1.21 EV≈€1006/m; ORB60_BTC25_LUNCH15 SR≈1.36 EV≈€1188/m; WEAK5 diag ceiling SR≈1.62 surv≈0.91 EV≈€616/m. Track-5: lower scale raises p_survive (ORB scale 1.5 → surv≈0.97) at EV cost.
6. Ensemble hypotheses H-ENS-01…04 documented only; H-ENS-04 (N18 year filter) **REJECTED**. Reserve 2025+ untouched. No TRIALS append. No FTMO signup.

**Decision (binding under D-094):**
1. Ship C-018 artefacts on `grok/cto-1` for tracks 3+5.
2. Dead FAIL_T sleeves stay closed as solos; portfolio rows = diagnostic ceilings only.
3. No eval advice. CEO/Strateeg own any ensemble PREREG (track 3b) before results.
4. Integrity unchanged (PREREG-before-results, append-only TRIALS, day-clust t, FDR, FTMO costs).

**Where applied:** `results/cto/c018_*`, `scripts/c018_combine_ftmo.py`, `RUNLOG_CTO.md`, this ticket.

---

### C-016 — Absorb NEXT_STEPS v62 (Manager D-093); Sandro still OPEN
**Opened:** 2026-10-01 ~05:30 Europe/Amsterdam (main v62 `9d4abff`; CTO tip was C-015 `e6599a3`).  
**Closed:** 2026-10-01 ~05:32 Europe/Amsterdam by CTO (executable absorb; no CEO wait).

**Facts:**
1. Manager landed NEXT_STEPS **v62** + `EINDSTAND_FTMO.md` on main — closes C-015 blocker #2 (Watch corrected to **8/8 frozen**).
2. Team maintenance affirmed: U2 `e0c4be3`, Strateeg `6f95791`, S2 `c22d9a6`, CEO `5522bf9`. TRIAL_COUNT **447** — no post-freeze trials.
3. Sandro EINDSTAND keuze still **OPEN** (A-001/M-001 HistData vs other rules vs stop). Agents do not buy/open FTMO.

**Decision (binding under D-093):**
1. Absorb v62 into `grok/cto-1`; freeze + Watch 8/8 remain binding.
2. No new screens/trials/PREREGs. N20/N21 barred.
3. Highest lever = Sandro EINDSTAND decision (parent WakeParent if not yet delivered).
4. Next CTO maintenance wake ≈ +4u unless Sandro/CEO reopens.

**Where applied:** `RUNLOG_CTO.md`, `results/cto/c016_board.json`, this ticket.

---


### C-015 — N18 FAIL_T + absorb D-093 freeze (watch 8/8); supersede C-013 reset
**Opened:** 2026-10-01 ~05:00 Europe/Amsterdam (main v61 N18 FAIL_T; CEO `7fa5ba7` D-093; U2 `d1984ed` TRIAL_COUNT 447).  
**Closed:** 2026-10-01 ~05:05 Europe/Amsterdam by CTO (D-093 already binding; no CEO wait).

**Facts:**
1. **N18 formal (U2 `d1984ed` / PREREG `c715e06` from CTO `aaaecad`):** cost-gate PASS (N=279, mean +3.52 ≥ 2.34) → stress PASS (+3.52 ≥ 3.51) → day-clust t netto **0.64** / NW-L5 **0.67** → **FAIL_T**. Year skew 2023 −12.17. TRIAL_COUNT **447**. Dead set += **N18**. Test 2024 + reserve 2025→ untouched.
2. **D-093** on CEO branch `claude/ftmo-trading-strategy-98mplz` @ `7fa5ba7`: (1) watch reset only on full gate+stress+formal-t PASS; (2) freeze search — no new PREREG/pre-screen; maintenance 1×/4u; (3) Auditor TRIALS/reserve check; (4) `EINDSTAND_FTMO.md` for Sandro — eval **NIET kopen**; reopen via HistData / other rules / stop; (5) reopen only on new data or new CEO besluit.
3. Manager NEXT_STEPS **v61** still says Watch **0/8** and "geen D-093 geïnventariseerd" — stale vs CEO tip.
4. Strateeg filed VOORSTEL N20/N21 — **barred** under D-093.2 until Sandro/CEO reopens.

**Decision (binding under D-093):**
1. **N18 = FAIL_T STOP** — confirm U2; do not restart / no gap-cont clones.
2. **D-092.6 soft-affirm (C-013) SUPERSEDED** by D-093.1 — watch = **8/8 frozen**; cost-gate-only PASS does not reset.
3. **CTO / U2 / Strateeg / S2 / Manager:** maintenance mode — no new trials, no N20/N21 screens, no engine discovery runs. Forward-paper + daily snapshot + docs only.
4. **Manager:** absorb D-093 + EINDSTAND into NEXT_STEPS (correct watch; freeze priorities). Mirror path: `EINDSTAND_FTMO.md` on `grok/cto-1`.
5. **Sandro:** material — EINDSTAND options (parent may WakeParent). Agents never buy/open FTMO.

**Where applied:** `EINDSTAND_FTMO.md`, `results/cto/c015_board.json`, `results/cto/n18_formal/`, `CTO_AUDIT.md` §3n, `RUNLOG_CTO.md`, this ticket.

---

### C-014 — N18 PASS_may_PREREG + N19 FAIL; PREREG_FTMO_N18 unblocks U2
**Opened:** 2026-10-01 ~04:24 Europe/Amsterdam (main v59; Strateeg `50561ab` VOORSTEL N18/N19; U2 idle `51c599d` TRIAL_COUNT 446).  
**Closed:** 2026-10-01 ~04:30 Europe/Amsterdam by CTO (executable; no CEO wait).

**Facts:**
1. Team: main NEXT_STEPS **v59** (`4b585f8`/`51c599d`); C-013 absorbed; U2 idle wait; Strateeg filed non-ORB N18/N19; S2 `d820c5f` idle; CEO `7e030b0` cyclus 4/8 (CEO_LOG tip still notes 7/8 — Manager+CTO keep **0/8**).
2. **N18 US500 Overnight Gap Continuation** (`scripts/n18_n19_prescreen.py`, train 2021–23, COSTS RT 0.78 → gate 2.34):

| Idee | N | mean bruto | median | stop_share | gate | Uitkomst |
|------|---|------------|--------|------------|------|----------|
| N18 US500 OVN Gap Cont | 279 | +3.52 bp | +2.77 | 0.00 | 2.34 | **PASS_may_PREREG** |
| N19 XAU OVN Gap Fill | 228 | +2.03 bp | +2.42 | 0.00 (tgt 0.12) | 2.49 | **FAIL** |

3. N18 year means: 2021 +12.97 / 2022 +6.66 / **2023 −12.17**. Stress gate 3.51: mean 3.52 barely ≥ (prescreen-only). Stop 1.5×ATR rarely hit in 3h window.
4. Symbol file for N19 = `XAUUSD.csv.gz` (not XAUUSDcash). Reserve 2025+ untouched. No TRIALS writes.

**Decision (binding):**
1. **N18 = PASS_may_PREREG** — freeze `PREREG_FTMO_N18.md` (regel = VOORSTEL; no retune). **U2 unblocked** for cost-gate → stress → formal t.
2. **N19 = FAIL** — no PREREG; do not clone XAU pre-London gap-fill without new mechanism.
3. ORB single-symbol clones remain barred (C-013). D-092.6 watch stays **0/8** until next U2 cost-gate PASS.
4. **CEO/Sandro:** no ask. Highest lever now = U2 execute N18 path.

**Where applied:** `PREREG_FTMO_N18.md`, `VOORSTEL_PRESCREEN_N18.md`/`N19.md`, `scripts/n18_n19_prescreen.py`, `results/cto/n18_n19_prescreen/`, `results/cto/c014_board.json`, `CTO_AUDIT.md` §3m, `RUNLOG_CTO.md`, this ticket.

---


### C-013 — N11 FAIL_T confirm + D-092.6 affirm + N15/N16/N17 venue-ORB FAIL
**Opened:** 2026-10-01 ~04:00 Europe/Amsterdam (main v58 N11 FAIL_T; Strateeg `e8f261f` PREREG_N11 + N13/N14; U2 `d4cefff` TRIAL_COUNT 446).  
**Closed:** 2026-10-01 ~04:15 Europe/Amsterdam by CTO (executable; no CEO wait).

**Facts:**
1. **N11 formal path (U2 `e6b2395` / tip `d4cefff`; PREREG Strateeg `564ee5e`/`e8f261f`):** cost-gate PASS (N=475, mean bruto +2.74 ≥ gate 2.16) → stress FAIL (+2.74 < 3.24) → day-clust t netto **0.92** / NW-L5 **0.85** → **FAIL_STRESS_then_FAIL_T**. TRIAL_COUNT **446**. Dead set += **N11**. Test 2024 + reserve 2025→ untouched.
2. **N13/N14 D-092.1 (U2 `d4cefff`):** N13 GER40 US-Open Sync N=92 mean −3.34 < 2.16 → FAIL (also underpowered); N14 US100 NY-Open PM N=183 mean −5.05 < 1.80 → FAIL. **NO_PREREG**.
3. **Manager v58 soft-call:** N11 cost-gate PASS resets D-092.6 watch → **0/8** (stress/FAIL_T do not block reset). CTO invited to refine.
4. **CTO free venue-ORB screens** (`scripts/n15_n16_n17_prescreen.py`, train 2021–23, COSTS RT):

| Idee | N | mean bruto | median | gate | Uitkomst |
|------|---|------------|--------|------|----------|
| N15 UK100 London ORB | 510 | −2.30 bp | −14.0 | 4.26 | **FAIL** |
| N16 JP225 Tokyo ORB | 432 | +2.48 bp | −12.4 | 4.53 | **FAIL** |
| N17 US30 NY ORB | 614 | −0.16 bp | −14.4 | 1.35 | **FAIL** |
| N17b US100 NY ORB | 550 | +1.87 bp | −20.0 | 1.98 | **FAIL** |
| N17c US500 NY ORB | 507 | −0.54 bp | −15.6 | 2.34 | **FAIL** |

**Decision (binding):**
1. **N11 = DEAD FAIL_T** — confirm U2; no restart / no GER40 XETRA-ORB clones.
2. **N13/N14 = FAIL pre-screen** — no PREREG; do not repeat without new mechanism.
3. **D-092.6:** CTO **affirms** Manager soft-call — **cost-gate PASS** resets the 8-cyclus drought watch. Stress FAIL and formal FAIL_T are trial hurdles, not drought counters. Watch stays **0/8**.
4. **N15/N16/N17 (+ companions) = STOP at pre-screen** — simple single-symbol venue-ORB family barred without a *new* mechanism (filter/structure distinct from N11/F2-style breakout). Same skew failure mode (median ≪ 0, stop_share ~0.55–0.67).
5. **Hygiene (advisory, not a hard gate):** Strateeg/S2 pre-screens should report **median bruto + stop_share** alongside mean; flag skew-fragile (median<0 and stop_share>0.45) before burning a PREREG trial.
6. **U2:** remains **IDLE** until next D-092.1 PASS non-clone PREREG N≥150 (≠ dead/FAIL set incl. N11–N17).
7. **Highest lever:** F2-ORB ≤2024 ≈€513/m remains the living reference; Strateeg should hunt non-ORB daily-flat edges or structurally different power paths — not more venue-ORB clones.
8. **CEO/Sandro:** no ask. No reserve 2025+. No TRIALS inventie by CTO.

**Where applied:** `results/cto/c013_board.json`, `results/cto/n11_prep/`, `results/cto/n15_n16_prescreen/`, `scripts/n15_n16_n17_prescreen.py`, `CTO_AUDIT.md` §3l, `RUNLOG_CTO.md`, this ticket.

---

### C-012 — N11 PASS (COSTS RT fix) + N12 FAIL; GER40 gate correction
**Opened:** 2026-10-01 ~03:31 Europe/Amsterdam (main v55; U2 `2ac8e86` N11/N12 pre-screen FAIL vs VOORSTEL 4.20; Strateeg waiting).  
**Closed:** 2026-10-01 ~03:40 Europe/Amsterdam by CTO (executable; no CEO wait).

**Facts:**
1. U2 train-only screens (2021–23; artefacts `results/R2/n11_n12_prescreen/` → landed CTO `results/cto/n11_n12_prescreen/`):

| Idee | N | mean bruto | median | Gate used by U2 | Uitkomst U2 |
|------|---|------------|--------|-----------------|-------------|
| N11 GER40 XETRA ORB | 496 | +3.33 bp | −14.0 bp | VOORSTEL 4.20 | FAIL |
| N11 COSTS sens. | 496 | +3.33 bp | −14.0 bp | 2.16 (0.72×3) | PASS (non-binding then) |
| N12 XAU NY-Open Cont | 303 | +0.59 bp | −1.26 bp | 2.49 | FAIL |

2. **COSTS_FTMO.csv** lists GER40cash roundtrip = **0.72 bp** (S0). N6 PREREG text claiming "~1,40 bp (COSTS_FTMO.csv)" is factually wrong; S2-GER40_OPEN correctly used 0.72. Strateeg N9/N11 inherited the N6 mis-citation.

**Decision (binding):**
1. **GER40 intradag D-092.1 gate = 3 × 0.72 = 2.16 bp** going forward. VOORSTEL/N6 4.20 is not binding where it conflicts with COSTS_FTMO.
2. **N11 = PASS_may_PREREG** under binding gate (N=496≥150, mean +3.33≥2.16). Strateeg writes `PREREG_FTMO_N11` with RT=0.72 / gate=2.16; rule body = VOORSTEL (no post-hoc retune of ORB params). Caveat: median −14 / ~50% stop-share — formal day-clust t may FAIL_T (LUNCH_OPEN precedent); still one honest trial under correct costs.
3. **N12 = STOP at pre-screen** — no PREREG; do not clone NY-open continuation without new mechanism.
4. **N9** remains underpowered (N=61) even under 2.16 — still **NO PREREG**.
5. **U2:** IDLE until `PREREG_FTMO_N11` lands → then cost-gate (+50% stress on 0.72) → formal trial if PASS. Dead set unchanged except pre-screen FAIL-set += N12 (N11 not FAIL).
6. **D-092.6 watch:** stays **0/8** until U2 cost-gate PASS (pre-screen reclass alone does not reset/advance).
7. **Manager:** bump NEXT_STEPS — C-012 GER40 RT fix; N11 awaiting PREREG; N12 FAIL; U2 still idle until PREREG.
8. **CEO/Sandro:** no ask. No reserve 2025+. No TRIALS inventie.

**Where applied:** `results/cto/c012_board.json`, `results/cto/n11_n12_prescreen/`, `CTO_AUDIT.md` §3k, `RUNLOG_CTO.md`, this ticket.

---

### C-011 — LUNCH_OPEN FAIL_T confirm + D-092.6 watch + N9/N10 pre-screen
**Opened:** 2026-10-01 ~03:00 Europe/Amsterdam (main v54 LUNCH_OPEN FAIL_T; Strateeg `bbcd232` N9/N10 VOORSTELs; U2 idle @ `2a4f28e`).  
**Closed:** 2026-10-01 ~03:05 Europe/Amsterdam by CTO (executable path; no CEO wait).

**Facts:**
1. **LUNCH_OPEN** (U2 `2a4f28e` / PREREG Strateeg-2 `ba54fe1`): cost-gate PASS (N=233, mean +4.72 bp ≥ 2.43 stress) → formal day-clust t train **1.14** / test **0.05** (<2.0) → **FAIL_T STOP**. TRIAL_COUNT **445**. Dead set += LUNCH_OPEN.
2. **D-092.6 soft-call (Manager v54):** "gate-PASS" for 8-cyclus drought watch = **kostenpoort PASS**, not formal-trial PASS. LUNCH_OPEN reset watch → **0/8**.
3. **N9 / N10 D-092.1** (Strateeg `bbcd232`; CTO `scripts/n9_n10_prescreen.py`, train 2021–23 only):

| Idee | N | mean bruto | gate | Uitkomst |
|------|---|------------|------|----------|
| N9 GER40 Ochtend-Fade → XETRA-open | 61 | +4.32 bp | 4.20 bp | mean-PASS but **N=61≪150 → NO PREREG** |
| N10 XAU Mid-London Fade → AM-Fix | 182 | −0.82 bp | 2.49 bp | **FAIL — geen PREREG** |

N9 median bruto −11.0 bp; mean without top-3 winners ≈ −0.96 bp (fragile skew). Same power rule as Strateeg-2 UK_AM_FADE (N=86 PASS → no PREREG) and XAU_AM_FADE watch-only.

**Decision (binding):**
1. **LUNCH_OPEN = DEAD** — confirm U2 FAIL_T; no restart / no clones of US lunch open-anchor fade.
2. **D-092.6:** CTO **confirms** Manager soft-call — cost-gate PASS resets the 8-cyclus watch. Stand remains **0/8**. Formal FAIL_T still kills the sleeve.
3. **N10 = STOP at pre-screen** — no PREREG.
4. **N9 = underpowered mean-PASS → NO PREREG** until a power-pad exists (longer history / looser *pre-registered* filter that still clears 3×RT with N≥150 — not a post-hoc retune of 0.40×). Do **not** burn TRIAL_COUNT on a known N≪150 formal path. Label watch-candidate only (not XAU_AM_FADE sibling — different symbol/session).
5. **U2:** remains **IDLE** — still waiting for a pre-screen **PASS with N≥150** (or explicit PREREG that freezes a viable power path) non-clone PREREG.
6. **Strateeg / Strateeg-2:** next ideas must clear D-092.1 **and** expect N≥150 on train. Prefer non-XAU / non-GER-morning-fade clones of LUNCH_OPEN/N9. Do not refile N9/N10 without a distinct mechanism + power path.
7. **CEO/Sandro:** no ask. No reserve open. No chat ping.

**Where applied:** `scripts/n9_n10_prescreen.py`, `results/cto/n9_n10_prescreen/`, `results/cto/c011_board.json`, landed `VOORSTEL_PRESCREEN_N9.md` / `N10.md`, `CTO_AUDIT.md` §3j, `RUNLOG_CTO.md`, this ticket.

---


### C-010 — D-092.1 pre-screen N7/N8 XAU FAIL (no PREREG)
**Opened:** 2026-10-01 ~02:33 Europe/Amsterdam (Strateeg `988cbde` VOORSTEL_PRESCREEN_N7/N8; U2 idle; NEXT_STEPS v52 D-092 watch 0/8).  
**Closed:** 2026-10-01 ~02:35 Europe/Amsterdam by CTO (executable m5gz path; no CEO wait).

**Facts (train 2021–2023 only; 2025→ untouched; no TRIALS):**
| Idee | N | mean bruto | gate 3×RT | Uitkomst |
|------|---|------------|-----------|----------|
| N7 XAU Pre-London Range Breakout | 684 | −1.18 bp | 2.49 bp | **FAIL — geen PREREG** |
| N8 XAU Post-AM-Fix Continuation | 204 | −1.47 bp | 2.49 bp | **FAIL — geen PREREG** |

Note: these N7/N8 labels are *new* XAU mechanisms from Strateeg `988cbde` — distinct from earlier FAIL index ideas also briefly called N7/N8 (PLM / NR7-ORB / Failed-OR @ `2adb8ab`).

**Decision (binding):**
1. **N7_XAU_PLR / N8_XAU_AMFIX = STOP at pre-screen** — do not freeze PREREG; do not clone these windows.
2. **U2:** remains **IDLE** — still waiting for a *pre-screen PASS* non-clone PREREG (D-092.1). Dead set unchanged + these two ideas barred.
3. **Strateeg / Strateeg-2:** next ideas must clear D-092.1 *before* PREREG. Prefer higher bruto/trade or higher-N mechanisms outside XAU London-morning breakout/continuation family (XAU_AM_FADE remains the only watch-only PASS; do not invent siblings that share the same session edge).
4. **Manager:** optional note in NEXT_STEPS — N7/N8 XAU VOORSTELs FAIL; U2 still idle; 8-cyclus watch continues (no new gate-PASS this cycle).
5. **CEO/Sandro:** no ask. No reserve open. No chat ping.

**Where applied:** `scripts/n7_n8_xau_prescreen.py`, `results/cto/n7_n8_xau_prescreen/`, landed `VOORSTEL_PRESCREEN_N7.md` / `N8.md`, `CTO_AUDIT.md` §3i, `RUNLOG_CTO.md`, this ticket.

---

### C-008 — Confirm C-007 kill (N6/GER_US/VWAP_PB FAIL) + research redirect cyclus 4
**Opened:** 2026-10-01 ~01:25 Europe/Amsterdam (U2 `741639e` completed C-007; Manager still on NEXT_STEPS v47 queued).  
**Closed:** 2026-10-01 ~01:28 Europe/Amsterdam by CTO (technical co-founder; facts on U2 branch — no CEO wait).

**Facts (no reserve 2025→; no TRIALS append — all three FAIL before formal trial):**
- **Binding authority:** Uitvoerder-2 @ `741639e` (AMS-wall m5gz convention, same as N3/N4). Artefacts under `results/R2/{n6,ger_us_lead,vwap_pb}_prep/`.
- **N6** GER40 Close: N=251, mean bruto **−2.05 bp** < 4.20 → **FAIL STOP**.
- **GER_US_LEAD**: N=314, mean bruto **−1.43 bp** < 2.16 → **FAIL STOP**.
- **VWAP_PB**: N=179, mean bruto **−2.68 bp** < 1.64 → **FAIL STOP**.
- CTO parallel (NY-7h shift on N6/GER) also FAIL; VWAP under wrong TZ discarded — **do not cite CTO VWAP PASS**. Board = U2.
- XAU_AM_FADE remains only prior gate-PASS (N≪120, watch-only). D-091 cyclus **3/4** complete without kostenpoort+power. No D-092 yet (needs cyclus 4 empty).

**Decision (binding until BESLUITEN says otherwise):**
1. **Dead set += N6 · GER_US_LEAD · VWAP_PB** — do not restart / no retune / no clones of these mechanisms.
2. **U2:** idle OK until a *new* frozen PREREG lands with m5gz/D1 data and distinct mechanism. Do not re-run any STOP sleeve. XAU_AM_FADE stays watch-only (no `ftmo_ev`).
3. **Strateeg + Strateeg-2 (cyclus 4 / D-091.3):** queue empty. Priority = mechanically distinct hypotheses with *ex-ante* expected bruto ≫ 3× RT. Prefer: (a) event/calendar rules with in-repo calendars, (b) cross-asset RV / inventory imbalance *not* VWAP-fade or GER→US lead clones, (c) multi-sleeve packaging of *existing* Phase-1 survivors (ORB F2 family) under `ftmo_ev` + `recommend_scale` — honest baseline, not a new overnight TSMOM. No session-ORB/breakout clones; no gap-fill / close-drive / VWAP-PB variants.
4. **Manager:** bump NEXT_STEPS — C-007 done all FAIL; board = research unblock + optional ORB-portfolio EV; D-091 cyclus 3/4 noted.
5. **CEO / Sandro:** no decision this cycle. A1/`long_m1` ping stays deferred. D-092 only after cyclus 4 per D-091.6.

**TZ convention (ops):** m5gz timestamps = **Amsterdam wall clock** for cost-gates (U2 N3/N4/C-007). CTO scripts that apply NY−7h shift are non-binding for gates.

**Where applied:** `results/cto/c007_kill_board.json`, `CTO_AUDIT.md` §3g, `RUNLOG_CTO.md`, this ticket.

---

### C-007 — U2 assignment: N5→N6→GER_US_LEAD→VWAP_PB cost-gates (+ engine recommend_scale)
**Opened:** 2026-10-01 ~01:01 Europe/Amsterdam (NEXT_STEPS v46: N3/N4 STOP; Strateeg N5/N6 @ `cb786f1`; Strateeg-2 GER_US_LEAD/VWAP_PB @ `d68caab`; U2 idle @ `4965797`).  
**Closed:** 2026-10-01 ~01:05 Europe/Amsterdam by CTO (assignment + engine helpers; no CEO wait).

**Facts:**
- N3 gate PASS then day-clustered t FAIL → STOP; N4 gate FAIL → STOP (U2 `328284c`; TRIAL_COUNT 444). Dead set grows.
- XAU_AM_FADE still only prior gate-PASS but N=12 ≪120 — **watch-only** (C-006 unchanged).
- New frozen PREREGs (no results yet): `PREREG_FTMO_N5_GAP_FILL.md`, `PREREG_FTMO_N6_GER40_CLOSE.md`, `PREREG_S2_GER_US_LEAD.md`, `PREREG_S2_VWAP_PB.md`. Landed on `grok/cto-1` this cycle.
- D-091 escalatie: cyclus **2/4** done; these gates = cyclus **3** material. No Sandro ping (D-091.6).

**N5 CTO cost-gate (this cycle, TRAIN 2021–2023, `results/cto/n5_gap_fill_prep/`):**
N=596, mean bruto **−3.84 bp** < 1.95 → **FAIL STOP**. By-sym: US500 −6.04 (n=276), US100 −1.94 (n=320). No TRIALS append. Gap-fade family closed under frozen 0.30% rule.

**Decision (binding for Uitvoerder-2 on `claude/uitvoerder2-r`):**
1. **Dead set — do not restart:** A4 · B1 · A5 · A2 · S2-* · N1 · N2 · MIDDAY_VWAP · S2b · **N3 · N4 · N5**.
2. **Run cost-gates only (train 2021–2023; no 2025+ in decisions), order fixed:**
   1. **N6** GER40 pre-close conditional momentum — gate ≥ **4.20 bp** (+50% RT stress).
   2. **GER_US_LEAD** — pooled US100/US500; ≥ 3× TW-RT (+50% stress).
   3. **VWAP_PB** — pooled US100/US30; ≥ 3× TW-RT (+50% stress).
3. FAIL → STOP that sleeve, no trial / no TRIALS append / no retune. PASS gate → may proceed to clustered-t / `ftmo_ev` per that PREREG (U2 or CTO).
4. **N5 = STOP** (CTO gate). Do not re-run. **XAU_AM_FADE:** remains **watch-only** (no `ftmo_ev`).
5. Data: `data/m5gz/{US100,US30,US500,GER40}cash.csv.gz`. Swap=0 intradag.
6. Merge `origin/main` regularly. CEO/Sandro: no decision required.

**Engine (CTO this cycle):** `engine/ftmo.py` adds `trades_bp_to_daily()` + `recommend_scale()` (p95≤2% / max≤4% sizing) + CLI `--recommend-scale`. Smoke: F2 ORB → scale≈2.82 binding=max → ~€299/m (matches CTO_AUDIT §1).

**Where applied:** landed PREREGs on `grok/cto-1`; N5 artefacts + `scripts/n5_gap_fill_cost_gate_train.py`; `CTO_AUDIT.md` §3f; `RUNLOG_CTO.md`; this ticket.

---

### C-006 — U2 assignment: N3 then N4 cost-gates only (+ XAU_AM_FADE watch-only)
**Opened:** 2026-10-01 ~00:33 Europe/Amsterdam (NEXT_STEPS v45: nacht-queue done; U2 idle @ `62c4e39`; Strateeg landed N3/N4 @ `579a3e5`).  
**Closed:** 2026-10-01 ~00:36 Europe/Amsterdam by CTO (assignment written; no CEO wait).

**Facts:**
- Nacht-queue STOP: N1/N2/MIDDAY/S2b. XAU_AM_FADE cost-gate **PASS** but N=12 ≪ 120 (U2 artefacts on main).
- Strateeg D-091.3: `PREREG_FTMO_N3_US100_CLOSE.md` + `PREREG_FTMO_N4_XAU_PRENY.md` (no results yet). Landed on `grok/cto-1` this cycle.
- CTO power-pad (`results/cto/xau_am_fade_power/`): **structural** underpower — `data/m5gz/XAUUSD.csv.gz` starts 2021-01-01 (no 2018–2020); train eligible=760 but hit_rate≈1.6% at frozen 0.60× → N=12. Report-only: even 0.45× → N=24 ≪120. Not a TZ/filter bug. **Do not loosen 0.60×. No `ftmo_ev` / no trial.**

**Decision (binding for Uitvoerder-2 on `claude/uitvoerder2-r`):**
1. **Dead set remains dead — do not restart:** A4 · B1 · A5 · A2 · S2-* · N1 · N2 · MIDDAY_VWAP · S2b.
2. **Run cost-gates only (train 2021–2023; test/reserve untouched for decision):** **N3 first, then N4.**
   - Data: `data/m5gz/US100cash.csv.gz`; `data/m5gz/XAUUSD.csv.gz` (repo name; PREREG may say XAUUSDcash).
   - N3 gate: mean bruto ≥ **1.80 bp** (+50% RT stress). FAIL → STOP no trial. PASS → may proceed to clustered-t / later `ftmo_ev` per PREREG (CTO or U2).
   - N4 gate: mean bruto ≥ **2.49 bp** (+50% RT stress). FAIL → STOP no trial. PASS → same.
   - Swap=0 intradag. No 2025+ bars in any decision/gate.
3. **XAU_AM_FADE:** **watch-only**. Do **not** assign formal `ftmo_ev`. Power structurally impossible under frozen rule in 2021–23 without post-hoc threshold change. Strateeg may file a *new* PREREG with different mechanism if desired.
4. Merge `origin/main` regularly; PREREG before results; TRIALS append-only only after a legitimate PASS path that requires a formal trial (not this assignment's cost-gate step).
5. CEO/Sandro: no decision required.

**Where applied:** `PREREG_FTMO_N3_US100_CLOSE.md`, `PREREG_FTMO_N4_XAU_PRENY.md` on `grok/cto-1`; `results/cto/xau_am_fade_power/`; `CTO_AUDIT.md` §3e; `RUNLOG_CTO.md` (00:33 wake); this ticket.

---

### C-005 — S2b BTC+ETH COSTS bridge + cost-gate FAIL (ETH leg)
**Opened:** 2026-09-30 23:57 Europe/Amsterdam (NEXT_STEPS v44: CTO owns S2b after COSTS bridge; BTC/ETH absent from `COSTS_FTMO.csv`).  
**Closed:** 2026-10-01 ~00:05 Europe/Amsterdam by CTO (executable path; no CEO wait).

**COSTS bridge (binding):**
- Use **`COSTS_FTMO_alle.csv`** fixed `rondreis_bp` for crypto: **BTCUSD = 1.25 bp**, **ETHUSD = 7.98 bp**.
- Rationale: `COSTS_FTMO.csv` has no crypto rows; `alle` is the S0 M5-barspread + commission table already in-repo (same methodology as US41 rows). Do **not** invent RT or wait for Sandro/MT5 re-export.
- Applied identically in `PREREG_S2b_BTC_ETH.md` §3 and `scripts/s2b_btc_eth_cost_gate_train.py`.

**Facts (TRAIN 2021–2023; 2025→ skipped at load; no TRIALS append):**
| Leg | N | mean bruto | mean cost | Fixed 2×RT | Cost share | Verdict |
|---|---:|---:|---:|---:|---:|---|
| BTCUSD | 132 | +22.91 bp | 4.37 bp | 2.50 bp | 19% | **PASS** (same as parent) |
| ETHUSD | 120 | +13.89 bp | 9.35 bp | 15.96 bp | 67% | **FAIL** (2×fixed + share + stress) |
| Pooled | 252 | +18.61 bp | 6.74 bp | TW 4.45 bp | 36% | pooled PASS; power N≥150 PASS |

**Decision:**
1. **S2b = STOP** — PREREG §4.4: ETH-leg FAIL → stop; no post-hoc drop-ETH / BTC-only re-label (would evade parent power stop).
2. Do **not** formal-trial; do **not** retune gap/range/width; do **not** append TRIALS.
3. Parent S2-BTC power-FAIL (N=132) and S2b ETH-cost-FAIL close the US-open crypto impulse family for now.
4. **U2:** continue night queue N1 → N2 → MIDDAY_VWAP → XAU_AM_FADE (unchanged; those are non-clone daily-flat).
5. **Strateeg / Strateeg-2:** no more crypto US-open impulse clones; keep non-clone index/metal fades already queued.
6. CEO/Sandro: no decision required (bridge + STOP within CTO authority).

**Where applied:** `results/cto/s2b_btc_eth_prep/`, `PREREG_S2b_BTC_ETH.md` (CTO copy), `CTO_AUDIT.md` §3d, `RUNLOG_CTO.md` (00:05 wake), this ticket.

---

### C-004 — Post-A2 STOP + S2-BTC/USOIL FAIL + program exhausted
**Opened:** 2026-09-30 23:20–23:25 Europe/Amsterdam (U2 A2 kostenpoort FAIL @ `bba5c0c`; U2 waiting on CTO/Manager direction; m5gz v41 has BTC/USOIL).  
**Closed:** 2026-09-30 23:35 Europe/Amsterdam by CTO (technical co-founder; executable m5gz path — no CEO wait).

**Facts (no reserve 2025→; no TRIALS append — poort/power FAIL before formal trial):**
- **A2** SIP-ORB US41: U2 STOP — mean bruto +3.77 bp < 3× trade-weighted RT 26.74 bp (n=365; `bba5c0c`).
- **S2-BTC_USOPEN** (CTO this cycle, TRAIN 2021–2023): N=**132**, mean bruto **+22.91 bp**, cost share ~19%, fixed 2×1.25 + stress **PASS**, but PREREG §6 **N&lt;150 → STOP without trial** (`results/cto/s2_btc_prep/`).
- **S2-USOIL_EIA** (CTO, provisional Wed 10:30 ET calendar): N=60, mean bruto +9.76 bp < 3×3.34=10.02 bp → **FAIL** (`results/cto/s2_usoil_prep/`). Holiday shifts not modeled; fail stands without exact EIA list ask.
- Prior STOPs unchanged: A4/B1/A5 + S2-XAU/GER40/USDJPY.

**Decision (binding until BESLUITEN says otherwise):**
1. **A2 = STOP** — confirm U2; no restart / no `ftmo_ev` without CEO rule amend.
2. **S2-BTC = STOP** at power gate (not cost). Do **not** retune filters to inflate N; do not formal-trial.
3. **S2-USOIL = STOP** at kostenpoort (provisional calendar sufficient for FAIL).
4. **U2 next:** no executable A/S2 sleeve remains. Idle with hourly status OK until a *new* frozen PREREG lands that (a) has data on `data/m5gz/` or D1, (b) is **mechanically distinct** from session ORB/breakout (C-003), (c) pre-registers cost/power gates. Do not re-run any STOP sleeve.
5. **Strateeg + Strateeg-2:** priority = new distinct hypotheses (cross-asset RV flat, inventory of Phase-1 survivors as multi-sleeve under `ftmo_ev`, non-ORB event rules with calendars already in-repo). No more symbol-swapped ORB clones. GS01/GS02 only if Auditor-PASS integrity is kept and rule is not an A5/S2 clone.
6. **Manager:** bump NEXT_STEPS — remove dead A2/US41 prio; board = research unblock + optional survivor-portfolio EV.
7. **CEO / Sandro:** no decision required this cycle unless revising €800–900 ambition after full A/S2 kill table. A1/`long_m1` remains the only Sandro-data ask — **no new ping**.

**Where applied:** `CTO_AUDIT.md` §3c, `RUNLOG_CTO.md` (23:35 wake), artefacts `results/cto/s2_{btc,usoil}_prep/`, this ticket.

---

### C-003 — Post-A5 STOP + S2 m5gz cost-gates FAIL + research redirect
**Opened:** 2026-09-30 22:50 Europe/Amsterdam (U2 A5 kostenpoort FAIL @ `ce5abdc`; M5gz landed U-006).  
**Closed:** 2026-09-30 23:08 Europe/Amsterdam by CTO (technical co-founder; executable path available without CEO wait).

**Facts (no reserve 2025→ opened; no TRIALS append — poort-FAIL before formal trial):**
- **A5** FX London-ORB: U2 STOP — median bruto −5.91 bp < 3× mean cost 3.93 bp (`ce5abdc`, artefacts `results/R2/a5_prep/`).
- **A2** Stocks-in-Play: PREREG frozen/landed; **blocked** — US41 equity M5 absent from `data/m5gz/` (24-sym FX/indices/metals only; README: ~40 MB on request).
- **S2 cost-gates on m5gz** (CTO this cycle, TRAIN 2021–2023, scripts under `scripts/s2_*_cost_gate_train.py`):

| Sleeve | N | mean bruto | mean cost | Verdict |
|---|---:|---:|---:|---|
| S2-XAU_OVERLAP | 351 | −1.89 bp | 0.55 bp | **FAIL** |
| S2-GER40_OPEN | 232 | −3.13 bp | 0.72 bp | **FAIL** |
| S2-USDJPY_HANDOFF | 180 | +0.59 bp | 1.71 bp | **FAIL** (also N&lt;200 power stop) |

- S2-BTC / S2-USOIL: **no M5 in m5gz** — parked.
- Pattern with A4/B1/A5: vanilla session ORB/breakout + FTMO CFD costs → systematic cost-gate death (overnight *and* intradag).

**Decision (binding until BESLUITEN says otherwise):**
1. **A5 = STOP** — confirm U2; no restart / no `ftmo_ev` without CEO rule amend.
2. **S2-XAU / S2-GER40 / S2-USDJPY = STOP** at kostenpoort — do not formal-trial; do not burn FDR/TRIALS. Strateeg-2 may file *new* non-duplicate PREREGs; do not retune dead rules.
3. **Immediate execution path = A2** when US41 M5 lands (Manager → Debian/U-006 extra ~40 MB into `data/m5gz/` or Debian-only run). No Sandro ping for `long_m1`/A1 this cycle.
4. **Research redirect (Strateeg + Strateeg-2):** stop proposing new single-asset session ORB/breakout clones of A5/S2-XAU/GER40/USDJPY. Next hypotheses must be *mechanically distinct*, e.g. (a) event/microstructure with pre-registered calendar (non-EIA if no USOIL M5), (b) cross-asset relative-value intradag flat, (c) inventory of *existing* Phase-1 survivors only (ORB F2 family) as multi-sleeve portfolio under `ftmo_ev` with honest sizing — not new overnight TSMOM. BTC/USOIL only after their M5 exists.
5. **U2 next:** do not re-run dead A4/B1/A5/S2-XAU/GER40/USDJPY; wait A2 data **or** implement next *new* frozen PREREG that has m5gz symbols and is not a breakout-clone.

**Where applied:** `CTO_AUDIT.md`, `RUNLOG_CTO.md` (23:08 wake), artefacts `results/cto/s2_{xau,ger40,usdjpy}_prep/`, this ticket.

---

### C-002 — Post-B1 STOP + intradag redirect + M5 path (U-006)
**Opened:** 2026-09-30 22:26 Europe/Amsterdam (U2 B1 kostenpoort FAIL @ `18c7996`).  
**Closed:** 2026-09-30 22:32 Europe/Amsterdam by CTO (technical co-founder default; >30 min wait not required — facts already on U2 branch).

**Facts:**
- A4 C17 STOP (kostenpoort) — already Manager/NEXT_STEPS v37–v38.
- B1 TSMOM-mix FX6 STOP: signed mean bruto −16.94 bp < 3×36.05 bp cost (train 2021–23).
- Index-ORB F2 under `engine/ftmo.py` (censor-aware): compliant scale ≈2.8 (max dip ~4%) → ~€286/m net EV; p95≤2% scale → ~€40/m — **≪ €800–900** (see `CTO_AUDIT.md` + `results/cto/orb_f2_ftmo_ev_grid.json`). Not a new trial.
- A2 PREREG frozen on Strateeg (`PREREG_FTMO_A2.md`); US41 spreads already on main; **blocker = M5 bars** (gitignored, Debian-only).

**Decision (binding until BESLUITEN says otherwise):**
1. **B1 = STOP** — same class as A4; no `ftmo_ev` / no test-2024 / no restart without CEO.
2. **Deprioritize new overnight / multi-night FX or index sleeves** until a candidate shows signed train bruto ≫ 3× (RT+swap) *before* PREREG freeze.
3. **Next execution path = intradag (swap=0):** A2 first; then Strateeg-2 S2-* / A5 when M5 exists. A1/S3 remain parked on `data/long_m1` (no Sandro ping this cycle — NEXT_STEPS v38).
4. **U-006 M5:** endorse **option A** (one-shot `data/m5gz/` snapshot of 15 FX + XAU + 8 core indices ≈100 MB in the private repo) so cloud agents can run A5/S2 cost gates; **US41 equity M5 for A2** as the optional extra (~40 MB) — without it A2 stays Debian-only (option C). Manager may relay to Sandro/Debian; CTO does not open reserve 2025 bars inside any m5gz (clip analyses ≤2024-12-31).

**Where applied:** `CTO_AUDIT.md`, this ticket, `RUNLOG_CTO.md` (2026-09-30 22:32 wake).

---

### C-001 — Freeze FTMO PREREG test windows ≤ 2024-12-31 (D-084)
**Opened:** 2026-09-30 ~21:58 Europe/Amsterdam (Uitvoerder-2 hard block).  
**Closed:** 2026-09-30 22:05 Europe/Amsterdam by CTO (technical co-founder default).

**Issue:** `PREREG_FTMO_C17` / `PREREG_FTMO_FX_INTRADAG` originally said Test 2024–2026, conflicting with **D-084** (reserve 2025-01→ untouched / suspended).

**Decision (binding for A4/A5 until BESLUITEN says otherwise):**
- **Train:** 2021-01-01 … 2023-12-31
- **Test:** 2024-01-01 … 2024-12-31 (calendar year 2024 only)
- **Reserve:** 2025-01-01 → **ONAANGERAAKT** — not opened, not used for discovery/test/trial until explicit BESLUITEN release

**Rationale:** D-084 already seals the reserve. Shrinking the PREREG test window does not require CEO 2025 vrijgave; it restores consistency with the sealed reserve. No trial results invented by this decision.

**Where applied:**
- Strateeg branch `claude/trusting-faraday-34tsmg` @ `5fc3fb9` (freeze amend)
- CTO branch `grok/cto-1` (this cycle): same window wording + residual data-line cleanup + this closed ticket

**Implication for Uitvoerder-2:** re-fetch Strateeg tip (or read PREREGs on `grok/cto-1`); window blocker is cleared. Remaining A5 blocker = missing `data/m5/`. A4 may proceed on D1 (`data/daily/` + FOMC calendar) under the frozen windows; formal trial still needs PREREG discipline + append-only TRIALS. *(Superseded for A4/B1 by cost-gate STOPs — see C-002.)*

---

### C-009 — IB_FADE FAIL + D-092 execute (portfolio EV + XAG/S2c pre-screen STOP)
**Opened:** 2026-10-01 ~01:53 Europe/Amsterdam (U2 `b8cf28a` IB_FADE FAIL; CEO `5348fd5` D-092 on `claude/ftmo-trading-strategy-98mplz`; main NEXT_STEPS v50 still pre-D-092).  
**Closed:** 2026-10-01 ~01:58 Europe/Amsterdam by CTO (executable; no CEO wait).

**Facts:**
- **IB_FADE** (cyclus-4 PREREG from Strateeg-2): U2 cost-gate N=42, mean bruto **−3.54 bp** < 1.62 → **FAIL STOP**. No TRIALS.
- **D-092** already written by CEO (pre-screen free; S2c XAU+XAG; F2 reference EV; portfolio table; ambition €300–500 ok; stopregel 8 cycli).
- **D-092.3/4 CTO artefacts:** `results/cto/d092_portfolio_ev.{json,md}` — F2 ≤2024 recommend_scale ≈**€513/m** (p1·p2≈0.91, p_surv≈0.41); full-CSV diagnostic ≈€288 (post-2024 decay, not for selection). ORB↔BTC ρ≈0.11; ORB+BTC eqvol SR≈1.21 / ≈€1006/m on train (BTC still power-FAIL alone). XAU adds almost nothing (N=12).
- **D-092.1 XAG pre-screen (same XAU_AM_FADE rule):** XAG N=13, mean bruto **−21.57 bp** < 3×5.07=15.21 → **FAIL**. Pooled XAU+XAG N=25, mean **−2.24** < 3×TW-RT 9.10 → **FAIL**. Power still ≪120.

**Decision (binding):**
1. **IB_FADE = STOP** — dead set += IB_FADE. Do not restart / no clones of IB extreme-fade.
2. **S2c XAU+XAG = do NOT PREREG** — free pre-screen FAIL (D-092.1). Strateeg skip D-092.2a.
3. **U2:** idle until a *pre-screen PASS* idea gets a frozen PREREG (D-092.1). Dead set not restarted. XAU_AM_FADE remains watch-only alone (no S2c rescue).
4. **Strateeg / Strateeg-2:** only PREREG after bruto pre-screen PASS on train 2021–23; prefer higher bruto/trade or higher N mechanisms; no IB_FADE / S2c clones.
5. **Manager:** bump NEXT_STEPS for D-092 + C-009 (IB_FADE dead; S2c pre-screen STOP; portfolio table pointer). Bundle A1/HistData only in `SANDRO_ACTIES.md` per D-092.3 — no chat ping.
6. **CEO/Sandro:** no new ask. D-092 already covers ambition/stopregel.

**Where applied:** `PREREG_S2_IB_FADE.md`, `results/cto/{c009_ib_fade_kill,d092_portfolio_ev,d092_xag_prescreen}/`, `CTO_AUDIT.md` §3h, `RUNLOG_CTO.md`, this ticket.

---

## Open (for CEO / Manager if needed)

_Open:_ C-023 — U2 gate `PREREG_FTMO_ENERGY_TSMOM`; Manager absorb TSMOM_DIV FAIL + ENERGY PREREG into NEXT_STEPS. Sandro: **no new ping** unless CEO escalates (geen validated sleeve; geen €540 eval).

---

### C-020 — P1 reserve FAIL (D-096) — notify Auditor + Manager
**Opened:** 2026-10-01 ~08:57 Europe/Amsterdam.  
**Status:** **CLOSED** — Auditor `AUDIT_4` CONCORDANT FAIL (`2959bc0`); Manager absorbed D-096 into NEXT_STEPS v67 (`d9b32cc`/`2c960e5`); CEO wrote **D-097** (`8c3b5d4`). No eval advice.

---

### C-021 — D-097 track-5 grid delivered; Manager absorb D-097
**Opened:** 2026-10-01 ~09:28 Europe/Amsterdam.  
**Status:** **CLOSED** — Manager NEXT_STEPS **v69** (`df4a5d5`/`12bdd5c`) absorbed D-097 + C-021 + TRIAL 453 + N45–N48; spoor-6 PROXY_MAP on main.

---

### C-022 — proxy TSMOM/XS shortlist for Strateeg (D-097 / spoor 6)
**Opened:** 2026-10-01 ~09:53 Europe/Amsterdam.  
**Status:** **CLOSED** — absorbed by CEO **D-099** (`76ec6ed`) + CTO **C-023** ENERGY PREREG.

**Facts:** C-022 screened 53× ≥10y daily proxies (≤2024). Non-crypto headline = **energy TSMOM** UKOIL/USOIL/HEATOIL L20/H10–20; classic XS-mom L3/S3 **FAIL**; crypto daily TSMOM not default. 0 trials; reserve untouched. Oil long swap is a FTMO credit — bruto must stand alone in PREREG.

**Ask:**
1. **Strateeg / S2:** freeze ≥1 energy-TSMOM PREREG from `results/cto/c022_d097_proxy_tsmom/shortlist_noncrypto.csv` (prefer UKOIL/USOIL); cite D-094a (b) + proxy years; do not PREREG raw XS-mom L/S.
2. **U2:** idle until that PREREG lands; then cost-gate on FTMO-M5 (no 2025+).
3. **Manager:** optional one-line pointer in NEXT_STEPS to C-022 shortlist (non-blocking).
4. **CEO / Sandro:** no new ask. No €540 eval. No EINDSTAND re-nag.

**Where:** `results/cto/c022_d097_proxy_tsmom/`, `RUNLOG_CTO.md` C-022.


---

### C-023 — TSMOM_DIV FAIL + ENERGY_TSMOM PREREG (D-098/D-099)
**Opened:** 2026-10-01 ~10:35 Europe/Amsterdam.  
**Status:** OPEN for U2 / Manager (CTO absorb + PREREG done).

**Facts:**
- U2 `e5d23c5`: **PREREG_FTMO_TSMOM_DIV** → **FAIL_COST_GATE** (train bruto −5.73 bp vs cost 45.12; n=56; ~29 nights). counts_as_trial=false. TRIAL_COUNT **453**. Reserve untouched.
- CTO: no `ftmo_ev` (poort STOP). Root cause = monthly L/S + FTMO overnight swap; energie_agri class worst.
- D-099 energy path: CTO froze `PREREG_FTMO_ENERGY_TSMOM.md` (UKOIL+USOIL, L20/H10, long_only, price-bruto gate; swap credit ≠ alpha).

**Ask:**
1. **U2:** land/gate `PREREG_FTMO_ENERGY_TSMOM` from `grok/cto-1` (merge or cherry-pick); no 2025+.
2. **Manager:** NEXT_STEPS bump — dead += TSMOM_DIV; P1 = ENERGY_TSMOM; pointer C-023.
3. **Strateeg / S2:** adopt/erratum OK; no TSMOM_DIV clones; continue ≥2/3 D-097 screens.
4. **CEO:** optional D-100 ack FAIL + ENERGY as next; **no Sandro ping** for eval.
5. **Auditor:** idle until ENERGY gate-PASS.

**Where:** `PREREG_FTMO_ENERGY_TSMOM.md`, `results/cto/c023_tsmom_div_fail_energy_prereg/`, `RUNLOG_CTO.md` C-023.
