# VOORSTEL_PRESCREEN_N54 — UKOILcash Winter-Season Long Bias (D-097 commodities-seizoen)

**Status:** **geen PREREG — underpowered** Strateeg `n45_n51` (mean **101.8346** ≥ gate **50.0** maar **N=33≪150**). Geen drempel/hold-shift; zie N55/N56 pool.
**Auteur:** Strateeg (Faraday).  
**Instrument:** `UKOILcash` (RT **2,71**; swap_long **−5,98**).  
**Gate (long-only hold 10d in-season):** RT_eff = **2,71** → 3× = **8,13**; binding ≥ **50 bp** (C-021).  
**Mechanisme:** energie-seizoen (Nov–Mar CET) long-bias — vraag/voorraden winter; géén TSMOM-signaal (≠ N49). Hold 10 handelsdagen vanaf eerste D1-close in venster wanneer flat; max non-overlap.

**D-094a (b):** commodity seasonality literatuur + BRENT_F proxy ≥10j voor mechanisme; FTMO-M5 = kosten.

**Onderscheid:** ≠ **N49** TSMOM FAIL (seizoen ≠ momentum); ≠ **N22/N43** intradag; ≠ **CEO TSMOM_DIV**.

## Regel
- Alleen maanden **nov, dec, jan, feb, mrt** (CET month-of-day0).
- Entry: D1 close wanneer flat en maand in seizoen → LONG; exit close_{t+10}; non-overlap.
- Buiten seizoen: geen trades.

## Pre-screen
- Train 2021–2023. PASS iff mean ≥ **50 bp**, N≥150 (of N≥100 + D-094a b). FAIL → STOP (geen maand-set uitbreiden post-hoc).
