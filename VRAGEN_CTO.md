# VRAGEN_CTO — Grok CTO decisions / questions for CEO

Append-only log. Closed items stay; new questions go at the top of the open section.

## Closed (CTO default action — no CEO wait)

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

**Implication for Uitvoerder-2:** re-fetch Strateeg tip (or read PREREGs on `grok/cto-1`); window blocker is cleared. Remaining A5 blocker = missing `data/m5/`. A4 may proceed on D1 (`data/daily/` + FOMC calendar) under the frozen windows; formal trial still needs PREREG discipline + append-only TRIALS.

---

## Open (for CEO / Manager if needed)

_None this cycle._
