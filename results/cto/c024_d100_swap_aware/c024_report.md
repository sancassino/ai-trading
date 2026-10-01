# C-024 — ENERGY_TSMOM FAIL absorb + D-100 swap-aware shortlist + IDX_SHORT PREREG

- When: 2026-10-01 ~11:05 Europe/Amsterdam (CEST / UTC+2)
- Branch: `grok/cto-1`
- Reserve 2025+: **untouched**
- Trials appended: **0** (ENERGY = cost-gate STOP, not a trial)
- No FTMO signup / spend. No EINDSTAND re-nag.

## 1. ENERGY_TSMOM — CTO absorb (no `ftmo_ev`)

U2 `c1499ce` gated `PREREG_FTMO_ENERGY_TSMOM` (L20/H10 LO, UKOIL+USOIL):

| Metric (train 2010–2016) | Value |
|-------------------------|------:|
| N_trades | 209 |
| mean bruto bp | **29.08** |
| mean cost bp (RT+swap gate) | 90.69 |
| gate 3× | **272.08 → FAIL** |
| swap ≈ | 83 bp/trade (~14 cal nights × oil overnight) |
| counts_as_trial | false |
| TRIAL_COUNT | **453** unchanged |

**CTO action:** skip `recommend_scale` / `ftmo_ev`. Dead/FAIL += **ENERGY_TSMOM**.
**No clones:** no L/H grid, no HEATOIL add, no short leg, **no N59** (UKOIL L20/H10 + ATR regime = same energy long-only family).

Root cause aligns with **D-100**: overnight structure kills multi-night oil holds when swap/roll is treated honestly; 29 bp bruto ≪ 3× cost.

## 2. D-100 operationalization

CEO `615bca0` + `results/ceo/swap_side_map.csv` (166 symbols, snapshot 2026-09-30). Copied here for offline use.

**Binding PREREG checklist (CTO):**
1. Intradag-flat (swap 0) **or** overnight only on `best_side` from swap map.
2. Cost gate uses max(swap_side, 0)×nights (credits → 0); alfa = **bruto prijs**.
3. **CREDIT_TRAP** (UKOIL/USOIL/HEATOIL/UK100 long): never count swap credit as alpha; prefer other families after ENERGY FAIL.
4. Long US/EU indices pay ≈6–8 %/jr — only if bruto edge covers it with margin; prefer **short** side (≈0 to +0.4 %/jr).
5. Hold 1–2 nights only with large bruto; else design for cheap overnight or flat.

Swap-cheap shortlist (excl. crypto; best_side ≥ −2 %/jr): **75** names → `swap_cheap_shortlist.csv`.

### Family buckets (for Strateeg / S2; ≥2/3 screens on these)

- **A_index_short_regime** (n=9): US100.cash(short), AUS200.cash(short), HK50.cash(short), US30.cash(short), GER40.cash(short), EU50.cash(short)
- **B_fx_carry_positive_side** (n=23): AUDCHF(long), AUDJPY(long), EURHUF(short), AUDCAD(long), GBPCHF(long), USDSEK(long)
- **C_metal_cheap_side** (n=6): XAGAUD(short), XAGEUR(short), XAGUSD(short), XAUEUR(short), XAUUSD(short), XAUAUD(short)
- **D_commodity_non_oil_cheap** (n=9): NATGAS.cash(short), COFFEE.c(long), CORN.c(short), COTTON.c(short), SUGAR.c(short), WHEAT.c(short)

### Flags

- **N58** (AUDUSD long + USDJPY short): **SWAP_HOSTILE** — AUDUSD long pays −1.73 %/jr; USDJPY short pays −5.13 %/jr. Redesign to cheap sides (e.g. USDJPY/USDCHF/AUDCHF **long** carry+trend) or intradag-flat.
- **N59** (UKOIL L20/H10 + ATR): **BARRED** as ENERGY clone after FAIL.
- **N60** (XAGUSD 5d): OK to pre-screen; gate uses long worst-case (XAG short is cheap side).

## 3. Frozen PREREG — `PREREG_FTMO_IDX_SHORT_TSMOM.md`

D-100 direction “korte kant van indices op regime-signaal”:
- Universe: **US100.cash + US30.cash**, **short-only** when 20d momentum < 0; hold 10d
- Proxy: NDX / DJI (≥10y; D-094a b)
- Swap: short side ≈ +0.42 %/jr (nearly free); long side ~−8 %/jr avoided by design
- Not a clone of N35/N41 (intradag EU→US), ENERGY, or TSMOM_DIV
- U2: cost-gate next; no 2025+

## 4. CTO next

1. U2: gate IDX_SHORT_TSMOM (skip ENERGY re-gate / N59).
2. Strateeg: drop N59; fix N58 swap sides; keep N60; prefer family A/B screens.
3. On PASS → track-5 `ftmo_ev`. Track-3 still PAUSED.
4. No Sandro ping (no validated sleeve; no eval).

Artefacts: `swap_side_map.csv`, `swap_cheap_shortlist.csv`, `c024_board.json`, this report.
