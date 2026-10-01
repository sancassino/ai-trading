# EDGE_SEARCH_UPGRADE — C-028 (bindend voor Grok-team)

**Status:** BINDEND voor Grok-team (CTO / Manager / Strateeg / Strateeg-2 / U2) tot CEO **D-*** supersedes.  
**Cycle:** C-028 · **Branch tip:** `grok/cto-1` · **When:** 2026-10-01 ~12:40 Europe/Amsterdam (CEST / UTC+2)  
**Trials this upgrade:** **0** (process + research only; geen TRIALS.csv / TRIAL_COUNT).  
**Reserve 2025+:** untouched. Geen FTMO eval / MetaApi paid / paid data.

---

## Waarom

Recente FAIL_T-reeks (o.a. IDX_SHORT, FX_EUR_SHORT, USDJPY_MED; EURJPY_MED in flight) toont **parameter-clones** van dode sleeves (L60 FX-med / ORB / classic TSMOM). Hit-rate blijft laag omdat discovery te vroeg FTMO-kosten en PREREG-discipline draagt. Deze upgrade scheidt **discovery** van **FTMO-gate** en dwingt **novelty**.

**Honesty:** geen gegarandeerde edge. Upgrade verhoogt hit-rate *odds*, niet certainty. PREREG-before-results blijft staan; dit is geen fake PASS.

---

## Lane A — discovery (Yahoo / Stooq / proxy daily)

1. **Eerst** ≥10y (soft floor ≥5y; markeer als `short` indien <5y) mechanism screens op **gratis** daily proxies:
   - Prefer free Yahoo downloads on box (`data/yahoo/`, `data/daily/`).
   - Keep **`data/PROXY_MAP_FTMO.csv`** as FTMO↔proxy map.
   - Stooq / FRED / existing repo CSVs OK. **Geen** paid feeds.
2. **Goal:** families met **day-clustered t ≥ 2 bruto** (vóór FTMO cost) op train window ≤2024-12-31.
3. **Output:** shortlist CSV under `results/cto/c028_edge_upgrade/` (en latere cycles onder `results/cto/…`). Kolommen minimaal: `family, symbols, lookback/hold, train_years, mean_bp, day_t, n_days, promote_to_lane_b, notes`.
4. **Promote-regel:** alleen rijen met `promote_to_lane_b=yes` (day_t≥2 bruto + n_days voldoende + geen dead-family clone) gaan naar Lane B.
5. Debian MT5 blijft **owner** van m5 export. Claim **geen** cloud MT5.

## Lane B — FTMO

1. Alleen Lane-A survivors (of intradag met **honest RT** kosten) → **PREREG** + U2 cost gate.
2. Geen PREREG vanuit pure parameter-clones van FAIL/dead sleeves.
3. Swap-aware **D-100** blijft gelden (cheap sides / intradag-flat waar relevant).
4. Formal trials = **U2 only**. CTO/Strateeg diagnostic screens ≠ trials.

---

## Novelty quota

- Elke Strateeg / Strateeg-2 cycle: **≥2/3** pre-screens moeten een **`NEW_FAMILY`** tag dragen die **niet** gebruikt is door enig FAIL/dead sleeve in de **laatste 30 dagen**.
- Parameter clones van dead sleeves zijn **BARRED** (geen L60 FX-med / ORB / classic TSMOM-varianten die de FAIL-cyclus herhalen).
- Manager **enforce** quota in `NEXT_STEPS` (zie VRAGEN_CTO C-028).

## Kill circuit

- Na **5 consecutive FAIL_T** die de **cost-gate PASS**den → **mandatory family pivot**.
- Geen verdere L60 FX-med / ORB-varianten die cyclen.
- Documenteer pivot expliciet in `NEXT_STEPS` (Manager) + RUNLOG/VOORSTEL referentie.
- Telling: alleen cost-gate-PASS → FAIL_T (niet FAIL_COST_GATE). Huidige streak context: FX_EUR_SHORT, USDJPY_MED (+ eerdere cost-gate-PASS FAIL_T); EURJPY_MED nog OPEN — bij FAIL_T dreigt L60 FX-med kill.

---

## Role tweak (light — geen nieuwe agents)

| Rol | Focus |
|-----|--------|
| **Strateeg-2** | **Lane-A novelty researcher** — Yahoo-first, schrijf VOORSTEL + raw screens; NEW_FAMILY tags; geen FTMO PREREG uit dode clones. |
| **Strateeg** | **Lane-B FTMO PREREG writer** — alleen van Lane-A survivors + swap-aware D-100; stop L60 FX-med clones als EURJPY sterft. |
| **Manager** | Enforce novelty quota + kill circuit in `NEXT_STEPS`; absorb `EDGE_SEARCH_UPGRADE.md`. |
| **U2** | Blijft gate OPEN PREREGs; append TRIALS alleen bij formal gate. |
| **CTO** | Process/research upgrades; diagnostic Lane-A; freeze PREREG bij survivors; **0** TRIALS append. |
| **CEO** | Optioneel latere **D-*** om dit te bevestigen/wijzigen. |

---

## Data rules

- Keep **PROXY_MAP** (`data/PROXY_MAP_FTMO.csv`).
- Prefer free Yahoo on box; existing `data/daily/` / `data/yahoo/` / FRED OK.
- Hard cut discovery ≤ **2024-12-31** (geen reserve 2025+).
- Debian MT5 = m5 export owner; **do not claim cloud MT5**.

## Integrity

- PREREG before results blijft.
- Diagnostic ≠ trial. Geen TRIAL_COUNT bump door Lane-A.
- Geen EINDSTAND / Sandro eval ping vanuit deze upgrade.
- Geen buy/open/spend (FTMO eval, MetaApi paid, paid data).

---

## Pointers

- First Lane-A diagnostic: `results/cto/c028_edge_upgrade/` (board.json, report.md, lane_a_shortlist.csv).
- RUNLOG: `RUNLOG_CTO.md` § C-028.
- Asks: `VRAGEN_CTO.md` § C-028.
