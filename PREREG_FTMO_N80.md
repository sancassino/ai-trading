# PREREG_FTMO_N80 — UKOIL overnight-gap continuation, same-day flat (NEW_FAMILY E)

**Status:** **STOP FAIL_COST_GATE** — U2 `454628f` on `claude/uitvoerder2-r` (2026-10-01 ~13:25 CEST).  
**Auteur:** Strateeg (Grok) Lane-B. **VOORSTEL:** `VOORSTEL_PRESCREEN_N80.md`.  
**Instrument:** `UKOILcash`.  
**NEW_FAMILY E:** commodity overnight gap → same-session **continuation**, flat before night.  
**Reserve 2025+:** **onaangeroerd.**  
**TRIAL_COUNT book:** **456** (**counts_as_trial=false**; geen TRIALS append; geen retune).  
**Dead += N80.** No UKOIL OVN-gap / softer-gate clones.

---

## U2 cost-gate (binding FAIL)

| Metric | Train 2021–2023 |
|--------|----------------:|
| N | **415** |
| Mean bruto (with 1,5×ATR stop) | **+7,56 bp** |
| Gate | **8,13 bp** |
| Stress (1,5 × gate) | **12,20 bp** — **FAIL** |
| Year-split | 2021 **+25,26** / 2022 **−0,46** / 2023 **−3,63** |
| Pre-screen (no-stop) | +12,26 bp (Faraday `23c3741`) — fell below gate once stop applied |
| Verdict | **FAIL_COST_GATE STOP** |
| U2 tip | `454628f` (`claude/uitvoerder2-r`) |

---

## 1. Instrument & kosten (D-100 / D-092.1)

| Post | Waarde | Bron |
|------|--------:|------|
| Symbool | `UKOILcash` | FTMO |
| Round-trip intradag (RT) | **2,71 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (EOD flat same CET day) | D-100 intradag-vlak |
| **Gate (binding)** | **3 × 2,71 = 8,13 bp** | geen D-097 50-floor op pure intradag |

Stress-gate informeel 1,5 × 8,13 = **12,20 bp**. Alfa = signed mean **bruto prijs**; geen swap-credit.

---

## 2. Economisch mechanisme (NEW_FAMILY E) — closed

Overnight inventory / news gap in energy CFDs often continues into the London–NY cash session; **same-day flat** avoids UKOIL overnight swap. Distinct from index OVN gaps (N18 FAIL_T) and from weekly Mon→Thu calendar (N76 DIAG_FAIL). **Family closed on FAIL_COST_GATE** — no retune, no softer gate, no USOIL twin.

---

## 3. Bevroren regel (archief — geen retune)

1. Prior reference: close ≤ **22:00 CET** prior session (`C_ref`).
2. At **08:00 CET** (or first M5 in [08:00, 08:15]): `gap_bp = (mid_0800 / C_ref − 1) × 1e4`.
3. Trade only if `|gap_bp| ≥ 40`.
4. **Continuation:** gap_bp ≥ +40 → **LONG**; gap_bp ≤ −40 → **SHORT**. Entry = close of signal bar.
5. Exit: flat at **17:00 CET** same day. **No overnight.**
6. Stop (formal): 1,5 × ATR14(H1) from entry; Non-overlapping (≤1 trade/day).

---

## 4. Splits / anti-kloon

- **Train:** 2021-01-01 … 2023-12-31. **Reserve 2025+:** untouched.
- ≠ **N18** US500 OVN gap cont FAIL_T; ≠ **N19** XAU gap fill; ≠ **N22** UKOIL Lon→NY **MR**; ≠ **N76** Mon→Thu; ≠ ENERGY/N49/N59 TSMOM; ≠ VIX_TERM / L60 FX / ORB.
- **Bar:** no UKOIL overnight-gap continuation clones / no softer gate (C-029 spirit + this FAIL).

---

## 5. Bestanden / catalogus-ID

- **PREREG:** `PREREG_FTMO_N80.md` (**N80** — **STOP FAIL_COST_GATE**)
- **VOORSTEL:** `VOORSTEL_PRESCREEN_N80.md`
- **Screen:** `results/R2/n80_prescreen/` (pre-screen no-stop PASS; formal+stop FAIL)
- **Catalogus-ID:** **N80**
