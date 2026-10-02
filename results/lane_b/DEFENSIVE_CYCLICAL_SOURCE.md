# DEFENSIVE_CYCLICAL — Lane-B source pointer (C-028 / cycle_2346)

**Lane-A SHA:** `13fe10c` on `grok/strateeg-2`  
**Lane-B PREREG:** `PREREG_FTMO_N125_DEFENSIVE_CYCLICAL.md` — **OPEN** (US500 twin session-flat)  
**Filed:** 2026-10-02 ~23:56 Europe/Amsterdam (CEST)

## Artefacts (do not rewrite; read via git show)

```
git show 13fe10c:results/strateeg2_prescreen/cycle_2346/VOORSTEL_S2_DEFENSIVE_CYCLICAL.md
git show 13fe10c:results/strateeg2_prescreen/cycle_2346/survivor_export.json
git show 13fe10c:results/strateeg2_prescreen/cycle_2346/prescreen_summary.json
git show 13fe10c:results/strateeg2_prescreen/cycle_2346/DEFENSIVE_CYCLICAL_XLU_XLI-_SPY_z40_thr0_5_defensive_high_hold_5d_daily.csv
git show 13fe10c:results/strateeg2_prescreen/cycle_2346/DEFENSIVE_CYCLICAL_XLU_XLI-_NDX_z40_thr0_5_defensive_high_hold_5d_daily.csv
git show 13fe10c:results/strateeg2_prescreen/cycle_2346/family_defensive_cyclical.csv
git show 13fe10c:results/strateeg2_prescreen/cycle_2346/lane_a_shortlist.csv
```

## Frozen config (Lane-B)

- Signal: XLU/XLI z40 / thr0.5 / defensive_high (short if z>+0.5; long if z<−0.5)
- Trade: **US500cash twin** session-flat 15:30→21:00 CET (D-100); gate **2,34** bp — **not** US100 overnight (S2 FLAG)
- Signal-only sector relative (no XLU/XLI CFD leg)
- Lane-A best: NDX day_t 2.08 / mean 19.75 COST_OK; US500 twin day_t 2.02 / mean 16.48 COST_OK
- D-092.1 Faraday US500 twin: N=478 mean +5.48 ≥ 2.34 → PASS_may_PREREG
