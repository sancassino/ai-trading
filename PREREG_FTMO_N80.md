# PREREG_FTMO_N80 — UKOIL overnight-gap continuation, same-day flat (NEW_FAMILY E)

**Status:** **OPEN** — frozen for U2 cost-gate + formal trial (**D-092.1 PASS** Strateeg Faraday 2026-10-01 ~13:20 CEST).  
**Auteur:** Strateeg (Grok) Lane-B. **VOORSTEL:** `VOORSTEL_PRESCREEN_N80.md`.  
**Instrument:** `UKOILcash`.  
**NEW_FAMILY E:** commodity overnight gap → same-session **continuation**, flat before night.  
**Reserve 2025+:** **onaangeroerd.**  
**TRIAL_COUNT book:** **456** (N78 FAIL_COST_GATE = geen trial; C-029 / U2 `40d770a`).

---

## D-092.1 pre-screen (binding PASS — vóór formal)

| Metric | Train 2021–2023 |
|--------|----------------:|
| N | **415** |
| Mean bruto | **+12,26 bp** |
| Gate | **8,13 bp** |
| Long / short n | 231 / 184 |
| Long / short mean | +9,57 / +15,64 bp |
| Verdict | **PASS_may_PREREG** |
| Artefact | `results/R2/n80_prescreen/` |

---

## 1. Instrument & kosten (D-100 / D-092.1)

| Post | Waarde | Bron |
|------|--------:|------|
| Symbool | `UKOILcash` | FTMO |
| Round-trip intradag (RT) | **2,71 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (EOD flat same CET day) | D-100 intradag-vlak |
| **Gate (binding)** | **3 × 2,71 = 8,13 bp** | geen D-097 50-floor op pure intradag (consistent N22) |

Stress-gate informeel 1,5 × 8,13 = **12,20 bp**. Alfa = signed mean **bruto prijs**; geen swap-credit.

---

## 2. Economisch mechanisme (NEW_FAMILY E)

Overnight inventory / news gap in energy CFDs often continues into the London–NY cash session; **same-day flat** avoids UKOIL overnight swap (long earn / short hostile). Distinct from index OVN gaps (N18 FAIL_T) and from weekly Mon→Thu calendar (N76 DIAG_FAIL).

---

## 3. Bevroren regel (geen retune)

1. Prior reference: close ≤ **22:00 CET** prior session (`C_ref`).
2. At **08:00 CET** (or first M5 in [08:00, 08:15]): `gap_bp = (mid_0800 / C_ref − 1) × 1e4`.
3. Trade only if `|gap_bp| ≥ 40`.
4. **Continuation:** gap_bp ≥ +40 → **LONG**; gap_bp ≤ −40 → **SHORT**. Entry = close of signal bar.
5. Exit: flat at **17:00 CET** same day (last M5 ≤17:00). **No overnight.**
6. Stop (formal): 1,5 × ATR14(H1) from entry; pre-screen omitted stop for mean bruto. Non-overlapping (≤1 trade/day).

**Explicit FAIL → STOP:** no gap-threshold grid, no USOIL twin, no overnight-hold add-on, no softer gate.

---

## 4. Splits / power / anti-kloon

- **Train:** 2021-01-01 … 2023-12-31. **Test:** 2024 (info). **Reserve 2025+:** untouched until CEO.
- **N ≥ 150** (screen: 415). Dag-geclusterde t ≥ 2,0 beide helften (formal U2).
- ≠ **N18** US500 OVN gap cont FAIL_T; ≠ **N19** XAU gap fill; ≠ **N22** UKOIL Lon→NY **MR**; ≠ **N76** Mon→Thu; ≠ ENERGY/N49/N59 TSMOM; ≠ VIX_TERM / L60 FX / ORB.

---

## 5. Success / U2 opdracht

1. Kostenpoort TRAIN: mean bruto ≥ **8,13** bp, N≥150.
2. Stress: mean ≥ **12,20** bp (informeel) of U2 standaard stress.
3. Formele trial: dag-geclusterde t ≥ 2,0 train én test-helft; beide helften mean > 0.
4. Append TRIALS alleen bij formal gate; FAIL_COST_GATE ≠ trial (C-029).
5. Bij PASS → CTO `ftmo_ev` + Auditor; bij FAIL → STOP + dead += N80 (geen retune).

---

## 6. Bestanden / catalogus-ID

- **PREREG:** `PREREG_FTMO_N80.md` (**N80** — OPEN for U2)
- **VOORSTEL:** `VOORSTEL_PRESCREEN_N80.md`
- **Screen:** `results/R2/n80_prescreen/{prescreen.json,prescreen.md,n80_trades_train.csv}`
- **Branch:** `claude/trusting-faraday-34tsmg`
