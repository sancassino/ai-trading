# PREREG_FTMO_N35 — US100cash Europe-Session Momentum → US Open Continuation

**Status:** **STOP FAIL_T** — U2 `a498a69` op `claude/uitvoerder2-r` (TRIAL_COUNT **451**).  
Cost-gate PASS (mean bruto +6,60 ≥ 1,98; N=214); stress PASS; formele dag-geclusterde t train ≈**1,22** / test ≈**0,29** → **FAIL_T**.  
**Geen herstart zonder CEO.** Dead-set += N35. Reserve 2025→ onaangeraakt.

**Auteur:** Strateeg (Claude/Grok). **Instrument:** `US100cash`.  
**TRIAL_COUNT bij freeze:** 448 → formal **450** (U2 log; lopend totaal na N36 = **451**).  
**SHA VOORSTEL:** `7ede6d0` / Faraday tip bij PREREG `1d5bdb2`.

---

## Instrument & kosten

- **Symbool:** `US100cash`
- **Round-trip (COSTS_FTMO.csv):** 0,66 bp → gate 1,98 bp
- **D-092.1 screen:** N=214, +6,60 bp → PASS (pre-formal)
- **Formal (U2 `a498a69`):** gate+stress PASS; **FAIL_T**

---

## Regel (bevroren — archief; niet herstarten)

- `eu_bp = 1e4 × (C_1500 − C_0900) / C_0900`
- `|eu| ≥ 40` → side=sign; entry 15:30; stop 1×ATR14; flat **17:00 CET**
- Max 1/dag; swap 0

---

## Onderscheid / anti-kloon

≠ N3 / N14 / N20 / ORB. Geen threshold- of window-tweaks als herstart.
