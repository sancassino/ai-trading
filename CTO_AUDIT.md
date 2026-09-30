# CTO_AUDIT — ORB / S3 + post-A4/B1 FTMO redirect

**Status:** written 2026-09-30 22:30 Europe/Amsterdam (CTO wake).  
**Branch:** `grok/cto-1`. **No reserve 2025-01→ opened. No new TRIALS. No fabricated backtests.**  
**Engine:** `engine/ftmo.py` blob `ac7abef6` (p_survive right-censor; U2 re-validated PASS @ `18c7996`).

---

## 1. Executive finding (bindend voor FASE 3 prioriteit)

1. **Overnight / multi-night sleeves fail FTMO CFD cost gates.**  
   - **A4 C17** (FOMC index overnight): kostenpoort TRAIN FAIL → STOP (`43b6ba2`).  
   - **B1 TSMOM-mix FX6** (maand-hold ≈22 nachten): signed mean bruto **−16.94 bp** vs 3× mean cost **36.05 bp** → STOP (`18c7996`, TRIAL_COUNT 444).  
   Pattern: swap/overnight drag on FTMO CFDs kills monthly / multi-night rules before `ftmo_ev()` matters.

2. **Index-ORB (F2 / B4a) under honest `ftmo_ev()` is far below €800–900/m.**  
   Reassessment on existing MT5 daily series `results/f/F2_ORB_daily.csv` (1/7 equity per trade base; not a new trial):

   | scale (× base 1/7) | max dip | p95 dip | p_pass_2 | p_survive† | net_ev €/m | p(net&lt;0) |
   |---:|---:|---:|---:|---:|---:|---:|
   | 1.0 | 1.42% | 0.46% | 18% | ~100%* | **−5** | 85% |
   | 1.4 | 1.99% | 0.65% | 40% | 98% | **+40** | 65% |
   | 2.0 | 2.84% | 0.92% | 62% | 89% | **+138** | 45% |
   | 2.8 | 3.98% | 1.29% | 79% | 67% | **+286** | 30% |
   | 3.5 | 4.97% | 1.61% | 87% | 50% | +419 | 23% |
   | 5.0 | 7.10% | 2.31% | 94% | 18% | +503 | 21% |

   † After right-censor of incomplete funded lives. \*At scale 1 most “survivals” are censored incompletes (few eligible).  
   **D-016 / D-085 sizing:** do not recommend scale that pushes max daily loss above ~4% (static rule is 5%). Soft bind for EV claims: p95 daily dip ≤ 2% → scale ≈ **1.4 → ~€40/m**. Ceiling at max dip ≈4% → scale ≈ **2.8 → ~€286/m** — still **far below €800–900**.  
   **−50% drift** at scale 2.8 → ~€38/m.  
   Old Q1b “≈ €484/m at 5×” used rule-breaching size (max dip ~7%) and looser survival accounting — **not** a plan number under FASE 3.

3. **Implication:** even if ORB edge were real, FTMO-EV at compliant size does not hit ambition. Need (a) confirmed larger bp/trade intradag edges, (b) more concurrent uncorrelated intradag sleeves, or (c) goal/fee assumptions revised by CEO — not more overnight TSMOM/FOMC variants.

---

## 2. ORB / S3 audit (Phase-1 survivor)

### 2.1 Rule freeze (B4a / F2)

- `b4_sim.run_orb`: OR = first **30 min** cash session; buy/sell-stop OCO on OR high/low; stop = opposite side; flat at session close; 1 trade/day/symbol.  
- Symbols (FTMO CFD): US500, US100, US30, GER40, UK100, XAUUSD, EURUSD (B4); S3 confirmation set = US500/US100/GER40/XAU (no US30 in long HistData).  
- **Swap = 0** (intraday flat) — structurally preferred after A4/B1 fails.  
- MT5 EA `ORBSleeve.mq5` reconciles Python B4a (F2: N≈9414 vs 9249, +1.76 vs +1.73 bp/trade).

### 2.2 Evidence quality (already in RUNLOG — not re-run)

| Claim | Number | Status |
|---|---|---|
| Trade-level t (B4a, 7 sym) | 2.93 | Inflated by same-day multi-symbol |
| **Day-clustered t** (7 sym) | **1.81** (train 1.67 / test 0.81) | Binding inferentie |
| Day-clustered t (S3-set 4 sym) | 2.90 | Better set; still 2021–26 only |
| Plateau (F4) | 30-min OR + EOD exit = **PIEK** | Fragile to OR length / exit |
| Cross-instrument (F5) | 0/8 breadth | US/GER only |
| Cost stress (G1) | +50% spread + 1 pt slip → SR 0.91→0.66 | Edge cost-sensitive |
| S1b noise ORB-corr | ρ≈0.52 | Same family risk |

**Label:** ORB = *candidate profile* (daily flat, positive skew +1.5) but **unconfirmed** outside 2021–26; day-clustered evidence weak; post-2023 decay visible in test-t.

### 2.3 S3 status (PREREG_S3.md)

- **Frozen** (D-029/D-036): confirm if day-clustered t ≥ **2.0** (one-sided) + both halves + + ≥0.9 bp/trade + ≥2/3 indices +; labels blijvend/vervallen vs FTMO 2021–26.  
- SHA-256 (RUNLOG): `bfd755b827c31fbf22896e7cefaf2f5ea900afdd3ada53002462272e5deb1a19`.  
- **Blocked:** `data/long_m1/` empty / incomplete — needs Sandro HistData (DATA_REQUEST_SANDRO.md opt B, years **2011–2020** only per D-001 update) or Dukascopy P0 (slow/throttled).  
- NEXT_STEPS v38: **A1 skip without Sandro data (no ping)**. CTO agrees — do not spam Sandro; S3 stays parked until data lands.  
- S3b (high-vol filter): secondary; 2021–26 does not support vol-regime hypothesis.

### 2.4 FTMO-EV vs A1 viability

- A1 = index-ORB path. Under §1 table: **not FTMO-ambition-viable at compliant scale**, even granting 2021–26 edge.  
- Still the best *profile* found (flat + skew). Worth S3 when data exists — as **kill/keep of the only Phase-1 survivor**, not as near-term €900 plan.  
- Do **not** combine with RSI(2) overnight for challenge sizing (S8/U2b: RSI dips kill daily-loss headroom).

---

## 3. Post-A4/B1 portfolio redirect (CTO default)

| Priority | Item | Owner | Note |
|---|---|---|---|
| **1** | **A2** Stocks-in-Play ORB (earnings, EOD flat, swap=0) | Strateeg PREREG frozen @ Strateeg tip; U2 when data | `PREREG_FTMO_A2.md` — needs US41 **M5** (gitignored). Spreads already on main (`COSTS_FTMO_alle.csv`). |
| **2** | **M5 path** for A2/A5/S2-* | Sandro/Debian or U-006 | See `VRAGEN_CTO.md` C-002. |
| **3** | Strateeg-2 intradag PREREGs (XAU overlap, GER40 open, USOIL EIA, BTC US open) | Strateeg-2 | After/with M5; overnight holds disfavored unless swap-positive by design. |
| — | A4 / B1 | — | **STOP** — no restart without CEO. |
| — | A5 FX intradag | U2 | Parked until M5. |
| — | A1 / S3 | — | Parked until `data/long_m1/`. |
| — | New overnight monthly FX/index | Strateeg | **Deprioritize** until a sleeve shows signed train bruto ≫ 3× (RT+swap) *before* PREREG freeze. |

---

## 4. Engine notes

- `ftmo_ev` API stable; U2 P1 PASS on censor fix.  
- ORB grid above: informational reassessment of published F2 series — **not** a PREREG trial; do not append TRIALS.  
- Next engine work (later wake): optional CLI `--scale-grid` + JSON emit for sleeve EV tables; not blocking.

---

## 5. Pointers

- PREREG: `PREREG_S3.md`, `PREREG_FTMO_A2.md` (Strateeg), `PREREG_FTMO_B1.md` (landed U2), `PREREG_FTMO_C17.md`  
- Results: `results/f/F2_ORB_daily.csv`, `results/r3/ORB_frontier.txt`, `results/R2/b1_prep/cost_gate_b1_train.*`  
- Decisions: `VRAGEN_CTO.md` C-001 (windows), C-002 (post-B1 + M5)
