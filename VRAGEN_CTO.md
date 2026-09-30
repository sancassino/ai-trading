# VRAGEN_CTO — Grok CTO decisions / questions for CEO

Append-only log. Closed items stay; new questions go at the top of the open section.

## Closed (CTO default action — no CEO wait)

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

## Open (for CEO / Manager if needed)

_Open for Manager (not blocking):_ bump NEXT_STEPS off dead A2 — **all A-tier + S2-* STOP** (C-004); board = non-clone research + optional multi-sleeve survivor `ftmo_ev`. CEO/Sandro: no new decision required unless revising €800–900 ambition / fee €540 after full kill table. A1/`long_m1` ping stays deferred.
