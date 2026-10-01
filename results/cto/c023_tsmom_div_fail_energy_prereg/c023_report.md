# C-023 — TSMOM_DIV FAIL absorb + energy-TSMOM PREREG (D-098/D-099)

- When: 2026-10-01 ~10:32 Europe/Amsterdam (CEST / UTC+2)
- Branch: `grok/cto-1`
- Reserve 2025+: **untouched**
- Trials appended: **0** (TSMOM_DIV = cost-gate STOP, not a trial)
- No FTMO signup / spend. No EINDSTAND re-nag.

## Inputs

| Source | Tip / path |
|--------|------------|
| main NEXT_STEPS | **v70** `1f6b53f` (D-098 TSMOM_DIV + C-022) |
| CEO | `76ec6ed` **D-099** (+ erratum on TSMOM_DIV) |
| U2 | **`e5d23c5`** TSMOM_DIV `FAIL_COST_GATE` |
| C-022 | `de97468` / `results/cto/c022_d097_proxy_tsmom/` |

## 1. TSMOM_DIV — CTO absorb (no `ftmo_ev`)

U2 froze universe n=56 and ran PREREG §4.1 cost-gate on train 2008–2016:

| Metric (train) | Value |
|----------------|------:|
| mean bruto bp/unit-trade | **−5.73** |
| mean cost bp (RT+swap) | 45.12 |
| mean nights / trade | ≈29 |
| gate 3× | **FAIL** |
| klassen netto + | 0/4 |
| counts_as_trial | false |

**CTO action:** skip `recommend_scale` / `ftmo_ev` (PREREG: faalt poort → STOP). Dead/FAIL += **TSMOM_DIV** (no clones: no lookback tweak, no post-hoc universe shrink).

### Root cause (class decomp, train month-trades)

| klasse | n | mean bruto bp | mean cost bp | mean nights |
|--------|--:|-------------:|-------------:|------------:|
| energie_agri | 1169 | −39.1 | 104.7 | 28.8 |
| fx | 2354 | −0.4 | 16.1 | 28.8 |
| indices | 1494 | +3.4 | 37.0 | 28.8 |
| metalen | 945 | +7.8 | 56.5 | 28.8 |

Monthly L/S hold ≈29 nights → FTMO overnight swap dominates; diversified 12-1 unit bruto is already ≤0 on energy/FX. This is a **cost/structure** kill, not a near-miss t-fail.

## 2. Energy-TSMOM PREREG (D-099 unblock)

D-099 orders Strateeg to write energy-TSMOM. To keep cadans (D-094), CTO freezes the rule on `grok/cto-1` as `PREREG_FTMO_ENERGY_TSMOM.md` for U2 to gate next.

Frozen (from C-022 diagnostic, disclosed forking path):

- Symbols: **UKOIL.cash**, **USOIL.cash** (equal risk; HEATOIL deferred — fallback costs only)
- Mode: **long_only**
- Lookback **20d**, hold **10d**, enter next session close
- Gate metric = **price bruto** (swap credit reported separately; not alpha)
- Windows: proxy train/test ≤2024-12-31; reserve 2025+ untouched until CEO

C-022 reference row (diagnostic only): UKOIL L20/H10 long_only — bruto≈117 bp, t_net≈3.6, both halves >0; USOIL same rule bruto≈61 bp, t_net≈2.3 (h1 weaker).

## 3. CTO next

1. U2: gate `PREREG_FTMO_ENERGY_TSMOM` (no 2025+).
2. On PASS → CTO track-5 `ftmo_ev` / `recommend_scale` (+50% swap stress).
3. Track-3 combine still **PAUSED**.
4. Strateeg/S2: do not re-PREREG TSMOM_DIV clones; prefer carry/RV / regime if energy fails.

## Artefacts

- `c023_board.json`
- `class_cost_decomp_train.csv`
- `energy_freeze_rows_from_c022.csv`
- `../../PREREG_FTMO_ENERGY_TSMOM.md`
