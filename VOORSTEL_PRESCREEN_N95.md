# VOORSTEL_PRESCREEN_N95 — XAUUSD London-AM → NY cash continuation, session-flat (NEW_FAMILY T)

**Status:** **OPEN** — pipeline fill after N92 FAIL_T (TRIAL **458**; filed 2026-10-02 ~20:56 CEST).  
**Auteur:** Strateeg (Grok). **NEW_FAMILY T** (gold London-AM directional impulse → NY cash-session continuation — nooit als deze setup).  
**Instrument:** `XAUUSD` (RT **0,83 bp** — `COSTS_FTMO.csv`; intradag-flat = geen swap).  
**Track 2+4 + D-100:** richtingmomentum in London AM (08:00–11:00 CET) → continuer positie in NY cash window; **flat vóór nacht**.

**Gate (intradag-flat; geen swap):**  
0,83 + 0 = **0,83 bp** → gate 3 × 0,83 = **2,49 bp**.

**D-094a:** train 2021–2023. Reden **(b)**: goud liquiditeit migreert London AM → NY; directional AM impulse vaak continueert in overlapping/NY cash (Batten et al. gold microstructure / London–NY handoff literatuurlijn; FTMO-M5 = kosten). Herhaal in PREREG.

**Onderscheid:**
- ≠ **S2-XAU_AM_FADE** watch (AM **fade**/mean-reversion → flat 14:00; dit = AM **continuation** into NY)
- ≠ **N36** XAU NY-open drive cont FAIL_T (NY-only 15:30–16:00 drive; dit = London-AM signal → NY hold)
- ≠ **N12** / **N10** / **N25** XAU intradag fades
- ≠ **N82** XAG London AM-Fix Fade DIAG_FAIL (silver + fade ≠ gold + continuation)
- ≠ **N86** XAU own VoV 3d MR DIAG_FAIL (multi-day VoV ≠ session cont)
- ≠ **N78** VIX_TERM / **N92** NY-2h equity mom / ORB / L60 / UKOIL-OVN / CORN / gap-fade

## Regel
1. `P_0800` = close eerste M5 ≥ 08:00 CET; `P_1100` = close eerste M5 ≥ 11:00 CET (span ≤15 min elk).
2. `am_bp = 1e4 × (P_1100 / P_0800 − 1)`.
3. Trade only if `|am_bp| ≥ 25`.
4. **Continuation:** am_bp ≥ +25 → **LONG** at first M5 ≥ **15:30 CET**; am_bp ≤ −25 → **SHORT** at 15:30.
5. Exit: flat at **21:00 CET** same day. **No overnight.**
6. Non-overlapping (≤1/day). Geen drempel-grid op |am_bp| buiten freeze 25.

## Pre-screen
- Data: `data/m5gz/XAUUSD.csv.gz`, train **2021-01-01 … 2023-12-31**.
- Gate: mean bruto ≥ **2,49 bp**, N ≥ 150.
- PASS → PREREG_FTMO_N95. FAIL → STOP (geen fade-rewrite → S2-XAU_AM_FADE clone, geen XAG twin, geen overnight hold).
