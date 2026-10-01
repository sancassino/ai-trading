# VOORSTEL_PRESCREEN_N81 — US100/US500 equity-pair RV 3d (NEW_FAMILY F; D-094a c / D-100)

**Status:** **OPEN** — awaiting D-092.1 (**D-094** + **C-028** replace cycle after N78 FAIL_COST_GATE; filed 2026-10-01 ~12:55 CEST).  
**Auteur:** Strateeg (Grok).  
**Instrumenten:** `US100cash` + `US500cash` (pair legs; RT **0,66** + **0,78** = **1,44** bp).  
**NEW_FAMILY F:** equity **pair relative-value / ratio MR** (EOD 3d) — ≠ N2 morning relative intradag, ≠ N26 XS1d basket5, ≠ N30 XS5d momentum, ≠ VIX_TERM_VOV single-index overnight.

**Track 4 + D-100:** hold 3 handelsdagen = **2 nachten**. Swap **in gate**; no swap-credits as alfa.

**Swap sides (COSTS_FTMO):**  
US100 long **1,95** / short **0,21**; US500 long **1,36** / short **0,81**.  
Long-US100/short-US500 night = 1,95+0,81 = **2,76** bp.  
Short-US100/long-US500 night = 0,21+1,36 = **1,57** bp.  
→ **Allowed overnight side = short US100 / long US500 only** (cheaper; mirrors N75 one-side lock). When ratio signal wants the hostile side → **flat** (no trade).

**Gate (D-100):**  
cost = 1,44 + 2 × 1,57 = **4,58** bp → gate 3 × 4,58 = **13,74** bp.

**D-094a:** train 2021–2023. Reden **(c)**: twin-index relative value (NDX vs SPX) is a multi-leg RV sleeve with shared US-equity factor stripped; literature on sector/style relative mean-reversion. FTMO-M5 both legs. Herhaal in PREREG.

**Onderscheid:**
- ≠ **N2** US100↔US500 **morning** relative FAIL (intradag sync; other horizon)
- ≠ **N26** XS 1d reversal basket5 FAIL; ≠ **N30** XS 5d **momentum** FAIL
- ≠ **N23 / N52** US100 solo TSMOM FAIL/underpowered
- ≠ **N78 VIX_TERM_VOV** dead (geen VIX; pair RV not vol-structure; not overnight long-only US100)
- ≠ **N75** metal ratio; ≠ **N77** FX XS; ≠ IDX_SHORT; ≠ L60 FX-med; ≠ ORB

## Regel
1. `R_t = close_US100_t / close_US500_t` (dagclose ≤22:00 CET).
2. `z_t = (ln R_t − mean_20(ln R)) / std_20(ln R)` (min 20 prior days).
3. Signal: `z_t > +1,0` → **SHORT US100 + LONG US500** next close (US100 rich vs US500 → expect ratio down).  
   `z_t < −1,0` → **flat** (hostile long-US100/short-US500 overnight barred under D-100).
4. Hold: exit close_{t+3} (**2 nachten**). **Non-overlapping**.
5. PnL bruto bp = 0,5 × (US100_short_bp + US500_long_bp) equal €-notional.

## Pre-screen
- Data: `data/m5gz/US100cash.csv.gz` + `US500cash.csv.gz` → dagclose; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **13,74** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N81. FAIL → STOP (geen z-grid, geen bilateral hostile side, geen GER40 substitute).
