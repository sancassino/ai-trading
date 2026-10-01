# C-025 — IDX_SHORT FAIL absorb + D-100 family diag + FX_EUR_SHORT PREREG

- When: 2026-10-01 ~11:35 Europe/Amsterdam (CEST / UTC+2)
- Branch: `grok/cto-1`
- Reserve 2025+: **untouched**
- Trials appended: **0** (IDX_SHORT = cost-gate STOP, not a trial)
- No FTMO signup / spend. No EINDSTAND re-nag.

## 1. IDX_SHORT_TSMOM — CTO absorb (no `ftmo_ev`)

U2 `72f40d3` gated `PREREG_FTMO_IDX_SHORT_TSMOM` (L20/H10 SO, US100+US30):

| Metric (train 2010–2016) | Value |
|-------------------------|------:|
| N_trades | 177 |
| mean bruto bp | **−66.22** |
| mean cost bp (RT+swap gate) | 2.04 |
| gate 3× | **6.13 → FAIL** |
| counts_as_trial | false |
| TRIAL_COUNT | **453** unchanged |

**CTO action:** skip `recommend_scale` / `ftmo_ev`. Dead/FAIL += **IDX_SHORT_TSMOM**.
**No clones:** no L/H grid, no US500/GER40/HK50 add, no long-leg, **no N68** (GER40 short-only TSMOM = family A).

Root cause: equity upward drift. D-100 cheap overnight short side is necessary but not sufficient — bruto expectatie already deeply negative.

## 2. D-100 family diagnostic (proxy ≤2024; 0 trials)

CTO ran a non-binding L20/H10 screen on C-024 families A/B/C after the FAIL (see `c025_family_diag.csv`).

| Bucket | Finding |
|--------|---------|
| **A index-short** | IDX_SHORT FAIL; DAX short diag −47 bp → **BAR family A overnight short-TSMOM** (N68 BARRED) |
| **B AUD* long carry** | AUDCHF/AUDJPY/GBPCHF/USDCHF/USDJPY long train means **negative** → no PREREG; **N67 DIAG_FAIL** |
| **B EUR short carry** | EURUSD short +21 / EURAUD short +16; **pooled N=226 mean +18.6 bp**, h1/h2 both >0 → **freeze PREREG** |
| **C metal short** | SILVER_F short −39 bp; N60 XAG already FAIL → no metal short PREREG |

Caveat: EURUSD/EURAUD year skew (2011/2013 negative); EURAUD test mean −10 bp. Prior = moderate. Diagnostic ≠ formal gate.

## 3. Frozen PREREG — `PREREG_FTMO_FX_EUR_SHORT_TSMOM.md`

D-100 family B (FX cheap overnight short sides) with positive diagnostic bruto:
- Universe: **EURUSD + EURAUD**, **short-only** when 20d momentum < 0; hold 10d
- Proxy: `FX_EURUSD` + BIS cross AUD/EUR (≥10y; D-094a b)
- Swap: short sides earn/flat per `swap_side_map` (credits → 0 in gate); alfa = bruto prijs
- Not a clone of IDX_SHORT / ENERGY / N58 / B1 / A5
- U2: cost-gate next; no 2025+

## 4. Flags for Strateeg / S2 / Manager

- **N68 BARRED** (IDX_SHORT family A).
- **N67** drop (USDJPY long L20/H10 diag FAIL).
- **N66** subsumed into FX_EUR_SHORT PREREG (optional keep as note; do not dual-gate).
- Family A overnight index-short TSMOM **closed**. Prefer intradag-flat or other B/C/D with **positive** proxy bruto before PREREG.

## 5. CTO next

1. U2: gate `PREREG_FTMO_FX_EUR_SHORT_TSMOM` (`scripts/fx_eur_short_tsmom_gate.py`).
2. On PASS → track-5 `ftmo_ev`. Track-3 still PAUSED.
3. No Sandro ping (no validated sleeve; no eval).

Artefacts: `c025_board.json`, `c025_family_diag.csv`, this report.
