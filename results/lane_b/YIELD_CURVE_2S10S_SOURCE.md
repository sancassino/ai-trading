# YIELD_CURVE_2S10S — Lane-B source pointer (C-028 / cycle_2346)

**Lane-A SHA:** `13fe10c` on `grok/strateeg-2`  
**Lane-B PREREG:** `PREREG_FTMO_N124_YIELD_CURVE_2S10S.md` — **OPEN** (session-flat)  
**Filed:** 2026-10-02 ~23:56 Europe/Amsterdam (CEST)

## Artefacts (do not rewrite; read via git show)

```
git show 13fe10c:results/strateeg2_prescreen/cycle_2346/VOORSTEL_S2_YIELD_CURVE_2S10S.md
git show 13fe10c:results/strateeg2_prescreen/cycle_2346/survivor_export.json
git show 13fe10c:results/strateeg2_prescreen/cycle_2346/prescreen_summary.json
git show 13fe10c:results/strateeg2_prescreen/cycle_2346/YIELD_CURVE_2S10S_10Y-3M-_SPY_z60_thr1_5_flatten_fade_hold_5d_daily.csv
git show 13fe10c:results/strateeg2_prescreen/cycle_2346/family_yield_curve_2s10s.csv
git show 13fe10c:results/strateeg2_prescreen/cycle_2346/lane_a_shortlist.csv
```

## Frozen config (Lane-B)

- Signal: 10Y−3M slope z60 / thr1.5 / flatten_fade (short if z>+1.5; long if z<−1.5)
- Trade: US500cash **session-flat** 15:30→21:00 CET (D-100); gate **2,34** bp
- Signal-only curve (no TLT/IEF/TIP CFD leg)
- Lane-A: day_t 2.53 / mean 28.93 / net after drag 21.37 COST_OK (hold=5d overnight proxy)
- D-092.1 Faraday: N=240 mean +8.97 ≥ 2.34 → PASS_may_PREREG
