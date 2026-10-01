# C-028 — Edge-search upgrade (Lane A/B + novelty quota)

**Time:** 2026-10-01 ~12:41 Europe/Amsterdam (CEST).  
**Branch:** `grok/cto-1`. **Trials:** **0**. Reserve 2025+: **untouched**. No spend.

## EN — Summary

Process upgrade (binding until CEO D-*): split **Lane A** (free Yahoo/proxy daily discovery, day-clustered t≥2 bruto before FTMO cost) from **Lane B** (PREREG + U2 cost gate only for survivors / honest-RT intradag). Novelty quota ≥2/3 NEW_FAMILY per Strateeg/S2 cycle; kill circuit after 5 consecutive cost-gate-PASS FAIL_T → mandatory family pivot. Roles: Strateeg-2 = Lane-A novelty; Strateeg = Lane-B PREREG; Manager enforces in NEXT_STEPS.

**Lane-A diagnostic (this cycle):** 4 NEW_FAMILY mechanisms vs dead TSMOM/ORB/FX-med on `data/daily`+FRED ≤2024.

| Family | Best day_t | Promote? |
|--------|-----------:|:--------:|
| COMMODITY_SEASONALITY (CORN_F → FTMO CORN.c) | **2.11** (n=4022, ~16y) | **yes** |
| OVERNIGHT_GAP_FADE (SPY) | 3.07 but n=45 | no (near-miss) |
| XASSET_VOL_TIMING | 1.52 | no |
| FX_CARRY_TREND_RESIDUAL | 0.13 | no |

CATTLE_F also t=3.30 but **demoted** (no FTMO PROXY_MAP symbol). Honesty: not a PASS; CORN seasonality is a Lane-B *candidate* only after honest agri RT/swap + PREREG.

## NL — Samenvatting

Proces-upgrade (bindend tot CEO D-*): **Lane A** = gratis daily discovery (Yahoo/proxy); **Lane B** = alleen survivors → PREREG + U2. Novelty-quota ≥2/3 NEW_FAMILY; kill circuit na 5× FAIL_T (cost-gate PASS). Strateeg-2 = Lane-A; Strateeg = Lane-B; Manager enforce in NEXT_STEPS.

Eén echte Lane-A screen (0 trials): **1 promote** = `COMMODITY_SEASONALITY` / CORN_F (FTMO `CORN.c`), day_t≈2.11, ≥5j. Gap-fade bijna (t≥2, te weinig trades). Geen edge-garantie.

## Files

- `EDGE_SEARCH_UPGRADE.md` (repo root)
- `board.json`, `lane_a_shortlist.csv`, family_*.csv, `scripts/c028_lane_a_screen.py`
