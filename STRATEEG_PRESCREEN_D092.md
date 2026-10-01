# Strateeg D-092.1 pre-screens — 2026-10-01 ~02:25 Europe/Amsterdam

**Branch:** `claude/trusting-faraday-34tsmg`  
**Regel:** mean bruto (train 2021–2023) ≥ 3× RT → anders **geen PREREG**. Reserve 2025→ onaangeraakt. Geen test-window peeks voor selectie.

## Context
- C-007 drained: N6 / GER_US_LEAD / VWAP_PB = FAIL STOP (`741639e` / `9f5c843`).
- C-009: IB_FADE FAIL STOP (`b8cf28a` / `a416fa7`).
- S2c XAU+XAG: CTO pre-screen FAIL (pooled −2.24 bp).
- D-092 actief; 8-cyclus watch vanaf Manager v52 (0/8).
- U2 idle tot pre-screened non-clone PREREG.

## Screens deze cyclus

| Idee | Universum | N (train) | mean bruto | gate 3×TW-RT | Uitkomst |
|------|-----------|----------:|-----------:|-------------:|----------|
| N7 PLM (ochtendimpuls → 17:30–20:00 hold) | US30+US100 | 595 | −2.60 bp | 1.69 bp | **FAIL — geen PREREG** |
| N7 NR7→ORB (Crabel compression) | US30+US100 | 198 | −2.57 bp | 1.61 bp | **FAIL — geen PREREG** |
| N8 Failed-OR fade | US30+US100 | 1131 | −3.14 bp | 1.62 bp | **FAIL — geen PREREG** |
| GS01 rule (gap≥0.20% long-only ORB) diagnostic | US30+US100+US500+GER40 | 718 | −0.38 bp | 1.92 bp | **FAIL pooled** |

### GS01 note (diagnostic, geen cherry-pick)
- GER40-leg alleen: N=156, mean **+6.21 bp** ≥ gate 2.16 → zou solo passen.
- US-legs negatief. **Geen GER40-only PREREG** deze cyclus (post-hoc selectie verboden na pooled zien).
- Implicatie §10: GS01 als *gepoold* research-fit is **verzwakt** t.o.v. eerdere ranking; formele U2-gate nog steeds open voor eigenaar `grok/strateeg-1` + erratum, maar verwachting = FAIL.

## Artefacts
- `scripts/n7_plm_prescreen.py`
- `results/strateeg_prescreen/n7_plm/`
- `results/strateeg_prescreen/n7_nr7orb/`
- `results/strateeg_prescreen/n8_failed_or_trades.csv`
- `results/strateeg_prescreen/gs01_prescreen_trades.csv`
- `results/strateeg_prescreen/multi_prescreen.json`

## Besluit
Geen nieuwe PREREG deze cyclus. Catalogus §9/§10 bijgewerkt naar C-007/C-009/D-092 realiteit. TRIAL_COUNT ongewijzigd (**444**). Geen Sandro-ping.


---

## Follow-up (C-010 / C-011 — 2026-10-01 ~03:10)

| Idee | Bron | Uitkomst (CTO/Manager, geen herberekening hier) |
|------|------|--------------------------------------------------|
| XAU N7 Pre-London BO | `VOORSTEL_PRESCREEN_N7.md` | **FAIL** C-010 `fc974de` (−1,18 bp) — geen PREREG |
| XAU N8 Post-AM-Fix cont. | `VOORSTEL_PRESCREEN_N8.md` | **FAIL** C-010 `fc974de` (−1,47 bp) — geen PREREG |
| N9 GER40 Ochtend-Fade | `VOORSTEL_PRESCREEN_N9.md` | mean-PASS +4,32≥4,20 maar **N=61≪150 → NO PREREG** (C-011 `01d93b7`) |
| N10 XAU Mid-London Fade | `VOORSTEL_PRESCREEN_N10.md` | **FAIL** C-011 `01d93b7` (−0,82 < 2,49) — geen PREREG |
| S2-LUNCH_OPEN (Strateeg-2) | `PREREG_S2_LUNCH_OPEN` / U2 `2a4f28e` | D-092.1 PASS → gate PASS → formal **FAIL_T**; TRIAL_COUNT **445**; watch reset **0/8** |

Geen nieuwe Faraday-PREREG. Volgende non-clone alleen na D-092.1 PASS met verwachte N≥150.
