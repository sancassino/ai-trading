# VOORSTEL_PRESCREEN_N59 — UKOILcash TSMOM 20d→10d long-only in high-vol regime (D-097.2)

**Status:** **OPEN** — awaiting D-092.1 (**D-094** track 4 + D-097 regime; filed 2026-10-01 ~10:25 CEST).  
**Auteur:** Strateeg (Faraday).  
**Instrument:** `UKOILcash`.  
**Regime (vooraf):** alleen traden als `ATR14(D1) > median(ATR14)` over trailing 252 handelsdagen (hoog-vol; één regel, geen tuning).  
**Signal:** `ret20>0` → LONG → exit t+10; non-overlap; long-only.  
**Gate:** ≥ **50 bp** (C-021); 3×RT=8,13.  
**D-094a (b):** C-022 energy TSMOM + regime-filter D-097.2; BRENT_F proxy.

**Onderscheid:** ≠ N49 (geen regime) FAIL; ≠ N54 seizoen underpowered; ≠ N56 pool FAIL; ≠ intradag oil.

## Pre-screen
- Train 2021–2023. PASS iff mean ≥ **50**, N≥150 (of N≥100 + D-094a b). FAIL → STOP (geen ATR-percentiel retune).
