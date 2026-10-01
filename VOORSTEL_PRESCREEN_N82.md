# VOORSTEL_PRESCREEN_N82 — XAGUSD London AM-Fix Fade (NEW_FAMILY G; D-097/D-100)

**Status:** **OPEN** — awaiting D-092.1 (**D-094** + **C-028/C-029** replace after N75–N77/N81 DIAG_FAIL; filed 2026-10-01 ~13:20 CEST).  
**Auteur:** Strateeg (Grok).  
**Instrument:** `XAGUSD` (RT **5,07** bp; swap irrelevant — **EOD flat**).  
**NEW_FAMILY G:** silver **London AM-fix extension fade**, same-day flat — ≠ XAU_AM_FADE (gold), ≠ N25 NY-PM fade, ≠ N10 Mid-London XAU, ≠ N75 ratio 3d DIAG_FAIL.

**Track 2 + D-100:** **intradag-vlak** (swap = 0).

**Gate:** 3 × RT = 3 × 5,07 = **15,21** bp. No D-097 50-floor on pure intradag.

**D-094a:** train 2021–2023. Reden **(b)**: LBMA silver AM-fix / London morning extension fade is a metals microstructure effect distinct from gold AM_FADE and from multi-day ratio MR (N75). FTMO-M5 = uitvoering. Herhaal in PREREG.

**Onderscheid:**
- ≠ **S2-XAU_AM_FADE** (gold; other metal)
- ≠ **N25** XAU NY Afternoon Fade FAIL
- ≠ **N10** XAU Mid-London Fade FAIL
- ≠ **N75** XAU/XAG ratio 3d overnight DIAG_FAIL (this = **solo silver intradag fade**)
- ≠ N31/N36/N60/N65 XAG/XAU swings; ≠ VIX_TERM / L60 FX / ORB / CORN

## Regel
1. At **08:00 CET**: record `P0` = mid of first M5 in [08:00, 08:15].
2. At **10:30 CET** (AM-fix window proxy): `ext_bp = 1e4 × (mid_1030 / P0 − 1)`.
3. Trade only if `|ext_bp| ≥ 35`.
4. **Fade:** ext_bp ≥ +35 → **SHORT**; ext_bp ≤ −35 → **LONG**. Entry = close of 10:30 signal bar.
5. Exit: flat at **13:00 CET** same day. **No overnight.**
6. Stop (formal): 1,0 × ATR14(D1 prior) from entry. Non-overlapping (≤1/day).

## Pre-screen
- Data: `data/m5gz/XAGUSD.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **15,21** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N82. FAIL → STOP (geen threshold grid, geen XAU twin, geen longer hold).
