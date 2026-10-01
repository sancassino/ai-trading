# PREREG_FTMO_N78 — VIX_TERM_VOV (US100cash; Lane-B from S2)

**Status:** **STOP FAIL_COST_GATE** — U2 `b998253` on uitvoerder2-r (formal tip; PREREG was `52a5212` from Faraday `6c9cdca`).  
**Auteur:** Strateeg (Grok) Lane-B. **Bron Lane-A:** Strateeg-2 (`grok/strateeg-2`) @ **`b765613c`** — `VOORSTEL_S2_VIX_TERM_VOV.md` / cycle_1240.  
**Instrument (primary):** `US100cash` (NDX proxy).  
**Config freeze:** **vov10 / combo** only (niet vov20; niet stress_mr-only). **Geen retune.**  
**TRIAL_COUNT:** **457** (U2 append after FAIL_COST_GATE).  
**Reserve 2025+:** **onaangeroerd.**

Pointer: `results/lane_b/VIX_TERM_VOV_SOURCE.md` → S2 artefacts @ `b765613c` (geen CSV-rewrite).

---

## U2 formal result (binding STOP)

| Metric | Train 2021–23 US100cash |
|--------|------------------------:|
| N | **492** |
| Mean bruto | **+2,21 bp** |
| Gate (binding) | **7,83 bp** |
| Verdict | **FAIL_COST_GATE** (2,21 ≪ 7,83) |
| Stress | **FAIL** |
| t (approx) | **~0,12** |
| Years | 2021 **+3,43** / 2022 **−8,25** / 2023 **+9,21** |
| Test 2024 | info only (not used for pass/fail) |
| Tip SHA | U2 **`b998253`** |
| Dead += | **N78** |
| Retune | **verboden** |

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze record

| Post | Waarde | Bron |
|------|--------:|------|
| Symbool | `US100cash` | FTMO |
| Round-trip intradag (RT) | **0,66 bp** | `COSTS_FTMO.csv` |
| Swap long / nacht | **+1,95 bp** (kosten; swap-hostile) | `COSTS_FTMO.csv` |
| Hold | **1 handelsdag** = 1 overnight | bevroren regel |
| **Gate (binding)** | **3 × (0,66 + 1×1,95) = 7,83 bp** | N23/N48 overnight formule |

Bruto mean in D-092.1 blijft **bruto**; swap zat in de **drempel**. Stress-gate informeel 1,5 × 7,83 = **11,75 bp**.

---

## 2. Economisch mechanisme (NEW_FAMILY) — archive

`NEW_FAMILY: VIX_TERM_VOV` — VIX **term structure** (VIX9D / VIX3M) + **vol-of-vol** regime. **Dead** — no VIX_TERM_VOV clones, no softer gate (CTO reinforce).

---

## 3. Bevroren regel (archive — geen retune)

```
if term > 1.0 OR vov_z > 1.25:
    position = +1.0
elif term < 0.90 AND vov_z < -0.25:
    position = +0.5
else:
    position = 0
```

**PnL:** `pnl_bp = position × r_{t→t+1} × 1e4` op **US100cash**. Geen short-leg. Geen vov20. Geen threshold-grid op 2025+.

---

## 4–8. Splits / anti-kloon / success (archive)

Train was **2021–2023**; test 2024 info; reserve 2025+ untouched. Success required mean bruto ≥ **7,83** bp + formele t — **niet gehaald**.

**Expliciet STOP:** FAIL → **geen** vov-window retune, **geen** threshold-grid, **geen** US500-first fallback, **geen** softer gate.

---

## 9. Bestanden / catalogus-ID

- **PREREG path:** `PREREG_FTMO_N78_VIX_TERM_VOV.md` (**N78** — **STOP FAIL_COST_GATE**)
- **Catalogus:** §9/§10 row **N78** dead; dropped from live ranking
- **Source pointer:** `results/lane_b/VIX_TERM_VOV_SOURCE.md`
- **Branch:** `claude/trusting-faraday-34tsmg`
- **TRIAL_COUNT:** **457**
