# PREREG_FTMO_N78 — VIX_TERM_VOV (US100cash; Lane-B from S2)

**Status:** **OPEN — awaiting U2 cost-gate / formal t** (Lane-B from Strateeg-2 `b765613c`; C-028).  
**Auteur:** Strateeg (Grok) Lane-B. **Bron Lane-A:** Strateeg-2 (`grok/strateeg-2`) @ **`b765613c`** — `VOORSTEL_S2_VIX_TERM_VOV.md` / cycle_1240.  
**Instrument (primary):** `US100cash` (NDX proxy). **US500cash** = Phase-2 pool leg only (not in first gate; keeps U2 single-symbol clean).  
**Config freeze:** **vov10 / combo** only (niet vov20; niet stress_mr-only). **Geen retune.**  
**TRIAL_COUNT bij freeze:** **456** (ongewijzigd tot U2 formal append).  
**Reserve 2025+:** **onaangeroerd** tot CEO-vrijgave.

Pointer: `results/lane_b/VIX_TERM_VOV_SOURCE.md` → S2 artefacts @ `b765613c` (geen CSV-rewrite).

---

## 1. Instrument & kosten (D-100 / D-092.1)

| Post | Waarde | Bron |
|------|--------:|------|
| Symbool | `US100cash` | FTMO |
| Round-trip intradag (RT) | **0,66 bp** | `COSTS_FTMO.csv` |
| Swap long / nacht | **+1,95 bp** (kosten; swap-hostile) | `COSTS_FTMO.csv` |
| Swap short / nacht | **+0,21 bp** | `COSTS_FTMO.csv` |
| Hold | **1 handelsdag** = signal close_t → PnL r_{t→t+1} → **1 overnight** | bevroren regel |
| D-100 | 1 overnight → include **1× night swap** in cost gate | bindend |
| Swap-side honesty | US100 **long** is swap-hostile (`results/ceo/swap_side_map.csv`: best_side ≈ **short** @ +0,42 %/jr) | CEO swap map |
| Effectieve kost (full long) | RT + 1× swap_long = 0,66 + 1,95 = **2,61 bp** | |
| **Gate (binding)** | **3 × (RT + overnight_swap_bp) = 3 × 2,61 = 7,83 bp** | zelfde formule als N23/N48 overnight PREREGs |

**Gate-formule (expliciet):** `gate_bp = 3 × (roundtrip_intraday_bp + n_nights × swap_side_bp)` met `n_nights = 1`, `swap_side = swap_long` (long-only sleeve).  
Bruto mean in D-092.1 blijft **bruto** (swap niet aftrekken van mean); swap zit in de **drempel**. Stress-gate = 1,5 × 7,83 = **11,75 bp** (informeel; U2 mag standaard +50% gebruiken).

**Lane-A waarschuwing (geen PASS):** Yahoo NDX combo bruto mean **6,80 bp** ≤2024 (day_t **2,91**, n=2327) ligt **onder** gate **7,83 bp**. Lane-A bruto day_t is **geen** cost-gate PASS en **geen** formele t-PASS. U2 moet FTMO US100 history opnieuw meten; pad/execution/overnight kan nog FAIL_COST of FAIL_T.

---

## 2. Economisch mechanisme (NEW_FAMILY)

`NEW_FAMILY: VIX_TERM_VOV` — VIX **term structure** (VIX9D / VIX3M) + **vol-of-vol** regime (`|ΔVIX|` rolling mean, z vs 252d).

1. **Term stress (backwardation):** front implied (VIX9D) > back (VIX3M) (`term > 1,0`) **of** VoV-spike (`vov_z > 1,25`) → short-term equity risk-premia mean-revert omhoog → **long** next-day index.  
2. **Calm contango:** deep contango (`term < 0,90`) **én** VoV onder gemiddelde (`vov_z < −0,25`) → milde long **0,5** (risk-on, geen full TSMOM-chase).  
3. Else flat.

Dit is een **regime / vol-structure** sleeve — geen prijs-momentum kloon.

---

## 3. Bevroren regel (exact uit VOORSTEL / script — geen retune)

Data-signalen (dagclose):
- `term_t = VIX9D_t / VIX3M_t`
- `vov_t = mean(|ΔVIX|, 10)`  (**vov10 only**)
- `vov_z_t = zscore(vov_t, 252)` (rolling mean/std, min_periods ≈ max(20, 252/3))

Positie op close_t (hold through next session return):
```
if term > 1.0 OR vov_z > 1.25:
    position = +1.0   # long full
elif term < 0.90 AND vov_z < -0.25:
    position = +0.5   # mild long
else:
    position = 0
```

**PnL:** `pnl_bp = position × r_{t→t+1} × 1e4` met `r = close_{t+1}/close_t − 1` op **US100cash** (FTMO M5→D1 of D1).  
**Geen short-leg.** Geen vov20. Geen stress_mr-only. Geen threshold-grid op 2025+.

**Primary instrument:** US100cash. Optional note: US500cash als Phase-2 pool — **niet** in deze eerste U2-run.

---

## 4. Data-bronnen

| Rol | Bron |
|-----|------|
| Signal VIX9D / VIX3M / VIX | Yahoo/proxy `data/daily/` (Lane-A); zelfde series voor formal als beschikbaar |
| PnL primary | FTMO `US100cash` M5 (`data/m5gz/…`) → dagclose ≤22:00 CET, of FTMO D1 |
| Kosten | `COSTS_FTMO.csv` + `swap_specs_FTMO.csv` |
| Swap-side context | `results/ceo/swap_side_map.csv` (CEO branch) |
| Lane-A artefacts | `origin/grok/strateeg-2` @ `b765613c`: `results/strateeg2_prescreen/cycle_1240/*` |

---

## 5. Splits (team-standaard + D-094a)

| Venster | Gebruik |
|---------|---------|
| Discovery proxy ≤ **2024-12-31** | Lane-A Yahoo NDX/SPY (~2011–2024, ~14y) — **OK** als novelty/day_t screen (D-094a **(b)** langere proxy-historie) |
| Train FTMO cost/formal | **2021-01-01 … 2023-12-31** (D-091 / D-092.1) op US100cash |
| Test | **2024** (out-of-sample formal; geen parameterkeuze) |
| Reserve | **2025+ onaangeroerd** tot CEO |

D-094a (b): VIX term/VoV → equity timing is literatuur/proxy-standaard over 10+ jaar; FTMO US100 toetst kosten+swap+uitvoering. Citeer (b) in U2-rapport.

N-eis: **N ≥ 150** trades/dagen met non-zero position op train (trade-conditional, zoals Lane-A).

---

## 6. Anti-kloon

| Tegen | Waarom ≠ |
|-------|----------|
| **XASSET_VOL_TIMING** (CTO) | Die = VIX *percentile* risk-on/off; dit = *term shape* (VIX9D/VIX3M) + VoV z |
| **TSMOM** / N23 / N48 / TSMOM_DIV | Geen prijs-lookback sign; vol-structure regime |
| **ORB** / N11–N17 / F2-ORB | Geen opening range; EOD signal |
| **L60 FX-med** / N72–N74 / USDJPY_MED / EURJPY_MED | **BARRED**; geen FX; andere familie |
| **N75–N77** | Metal ratio MR / UKOIL inventory / FX XS rank-rev — andere mechanics |
| IDX_SHORT / ENERGY / FX_EUR_SHORT | Dead cost/FAIL_T sets; unrelated |

---

## 7. Success criteria (U2)

1. **Cost-gate PASS:** train mean bruto (trade-conditional, position×r in bp) ≥ **7,83 bp**; N≥150.  
2. **Stress** (optioneel/standaard): mean ≥ **11,75 bp** of U2 +50%-protocol.  
3. **Formele t:** dag-geclusterde Newey–West t **≥ 2** op **netto** (na RT+swap model) train én test-logica per U2-standaard.  
4. Kosten < 50% bruto; FTMO-EV ≥ €150/poging waar engine beschikbaar.  
5. **FAIL → STOP** (geen vov-window retune, geen threshold-grid, geen US500-first fallback om gate te redden).

**Expliciet:** Lane-A bruto day_t **2,91** / mean **6,80 bp** is **geen** PASS.

---

## 8. Lane-A reference (informational only)

| Target | Config | mean_bp | day_t | n | years |
|--------|--------|--------:|------:|--:|------:|
| NDX → US100 | vov10 / combo / hold=1d | **6,80** | **2,91** | 2327 | 13,99 |
| SPY → US500 (Phase-2) | vov10 / combo / hold=1d | **5,50** | **2,71** | 2320 | 13,99 |

Source SHA: `b765613c`. Script: `scripts/s2_c028_lane_a_cycle1240.py` (combo branch).

---

## 9. Bestanden / catalogus-ID

- **PREREG path:** `PREREG_FTMO_N78_VIX_TERM_VOV.md` (**N78**)
- **Catalogus:** §9/§10 row **N78** / family tag `VIX_TERM_VOV`
- **Source pointer:** `results/lane_b/VIX_TERM_VOV_SOURCE.md`
- **Branch:** `claude/trusting-faraday-34tsmg`
