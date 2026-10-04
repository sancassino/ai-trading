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

### C-070 — absorb v137 + confirm cost exhaustion HOLD (closed — QUIET)
**Opened/closed:** 2026-10-04 ~11:28 Europe/Amsterdam.  
**Status:** CLOSED — routine absorb + honest exhaustion; C-048 nine fully closed; **0** new authorize-able cost rows; Strateeg HOLD; U2 IDLE; Lane-A/S2 is novelty path; **no Sandro ping**.

**Facts:** Main v137 `98b792b` + U2 `469ffe0` IDLE TRIAL **471** + Faraday idle `836d45c` / results `1e5a7f1` (N180–N183 FAIL unchanged) + S2 EWC/XLU DEFER. Alle-book audit: ok_new_authorize **0** (md5 unchanged since C-050). FREEZE OFF. Track-3 PAUSED. Formal OPEN **empty**. CTO trials **0**.

### C-050 — absorb v117 + Faraday N180–N183 FAIL; honest cost exhaustion HOLD (closed — QUIET)
**Opened/closed:** 2026-10-04 ~01:35 Europe/Amsterdam.  
**Status:** CLOSED — routine absorb + honest exhaustion; C-048 nine fully closed; **0** new authorize-able cost rows; Strateeg HOLD; U2 IDLE; Lane-A/S2 is novelty path; **no Sandro ping**.

**Facts:** Main v117 `9b85bae` + Faraday `1e5a7f1` (N180 UK100 FAIL / N181 JP225 FAIL / N182 HK50 FAIL / N183 AUS200 FAIL) + U2 `8fefd81` IDLE TRIAL **471** + S2 EWC/XLU DEFER. Alle-book audit: ok_new_authorize **0** (Q2 stocks/crypto, aangenomen metals, a0-high, proxy_lt5 FX, SPN35/N25/EU50 standing-no, dead soles). FREEZE OFF. Track-3 PAUSED. Formal OPEN **empty**. CTO trials **0**.

### C-049 — absorb v114 + Faraday N176–N179 FAIL; S2 EWC/XLU defer (closed — QUIET)
**Opened/closed:** 2026-10-04 ~01:05 Europe/Amsterdam.  
**Status:** CLOSED — routine absorb; Faraday already D-092.1 FAIL on 4 of 9 authorized names; remaining 4 indices for Strateeg; S2 EWC/XLU deferred; no live PREREG; U2 IDLE; **no Sandro ping**.

**Facts:** Main v114 `39c7182` + Faraday `aadaf71` (N176 GBPCAD FAIL / N177 EURNOK FAIL / N178 AUDJPY FAIL / N179 EURAUD FAIL) + U2 `b0b64e9` IDLE TRIAL **471** + S2 `e31d1b5` EWC/XLU packed. Remaining authorized unscreened: UK100/JP225/HK50/AUS200 (+ USDHKD soft-skip). FREEZE OFF. Track-3 PAUSED. Formal OPEN **empty**. CTO trials **0**.

### C-044 — absorb v104 + Faraday 7c1a880; N162/N163 DIAG_FAIL_CLONE (closed — QUIET)
**Opened/closed:** 2026-10-03 ~22:57 Europe/Amsterdam.  
**Status:** CLOSED — catch-up absorb after missed ~22:25 cycle; both OPEN screens DIAG_FAIL_CLONE; no live PREREG; U2 IDLE; Strateeg needs ≥2 NEW_FAMILY; **no Sandro ping**.

**Facts:** Main v104 `95624bb` + Faraday `7c1a880` N160 FAIL / N161 PASS→PREREG + U2 `03a1a1d` N161 FAIL_T TRIAL **471**. CTO diag N162 mean −0.308 < 2.34 n=217 (US30/US100 twin clone) / N163 mean −1.674 < 3.66 n=296 (NZD twin clone) → **DIAG_FAIL_CLONE**. Agrees Faraday uncommitted WT. FREEZE OFF. Track-3 PAUSED. Formal OPEN **empty**.


### C-043 — absorb v103 + Faraday 78ee291; N158/N159 DIAG_FAIL (closed — QUIET)
**Opened/closed:** 2026-10-03 ~01:53 Europe/Amsterdam.  
**Status:** CLOSED — routine absorb; both OPEN screens DIAG_FAIL; no live PREREG; U2 IDLE; Strateeg needs ≥2 NEW_FAMILY; **no Sandro ping**.

**Facts:** Faraday `78ee291` N156/N157 FAIL + OPEN N158/N159; CTO diag N158 mean −0.57 < 10.02 (n=491) / N159 mean −4.34 < 2.16 (n=141) → DIAG_FAIL. Main v103 absorbed. TRIAL 470. FREEZE OFF. Track-3 PAUSED.


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

_Open:_ C-025 — U2 gate `PREREG_FTMO_FX_EUR_SHORT_TSMOM`; Manager absorb IDX_SHORT FAIL + C-025; Strateeg bar N68 / drop N67 / N66 subsumed. Sandro: **no new ping** (geen validated sleeve; geen €540 eval).

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
**Status:** **CLOSED** — U2 ENERGY FAIL_COST_GATE (`c1499ce`); Manager v71; CEO D-100; CTO C-024 next.

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

---

### C-024 — ENERGY FAIL absorb + D-100 shortlist + IDX_SHORT PREREG
**Opened:** 2026-10-01 ~11:05 Europe/Amsterdam.  
**Status:** **CLOSED** — U2 IDX_SHORT FAIL_COST_GATE (`72f40d3`); Manager v72; CTO C-025 next.

**Facts:**
- U2 `c1499ce` / idle `0f5295c`: **PREREG_FTMO_ENERGY_TSMOM** → **FAIL_COST_GATE** (train bruto 29.08 bp vs gate 272.08; ~83 bp swap/trade; n=209). counts_as_trial=false. TRIAL_COUNT **453**. Reserve untouched.
- CEO **D-100** (`615bca0`): swap-bewust ontwerpen; `results/ceo/swap_side_map.csv` (166 symb.).
- CTO: no `ftmo_ev` on ENERGY. Dead += ENERGY_TSMOM. **No clones** (incl. **N59** BARRED).
- C-024 artefacts: swap-cheap shortlist (75 names; families index-short / FX-carry+ / metal / non-oil commodity).
- Frozen `PREREG_FTMO_IDX_SHORT_TSMOM.md` (US100+US30 short-only L20/H10; D-100 cheap side).
- **N58** flagged SWAP_HOSTILE (AUD long + USDJPY short = expensive sides).

**Ask:**
1. **U2:** gate `PREREG_FTMO_IDX_SHORT_TSMOM` from `grok/cto-1`; no 2025+; skip ENERGY re-gate / N59.
2. **Manager:** NEXT_STEPS bump — dead += ENERGY_TSMOM; P1 = IDX_SHORT_TSMOM; pointer C-024 / D-100; N59 barred; N58 swap warning.
3. **Strateeg / S2:** drop N59; redesign N58 to cheap FX sides (USDJPY/USDCHF/AUDCHF long carry+trend) or intradag-flat; keep N60; ≥2/3 screens on C-024 families A/B.
4. **CEO:** optional ack ENERGY FAIL + D-100 → IDX_SHORT; **no Sandro ping** for eval.
5. **Auditor:** idle until IDX_SHORT gate-PASS.

**Where:** `PREREG_FTMO_IDX_SHORT_TSMOM.md`, `results/cto/c024_d100_swap_aware/`, `RUNLOG_CTO.md` C-024.


---

### C-025 — IDX_SHORT FAIL absorb + FX_EUR_SHORT PREREG (D-100)
**Opened:** 2026-10-01 ~11:35 Europe/Amsterdam.  
**Status:** **CLOSED** — U2 FX_EUR_SHORT FAIL_T (`0e04df6`, TRIAL 454); Manager v74; CTO C-026/C-027 path.

**Facts:**
- U2 `72f40d3`: **PREREG_FTMO_IDX_SHORT_TSMOM** → **FAIL_COST_GATE** (train bruto −66.22 bp vs gate 6.13; n=177). counts_as_trial=false. TRIAL_COUNT **453**. Reserve untouched.
- Root cause = equity drift (not swap). CTO: no `ftmo_ev`. Dead += IDX_SHORT_TSMOM. **No clones** (incl. **N68** BARRED).
- C-025 family diag (0 trials): family A overnight index-short TSMOM closed; AUD* long carry L20/H10 diag FAIL; **N67** USDJPY long diag FAIL; EURUSD+EURAUD short diag pooled +18.6 bp / N=226.
- Frozen `PREREG_FTMO_FX_EUR_SHORT_TSMOM.md` + `scripts/fx_eur_short_tsmom_gate.py` (EURUSD+EURAUD short-only L20/H10; D-100 cheap sides).
- **N66** subsumed into PREREG. Strateeg tip `bafbe9e`; S2 still `365f704` drought.

**Ask:**
1. **U2:** gate `PREREG_FTMO_FX_EUR_SHORT_TSMOM` from `grok/cto-1`; no 2025+; skip IDX_SHORT re-gate / N68 / N67.
2. **Manager:** NEXT_STEPS bump — dead += IDX_SHORT_TSMOM; P1 = FX_EUR_SHORT_TSMOM; pointer C-025 / D-100; N68 barred; N67 drop; N66 subsumed.
3. **Strateeg / S2:** bar N68; drop N67; treat N66 as subsumed; ≥2/3 screens with positive proxy bruto on D-100 cheap sides or intradag-flat.
4. **CEO:** optional ack IDX_SHORT FAIL + FX_EUR_SHORT next; **no Sandro ping** for eval.
5. **Auditor:** idle until FX_EUR_SHORT gate-PASS (or FAIL_T trial append by U2).

**Where:** `PREREG_FTMO_FX_EUR_SHORT_TSMOM.md`, `scripts/fx_eur_short_tsmom_gate.py`, `results/cto/c025_idx_short_fail_fx_prereg/`, `RUNLOG_CTO.md` C-025.


---

### C-026 — FX_EUR_SHORT FAIL_T absorb + USDJPY_MED PREREG (D-100)
**Opened:** 2026-10-01 ~12:05 Europe/Amsterdam.  
**Status:** **CLOSED** — U2 USDJPY_MED FAIL_T (`910d6ff`, TRIAL 455); Manager v74; CTO C-027 next.

**Facts:**
- U2 `0e04df6`: **PREREG_FTMO_FX_EUR_SHORT_TSMOM** → **FAIL_T** (cost-gate+stress PASS; t train 1.90; test bruto −3.42; EURAUD test −8.09). counts_as_trial=true. TRIAL_COUNT **454**. Reserve untouched.
- CTO: no `ftmo_ev`. Dead += FX_EUR_SHORT_TSMOM. **No clones** (no L/H / EURGBP / long-been).
- C-026 family diag (0 trials): N69/N70/N71 **DIAG_FAIL**; COFFEE long dies under honest CEO spread_bp≈10.4; soft shorts FAIL; family A still closed.
- Frozen `PREREG_FTMO_FX_USDJPY_MED_TSMOM.md` + `scripts/fx_usdjpy_med_tsmom_gate.py` (USDJPY long-only L60/H10; train 2000–2016; D-097 medium-term; **≠ N67 L20**).
- Strateeg tip `cc3c808` N69–N71; S2 tip `4575a4f` drought; main v73 `358ead9`.

**Ask:**
1. **U2:** gate `PREREG_FTMO_FX_USDJPY_MED_TSMOM` from `grok/cto-1`; no 2025+; skip FX_EUR_SHORT re-gate / N67 L20 / N69–N71.
2. **Manager:** NEXT_STEPS bump — dead += FX_EUR_SHORT_TSMOM; TRIAL **454**; P1 = USDJPY_MED_TSMOM; pointer C-026 / D-100; N69–N71 DIAG_FAIL.
3. **Strateeg / S2:** drop N69–N71 as PREREG candidates; ≥2/3 screens with **honest** RT (not soft category-fallback 2 bp) on D-100 cheap sides or intradag-flat.
4. **CEO:** optional ack FX_EUR_SHORT FAIL_T + USDJPY_MED next; **no Sandro ping** for eval.
5. **Auditor:** idle until USDJPY_MED gate-PASS (or FAIL_T trial append by U2). FDR-context: C-025 EUR-short path → C-026 JPY-med fork.

**Where:** `PREREG_FTMO_FX_USDJPY_MED_TSMOM.md`, `scripts/fx_usdjpy_med_tsmom_gate.py`, `results/cto/c026_fx_eur_short_fail_next/`, `RUNLOG_CTO.md` C-026.


---

### C-027 — USDJPY_MED FAIL_T absorb + EURJPY_MED PREREG (D-100)
**Opened:** 2026-10-01 ~12:30 Europe/Amsterdam.  
**Status:** **CLOSED** — U2 EURJPY_MED FAIL_T (TRIAL 456); L60 FX-med BARRED; Manager v75+; C-028/C-029 next.

**Facts:**
- U2 `910d6ff`: **PREREG_FTMO_FX_USDJPY_MED_TSMOM** → **FAIL_T** (cost-gate+stress PASS; t train 1.15; test h1 bruto −11.88). counts_as_trial=true. TRIAL_COUNT **455**. Reserve untouched.
- CTO: no `ftmo_ev`. Dead += FX_USDJPY_MED_TSMOM. **No clones** (no L/H / USDCNH / short-been). Independent re-run concordant; no double TRIALS append.
- C-027 family diag (0 trials): **N72 EURJPY DIAG_PASS** (train +7.81 ≥ 3.30; t≈0.55); **N73/N74 DIAG_FAIL**.
- Frozen `PREREG_FTMO_FX_EURJPY_MED_TSMOM.md` + `scripts/fx_eurjpy_med_tsmom_gate.py` (EURJPY long-only L60/H10; train from 2003-01-23; D-097 medium-term; **≠ USDJPY_MED pair**).
- Strateeg tip `78673d0` N72–N74; S2 tip `4575a4f` drought; main v74 `b340e56`.

**Ask:**
1. **U2:** gate `PREREG_FTMO_FX_EURJPY_MED_TSMOM` from `grok/cto-1`; no 2025+; skip USDJPY_MED re-gate / N73 / N74.
2. **Manager:** NEXT_STEPS bump — dead += FX_USDJPY_MED_TSMOM; TRIAL **455**; P1 = EURJPY_MED_TSMOM; pointer C-027 / D-100; N73–N74 DIAG_FAIL; N72 subsumed.
3. **Strateeg / S2:** drop N73–N74 as PREREG candidates; treat N72 as subsumed; prepare **non-L60 FX-med** screens (intradag-flat / other families) if EURJPY FAIL_T — L60 FX-med path thinning.
4. **CEO:** optional ack USDJPY_MED FAIL_T + EURJPY_MED next; **no Sandro ping** for eval.
5. **Auditor:** idle until EURJPY_MED gate-PASS (or FAIL_T trial append by U2). FDR-context: C-026 JPY-med → C-027 EURJPY-med fork (same family, different pair).

**Where:** `PREREG_FTMO_FX_EURJPY_MED_TSMOM.md`, `scripts/fx_eurjpy_med_tsmom_gate.py`, `results/cto/c027_usdjpy_fail_next/`, `RUNLOG_CTO.md` C-027.

---

### C-028 — Edge-search upgrade (Lane A/B + novelty quota)
**Opened:** 2026-10-01 ~12:41 Europe/Amsterdam.  
**Status:** **CLOSED** — Manager v76+ absorbed C-028; S2/Strateeg role split live; CORN promote later demoted in C-029.

**Facts:**
- Binding doc: `EDGE_SEARCH_UPGRADE.md` (until CEO D-* supersedes).
- Lane A = free Yahoo/proxy daily discovery (day_t≥2 bruto before FTMO cost); Lane B = survivors only → PREREG + U2.
- Novelty quota: ≥2/3 pre-screens carry NEW_FAMILY not used by FAIL/dead last 30d; parameter clones BARRED.
- Kill circuit: after 5 consecutive cost-gate-PASS FAIL_T → mandatory family pivot (no more L60 FX-med / ORB cycle); document in NEXT_STEPS.
- Roles: Strateeg-2 = Lane-A novelty researcher; Strateeg = Lane-B PREREG writer + D-100; Manager enforces quota.
- Lane-A diagnostic (0 trials): **promote_to_lane_b=yes** → `COMMODITY_SEASONALITY` CORN_F (FTMO `CORN.c`, day_t≈2.11, ~16y). Near-miss: overnight gap-fade t≥2 but n<80; CATTLE_F demoted (no PROXY_MAP). FX carry residual / xasset vol-timing not promote.
- Trials/TRIAL_COUNT: **unchanged** (0 CTO trials). Reserve 2025+ untouched. EURJPY_MED PREREG still OPEN for U2 (C-027).

**Ask:**
1. **Manager:** absorb `EDGE_SEARCH_UPGRADE.md` into `NEXT_STEPS` — new section (Lane A/B, novelty quota, kill circuit, role tweak); enforce ≥2/3 NEW_FAMILY in Strateeg/S2 tasking; note CORN seasonality as optional Lane-B candidate (not P1 over EURJPY_MED).
2. **Strateeg-2:** switch to **Lane-A mode** next cycle — Yahoo-first, write VOORSTEL + raw screens with NEW_FAMILY tags; do not emit FTMO PREREG from dead-sleeve clones.
3. **Strateeg:** stop L60 FX-med clones if EURJPY dies; Lane-B PREREGs only from Lane-A survivors (or honest-RT intradag) + D-100; optional CORN.c seasonality only after honest agri cost design.
4. **U2:** continue gating current OPEN PREREGs (EURJPY_MED); Lane-A screens ≠ trials; no TRIALS append for C-028.
5. **CEO:** optional later D-* to confirm/supersede EDGE_SEARCH_UPGRADE; **no Sandro ping** for eval.
6. **Auditor:** idle on C-028 process; FDR-context when/if CORN Lane-B PREREG gates.

**Where:** `EDGE_SEARCH_UPGRADE.md`, `results/cto/c028_edge_upgrade/`, `scripts/c028_lane_a_screen.py`, `RUNLOG_CTO.md` C-028.

---

### C-029 — N78 FAIL_COST_GATE absorb + Lane-B diag + CORN demote
**Opened:** 2026-10-01 ~12:55 Europe/Amsterdam.  
**Status:** **CLOSED** — Manager v81 absorbed N78/N80 bookkeeping; superseded by C-030 for N82–N86.

**Facts:**
- U2 `b998253`: **N78 VIX_TERM_VOV** → **FAIL_COST_GATE** (mean +2,21 ≪ 7,83). Manager v78: **geen trial**; TRIAL_COUNT **456**. Dead += N78. Bar VIX_TERM clones. Reserve untouched.
- CTO C-029 diag (0 trials): **N75/N76/N77 DIAG_FAIL**; **N81 DIAG_FAIL**; **N79 UNDERPOWERED** (n=46, mean 127≥50). **No PREREG freeze.**
- **CORN_F demote:** honest M5 spread≈20.8 bp → gate≈62 bp; Lane-A mean 5.98≪62; not in COSTS_FTMO. Was C-028 Lane-A promote — not Lane-B ready.
- Kill circuit: FAIL_COST_GATE does not increment FAIL_T streak; pivot already ON (L60 FX-med / ORB / classic-TSMOM barred).
- Strateeg tip `bdc0387` N79–N81 NEW_FAMILY; U2 IDLE after bookkeeping.

**Ask:**
1. **U2:** IDLE; TRIAL_COUNT→456 + TRIALS N78 `ongeldig`; skip N75–N78 / CORN.
2. **Manager:** NEXT_STEPS bump — dead+=N78; N75–N77 DIAG_FAIL; CORN demote; TRIAL 456; pointer C-029.
3. **Strateeg:** drop N75–N77; N79 underpowered / N80 open / skip N81; ≥2/3 NEW_FAMILY.
4. **S2:** Lane-A with honest-cost survivors only; bar VIX_TERM / CORN-as-FTMO / L60 FX / ORB / classic-TSMOM.
5. **CEO:** optional ack; **no Sandro ping**.
6. **Auditor:** idle until next gate-PASS.

**Where:** `results/cto/c029_n78_absorb_lane_b/`, `scripts/c029_lane_b_diag.py`, `RUNLOG_CTO.md` C-029.


---

### C-030 — N80 FAIL_COST_GATE absorb + Lane-B diag N82–N86
**Opened:** 2026-10-01 ~13:35 Europe/Amsterdam.  
**Status:** **CLOSED** — Manager v83 absorbed; superseded by C-031 (N87 + N90–N92).

**Facts:**
- U2 `454628f`: **N80** UKOIL OVN-gap → **FAIL_COST_GATE** (mean +7,56 < 8,13; **geen trial**). Manager v81: TRIAL_COUNT **456**. Dead += N80. **Bar** UKOIL OVN-gap / softer-gate / USOIL twin. Reserve untouched.
- CTO C-030 diag (0 trials): **N82/N84/N85/N86 DIAG_FAIL**; **N83 UNDERPOWERED** (n=52, mean +15,36 ≥ 1,98; DXYcash M5 only from 2024-11 → Yahoo DXY daily proxy). **No PREREG freeze.**
- Faraday `6c9c1e5` N84–N86 VOORSTEL mirrored on `grok/cto-1`. U2 tip `35412c1` IDLE.
- Kill circuit: FAIL_COST_GATE does not increment FAIL_T streak; pivot ON; L60 FX / ORB / classic-TSMOM / VIX_TERM / CORN-as-FTMO / UKOIL OVN-gap **BARRED**.

**Ask:**
1. **U2:** IDLE; skip N75–N86 / CORN / VIX_TERM; wake only on next PASS→PREREG.
2. **Manager:** NEXT_STEPS bump — N82/N84/N85/N86 DIAG_FAIL; N83 UNDERPOWERED; pointer C-030; enforce ≥2 NEW_FAMILY replacements (D-094).
3. **Strateeg:** drop N82–N86 PREREG path; file ≥2 NEW_FAMILY (≥2/3 novelty); no barred clones; no DXY→equity PREREG until DXYcash history covers train or CEO accepts Yahoo proxy + N≥150.
4. **S2:** Lane-A Yahoo-first NEW_FAMILY; honest FTMO RT in COSTS before promote.
5. **CEO:** optional ack; **no Sandro ping**.
6. **Auditor:** idle until next gate-PASS.

**Where:** `results/cto/c030_n80_absorb_n82_n86/`, `scripts/c030_lane_b_diag.py`, `VOORSTEL_PRESCREEN_N84.md`…`N86.md`, `RUNLOG_CTO.md` C-030.


---

### C-031 — N87 FAIL_T absorb + N90–N92 Lane-B + N92 PREREG
**Opened:** 2026-10-02 ~20:31 Europe/Amsterdam.  
**Status:** **CLOSED** — Manager v86 absorbed N92/N93; superseded by C-032 (N94/N95 DIAG_FAIL).

**Facts:**
- Merged main `054a8eb` NEXT_STEPS **v83** (D-101…D-104 + N87). TRIAL_COUNT **457**. FREEZE **OFF**. Reserve untouched.
- U2 `3a9108e` **N87** FAIL_T (counts_as_trial). Dead += N87. Kill streak +=1; pivot ON. U2 tip `6f6ef86` was IDLE.
- CTO C-031 diag (0 trials): **N91 DIAG_FAIL**; **N90 UNDERPOWERED** (n=113, mean +10.15≥2.16); **N92 DIAG_PASS** (n=592, mean +5.90≥1.98).
- Frozen `PREREG_FTMO_N92.md` + `scripts/n92_us100_ny_2h_mom_gate.py`. Engine: `adverse_bp_to_daily_drawdowns` for D-101 lat-B intradag-DD.
- main `catalogus/TRIALS.csv` still missing N87 row (present on U2) — Manager merge hygiene.

**Ask:**
1. **U2:** gate `PREREG_FTMO_N92` from `grok/cto-1`; no 2025+; skip N75–N91 / CORN / VIX / L60 / UKOIL-OVN / ORB-meta.
2. **Manager:** NEXT_STEPS bump — pointer C-031; N91 FAIL; N90 UNDERPOWERED; N92 OPEN PREREG; note TRIALS N87 merge from U2.
3. **Strateeg:** drop N91; replace N90 with NEW_FAMILY (no N-inflate retune); if N92 FAIL_T file ≥2 NEW_FAMILY (D-094).
4. **S2:** restart Lane-A; honest RT before promote; tip `b765613` stale.
5. **CEO:** optional ack; **no Sandro ping**.
6. **Auditor:** idle until N92 gate-PASS or FAIL_T append.

**Where:** `PREREG_FTMO_N92.md`, `scripts/n92_us100_ny_2h_mom_gate.py`, `results/cto/c031_n87_absorb_n90_n92/`, `engine/ftmo.py` (`adverse_bp_to_daily_drawdowns`), `RUNLOG_CTO.md` C-031.


---

### C-032 — N92 FAIL_T + N93 FAIL_COST_GATE absorb + N94/N95 Lane-B DIAG_FAIL
**Opened:** 2026-10-02 ~21:05 Europe/Amsterdam.  
**Status:** OPEN for Manager / Strateeg / S2 (CEO optional).

**Facts:**
- Merged main `615b9af` NEXT_STEPS **v86** (N93 FAIL_COST_GATE; TRIAL **458**; N94/N95 OPEN). FREEZE **OFF**. Reserve untouched.
- U2 `b5b59e0` **N92** FAIL_T (counts_as_trial) → TRIAL **458**. Dead += `N92_US100_NY_2H_MOM`. Kill streak +=1; pivot ON.
- U2 `b382307` **N93** FAIL_COST_GATE (mean +0,99 ≪ 1,98; **geen trial**). Dead += `N93_SECTOR_DISP_ROTATION`. U2 tip IDLE/HOLD.
- CTO C-032 diag (0 trials): **N94 DIAG_FAIL** (n=107, mean −0,97 ≪ gate 6,00; day_t −0,07; h1/h2 split); **N95 DIAG_FAIL** (n=226, mean +1,40 < gate 2,49; day_t 0,30; h2 <0). **No PREREG freeze.**
- Barred remain: L60 FX-med / VIX_TERM / UKOIL-OVN / ORB-meta / CORN-as-FTMO / N87 / N92 / N93 / SECTOR_DISP clones. Track-3 PAUSED.

**Ask:**
1. **U2:** stay IDLE/HOLD; skip N75–N95 / CORN / VIX / L60 / UKOIL-OVN / ORB-meta / SECTOR_DISP; wake only on next PASS→PREREG.
2. **Manager:** NEXT_STEPS bump — pointer C-032; N94/N95 DIAG_FAIL; TRIAL 458; enforce ≥2 NEW_FAMILY replacements (D-094).
3. **Strateeg:** drop N94/N95 PREREG path; file ≥2 NEW_FAMILY (≥2/3 novelty); no barred clones; no NZDJPY/XAU-AM-cont retune.
4. **S2:** Lane-A Yahoo-first NEW_FAMILY with honest FTMO RT in COSTS before promote (SECTOR_DISP already dead as N93).
5. **CEO:** optional ack; **no Sandro ping**.
6. **Auditor:** idle until next gate-PASS.

**Where:** `results/cto/c032_n92_n93_absorb_n94_n95/`, `scripts/c032_lane_b_diag.py`, `RUNLOG_CTO.md` C-032.


---

### C-033 — absorb main v87 + N96/N97 Lane-B (UNDERPOWERED / DIAG_FAIL)
**Opened:** 2026-10-02 ~21:17 Europe/Amsterdam.  
**Status:** OPEN for Manager / Strateeg / S2 (CEO optional).

**Facts:**
- Merged main `6775e28` NEXT_STEPS **v87** (C-032 + N94/N95 DIAG_FAIL; N96/N97 OPEN; TRIAL **458**). FREEZE **OFF**. Reserve untouched.
- Faraday `b2ab614` filed N96/N97 VOORSTEL; no prior D-092.1 results → CTO Lane-B.
- CTO C-033 diag (0 trials): **N96 UNDERPOWERED** (n=112, mean +16.45≥4.80, day_t 1.28); **N97 DIAG_FAIL** (n=101, mean −8.87≪4.50, day_t −0.88). **No PREREG freeze.**
- U2 remains IDLE/HOLD. Kill-circuit pivot ON (no new cost-PASS→FAIL_T this cycle). Track-3 PAUSED.
- Barred remain: L60 FX-med / VIX_TERM / UKOIL-OVN / ORB-meta / CORN-as-FTMO / N87 / N92–N97 / SECTOR_DISP / NZDJPY-LO / XAU-Lon→NY clones.

**Ask:**
1. **U2:** stay IDLE/HOLD; skip N75–N97 / CORN / VIX / L60 / UKOIL-OVN / ORB-meta / SECTOR_DISP / NZDJPY-LO / XAU-Lon→NY; wake only on next PASS→PREREG.
2. **Manager:** NEXT_STEPS bump — pointer C-033; N96 UNDERPOWERED; N97 DIAG_FAIL; TRIAL 458; enforce ≥2 NEW_FAMILY replacements (D-094).
3. **Strateeg:** drop N96/N97 PREREG path; file ≥2 NEW_FAMILY (≥2/3 novelty); no barred clones; do not inflate N96 n via lookback/history retune without CEO/D-094a reason.
4. **S2:** Lane-A Yahoo-first NEW_FAMILY with honest FTMO RT in COSTS before promote.
5. **CEO:** optional ack; **no Sandro ping**.
6. **Auditor:** idle until next gate-PASS.

**Where:** `results/cto/c033_absorb_v87_n96_n97/`, `scripts/c033_lane_b_diag.py`, `VOORSTEL_PRESCREEN_N96.md`, `VOORSTEL_PRESCREEN_N97.md`, `RUNLOG_CTO.md` C-033.


---

### C-034 — N98/N99 Lane-B DIAG_FAIL (no PREREG)
**Opened:** 2026-10-02 ~21:32 Europe/Amsterdam.  
**Status:** OPEN for Manager / Strateeg / S2 (CEO optional).

**Facts:**
- `origin/main` still `6775e28` NEXT_STEPS **v87** (Manager not yet v88 for C-033). FREEZE **OFF**. Reserve untouched.
- Faraday `4a5ec7c` filed N98/N99 after N96 UNDERPOWERED + N97 FAIL; no prior D-092.1 for N98/N99 → CTO Lane-B.
- CTO C-034 diag (0 trials): **N98 DIAG_FAIL** (n=356, mean −3.79 ≪ gate 1.98, day_t −0.62; h1 −8.6 / h2 +1.0); **N99 DIAG_FAIL** (n=103, mean −4.00 ≪ gate 6.81, day_t −0.39; h1/h2 flip). **No PREREG freeze.**
- Prior C-033: N96 UNDERPOWERED / N97 DIAG_FAIL (concordant with Faraday D-092.1).
- U2 remains IDLE/HOLD. Kill-circuit pivot ON (no new cost-PASS→FAIL_T). Track-3 PAUSED.
- Barred remain: L60 FX-med / VIX_TERM / UKOIL-OVN / ORB-meta / CORN-as-FTMO / N87 / N92–N99 / SECTOR_DISP / NZDJPY-LO / XAU-Lon→NY / USOIL→US100 risk-on / CADCHF-LO-5d clones.

**Ask:**
1. **U2:** stay IDLE/HOLD; skip N75–N99 / CORN / VIX / L60 / UKOIL-OVN / ORB-meta / SECTOR_DISP / NZDJPY-LO / XAU-Lon→NY / USOIL→US100 / CADCHF-LO-5d; wake only on next PASS→PREREG.
2. **Manager:** NEXT_STEPS bump — pointer C-033 + **C-034**; N96 UNDERPOWERED; N97–N99 DIAG_FAIL; TRIAL 458; enforce ≥2 NEW_FAMILY replacements (D-094).
3. **Strateeg:** drop N98/N99 PREREG path; file ≥2 NEW_FAMILY (≥2/3 novelty); no barred clones; no thr-grid / UKOIL twin / CADJPY twin / soft gate.
4. **S2:** Lane-A Yahoo-first NEW_FAMILY with honest FTMO RT in COSTS before promote.
5. **CEO:** optional ack; **no Sandro ping**.
6. **Auditor:** idle until next gate-PASS.

**Where:** `results/cto/c034_absorb_n98_n99/`, `scripts/c034_lane_b_diag.py`, `VOORSTEL_PRESCREEN_N98.md`, `VOORSTEL_PRESCREEN_N99.md`, `RUNLOG_CTO.md` C-034.


---

### C-035 — absorb N100/N101 FAIL_T + N103 PREREG (N102 DIAG_FAIL)
**Opened:** 2026-10-02 ~22:05 Europe/Amsterdam.  
**Status:** OPEN for U2 (N103 gate) / Manager / Strateeg / S2 (CEO optional).

**Facts:**
- Merged main `a74ca46` NEXT_STEPS **v89**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **460** (U2).
- Faraday `edbd2ee` PREREG N100/N101 + OPEN N102/N103 NEW_FAMILY Y/Z. S2 tip `67a9be1` (EMB+CRACK promote — both now FAIL_T).
- U2: N100 EMB_CREDIT_STRESS **FAIL_T** TRIAL **459**; N101 CRACK_SPREAD_MACRO **FAIL_T** TRIAL **460**.
- CTO C-035 Lane-B (0 trials): **N102 DIAG_FAIL** (n=104, mean +2.94 < gate 3.03); **N103 DIAG_PASS** (n=286, mean +1.75 ≥ 1.35, day_t 0.38) → **PREREG_FTMO_N103 frozen**.
- Gate smoke N103: cost PASS / stress FAIL (1.75 < 2.025); t_nw≈0.24 — elevated FAIL_STRESS/FAIL_T risk; no retune.
- Kill-circuit pivot **ON** (N87→N92→N100→N101 cost-PASS→FAIL_T). Track-3 PAUSED.
- Barred += EMB_CREDIT_STRESS / CRACK_SPREAD_MACRO / USDCHF-LO-5d (N102) clones + prior N75–N101 / CORN / VIX / L60 / UKOIL-OVN / ORB-meta / SECTOR_DISP / …

**Ask:**
1. **U2:** run **N103** cost-gate + formal (`PREREG_FTMO_N103.md` / `scripts/n103_ger40_us30_industrial_gate.py`); skip N75–N102 + barred clones; no 2025+; no retune on stress/t fail.
2. **Manager:** NEXT_STEPS bump — pointer **C-035**; TRIAL **460**; N100/N101 FAIL_T; N102 DIAG_FAIL; N103 PREREG live; U2 unblocked.
3. **Strateeg:** drop N102; file ≥1 NEW_FAMILY replace (D-094); no USDCHF-LO-5d / GER→US100 / thr-grid clones.
4. **S2:** Lane-A NEW_FAMILY; do not re-promote EMB/CRACK as FTMO.
5. **CEO:** optional ack; **no Sandro ping**.
6. **Auditor:** sample N100/N101 + N103 when landed.

**Where:** `results/cto/c035_absorb_n100_n103/`, `scripts/c035_lane_b_diag.py`, `scripts/n103_ger40_us30_industrial_gate.py`, `PREREG_FTMO_N103.md`, `VOORSTEL_PRESCREEN_N102.md`, `VOORSTEL_PRESCREEN_N103.md`, `RUNLOG_CTO.md` C-035.


---

### C-036 — absorb main v90 + N110/N111 DIAG_FAIL (no PREREG)
**Opened:** 2026-10-02 ~22:35 Europe/Amsterdam.  
**Status:** OPEN for Manager / Strateeg / S2 (CEO optional).

**Facts:**
- Merged main `b7b8004` NEXT_STEPS **v90**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **460**.
- U2 `a70dc8b` IDLE after N103 FAIL_STRESS; hold N110/N111; no live PREREG.
- Faraday `107e502` (prior `7d2d48a`): N104 UNDERPOWERED / N105–N108 FAIL / N109 UNDERPOWERED; OPEN N110/N111 — Manager v90 still points at N104/N105 (lag).
- CTO C-036 Lane-B (0 trials): **N110 DIAG_FAIL** (n=0 — DXYcash M5 starts 2024-11-26, train empty); **N111 DIAG_FAIL** (n=104, mean +3.24 < gate 4.38). **No PREREG freeze.**
- Kill-circuit pivot **ON**. Track-3 PAUSED.
- Barred += N104–N111 families (GBPCHF-LO / JP225 Tokyo→Lon / EURNZD-LO / UK→FRA40 / AUS Asia→Lon / CHFJPY-LO / DXY Lon→EU-PM / GBPAUD-LO-5d) + prior N75–N103 / EMB / CRACK / …

**Ask:**
1. **U2:** stay IDLE/HOLD; skip N75–N111 / barred clones; wake only on next PASS→PREREG.
2. **Manager:** NEXT_STEPS bump — pointer **C-036**; formal OPEN catch-up past N104–N109; N110/N111 DIAG_FAIL; TRIAL 460; enforce ≥2 NEW_FAMILY replacements (D-094).
3. **Strateeg:** drop N110/N111; file ≥2 NEW_FAMILY (≥2/3 novelty); no barred clones; no soft gate on short DXY history; no thr-grid / EURUSD / GBPCHF twin.
4. **S2:** Lane-A Yahoo-first NEW_FAMILY with honest FTMO RT before promote; DXYcash M5 gap = Spoor-6 (optional backfill 2021–23).
5. **CEO:** optional ack; **no Sandro ping**. Optional non-blocking: DXYcash HistData/M5 2021–23 backfill.
6. **Auditor:** idle until next gate-PASS.

**Where:** `results/cto/c036_absorb_v90_n104_n111/`, `scripts/c036_lane_b_diag.py`, `VOORSTEL_PRESCREEN_N106.md`…`N111.md`, `RUNLOG_CTO.md` C-036.


---

### C-037 — absorb main v92 + N114 PREREG (N115 DIAG_FAIL)
**Opened:** 2026-10-02 ~23:05 Europe/Amsterdam.  
**Status:** CLOSED — U2 ran N114 → FAIL_T (TRIAL 462; absorbed main v93+). Superseded by C-038.

**Facts:**
- Merged main `e988749` NEXT_STEPS **v92**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **461** (U2).
- Faraday `791a17c` PREREG N112/N113 + OPEN N114/N115 NEW_FAMILY AI/AJ. S2 tip `35e38ac` (GAS+SILVER promote — both now dead at U2).
- U2: N112 GAS_EQUITY_MACRO **FAIL_T** TRIAL **461**; N113 SILVER_GOLD_RATIO **FAIL_COST_GATE** (geen trial; TRIAL stays 461).
- CTO C-037 Lane-B (0 trials): **N114 DIAG_PASS** (n=371, mean +3.812 ≥ gate 2.34, day_t 0.85) → **PREREG_FTMO_N114 frozen**; **N115 DIAG_FAIL** (n=126, mean −3.43 < 2.34).
- Gate smoke N114: cost PASS / stress PASS (3.81≥3.51); t_nw≈0.71; test 2024 mean −2.16 — elevated FAIL_T risk; no retune.
- Kill-circuit pivot **ON** (N87→N92→N100→N101→N112 cost-PASS→FAIL_T ≥5). Track-3 PAUSED.
- Barred += GAS_EQUITY / SILVER_GOLD / N115 EURUSD Lon-AM→US500 + prior N75–N113 / EMB / CRACK / …

**Ask:**
1. **U2:** run **N114** cost-gate + formal (`PREREG_FTMO_N114_HYG_CREDIT_STRESS.md` / `scripts/n114_hyg_credit_stress_gate.py`); skip N75–N113 + N115 + barred clones; no 2025+; no retune on stress/t fail.
2. **Manager:** NEXT_STEPS bump — pointer **C-037**; TRIAL **461**; N112 FAIL_T; N113 FAIL_COST_GATE; N114 PREREG live; N115 DIAG_FAIL; U2 unblocked.
3. **Strateeg:** drop N115; file ≥1 NEW_FAMILY replace (D-094); no EURUSD→US500 / DXY Lon→EU / N83 opposite / thr-grid clones.
4. **S2:** Lane-A NEW_FAMILY; do not re-promote GAS/SILVER/EMB/CRACK as FTMO.
5. **CEO:** optional ack; **no Sandro ping**.
6. **Auditor:** sample N112/N113 + N114 when landed.

**Where:** `results/cto/c037_absorb_v92_n112_n115/`, `scripts/c037_lane_b_diag.py`, `scripts/n114_hyg_credit_stress_gate.py`, `PREREG_FTMO_N114_HYG_CREDIT_STRESS.md`, `VOORSTEL_PRESCREEN_N114.md`, `VOORSTEL_PRESCREEN_N115.md`, `RUNLOG_CTO.md` C-037.

---

### C-038 — absorb main v95 + N122/N123 DIAG_FAIL (no PREREG)
**Opened:** 2026-10-02 ~23:29 Europe/Amsterdam.  
**Status:** OPEN for Manager / Strateeg / S2 (CEO optional). U2 IDLE — no live PREREG.

**Facts:**
- Merged main `6665e3e` NEXT_STEPS **v95**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **464** (U2). Live PREREG **none**.
- Faraday `47e0eab`: N118 FAIL_T sync; N120/N121 D-092.1 FAIL; OPEN N122/N123 NEW_FAMILY AQ/AR (Manager v95 still listed N120/N121 OPEN — stale).
- U2 `7834a1a` IDLE/HOLD post-N118 FAIL_T (material `9a00524`→`9e928af`).
- CTO C-038 Lane-B (0 trials): **N122 DIAG_FAIL** (n=368, mean −6.312 < gate 2.34, day_t −1.46); **N123 DIAG_FAIL** (n=201, mean −2.656 < 2.34, day_t −0.46). No PREREG.
- Kill-circuit pivot **ON** (N100+N101+N112+N114+N116+N118 cost-PASS→FAIL_T ≥5). Track-3 PAUSED.
- Barred += TIP/IWM/VNQ/EEM/DBC/EFA→US500 + TLT/CPER/HYG/EURUSD Lon-AM + GAS/SILVER + N75–N123 + prior.

**Ask:**
1. **U2:** remain IDLE/HOLD until next PASS→PREREG; skip N75–N123 + barred clones; no 2025+.
2. **Manager:** NEXT_STEPS bump — pointer **C-038**; TRIAL **464**; N118 FAIL_T; N120/N121 FAIL; N122/N123 DIAG_FAIL; formal OPEN empty; ≥2 NEW_FAMILY (D-094).
3. **Strateeg:** file **≥2 NEW_FAMILY** replacements (D-094); no DBC/EFA/VNQ/EEM/TIP/IWM/TLT/CPER/HYG/EURUSD Lon-AM / GAS/SILVER / EMB / CRACK / thr-grid clones.
4. **S2:** Lane-A NEW_FAMILY; do not re-promote dead ETF→US500 stress families as FTMO.
5. **CEO:** optional ack; **no Sandro ping**.
6. **Auditor:** sample N118 FAIL_T + N120–N123 when convenient.

**Where:** `results/cto/c038_absorb_v95_n118_n123/`, `scripts/c038_lane_b_diag.py`, `VOORSTEL_PRESCREEN_N120…N123.md`, `PREREG_FTMO_N118_TIP_REALRATE_STRESS.md`, `RUNLOG_CTO.md` C-038.


---

### C-039 — absorb main v96 + N124/N125 DIAG_PASS→PREREG (U2 unblocked)
**Opened:** 2026-10-02 ~23:56 Europe/Amsterdam.  
**Status:** OPEN for Manager / U2 / Strateeg / S2 (CEO optional). **Live PREREG: N124 + N125.**

**Facts:**
- Merged main `d6b9867` NEXT_STEPS **v96**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **464** (U2).
- Faraday `47e0eab` unchanged (OPEN empty after N122/N123 DIAG_FAIL).
- U2 `6ed73cf` IDLE/HOLD absorb v96 (pre this PREREG).
- S2 `13fe10c` cycle_2346 PROMOTE YIELD_CURVE_2S10S + DEFENSIVE_CYCLICAL — CTO picked up as NEW_FAMILY AS/AT (pipeline refill D-094).
- CTO C-039 Lane-B (0 trials): **N124 DIAG_PASS** (n=240, mean +8.971 ≥ gate 2.34, day_t 1.89) → **PREREG_FTMO_N124 frozen**; **N125 DIAG_PASS** (n=478, mean +5.479 ≥ 2.34, day_t 1.43) → **PREREG_FTMO_N125 frozen**.
- Gate smoke N124: cost PASS / stress PASS (8.97≥3.51); t_nw≈1.82; test 2024 mean +2.89 — elevated FAIL_T risk; no retune.
- Gate smoke N125: cost PASS / stress PASS (5.48≥3.51); t_nw≈1.29; test 2024 mean −2.32 — elevated FAIL_T risk; no retune.
- Kill-circuit pivot **ON** (N100+N101+N112+N114+N116+N118 cost-PASS→FAIL_T ≥5). Track-3 PAUSED.
- Barred += N75–N123 + TIP/IWM/VNQ/EEM/DBC/EFA→US500 + TLT/CPER/HYG/EURUSD Lon-AM + GAS/SILVER + prior. N124/N125 novelty AS/AT kept.

**Ask:**
1. **U2:** run **N124** then **N125** cost-gate + formal (`PREREG_FTMO_N124_YIELD_CURVE_2S10S.md` / `scripts/n124_yield_curve_2s10s_gate.py`; `PREREG_FTMO_N125_DEFENSIVE_CYCLICAL.md` / `scripts/n125_defensive_cyclical_gate.py`); skip N75–N123 + barred clones; no 2025+; no retune on stress/t fail.
2. **Manager:** NEXT_STEPS bump — pointer **C-039**; TRIAL **464**; N124+N125 PREREG live; formal OPEN = N124/N125; U2 unblocked.
3. **Strateeg:** sync — OPEN was empty; CTO filed AS/AT from S2; do not duplicate as Faraday OPEN; keep ≥2/3 novelty feed; bar N75–N123 clones.
4. **S2:** Lane-A NEW_FAMILY; YIELD/DEFENSIVE now in Lane-B; do not re-promote dead ETF→US500 stress families.
5. **CEO:** optional ack; **no Sandro ping**.
6. **Auditor:** sample N124/N125 when U2 lands; FDR vs TLT/SECTOR_DISP.

**Where:** `results/cto/c039_absorb_v96_n124_n125/`, `scripts/c039_lane_b_diag.py`, `scripts/n124_yield_curve_2s10s_gate.py`, `scripts/n125_defensive_cyclical_gate.py`, `PREREG_FTMO_N124_YIELD_CURVE_2S10S.md`, `PREREG_FTMO_N125_DEFENSIVE_CYCLICAL.md`, `VOORSTEL_PRESCREEN_N124.md`, `VOORSTEL_PRESCREEN_N125.md`, `RUNLOG_CTO.md` C-039.

---

### C-040 — absorb main v100 + N134/N135 DIAG_FAIL (no PREREG)
**Opened:** 2026-10-03 ~00:30 Europe/Amsterdam.  
**Status:** OPEN for Manager / Strateeg / S2 (CEO optional). U2 IDLE — no live PREREG.

**Facts:**
- Merged main `b8a1450` NEXT_STEPS **v100**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **470** (U2). Live PREREG **none**.
- Faraday `c19fd24`: N132/N133 D-092.1 FAIL; OPEN N134/N135 (Manager v100 still listed Faraday tip 0af85da / OPEN empty — stale).
- U2 `a76b07a` IDLE/HOLD post-N130+N131 FAIL_T (material `03ad9da`).
- CTO C-040 Lane-B (0 trials): **N134 DIAG_FAIL** (n=184, mean −1.457 < gate 2.34, day_t −0.24); **N135 DIAG_FAIL** (n=211, mean −5.029 < 2.34, day_t −1.04). No PREREG.
- Absorbed N132 MTUM FAIL / N133 GLD FAIL from Faraday (no re-run).
- Kill-circuit pivot **ON** (N100…N131 cost-PASS→FAIL_T ≥5). Track-3 PAUSED.
- Barred += XLF→US500 / QUAL→US500 + N75–N135 + EQW/DXY_DOLLAR/BWX/EWZ/YIELD/DEFENSIVE + prior.
- Faraday local WIP (uncommitted): draft VOORSTEL N136 BRENT_WTI_XS / N137 USDMXN_EM_CARRY_FADE — Strateeg to file/screen.

**Ask:**
1. **U2:** remain IDLE/HOLD until next PASS→PREREG; skip N75–N135 + barred clones; no 2025+.
2. **Manager:** NEXT_STEPS bump — pointer **C-040**; TRIAL **470**; Faraday tip **c19fd24**; N132/N133 FAIL; N134/N135 DIAG_FAIL; formal OPEN empty; ≥2 NEW_FAMILY (D-094).
3. **Strateeg:** file **≥2 NEW_FAMILY** replacements (D-094); prefer non-ETF→US500 stress; WIP N136/N137 ok if distinct; no XLF/QUAL/MTUM/GLD/EQW/DXY/HYG/SECTOR_DISP clones.
4. **S2:** Lane-A NEW_FAMILY; do not re-promote dead ETF→US500 stress families as FTMO.
5. **CEO:** optional ack; **no Sandro ping**.
6. **Auditor:** sample N134/N135 DIAG_FAIL when convenient.

**Where:** `results/cto/c040_absorb_v100_n134_n135/`, `scripts/c040_lane_b_diag.py`, `VOORSTEL_PRESCREEN_N132…N135.md`, `RUNLOG_CTO.md` C-040.

---

### C-041 — absorb main v102 + N142 DIAG_FAIL / N143 DIAG_PASS→PREREG (U2 unblocked)
**Opened:** 2026-10-03 ~01:03 Europe/Amsterdam.  
**Status:** OPEN for Manager / U2 / Strateeg / S2 (CEO optional). **Live PREREG: N143.**

**Facts:**
- Merged main tip `cb1b8d1` (NEXT_STEPS **v102** @ `b0b20ac`). FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **470** (U2).
- Faraday `e1bf004`: N140 FAIL / N141 FAIL_CLONE; prior N138 FAIL_CLONE / N139 FAIL; OPEN N142/N143 (Manager v102 still listed Faraday tip f5523fb / OPEN N138/N139 — stale).
- U2 `78775a2` IDLE/HOLD absorb v102 (pre this PREREG).
- S2 `5a21939` cycle_0047 XLE_ENERGY_EQUITY_STRESS — CTO picked up as NEW_FAMILY BL.
- CTO C-041 Lane-B (0 trials): **N142 DIAG_FAIL** (n=187, mean −1.681 < gate 3.69, day_t −0.71); **N143 DIAG_PASS** (n=356, mean +7.856 ≥ 2.34, day_t 1.81) → **PREREG_FTMO_N143 frozen**.
- Gate smoke N143: cost PASS / stress PASS (7.86≥3.51); t_nw≈1.56; test 2024 mean +6.83 t_nw≈1.25 — elevated FAIL_T risk; no retune.
- Kill-circuit pivot **ON** (N100…N131 cost-PASS→FAIL_T ≥5). Track-3 PAUSED.
- Barred += N75–N142 + US30/US500 XS + XLF/QUAL/BRENT_WTI/USDMXN/GER40_UK/JP_HK/XAU_UKOIL/XAG_UKOIL + prior. N143 novelty BL kept.

**Ask:**
1. **U2:** run **N143** cost-gate + formal (`PREREG_FTMO_N143_XLE_ENERGY_EQUITY_STRESS.md` / `scripts/n143_xle_energy_equity_stress_gate.py`); skip N75–N142 + barred clones; no 2025+; no retune on stress/t fail.
2. **Manager:** NEXT_STEPS bump — pointer **C-041**; TRIAL **470**; Faraday tip **e1bf004**; N138–N142 FAIL/DIAG_FAIL; N143 PREREG live; U2 unblocked.
3. **Strateeg:** refill ≥2 NEW_FAMILY after N142 dead (D-094); do not duplicate XLE as Faraday OPEN while PREREG live; bar N75–N142 clones.
4. **S2:** Lane-A NEW_FAMILY; XLE now in Lane-B; do not re-promote dead ETF→US500 stress families.
5. **CEO:** optional ack; **no Sandro ping**.
6. **Auditor:** sample N143 when U2 lands; FDR vs GAS/XLF/CRACK/N98.

**Where:** `results/cto/c041_absorb_v102_n142_n143/`, `scripts/c041_lane_b_diag.py`, `scripts/n143_xle_energy_equity_stress_gate.py`, `PREREG_FTMO_N143_XLE_ENERGY_EQUITY_STRESS.md`, `VOORSTEL_PRESCREEN_N142.md`, `VOORSTEL_PRESCREEN_N143.md`, `VOORSTEL_S2_XLE_ENERGY_EQUITY_STRESS.md`, `RUNLOG_CTO.md` C-041.

---

### C-042 — absorb Faraday aca4d2f; retract N143 FAIL_CLONE; N150/N151 DIAG_FAIL (no PREREG)
**Opened:** 2026-10-03 ~01:30 Europe/Amsterdam.  
**Status:** OPEN for Manager / Strateeg / S2 (CEO optional). U2 IDLE — **no live PREREG**.

**Facts:**
- Main tip `cb1b8d1` NEXT_STEPS **v102** unchanged. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **470** (U2).
- Faraday `aca4d2f`: N148/N149 D-092.1 FAIL; OPEN N150/N151 (Manager v102 still lists tip f5523fb / OPEN N138/N139 — stale).
- Faraday `93cb002`: **N143 FAIL_CLONE of DBC_z40_thr1.0** — binding over C-041 DIAG_PASS→PREREG → **retracted**. Live PREREG cleared before U2 wake.
- Absorbed N142 FAIL / N144–N147 FAIL/FAIL_CLONE (no re-run).
- U2 `78775a2` IDLE/HOLD (never started N143).
- CTO C-042 Lane-B (0 trials): **N150 DIAG_FAIL** (n=225, mean +10.046 < gate 16.56, day_t 1.26); **N151 DIAG_FAIL** (n=221, mean −0.597 < 6.33, day_t −0.19). No PREREG.
- Kill-circuit pivot **ON** (N100…N131 cost-PASS→FAIL_T ≥5). Track-3 PAUSED. Formal OPEN **empty**.
- Barred += N75–N151 + XLE→US500(DBC clone) / XAG-US30 / EURJPY-USDCHF + US30/US500 / XPT_XPD / BTC_ETH / AUD_XAU / GBP_UKOIL / USDJPY_US100 / EUR_GER40 + prior.

**Ask:**
1. **U2:** remain IDLE/HOLD until next PASS→PREREG; **do not run N143**; skip N75–N151 + barred clones; no 2025+.
2. **Manager:** NEXT_STEPS bump — pointer **C-042**; TRIAL **470**; Faraday tip **aca4d2f**; N142–N151 FAIL/DIAG_FAIL/FAIL_CLONE; no live PREREG; OPEN empty; ≥2 NEW_FAMILY (D-094).
3. **Strateeg:** file **≥2 NEW_FAMILY** replacements (D-094); pipeline empty; no N75–N151 / DBC/XLE / FX-index / FX-metal / FX-oil / PGM / crypto clones.
4. **S2:** Lane-A NEW_FAMILY; do not re-promote dead ETF→US500 stress / dead two-leg XS as FTMO.
5. **CEO:** optional ack of N143 retract (process); **no Sandro ping**.
6. **Auditor:** sample N143 FAIL_CLONE + N150/N151 DIAG_FAIL when convenient.

**Where:** `results/cto/c042_absorb_faraday_n150_n151/`, `scripts/c042_lane_b_diag.py`, `PREREG_FTMO_N143_…` (STOP), `VOORSTEL_PRESCREEN_N143…N151.md`, `RUNLOG_CTO.md` C-042.

---

### C-044 — absorb main v104 + N162/N163 DIAG_FAIL_CLONE (no PREREG)
**Opened:** 2026-10-03 ~22:57 Europe/Amsterdam.  
**Status:** OPEN for Manager / Strateeg / S2 (CEO optional). U2 IDLE — **no live PREREG**.

**Facts:**
- Main tip `95624bb` NEXT_STEPS **v104**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2 N161 FAIL_T).
- Faraday `7c1a880`: N154–N160 D-092.1 FAIL/FAIL_CLONE; N161 PASS→PREREG (consumed); OPEN N162/N163 (VOORSTEL only; WT left uncommitted FAIL_CLONE both).
- U2 `03a1a1d`: **N161 FAIL_T** (TRIAL **471**); IDLE/HOLD.
- CTO C-044 Lane-B (0 trials): **N162 DIAG_FAIL_CLONE** (n=217, mean −0.308 < gate 2.34; US30+US100 same-window twins); **N163 DIAG_FAIL_CLONE** (n=296, mean −1.674 < 3.66; NZD same-window twin). No PREREG.
- Kill-circuit pivot **ON** (N100…N131 + N161 cost-PASS→FAIL_T ≥5). Track-3 PAUSED. Formal OPEN **empty**.
- Barred += N75–N163 + US500 cash-close / AUD NY-fade + US30/US100 same-window / NZD same-window + XLK→US100 + prior.
- Catch-up after missed CTO ~22:25 CEST cycle (~21h).

**Ask:**
1. **U2:** remain IDLE/HOLD until next PASS→PREREG; skip N75–N163 + barred clones; no 2025+.
2. **Manager:** NEXT_STEPS bump — pointer **C-044**; TRIAL **471**; Faraday tip **7c1a880**; N154–N163 FAIL/DIAG_FAIL_CLONE/FAIL_T; no live PREREG; OPEN empty; ≥2 NEW_FAMILY (D-094).
3. **Strateeg:** file **≥2 NEW_FAMILY** replacements (D-094); pipeline empty; no N75–N163 / cash-close twins / AUD-NZD same-window / XLK→US100 clones.
4. **S2:** Lane-A NEW_FAMILY; XLK consumed FAIL_T; do not re-promote dead ETF→index stress / dead one-leg fades.
5. **CEO:** optional ack; **no Sandro ping**.
6. **Auditor:** sample N161 FAIL_T + N162/N163 DIAG_FAIL_CLONE when convenient.

**Where:** `results/cto/c044_absorb_v104_n162_n163/`, `scripts/c044_lane_b_diag.py`, `VOORSTEL_PRESCREEN_N160…N163.md`, `RUNLOG_CTO.md` C-044.

### C-045 — absorb main v105 + N164/N165 DIAG_FAIL (no PREREG)
**Opened:** 2026-10-03 ~23:30 Europe/Amsterdam.  
**Status:** OPEN for Manager / Strateeg / S2 (CEO optional). U2 IDLE — **no live PREREG**.

**Facts:**
- Main tip `31af9f2` NEXT_STEPS **v105**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2).
- Faraday `218eb11`: absorb C-044; OPEN N164/N165 (NEW_FAMILY CG/CH); commit n162_n163_prescreen FAIL_CLONE. Manager v105 still pointed at Faraday `7c1a880` — CTO absorbed newer tip.
- U2 `69c1a34`: IDLE/HOLD absorb v105; TRIAL **471**; no live PREREG.
- CTO C-045 Lane-B (0 trials): **N164 DIAG_FAIL** (n=493, mean +1.567 < gate 9.43; day_t 0.402; no clone — US500 agree 0.97 cover 0.36); **N165 DIAG_FAIL** (n=259, mean −2.233 < 3.45; day_t −1.868; no clone — GBPCHF agree 0.92 cover 0.66). No PREREG.
- Kill-circuit pivot **ON** (N100…N131 + N161 cost-PASS→FAIL_T ≥5). Track-3 PAUSED. Formal OPEN **empty**.
- Barred += N75–N165 + US2000 NY-impulse / EURCHF London-haven + US500/US30/US100 same-window / GBPCHF/USDCHF/AUDCHF same-window + prior.

**Ask:**
1. **U2:** remain IDLE/HOLD until next PASS→PREREG; skip N75–N165 + barred twins/clones; no 2025+.
2. **Manager:** NEXT_STEPS bump — pointer **C-045**; TRIAL **471**; Faraday tip **218eb11**; N164/N165 DIAG_FAIL; no live PREREG; OPEN empty; ≥2 NEW_FAMILY (D-094).
3. **Strateeg:** file **≥2 NEW_FAMILY** replacements (D-094); pipeline empty; no N75–N165 / NY-impulse index twins / London CHF-haven twins.
4. **S2:** Lane-A NEW_FAMILY; do not re-promote dead ETF→index / one-leg fades / XS / NY-impulse / London-haven.
5. **CEO:** optional ack; **no Sandro ping**.
6. **Auditor:** sample N164/N165 DIAG_FAIL when convenient.

**Where:** `results/cto/c045_absorb_v105_n164_n165/`, `scripts/c045_lane_b_diag.py`, `VOORSTEL_PRESCREEN_N164.md`, `VOORSTEL_PRESCREEN_N165.md`, `RUNLOG_CTO.md` C-045.


### C-046 — absorb main v106 + N168 DIAG_FAIL_CLONE / N169 DIAG_FAIL (no PREREG)
**Opened:** 2026-10-04 ~00:05 Europe/Amsterdam.  
**Status:** OPEN for Manager / Strateeg / S2 (CEO optional). U2 IDLE — **no live PREREG**.

**Facts:**
- Main tip `03ac200` NEXT_STEPS **v106**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2).
- Faraday `0019de4`: S2 `885090b` → N166 FAIL_CLONE (HYG) / N167 FAIL; absorb C-045; OPEN N168/N169 (VOORSTEL only).
- U2 `c5a0a4d`: IDLE/HOLD absorb v106; TRIAL **471**; no live PREREG.
- CTO C-046 Lane-B (0 trials): **N168 DIAG_FAIL_CLONE** (n=214, mean +3.049 ≥ gate 1.35 but US500+US100 Europe same-window twins); **N169 DIAG_FAIL** (n=249, mean −0.262 < 2.10; EUR/AUD cover <0.70). No PREREG. N166/N167 not re-screened.
- Kill-circuit pivot **ON** (N100…N131 + N161 cost-PASS→FAIL_T ≥5). Track-3 PAUSED. Formal OPEN **empty**.
- Barred += N75–N169 + LQD/IG-credit / HYG twin / EWY→EUR / US30 Europe inventory / GBP London-fix + US500/US100 Europe same-window / EURUSD/AUDUSD fix same-window + prior.

**Ask:**
1. **U2:** remain IDLE/HOLD until next PASS→PREREG; skip N75–N169 + barred twins/clones; no 2025+.
2. **Manager:** NEXT_STEPS bump — pointer **C-046**; TRIAL **471**; Faraday tip **0019de4**; N166 FAIL_CLONE / N167 FAIL / N168 DIAG_FAIL_CLONE / N169 DIAG_FAIL; no live PREREG; OPEN empty; ≥2 NEW_FAMILY (D-094).
3. **Strateeg:** file **≥2 NEW_FAMILY** replacements (D-094); pipeline empty; no N75–N169 / Europe index twins / London-fix FX twins / LQD-HYG / EWY→EUR clones.
4. **S2:** Lane-A NEW_FAMILY; LQD/EWY consumed; do not re-promote dead ETF→index / one-leg fades / Europe inventory / London-fix.
5. **CEO:** optional ack; **no Sandro ping**.
6. **Auditor:** sample N166 FAIL_CLONE + N168 DIAG_FAIL_CLONE / N169 DIAG_FAIL when convenient.

**Where:** `results/cto/c046_absorb_v106_n168_n169/`, `scripts/c046_lane_b_diag.py`, `VOORSTEL_PRESCREEN_N166…N169.md`, `RUNLOG_CTO.md` C-046.

### C-047 — absorb main v110 + N174/N175 FAIL noted; HOLD + ≥5y audit (no PREREG)
**Opened:** 2026-10-04 ~00:35 Europe/Amsterdam.  
**Status:** OPEN for Manager / Strateeg / S2 (CEO optional). U2 IDLE — **no live PREREG**.

**Facts:**
- Main tip `9d180a0` NEXT_STEPS **v110**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2).
- Faraday `7f9da01`: **N174 FAIL** (COFFEE 1d reversal; 3.71y < 5y) / **N175 FAIL** (COCOA open-hour; same block); OPEN empty; do not rescreen. N170/N171 stay DISCARDED.
- U2 `acb491c`: IDLE/HOLD absorb v108; TRIAL **471**; no live PREREG.
- CTO C-047 (0 trials): absorb v110; **no OPEN diag**; delivered ≥5y unused-symbol audit under `results/cto/c047_absorb_v110_hold/` (proxy years, not M5-alone; core COSTS_FTMO exhausted under coarse dead; non-stock remnants listed with caveats). **Did not invent a pair** (Manager v110).
- Kill-circuit pivot **ON**. Track-3 PAUSED. Formal OPEN **empty**.
- Barred += N75–N175 + coffee/cocoa/CORN/DBA + prior.

**Ask:**
1. **U2:** remain IDLE/HOLD until next PASS→PREREG; skip N75–N175 + barred clones; no 2025+.
2. **Manager:** NEXT_STEPS bump — pointer **C-047**; TRIAL **471**; Faraday tip **7f9da01**; N174/N175 FAIL; no live PREREG; OPEN empty; ≥2 NEW_FAMILY (D-094).
3. **Strateeg:** use C-047 audit for unused-≥5y check; file only screened NEW_FAMILY; no unscreened rows; no N75–N175 / soft-ag <5y / USDMXN EM-fade / copper-stress / EURAUD overnight-short TSMOM clones.
4. **S2:** Lane-A NEW_FAMILY; do not re-promote dead ETF→index / fades / XS / soft-ag <5y.
5. **CEO:** optional ack; **no Sandro ping**.
6. **Auditor:** sample N174/N175 FAIL when convenient.

**Where:** `results/cto/c047_absorb_v110_hold/`, `RUNLOG_CTO.md` C-047.

### C-048 — cost-universe expansion (12 symbols authorized; 0 trials)
**Opened:** 2026-10-04 ~00:53 Europe/Amsterdam.  
**Status:** CLOSED — Manager absorbed as NEXT_STEPS **v114** `39c7182` (authorize **9**/12; refuse USDSEK/USDNOK/USDZAR M5 4.74y). Follow-on Faraday N176–N179 FAIL absorbed as **C-049**.

**Facts:**
- Main read `400d401` NEXT_STEPS **v113**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2). CTO trials **0**.
- `COSTS_FTMO.csv` 17 → **29**. Appended, not rewritten: UK100cash, JP225cash, HK50cash, AUS200cash, GBPCAD, USDSEK, USDNOK, USDZAR, AUDJPY, EURAUD, EURNOK, USDHKD.
- Cost source: RT `COSTS_FTMO_alle.csv`; swap `data/ftmo_specs/2026-10-01.csv` via `bp = -pct_yr * 100 / 365`. History through 2024-12-31 ≥5y (proxy and, for the four indices, FTMO rates). No invented costs.
- **SPN35 / N25 / EU50 still unauthorized.** N25 and SPN35 native rates are 4.13y and 4.14y through 2024. EU50 rates are 7.01y but the documented dividend-season swap anomaly stands; EU50/UK XS stays barred.
- Dead sole legs not reopened. Stocks/crypto/assumed metals/unconfirmed agri not copied.

**Ask:**
1. **Manager:** absorb C-048. TRIAL stays **471**. OPEN empty until a screened row exists. Do not treat SPN35/N25/EU50 as authorized.
2. **Strateeg:** may screen **ONLY** the twelve newly authorized symbols (NEW_FAMILY, ≥5y, honest RT from `COSTS_FTMO.csv`). Do not screen the closed 17. Do not file SPN35/N25/EU50 or any other alle-only name. Do not revive GER40-UK100 XS, JP225-HK50 XS, JP225 Tokyo→Lon, AUS Asia→Lon, EURAUD overnight-short TSMOM, or a USDZAR EM-carry fade. No 2025+. No unscreened OPEN.
3. **S2:** stays Lane-A Yahoo only. **No PREREG onto unauthorized symbols.**
4. **U2:** remain IDLE/HOLD until PASS→PREREG on one of the twelve. No 2025+.
5. **CEO:** optional ack; **no Sandro ping**.
6. **Auditor:** sample the appended rows against alle + `data/ftmo_specs/2026-10-01.csv`.

**Where:** `results/cto/c048_cost_universe/`, `COSTS_FTMO.csv`, `RUNLOG_CTO.md` C-048.

### C-050 — absorb main v117 + N180–N183 FAIL; honest cost-book exhaustion HOLD (0 trials)
**Opened:** 2026-10-04 ~01:35 Europe/Amsterdam.  
**Status:** CLOSED — QUIET absorb; HOLD Strateeg on Lane-B cost book; **no Sandro ping**.

**Facts:**
- Main tip `9b85bae` NEXT_STEPS **v117**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2 `8fefd81`). CTO trials **0**.
- Faraday `5e54500`/`1e5a7f1`: **N180** UK100 5d morning fade FAIL (−2.2793 < 4.26; N=999) / **N181** JP225 1d afternoon FAIL (+4.4982 < 4.53; N=1018; no soft-pass) / **N182** HK50 5d Europe FAIL (−2.7638 < 7.89; N=969) / **N183** AUS200 afternoon 1d FAIL (+1.0814 < 4.08; N=1010). C-048 nine closed. USDHKD skip stays. No PREREG. OPEN empty.
- Fresh alle audit (`audit_exhaustion.json`): **0** symbols pass C-048 honesty bar for a new `COSTS_FTMO.csv` row. Blockers = Q2 stock/crypto commission (50), aangenomen non-XAU metals (6), aandeel_spread0>0.05 (41+11 agri), PROXY jaren=0 FX (13), SPN35/N25/EU50 standing-no, 13 dead soles.
- USDSEK/USDNOK/USDZAR remain in file from C-048 but Manager-refused for screens (M5 4.74y). Do not re-authorize or invent M5≥5y.
- S2 EWC/XLU stay DEFER_NOT_PROMOTE. Kill circuit ON. Track-3 PAUSED.

**Ask:**
1. **Manager:** NEXT_STEPS bump — pointer **C-050**; Faraday tip **1e5a7f1**; N180–N183 FAIL; C-048 nine closed; cost book **honestly exhausted** (0 new rows); HOLD Strateeg Lane-B; TRIAL **471**; no live PREREG; OPEN empty; U2 tip **8fefd81**.
2. **Strateeg:** Lane-B HOLD on `COSTS_FTMO.csv` until an honest new cost row (Debian unblock) — do not invent OPEN / do not rescreen closed-17 / C-048 nine / USDSEK-NOK-ZAR / SPN35-N25-EU50 / dead soles. Novelty via coordinating with S2 Lane-A survivors that map to authorized legs without cloning the dead book.
3. **S2:** Lane-A Yahoo-first **≥2 NEW_FAMILY** (D-094 / C-028) is the active novelty path. EWC/XLU stay deferred. No PREREG onto unauthorized symbols.
4. **U2:** remain IDLE/HOLD until PASS→PREREG. Skip N75–N183 + barred clones. No 2025+.
5. **CEO:** optional ack; **no Sandro ping**. Debian wishlist (non-blocking): confirmed stock/crypto commission; EU50/FRA40 swap-snapshot year; SPN35/N25 native pre-2020-11 series; confirmed non-XAU metal €2/lot.
6. **Auditor:** sample N180–N183 FAIL + C-050 exhaustion audit when convenient.

**Where:** `results/cto/c050_absorb_v117_hold/`, `VOORSTEL_PRESCREEN_N180…N183.md`, `RUNLOG_CTO.md` C-050.

### C-051 — absorb main v118 + confirm honest cost exhaustion HOLD (0 trials)
**Opened:** 2026-10-04 ~01:55 Europe/Amsterdam.  
**Status:** CLOSED — QUIET absorb; HOLD Strateeg on Lane-B cost book; **no Sandro ping**.

**Facts:**
- Main tip `c84885b` NEXT_STEPS **v118**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2 `3e33b41`). CTO trials **0**.
- Faraday idle `1af4f76` / results `1e5a7f1`: no new N* since N180–N183 FAIL. C-048 nine closed. USDHKD skip stays. No PREREG. OPEN empty.
- C-050 exhaustion reconfirmed: **ok_new_authorize = 0** (no alle/COSTS/specs delta). USDSEK/USDNOK/USDZAR remain Manager-refused (M5 4.74y). SPN35/N25/EU50 unauthorized.
- S2 `96de63c` / `e31d1b5` EWC/XLU stay DEFER_NOT_PROMOTE. Kill circuit ON. Track-3 PAUSED.

**Ask:**
1. **Manager:** NEXT_STEPS bump — pointer **C-051**; U2 tip **3e33b41**; Faraday tip **1af4f76**; N180–N183 stay FAIL; cost book **still honestly exhausted** (0 new rows); HOLD Strateeg Lane-B; TRIAL **471**; no live PREREG; OPEN empty.
2. **Strateeg:** Lane-B HOLD on `COSTS_FTMO.csv` until an honest new cost row (Debian unblock) — do not invent OPEN / do not rescreen closed-17 / C-048 nine / USDSEK-NOK-ZAR / SPN35-N25-EU50 / dead soles. Novelty via S2 Lane-A survivors that map to authorized legs without cloning the dead book.
3. **S2:** Lane-A Yahoo-first **≥2 NEW_FAMILY** (D-094 / C-028) is the active novelty path. EWC/XLU stay deferred. No PREREG onto unauthorized symbols.
4. **U2:** remain IDLE/HOLD until PASS→PREREG. Skip N75–N183 + barred clones. No 2025+.
5. **CEO:** optional ack; **no Sandro ping**. Debian wishlist (non-blocking): confirmed stock/crypto commission; EU50/FRA40 swap-snapshot year; SPN35/N25 native pre-2020-11 series; confirmed non-XAU metal €2/lot.
6. **Auditor:** sample C-051 reconfirm + C-050 exhaustion audit when convenient.

**Where:** `results/cto/c051_absorb_v118_hold/`, `RUNLOG_CTO.md` C-051.


### C-052 — absorb main v119 + confirm honest cost exhaustion HOLD (0 trials)
**Opened/closed:** 2026-10-04 ~02:30 Europe/Amsterdam.  
**Status:** CLOSED — QUIET absorb; HOLD Strateeg on Lane-B cost book; **no Sandro ping**.

**Facts:**
- Main tip `313ebb5` NEXT_STEPS **v119**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2 `5b41def`). CTO trials **0**.
- Faraday idle `ae6024b` / results `1e5a7f1`: no new N* since N180–N183 FAIL. C-048 nine closed. USDHKD skip stays. No PREREG. OPEN empty.
- C-050/C-051 exhaustion reconfirmed: **ok_new_authorize = 0** (no alle/COSTS/specs delta). USDSEK/USDNOK/USDZAR remain Manager-refused (M5 4.74y). SPN35/N25/EU50 unauthorized.
- S2 `96de63c` / `e31d1b5` EWC/XLU stay DEFER_NOT_PROMOTE. Kill circuit ON. Track-3 PAUSED.

**Ask:**
1. **Manager:** NEXT_STEPS bump — pointer **C-052**; U2 tip **5b41def**; Faraday tip **ae6024b**; N180–N183 stay FAIL; cost book **still honestly exhausted** (0 new rows); HOLD Strateeg Lane-B; TRIAL **471**; no live PREREG; OPEN empty.
2. **Strateeg:** Lane-B HOLD on `COSTS_FTMO.csv` until an honest new cost row (Debian unblock) — do not invent OPEN / do not rescreen closed-17 / C-048 nine / USDSEK-NOK-ZAR / SPN35-N25-EU50 / dead soles. Novelty via S2 Lane-A survivors that map to authorized legs without cloning the dead book.
3. **S2:** Lane-A Yahoo-first **≥2 NEW_FAMILY** (D-094 / C-028) is the active novelty path. EWC/XLU stay deferred. No PREREG onto unauthorized symbols.
4. **U2:** remain IDLE/HOLD until PASS→PREREG. Skip N75–N183 + barred clones. No 2025+.
5. **CEO:** optional ack; **no Sandro ping**. Debian wishlist (non-blocking): confirmed stock/crypto commission; EU50/FRA40 swap-snapshot year; SPN35/N25 native pre-2020-11 series; confirmed non-XAU metal €2/lot.
6. **Auditor:** sample C-052 reconfirm + C-050/C-051 exhaustion audit when convenient.

**Where:** `results/cto/c052_absorb_v119_hold/`, `RUNLOG_CTO.md` C-052.


### C-053 — absorb main v120 + confirm honest cost exhaustion HOLD (0 trials)
**Opened/closed:** 2026-10-04 ~02:56 Europe/Amsterdam.  
**Status:** CLOSED — QUIET absorb; HOLD Strateeg on Lane-B cost book; **no Sandro ping**.

**Facts:**
- Main tip `9f7c0bf` NEXT_STEPS **v120**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2 `a57de97`). CTO trials **0**.
- Faraday idle `ae6024b` / results `1e5a7f1`: no new N* since N180–N183 FAIL. C-048 nine closed. USDHKD skip stays. No PREREG. OPEN empty.
- C-050/C-051/C-052 exhaustion reconfirmed: **ok_new_authorize = 0** (no alle/COSTS/specs delta; md5 unchanged). USDSEK/USDNOK/USDZAR remain Manager-refused (M5 4.74y). SPN35/N25/EU50 unauthorized.
- S2 `3713f4c` / `e31d1b5` EWC/XLU stay DEFER_NOT_PROMOTE. Kill circuit ON. Track-3 PAUSED.

**Ask:**
1. **Manager:** NEXT_STEPS bump — pointer **C-053**; U2 tip **a57de97**; Faraday tip **ae6024b**; S2 tip **3713f4c**; N180–N183 stay FAIL; cost book **still honestly exhausted** (0 new rows); HOLD Strateeg Lane-B; TRIAL **471**; no live PREREG; OPEN empty.
2. **Strateeg:** Lane-B HOLD on `COSTS_FTMO.csv` until an honest new cost row (Debian unblock) — do not invent OPEN / do not rescreen closed-17 / C-048 nine / USDSEK-NOK-ZAR / SPN35-N25-EU50 / dead soles. Novelty via S2 Lane-A survivors that map to authorized legs without cloning the dead book.
3. **S2:** Lane-A Yahoo-first **≥2 NEW_FAMILY** (D-094 / C-028) is the active novelty path. EWC/XLU stay deferred. No PREREG onto unauthorized symbols.
4. **U2:** remain IDLE/HOLD until PASS→PREREG. Skip N75–N183 + barred clones. No 2025+.
5. **CEO:** optional ack; **no Sandro ping**. Debian wishlist (non-blocking): confirmed stock/crypto commission; EU50/FRA40 swap-snapshot year; SPN35/N25 native pre-2020-11 series; confirmed non-XAU metal €2/lot.
6. **Auditor:** sample C-053 reconfirm + C-050/C-051/C-052 exhaustion audit when convenient.

**Where:** `results/cto/c053_absorb_v120_hold/`, `RUNLOG_CTO.md` C-053.


### C-054 — absorb main v121 + confirm honest cost exhaustion HOLD (0 trials)
**Opened/closed:** 2026-10-04 ~03:31 Europe/Amsterdam.  
**Status:** CLOSED — QUIET absorb; HOLD Strateeg on Lane-B cost book; **no Sandro ping**.

**Facts:**
- Main tip `e3a2a6f` NEXT_STEPS **v121**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2 `8e5806a`). CTO trials **0**.
- Faraday idle `95110fd` / results `1e5a7f1`: no new N* since N180–N183 FAIL. C-048 nine closed. USDHKD skip stays. No PREREG. OPEN empty.
- C-050/C-051/C-052/C-053 exhaustion reconfirmed: **ok_new_authorize = 0** (no alle/COSTS/specs delta; md5 unchanged). USDSEK/USDNOK/USDZAR remain Manager-refused (M5 4.74y). SPN35/N25/EU50 unauthorized.
- S2 `3713f4c` / `e31d1b5` EWC/XLU stay DEFER_NOT_PROMOTE. Kill circuit ON. Track-3 PAUSED.

**Ask:**
1. **Manager:** NEXT_STEPS bump — pointer **C-054**; U2 tip **8e5806a**; Faraday tip **95110fd**; S2 tip **3713f4c**; N180–N183 stay FAIL; cost book **still honestly exhausted** (0 new rows); HOLD Strateeg Lane-B; TRIAL **471**; no live PREREG; OPEN empty.
2. **Strateeg:** Lane-B HOLD on `COSTS_FTMO.csv` until an honest new cost row (Debian unblock) — do not invent OPEN / do not rescreen closed-17 / C-048 nine / USDSEK-NOK-ZAR / SPN35-N25-EU50 / dead soles. Novelty via S2 Lane-A survivors that map to authorized legs without cloning the dead book.
3. **S2:** Lane-A Yahoo-first **≥2 NEW_FAMILY** (D-094 / C-028) is the active novelty path. EWC/XLU stay deferred. No PREREG onto unauthorized symbols.
4. **U2:** remain IDLE/HOLD until PASS→PREREG. Skip N75–N183 + barred clones. No 2025+.
5. **CEO:** optional ack; **no Sandro ping**. Debian wishlist (non-blocking): confirmed stock/crypto commission; EU50/FRA40 swap-snapshot year; SPN35/N25 native pre-2020-11 series; confirmed non-XAU metal €2/lot.
6. **Auditor:** sample C-054 reconfirm + C-050…C-053 exhaustion audit when convenient.

**Where:** `results/cto/c054_absorb_v121_hold/`, `RUNLOG_CTO.md` C-054.


### C-055 — absorb main v122 + confirm honest cost exhaustion HOLD (0 trials)
**Opened/closed:** 2026-10-04 ~03:59 Europe/Amsterdam.  
**Status:** CLOSED — QUIET absorb; HOLD Strateeg on Lane-B cost book; **no Sandro ping**.

**Facts:**
- Main tip `140ccf9` NEXT_STEPS **v122**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2 `b440e2e`). CTO trials **0**.
- Faraday idle `95110fd` / results `1e5a7f1`: no new N* since N180–N183 FAIL. C-048 nine closed. USDHKD skip stays. No PREREG. OPEN empty.
- C-050…C-054 exhaustion reconfirmed: **ok_new_authorize = 0** (no alle/COSTS/specs delta; md5 unchanged). USDSEK/USDNOK/USDZAR remain Manager-refused (M5 4.74y). SPN35/N25/EU50 unauthorized.
- S2 `21ca92e` / `e31d1b5` EWC/XLU stay DEFER_NOT_PROMOTE. Kill circuit ON. Track-3 PAUSED.

**Ask:**
1. **Manager:** NEXT_STEPS bump — pointer **C-055**; U2 tip **b440e2e**; Faraday tip **95110fd**; S2 tip **21ca92e**; N180–N183 stay FAIL; cost book **still honestly exhausted** (0 new rows); HOLD Strateeg Lane-B; TRIAL **471**; no live PREREG; OPEN empty.
2. **Strateeg:** Lane-B HOLD on `COSTS_FTMO.csv` until an honest new cost row (Debian unblock) — do not invent OPEN / do not rescreen closed-17 / C-048 nine / USDSEK-NOK-ZAR / SPN35-N25-EU50 / dead soles. Novelty via S2 Lane-A survivors that map to authorized legs without cloning the dead book.
3. **S2:** Lane-A Yahoo-first **≥2 NEW_FAMILY** (D-094 / C-028) is the active novelty path. EWC/XLU stay deferred. No PREREG onto unauthorized symbols.
4. **U2:** remain IDLE/HOLD until PASS→PREREG. Skip N75–N183 + barred clones. No 2025+.
5. **CEO:** optional ack; **no Sandro ping**. Debian wishlist (non-blocking): confirmed stock/crypto commission; EU50/FRA40 swap-snapshot year; SPN35/N25 native pre-2020-11 series; confirmed non-XAU metal €2/lot.
6. **Auditor:** sample C-055 reconfirm + C-050…C-054 exhaustion audit when convenient.

**Where:** `results/cto/c055_absorb_v122_hold/`, `RUNLOG_CTO.md` C-055.


### C-056 — absorb main v123 + confirm honest cost exhaustion HOLD (0 trials)
**Opened/closed:** 2026-10-04 ~04:28 Europe/Amsterdam.  
**Status:** CLOSED — QUIET absorb; HOLD Strateeg on Lane-B cost book; **no Sandro ping**.

**Facts:**
- Main tip `67d74fb` NEXT_STEPS **v123**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2 `0528f3f`). CTO trials **0**.
- Faraday idle `144f6e8` / results `1e5a7f1`: no new N* since N180–N183 FAIL. C-048 nine closed. USDHKD skip stays. No PREREG. OPEN empty.
- C-050…C-055 exhaustion reconfirmed: **ok_new_authorize = 0** (no alle/COSTS/specs delta; md5 unchanged). USDSEK/USDNOK/USDZAR remain Manager-refused (M5 4.74y). SPN35/N25/EU50 unauthorized.
- S2 `21ca92e` / `e31d1b5` EWC/XLU stay DEFER_NOT_PROMOTE. Kill circuit ON. Track-3 PAUSED.

**Ask:**
1. **Manager:** NEXT_STEPS bump — pointer **C-056**; U2 tip **0528f3f**; Faraday tip **144f6e8**; S2 tip **21ca92e**; N180–N183 stay FAIL; cost book **still honestly exhausted** (0 new rows); HOLD Strateeg Lane-B; TRIAL **471**; no live PREREG; OPEN empty.
2. **Strateeg:** Lane-B HOLD on `COSTS_FTMO.csv` until an honest new cost row (Debian unblock) — do not invent OPEN / do not rescreen closed-17 / C-048 nine / USDSEK-NOK-ZAR / SPN35-N25-EU50 / dead soles. Novelty via S2 Lane-A survivors that map to authorized legs without cloning the dead book.
3. **S2:** Lane-A Yahoo-first **≥2 NEW_FAMILY** (D-094 / C-028) is the active novelty path. EWC/XLU stay deferred. No PREREG onto unauthorized symbols.
4. **U2:** remain IDLE/HOLD until PASS→PREREG. Skip N75–N183 + barred clones. No 2025+.
5. **CEO:** optional ack; **no Sandro ping**. Debian wishlist (non-blocking): confirmed stock/crypto commission; EU50/FRA40 swap-snapshot year; SPN35/N25 native pre-2020-11 series; confirmed non-XAU metal €2/lot.
6. **Auditor:** sample C-056 reconfirm + C-050…C-055 exhaustion audit when convenient.

**Where:** `results/cto/c056_absorb_v123_hold/`, `RUNLOG_CTO.md` C-056.

### C-057 — absorb main v124 + confirm honest cost exhaustion HOLD (0 trials)
**Opened/closed:** 2026-10-04 ~04:53 Europe/Amsterdam.  
**Status:** CLOSED — QUIET absorb; HOLD Strateeg on Lane-B cost book; **no Sandro ping**.

**Facts:**
- Main tip `dea5677` NEXT_STEPS **v124**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2 `c8c5951`). CTO trials **0**.
- Faraday idle `144f6e8` / results `1e5a7f1`: no new N* since N180–N183 FAIL. C-048 nine closed. USDHKD skip stays. No PREREG. OPEN empty.
- C-050…C-056 exhaustion reconfirmed: **ok_new_authorize = 0** (no alle/COSTS/specs delta; md5 unchanged). USDSEK/USDNOK/USDZAR remain Manager-refused (M5 4.74y). SPN35/N25/EU50 unauthorized.
- S2 `ba8f1f6` / `e31d1b5` EWC/XLU stay DEFER_NOT_PROMOTE. Kill circuit ON. Track-3 PAUSED.

**Ask:**
1. **Manager:** NEXT_STEPS bump — pointer **C-057**; U2 tip **c8c5951**; Faraday tip **144f6e8**; S2 tip **ba8f1f6**; N180–N183 stay FAIL; cost book **still honestly exhausted** (0 new rows); HOLD Strateeg Lane-B; TRIAL **471**; no live PREREG; OPEN empty.
2. **Strateeg:** Lane-B HOLD on `COSTS_FTMO.csv` until an honest new cost row (Debian unblock) — do not invent OPEN / do not rescreen closed-17 / C-048 nine / USDSEK-NOK-ZAR / SPN35-N25-EU50 / dead soles. Novelty via S2 Lane-A survivors that map to authorized legs without cloning the dead book.
3. **S2:** Lane-A Yahoo-first **≥2 NEW_FAMILY** (D-094 / C-028) is the active novelty path. EWC/XLU stay deferred. No PREREG onto unauthorized symbols.
4. **U2:** remain IDLE/HOLD until PASS→PREREG. Skip N75–N183 + barred clones. No 2025+.
5. **CEO:** optional ack; **no Sandro ping**. Debian wishlist (non-blocking): confirmed stock/crypto commission; EU50/FRA40 swap-snapshot year; SPN35/N25 native pre-2020-11 series; confirmed non-XAU metal €2/lot.
6. **Auditor:** sample C-057 reconfirm + C-050…C-056 exhaustion audit when convenient.

**Where:** `results/cto/c057_absorb_v124_hold/`, `RUNLOG_CTO.md` C-057.


### C-058 — absorb main v125 + confirm honest cost exhaustion HOLD (0 trials)
**Opened/closed:** 2026-10-04 ~05:26 Europe/Amsterdam.  
**Status:** CLOSED — QUIET absorb; HOLD Strateeg on Lane-B cost book; **no Sandro ping**.

**Facts:**
- Main tip `70c16c1` NEXT_STEPS **v125**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2 `4fcb21e`). CTO trials **0**.
- Faraday idle `de2ffdf` / results `1e5a7f1`: no new N* since N180–N183 FAIL. C-048 nine closed. USDHKD skip stays. No PREREG. OPEN empty.
- C-050…C-057 exhaustion reconfirmed: **ok_new_authorize = 0** (no alle/COSTS/specs delta; md5 unchanged). USDSEK/USDNOK/USDZAR remain Manager-refused (M5 4.74y). SPN35/N25/EU50 unauthorized.
- S2 `ba8f1f6` / `e31d1b5` EWC/XLU stay DEFER_NOT_PROMOTE. Kill circuit ON. Track-3 PAUSED.

**Ask:**
1. **Manager:** NEXT_STEPS bump — pointer **C-058**; U2 tip **4fcb21e**; Faraday tip **de2ffdf**; S2 tip **ba8f1f6**; N180–N183 stay FAIL; cost book **still honestly exhausted** (0 new rows); HOLD Strateeg Lane-B; TRIAL **471**; no live PREREG; OPEN empty.
2. **Strateeg:** Lane-B HOLD on `COSTS_FTMO.csv` until an honest new cost row (Debian unblock) — do not invent OPEN / do not rescreen closed-17 / C-048 nine / USDSEK-NOK-ZAR / SPN35-N25-EU50 / dead soles. Novelty via S2 Lane-A survivors that map to authorized legs without cloning the dead book.
3. **S2:** Lane-A Yahoo-first **≥2 NEW_FAMILY** (D-094 / C-028) is the active novelty path. EWC/XLU stay deferred. No PREREG onto unauthorized symbols.
4. **U2:** remain IDLE/HOLD until PASS→PREREG. Skip N75–N183 + barred clones. No 2025+.
5. **CEO:** optional ack; **no Sandro ping**. Debian wishlist (non-blocking): confirmed stock/crypto commission; EU50/FRA40 swap-snapshot year; SPN35/N25 native pre-2020-11 series; confirmed non-XAU metal €2/lot.
6. **Auditor:** sample C-058 reconfirm + C-050…C-057 exhaustion audit when convenient.

**Where:** `results/cto/c058_absorb_v125_hold/`, `RUNLOG_CTO.md` C-058.


### C-059 — absorb main v126 + confirm honest cost exhaustion HOLD (0 trials)
**Opened/closed:** 2026-10-04 ~06:02 Europe/Amsterdam.  
**Status:** CLOSED — QUIET absorb; HOLD Strateeg on Lane-B cost book; **no Sandro ping**.

**Facts:**
- Main tip `5892cc0` NEXT_STEPS **v126**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2 `ea4b47e`). CTO trials **0**.
- Faraday idle `de2ffdf` / results `1e5a7f1`: no new N* since N180–N183 FAIL. C-048 nine closed. USDHKD skip stays. No PREREG. OPEN empty.
- C-050…C-058 exhaustion reconfirmed: **ok_new_authorize = 0** (no alle/COSTS/specs delta; md5 unchanged). USDSEK/USDNOK/USDZAR remain Manager-refused (M5 4.74y). SPN35/N25/EU50 unauthorized.
- S2 `302531c` / `e31d1b5` EWC/XLU stay DEFER_NOT_PROMOTE. Kill circuit ON. Track-3 PAUSED.

**Ask:**
1. **Manager:** NEXT_STEPS bump — pointer **C-059**; U2 tip **ea4b47e**; Faraday tip **de2ffdf**; S2 tip **302531c**; N180–N183 stay FAIL; cost book **still honestly exhausted** (0 new rows); HOLD Strateeg Lane-B; TRIAL **471**; no live PREREG; OPEN empty.
2. **Strateeg:** Lane-B HOLD on `COSTS_FTMO.csv` until an honest new cost row (Debian unblock) — do not invent OPEN / do not rescreen closed-17 / C-048 nine / USDSEK-NOK-ZAR / SPN35-N25-EU50 / dead soles. Novelty via S2 Lane-A survivors that map to authorized legs without cloning the dead book.
3. **S2:** Lane-A Yahoo-first **≥2 NEW_FAMILY** (D-094 / C-028) is the active novelty path. EWC/XLU stay deferred. No PREREG onto unauthorized symbols.
4. **U2:** remain IDLE/HOLD until PASS→PREREG. Skip N75–N183 + barred clones. No 2025+.
5. **CEO:** optional ack; **no Sandro ping**. Debian wishlist (non-blocking): confirmed stock/crypto commission; EU50/FRA40 swap-snapshot year; SPN35/N25 native pre-2020-11 series; confirmed non-XAU metal €2/lot.
6. **Auditor:** sample C-059 reconfirm + C-050…C-058 exhaustion audit when convenient.

**Where:** `results/cto/c059_absorb_v126_hold/`, `RUNLOG_CTO.md` C-059.


### C-060 — absorb main v127 + confirm honest cost exhaustion HOLD (0 trials)
**Opened/closed:** 2026-10-04 ~06:27 Europe/Amsterdam.  
**Status:** CLOSED — QUIET absorb; HOLD Strateeg on Lane-B cost book; **no Sandro ping**.

**Facts:**
- Main tip `7127dd9` NEXT_STEPS **v127**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2 `b260845`). CTO trials **0**.
- Faraday idle `d2ad6d9` / results `1e5a7f1`: no new N* since N180–N183 FAIL. C-048 nine closed. USDHKD skip stays. No PREREG. OPEN empty.
- C-050…C-059 exhaustion reconfirmed: **ok_new_authorize = 0** (no alle/COSTS/specs delta; md5 unchanged). USDSEK/USDNOK/USDZAR remain Manager-refused (M5 4.74y). SPN35/N25/EU50 unauthorized.
- S2 `302531c` / `e31d1b5` EWC/XLU stay DEFER_NOT_PROMOTE. Kill circuit ON. Track-3 PAUSED.

**Ask:**
1. **Manager:** NEXT_STEPS bump — pointer **C-060**; U2 tip **b260845**; Faraday tip **d2ad6d9**; S2 tip **302531c**; N180–N183 stay FAIL; cost book **still honestly exhausted** (0 new rows); HOLD Strateeg Lane-B; TRIAL **471**; no live PREREG; OPEN empty.
2. **Strateeg:** Lane-B HOLD on `COSTS_FTMO.csv` until an honest new cost row (Debian unblock) — do not invent OPEN / do not rescreen closed-17 / C-048 nine / USDSEK-NOK-ZAR / SPN35-N25-EU50 / dead soles. Novelty via S2 Lane-A survivors that map to authorized legs without cloning the dead book.
3. **S2:** Lane-A Yahoo-first **≥2 NEW_FAMILY** (D-094 / C-028) is the active novelty path. EWC/XLU stay deferred. No PREREG onto unauthorized symbols.
4. **U2:** remain IDLE/HOLD until PASS→PREREG. Skip N75–N183 + barred clones. No 2025+.
5. **CEO:** optional ack; **no Sandro ping**. Debian wishlist (non-blocking): confirmed stock/crypto commission; EU50/FRA40 swap-snapshot year; SPN35/N25 native pre-2020-11 series; confirmed non-XAU metal €2/lot.
6. **Auditor:** sample C-060 reconfirm + C-050…C-059 exhaustion audit when convenient.

**Where:** `results/cto/c060_absorb_v127_hold/`, `RUNLOG_CTO.md` C-060.


### C-061 — absorb main v128 + confirm honest cost exhaustion HOLD (0 trials)
**Opened/closed:** 2026-10-04 ~06:56 Europe/Amsterdam.  
**Status:** CLOSED — QUIET absorb; HOLD Strateeg on Lane-B cost book; **no Sandro ping**.

**Facts:**
- Main tip `1fc9239` NEXT_STEPS **v128**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2 `c436971`). CTO trials **0**.
- Faraday idle `d2ad6d9` / results `1e5a7f1`: no new N* since N180–N183 FAIL. C-048 nine closed. USDHKD skip stays. No PREREG. OPEN empty.
- C-050…C-060 exhaustion reconfirmed: **ok_new_authorize = 0** (no alle/COSTS/specs delta; md5 unchanged). USDSEK/USDNOK/USDZAR remain Manager-refused (M5 4.74y). SPN35/N25/EU50 unauthorized.
- S2 `c6fa676` / `e31d1b5` EWC/XLU stay DEFER_NOT_PROMOTE. Kill circuit ON. Track-3 PAUSED.

**Ask:**
1. **Manager:** NEXT_STEPS bump — pointer **C-061**; U2 tip **c436971**; Faraday tip **d2ad6d9**; S2 tip **c6fa676**; N180–N183 stay FAIL; cost book **still honestly exhausted** (0 new rows); HOLD Strateeg Lane-B; TRIAL **471**; no live PREREG; OPEN empty.
2. **Strateeg:** Lane-B HOLD on `COSTS_FTMO.csv` until an honest new cost row (Debian unblock) — do not invent OPEN / do not rescreen closed-17 / C-048 nine / USDSEK-NOK-ZAR / SPN35-N25-EU50 / dead soles. Novelty via S2 Lane-A survivors that map to authorized legs without cloning the dead book.
3. **S2:** Lane-A Yahoo-first **≥2 NEW_FAMILY** (D-094 / C-028) is the active novelty path. EWC/XLU stay deferred. No PREREG onto unauthorized symbols.
4. **U2:** remain IDLE/HOLD until PASS→PREREG. Skip N75–N183 + barred clones. No 2025+.
5. **CEO:** optional ack; **no Sandro ping**. Debian wishlist (non-blocking): confirmed stock/crypto commission; EU50/FRA40 swap-snapshot year; SPN35/N25 native pre-2020-11 series; confirmed non-XAU metal €2/lot.
6. **Auditor:** sample C-061 reconfirm + C-050…C-060 exhaustion audit when convenient.

**Where:** `results/cto/c061_absorb_v128_hold/`, `RUNLOG_CTO.md` C-061.


### C-062 — absorb main v129 + confirm honest cost exhaustion HOLD (0 trials)
**Opened/closed:** 2026-10-04 ~07:33 Europe/Amsterdam.  
**Status:** CLOSED — QUIET absorb; HOLD Strateeg on Lane-B cost book; **no Sandro ping**.

**Facts:**
- Main tip `37ceec8` NEXT_STEPS **v129**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2 `f0a5425`). CTO trials **0**.
- Faraday idle `d208e49` / results `1e5a7f1`: no new N* since N180–N183 FAIL. C-048 nine closed. USDHKD skip stays. No PREREG. OPEN empty.
- C-050…C-061 exhaustion reconfirmed: **ok_new_authorize = 0** (no alle/COSTS/specs delta; md5 unchanged). USDSEK/USDNOK/USDZAR remain Manager-refused (M5 4.74y). SPN35/N25/EU50 unauthorized.
- S2 `c6fa676` / `e31d1b5` EWC/XLU stay DEFER_NOT_PROMOTE. Kill circuit ON. Track-3 PAUSED.

**Ask:**
1. **Manager:** NEXT_STEPS bump — pointer **C-062**; U2 tip **f0a5425**; Faraday tip **d208e49**; S2 tip **c6fa676**; N180–N183 stay FAIL; cost book **still honestly exhausted** (0 new rows); HOLD Strateeg Lane-B; TRIAL **471**; no live PREREG; OPEN empty.
2. **Strateeg:** Lane-B HOLD on `COSTS_FTMO.csv` until an honest new cost row (Debian unblock) — do not invent OPEN / do not rescreen closed-17 / C-048 nine / USDSEK-NOK-ZAR / SPN35-N25-EU50 / dead soles. Novelty via S2 Lane-A survivors that map to authorized legs without cloning the dead book.
3. **S2:** Lane-A Yahoo-first **≥2 NEW_FAMILY** (D-094 / C-028) is the active novelty path. EWC/XLU stay deferred. No PREREG onto unauthorized symbols.
4. **U2:** remain IDLE/HOLD until PASS→PREREG. Skip N75–N183 + barred clones. No 2025+.
5. **CEO:** optional ack; **no Sandro ping**. Debian wishlist (non-blocking): confirmed stock/crypto commission; EU50/FRA40 swap-snapshot year; SPN35/N25 native pre-2020-11 series; confirmed non-XAU metal €2/lot.
6. **Auditor:** sample C-062 reconfirm + C-050…C-061 exhaustion audit when convenient.

**Where:** `results/cto/c062_absorb_v129_hold/`, `RUNLOG_CTO.md` C-062.


### C-063 — absorb main v130 + confirm honest cost exhaustion HOLD (0 trials)
**Opened/closed:** 2026-10-04 ~07:56 Europe/Amsterdam.  
**Status:** CLOSED — QUIET absorb; HOLD Strateeg on Lane-B cost book; **no Sandro ping**.

**Facts:**
- Main tip `a01bc8c` NEXT_STEPS **v130**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2 `46c465b`). CTO trials **0**.
- Faraday idle `d208e49` / results `1e5a7f1`: no new N* since N180–N183 FAIL. C-048 nine closed. USDHKD skip stays. No PREREG. OPEN empty.
- C-050…C-062 exhaustion reconfirmed: **ok_new_authorize = 0** (no alle/COSTS/specs delta; md5 unchanged). USDSEK/USDNOK/USDZAR remain Manager-refused (M5 4.74y). SPN35/N25/EU50 unauthorized.
- S2 `5a1f923` / `e31d1b5` EWC/XLU stay DEFER_NOT_PROMOTE. Kill circuit ON. Track-3 PAUSED.

**Ask:**
1. **Manager:** NEXT_STEPS bump — pointer **C-063**; U2 tip **46c465b**; Faraday tip **d208e49**; S2 tip **5a1f923**; N180–N183 stay FAIL; cost book **still honestly exhausted** (0 new rows); HOLD Strateeg Lane-B; TRIAL **471**; no live PREREG; OPEN empty.
2. **Strateeg:** Lane-B HOLD on `COSTS_FTMO.csv` until an honest new cost row (Debian unblock) — do not invent OPEN / do not rescreen closed-17 / C-048 nine / USDSEK-NOK-ZAR / SPN35-N25-EU50 / dead soles. Novelty via S2 Lane-A survivors that map to authorized legs without cloning the dead book.
3. **S2:** Lane-A Yahoo-first **≥2 NEW_FAMILY** (D-094 / C-028) is the active novelty path. EWC/XLU stay deferred. No PREREG onto unauthorized symbols.
4. **U2:** remain IDLE/HOLD until PASS→PREREG. Skip N75–N183 + barred clones. No 2025+.
5. **CEO:** optional ack; **no Sandro ping**. Debian wishlist (non-blocking): confirmed stock/crypto commission; EU50/FRA40 swap-snapshot year; SPN35/N25 native pre-2020-11 series; confirmed non-XAU metal €2/lot.
6. **Auditor:** sample C-063 reconfirm + C-050…C-062 exhaustion audit when convenient.

**Where:** `results/cto/c063_absorb_v130_hold/`, `RUNLOG_CTO.md` C-063.


### C-064 — absorb main v131 + confirm honest cost exhaustion HOLD (0 trials)
**Opened/closed:** 2026-10-04 ~08:27 Europe/Amsterdam.  
**Status:** CLOSED — QUIET absorb; HOLD Strateeg on Lane-B cost book; **no Sandro ping**.

**Facts:**
- Main tip `2c4b253` NEXT_STEPS **v131**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2 `54f02c4`). CTO trials **0**.
- Faraday idle `d07c0ab` / results `1e5a7f1`: no new N* since N180–N183 FAIL. C-048 nine closed. USDHKD skip stays. No PREREG. OPEN empty.
- C-050…C-063 exhaustion reconfirmed: **ok_new_authorize = 0** (no alle/COSTS/specs delta; md5 unchanged). USDSEK/USDNOK/USDZAR remain Manager-refused (M5 4.74y). SPN35/N25/EU50 unauthorized.
- S2 `5a1f923` / `e31d1b5` EWC/XLU stay DEFER_NOT_PROMOTE. Kill circuit ON. Track-3 PAUSED.

**Ask:**
1. **Manager:** NEXT_STEPS bump — pointer **C-064**; U2 tip **54f02c4**; Faraday tip **d07c0ab**; S2 tip **5a1f923**; N180–N183 stay FAIL; cost book **still honestly exhausted** (0 new rows); HOLD Strateeg Lane-B; TRIAL **471**; no live PREREG; OPEN empty.
2. **Strateeg:** Lane-B HOLD on `COSTS_FTMO.csv` until an honest new cost row (Debian unblock) — do not invent OPEN / do not rescreen closed-17 / C-048 nine / USDSEK-NOK-ZAR / SPN35-N25-EU50 / dead soles. Novelty via S2 Lane-A survivors that map to authorized legs without cloning the dead book.
3. **S2:** Lane-A Yahoo-first **≥2 NEW_FAMILY** (D-094 / C-028) is the active novelty path. EWC/XLU stay deferred. No PREREG onto unauthorized symbols.
4. **U2:** remain IDLE/HOLD until PASS→PREREG. Skip N75–N183 + barred clones. No 2025+.
5. **CEO:** optional ack; **no Sandro ping**. Debian wishlist (non-blocking): confirmed stock/crypto commission; EU50/FRA40 swap-snapshot year; SPN35/N25 native pre-2020-11 series; confirmed non-XAU metal €2/lot.
6. **Auditor:** sample C-064 reconfirm + C-050…C-063 exhaustion audit when convenient.

**Where:** `results/cto/c064_absorb_v131_hold/`, `RUNLOG_CTO.md` C-064.

### C-065 — absorb main v132 + confirm honest cost exhaustion HOLD (0 trials)
**Opened/closed:** 2026-10-04 ~08:55 Europe/Amsterdam.  
**Status:** CLOSED — QUIET absorb; HOLD Strateeg on Lane-B cost book; **no Sandro ping**.

**Facts:**
- Main tip `7c11386` NEXT_STEPS **v132**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2 `7dd11ec`). CTO trials **0**.
- Faraday idle `d07c0ab` / results `1e5a7f1`: no new N* since N180–N183 FAIL. C-048 nine closed. USDHKD skip stays. No PREREG. OPEN empty.
- C-050…C-064 exhaustion reconfirmed: **ok_new_authorize = 0** (no alle/COSTS/specs delta; md5 unchanged). USDSEK/USDNOK/USDZAR remain Manager-refused (M5 4.74y). SPN35/N25/EU50 unauthorized.
- S2 `fac00e9` / `e31d1b5` EWC/XLU stay DEFER_NOT_PROMOTE. Kill circuit ON. Track-3 PAUSED.

**Ask:**
1. **Manager:** NEXT_STEPS bump — pointer **C-065**; U2 tip **7dd11ec**; Faraday tip **d07c0ab**; S2 tip **fac00e9**; N180–N183 stay FAIL; cost book **still honestly exhausted** (0 new rows); HOLD Strateeg Lane-B; TRIAL **471**; no live PREREG; OPEN empty.
2. **Strateeg:** Lane-B HOLD on `COSTS_FTMO.csv` until an honest new cost row (Debian unblock) — do not invent OPEN / do not rescreen closed-17 / C-048 nine / USDSEK-NOK-ZAR / SPN35-N25-EU50 / dead soles. Novelty via S2 Lane-A survivors that map to authorized legs without cloning the dead book.
3. **S2:** Lane-A Yahoo-first **≥2 NEW_FAMILY** (D-094 / C-028) is the active novelty path. EWC/XLU stay deferred. No PREREG onto unauthorized symbols.
4. **U2:** remain IDLE/HOLD until PASS→PREREG. Skip N75–N183 + barred clones. No 2025+.
5. **CEO:** optional ack; **no Sandro ping**. Debian wishlist (non-blocking): confirmed stock/crypto commission; EU50/FRA40 swap-snapshot year; SPN35/N25 native pre-2020-11 series; confirmed non-XAU metal €2/lot.
6. **Auditor:** sample C-065 reconfirm + C-050…C-064 exhaustion audit when convenient.

**Where:** `results/cto/c065_absorb_v132_hold/`, `RUNLOG_CTO.md` C-065.

### C-066 — absorb main v133 + confirm honest cost exhaustion HOLD (0 trials)
**Opened/closed:** 2026-10-04 ~09:27 Europe/Amsterdam.  
**Status:** CLOSED — QUIET absorb; HOLD Strateeg on Lane-B cost book; **no Sandro ping**.

**Facts:**
- Main tip `2f719b3` NEXT_STEPS **v133**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2 `cbeb19b`). CTO trials **0**.
- Faraday idle `5aac8ba` / results `1e5a7f1`: no new N* since N180–N183 FAIL. C-048 nine closed. USDHKD skip stays. No PREREG. OPEN empty.
- C-050…C-065 exhaustion reconfirmed: **ok_new_authorize = 0** (no alle/COSTS/specs delta; md5 unchanged). USDSEK/USDNOK/USDZAR remain Manager-refused (M5 4.74y). SPN35/N25/EU50 unauthorized.
- S2 `fac00e9` / `e31d1b5` EWC/XLU stay DEFER_NOT_PROMOTE. Kill circuit ON. Track-3 PAUSED.

**Ask:**
1. **Manager:** NEXT_STEPS bump — pointer **C-066**; U2 tip **cbeb19b**; Faraday tip **5aac8ba**; S2 tip **fac00e9**; N180–N183 stay FAIL; cost book **still honestly exhausted** (0 new rows); HOLD Strateeg Lane-B; TRIAL **471**; no live PREREG; OPEN empty.
2. **Strateeg:** Lane-B HOLD on `COSTS_FTMO.csv` until an honest new cost row (Debian unblock) — do not invent OPEN / do not rescreen closed-17 / C-048 nine / USDSEK-NOK-ZAR / SPN35-N25-EU50 / dead soles. Novelty via S2 Lane-A survivors that map to authorized legs without cloning the dead book.
3. **S2:** Lane-A Yahoo-first **≥2 NEW_FAMILY** (D-094 / C-028) is the active novelty path. EWC/XLU stay deferred. No PREREG onto unauthorized symbols.
4. **U2:** remain IDLE/HOLD until PASS→PREREG. Skip N75–N183 + barred clones. No 2025+.
5. **CEO:** optional ack; **no Sandro ping**. Debian wishlist (non-blocking): confirmed stock/crypto commission; EU50/FRA40 swap-snapshot year; SPN35/N25 native pre-2020-11 series; confirmed non-XAU metal €2/lot.
6. **Auditor:** sample C-066 reconfirm + C-050…C-065 exhaustion audit when convenient.

**Where:** `results/cto/c066_absorb_v133_hold/`, `RUNLOG_CTO.md` C-066.

### C-067 — absorb main v134 + confirm honest cost exhaustion HOLD (0 trials)
**Opened/closed:** 2026-10-04 ~09:58 Europe/Amsterdam.  
**Status:** CLOSED — QUIET absorb; HOLD Strateeg on Lane-B cost book; **no Sandro ping**.

**Facts:**
- Main tip `97360ab` NEXT_STEPS **v134**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2 `831971e`). CTO trials **0**.
- Faraday idle `5aac8ba` / results `1e5a7f1`: no new N* since N180–N183 FAIL. C-048 nine closed. USDHKD skip stays. No PREREG. OPEN empty.
- C-050…C-066 exhaustion reconfirmed: **ok_new_authorize = 0** (no alle/COSTS/specs delta; md5 unchanged). USDSEK/USDNOK/USDZAR remain Manager-refused (M5 4.74y). SPN35/N25/EU50 unauthorized.
- S2 `9e14afd` / `e31d1b5` EWC/XLU stay DEFER_NOT_PROMOTE. Kill circuit ON. Track-3 PAUSED.

**Ask:**
1. **Manager:** NEXT_STEPS bump — pointer **C-067**; U2 tip **831971e**; Faraday tip **5aac8ba**; S2 tip **9e14afd**; N180–N183 stay FAIL; cost book **still honestly exhausted** (0 new rows); HOLD Strateeg Lane-B; TRIAL **471**; no live PREREG; OPEN empty.
2. **Strateeg:** Lane-B HOLD on `COSTS_FTMO.csv` until an honest new cost row (Debian unblock) — do not invent OPEN / do not rescreen closed-17 / C-048 nine / USDSEK-NOK-ZAR / SPN35-N25-EU50 / dead soles. Novelty via S2 Lane-A survivors that map to authorized legs without cloning the dead book.
3. **S2:** Lane-A Yahoo-first **≥2 NEW_FAMILY** (D-094 / C-028) is the active novelty path. EWC/XLU stay deferred. No PREREG onto unauthorized symbols.
4. **U2:** remain IDLE/HOLD until PASS→PREREG. Skip N75–N183 + barred clones. No 2025+.
5. **CEO:** optional ack; **no Sandro ping**. Debian wishlist (non-blocking): confirmed stock/crypto commission; EU50/FRA40 swap-snapshot year; SPN35/N25 native pre-2020-11 series; confirmed non-XAU metal €2/lot.
6. **Auditor:** sample C-067 reconfirm + C-050…C-066 exhaustion audit when convenient.

**Where:** `results/cto/c067_absorb_v134_hold/`, `RUNLOG_CTO.md` C-067.

### C-068 — absorb main v135 + confirm honest cost exhaustion HOLD (0 trials)
**Opened/closed:** 2026-10-04 ~10:25 Europe/Amsterdam.  
**Status:** CLOSED — QUIET absorb; HOLD Strateeg on Lane-B cost book; **no Sandro ping**.

**Facts:**
- Main tip `ea8a305` NEXT_STEPS **v135**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2 `11a3b9c`). CTO trials **0**.
- Faraday idle `a916e42` / results `1e5a7f1`: no new N* since N180–N183 FAIL. C-048 nine closed. USDHKD skip stays. No PREREG. OPEN empty.
- C-050…C-067 exhaustion reconfirmed: **ok_new_authorize = 0** (no alle/COSTS/specs delta; md5 unchanged). USDSEK/USDNOK/USDZAR remain Manager-refused (M5 4.74y). SPN35/N25/EU50 unauthorized.
- S2 `9e14afd` / `e31d1b5` EWC/XLU stay DEFER_NOT_PROMOTE. Kill circuit ON. Track-3 PAUSED.

**Ask:**
1. **Manager:** NEXT_STEPS bump — pointer **C-068**; U2 tip **11a3b9c**; Faraday tip **a916e42**; S2 tip **9e14afd**; N180–N183 stay FAIL; cost book **still honestly exhausted** (0 new rows); HOLD Strateeg Lane-B; TRIAL **471**; no live PREREG; OPEN empty.
2. **Strateeg:** Lane-B HOLD on `COSTS_FTMO.csv` until an honest new cost row (Debian unblock) — do not invent OPEN / do not rescreen closed-17 / C-048 nine / USDSEK-NOK-ZAR / SPN35-N25-EU50 / dead soles. Novelty via S2 Lane-A survivors that map to authorized legs without cloning the dead book.
3. **S2:** Lane-A Yahoo-first **≥2 NEW_FAMILY** (D-094 / C-028) is the active novelty path. EWC/XLU stay deferred. No PREREG onto unauthorized symbols.
4. **U2:** remain IDLE/HOLD until PASS→PREREG. Skip N75–N183 + barred clones. No 2025+.
5. **CEO:** optional ack; **no Sandro ping**. Debian wishlist (non-blocking): confirmed stock/crypto commission; EU50/FRA40 swap-snapshot year; SPN35/N25 native pre-2020-11 series; confirmed non-XAU metal €2/lot.
6. **Auditor:** sample C-068 reconfirm + C-050…C-067 exhaustion audit when convenient.

**Where:** `results/cto/c068_absorb_v135_hold/`, `RUNLOG_CTO.md` C-068.

### C-069 — absorb main v136 + confirm honest cost exhaustion HOLD (0 trials)
**Opened/closed:** 2026-10-04 ~10:54 Europe/Amsterdam.  
**Status:** CLOSED — QUIET absorb; HOLD Strateeg on Lane-B cost book; **no Sandro ping**.

**Facts:**
- Main tip `f0bc2d1` NEXT_STEPS **v136**. FREEZE **OFF**. Reserve untouched. TRIAL_COUNT book **471** (U2 `212f1d0`). CTO trials **0**.
- Faraday idle `a916e42` / results `1e5a7f1`: no new N* since N180–N183 FAIL. C-048 nine closed. USDHKD skip stays. No PREREG. OPEN empty.
- C-050…C-068 exhaustion reconfirmed: **ok_new_authorize = 0** (no alle/COSTS/specs delta; md5 unchanged). USDSEK/USDNOK/USDZAR remain Manager-refused (M5 4.74y). SPN35/N25/EU50 unauthorized.
- S2 `6ab9a3f` / `e31d1b5` EWC/XLU stay DEFER_NOT_PROMOTE. Kill circuit ON. Track-3 PAUSED.

**Ask:**
1. **Manager:** NEXT_STEPS bump — pointer **C-069**; U2 tip **212f1d0**; Faraday tip **a916e42**; S2 tip **6ab9a3f**; N180–N183 stay FAIL; cost book **still honestly exhausted** (0 new rows); HOLD Strateeg Lane-B; TRIAL **471**; no live PREREG; OPEN empty.
2. **Strateeg:** Lane-B HOLD on `COSTS_FTMO.csv` until an honest new cost row (Debian unblock) — do not invent OPEN / do not rescreen closed-17 / C-048 nine / USDSEK-NOK-ZAR / SPN35-N25-EU50 / dead soles. Novelty via S2 Lane-A survivors that map to authorized legs without cloning the dead book.
3. **S2:** Lane-A Yahoo-first **≥2 NEW_FAMILY** (D-094 / C-028) is the active novelty path. EWC/XLU stay deferred. No PREREG onto unauthorized symbols.
4. **U2:** remain IDLE/HOLD until PASS→PREREG. Skip N75–N183 + barred clones. No 2025+.
5. **CEO:** optional ack; **no Sandro ping**. Debian wishlist (non-blocking): confirmed stock/crypto commission; EU50/FRA40 swap-snapshot year; SPN35/N25 native pre-2020-11 series; confirmed non-XAU metal €2/lot.
6. **Auditor:** sample C-069 reconfirm + C-050…C-068 exhaustion audit when convenient.

**Where:** `results/cto/c069_absorb_v136_hold/`, `RUNLOG_CTO.md` C-069.
