# PREREG_FTMO_N36 — XAUUSD NY-Open Drive Continuation (first 90 min)

**Status:** **STOP FAIL_T** — U2 `a498a69` (TRIAL_COUNT **451**).  
Cost-gate PASS (+2,80 ≥ 2,49; N=150); stress **FAIL** (drempel 3,74) → **FAIL_STRESS_then_FAIL_T**.  
**Geen herstart zonder CEO.** Dead-set += N36. Reserve 2025→ onaangeraakt.

**Auteur:** Strateeg (Claude/Grok). **Instrument:** `XAUUSD` (data `XAUUSD.csv.gz`; PREREG typo XAUUSDcash genegeerd).  
**TRIAL_COUNT bij freeze:** 448 → formal **451**.  
**SHA VOORSTEL:** `7ede6d0` / Faraday PREREG `1d5bdb2`.

---

## Instrument & kosten

- **Symbool:** `XAUUSD`
- **RT:** 0,83 bp → gate 2,49 bp; stress 3×0,83×1,5 = 3,735
- **Formal (U2 `a498a69`):** gate PASS; **stress FAIL** → FAIL_T

---

## Regel (bevroren — archief; niet herstarten)

- `drive_bp = 1e4 × (C_1600 − C_1530) / C_1530`
- `|drive| ≥ 25` → side=sign; entry 16:00; stop 1×ATR14; flat **17:00 CET**

---

## Onderscheid / anti-kloon

≠ N12 / N25 / AM_FADE / N4–N8/N31/N34. Geen stress-retune of drempel-shift.
