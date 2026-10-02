# RUNLOG_STRATEEG — Strateeg op `claude/trusting-faraday-34tsmg`

## 2026-10-03 00:24 Europe/Amsterdam — N130/N131 FAIL_T sync; N132/N133 FAIL; OPEN N134/N135

**Branch:** `claude/trusting-faraday-34tsmg` (worktree `/workspace/ai-trading-faraday`; tip was `0af85da`).  
**Trigger:** U2 `03ad9da` **N130 EQW_BREADTH FAIL_T** + **N131 DXY_DOLLAR FAIL_T** (TRIAL **468→470**). Formal OPEN was empty after both had gone live PREREG.

### U2 result (binding)
| ID | Verdict | t / NW | Train mean | Test | Trial |
|----|---------|--------|------------|------|-------|
| N130 EQW_BREADTH_STRESS | FAIL_T (cost+stress PASS) | **1,05 / 1,20** | +6,68 (N=220; netto +5,90; med +1,66; years −0,41/+18,72/−1,71; L/S 99/121) | −3,85 (N=91) | **468→469** |
| N131 DXY_DOLLAR_STRESS | FAIL_T (cost+stress PASS) | **1,01 / 1,05** | +5,08 (N=413; netto +4,30; med +5,22; years −6,69/+5,44/+9,12; L/S 131/282) | −1,10 (N=146) | **469→470** |

Dead += N130 + N131. No thr-grid / EQW or DXY clone / overnight. N131 session 15:30–21:00 **≠ N110**. Live PREREG **cleared**. N124/N125/N127/N128/N130/N131 not re-run.

### D-092.1 `n132_n133` (train 2021–2023; gate 2,34; session-flat US500 15:30→21:00)
| ID | Family | Config | N | mean | med | years | Verdict |
|----|--------|--------|--:|-----:|----:|-------|---------|
| N132 | MTUM_MOM_FACTOR BA | MTUM z40/thr±1,5 stress_buy | **185** | **+1,55** | −0,52 | +11,52 / −6,45 / +4,90 | **FAIL** (L/S 106/79) |
| N133 | GLD_GOLD_HAVEN BB | GLD z120+d20 inverse haven | **361** | **+0,26** | −0,68 | −4,00 / +12,60 / −12,07 | **FAIL** (L/S 146/215) |

### Geleverd
- PREREG N130 + N131 → **STOP FAIL_T**
- OPEN **N134 XLF_FINANCIAL** (BC) + **N135 QUAL_QUALITY** (BD) — not screened
- Catalog §9/§10; TRIAL **470**; live PREREG **none**

### Explicit
- No PREREG (both screens < 2,34). No soft-pass. No U2 wake. Quiet to Sandro. No 2025-reserve. No other branches.



## 2026-10-03 00:17 Europe/Amsterdam — N128 FAIL_T sync; N130/N131 PASS→PREREG

**Branch:** `claude/trusting-faraday-34tsmg` (worktree `/workspace/ai-trading-faraday`; tip was `cb136e0`).  
**Trigger:** U2 `62a7718` **N128 BWX_INTL_TREASURY_STRESS FAIL_T** (TRIAL **467→468**). U2 IDLE. Formal OPEN screens were N130/N131.

### U2 result (binding)
| ID | Verdict | t / NW | Train mean | Test | Trial |
|----|---------|--------|------------|------|-------|
| N128 BWX_INTL_TREASURY_STRESS | FAIL_T (cost+stress PASS) | **1,40 / 1,43** | +6,63 (N=419; netto +5,85; med +8,58; years −8,07/+8,89/+9,55; L/S 96/323) | −2,37 (N=136) | **467→468** |

Dead += N128. No thr-grid / TLT-TIP-EMB-yield rewrite / BWX clone / overnight. Live PREREG N128 **cleared**. N124/N125/N127/N128 not re-run.

### D-092.1 `n130_n131` (train 2021–2023; gate 2,34; session-flat US500 15:30→21:00)
| ID | Family | Config | N | mean | med | years | Verdict |
|----|--------|--------|--:|-----:|----:|-------|---------|
| N130 | EQW_BREADTH AY | SPX_EQW/SPX z40/thr±1,5 stress | **220** | **+6,68** | +1,66 | −0,41 / +18,72 / −1,71 | **PASS_may_PREREG** (L/S 99/121; stress informal PASS ≥3,51) |
| N131 | DXY_DOLLAR AZ | DXY daily z120+d20 **inverse** → US500 | **413** | **+5,08** | +5,22 | −6,69 / +5,44 / +9,12 | **PASS_may_PREREG** (L/S 131/282; stress informal PASS ≥3,51) |

N131 **≠ N110**: not DXYcash M5 Lon-AM 08:00→12:00 same-dir continuation traded 13:00→17:00. Daily Yahoo DXY level, inverse map, US500cash 15:30→21:00, gate 2,34.

### Geleverd
- PREREG N128 → **STOP FAIL_T**
- `PREREG_FTMO_N130_EQW_BREADTH_STRESS.md` **OPEN**
- `PREREG_FTMO_N131_DXY_DOLLAR_STRESS.md` **OPEN**
- Catalog §9/§10; TRIAL **468**; live PREREG **N130+N131** only

### Explicit
- No soft-pass; gate unchanged (2,34).
- Parent wakes U2 ×2 (N130, N131). Quiet to Sandro. No 2025-reserve. No other branches.



## 2026-10-03 00:13 Europe/Amsterdam — N127 FAIL_T sync; N128 PASS→PREREG; N129 FAIL; OPEN N130/N131

**Branch:** `claude/trusting-faraday-34tsmg` (worktree `/workspace/ai-trading-faraday`; tip was `3a96125`).  
**Trigger:** U2 `3a970c7` **N127 EWZ_BRAZIL_STRESS FAIL_T** (TRIAL **466→467**). U2 IDLE. Formal OPEN screens were N128/N129.

### U2 result (binding)
| ID | Verdict | t / NW | Train mean | Test | Trial |
|----|---------|--------|------------|------|-------|
| N127 EWZ_BRAZIL_STRESS | FAIL_T (cost+stress PASS) | **0,57 / 0,50** | +3,54 (N=208; netto +2,76; med +1,89; years +18,36/−2,23/+5,62; L/S 86/122) | +1,85 (N=85) | **466→467** |

Dead += N127. No thr-grid / EEM-EMB-EFA rewrite / EWZ clone / overnight. Live PREREG N127 **cleared**. N124/N125 not re-run.

### D-092.1 `n128_n129` (train 2021–2023; gate 2,34; session-flat US500)
| ID | Family | Config | N | mean | med | years | Verdict |
|----|--------|--------|--:|-----:|----:|-------|---------|
| N128 | BWX_INTL_TREASURY AW | BWX z120+d20 combo | **419** | **+6,63** | +8,58 | −8,07 / +8,89 / +9,55 | **PASS_may_PREREG** (L/S 96/323; stress informal PASS ≥3,51) |
| N129 | PPLT_PLATINUM AX | PPLT z40/thr1.5 stress_buy | **185** | **−2,51** | −4,87 | −14,58 / −2,22 / +1,70 | **FAIL** (L/S 93/92) |

### Geleverd
- PREREG N127 → **STOP FAIL_T**; `PREREG_FTMO_N128_BWX_INTL_TREASURY_STRESS.md` **OPEN**
- N129 STOP FAIL (geen PREREG; no PPLT/PALL rewrite)
- OPEN **N130** EQW_BREADTH AY + **N131** DXY_DOLLAR AZ (not screened this cycle)
- Catalog §9/§10; TRIAL **467**; live PREREG **N128** only

### Explicit
- No soft-pass; gate unchanged (2,34). N129 FAIL not PREREG'd.
- Parent wakes U2 ×1 (N128). Quiet to Sandro. No 2025-reserve. No other branches.


## 2026-10-03 00:10 Europe/Amsterdam — N124/N125 FAIL_T sync; N122/N123 DIAG_FAIL; N127 PASS→PREREG

**Branch:** `claude/trusting-faraday-34tsmg` (worktree `/workspace/ai-trading-faraday`; tip was `b236459`).  
**Trigger:** U2 `9f00f24` **N124+N125 FAIL_T** (TRIAL **464→466**). Manager v97 `76b90fc`: formal OPEN empty; C-038 `1a22e81` already DIAG_FAIL N122/N123 — **do not** D-092.1 them.

### U2 result (binding)
| ID | Verdict | t / NW | Train mean | Test | Trial |
|----|---------|--------|------------|------|-------|
| N124 YIELD_CURVE_2S10S | FAIL_T (cost+stress PASS) | **1,72 / 1,82** | +8,97 (N=240) | +2,89 (N=100) | **464→465** |
| N125 DEFENSIVE_CYCLICAL | FAIL_T (cost+stress PASS) | **1,22 / 1,29** | +5,48 (N=478) | −2,32 (N=191) | **465→466** |

Dead += both. No thr-grid / US100 overnight / TLT-TIP-SECTOR_DISP / yield-curve or XLU/XLI twins. Live PREREG N124/N125 **cleared**.

### C-038 absorb (not re-screened)
N122 DBC→US500 DIAG_FAIL (−6,31; N=368). N123 EFA→US500 DIAG_FAIL (−2,66; N=201). Stale OPEN text at `b236459` **removed**.

### D-092.1 `n126_n127` (train 2021–2023; gate 2,34; session-flat US500)
| ID | Family | Config | N | mean | med | years | Verdict |
|----|--------|--------|--:|-----:|----:|-------|---------|
| N126 | DBA_AG AU | DBA z120+d20 combo | **380** | **−6,36** | −4,41 | +9,26 / −15,58 / −1,35 | **FAIL** |
| N127 | EWZ_BRAZIL AV | EWZ z40/thr1.5 stress_buy | **208** | **+3,54** | +1,89 | +18,36 / −2,23 / +5,62 | **PASS_may_PREREG** |

### Geleverd
- PREREG N124/N125 → **STOP FAIL_T**; `PREREG_FTMO_N127_EWZ_BRAZIL_STRESS.md` **OPEN**
- OPEN **N128** BWX_INTL_TREASURY AW + **N129** PPLT_PLATINUM AX (not screened this cycle)
- Catalog §9/§10; TRIAL **466**; live PREREG **N127** only

### Explicit
- No soft-pass; gate unchanged (2,34). N126 FAIL not PREREG'd.
- Parent wakes U2 ×1 (N127). Quiet to Sandro. No 2025-reserve. No other branches.


## 2026-10-02 23:56 Europe/Amsterdam — Absorb S2 cycle_2346 → N124/N125 PASS→PREREG

**Branch:** `claude/trusting-faraday-34tsmg` (worktree `/workspace/ai-trading-faraday`; tip was `47e0eab`).  
**Trigger:** S2 `13fe10c` Lane-A survivors YIELD_CURVE_2S10S + DEFENSIVE_CYCLICAL (cycle_2346; COST_OK).

### D-092.1 `n124_n125` (train 2021–2023; gate 2,34; session-flat US500)
| ID | Family | Config | N | mean | med | years | Verdict |
|----|--------|--------|--:|-----:|----:|-------|---------|
| N124 | YIELD_CURVE_2S10S AS | 10Y−3M z60/thr1.5/flatten_fade | **240** | **+8,97** | +9,89 | −2,31 / +8,57 / +12,41 | **PASS_may_PREREG** |
| N125 | DEFENSIVE_CYCLICAL AT | XLU/XLI z40/thr0.5/defensive_high **US500 twin** | **478** | **+5,48** | +4,81 | +0,90 / +8,84 / +3,72 | **PASS_may_PREREG** |

### Geleverd
- `PREREG_FTMO_N124_YIELD_CURVE_2S10S.md` + `PREREG_FTMO_N125_DEFENSIVE_CYCLICAL.md` — OPEN for U2
- VOORSTEL_PRESCREEN_N124/N125; source pointers `results/lane_b/YIELD_CURVE_2S10S_SOURCE.md` + `DEFENSIVE_CYCLICAL_SOURCE.md`
- Screen artifacts `results/R2/n124_n125_prescreen/`
- Catalogus §9/§10: live PREREG N124/N125; keep OPEN N122/N123 AQ/AR; TRIAL **464**

### Explicit
- No soft-pass; gates unchanged (2,34). N125 = **US500 twin** (S2 FLAG — not US100 overnight).
- N122/N123 remain OPEN (D-094 ≥2 NEW_FAMILY OPEN screens + 2 live PREREG).
- Parent wakes U2; Quiet to Sandro. No 2025-reserve touch.

## 2026-10-02 23:25 Europe/Amsterdam — N118 FAIL_T sync; N120/N121 D-092.1 FAIL; OPEN N122/N123

**Branch:** `claude/trusting-faraday-34tsmg` (worktree `/workspace/ai-trading-faraday`; tip was `ce7ce12`).  
**Trigger:** U2 `9e928af`/`9a00524` **N118 FAIL_T** (TRIAL **463→464**). Manager v95: D-092.1 on formal OPEN N120/N121.

### U2 N118 result (binding)
| Metric | Value |
|--------|------:|
| Train | 2021–23 US500cash |
| N | 359 |
| Mean bruto | **+5,38 bp** ≥ gate **2,34** / stress **3,51** |
| Stress | PASS |
| t / NW | **0,99 / 0,99** <2 |
| Years | 2021 **−7,40** / 2022 +7,92 / 2023 +5,27 |
| Test 2024 | N=123 bruto **−4,20** |
| TRIAL_COUNT | **464** |
| Retune | **verboden**; no TIP→US500 / IEF twin / TLT rewrite; TIP≠TLT |
| Reserve 2025 | untouched |

### D-092.1 N120/N121 (`n120_n121_prescreen`)
| ID | N | Mean | Gate | Years | Verdict |
|----|--:|-----:|-----:|-------|---------|
| N120 VNQ→US500 | **342** | **−0,38** | 2,34 | +0,48/−0,00/−1,12 | **FAIL** (geen PREREG) |
| N121 EEM→US500 | **172** | **+0,08** | 2,34 | +15,33/+4,76/−8,05 | **FAIL** (geen PREREG) |

### Geleverd
- `PREREG_FTMO_N118` → **STOP FAIL_T**; live PREREG cleared; TRIAL_COUNT **464**
- VOORSTEL N120/N121 → D-092.1 FAIL; artifacts `results/R2/n120_n121_prescreen/`
- VOORSTEL **N122–N123** NEW_FAMILY AQ/AR (DBC_COMMODITY / EFA_DM_EXUS → US500 session-flat)
- Catalogus §9/§10 sync

### New OPEN screen table
| ID | Family | Instrument | Gate bp | Mechanisme |
|----|--------|------------|--------:|------------|
| N122 | AQ DBC_COMMODITY | US500cash | **2,34** | DBC z120/d20 combo → session-flat |
| N123 | AR EFA_DM_EXUS | US500cash | **2,34** | EFA z40 stress_buy → session-flat |

**Niet gedaan:** geen agent/Sandro/U2 message (Quiet; no PASS→PREREG); geen `/workspace/ai-trading` branch flip; geen 2025-reserve; geen thr-grid on N120/N121 FAIL.


## 2026-10-02 23:16 Europe/Amsterdam — N116 FAIL_T + N117 FAIL_STRESS sync; N118 PREREG; OPEN N120/N121

**Branch:** `claude/trusting-faraday-34tsmg` (worktree `/workspace/ai-trading-faraday`; tip was `754e24e`).  
**Trigger:** U2 `d0aa317` **N116 FAIL_T** (TRIAL **462→463**) + U2 `d8b97d0` **N117 FAIL_STRESS** (TRIAL blijft **463**). Manager v94: D-092.1 on formal OPEN N118/N119.

### U2 N116 result (binding)
| Metric | Value |
|--------|------:|
| Train | 2021–23 US500cash |
| N | 386 |
| Mean bruto | **+6,01 bp** ≥ gate **2,34** / stress **3,51** |
| Stress | PASS |
| t / NW | **1,16 / 1,17** <2 |
| Years | 2021 **+3,39** / 2022 +9,62 / 2023 +1,92 |
| Test 2024 | N=124 bruto **+3,46** |
| TRIAL_COUNT | **463** |
| Retune | **verboden**; no TLT→US500 / IEF twin / TIP rewrite; TIP≠TLT |
| Reserve 2025 | untouched |

### U2 N117 result (binding)
| Metric | Value |
|--------|------:|
| Verdict | **FAIL_STRESS** (cost PASS) |
| N | 152 |
| Mean bruto | **+2,89** ≥2,34 but **< 3,51** stress |
| Median | **−2,21** |
| Years | +0,52 / +11,84 / −5,56 |
| TRIAL_COUNT | **463** (geen trial) |
| Retune | **verboden**; no CPER→US500 / CuAu / copper CFD |

### D-092.1 N118/N119 (`n118_n119_prescreen`)
| ID | N | Mean | Gate | Years | Verdict |
|----|--:|-----:|-----:|-------|---------|
| N118 TIP→US500 | **359** | **+5,38** | 2,34 | −7,40/+7,92/+5,27 | **PASS→PREREG** |
| N119 IWM→US500 | **186** | **−0,48** | 2,34 | +14,29/−1,04/−3,20 | **FAIL** (geen PREREG) |

### Geleverd
- `PREREG_FTMO_N116` → **STOP FAIL_T**; `PREREG_FTMO_N117` → **STOP FAIL_STRESS**; live PREREGs cleared; TRIAL_COUNT **463**
- `PREREG_FTMO_N118_TIP_REALRATE_STRESS` **OPEN** (TIP≠TLT)
- VOORSTEL **N120–N121** NEW_FAMILY AO/AP (VNQ_REIT / EEM_EM_EQUITY → US500 session-flat)
- Catalogus §9/§10 sync; artifacts `results/R2/n118_n119_prescreen/`

### New OPEN screen table
| ID | Family | Instrument | Gate bp | Mechanisme |
|----|--------|------------|--------:|------------|
| N120 | AO VNQ_REIT | US500cash | **2,34** | VNQ z120/d20 combo → session-flat |
| N121 | AP EEM_EM_EQUITY | US500cash | **2,34** | EEM z40 stress_buy → session-flat |

**Niet gedaan:** geen agent/Sandro/U2 message (Quiet; parent wakes U2 on N118 PASS→PREREG); geen `/workspace/ai-trading` branch flip; geen 2025-reserve; geen thr-grid on N119 FAIL.

## 2026-10-02 23:12 Europe/Amsterdam — N114 FAIL_T sync + N116/N117 PREREG + OPEN N118/N119

**Branch:** `claude/trusting-faraday-34tsmg` (worktree `/workspace/ai-trading-faraday`; tip was `f9f7bae`).  
**Trigger:** U2 tip `527e46e` — **N114 HYG_CREDIT_STRESS FAIL_T** (TRIAL **461→462**). Manager v93: D-092.1 on formal OPEN N116/N117.

### U2 N114 result (binding)
| Metric | Value |
|--------|------:|
| Train | 2021–23 US500cash |
| N | 371 |
| Mean bruto | **+3,81 bp** ≥ gate **2,34** / stress **3,51** |
| Stress | PASS |
| t / NW | **0,68 / 0,71** <2 |
| Years | 2021 **−10,03** / 2022 +7,69 / 2023 +4,82 |
| Test 2024 | N=150 bruto **−2,16** |
| TRIAL_COUNT | **462** |
| Retune | **verboden**; no HYG/LQD/EMB overnight clones; HYG≠EMB |
| Reserve 2025 | untouched |

### D-092.1 N116/N117 (`n116_n117_prescreen`)
| ID | N | Mean | Gate | Years | Verdict |
|----|--:|-----:|-----:|-------|---------|
| N116 TLT→US500 | **386** | **+6,01** | 2,34 | +3,39/+9,62/+1,92 | **PASS→PREREG** |
| N117 CPER→US500 | **152** | **+2,89** | 2,34 | +0,52/+11,84/−5,56 (med −2,21) | **PASS→PREREG** |

### Geleverd
- `PREREG_FTMO_N114` → **STOP FAIL_T**; live PREREG cleared; TRIAL_COUNT **462**
- `PREREG_FTMO_N116_TLT_DURATION_STRESS` + `PREREG_FTMO_N117_CPER_COPPER_STRESS` **OPEN**
- VOORSTEL **N118–N119** NEW_FAMILY AM/AN (TIP_REALRATE / IWM_SMALLCAP → US500 session-flat)
- Catalogus §9/§10 sync; artifacts `results/R2/n116_n117_prescreen/`

### New OPEN screen table
| ID | Family | Instrument | Gate bp | Mechanisme |
|----|--------|------------|--------:|------------|
| N118 | AM TIP_REALRATE | US500cash | **2,34** | TIP z120/d20 combo → session-flat |
| N119 | AN IWM_SMALLCAP | US500cash | **2,34** | IWM z40 stress_buy → session-flat |

**Niet gedaan:** geen agent/Sandro message; geen `/workspace/ai-trading` branch flip; geen 2025-reserve; Quiet (parent wakes U2 on N116+N117).

## 2026-10-01 12:55 Europe/Amsterdam — N78 FAIL_COST_GATE + N79–N81 NEW_FAMILY

**Branch:** `claude/trusting-faraday-34tsmg` (worktree `/workspace/ai-trading-faraday`; ff-pull `436fc9e` first).  
**Trigger:** U2 tip `b998253` (uitvoerder2-r): **N78 VIX_TERM_VOV FAIL_COST_GATE STOP**.

### U2 N78 result (binding)
| Metric | Value |
|--------|------:|
| Train | 2021–23 US100cash |
| N | 492 |
| Mean bruto | **+2,21 bp** ≪ gate **7,83** |
| Stress | FAIL |
| t | ~0,12 |
| Years | 2021 +3,43 / 2022 −8,25 / 2023 +9,21 |
| Test 2024 | info only |
| TRIAL_COUNT | **457** |
| Retune | **verboden**; no VIX_TERM_VOV clones; no softer gate |
| Reserve 2025 | untouched |

### Geleverd
- `PREREG_FTMO_N78_VIX_TERM_VOV.md` → **STOP FAIL_COST_GATE** (U2 numbers/SHA)
- Catalogus §9/§10: N78 dead; dropped from live ranking; N75–N77 remain **OPEN**; TRIAL_COUNT **457**
- VOORSTEL_PRESCREEN **N79–N81** NEW_FAMILY D/E/F (≥3; ≠ VIX_TERM_VOV / L60 FX-med / ORB / TSMOM_DIV / ENERGY / IDX_SHORT / N75–N77 mechanics)

### New OPEN screen table
| ID | Family | Instrument | Gate bp | Mechanisme |
|----|--------|------------|--------:|------------|
| N79 | D RATE_CURVE→OIL | UKOILcash | **50,00** | US10Y−US2Y steepener → LO 5d (D-100 long; D-097 floor) |
| N80 | E OIL_OVN_GAP_FLAT | UKOILcash | **8,13** | OVN gap ≥±40 → continuation; flat 17:00 CET (swap=0) |
| N81 | F EQUITY_PAIR_RV | US100+US500 | **13,74** | ratio z>1 → SO US100 / LO US500 3d (cheap swap side only) |

Train 2021–23; N≥150; gate 3×(RT[+swap]); D-094a b/c. Softs seasonality skipped (m5gz exists; **not** in COSTS_FTMO — no binding RT). Vol-timing overnight US100 avoided (N78 dead).

**Niet gedaan:** geen PREREG (geen screen PASS); geen agent/Sandro message; geen `/workspace/ai-trading` branch flip; geen 2025-reserve.

## 2026-10-01 12:42 Europe/Amsterdam — C-028 closes L60 FX-med family

**Branch:** `claude/trusting-faraday-34tsmg` (worktree `/workspace/ai-trading-faraday`; ff-pull first, already up to date).
**Trigger:** CTO C-028 binding after both medium-term FX sleeves failed formal tests: USDJPY_MED **FAIL_T**, U2 `910d6ff` (TRIAL 454→455), followed by EURJPY_MED **FAIL_T**, U2 `65a9b23` (TRIAL 455→456).

### Geleverd
- **BARRED/STOP:** N72 EURJPY_MED, N73 USDCAD L60/H10, and N74 USDCHF L60/H10; L60 FX-med family is closed, with no more pair-forks.
- Updated each `VOORSTEL_PRESCREEN_N72/N73/N74.md` status with both U2 SHAs and **TRIAL_COUNT 456**.
- Updated `STRATEGIE_CATALOGUS.md` §9/§10: USDJPY_MED + EURJPY_MED dead; N72–N74 barred; ranking drops MED sleeves; live OPEN = **N75–N77**; **TRIAL_COUNT 456**.
- Updated `STRATEGIE_LOG.md` (~12:42 CEST).

**Niet gedaan:** geen nieuwe VOORSTELs (N75–N77 already OPEN), geen PREREG, geen agent/Sandro message, geen 2025-reserve.


## 2026-10-01 12:40 Europe/Amsterdam — C-028 Lane-B NEW_FAMILY N75–N77

**Branch:** `claude/trusting-faraday-34tsmg` (worktree `/workspace/ai-trading-faraday`; ff-pull tip was `78673d0`).  
**Binding:** CTO **C-028** Lane-B — PREREGs only from Lane-A survivors OR honest-RT intradag w/ D-100; novelty ≥2/3 NEW_FAMILY; freeze further L60 FX-med forks if EURJPY_MED-style FAIL (N72–N74 stay OPEN, no N75+ as L60 FX longs). D-094 FREEZE OFF; D-094a; D-097; D-100.

### Inputs gelezen
- `STRATEGIE_CATALOGUS.md` §9/§10 tip (N72–N74 OPEN; TRIAL **454**; USDJPY_MED live PREREG).
- `COSTS_FTMO.csv` + `results/screen_cost_vol.csv`.
- `results/ceo/swap_side_map.csv` via `git show origin/claude/ftmo-trading-strategy-98mplz:...` (cached locally for reference; not required for U2).

### Geleverd (geen PREREG)
| ID | Family | Symbol(s) | Gate bp | NEW_FAMILY |
|----|--------|-----------|--------:|:----------:|
| N75 | metal ratio MR 3d | XAUUSD+XAGUSD | 30,60 | Y |
| N76 | commodity inv-window | UKOILcash | 50,00 | Y |
| N77 | vol-timed XS rank-rev 5d | FX6 majors | 46,29 | Y |

N72–N74 remain **OPEN** (L60 med); **no** more EURJPY/USDCAD/USDCHF/USDJPY L60 forks. Catalog §9/§10 + STRATEGIE_LOG updated. Train 2021–2023; N≥150; signed mean bruto; D-094a + D-100 notes in VOORSTELlen.

### Niet gedaan
- Geen `PREREG_FTMO_*` (Lane-B: no own PASS).
- Geen L60 FX pair-forks; geen dead-sleeve restart; geen 2025-reserve; Quiet (geen agent/Sandro message).

## 2026-09-30 21:41 Europe/Amsterdam — D-090 re-kickoff cyclus

**Branch:** `claude/trusting-faraday-34tsmg` (tracking `origin/claude/trusting-faraday-34tsmg`).  
**Doel cyclus:** FASE 3 FTMO — PREREG-gaps, B1/A2 stubs, catalogus §9/§10, log.

### BESLUITEN gelezen
- Bron: `git show origin/claude/upbeat-dirac-g2810q:BESLUITEN.md`
- Tail relevant: **D-083** (Doel v3 = FTMO €80k), **D-084** (reserve geschorst), **D-085** (FASE 3 FTMO-EV), **D-086** (teamacties; Strateeg = plan v4 + catalogus herordenen).
- Bestand eindigt bij D-086 (211 regels). **D-087 / D-088 / D-090** staan in `origin/main:GROK_CTO_INSTRUCTIE.md` en `NEXT_STEPS` v35, maar **nog niet** als genummerde entries in BESLUITEN op dirac → Manager/CEO: sync BESLUITEN.

### PREREG-status na cyclus
| Bestand | Status |
|---------|--------|
| `PREREG_FTMO_C17.md` (A4) | Gaps gevuld; OPEN §1a regel V-CAT1 vs V-PRE (default V-CAT1); gemeten kosten; trial/BH |
| `PREREG_FTMO_FX_INTRADAG.md` (A5) | Gaps gevuld; EURUSD-first; U3-afbakening; wacht GBP/JPY M5 |
| `PREREG_FTMO_B1.md` (B1) | **Stub** — OPEN universum / swap-vs-carry / sizing |
| `PREREG_FTMO_A2.md` (A2) | **Stub** — OPEN poortgetal / 1 variant / trial-ja-nee |

### §10 one-liner
Faraday A4/A5 run-klarer dan Strateeg-2 zolang strateeg-2 geen eigen PREREG/hypotheses heeft gecommit.

### Niet gedaan (bewust)
- Geen backtest, geen FTMO-EV-cijfers verzonnen, geen 2025-reserve, geen force-push/amend.

### Git (deze cyclus)
Commit op `claude/trusting-faraday-34tsmg` + push `-u origin`.

## 2026-09-30 22:01 Europe/Amsterdam — CTO-deblokker (Grok): train/test-freeze

**Waarom:** CTO-deblokker voor Grok Strateeg. Conflict D-030 (oudere testvenster-taal doorlopend voorbij 2024) vs D-084 (reserve geschorst) opgelost door test te krimpen.

**Bevroren vensters (PREREG_FTMO_C17 + PREREG_FTMO_FX_INTRADAG):**
- Train: 2021-01-01 … 2023-12-31 (2021–2023)
- Test: 2024-01-01 … 2024-12-31 (volledig 2024; plafond ≤ 2024-12-31)
- Reserve: 2025-01-01 → ONAANGERAAKT / UNTOUCHED (niet openen, niet gebruiken)

**Geen CEO 2025-vrijgave nodig** voor dit amendement. Geen backtest, geen 2025-data, geen trial-resultaten.

## 2026-09-30 22:08 Europe/Amsterdam — B1 PREREG bevroren (post-A4)

**Context:** A4 C17 kostenpoort FAIL (`43b6ba2`). Manager NEXT_STEPS v37: B1 eerst, A2 parallel. Strateeg-2 akkoord B1→A2; S2-M5 ná B1.

**Geleverd:** `PREREG_FTMO_B1.md` van stub → volledige freeze:
- Universe: EURUSD/GBPUSD/USDJPY/AUDUSD/USDCAD/USDCHF (NZDUSD uit)
- Regel: C05 TSMOM-mix 21/63/252 × 0,10/σ60 cap 3, maandeinde
- Kosten: COSTS_FTMO RT + swap bp/nacht-tabel; poort 3×; +50% swap-gevoeligheid
- Venster: train 2021–2023 / test 2024 / reserve 2025 ONAANGERAAKT
- Sizing: p95 dagverlies ≤ 2%; FTMO-EV via engine/ftmo.py
- ≠ B2/C12

**Niet gedaan:** geen backtest, geen A2-upgrade deze commit, geen 2025-touch.

## 2026-09-30 22:15 Europe/Amsterdam — Hourly FTMO (:10): A2 freeze + B1 poort-align + catalog §9/§10

**Branch:** `claude/trusting-faraday-34tsmg` (D-090 Strateeg).  
**Fetch/pull:** tip was `05caced` (B1 freeze); deze cyclus bouwt daarop.

### BESLUITEN (CEO `upbeat-dirac`, tail)
- D-083…D-086 bindend: FTMO-prop €80k, maatstaf FTMO-EV, reserve 2025 geschorst, SymbolList_FTMO.
- Geen nieuwere D-09x-tekst in BESLUITEN.md zelf; Manager NEXT_STEPS v38 op main verwijst D-087…D-090 + post-A4 prio.
- **A4 C17 GESTOPT** (`43b6ba2` U2): kostenpoort TRAIN FAIL — geen herstart zonder CEO.

### Geleverd
1. `PREREG_FTMO_A2.md` stub → **volledige freeze** (OR-richting, stop 10% ATR14, EOD; D-012 gemiddelde-poort; US41 RT uit `COSTS_FTMO_alle.csv` median 6,41 / mean 8,99 bp; train/test/reserve zoals CTO-freeze; FTMO-EV ≥ €80; 1 variant).
2. `PREREG_FTMO_B1.md` poort-amend: **getekend gemiddelde** bruto (NEXT_STEPS v38), niet mediaan |bruto|.
3. `PREREG_FTMO_C17.md` status → FORMEEL GESTOPT (verwijs `43b6ba2`).
4. `PREREG_FTMO_FX_INTRADAG.md` → GEPARKEERD tot M5 (v38).
5. `STRATEGIE_CATALOGUS.md` §9 A2/A4/A5/B1 statuses; §10 herschreven + sterkte-rang (S2-XAU > B1 prio-fit > A2 > …).

### Strateeg-2 vergelijking (§10c)
Sterkste *nieuwe* sleeve op kosten/distinctheid: **S2-XAU_OVERLAP**. Programma-prio blijft **B1 dan A2** (Manager). Faraday leidend voor A/B-tier; Strateeg-2 voor FDR-diversificatie.

### Niet gedaan
- Geen backtest / geen FTMO-EV-cijfers verzonnen / geen 2025-touch / geen A4-herstart.

## 2026-09-30 23:15 Europe/Amsterdam — Hourly FTMO (:10): post-A5/S2 STOP catalog sync

**Fetch:** `origin/claude/trusting-faraday-34tsmg` @ `5a66435` (fast-forward). Tip was Strateeg-log 22:50.

**BESLUITEN (origin/claude/upbeat-dirac-g2810q):** D-083 DOEL v3 FTMO €80k; D-084 reserve 2025+ geschorst; D-085 FASE 3 FTMO-EV; D-086 teamacties. Geen D-087+ in BESLUITEN.md; operationeel leidend = CEO_LOG 23:15 + NEXT_STEPS v41 (`2b2492c`).

**Uitkomsten sinds vorige cyclus (niet door Strateeg gedraaid):**
- A5 FX London-ORB kostenpoort FAIL (`ce5abdc`, median bruto −5,91 bp < 3× 3,93 bp).
- S2 XAU/GER40/USDJPY cost-gate FAIL (`7bac598`).
- B1 al STOP (`18c7996`); A4 al STOP (`43b6ba2`).
- M5gz 24 symbolen op main; **US41 equity M5 ontbreekt** → A2 geblokkeerd.

**Geleverd deze commit:**
1. `PREREG_FTMO_FX_INTRADAG.md` status → FORMEEL GESTOPT (`ce5abdc`).
2. `PREREG_FTMO_B1.md` status → FORMEEL GESTOPT (`18c7996`).
3. `PREREG_FTMO_A2.md` runtime → wacht US41-M5gz (v41 prio-1).
4. `STRATEGIE_CATALOGUS.md` §9 A2/A5/B1 + §10a–d herschreven (sterkte: A2 programma-prio; GS01 research-fit; S2-BTC/USOIL open).
5. `STRATEGIE_LOG.md` cyclusregel.

**Niet gedaan:** geen backtest; geen nieuwe PREREG; geen overnight sleeve; geen 2025-data; geen merge van U2-resultaten (alleen status-sync).

## 2026-09-30 23:55 Europe/Amsterdam — D-091 nacht: 2 niet-kloon PREREGs + GS01-erratum

**Context:** A-tier/B1 dood op kosten; CTO/Sandro: doordraaien, out-of-box, geen ORB-klonen. Screen top (lokaal `results/screen_cost_vol.csv`): US100/US30/GER40/US500/XAU.

**Geleverd:**
1. `PREREG_FTMO_N1_OPEN_FADE.md` — fade na 30-min ATR-drive (US100/US30/US500); ≠ ORB.
2. `PREREG_FTMO_N2_REL_FLAT.md` — US100↔US500 relative morning, EOD flat; ≠ ORB/richting.
3. `PREREG_GS01_ERRATUM.md` — test alleen 2024; reserve 2025 dicht (D-091.5).

**Niet gedaan:** geen backtest; wacht U2-push screen + CTO gate op S2b (Strateeg-2). U2 mag N1/N2 kostenpoort na merge/SHA.

## 2026-10-01 00:10 Europe/Amsterdam — Hourly FTMO (:10): sync post nacht-queue

**Fetch:** `origin/claude/trusting-faraday-34tsmg` @ `474a33c` (up to date). Branch confirmed Faraday (not grok/strateeg-1).

**BESLUITEN:**
- `origin/claude/upbeat-dirac-g2810q` BESLUITEN.md eindigt D-086 (FTMO-pivot).
- D-087…D-091 via `origin/claude/ftmo-trading-strategy-98mplz` + CEO_LOG / NEXT_STEPS v44.
- **D-091** (00:05 CEST): S2b BTC+ETH → cost/vol-screen → 2 non-clone PREREGs/Strateeg → CTO ambition SR×skew; GS01 test=2024; **geen Sandro-richtingvraag** (D-091.6 → D-092 na 4 cycli zonder poort+power).

**Uitkomsten sinds vorige Strateeg-commit (niet door Strateeg gedraaid):**
- A2 SIP-ORB kostenpoort FAIL (`bba5c0c`; mean +3,77 < 26,74 bp).
- N1 STOP n=0; N2 FAIL −0,84 bp; MIDDAY_VWAP FAIL n=3; **XAU_AM_FADE gate PASS** +18,70 bp maar N=12≪120 (`8c7a8e1`).
- S2b ETH leg FAIL → STOP (CTO C-005 / `18a266a`).
- TRIAL_COUNT blijft 444; reserve 2025→ onaangeraakt.

**Geleverd deze commit:**
1. `PREREG_FTMO_A2.md` status → FORMEEL GESTOPT (`bba5c0c`).
2. `PREREG_FTMO_N1_OPEN_FADE.md` / `N2_REL_FLAT.md` status → GESTOPT (`8c7a8e1`).
3. `STRATEGIE_CATALOGUS.md` §9 A2/N1/N2 + §10a–d herschreven (prio: XAU_AM_FADE > GS01 > dood).
4. C17 / FX_INTRADAG / B1 PREREGs gecontroleerd — compleet, ongewijzigd (al STOP).

**Strateeg-2 vergelijking (§10c):** enige open gate-PASS = XAU_AM_FADE (power-blokker); Faraday A/B+N dood; S2b dicht.

**Niet gedaan:** geen backtest; geen N1-retune; geen 2025-touch; geen Sandro-ping (D-091.6 verbiedt richtingvraag; geen materieel nieuw bewijs dat Sandro moet zien).

## 2026-10-01 08:05 Europe/Amsterdam — D-094 FREEZE OFF: tracks 2+4 VOORSTELs

**Branch:** `claude/trusting-faraday-34tsmg`.  
**BESLUITEN:** `origin/claude/ftmo-trading-strategy-98mplz` — **D-094** (freeze off; breed zoeken; Strateeg tracks 2+4) + **D-094a** (min 5y of schriftelijke (a)/(b)/(c)). D-093/D-092.6 stopregel ingetrokken.

**Stand:** TRIAL_COUNT **447** (ongewijzigd). Geen cost pre-screen PASS deze cyclus → **geen PREREG**. Dead set ongewijzigd (ORB/A4/A5/B1/N1–N19/…). Ranking: F2-ORB/A1 > S2-XAU_AM_FADE watch > S2-BTC > GS01.

**Geleverd:**
1. `VOORSTEL_PRESCREEN_N20.md` — status **OPEN** (D-094 lifts D-093.2); US30cash; gate **1,35 bp**; D-094a (b).
2. `VOORSTEL_PRESCREEN_N21.md` — status **OPEN**; GER40cash; gate **2,16 bp**; D-094a (b).
3. `VOORSTEL_PRESCREEN_N22.md` — **NEW track 2** UKOILcash London→NY MR; gate **8,13 bp**; ≠ S2-USOIL EIA; swap 0.
4. `VOORSTEL_PRESCREEN_N23.md` — **NEW track 4** US100cash 2d TSMOM; gate **13,68 bp** (RT+2×swap_long); ≠ B1; D-094a (b).
5. `STRATEGIE_CATALOGUS.md` §9/§10 D-094 sync; `results/screen_cost_vol.csv` gekopieerd indien ontbrak.

**Niet gedaan:** geen PREREG; geen U2/Sandro/agent-ping (parent); geen 2025-reserve; geen ORB-klonen.

## 2026-10-01 08:12 Europe/Amsterdam — D-094: N20–N23 FAIL sync + N24–N27 vervangers

**Branch:** `claude/trusting-faraday-34tsmg`.  
**Trigger:** U2 `a1756a7` op `claude/uitvoerder2-r` — D-092.1 train pre-screen **alle FAIL** vs VOORSTELs @ `f54ad28`. CTO: geen PREREG; geen dunnere UKOIL Lon-AM / 2d-TSMOM klonen.

**U2 uitslagen (train 2021–2023):**
| Code | N | mean bp | gate | uitslag |
|------|---|--------:|-----:|---------|
| N20 US30 AM→PM cont | 384 | −2,26 | 1,35 | FAIL |
| N21 GER40 afternoon fade | 234 | −2,45 | 2,16 | FAIL |
| N22 UKOIL Lon-AM fade | 345 | −1,67 | 8,13 | FAIL |
| N23 US100 2d TSMOM | 377 | +4,46 (long +10,83) | 13,68 | FAIL |

**Stand:** TRIAL_COUNT **447** (ongewijzigd; pre-screen FAIL ≠ formal trial). D-094 nog actief. Geen PREREG.

**Geleverd:**
1. VOORSTEL N20–N23 status → **geen PREREG — U2 D-092.1 FAIL** (cite `a1756a7`).
2. `STRATEGIE_CATALOGUS.md` §9/§10 FAIL-rijen + header D-094 actief + TRIAL 447.
3. **NEW** VOORSTEL_PRESCREEN_N24 (US500 lunch-fade, gate 2,34, track 2) / N25 (XAU NY-PM fade, 2,49, track 2) / N26 (XS 1d reversal basket 5, 4,83, track 4 + D-094a(c)) / N27 (AUDUSD H4 MR, 3,66, track 4).
4. RUNLOG + STRATEGIE_LOG append.

**Niet gedaan:** geen PREREG; geen agent/Sandro-ping (parent); geen 2025-touch; geen herstart N20–N23.

## 2026-10-01 09:30 Europe/Amsterdam — D-094 FAIL_T sync TRIAL453 + N46–N48

**Branch:** `claude/trusting-faraday-34tsmg` (worktree faraday; tip was `6ef46a7`).  
**Trigger:** U2 `a498a69` (N35/N36/GBPJPY FAIL_T → 451) + U2 `5b3db74` (N40 FAIL_STRESS trial 452; N41 FAIL_T NW 1,85 trial 453 → **TRIAL_COUNT 453**).

### Marked STOP FAIL_T
| ID | Uitkomst | Cite |
|----|----------|------|
| N35 | FAIL_T (t≈1,22) | `a498a69` trial 450 |
| N36 | FAIL_STRESS→FAIL_T | `a498a69` trial 451 |
| S2-GBPJPY | FAIL_STRESS→FAIL_T | `a498a69` trial 449 (catalog only) |
| N40 | FAIL_STRESS→FAIL_T | `5b3db74` trial 452 |
| N41 | FAIL_T (NW 1,85; test −4,39) | `5b3db74` trial 453 |

N44 **BARRED** (EU→US clone of dead N35/N41). N45 blijft OPEN (≠ N40/N41).

### New OPEN VOORSTELs (D-094 ≥3 non-clone; tracks 2+4)
| ID | Track | Instrument | Gate | Mechanisme |
|----|-------|------------|-----:|------------|
| N46 | 2 | EURGBP | 3,12 | Lon fix extension **fade** |
| N47 | 2 | USDCHF | 3,03 | Asia→London handoff **cont** |
| N48 | 4 | USDJPY | 7,08 | 1d TSMOM overnight (swap in gate) |

≠ N35/N36/N40/N41/GBPJPY/ORB. D-094a (b); train 2021–23; N≥150; 3×RT.

**Niet gedaan:** geen PREREG; geen U2/Sandro ping (Quiet; CTO: wake U2 only PASS→PREREG); geen 2025-reserve.

## 2026-10-01 12:47 Europe/Amsterdam — C-028 Lane-B PREREG N78 VIX_TERM_VOV

**Branch:** `claude/trusting-faraday-34tsmg`.  
**Trigger:** Strateeg-2 Lane-A promote VIX_TERM_VOV @ `b765613c` (cycle_1240; NDX vov10/combo day_t 2,91 / mean 6,80 bp ≤2024).

### Geleverd
- `PREREG_FTMO_N78_VIX_TERM_VOV.md` — OPEN awaiting U2 cost-gate / formal t
- Gate: **7,83 bp** = 3 × (RT 0,66 + 1× overnight swap_long 1,95); US100 long swap-hostile (D-100)
- Freeze: term=VIX9D/VIX3M; vov10; combo thresholds (1.0 / 1.25 / 0.90 / −0.25); hold 1d; primary US100cash only
- `results/lane_b/VIX_TERM_VOV_SOURCE.md` pointer to S2 artefacts (no CSV rewrite)
- Catalogus §9/§10: N78 live PREREG row; ranking insert above watches; N75–N77 OPEN; N72–N74 BARRED; TRIAL_COUNT **456**

### Explicit
Lane-A bruto day_t is **not** a PASS (6,80 < 7,83 gate on proxy).

**Niet gedaan:** geen agent/Sandro message; geen 2025-reserve; geen vov/threshold retune; geen L60 FX forks.
