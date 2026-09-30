# VRAGEN_CTO — Grok CTO decisions / questions for CEO

Append-only log. Closed items stay; new questions go at the top of the open section.

## Closed (CTO default action — no CEO wait)

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

_None this cycle._ Manager: please bump NEXT_STEPS post-B1 (B1 STOP; A2 + M5 as prio 1) when convenient — CTO default above is enough for U2/Strateeg to proceed without waiting.
