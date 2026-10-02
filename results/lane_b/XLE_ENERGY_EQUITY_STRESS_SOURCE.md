# XLE_ENERGY_EQUITY_STRESS — Lane-B source pointer (S2 cycle_0047)

**Lane-A SHA:** `5a21939` on `grok/strateeg-2`  
**Lane-B voorstel:** `VOORSTEL_S2_XLE_ENERGY_EQUITY_STRESS.md` — **N143 STOP FAIL_CLONE** (DBC agree 0,98 cover 0,75; mean +7,86 is not a PASS)  
**Filed:** 2026-10-03 ~00:55 Europe/Amsterdam (CEST)

## Artefacts (do not rewrite; read via git show)

```
git show 5a21939:results/strateeg2_prescreen/cycle_0047/VOORSTEL_S2_XLE_ENERGY_EQUITY_STRESS.md
git show 5a21939:results/strateeg2_prescreen/cycle_0047/survivor_export.json
git show 5a21939:results/strateeg2_prescreen/cycle_0047/prescreen_summary.json
git show 5a21939:results/strateeg2_prescreen/cycle_0047/XLE_ENERGY_EQUITY_STRESS_XLE-_SPY_z40_thr1_0_fade_extreme_hold_1d_daily.csv
git show 5a21939:results/strateeg2_prescreen/cycle_0047/family_xle_energy_equity_stress.csv
```

## Frozen config (Lane-B)

- Signal: XLE level z40 / thr±1.0 / fade_extreme (short US500 if z>+1.0; long if z<−1.0)
- Trade: US500cash **session-flat** 15:30→21:00 CET (D-100); gate **2,34** bp
- **Not** overnight long US100
- Signal-only sector ETF (no XLE CFD, no oil CFD)
- Lane-A: day_t 2.29 / mean 5.41 / net after drag 3.82 COST_OK on hold=1d — **not** a Lane-B PASS
- Lane-B D-092.1 2026-10-03: N=356 mean +7.86 ≥ 2.34 but **FAIL_CLONE** of DBC z40 — no PREREG
